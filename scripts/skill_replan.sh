#!/usr/bin/env bash
set -euo pipefail

python3 scripts/skill_reflect.py
python3 scripts/skill_goal_plan.py --goal "fix recent failures" --output reflection-plan.json
./scripts/skill_execute_plan.sh workflows/reflection-plan.json
