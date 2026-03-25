#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import plistlib
from pathlib import Path

DEFAULT_LABEL = "cloud.codysumpter.bmo-workspace-sync"
DEFAULT_PLIST = Path.home() / "Library" / "LaunchAgents" / f"{DEFAULT_LABEL}.plist"
DEFAULT_SYNC_SCRIPT = Path.home() / "bmo-stack" / "scripts" / "bmo-workspace-sync.py"


def build_plist(label: str, python_bin: str, sync_script: str, interval: int) -> dict[str, object]:
    return {
        "Label": label,
        "ProgramArguments": [python_bin, sync_script],
        "RunAtLoad": True,
        "StartInterval": interval,
        "StandardOutPath": str(Path.home() / "Library" / "Logs" / "bmo-workspace-sync.log"),
        "StandardErrorPath": str(Path.home() / "Library" / "Logs" / "bmo-workspace-sync.err.log"),
        "EnvironmentVariables": {
            "BMO_STACK_REPO_URL": "https://github.com/codysumpter-cloud/bmo-stack.git",
            "BMO_OPENCLAW_WORKSPACE_DIR": str(Path.home() / ".openclaw" / "workspace" / "bmo-stack"),
            "BMO_HOST_CONTEXT_DIR": str(Path.home() / "bmo-context"),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Write a LaunchAgent plist for automatic BMO workspace sync.")
    parser.add_argument("--label", default=DEFAULT_LABEL)
    parser.add_argument("--plist", default=str(DEFAULT_PLIST))
    parser.add_argument("--python-bin", default=os.environ.get("PYTHON_BIN", "/usr/bin/python3"))
    parser.add_argument("--sync-script", default=str(DEFAULT_SYNC_SCRIPT))
    parser.add_argument("--interval-sec", type=int, default=300)
    parser.add_argument("--output", default="workflows/bmo-launchd-install.json")
    args = parser.parse_args()

    plist_path = Path(args.plist).expanduser()
    plist_path.parent.mkdir(parents=True, exist_ok=True)
    payload = build_plist(args.label, args.python_bin, args.sync_script, args.interval_sec)
    with plist_path.open("wb") as fh:
        plistlib.dump(payload, fh)

    result = {
        "label": args.label,
        "plist": str(plist_path),
        "sync_script": args.sync_script,
        "interval_sec": args.interval_sec,
        "launchctl_load": f"launchctl load -w {plist_path}",
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
