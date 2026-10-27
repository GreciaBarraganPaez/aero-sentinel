# Issue #1 — Research scope, hypotheses and success criteria

**Owner:** GreciaBarraganPaez  
**Sprint:** Sprint 1 (CW43–44, 2026)  
**Issue:** [#1](https://github.com/GreciaBarraganPaez/aero-sentinel/issues/1)  
**Status:** Scoped Sprint 1 deliverable closed 2026-10-27; professor approval reported by owner; final alert details remain for #13/#21.  
**Prepared:** 2026-10-26  
**Professor approval:** Confirmed by project owner on 2026-10-27; no independent approval artifact attached.

## 1. Motivation and problem statement

Aircraft engines generate multivariate sensor measurements over operating cycles. An engineering monitoring system should make those time series understandable and estimate whether an engine is approaching its simulated end of useful life. Aero Sentinel studies **NASA C-MAPSS**, a simulated turbofan run-to-failure dataset, to evaluate the feasibility of a transparent predictive-maintenance prototype.

This is a **course research prototype**, not a deployable aircraft safety system, and does not claim certified fault diagnosis.

## 2. Proposed research question (requires team approval)

> **How accurately can leakage-aware machine-learning models estimate remaining useful life for previously unseen simulated turbofan engines, and how useful are explicitly defined RUL-based warning rules in terms of alert lead time and false-alert behavior?**

This wording distinguishes two measurable tasks:
- **RUL regression:** predict remaining simulated operating cycles until recorded failure.
- **Operational early warning:** turn predicted RUL into a *defined alert proxy* and evaluate warning behavior. It is **not** the true physical onset of degradation.

### Subquestions

1. How much does a Random Forest improve over a constant-median baseline on FD001?
2. Do alternative regressors and causal temporal features improve unseen-engine error without data leakage?
3. How sensitive are alerts to chosen RUL thresholds, persistence rules and model errors?
4. How do sensor behavior and operating regimes differ across FD001–FD004, and what generalization limitations result?

## 3. Hypotheses — to test, not established findings

| ID | Proposed hypothesis | Evidence needed |
| --- | --- | --- |
| H1 | Sensor-based RUL regression beats a constant-median baseline on unseen FD001 engines. | MAE/RMSE from engine-disjoint validation and official test. |
| H2 | Causal temporal features improve RUL prediction compared with instantaneous measurements. | Controlled comparison with identical engine splits and train-only preprocessing. |
| H3 | An alert rule using estimated RUL can provide nonzero lead time before simulated failure, at the cost of some false or premature warnings. | Per-engine alert timeline, lead-time distribution, alert rate and sensitivity to thresholds. |
| H4 | Models trained on FD001 may not generalize unchanged to multi-condition subsets. | FD002/FD004 condition analysis and, if feasible, explicit cross-subset evaluation. |

**Existing evidence for H1 only:** a locally evaluated FD001 Random Forest produced **13.50 MAE / 18.07 RMSE cycles** on the official 100-engine test, versus **39.08 / 49.82** for the constant-median predictor. See [baseline experiment](../../rul-baseline.md). This is an initial result, not proof of H2–H4.

## 4. Dataset and experimental unit

- NASA C-MAPSS contains `FD001`, `FD002`, `FD003`, `FD004`; each subset has training trajectories, truncated test trajectories and test RUL labels.
- Observation unit: one engine at one cycle; evaluation grouping unit: **engine**.
- FD001 is the first modeling subset. Other subsets are initially used for comparative EDA.
- Input: cycle index, 3 operational settings, 21 sensor measurements; optional **causal** rolling-window features after implementation.
- Output: predicted RUL (simulated cycles); later, a categorical warning state and time-stamped alert history.

## 5. Experimental design and safeguards

1. Split training/validation by engine ID. Never distribute rows of the same engine across both partitions.
2. Fit transformations, sensor filters and model selection on training engines only.
3. Use partial engine histories for evaluation; never expose future cycles as model features.
4. Treat NASA's official test as a held-out benchmark, not a hyperparameter search set.
5. Repeat engine-level validation to assess variability; report seed/split details.
6. Separate descriptive plots, predictive performance and alert performance in the results.
7. Document generated data artifacts and commands, while excluding raw NASA files from Git.

## 6. Proposed success criteria (team to ratify)

### Research / model quality
- **Required:** reproduce a deterministic FD001 baseline and report engine-level MAE and RMSE, alongside the constant-median reference.
- **Required:** demonstrate no overlap of engine IDs in the internal training and validation partitions.
- **Required:** report errors and limitations on at least one official held-out dataset.
- **Target (proposed, not promised):** selected model improves over the median baseline on both MAE and RMSE without test-set tuning.
- **Stretch:** repeated engine-level splits, uncertainty intervals and ablation experiments.

### Early-warning quality
- **Required for MVP:** define the warning target and alert rule **before** evaluating it; report threshold, persistence and assumptions.
- **Required for MVP:** show per-engine alert timing, false/premature alert definition and lead time relative to simulated failure.
- **Required:** explain that this is a proxy evaluation; exact physical degradation onset is unknown.
- **Stretch:** threshold sensitivity analysis and calibrated warning levels.

### Software and presentation
- **Required:** runnable local end-to-end demonstration for a selected engine.
- **Required:** readable RUL trajectory, current status, relevant sensors and warning explanation.
- **Required:** source, tests, reproducibility commands, sprint evidence, model limitations and final presentation.
- **Not in scope:** real-time flight integration, real-world flight safety claims, certification, physical fault localization.

## 7. Planned MVP user journey (proposal)

1. A reviewer opens the dashboard and selects an FD001 test engine.
2. The app replays only the observations available up to the chosen cycle.
3. The model estimates RUL from the observed history.
4. A clearly labeled **research-proxy** alert rule assigns a warning state.
5. The user sees an RUL trend, sensor traces, the alert timeline and model limitations.
6. The reviewer can compare predicted and known test RUL **for evaluation**, without leaking that ground truth into predictions.

## 8. Decisions pending with the team/professor

- [ ] Confirm the final primary research question and exact course expectations.
- [ ] Confirm which subsets are in final modeling scope (FD001 only vs FD002–FD004).
- [ ] Agree on the early-warning proxy, threshold selection and alert metrics (#13).
- [ ] Confirm whether the dashboard is mandatory MVP or a stretch goal.
- [ ] Record date, attendees and written evidence of professor approval; **do not mark approved without confirmation**.
- [ ] Assign ownership of future issues to teammates.

## 9. Implementation references

- `docs/architecture.md` — architecture draft and cautions (some planned status text may be stale).
- `src/aero_sentinel/data.py` — schema/ingestion.
- `src/aero_sentinel/rul_baseline.py` — initial FD001 RUL baseline.
- `docs/rul-baseline.md` — experimental details and measured results.
- Issues [#13](https://github.com/GreciaBarraganPaez/aero-sentinel/issues/13), [#21](https://github.com/GreciaBarraganPaez/aero-sentinel/issues/21), [#24](https://github.com/GreciaBarraganPaez/aero-sentinel/issues/24) — later product requirements and alert design.

## Suggested discussion prompts

- Should we prioritize reliable RUL estimates or an explainable early-warning demonstration when trade-offs arise?
- What would count as a *useful* warning if the actual onset of damage is not labeled?
- Which false-alert cost matters in the simulated setting, and how should we communicate it?
- How can we avoid overclaiming aviation relevance from synthetic data?

**Issue #1 closed:** 2026-10-27 09:46:48 UTC, on the basis of documented research scope and owner-reported professor approval. See [closure record](issue-01-closure.md). Final operational alert details remain in #13/#21.
