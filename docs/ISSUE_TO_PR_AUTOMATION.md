# Issue to PR Automation

This repository now supports a safer v2 issue-to-PR flow.

## Trigger paths

- label an issue with `autonomy:execute`
- or run the `BMO Issue to PR v2` workflow manually with `workflow_dispatch`

## Execution modes

### Builtin scaffold mode

Used when:
- execution is enabled
- no external executor is configured

Result:
- a draft PR is opened
- the PR contains a reviewable autonomy packet under `.github/autonomy/issues/`
- the issue is referenced, but not auto-closed

This mode is safe by default and does not pretend to have fully implemented the issue.

### External executor mode

Used when:
- execution is enabled
- `BMO_GITHUB_AUTONOMY_EXECUTOR` is configured on a self-hosted runner

Result:
- the workflow hands the plan to the configured local executor
- the executor may produce real code changes
- a draft PR is opened from those changes

## Required repo variables

- `BMO_AUTONOMY_EXECUTION_ENABLED`
  - set to `true` to allow execution beyond the planning comment
- `BMO_GITHUB_AUTONOMY_EXECUTOR`
  - optional
  - if set, enables external executor mode on the self-hosted runner

## Notes

- high-risk issues are still planner-blocked
- builtin mode creates a bounded implementation packet instead of speculative edits
- the generated draft PR should still be reviewed before merge
- the older `autonomy:ready` workflow remains in the repo, but `autonomy:execute` is the intended trigger for the v2 flow
