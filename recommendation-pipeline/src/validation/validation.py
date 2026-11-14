from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from src.config import ERRORS_DIR, PROCESSED_DIR, REPORTS_DIR


def validate_datasets(users: pd.DataFrame, items: pd.DataFrame, interactions: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict]:
    errors = []
    invalid_records = []

    users_valid = users.drop_duplicates().copy()
    items_valid = items.drop_duplicates().copy()
    interactions_valid = interactions.copy().reset_index(drop=True)

    def record_invalid(mask: pd.Series, reason: str, column: str) -> None:
        count = int(mask.sum())
        if not count:
            return
        invalid = interactions_valid.loc[mask].copy()
        invalid['row_reason'] = reason
        invalid_records.append(invalid)
        errors.append({
            'dataset': 'interactions',
            'column': column,
            'reason': reason,
            'count': count,
        })

    missing_users = interactions_valid['user_id'].isna()
    missing_items = interactions_valid['item_id'].isna()
    record_invalid(missing_users, 'missing', 'user_id')
    record_invalid(missing_items, 'missing', 'item_id')

    interactions_valid = interactions_valid[~(interactions_valid['user_id'].isna() | interactions_valid['item_id'].isna())].copy()

    interactions_valid['rating'] = pd.to_numeric(interactions_valid['rating'], errors='coerce')
    invalid_rating_mask = interactions_valid['rating'].isna() | (interactions_valid['rating'] < 1) | (interactions_valid['rating'] > 5)
    record_invalid(invalid_rating_mask, 'invalid_rating', 'rating')
    interactions_valid = interactions_valid[~invalid_rating_mask].copy()

    interactions_valid['timestamp'] = pd.to_datetime(interactions_valid['timestamp'], errors='coerce')
    invalid_timestamp_mask = interactions_valid['timestamp'].isna()
    record_invalid(invalid_timestamp_mask, 'invalid_timestamp', 'timestamp')
    interactions_valid = interactions_valid[~invalid_timestamp_mask].copy()

    duplicate_mask = interactions_valid.duplicated(subset=['user_id', 'item_id', 'timestamp'], keep='first')
    record_invalid(duplicate_mask, 'duplicate_rows', 'user_id,item_id,timestamp')
    interactions_valid = interactions_valid.drop_duplicates(subset=['user_id', 'item_id', 'timestamp']).copy()

    valid_user_ids = set(users_valid['user_id'].astype(int))
    valid_item_ids = set(items_valid['item_id'].astype(int))
    interaction_user_valid = interactions_valid['user_id'].astype(int).isin(valid_user_ids)
    interaction_item_valid = interactions_valid['item_id'].astype(int).isin(valid_item_ids)
    referential_invalid = ~(interaction_user_valid & interaction_item_valid)
    record_invalid(referential_invalid, 'referential_integrity', 'user_id,item_id')
    interactions_valid = interactions_valid[interaction_user_valid & interaction_item_valid].copy()

    ERRORS_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    users_valid.to_csv(PROCESSED_DIR / 'users_validated.csv', index=False)
    items_valid.to_csv(PROCESSED_DIR / 'items_validated.csv', index=False)
    interactions_valid.to_csv(PROCESSED_DIR / 'interactions_validated.csv', index=False)

    invalid_interactions = (
        pd.concat(invalid_records, ignore_index=True)
        if invalid_records
        else pd.DataFrame(columns=[*interactions.columns, 'row_reason'])
    )
    invalid_interactions.to_csv(ERRORS_DIR / 'invalid_interactions.csv', index=False)

    report = {
        'total_users': int(len(users_valid)),
        'total_items': int(len(items_valid)),
        'total_interactions': int(len(interactions_valid)),
        'invalid_rows_logged': int(len(invalid_interactions)),
        'errors': errors,
        'status': 'passed' if not errors else 'warnings_detected'
    }

    with (REPORTS_DIR / 'validation_report.json').open('w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, default=str)

    return users_valid, items_valid, interactions_valid, report
