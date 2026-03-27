#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import plistlib
from pathlib import Path

DEFAULT_LABEL = "cloud.codysumpter.bmo-workspace-sync"
DEFAULT_PLIST = Path.home() / "Library" / "LaunchAgents" / f"{DEFAULT_LABEL}.plist"
DEFAULT_SYNC_SCRIPT = Path(__file__).resolve().with_name("bmo-workspace-sync.py")
DEFAULT_WORKSPACE = Path.home() / ".openclaw" / "workspace" / "bmo-stack"
DEFAULT_HOST_CONTEXT = Path.home() / "bmo-context"
DEFAULT_REPO_URL = "https://github.com/codysumpter-cloud/bmo-stack.git"


def build_plist(
    label: str,
    python_bin: str,
    sync_script: str,
    interval: int,
    repo_url: str,
    workspace_dir: str,
    host_context_dir: str,
    continuity_surface: str,
    continuity_output: str,
    continuity_publish: str,
    continuity_url: str,
    continuity_token: str,
) -> dict[str, object]:
    return {
        "Label": label,
        "ProgramArguments": [python_bin, sync_script],
        "RunAtLoad": True,
        "StartInterval": interval,
        "StandardOutPath": str(Path.home() / "Library" / "Logs" / "bmo-workspace-sync.log"),
        "StandardErrorPath": str(Path.home() / "Library" / "Logs" / "bmo-workspace-sync.err.log"),
        "EnvironmentVariables": {
            "BMO_STACK_REPO_URL": repo_url,
            "BMO_OPENCLAW_WORKSPACE_DIR": workspace_dir,
            "BMO_HOST_CONTEXT_DIR": host_context_dir,
            "BMO_CONTINUITY_SURFACE": continuity_surface,
            "BMO_CONTINUITY_OUTPUT": continuity_output,
            "BMO_CONTINUITY_PUBLISH": continuity_publish,
            "PRISMTEK_CONTINUITY_URL": continuity_url,
            "PRISMTEK_CONTINUITY_TOKEN": continuity_token,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Write a LaunchAgent plist for automatic BMO workspace sync.")
    parser.add_argument("--label", default=DEFAULT_LABEL)
    parser.add_argument("--plist", default=str(DEFAULT_PLIST))
    parser.add_argument("--python-bin", default=os.environ.get("PYTHON_BIN", "/usr/bin/python3"))
    parser.add_argument("--sync-script", default=str(DEFAULT_SYNC_SCRIPT))
    parser.add_argument("--interval-sec", type=int, default=300)
    parser.add_argument("--repo-url", default=os.environ.get("BMO_STACK_REPO_URL", DEFAULT_REPO_URL))
    parser.add_argument("--workspace-dir", default=os.environ.get("BMO_OPENCLAW_WORKSPACE_DIR", str(DEFAULT_WORKSPACE)))
    parser.add_argument("--host-context", default=os.environ.get("BMO_HOST_CONTEXT_DIR", str(DEFAULT_HOST_CONTEXT)))
    parser.add_argument("--continuity-surface", default=os.environ.get("BMO_CONTINUITY_SURFACE", "macbook"))
    parser.add_argument("--continuity-output", default=os.environ.get("BMO_CONTINUITY_OUTPUT", "workflows/bmo-continuity.json"))
    parser.add_argument("--continuity-publish", default=os.environ.get("BMO_CONTINUITY_PUBLISH", "false"))
    parser.add_argument("--continuity-url", default=os.environ.get("PRISMTEK_CONTINUITY_URL", ""))
    parser.add_argument("--continuity-token", default=os.environ.get("PRISMTEK_CONTINUITY_TOKEN", ""))
    parser.add_argument("--output", default="workflows/bmo-launchd-install.json")
    args = parser.parse_args()

    plist_path = Path(args.plist).expanduser()
    plist_path.parent.mkdir(parents=True, exist_ok=True)
    sync_script = str(Path(args.sync_script).expanduser())
    payload = build_plist(
        args.label,
        args.python_bin,
        sync_script,
        args.interval_sec,
        args.repo_url,
        str(Path(args.workspace_dir).expanduser()),
        str(Path(args.host_context).expanduser()),
        args.continuity_surface,
        args.continuity_output,
        args.continuity_publish,
        args.continuity_url,
        args.continuity_token,
    )
    with plist_path.open("wb") as fh:
        plistlib.dump(payload, fh)

    result = {
        "label": args.label,
        "plist": str(plist_path),
        "sync_script": sync_script,
        "interval_sec": args.interval_sec,
        "workspace_dir": payload["EnvironmentVariables"]["BMO_OPENCLAW_WORKSPACE_DIR"],
        "host_context": payload["EnvironmentVariables"]["BMO_HOST_CONTEXT_DIR"],
        "repo_url": payload["EnvironmentVariables"]["BMO_STACK_REPO_URL"],
        "continuity_surface": payload["EnvironmentVariables"]["BMO_CONTINUITY_SURFACE"],
        "continuity_output": payload["EnvironmentVariables"]["BMO_CONTINUITY_OUTPUT"],
        "continuity_publish": payload["EnvironmentVariables"]["BMO_CONTINUITY_PUBLISH"],
        "continuity_url_configured": bool(payload["EnvironmentVariables"]["PRISMTEK_CONTINUITY_URL"]),
        "continuity_token_configured": bool(payload["EnvironmentVariables"]["PRISMTEK_CONTINUITY_TOKEN"]),
        "launchctl_bootstrap": f"launchctl bootstrap gui/$(id -u) {plist_path}",
        "launchctl_kickstart": f"launchctl kickstart -k gui/$(id -u)/{args.label}",
        "launchctl_enable": f"launchctl enable gui/$(id -u)/{args.label}",
        "launchctl_legacy_load": f"launchctl load -w {plist_path}",
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
