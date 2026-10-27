# Running the first C-MAPSS analysis

## Prerequisites

Python 3.10+. The project now intends to version the 12 original NASA C-MAPSS text files in `data/raw/` so that a clone includes them once the dataset commit is merged. Until then, download the files from NASA separately.

### Dataset source and citation

The dataset is **Turbofan Engine Degradation Simulation Data Set** from the NASA Ames Prognostics Center of Excellence (PCoE), generated using the Commercial Modular Aero-Propulsion System Simulation (C-MAPSS). FD001–FD004 represent different combinations of operating conditions and fault modes.

- **Download:** [NASA PCoE dataset ZIP](https://phm-datasets.s3.amazonaws.com/NASA/6.+Turbofan+Engine+Degradation+Simulation+Data+Set.zip)
- **Citation:** A. Saxena and K. Goebel (2008). *Turbofan Engine Degradation Simulation Data Set*. NASA Prognostics Data Repository, NASA Ames Research Center, Moffett Field, CA.
- **Detailed provenance and verification:** [Sprint 1 dataset provenance](sprints/sprint-01/grecia-dataset-provenance.md).

Extract the ZIP and place the 12 `train_`, `test_`, and `RUL_` text files directly inside `data/raw/` (no extra nested folder). These 12 raw text files are intended to be tracked by Git. The repository owner must still commit and push them; their presence on GitHub has not yet been verified.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

## Dataset layout

The repository should contain the following tracked files in `data/raw/` after the dataset commit is merged:

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

**Dataset publication pending:** The owner reported copying the files locally and decided to commit them to GitHub. The files are not yet confirmed as pushed. After committing, check that all 12 appear in the GitHub PR and verify their SHA-256 hashes.

## Status

Execute the commands above locally to verify the analysis in your own environment. A GitHub Actions documentation gate exists for pull requests; local dataset-dependent analysis still needs to be run on each contributor's machine.
