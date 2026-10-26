# Issue #4 — Exploratory sensor analysis: evidence, ideas and next experiments

**Owner:** GreciaBarraganPaez  
**Sprint:** Sprint 1 (CW43–44, 2026)  
**Issue:** [#4](https://github.com/GreciaBarraganPaez/aero-sentinel/issues/4)  
**Status:** Initial visualizations implemented; extended interpretation **pending**  
**Prepared:** 2026-10-26

## 1. EDA objective

Describe how simulated turbofan sensor signals evolve across engine cycles, distinguish informative variation from constant features and generate **testable** hypotheses for preprocessing, model selection and early-warning design.

**Important distinction:** a sensor trend is an observed association, not proof of physical damage onset or model predictive performance.

## 2. What has actually been implemented

| Implemented analysis | Source code | Output (generated locally) |
| --- | --- | --- |
| FD001 data-quality statistics | `src/aero_sentinel/first_data_test.py` | `results/figures/fd001_quality_report.json` |
| Standardized sensor_2, sensor_3, sensor_4 vs cycles for one engine | `src/aero_sentinel/first_data_test.py` | `results/figures/fd001_engine_sensor_trends.png` |
| Sensor_2, sensor_11, sensor_15 trajectories for first five FD001 engines, indexed by fraction of full lifetime | `src/aero_sentinel/first_data_test.py` | `results/figures/fd001_engine_lifetime_trends.png` |
| Constant vs nonconstant sensor counts and subset comparison | `src/aero_sentinel/dataset_overview.py` | `results/figures/cmapss_all_subsets_quality.json`, `cmapss_subset_comparison.csv` |

The lifetime-fraction axis uses knowledge of full training trajectories and is **for retrospective visualization only**; it cannot be used as a real-time inference feature.

## 3. Reproduce the existing EDA

```powershell
python -m pip install -e ".[dev]"
python -m aero_sentinel.first_data_test
python -m aero_sentinel.dataset_overview
```

Requires locally downloaded NASA files under `data/raw/`; outputs are generated under `results/figures/` and are not versioned.

## 4. Evidence-backed observations from existing implementation

The following are **facts about the analysis/code**, not claims about uninspected plot values:

1. The pipeline explicitly measures per-engine cycle sequence lengths and reports missing, duplicate and constant-sensor indicators; this supports deciding whether validation and sensor filtering are necessary.
2. Selected sensor trajectories are visualized against cycles, enabling qualitative comparison between engines and across portions of simulated life. The script itself does not establish whether any particular sensor rises or falls consistently.
3. The FD001–FD004 overview separates subset-specific quality and operating-context differences; it does **not yet** quantify sensor–sensor correlation or causal degradation onset.

**Not yet verified in a committed scientific report:** specific monotonic sensor trends, correlation coefficients, distribution shifts, statistical significance, sensor importance rankings or physical failure mechanisms. Do not present these as completed findings.

## 5. Suggested EDA extensions (research ideas, not completed work)

### A. Distribution and variation
- Plot histograms/boxplots of every sensor and report near-zero variance.
- Compare sensor distributions at early, middle and late **retrospective** lifetime segments on training engines.
- Report sample counts and avoid treating cycles within the same engine as independent engines.
- **Potential insight:** identify uninformative sensors or strong skew requiring robust scaling. *To test.*

### B. Correlations and redundancy
- Compute training-only Pearson and Spearman correlation matrices.
- Flag highly correlated sensor pairs and inspect whether they are redundant.
- Compare correlation patterns across engines, not only pooled rows.
- **Potential insight:** feature selection or dimension reduction. *To test.*

### C. Operating conditions
- Compare the three setting columns across FD001–FD004.
- Stratify sensor distributions by operating regime before concluding that shifts imply wear.
- **Potential insight:** condition-aware normalization may be necessary for FD002/FD004. *To test.*

### D. Engine-level trends
- Plot selected sensors per engine and calculate slopes or rolling statistics using only past observations.
- Compare per-engine slope distributions and check outliers.
- **Potential insight:** causal temporal features may help RUL estimation. *To test.*

### E. Early-warning visual design
- Pair sensor traces with model-predicted RUL and clearly labeled proxy warning states.
- Show actual RUL only in evaluation mode; never as an input to a prediction.
- **Potential insight:** interpretable dashboard evidence for the final demonstration. *To test.*

## 6. Proposed reporting template for at least three future observations

Use this format after running and inspecting the actual results:

| Observation | Figure or numeric evidence | Interpretation | Limitation |
| --- | --- | --- | --- |
| O1: [sensor/behavior] | [plot path + measured value] | [what the evidence supports] | [confounding/uncertainty] |
| O2: [sensor/behavior] | [plot path + measured value] | [what the evidence supports] | [confounding/uncertainty] |
| O3: [sensor/behavior] | [plot path + measured value] | [what the evidence supports] | [confounding/uncertainty] |

**Current status:** These are placeholders; no invented observations have been entered.

## 7. Relevance to the MVP

- Sensor selection should be fit on training engines only.
- Future rolling statistics must be **causal** (no future cycles).
- Operating conditions can alter observed sensor distributions independently of degradation.
- The dashboard should distinguish observed sensor data, model estimates and alert rules.

## 8. Delegation and acceptance criteria

- [ ] Issue [#10](https://github.com/GreciaBarraganPaez/aero-sentinel/issues/10): distributions, correlations, numerical interpretation.
- [ ] Issue [#11](https://github.com/GreciaBarraganPaez/aero-sentinel/issues/11): operating-condition differences.
- [ ] Record three specific observations with actual plots/numbers and caveats.
- [ ] Decide whether the expanded analyses belong to #4 or should be cross-referenced as completed follow-up issues.
- [ ] Review interpretation with team before closing #4.

**Closure condition for #4:** evidence-backed interpretations, not just plotting code, are reviewed and linked. Initial EDA is complete but the issue remains open.
