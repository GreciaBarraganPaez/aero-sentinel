# Issue #2 — NASA C-MAPSS acquisition, provenance and integrity

**Owner:** GreciaBarraganPaez  
**Sprint:** Sprint 1 (CW43–44, 2026)  
**Issue:** [#2](https://github.com/GreciaBarraganPaez/aero-sentinel/issues/2)  
**Status:** Data available locally; provenance and team reproducibility **not yet fully verified**  
**Prepared:** 2026-10-26

## 1. Source and attribution

Dataset: **NASA C-MAPSS (Commercial Modular Aero-Propulsion System Simulation) turbofan engine simulated run-to-failure data**.

- Project source reference: [NASA C-MAPSS dataset landing page](https://data.nasa.gov/dataset/cmapss-jet-engine-simulated-data).
- Use the dataset landing page to locate the official download and capture the **exact** download URL, archive filename, version (if published) and access date in the local provenance manifest.
- Attribution in presentations: "NASA C-MAPSS simulated turbofan engine run-to-failure dataset." Include the official source reference.
- **Do not claim** a specific downloaded archive checksum, version or licensing condition without verifying it against the source.

## 2. Local directory layout

Raw data is deliberately **not committed** to Git:

```text
data/raw/
  train_FD001.txt    test_FD001.txt    RUL_FD001.txt
  train_FD002.txt    test_FD002.txt    RUL_FD002.txt
  train_FD003.txt    test_FD003.txt    RUL_FD003.txt
  train_FD004.txt    test_FD004.txt    RUL_FD004.txt
```

The repository's `docs/data-analysis-setup.md` explains installation and execution.

## 3. File roles and interpretation

- `train_FD00X.txt`: complete simulated run-to-failure sequences for training engines.
- `test_FD00X.txt`: truncated histories for separate test engines.
- `RUL_FD00X.txt`: one ground-truth remaining-life value per test engine, corresponding to its **last observed cycle**, ordered by test engine ID.
- Sensor tables contain 26 numeric columns: engine ID, cycle, three settings and 21 sensor measurements; they do not include header names.
- FD001 is the initial modeling subset; FD002–FD004 are included in cross-subset quality analysis.

## 4. Local setup and reproduction (Windows PowerShell)

```powershell
git clone https://github.com/GreciaBarraganPaez/aero-sentinel.git
cd aero-sentinel
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
# Manually download and extract the NASA data files into data/raw/.
python -m pytest -q
python -m aero_sentinel.first_data_test
python -m aero_sentinel.dataset_overview
python -m aero_sentinel.rul_baseline
```

Generated reports/plots/predictions are written locally to `results/figures/`, not committed. A local run on 2026-10-26 reported **10 passing tests** and official FD001 test MAE **13.50**, RMSE **18.07** cycles; see [baseline report](../../rul-baseline.md). Those numbers do not prove another teammate has reproduced the run.

## 5. Integrity manifest (fill from each actual local copy)

Record size and SHA-256 for each raw file. PowerShell commands:

```powershell
Get-ChildItem data/raw -Filter "*.txt" | Sort-Object Name |
  Select-Object Name, Length |
  Format-Table -AutoSize

Get-ChildItem data/raw -Filter "*.txt" | Sort-Object Name |
  Get-FileHash -Algorithm SHA256 |
  Select-Object @{Name="File";Expression={Split-Path $_.Path -Leaf}}, Hash |
  Format-Table -AutoSize
```

**Do not invent or copy arbitrary hashes.** After computing, populate this manifest or a separately committed metadata-only file:

| File group | Expected number | Local size (bytes) | SHA-256 | Verified by / date |
| --- | ---: | --- | --- | --- |
| FD001 train/test/RUL | 3 | Pending | Pending | Pending |
| FD002 train/test/RUL | 3 | Pending | Pending | Pending |
| FD003 train/test/RUL | 3 | Pending | Pending | Pending |
| FD004 train/test/RUL | 3 | Pending | Pending | Pending |

Also record:
- **Actual downloaded source URL:** Pending verification
- **Download date (UTC):** Pending verification
- **Archive filename and version:** Pending verification
- **Extracted by:** Pending verification

## 6. Validation already implemented

- `src/aero_sentinel/data.py`: `load_sensor_file`, `load_rul_file`, `describe_dataset`.
- `src/aero_sentinel/first_data_test.py`: FD001 report and selected sensor plots.
- `src/aero_sentinel/dataset_overview.py`: FD001–FD004 dataset summaries.
- `tests/test_data.py`: synthetic validation tests.
- [Issue #3 closure evidence](issue-03-data-schema-quality.md): completed schema and quality checks.

## 7. Teammate reproducibility checklist

Each teammate should independently confirm:
- [ ] Official NASA source accessed and downloaded.
- [ ] All 12 files extracted to the expected local directory.
- [ ] No raw data, local secrets or generated results are staged for Git.
- [ ] Dependencies install and tests run in their environment.
- [ ] FD001 quality summary and baseline can be regenerated.
- [ ] Hashes and file sizes agree with the agreed dataset version.
- [ ] Any differences in OS, Python or package versions are noted.

Record each teammate's GitHub handle, verification date and command outputs in the Sprint 1 evidence log **after they actually perform the checks**.

## 8. Research caveats

- Synthetic run-to-failure observations are not a substitute for measured in-flight engine behavior.
- No exact physical degradation-onset labels are provided.
- Different FD subsets have different operating regimes and fault configurations.
- Keep the official test data separate from model selection.

**Closure condition for #2:** source and acquisition provenance verified, hashes/sizes recorded from real files and teammate reproduction confirmed. Until then, keep the issue open.
