# Issue #5 — Repository workflow, reproducibility and team handoff

**Owner:** GreciaBarraganPaez  
**Sprint:** Sprint 1 (CW43–44, 2026)  
**Issue:** [#5](https://github.com/GreciaBarraganPaez/aero-sentinel/issues/5)  
**Status:** Initial workflow implemented; independent teammate verification **pending**  
**Prepared:** 2026-10-26

## 1. Repository organization

```text
aero-sentinel/
  .github/
    PULL_REQUEST_TEMPLATE.md         # PR description / closure-comment draft
    workflows/pr-documentation.yml   # PR documentation gate
  src/aero_sentinel/
    data.py                           # NASA file parsing and quality
    first_data_test.py                # FD001 descriptive analysis
    dataset_overview.py               # FD001–FD004 comparison
    rul_baseline.py                   # FD001 Random Forest baseline
  tests/                              # synthetic unit tests
  docs/
    architecture.md
    data-analysis-setup.md
    rul-baseline.md
    logs/sprint-01.md
    sprints/sprint-01/                # versioned issue evidence
  data/raw/                           # local NASA data, not committed
  results/figures/                    # locally generated outputs, not committed
  pyproject.toml
```

## 2. Contribution workflow

1. Select or receive an assigned GitHub issue and confirm acceptance criteria.
2. Pull the latest `main` and create a focused feature branch.
3. Implement code and tests, avoiding raw datasets and secrets.
4. Add/update matching `docs/sprints/sprint-XX/*.md` in the same PR.
5. Create a PR with the auto-filled template, including the issue link, exact source/test paths, reproduction commands, limitations and issue closure comment draft.
6. Wait for `documentation-gate` and other required checks to pass; request review according to the current ruleset.
7. Merge only after checks and human review requirements are satisfied.
8. When the issue is truly completed, add the final issue comment with the real closure timestamp and versioned evidence link.

The PR documentation gate is implemented in [PR #31](https://github.com/GreciaBarraganPaez/aero-sentinel/pull/31). Whether it is **currently required** by the live branch ruleset must be checked separately; do not infer enforcement from the existence of a workflow file.

## 3. Recommended Git commands (PowerShell)

```powershell
git switch main
git pull origin main
git switch -c feature/issue-NN-short-name
# Edit code, tests and docs.
python -m pytest -q
git status
git add src tests docs
git commit -m "feat: implement issue NN with sprint evidence"
git push -u origin feature/issue-NN-short-name
```

Create the PR on GitHub, fill the auto-populated template and link `Related to #NN` or `Closes #NN` as appropriate.

## 4. Reproducibility

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m pytest -q
python -m aero_sentinel.first_data_test
python -m aero_sentinel.dataset_overview
python -m aero_sentinel.rul_baseline
```

Requires separately downloaded NASA files under `data/raw/`. Locally generated reports are under `results/figures/`. Full instructions: [data analysis setup](../../data-analysis-setup.md) and [dataset provenance](grecia-dataset-provenance.md).

## 5. Existing verification (historical)

- Merged PR [#7](https://github.com/GreciaBarraganPaez/aero-sentinel/pull/7): data ingestion/EDA and initial tests.
- Merged PR [#8](https://github.com/GreciaBarraganPaez/aero-sentinel/pull/8): FD001 RUL baseline and tests.
- Merged PR [#30](https://github.com/GreciaBarraganPaez/aero-sentinel/pull/30): completed-issue evidence.
- Merged PR [#31](https://github.com/GreciaBarraganPaez/aero-sentinel/pull/31): PR documentation template and gate.
- A local run on 2026-10-26 reported **10 tests passed** across the data and RUL modules. No claim is made that teammates independently reproduced it or that GitHub Actions tests have run.

## 6. Team verification matrix — to be filled with real evidence

| Contributor | Install + pytest | NASA file integrity | FD001 EDA | FD001 RUL run | Date / evidence |
| --- | --- | --- | --- | --- | --- |
| GreciaBarraganPaez | Historical local run: 10 tests passed | Hashes pending | Historical local run | Historical local run | 2026-10-26; [baseline report](../../rul-baseline.md) |
| Teammate A (GitHub handle pending) | Pending | Pending | Pending | Pending | Pending |
| Teammate B (GitHub handle pending) | Pending | Pending | Pending | Pending | Pending |

## 7. Security and quality checklist

- [ ] Verify `git status` and `git diff --cached --name-only` before every push.
- [ ] Ensure `data/raw/`, `.venv/`, model weights, large generated outputs and secrets are ignored.
- [ ] Verify no passwords, API keys or personal information are committed.
- [ ] Use engine-wise train/validation splits and train-only transformations.
- [ ] Check that PR docs match actual code and test outcomes.
- [ ] Record coding-assistant usage and independent verification in sprint logs.

These are process requirements, **not** a claim that every contributor has already completed them.

## 8. Open decisions / next steps

- [ ] Obtain GitHub usernames of all contributors and assign issues.
- [ ] Ask each teammate to run setup, tests and FD001 analysis independently.
- [ ] Compare hashes and file sizes against the same NASA archive.
- [ ] Confirm `documentation-gate` runs successfully on a new PR and is required by the branch ruleset.
- [ ] Add automated unit-test CI if desired ([#20](https://github.com/GreciaBarraganPaez/aero-sentinel/issues/20)).
- [ ] Record the verified team results in `docs/logs/sprint-01.md`.

**Closure condition for #5:** reproducibility and ignore-rule checks verified across the team. Documentation alone does not complete that verification.
