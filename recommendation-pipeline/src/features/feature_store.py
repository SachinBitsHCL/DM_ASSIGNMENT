from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.config import FEATURES_DIR, REPORTS_DIR
from src.transform.transform import build_feature_catalog, generate_user_item_features


def create_feature_store(users: pd.DataFrame, items: pd.DataFrame, interactions: pd.DataFrame, user_activity_summary: pd.DataFrame, item_popularity: pd.DataFrame) -> dict:
    interaction_features = generate_user_item_features(interactions, user_activity_summary, item_popularity)
    feature_catalog = build_feature_catalog()

    user_feature_table = users.merge(user_activity_summary, on='user_id', how='left')
    item_feature_table = items.merge(item_popularity, on='item_id', how='left')

    FEATURES_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    interaction_features.to_csv(FEATURES_DIR / 'interaction_features.csv', index=False)
    user_feature_table.to_csv(FEATURES_DIR / 'user_features.csv', index=False)
    item_feature_table.to_csv(FEATURES_DIR / 'item_features.csv', index=False)
    feature_catalog.to_csv(REPORTS_DIR / 'feature_catalog.csv', index=False)

    return {
        'user_features': user_feature_table,
        'item_features': item_feature_table,
        'interaction_features': interaction_features,
        'feature_catalog': feature_catalog,
    }
