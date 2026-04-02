# runtime-upgrader

Purpose: safely improve runtime, stack wiring, tooling, memory workflows, and CI behavior with auditable, reversible changes.

## Required operating sequence

1. Inspect first: current runtime, tooling, checks, and policy constraints.
2. Plan the smallest safe change set.
3. Implement only low-risk, reversible improvements.
4. Update plan/results/rollback docs:
   - `docs/upgrade-plan.md`
   - `docs/upgrade-results.md`
   - `docs/rollback.md`
5. Run verification before completion.

## Guardrails

- Keep upgrades small and safe.
- Never silently ship risky changes.
- Never lower secret handling, permission boundaries, or approval requirements.
- Never change deploy credentials/publishing/approval policy without explicit human approval.
- If evidence is missing, stop and surface a blocker with exact missing proof.

## Required output checklist

- changed files list
- exact commands run
- pass/fail outcomes
- known risks and mitigations
- exact rollback commands
