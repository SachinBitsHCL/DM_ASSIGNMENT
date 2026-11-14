# Recommendation Pipeline for Amazon-style E-commerce Data

This repository contains a complete end-to-end recommendation pipeline for an Amazon-style e-commerce system. The project covers data ingestion, validation, preparation, transformation, feature engineering, model training, evaluation, and orchestration in a modular and reproducible way.

## Assignment objective

Build a recommendation system that recommends relevant products to users using user behavior and item information. The pipeline should ingest raw data, validate data quality, prepare processed datasets, generate reusable features, train multiple recommender models, compare them using ranking metrics, and automate the process.

## Scope covered

- Data ingestion for user, item, and interaction records
- Automated validation for missing values, duplicates, invalid ratings, invalid timestamps, and referential integrity
- Train/test temporal split
- User activity and item popularity summary datasets
- Reusable feature tables for training and prediction
- Baseline + personalized recommender model
- Model evaluation with Precision@K, Recall@K, NDCG@K, Coverage, and Diversity
- Workflow orchestration and reproducible execution

## Project structure

```text
recommendation-pipeline/
├── dags/
│   └── recommendation_dag.py
├── data/
│   ├── raw/
│   ├── processed/
│   ├── features/
│   └── errors/
├── docs/
│   ├── architecture.md
│   ├── final_report.md
│   └── Final_Report_DRL_Assignment.pdf
├── reports/
│   ├── model_metrics.csv
│   ├── pipeline_summary.json
│   ├── validation_report.json
│   └── success_run_output.txt
├── src/
│   ├── evaluation/
│   ├── features/
│   ├── ingestion/
│   ├── orchestration/
│   ├── preparation/
│   ├── training/
│   ├── transform/
│   ├── validation/
│   ├── config.py
│   └── __init__.py
├── .gitignore
├── README.md
├── requirements.txt
├── run_pipeline.py
└── .venv/
```

## Environment setup

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows
.venv\Scripts\activate
pip install -r requirements.txt
```

### Windows DLL load error

If pandas fails to import with `DLL load failed ... An Application Control policy has blocked this file`, the failure is from the active Python environment's compiled package files, not from the pipeline code. In PowerShell, deactivate that environment and run with an installed Python interpreter whose packages load correctly:

```powershell
deactivate
& "C:\Path\To\Python\python.exe" run_pipeline.py
```

In VS Code, select that same interpreter with **Python: Select Interpreter**, then open a new terminal. Do not disable Application Control or copy DLL files between environments.

## Run the project

```bash
python run_pipeline.py
```

## What the pipeline does

When executed, the workflow performs the following tasks:

1. Loads or generates raw user, item, and interaction data.
2. Validates data quality and logs invalid records.
3. Creates train/test datasets using a time-based split.
4. Produces derived user and item summaries.
5. Builds feature tables for user, item, and interaction information.
6. Trains:
   - popularity-based recommendation baseline
   - personalized SVD recommender
7. Evaluates the models with ranking metrics.
8. Saves all reports and metrics in the `reports/` folder.

## Output files

- `data/processed/users_validated.csv` — validated user records
- `data/processed/items_validated.csv` — validated item records
- `data/processed/interactions_validated.csv` — validated interaction records
- `data/errors/invalid_interactions.csv` — rejected interactions with a `row_reason`
- `reports/validation_report.json` — validation checks, warnings, and data summary
- `reports/model_metrics.csv` — model comparison table
- `reports/pipeline_summary.json` — packaged summary of the full run
- `reports/success_run_output.txt` — successful pipeline execution log
- `docs/final_report.pdf` — presentation-ready PDF report

## Models used

- Popularity baseline recommender
- Personalized SVD recommender

## Evaluation metrics

- Precision@K
- Recall@K
- NDCG@K
- Coverage
- Diversity

## Notes for submission

This implementation uses a reproducible synthetic dataset for demonstration. To adapt the pipeline to the public Amazon Reviews dataset, replace the raw CSV files under `data/raw/` with:

- `users.csv`
- `items.csv`
- `interactions.csv`

The code is modular and ready to extend with additional recommendation methods, stronger feature engineering, or production orchestration tools such as Airflow or Prefect.

## Submission checklist

README provided
Source code organized into modules
Data validation implemented
Feature catalog generated
Base and personalized models trained
Evaluation results saved
Workflow orchestrated in a reproducible way
Final report created in PDF format

## Final report

The final assignment report is available in PDF form at:

- [docs/Final_Report_DRL_Assignment.pdf](docs/Final_Report_DRL_Assignment.pdf)

The Markdown version is here:

- [docs/final_report.md](docs/final_report.md)
