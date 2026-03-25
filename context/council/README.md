# Prismtek Council System

This system defines how council-mode answers are scored, selected, and audited.

## Core Rules

1. **Strict Mode is enabled** (`context/council/STRICT_MODE.md`).
2. **All active council members may participate** for council-mode questions.
3. **Each candidate is scored 1-5 across:**
   - correctness
   - clarity
   - safety
   - actionability
4. **Highest score wins** (subject to the safety gate).
5. **Any candidate with a safety score of 1 is vetoed.**
6. **All rounds may be logged** in `data/council/votes.jsonl`.
7. **Ties are resolved by Prismo.**

## Rotation / Termination Policy

A member is marked for review when both are true:

- `zero_vote_streak >= 10 council rounds`
- `selection_rate_30 < 5%`

Replacement process:

1. Mark member `retired` in `context/council/roster.yaml`.
2. Add replacement member in `active` or `probation` status.
3. Re-run the audit and review outcomes before adopting the change.

## Files

- `context/council/roster.yaml` — active/retired/probation members
- `context/council/voting-rubric.md` — scoring guide
- `context/council/replacement-playbook.md` — replacement workflow
- `data/council/votes.jsonl` — append-only round log
- `scripts/council_audit.py` — participation audit + replacement recommendations
- `scripts/council_daily_audit.sh` — daily audit snapshot writer

## Daily Automation

Run manually:

```bash
bash scripts/council_daily_audit.sh
```

Outputs:

- `data/council/audit-latest.txt`
- `data/council/audit-<timestamp>.txt`

## Council Mode Trigger

Use council mode for:

- architecture decisions
- strategy decisions
- risky releases
- major UX/product choices
- model/tooling policy decisions
