from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from src.config import DATA_DIR, MODELS_DIR, REPORTS_DIR
from src.evaluation.evaluate import evaluate_models
from src.features.feature_store import create_feature_store
from src.ingestion.loader import load_datasets
from src.preparation.preparation import create_derived_datasets, split_time_based
from src.training.train_models import build_popularity_model, build_svd_model, recommend_svd
from src.validation.validation import validate_datasets


def run_pipeline(raw_data_dir: str | Path | None = None) -> dict:
    raw_dir = Path(raw_data_dir) if raw_data_dir else DATA_DIR / 'raw'
    raw_dir.mkdir(parents=True, exist_ok=True)
    datasets = load_datasets(raw_dir)

    users = datasets['users']
    items = datasets['items']
    interactions = datasets['interactions']

    users, items, interactions, validation_report = validate_datasets(users, items, interactions)
    train_df, test_df = split_time_based(interactions, split_ratio=0.8)

    derived = create_derived_datasets(interactions, users, items)
    feature_store = create_feature_store(users, items, interactions, derived['user_activity_summary'], derived['item_popularity'])

    popularity_model = build_popularity_model(train_df)
    all_user_ids = sorted(train_df['user_id'].unique().tolist())
    all_item_ids = sorted(items['item_id'].unique().tolist())
    svd_model = build_svd_model(train_df, all_item_ids, all_user_ids)

    seen_items_by_user = {user_id: set(train_df[train_df['user_id'] == user_id]['item_id']) for user_id in all_user_ids}
    svd_model['recommendations'] = {
        user_id: recommend_svd(svd_model, user_id, seen_items_by_user.get(user_id, set()), top_k=5)
        for user_id in all_user_ids
    }

    metrics = evaluate_models(train_df, test_df, items, popularity_model, svd_model, top_k=5)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(REPORTS_DIR / 'model_metrics.csv', index=False)

    summary = {
        'validation_report': validation_report,
        'metrics': metrics.to_dict(orient='records'),
        'feature_store': {key: str(value) for key, value in feature_store.items() if hasattr(value, 'shape')},
    }

    with (REPORTS_DIR / 'pipeline_summary.json').open('w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)

    return summary


if __name__ == '__main__':
    result = run_pipeline()
    print(json.dumps(result['validation_report'], indent=2))
    print('\nModel comparison:')
    print(pd.read_csv(REPORTS_DIR / 'model_metrics.csv').to_string(index=False))
