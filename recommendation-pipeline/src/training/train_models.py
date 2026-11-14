from __future__ import annotations

from typing import Dict, List

import numpy as np
import pandas as pd


def build_popularity_model(train_df: pd.DataFrame) -> pd.Series:
    popularity = (
        train_df.groupby('item_id', as_index=False)
        .agg(popularity_score=('user_id', 'size'), avg_rating=('rating', 'mean'))
        .sort_values(['popularity_score', 'avg_rating'], ascending=[False, False])
        .set_index('item_id')['popularity_score']
    )
    return popularity


def recommend_popularity(popularity_scores: pd.Series, user_id: int, seen_items: set, top_k: int = 5) -> List[int]:
    candidate_items = [item for item in popularity_scores.sort_values(ascending=False).index if item not in seen_items]
    return candidate_items[:top_k]


def build_svd_model(train_df: pd.DataFrame, all_item_ids: List[int], all_user_ids: List[int]) -> Dict[str, object]:
    matrix = (
        train_df.pivot_table(index='user_id', columns='item_id', values='rating', aggfunc='mean')
        .reindex(index=all_user_ids, columns=all_item_ids, fill_value=0.0)
        .fillna(0.0)
        .astype(float)
    )
    matrix_np = matrix.to_numpy()

    if matrix_np.size == 0 or np.allclose(matrix_np, 0):
        user_factors = np.zeros((len(all_user_ids), 1), dtype=float)
        item_factors = np.zeros((len(all_item_ids), 1), dtype=float)
    else:
        matrix_np = np.nan_to_num(matrix_np, nan=0.0, posinf=0.0, neginf=0.0)
        u, s, vt = np.linalg.svd(matrix_np, full_matrices=False)
        k = min(10, len(s))
        user_factors = u[:, :k] * s[:k]
        item_factors = vt[:k].T

    return {
        'user_factors': user_factors,
        'item_factors': item_factors,
        'matrix': matrix,
        'user_ids': np.array(all_user_ids),
        'item_ids': np.array(all_item_ids),
    }


def recommend_svd(model: Dict[str, object], user_id: int, seen_items: set, top_k: int = 5) -> List[int]:
    user_ids = model['user_ids']
    item_ids = model['item_ids']
    user_index = np.where(user_ids == user_id)[0]

    if len(user_index) == 0:
        return []

    user_idx = int(user_index[0])
    user_vector = model['user_factors'][user_idx]
    scores = user_vector @ model['item_factors'].T
    ranked = sorted(zip(item_ids, scores), key=lambda x: x[1], reverse=True)
    return [int(item_id) for item_id, _ in ranked if item_id not in seen_items][:top_k]
