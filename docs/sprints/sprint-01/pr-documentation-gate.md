# Sprint 1 — PR documentation gate setup

**Owner:** GreciaBarraganPaez  
**Sprint:** Sprint 1  
**Status:** Proposed (not yet merged or enforced)  
**Implementation:** `feature/pr-documentation-gate`

## What was implemented

- `.github/PULL_REQUEST_TEMPLATE.md` automatically pre-fills PR description sections and a draft for the eventual issue closure comment.
- `.github/workflows/pr-documentation.yml` validates the PR sections, linked issue, matching sprint documentation path and changed Markdown record. It is designed to post an initial guidance comment when a PR is opened.
- `docs/sprints/README.md` documents the workflow, reproducibility requirements and post-closure process.

## Where it lives

- `.github/PULL_REQUEST_TEMPLATE.md`
- `.github/workflows/pr-documentation.yml`
- `docs/sprints/README.md`

## Verification

Static review of configuration and paths; **no GitHub Actions execution has yet been verified**. Validate the gate on a new PR after merging this workflow to `main`.

## Remaining manual setup

Add the **documentation-gate** check as a required status check to the `main` branch ruleset. Until then, a failed check is informational and will not enforce a merge block.

## Limitations

- This gate checks documented structure, not whether scientific claims are correct or unit tests actually passed.
- The real issue close date and final issue comment are only possible after closing the issue; PRs carry a draft until then.
- The workflow deliberately never checks out or runs untrusted PR code.
