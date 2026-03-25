#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path

DEFAULT_REPO_URL = "https://github.com/codysumpter-cloud/bmo-stack.git"
DEFAULT_WORKSPACE = Path.home() / ".openclaw" / "workspace" / "bmo-stack"
DEFAULT_CONTEXT_HOST = Path.home() / "bmo-context"


def run(cmd: list[str], cwd: Path | None = None) -> dict[str, object]:
    completed = subprocess.run(cmd, cwd=str(cwd) if cwd else None, capture_output=True, text=True, check=False)
    return {
        "cmd": cmd,
        "cwd": str(cwd) if cwd else None,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def ensure_repo(path: Path, repo_url: str) -> list[dict[str, object]]:
    steps: list[dict[str, object]] = []
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        steps.append(run(["git", "clone", repo_url, str(path)]))
        return steps
    steps.append(run(["git", "fetch", "--all", "--prune"], cwd=path))
    steps.append(run(["git", "pull", "--ff-only"], cwd=path))
    return steps


def sync_context(repo_root: Path, host_context: Path) -> list[dict[str, object]]:
    steps: list[dict[str, object]] = []
    repo_context = repo_root / "context"
    if host_context.exists() and repo_context.exists() and shutil.which("rsync"):
        steps.append(run(["rsync", "-av", "--delete", f"{repo_context}/", f"{host_context}/"]))
    return steps


def main() -> None:
    parser = argparse.ArgumentParser(description="Keep the local OpenClaw workspace aligned with bmo-stack.")
    parser.add_argument("--repo-url", default=os.environ.get("BMO_STACK_REPO_URL", DEFAULT_REPO_URL))
    parser.add_argument("--workspace-dir", default=os.environ.get("BMO_OPENCLAW_WORKSPACE_DIR", str(DEFAULT_WORKSPACE)))
    parser.add_argument("--host-context", default=os.environ.get("BMO_HOST_CONTEXT_DIR", str(DEFAULT_CONTEXT_HOST)))
    parser.add_argument("--output", default="workflows/bmo-workspace-sync.json")
    args = parser.parse_args()

    workspace_dir = Path(args.workspace_dir).expanduser()
    host_context = Path(args.host_context).expanduser()

    payload = {
        "repo_url": args.repo_url,
        "workspace_dir": str(workspace_dir),
        "host_context": str(host_context),
        "steps": [],
    }
    payload["steps"].extend(ensure_repo(workspace_dir, args.repo_url))
    payload["steps"].extend(sync_context(workspace_dir, host_context))

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
