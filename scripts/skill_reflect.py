#!/usr/bin/env python3
import json
from pathlib import Path

MEMORY = Path("skills/memory.json")

if not MEMORY.exists():
    print("No memory yet")
    exit(0)

data = json.loads(MEMORY.read_text())
history = data.get("history", [])

total = len(history)
success = sum(1 for x in history if x.get("success"))

print(json.dumps({
    "total": total,
    "success": success,
    "failure": total - success,
    "success_rate": success / total if total else 0
}, indent=2))
