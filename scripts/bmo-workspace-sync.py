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
DEFAULT_CONTINUITY_OUTPUT = Path("workflows") / "bmo-continuity.json"
DEFAULT_SYNC_OUTPUT = Path("workflows") / "bmo-workspace-sync.json"
DEFAULT_CONTEXT_EXCLUDES = [
    "TASK_STATE.md",
    "WORK_IN_PROGRESS.md",
    "memory.md",
    "MEMORY.md",
    "memory/",
]


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


def sync_context(repo_root: Path, host_context: Path, delete: bool, excludes: list[str]) -> list[dict[str, object]]:
    steps: list[dict[str, object]] = []
    repo_context = repo_root / "context"
    if host_context.exists() and repo_context.exists() and shutil.which("rsync"):
        cmd = ["rsync", "-av"]
        if delete:
            cmd.append("--delete")
        for item in excludes:
            cmd.extend(["--exclude", item])
        cmd.extend([f"{repo_context}/", f"{host_context}/"])
        steps.append(run(cmd))
    return steps


def maybe_refresh_continuity(repo_root: Path, surface: str, output_path: Path, publish: bool) -> list[dict[str, object]]:
    steps: list[dict[str, object]] = []
    node = shutil.which("node")
    script_path = repo_root / "scripts" / "bmo-continuity-report.mjs"
    if not node or not script_path.exists():
        return steps

    cmd = [node, str(script_path), "--surface", surface, "--output", str(output_path)]
    if publish:
        cmd.append("--publish")
    steps.append(run(cmd, cwd=repo_root))
    return steps


def mirror_continuity_snapshot(repo_root: Path, output_path: Path) -> list[dict[str, object]]:
    steps: list[dict[str, object]] = []
    if not output_path.exists():
        return steps

    target = repo_root / "context" / "continuity" / "live-status.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(output_path, target)
    steps.append(
        {
            "cmd": ["copy", str(output_path), str(target)],
            "cwd": str(repo_root),
            "returncode": 0,
            "stdout": f"Mirrored continuity snapshot to {target}\n",
            "stderr": "",
        }
    )
    return steps


def resolve_workspace_path(workspace_dir: Path, value: str) -> Path:
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = workspace_dir / path
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description="Keep the local OpenClaw workspace aligned with bmo-stack.")
    parser.add_argument("--repo-url", default=os.environ.get("BMO_STACK_REPO_URL", DEFAULT_REPO_URL))
    parser.add_argument("--workspace-dir", default=os.environ.get("BMO_OPENCLAW_WORKSPACE_DIR", str(DEFAULT_WORKSPACE)))
    parser.add_argument("--host-context", default=os.environ.get("BMO_HOST_CONTEXT_DIR", str(DEFAULT_CONTEXT_HOST)))
    parser.add_argument("--delete-context", action="store_true", help="Delete files from host context that are absent in repo context.")
    parser.add_argument("--exclude", action="append", default=[], help="Additional rsync exclude patterns for context sync.")
    parser.add_argument(
        "--output",
        default=os.environ.get("BMO_WORKSPACE_SYNC_OUTPUT", str(DEFAULT_SYNC_OUTPUT)),
    )
    parser.add_argument("--continuity-surface", default=os.environ.get("BMO_CONTINUITY_SURFACE", "macbook"))
    parser.add_argument(
        "--continuity-output",
        default=os.environ.get("BMO_CONTINUITY_OUTPUT", str(DEFAULT_CONTINUITY_OUTPUT)),
    )
    parser.add_argument(
        "--publish-continuity",
        action="store_true",
        default=os.environ.get("BMO_CONTINUITY_PUBLISH", "").lower() == "true",
    )
    args = parser.parse_args()

    workspace_dir = Path(args.workspace_dir).expanduser()
    host_context = Path(args.host_context).expanduser()
    continuity_output = resolve_workspace_path(workspace_dir, args.continuity_output)
    output = resolve_workspace_path(workspace_dir, args.output)
    excludes = DEFAULT_CONTEXT_EXCLUDES + list(args.exclude)

    payload = {
        "repo_url": args.repo_url,
        "workspace_dir": str(workspace_dir),
        "host_context": str(host_context),
        "delete_context": args.delete_context,
        "excludes": excludes,
        "continuity_surface": args.continuity_surface,
        "continuity_output": str(continuity_output),
        "publish_continuity": args.publish_continuity,
        "output": str(output),
        "steps": [],
    }
    payload["steps"].extend(ensure_repo(workspace_dir, args.repo_url))
    payload["steps"].extend(
        maybe_refresh_continuity(workspace_dir, args.continuity_surface, continuity_output, args.publish_continuity)
    )
    payload["steps"].extend(mirror_continuity_snapshot(workspace_dir, continuity_output))
    payload["steps"].extend(sync_context(workspace_dir, host_context, args.delete_context, excludes))

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
