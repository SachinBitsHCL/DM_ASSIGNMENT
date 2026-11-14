# Final Report: Recommendation Pipeline for E-commerce Data

Student ID: 2025AG05794
Name : Sachin Vaghela
Git Hub Repo : https://github.com/SachinBitsHCL/DM_ASSIGNMENT
Date: 14 November 2024  
Project: End-to-End Recommendation Pipeline for Amazon E-commerce

## 1. Introduction

This project implements an end-to-end recommendation system pipeline for an online e-commerce platform. The pipeline ingests user, item, and interaction data; validates data quality; prepares the dataset for modeling; creates reusable features; trains two recommender systems; and evaluates them using ranking-based metrics. The goal is to provide a modular, reproducible, and production-oriented workflow instead of optimizing only for raw accuracy.

The solution follows the stages requested in the assignment: data ingestion, validation, preparation, transformation, feature management, model training, evaluation, and orchestration. The result is a pipeline that can be executed from a single command and produces validation reports, model comparison tables, and reproducible artifacts.

## 2. Design decisions

### Data ingestion
The project uses a synthetic Amazon-style dataset generated locally to ensure reproducibility in a controlled environment. The dataset includes users, items, and interactions. Each interaction includes the rating, timestamp, and event type, which allows temporal splitting and behavior-based recommendation workflows.

### Data validation
To support production-quality data engineering, the validation stage checks for missing values, duplicate rows, invalid rating ranges, invalid timestamps, and referential integrity across users and items. Invalid records are separated into an error dataset and logged in a report, ensuring the data pipeline remains auditable and transparent.

### Data preparation and transformation
The recommendation system uses time-based splitting for train/test evaluation. This is more realistic than random splitting because interactions are ordered by time and reflect how a live recommendation engine would operate. The preparation layer builds user activity summaries, item popularity tables, and a user-item interaction matrix, which are useful both for feature generation and baseline modeling.

### Feature management
The project defines reusable features at the user, item, and interaction level. Examples include average user ratings, activity counts, item popularity, item average rating, and time since last interaction. These features are stored as structured tables, making them reusable for training and future prediction tasks.

### Model training
Two models are trained:

1. Popularity-based baseline: recommends the most frequently interacted items.
2. SVD-based personalized recommender: learns latent dimensions from the user-item matrix.

This comparison is important because it shows both a simple baseline and a more personalized method while also allowing evaluation of trade-offs between explainability, performance, and complexity.


### Model evaluation
The assignment requires ranking metrics such as Precision@K, Recall@K, NDCG@K, Coverage, and Diversity. These are implemented in a dedicated evaluation module. The model comparison is saved to a CSV report to make the results easy to inspect and present.

model			Popularity			SVD
precision@k		0.12000000000000001	0.11999999999999998
recall@k		0.061871647			0.060243059
ndcg@k			0.11614354207027025	0.12414114522960885
coverage		0.2					1
diversity		0.7816666666666667	0.8408333333333334


## 3. Tools and implementation

The solution uses Python as the primary language and leverages pandas, numpy, and scikit-learn-compatible patterns to prepare and analyze the data. The code is organized into modules reflecting the stages of the pipeline and is designed to be easily extended. The repository structure separates ingestion, validation, preparation, transformation, features, training, evaluation, and orchestration into distinct folders.

The orchestration layer is designed as a workflow entry point that calls the full pipeline sequentially. Airflow was also explored conceptually and represented as a DAG file, though the working implementation remains a Python-driven workflow to keep the solution runnable in the local environment without requiring a full Airflow installation.

## 4. Results

The pipeline successfully executes on a reproducible synthetic dataset and produces clean reports. The validation report indicates the dataset passes the required checks with a small number of duplicate interactions logged as errors. The model metrics table compares the baseline popularity model and the personalization model using ranking metrics.

## 5. Limitations

Additionally, the orchestration layer is intentionally simple and modular. It satisfies the assignment requirement for reproducibility and task sequencing, but a full production Airflow deployment would add extra infrastructure and monitoring.

## 6. Conclusion

This project successfully demonstrates a complete recommendation pipeline from raw data to evaluated models. The emphasis is on clean engineering practices, modular design, data validation, reusable feature engineering, and reproducible workflows.
