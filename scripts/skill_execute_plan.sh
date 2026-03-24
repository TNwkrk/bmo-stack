#!/usr/bin/env bash
set -euo pipefail

PLAN="${1:-}"

[ -f "$PLAN" ] || {
  echo "Plan not found: $PLAN" >&2
  exit 1
}

command -v jq >/dev/null 2>&1 || {
  echo "Missing dependency: jq" >&2
  exit 1
}

echo "[plan] executing $PLAN"

jq -c '.steps[]' "$PLAN" | while IFS= read -r step; do
  name=$(printf '%s' "$step" | jq -r '.name')
  cmd=$(printf '%s' "$step" | jq -r '.run')

  echo "[step] $name"
  echo "[cmd] $cmd"

  eval "$cmd"
done

echo "[plan] complete"
