# Work In Progress

Last updated: 2026-03-27 10:45 UTC

## Current focus

- Active mission: clean up the remaining stale operator surfaces after the merged BMO operating-system pass.
- Why now: the repo still had a misleading README, a stale backlog, and helper scripts that existed but were not wired into the real operator path.
- Owner paths in play:
  - `README.md`
  - `context/BACKLOG.md`
  - `Makefile`
  - `scripts/bmo-context-reseed`
  - `scripts/bmo-worker-status`

## Current work packet

- make `worker-status` report the current merged state instead of a stale checkpoint-tail format
- make `context-reseed` a real first-class Make target
- make the dry-run path safe and informative
- remove stale `openclaw-start` and `openclaw-status` promises from the README
- refresh the backlog so it points at the true remaining work

## Next milestone

- rerun validation
- package the cleanup on a reviewable branch
- push it for GitHub checks

## Risks and watchouts

- do not claim runtime behavior changed; this pass is about the operator surface in `bmo-stack`
- keep `worker-status` and `context-reseed` useful on machines that do not have `openclaw` or `openshell` installed
