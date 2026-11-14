# Architecture Diagram

```mermaid
flowchart LR
    A[Raw Amazon Reviews Data] --> B[Data Ingestion]
    B --> C[Validation Layer]
    C --> D[Preparation / Transformation]
    D --> E[Feature Store]
    E --> F[Model Training]
    F --> G[Evaluation]
    G --> H[Reports / Artifacts]
    H --> I[Workflow Orchestration]
```

The recommended system pipeline is structured in stages: ingestion, validation, cleansing, feature engineering, model training, evaluation, and orchestration. Each stage produces artifacts and is tested for reproducibility.
