from __future__ import annotations

import pandas as pd


def generate_user_item_features(interactions: pd.DataFrame, user_activity_summary: pd.DataFrame, item_popularity: pd.DataFrame) -> pd.DataFrame:
    merged = interactions.merge(user_activity_summary, on='user_id', how='left')
    merged = merged.merge(item_popularity, on='item_id', how='left')
    merged['days_since_last_interaction'] = (
        pd.Timestamp.now().tz_localize(None) - merged['last_interaction']
    ).dt.days
    return merged


def build_feature_catalog() -> pd.DataFrame:
    catalog = pd.DataFrame([
        {'feature_group': 'user', 'feature_name': 'user_average_rating', 'description': 'Average rating given by the user.'},
        {'feature_group': 'user', 'feature_name': 'user_activity_count', 'description': 'Number of interactions for the user.'},
        {'feature_group': 'user', 'feature_name': 'last_interaction', 'description': 'Most recent interaction timestamp for the user.'},
        {'feature_group': 'item', 'feature_name': 'item_average_rating', 'description': 'Average rating received by the item.'},
        {'feature_group': 'item', 'feature_name': 'item_popularity_count', 'description': 'How frequently the item appears in interactions.'},
        {'feature_group': 'interaction', 'feature_name': 'days_since_last_interaction', 'description': 'Time gap between current interaction and most recent user event.'},
        {'feature_group': 'interaction', 'feature_name': 'event_type', 'description': 'Type of event such as click, view, or purchase.'},
    ])
    return catalog
