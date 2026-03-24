#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / "skills" / "index.json"
MEMORY_PATH = ROOT / "skills" / "memory.json"

STOPWORDS = {
    "the", "and", "for", "with", "that", "this", "from", "into", "have", "been",
    "again", "after", "before", "while", "when", "where", "there", "their", "your",
    "error", "failed", "failure", "issue", "problem", "debug", "trying", "attempt",
    "worker", "agent", "skill", "apply", "show", "status", "main", "route", "using",
    "cannot", "could", "would", "should", "about", "because", "still", "just", "really",
    "then", "than", "more", "less", "very", "some", "into", "onto", "over", "under",
    "file", "files", "script", "scripts", "json", "text", "input", "command", "commands",
}

WORD_RE = re.compile(r"[a-z0-9]{3,}")


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def dump_json(path: Path, data: dict) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def tokenize(text: str) -> Iterable[str]:
    for token in WORD_RE.findall(text.lower()):
        if token not in STOPWORDS and not token.isdigit():
            yield token


def failed_inputs(memory: dict) -> list[str]:
    return [entry.get("input", "") for entry in memory.get("history", []) if entry.get("success") is False]


def build_candidates(memory: dict, registry: dict, limit: int = 15) -> list[tuple[str, int]]:
    existing = {
        trig.lower()
        for skill in registry.get("skills", {}).values()
        for trig in skill.get("triggers", [])
    }
    counts: Counter[str] = Counter()
    for text in failed_inputs(memory):
        counts.update(tokenize(text))
    candidates = [(token, score) for token, score in counts.most_common() if token not in existing]
    return candidates[:limit]


def apply_candidates(skill: str, triggers: list[str], registry: dict) -> tuple[list[str], list[str]]:
    skills = registry.setdefault("skills", {})
    if skill not in skills:
        raise SystemExit(f"Unknown skill: {skill}")
    current = skills[skill].setdefault("triggers", [])
    current_lower = {t.lower() for t in current}
    added: list[str] = []
    skipped: list[str] = []
    for trigger in triggers:
        if trigger.lower() in current_lower or trigger in STOPWORDS or len(trigger) < 3:
            skipped.append(trigger)
            continue
        current.append(trigger)
        current_lower.add(trigger.lower())
        added.append(trigger)
    return added, skipped


def main() -> None:
    parser = argparse.ArgumentParser(description="Safely evolve skill triggers from failure memory.")
    parser.add_argument("--skill", help="Skill id to receive new triggers.")
    parser.add_argument("--apply", action="store_true", help="Write approved triggers back to skills/index.json.")
    parser.add_argument("--top", type=int, default=8, help="Maximum number of candidate triggers to consider.")
    args = parser.parse_args()

    registry = load_json(REGISTRY_PATH)
    memory = load_json(MEMORY_PATH)
    candidates = build_candidates(memory, registry, limit=max(args.top, 1))

    if not candidates:
        print("No new candidate triggers found.")
        return

    print("Candidate triggers:")
    for token, score in candidates:
        print(f"- {token} ({score})")

    if not args.apply:
        print("\nDry run only. Use --skill <id> --apply to write approved triggers.")
        return

    if not args.skill:
        raise SystemExit("--skill is required with --apply")

    selected = [token for token, _ in candidates[: args.top]]
    added, skipped = apply_candidates(args.skill, selected, registry)
    dump_json(REGISTRY_PATH, registry)

    print(f"\nApplied to skill: {args.skill}")
    print(f"Added: {', '.join(added) if added else '(none)'}")
    print(f"Skipped: {', '.join(skipped) if skipped else '(none)'}")


if __name__ == "__main__":
    main()
