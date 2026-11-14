from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple

import numpy as np
import pandas as pd

from src.config import RAW_DIR


def generate_synthetic_dataset(raw_dir: Path, n_users: int = 120, n_items: int = 80, n_interactions: int = 6000) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(42)
    categories = ['Electronics', 'Books', 'Home', 'Fashion', 'Beauty', 'Sports']

    users = pd.DataFrame({
        'user_id': np.arange(1, n_users + 1),
        'country': rng.choice(['US', 'UK', 'DE', 'IN', 'JP'], size=n_users),
        'signup_date': pd.date_range('2022-01-01', periods=n_users, freq='D').to_series().sample(n_users, random_state=42).values
    })
    users['signup_date'] = pd.to_datetime(users['signup_date'])

    items = pd.DataFrame({
        'item_id': np.arange(1, n_items + 1),
        'category': rng.choice(categories, size=n_items),
        'price': np.round(rng.uniform(10, 250, size=n_items), 2),
        'brand': rng.choice(['A', 'B', 'C', 'D', 'E'], size=n_items)
    })

    user_bias = rng.normal(3.2, 0.8, size=n_users)
    item_bias = rng.normal(3.6, 0.9, size=n_items)
    category_bonus = {'Electronics': 0.5, 'Books': 0.1, 'Home': 0.2, 'Fashion': -0.1, 'Beauty': 0.4, 'Sports': 0.3}

    records = []
    for _ in range(n_interactions):
        user_id = int(rng.integers(1, n_users + 1))
        item_id = int(rng.integers(1, n_items + 1))
        item_cat = items.loc[items['item_id'] == item_id, 'category'].iloc[0]
        rating = (
            user_bias[user_id - 1]
            + item_bias[item_id - 1]
            + category_bonus.get(item_cat, 0)
            + rng.normal(0, 0.7)
        )
        rating = float(np.clip(rating, 1.0, 5.0))
        timestamp = pd.Timestamp('2023-01-01') + pd.to_timedelta(rng.integers(0, 365 * 2), unit='D')
        records.append({
            'user_id': user_id,
            'item_id': item_id,
            'rating': round(rating, 2),
            'timestamp': timestamp,
            'event_type': rng.choice(['view', 'click', 'purchase'], p=[0.45, 0.35, 0.20])
        })

    interactions = pd.DataFrame(records)
    interactions = interactions.sort_values('timestamp').reset_index(drop=True)

    raw_dir.mkdir(parents=True, exist_ok=True)
    users.to_csv(raw_dir / 'users.csv', index=False)
    items.to_csv(raw_dir / 'items.csv', index=False)
    interactions.to_csv(raw_dir / 'interactions.csv', index=False)

    return users, items, interactions


def load_datasets(raw_dir: Path | None = None) -> Dict[str, pd.DataFrame]:
    raw_dir = raw_dir or RAW_DIR
    raw_dir.mkdir(parents=True, exist_ok=True)

    user_path = raw_dir / 'users.csv'
    item_path = raw_dir / 'items.csv'
    interaction_path = raw_dir / 'interactions.csv'

    if not (user_path.exists() and item_path.exists() and interaction_path.exists()):
        users, items, interactions = generate_synthetic_dataset(raw_dir)
        return {'users': users, 'items': items, 'interactions': interactions}

    users = pd.read_csv(user_path)
    items = pd.read_csv(item_path)
    interactions = pd.read_csv(interaction_path, parse_dates=['timestamp'])

    return {'users': users, 'items': items, 'interactions': interactions}
