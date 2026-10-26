# Aero Sentinel — Sprint documentation policy

Every Pull Request must have an automatically filled [PR description template](../../.github/PULL_REQUEST_TEMPLATE.md) and pass the [PR documentation gate](../../.github/workflows/pr-documentation.yml).

## Before PR approval or merge

1. Fill all sections of the PR template (Sprint, linked issue, summary, code paths, sprint documentation, verification, limitations and issue closure comment draft). Remove every `TODO`.
2. Add/update a Markdown evidence record **in the same PR** under `docs/sprints/sprint-01/`, `sprint-02/`, `sprint-03/`, `sprint-04/`, `delivery/` or `ongoing/`. Use the matching Sprint value.
3. Link the exact changed documentation path in the PR description.
4. Include real reproduction commands and actual results. Do not claim tests that have not been run.
5. A reviewer verifies the factual content. The automated gate checks structure and changed filenames, **not** scientific accuracy.

## After closing an issue

1. Verify acceptance criteria and link the merged PR/commit.
2. Record the **actual** GitHub `closed_at` UTC timestamp in its sprint closure record; before closure use `Pending`.
3. Post a final GitHub issue comment with sprint, owner, what was delivered, source/test paths, reproduction/verification, limitations and a link to the versioned record.
4. Update the sprint index and commit the final closure timestamp if it was not available at PR time.

**Important:** A final issue closure timestamp/comment cannot be required *before* PR merge because closing usually happens as a result of merging. The PR gate therefore requires a draft comment and versioned evidence before merge; the final issue comment is a post-closure responsibility.

## Activate the mandatory merge block

The workflow creates a status check named **`documentation-gate`**. A repository administrator must add that exact check as a **required status check** in the ruleset protecting `main`. Otherwise a failing check does not automatically prevent merging.

The workflow triggers for new/updated PRs and posts an initial guidance comment when a PR is opened. It reads only PR metadata via the GitHub API and never executes untrusted PR code.

## Recommended closure record format

```markdown
# Issue #NN — Short title
- Sprint:
- Owner:
- Status: Pending / Done
- Closed at (UTC): Pending until actually closed
- Linked issue:
- Implementation PR and commit:
## What was implemented
## Where the source and tests live
## Reproduction commands
## Observed results and tests
## Limitations and follow-up issues
## Final issue comment link
```

Historical Sprint 1 completed records are being added in documentation PR #30.
