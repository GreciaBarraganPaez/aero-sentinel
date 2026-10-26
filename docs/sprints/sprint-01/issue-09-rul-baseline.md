# Closure record — Issue #9: FD001 Random Forest RUL baseline

| Field | Value |
| --- | --- |
| Issue | [#9 — FD001 Random Forest RUL baseline](https://github.com/GreciaBarraganPaez/aero-sentinel/issues/9) |
| Sprint | Sprint 1 (actual completion; the issue's original title said Sprint 2) |
| Assignee | `GreciaBarraganPaez` |
| Status | **Closed / Done** |
| Closed at (GitHub UTC) | **2026-10-26 14:24:42 UTC** |
| Implementation PR | [#8 — RUL baseline](https://github.com/GreciaBarraganPaez/aero-sentinel/pull/8) |
| Integration PR | [#7 — data analysis branch merged into main](https://github.com/GreciaBarraganPaez/aero-sentinel/pull/7) |

## What was implemented

1. Created RUL targets from full training trajectories: `max_cycle(engine) - current_cycle`, with training targets capped at **125 cycles**.
2. Built a `RandomForestRegressor` baseline with 150 estimators, `min_samples_leaf=3`, `max_features=0.8` and seed 42.
3. Selected `cycle`, operating settings and nonconstant sensor features using the **training partition only**.
4. Created an **80/20 engine-disjoint** holdout with `GroupShuffleSplit`. Scored three retrospectively selected partial-trajectory snapshots (~50%, 70%, 90% lifetime) for each held-out engine.
5. Retrained on the full FD001 training set and evaluated on the official test engines' last observed cycles using `RUL_FD001.txt`.
6. Compared predictions against a constant-median RUL baseline; generated JSON metrics, CSV predictions and a scatter plot.
7. Added three RUL-specific synthetic unit tests and experiment documentation.

## Where the work lives

| Path | Purpose |
| --- | --- |
| `src/aero_sentinel/rul_baseline.py` | Label creation, model configuration, engine split, validation, official-test scoring and plots |
| `tests/test_rul_baseline.py` | Synthetic tests for labels, snapshots and evaluation |
| `docs/rul-baseline.md` | Method, reproduction steps, measured metrics and limitations |
| `src/aero_sentinel/data.py` | Shared C-MAPSS file loading and validation |
| `pyproject.toml` | Python package and scikit-learn dependency |

## How to reproduce

From the repository root, with `train_FD001.txt`, `test_FD001.txt` and `RUL_FD001.txt` under `data/raw/`:

```powershell
python -m pip install -e ".[dev]"
python -m pytest -q
python -m aero_sentinel.rul_baseline
```

Expected **locally generated** outputs under `results/figures/`:
- `fd001_rul_baseline_metrics.json`
- `fd001_rul_test_predictions.csv`
- `fd001_rul_predictions.png`

## Verified results — local execution on 2026-10-26

| Metric | Random Forest | Constant median |
| --- | ---: | ---: |
| Internal holdout MAE (20 engines, 60 snapshots) | **15.76** cycles | 47.45 cycles |
| Internal holdout RMSE | **20.27** cycles | 55.04 cycles |
| Official FD001 test MAE (100 engines) | **13.50** cycles | 39.08 cycles |
| Official FD001 test RMSE | **18.07** cycles | 49.82 cycles |

**Tests:** 10 local unit tests passed across data and RUL modules (2026-10-26). These are local measurements; no GitHub CI execution was claimed. No raw data, trained model or generated plots were committed.

## Limitations / follow-up

- Only one engine-wise validation split; repeated group-based validation remains in [#15](https://github.com/GreciaBarraganPaez/aero-sentinel/issues/15).
- The validation snapshot positions are selected with retrospective knowledge of engine lifetime, **not** a production streaming evaluation protocol.
- Training labels are capped at 125 cycles; high-RUL predictions may be underestimated.
- Official test data should not be used for repeated hyperparameter tuning.
- **RUL prediction does not establish early-warning performance or true physical degradation onset.** Warning thresholds and alert evaluation are separate tasks [#13](https://github.com/GreciaBarraganPaez/aero-sentinel/issues/13) and [#24](https://github.com/GreciaBarraganPaez/aero-sentinel/issues/24).
- Model comparison and production-style inference are tracked in [#12](https://github.com/GreciaBarraganPaez/aero-sentinel/issues/12) and [#23](https://github.com/GreciaBarraganPaez/aero-sentinel/issues/23).

## GitHub closure comment

The issue comment repeats this summary and links to this file, so the evidence remains discoverable from both the issue tracker and the source tree.
