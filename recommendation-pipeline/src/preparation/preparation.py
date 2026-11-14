from __future__ import annotations

import pandas as pd


def split_time_based(interactions: pd.DataFrame, split_ratio: float = 0.8) -> tuple[pd.DataFrame, pd.DataFrame]:
    if interactions.empty:
        raise ValueError('No interaction data to split.')

    sorted_df = interactions.sort_values('timestamp').reset_index(drop=True)
    cutoff = sorted_df['timestamp'].quantile(split_ratio)
    train_df = sorted_df[sorted_df['timestamp'] < cutoff].copy()
    test_df = sorted_df[sorted_df['timestamp'] >= cutoff].copy()

    return train_df, test_df


def create_derived_datasets(interactions: pd.DataFrame, users: pd.DataFrame, items: pd.DataFrame) -> dict:
    user_activity_summary = (
        interactions.groupby('user_id', as_index=False)
        .agg(user_activity_count=('user_id', 'size'),
             user_average_rating=('rating', 'mean'),
             last_interaction=('timestamp', 'max'))
    )

    item_popularity = (
        interactions.groupby('item_id', as_index=False)
        .agg(item_popularity_count=('item_id', 'size'),
             item_average_rating=('rating', 'mean'))
    )

    user_item_matrix = (
        interactions.pivot_table(index='user_id', columns='item_id', values='rating', aggfunc='mean')
        .fillna(0)
    )

    return {
        'user_activity_summary': user_activity_summary,
        'item_popularity': item_popularity,
        'user_item_matrix': user_item_matrix,
        'users': users,
        'items': items,
    }
