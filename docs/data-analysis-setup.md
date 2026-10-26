# Running the first C-MAPSS analysis

## Prerequisites

Python 3.10+ and the NASA C-MAPSS files downloaded separately.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

## Dataset layout

Place the following files in `data/raw/`:

```text
data/raw/
  train_FD001.txt
  test_FD001.txt
  RUL_FD001.txt
  train_FD002.txt
  test_FD002.txt
  RUL_FD002.txt
  train_FD003.txt
  test_FD003.txt
  RUL_FD003.txt
  train_FD004.txt
  test_FD004.txt
  RUL_FD004.txt
```

## Commands

```powershell
python -m pytest -q
python -m aero_sentinel.first_data_test
python -m aero_sentinel.dataset_overview
```

Generated locally under `results/figures/`:
- `fd001_quality_report.json`
- `fd001_engine_sensor_trends.png`
- `fd001_engine_lifetime_trends.png`
- `cmapss_subset_comparison.csv`
- `cmapss_all_subsets_quality.json`

The uploaded raw NASA files are **not included** in the GitHub branch.

## Status

Source and unit tests have been added to the feature branch. Execute the commands above locally to verify them in your own environment; no CI or GitHub Actions job has been added yet.
