from __future__ import annotations

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from src.orchestration.pipeline import run_pipeline


with DAG(
    dag_id='recommendation_pipeline',
    start_date=datetime(2024, 1, 1),
    schedule='@daily',
    catchup=False,
    tags=['recommendation', 'ml-pipeline'],
) as dag:
    run_pipeline_task = PythonOperator(
        task_id='run_recommendation_pipeline',
        python_callable=run_pipeline,
    )
