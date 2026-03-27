# Work In Progress

Last updated: 2026-03-27 11:52 UTC

## Current focus

- Active mission: make the Windows app the strongest practical local BMO workstation shell in this repo.
- Why now: the existing Windows app was installable but still too MVP to serve as the main operator surface for repo control, task supervision, validation, and source control.
- Owner paths in play:
  - `apps/windows-desktop/src/BMO.Desktop.ps1`
  - `apps/windows-desktop/src/BMO.Workstation.ps1`
  - `apps/windows-desktop/src/BMO.Broker.ps1`
  - `apps/windows-desktop/config/workstation-manifest.json`
  - `apps/windows-desktop/policies/capability-policy.example.json`
  - `apps/windows-desktop/config/appsettings.example.json`
  - `apps/windows-desktop/README.md`
  - `docs/WINDOWS_DESKTOP_APP.md`

## Current work packet

- make repo/worktree status and diff inspection first-class in the Windows app
- make task supervision real with cancel, rerun, logs, and persistent history
- make command execution policy-aware with explicit previews and approval gates
- surface routines, validations, skills, and docs from real repo manifests
- add a smoke-testable workstation entrypoint and packaging proof path

## Next milestone

- run the full Windows workstation UI interactively
- decide the next hardening slice after the new workstation baseline
- package follow-up refinements on a review branch if needed

## Risks and watchouts

- do not claim multi-agent orchestration beyond the supervised task capabilities that are actually implemented
- keep command execution inside the explicit allow/prompt/deny policy boundary
- keep BMO-specific operations honest when the chosen workspace is not the canonical `bmo-stack` repo
