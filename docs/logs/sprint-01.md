# Sprint 01 — Development & Evidence Log

**Project:** Aero Sentinel  
**Period:** CW 43–44, 2026  
**Sprint update:** CW 45  
**Status:** Partial evidence recorded on 2026-10-26; CW45 update pending

## Sprint goal

Define the project scope and establish a reproducible exploratory analysis of NASA C-MAPSS FD001 sensor data.

## Planned issues

- [x] #1 Define research scope and success criteria — closed 2026-10-27 09:46:48 UTC; [closure](../sprints/sprint-01/issue-01-closure.md)
- [x] #2 Download and document NASA C-MAPSS FD001 — closed 2026-10-27 09:46:52 UTC; [closure](../sprints/sprint-01/issue-02-closure.md); integrity follow-up #33
- [x] #3 Inspect dataset schema and quality — closed 2026-10-26 14:22:21 UTC; [evidence](../sprints/sprint-01/issue-03-data-schema-quality.md)
- [ ] #4 Exploratory analysis of sensor behavior
- [x] #5 Establish repository workflow and reproducibility — closed 2026-10-27 09:46:57 UTC; [closure](../sprints/sprint-01/issue-05-closure.md); team verification follow-up #34
- [ ] #6 Prepare sprint update and evidence log

- [x] #9 FD001 Random Forest RUL baseline — closed 2026-10-26 14:24:42 UTC; [evidence](../sprints/sprint-01/issue-09-rul-baseline.md)

## Grecia's assigned-issue documentation (prepared 2026-10-26)

- [#1 research scope and hypotheses](../sprints/sprint-01/grecia-research-scope.md): proposed research question, hypotheses, metrics, MVP scope and **pending** professor/team approval.
- [#2 dataset provenance](../sprints/sprint-01/grecia-dataset-provenance.md): NASA source attribution, local data structure, hash commands and **pending** verified manifest.
- [#4 EDA notes](../sprints/sprint-01/grecia-eda-notes.md): exact implemented plots, scientific cautions, and **proposed** deeper analysis.
- [#5 workflow](../sprints/sprint-01/grecia-workflow-reproducibility.md): Git/PR process, documentation gate, team verification matrix and **pending** teammate checks.
- Closed issues [#3](../sprints/sprint-01/issue-03-data-schema-quality.md) and [#9](../sprints/sprint-01/issue-09-rul-baseline.md) have separate historical closure records.

**Note:** these new notes document progress; they do not close #1, #2, #4 or #5 or claim unverified approvals, hashes or team test runs.

## Work completed

- GreciaBarraganPaez: C-MAPSS schema and quality validation, dataset summaries and synthetic tests ([PR #7](https://github.com/GreciaBarraganPaez/aero-sentinel/pull/7)).
- GreciaBarraganPaez: FD001 Random Forest RUL baseline, holdout/test evaluation and tests ([PR #8](https://github.com/GreciaBarraganPaez/aero-sentinel/pull/8)).
- Full closure records: [Sprint 01 completed index](../sprints/sprint-01/README.md).

## Findings and results

Local run on 2026-10-26: 10 unit tests passed. FD001 official test Random Forest MAE 13.50 cycles, RMSE 18.07 cycles (100 engines); see [experiment record](../sprints/sprint-01/issue-09-rul-baseline.md). No GitHub CI run was claimed.

## Decisions and rationale

Validation uses engine-disjoint splits; training RUL capped at 125 cycles. C-MAPSS does not label exact physical degradation onset, so RUL accuracy is not proof of early-warning quality.

## Blockers and risks

Open: team setup verification (#34), raw-file integrity/provenance (#33), deeper EDA (#4), repeated validation, early-warning protocol (#13), and CW45 presentation (#6).

## Evidence

| Item | Link | What it demonstrates |
| --- | --- | --- |
| [#3](https://github.com/GreciaBarraganPaez/aero-sentinel/issues/3) / [PR #7](https://github.com/GreciaBarraganPaez/aero-sentinel/pull/7) | [closure record](../sprints/sprint-01/issue-03-data-schema-quality.md) | Schema/quality validation |
| [#9](https://github.com/GreciaBarraganPaez/aero-sentinel/issues/9) / [PR #8](https://github.com/GreciaBarraganPaez/aero-sentinel/pull/8) | [closure record](../sprints/sprint-01/issue-09-rul-baseline.md) | RUL model and metrics |
| Code | `src/aero_sentinel/data.py`, `dataset_overview.py`, `rul_baseline.py` | Reproducible analysis/model |
| Generated results (local, gitignored) | `results/figures/` | Plots and JSON/CSV reports; not committed |

## AI coding-agent usage (if applicable)

| Date | Tool | Task / prompt summary | Output used | How it was verified |
| --- | --- | --- | --- | --- |
| 2026-10-26 | ChatGPT + GitHub integration | Draft code, tests, docs for data and RUL baseline | Merged PRs #7 and #8 | Local pytest: 10 passed; model metrics from local run; no CI |

## Sprint review

**What was achieved:** data schema/quality pipeline and first FD001 RUL baseline; see [completed evidence](../sprints/sprint-01/README.md)  
**What remains open:** #4 and #6 are open; raw-file integrity/team reproduction are tracked in follow-ups #33 and #34; CW45 update not yet delivered  
**Next sprint priorities:** #21 MVP requirements, #22 preprocessing, #13 alert protocol

> Keep this log factual: planned work is not evidence of completed work.

## Issue closure update — 2026-10-27

- #1 closed 09:46:48 UTC — professor approval reported by project owner; scope and research limitations documented. Formal approval artifact was not independently retrieved.
- #2 closed 09:46:52 UTC — acquisition/setup documentation complete; unverified NASA archive metadata, raw-file SHA-256 and teammate reproduction transferred to #33.
- #5 closed 09:46:57 UTC — repository/workflow documentation complete; unverified teammate environment execution and hygiene checks transferred to #34.
- Detailed records: [#1](../sprints/sprint-01/issue-01-closure.md), [#2](../sprints/sprint-01/issue-02-closure.md), [#5](../sprints/sprint-01/issue-05-closure.md).

**No new tests or hash computations were run for this closure update.**
