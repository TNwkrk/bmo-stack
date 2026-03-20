# Council Replacement Playbook

## Removal trigger
A member is removed when:
- zero_vote_streak >= 10 rounds
- selection_rate < 5% over last 30 rounds

## Process
1. Mark agent as `retired` in `COUNCIL/roster.yaml`.
2. Add replacement agent with `status: probation`.
3. Run probation for 10 rounds.
4. Promote to `active` if:
   - receives at least 2 winning votes
   - has no safety veto incidents

## Candidate qualities for replacement
- stronger domain perspective than retired role
- clear, concise communication
- measurable output quality on rubric

## Suggested replacement roles
- Systems Architect
- Gameplay Designer
- DevOps Reliability Engineer
- Data/Analytics Strategist
- UX Researcher
