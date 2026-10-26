# Closure record — Issue #3: Inspect dataset schema and quality

| Field | Value |
| --- | --- |
| Issue | [#3 — Inspect dataset schema and quality](https://github.com/GreciaBarraganPaez/aero-sentinel/issues/3) |
| Sprint | Sprint 1 (CW43–44, 2026) |
| Assignee | `GreciaBarraganPaez` |
| Status | **Closed / Done** |
| Closed at (GitHub UTC) | **2026-10-26 14:22:21 UTC** |
| Implementation PR | [#7 — data validation and exploratory analysis](https://github.com/GreciaBarraganPaez/aero-sentinel/pull/7) |
| Supporting PR | [#8 — engine-disjoint validation](https://github.com/GreciaBarraganPaez/aero-sentinel/pull/8) |

## What was implemented

1. Defined the 26-column C-MAPSS schema: `engine_id`, `cycle`, three operating settings and 21 sensor readings.
2. Implemented whitespace-delimited numeric file ingestion with explicit errors for missing files, empty files, wrong column counts, nonnumeric/missing entries, invalid IDs/cycles, duplicate `(engine_id, cycle)` pairs and out-of-order cycles within an engine.
3. Implemented test RUL-file ingestion, including nonnegative integer validation and optional engine-count consistency checks.
4. Added per-dataset summaries: record/engine counts, cycle ranges, engine sequence lengths, missing values, duplicate pairs and constant sensors.
5. Added a FD001–FD004 overview that compares train/test subsets and writes machine-readable quality reports; checks whether engine cycles are contiguous.
6. Added synthetic unit tests for ingestion and validation. The later RUL baseline performs a group-based train/validation split to keep engines separate.

## Where the work lives

| Path | Purpose |
| --- | --- |
| `src/aero_sentinel/data.py` | `COLUMNS`, `load_sensor_file`, `load_rul_file`, `describe_dataset`, `DataValidationError` |
| `src/aero_sentinel/first_data_test.py` | FD001 data-quality report and selected sensor plots |
| `src/aero_sentinel/dataset_overview.py` | FD001–FD004 comparisons and JSON/CSV outputs |
| `tests/test_data.py` | Synthetic input validation tests |
| `docs/data-analysis-setup.md` | Installation, required raw files and reproduction commands |
| `src/aero_sentinel/rul_baseline.py` | Engine-disjoint `GroupShuffleSplit` in downstream model evaluation |

## How to reproduce

From the repository root, place NASA text files in `data/raw/` (not committed), then:

```powershell
python -m pip install -e ".[dev]"
python -m pytest -q
python -m aero_sentinel.first_data_test
python -m aero_sentinel.dataset_overview
```

Expected **locally generated** outputs under `results/figures/`:
- `fd001_quality_report.json`
- `fd001_engine_sensor_trends.png`
- `fd001_engine_lifetime_trends.png`
- `cmapss_all_subsets_quality.json`
- `cmapss_subset_comparison.csv`

## Verification and evidence

- [Merged PR #7](https://github.com/GreciaBarraganPaez/aero-sentinel/pull/7) contains the data module, EDA scripts, setup documentation and seven synthetic data tests.
- The data and RUL test suites were run locally on 2026-10-26: **10 tests passed in total** (seven data tests plus three RUL tests). This is a historical local result, **not a GitHub CI run**.
- Actual NASA raw data and generated reports are **not committed** to the repository.

## Limitations / follow-up

- This closure establishes the *implemented schema and validation code*, not a fully interpreted scientific EDA report. Further distribution/correlation and operating-regime analysis are tracked in [#10](https://github.com/GreciaBarraganPaez/aero-sentinel/issues/10) and [#11](https://github.com/GreciaBarraganPaez/aero-sentinel/issues/11).
- C-MAPSS does not provide exact ground-truth physical degradation-onset labels.
- No CI pipeline was available at the time of this closure; see [#20](https://github.com/GreciaBarraganPaez/aero-sentinel/issues/20).

## GitHub closure comment

The issue comment repeats this summary and links to this file, so the evidence remains discoverable from both the issue tracker and the source tree.
