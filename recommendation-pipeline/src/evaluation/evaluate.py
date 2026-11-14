from __future__ import annotations

from typing import Dict, Iterable, List

import numpy as np
import pandas as pd


def dcg_at_k(scores: Iterable[float], k: int) -> float:
    scores = list(scores)[:k]
    if not scores:
        return 0.0
    return sum((2 ** rel - 1) / np.log2(rank + 2) for rank, rel in enumerate(scores))


def precision_at_k(actual: set, recommended: List[int], k: int) -> float:
    top_k = recommended[:k]
    if not top_k:
        return 0.0
    return len(set(top_k) & actual) / len(top_k)


def recall_at_k(actual: set, recommended: List[int], k: int) -> float:
    top_k = recommended[:k]
    if not actual:
        return 0.0
    return len(set(top_k) & actual) / len(actual)


def ndcg_at_k(actual: set, recommended: List[int], k: int) -> float:
    relevant = [1 if item in actual else 0 for item in recommended[:k]]
    idcg = dcg_at_k([1] * min(len(actual), k), k)
    if idcg == 0:
        return 0.0
    return dcg_at_k(relevant, k) / idcg


def coverage(recommended_lists: List[List[int]], total_items: int) -> float:
    all_recommended = {item for items in recommended_lists for item in items}
    if total_items == 0:
        return 0.0
    return len(all_recommended) / total_items


def diversity(recommended_lists: List[List[int]], item_categories: Dict[int, str]) -> float:
    if not recommended_lists:
        return 0.0
    diversity_scores = []
    for recs in recommended_lists:
        if len(recs) < 2:
            continue
        pairwise = []
        for i in range(len(recs)):
            for j in range(i + 1, len(recs)):
                a = item_categories.get(recs[i], 'Unknown')
                b = item_categories.get(recs[j], 'Unknown')
                pairwise.append(1 if a != b else 0)
        if pairwise:
            diversity_scores.append(sum(pairwise) / len(pairwise))
    if not diversity_scores:
        return 0.0
    return float(np.mean(diversity_scores))


def evaluate_models(train_df: pd.DataFrame, test_df: pd.DataFrame, items_df: pd.DataFrame, popularity_model: pd.Series, svd_model: Dict[str, object], top_k: int = 5) -> pd.DataFrame:
    item_categories = dict(zip(items_df['item_id'], items_df['category']))
    actual_by_user = test_df.groupby('user_id')['item_id'].apply(set).to_dict()
    user_ids = sorted(test_df['user_id'].unique())

    rows = []
    popularity_recs = []
    svd_recs = []

    for user_id in user_ids:
        seen_items = set(train_df[train_df['user_id'] == user_id]['item_id'].tolist())
        popularity_list = recommend_pop = list(popularity_model.sort_values(ascending=False).index)
        popularity_list = [item for item in popularity_list if item not in seen_items][:top_k]
        popularity_recs.append(popularity_list)

        svd_list = []
        if user_id in svd_model['user_ids']:
            svd_list = list(svd_model['recommendations'][user_id]) if user_id in svd_model['recommendations'] else []
        svd_recs.append(svd_list[:top_k])

        actual = actual_by_user.get(user_id, set())
        rows.append({
            'user_id': user_id,
            'actual_count': len(actual),
            'popularity_precision': precision_at_k(actual, popularity_list, top_k),
            'popularity_recall': recall_at_k(actual, popularity_list, top_k),
            'popularity_ndcg': ndcg_at_k(actual, popularity_list, top_k),
            'svd_precision': precision_at_k(actual, svd_list, top_k),
            'svd_recall': recall_at_k(actual, svd_list, top_k),
            'svd_ndcg': ndcg_at_k(actual, svd_list, top_k),
        })

    row_df = pd.DataFrame(rows)
    model_metrics = pd.DataFrame([
        {
            'model': 'Popularity',
            'precision@k': row_df['popularity_precision'].mean(),
            'recall@k': row_df['popularity_recall'].mean(),
            'ndcg@k': row_df['popularity_ndcg'].mean(),
            'coverage': coverage(popularity_recs, len(items_df)),
            'diversity': diversity(popularity_recs, item_categories),
        },
        {
            'model': 'SVD',
            'precision@k': row_df['svd_precision'].mean(),
            'recall@k': row_df['svd_recall'].mean(),
            'ndcg@k': row_df['svd_ndcg'].mean(),
            'coverage': coverage(svd_recs, len(items_df)),
            'diversity': diversity(svd_recs, item_categories),
        },
    ])
    return model_metrics


def recommend_by_popularity_for_all(model: pd.Series, user_ids: List[int], seen_items_by_user: Dict[int, set], top_k: int = 5) -> Dict[int, List[int]]:
    recs = {}
    for user_id in user_ids:
        recs[user_id] = [item for item in model.sort_values(ascending=False).index if item not in seen_items_by_user.get(user_id, set())][:top_k]
    return recs
