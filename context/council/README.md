# Prismtek Council System

This system defines how all agents participate in answer voting, how outcomes are recorded, and how low-performing members are rotated out.

## Core Rules

1. **Strict Mode is enabled** (`COUNCIL/STRICT_MODE.md`).
2. **All council agents are called for every council-mode question.**
2. **Every agent must submit one answer candidate.**
3. **Each candidate is scored 1-5 across:**
   - correctness
   - clarity
   - safety
   - actionability
4. **Highest score wins** (subject to safety gate).
5. **Reality Checker can veto unsafe answers.**
6. **All votes and participation are logged** in `data/council/votes.jsonl`.
7. **Members with no received votes over threshold windows are removed and replaced.**

## Rotation / Termination Policy

A member is marked for removal when BOTH are true:
- `zero_vote_streak >= 10 council rounds`
- `selection_rate < 5% over last 30 rounds`

Replacement process:
1. Mark member `retired` in roster.
2. Add replacement member in `active` status.
3. Start replacement on probation for 10 rounds.

## Files

- `COUNCIL/roster.yaml` — active/retired/probation members
- `COUNCIL/voting-rubric.md` — scoring guide
- `COUNCIL/replacement-playbook.md` — replacement workflow
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
