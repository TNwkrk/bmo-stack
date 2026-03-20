#!/usr/bin/env bash

# recover-session: Print recovery information for session restart

set -euo pipefail

HOST_CONTEXT_DIR="$HOME/bmo-context"
WORKSPACE_DIR="$HOME/.openclaw/workspace"
BMO_STACK_DIR="$WORKSPACE_DIR/bmo-stack"

echo "=== Host Context Files ==="
for file in BOOTSTRAP.md SESSION_STATE.md SYSTEMMAP.md RUNBOOK.md BACKLOG.md; do
    path="$HOST_CONTEXT_DIR/$file"
    if [ -f "$path" ]; then
        echo "✓ $path exists"
    else
        echo "✗ $path missing"
    fi
done

echo ""
echo "=== Task State Files ==="
for file in TASK_STATE.md WORK_IN_PROGRESS.md; do
    path="$HOST_CONTEXT_DIR/$file"
    if [ -f "$path" ]; then
        echo "✓ $path exists"
    else
        echo "✗ $path missing"
    fi
done

echo ""
echo "=== Git Status (if bmo-stack exists) ==="
if [ -d "$BMO_STACK_DIR" ]; then
    echo "Repository: $BMO_STACK_DIR"
    cd "$BMO_STACK_DIR"
    echo "Branch: $(git rev-parse --abbrev-ref HEAD)"
    echo "Status:"
    git status --porcelain
    echo ""
    echo "Last 5 commits:"
    git log --oneline -5
else
    echo "bmo-stack directory not found at $BMO_STACK_DIR"
fi

echo ""
echo "=== Safe to Resume? ==="
if [ -f "$HOST_CONTEXT_DIR/TASK_STATE.md" ]; then
    # Look for the last checkpoint in TASK_STATE.md
    # We'll check the last checkpoint entry for "Safe to resume: true"
    # This is a simple check; in practice, we might want to parse more carefully.
    if grep -q "Safe to resume: true" "$HOST_CONTEXT_DIR/TASK_STATE.md"; then
        echo "✓ Safe to resume (based on last checkpoint in TASK_STATE.md)"
    else
        echo "✗ Not safe to resume or unable to determine"
    fi
else
    echo "? TASK_STATE.md not found, assume not safe"
fi