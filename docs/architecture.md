# Aero Sentinel — architecture draft (v0.2)

## Goal

Explore early-warning approaches for simulated turbofan degradation using NASA C-MAPSS. **C-MAPSS does not label the exact physical onset of degradation.** Any early-warning target must be operationally defined and validated rather than presented as a ground-truth damage onset.

## Data pipeline

```mermaid
flowchart TD
    A[NASA C-MAPSS FD001–FD004] --> B[Data ingestion]
    B --> C[Schema & quality validation]
    C --> D[Exploratory data analysis]
    D --> E[Sensor selection & preprocessing]
    E --> F[Engine-wise train/validation split]
    F --> G1[RUL baseline — planned]
    F --> G2[Isolation Forest — planned]
    F --> G3[Autoencoder — planned]
    G1 --> H[Evaluation on unseen engines]
    G2 --> H
    G3 --> H
    H --> I[Early-warning indicators & reporting]
```

## Implemented in this branch

- `data.py`: whitespace-delimited data ingestion, schema validation, RUL loading, quality statistics.
- `first_data_test.py`: FD001 quality report and exploratory sensor plots.
- `dataset_overview.py`: comparison across FD001–FD004, CSV/JSON outputs.
- `tests/test_data.py`: synthetic fixtures to check validation behavior.

## Planned (not implemented)

- RUL target generation for training engines and leakage-safe splitting by engine.
- Scaling fitted on training engines only, sensor selection and time-window features.
- RUL regression baseline and anomaly-detection baselines.
- Evaluation using MAE/RMSE, false-alert rate, warning lead time and ablation studies.

## Research cautions

1. The training sets contain complete run-to-failure sequences; the test sets are truncated and include RUL at the last observed cycle.
2. Do not randomly split rows from the same engine across training and validation.
3. FD002 and FD004 have multiple operating conditions; preprocessing may need condition-aware treatment.
4. Plots are descriptive; they do not establish predictive performance.
5. Keep NASA raw data out of git; reproduce results from local `data/raw/`.
