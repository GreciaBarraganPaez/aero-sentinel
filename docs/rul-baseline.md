# FD001 — First RUL baseline

## Objective

Predict Remaining Useful Life (RUL), in simulated cycles, for NASA C-MAPSS FD001. This is a regression baseline, **not** a validated early-warning or physical fault-onset detector.

## Method

- Dataset: FD001 complete run-to-failure training trajectories and truncated test trajectories.
- Label: per-training-row RUL = maximum cycle for that engine minus current cycle.
- Training label capped at 125 cycles; evaluation against uncapped ground truth.
- Model: RandomForestRegressor (150 trees, min_samples_leaf=3, max_features=0.8, seed=42).
- Features: cycle, operating settings, nonconstant sensors (selected using training partition).
- Holdout: GroupShuffleSplit by engine ID, 80/20; no engine shared between partitions.
- Internal evaluation: 3 partial observations per unseen engine, at ~50%, 70%, and 90% of its full lifetime. These fractions are selected retrospectively for evaluation only; the model does not receive them.
- Official test: train model again on all 100 FD001 training engines, evaluate once on the last available cycle of each of the 100 test engines using the NASA RUL file.
- Baseline comparison: constant prediction equal to the median capped training RUL.

## Reproducing

```powershell
python -m pip install -e ".[dev]"
python -m pytest -q
python -m aero_sentinel.rul_baseline
```

Requires `train_FD001.txt`, `test_FD001.txt`, and `RUL_FD001.txt` in `data/raw/`. Outputs are ignored by Git and written under `results/figures/`.

## Local run — 2026-10-26

Ran against uploaded NASA C-MAPSS FD001 files in a local Python environment (scikit-learn 1.8.0). These are measured execution results, not claims about GitHub CI:

| Metric | Random Forest | Constant median |
|---|---:|---:|
| Holdout MAE (60 observations from 20 unseen engines) | 15.76 cycles | 47.45 cycles |
| Holdout RMSE | 20.27 cycles | 55.04 cycles |
| Official test MAE (100 engines) | 13.50 cycles | 39.08 cycles |
| Official test RMSE | 18.07 cycles | 49.82 cycles |

Ten local unit tests passed across the data and baseline modules.

## Limitations

- A single fixed holdout split is not enough to quantify uncertainty; use repeated engine-group cross-validation.
- Test metrics should not be repeatedly optimized against.
- Predictions are constrained by the 125-cycle training target cap, so high-RUL cases may be underestimated.
- Partial-life validation uses retrospective knowledge of full trajectories to pick evaluation points; this is a benchmark protocol, not deployable online truncation.
- RUL accuracy alone does not quantify false alerts or warning lead time.
- C-MAPSS does not provide a ground-truth exact physical degradation-onset timestamp.
