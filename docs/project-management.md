# Aero Sentinel — Project Management

**GitHub Project board:** https://github.com/users/GreciaBarraganPaez/projects/1/views/1  
**Issue tracker:** https://github.com/GreciaBarraganPaez/aero-sentinel/issues

## Workflow

The intended board statuses are:

1. **Backlog** — future tasks not yet selected for a sprint
2. **Todo** — ready to start
3. **In Progress** — work has started
4. **In Review** — deliverable is ready for another team member to review
5. **Done** — acceptance criteria have been checked and evidence is linked

Recommended project fields:
- **Sprint:** Sprint 1, Sprint 2, Sprint 3, Sprint 4
- **Priority:** High, Medium, Low
- **Assignees:** one owner per task (collaborators can review and contribute)

> Note: The board columns and custom fields must be configured in GitHub Projects. This document describes the intended configuration; it does not itself configure the board.

## Sprint schedule (course calendar)

| Sprint | Calendar weeks | Update |
| --- | --- | --- |
| Sprint 1 — Scope & Dataset Exploration | CW 43–44 | CW 45 |
| Sprint 2 — Preprocessing & Evaluation Design | CW 45–46 | CW 47 |
| Sprint 3 — Model Development | CW 47–48 | CW 49 |
| Sprint 4 — Evaluation & Presentation Preparation | CW 49–50 | CW 51 |

The schedule is a working plan aligned with the course's two-week sprint updates; update details as the team agrees with the professor.

## Sprint 1 issues

- #1 — Define research scope and success criteria
- #2 — Download and document NASA C-MAPSS FD001
- #3 — Inspect dataset schema and quality
- #4 — Exploratory analysis of sensor behavior
- #5 — Establish repository workflow and reproducibility
- #6 — Prepare sprint update and evidence log

## Working agreement

- Assign each issue to one primary owner after collaborators join the repository.
- Work in small branches (e.g. `docs/scope`, `data/fd001-inspection`).
- Link issue numbers in pull requests and relevant commits.
- Before moving an issue to **Done**, check its acceptance criteria and link reproducible evidence.
- Keep large raw datasets, model weights, local environment files and secrets out of version control.
- For coding-agent-assisted work, log the tool, its purpose, the generated or modified artifact, and how the result was independently checked.
- At the end of each sprint, summarize outcomes and blockers in `docs/logs/sprint-XX.md`.

## Course deliverables

- Approved project idea with motivation and preliminary sprint plan
- Four sprint updates, usually up to five minutes each
- Final video (~10–15 minutes) by **7 January 2027**
- Shark Tank discussion with buddy group and professor
- Code and documentation by **25 January 2027**

## Dataset caution

NASA C-MAPSS is simulated run-to-failure turbofan data. It does **not** supply ground-truth labels for the precise physical onset of degradation. Do not describe a proxy alert threshold as a validated physical damage onset.
