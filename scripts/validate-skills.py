#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "skills" / "index.json"


def fail(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    skills = data.get("skills")
    if not isinstance(skills, dict):
        fail("skills must be an object")

    for name, spec in skills.items():
        if not isinstance(spec, dict):
            fail(f"skill '{name}' must be an object")

        triggers = spec.get("triggers")
        if not isinstance(triggers, list) or not triggers:
            fail(f"skill '{name}' must have non-empty triggers list")

        if any(not isinstance(t, str) or not t.strip() for t in triggers):
            fail(f"skill '{name}' has invalid trigger entries")

        if len({t.lower() for t in triggers}) != len(triggers):
            fail(f"skill '{name}' has duplicate triggers (case-insensitive)")

        actions = spec.get("actions")
        if not isinstance(actions, list) or not actions:
            fail(f"skill '{name}' must have non-empty actions list")

        default_action = spec.get("default_action")
        if default_action not in actions:
            fail(f"skill '{name}' default_action must be one of actions")

    print("skills/index.json is valid")


if __name__ == "__main__":
    main()
