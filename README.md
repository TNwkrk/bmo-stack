# BMO Stack

A portable setup for BMO / OpenClaw / worker environment.

## Architecture

- **Host OpenClaw**: Handles Telegram replies (runs on the host machine).
- **Sandbox Worker**: Optional and disposable, managed via OpenShell/NemoClaw.
- **Canonical Context**: Lives outside disposable sandboxes in `~/bmo-context` (mounted as `./context` in the repo).

## Directory Structure

```
bmo-stack/
├── compose.yaml          # Docker Compose file (for OPTIONAL auxiliary services)
├── .env.example          # Example environment variables
├── Makefile              # Simple commands: make up, down, status, logs, doctor, sync-context*
├── README.md             # This file
├── scripts/
│   ├── bootstrap-mac.sh  # macOS bootstrap
│   ├── bootstrap-wsl.sh  # WSL2 bootstrap
│   ├── bootstrap-linux.sh # Linux VPS / private cloud host bootstrap
│   ├── common.sh         # Shared functions for bootstrap scripts
│   └── sync-context.sh   # Sync context between host and repo
├── config/
│   └── omni-core.env.example # Example config for local-first operation
├── context/
│   ├── BOOTSTRAP.md
│   ├── SESSION_STATE.md
│   ├── SYSTEMMAP.md
│   ├── RUNBOOK.md
│   └── BACKLOG.md
├── deploy/
│   ├── bmo-openclaw.service        # systemd service for OpenClaw gateway
│   ├── bmo-storage-prune.service   # systemd service for storage pruning
│   └── bmo-storage-prune.timer     # systemd timer for hourly pruning
└── memory/
    └── decisions/
        └── README.md
```

## What Runs Where

- **Host (bare metal or VM)**:
  - OpenClaw gateway (handles Telegram)
  - OpenShell / NemoClaw (for managing sandboxes)
  - Your personal data and configuration (e.g., `~/.openclaw`)

- **Worker Sandbox (optional, disposable)**:
  - Created via `openshell sandbox create --name bmo-tron`
  - Used for isolated commands, repo inspection, and risky work
  - Should not hold important context; context is synced from `~/bmo-context`

## Getting Started

### Prerequisites

- Docker Engine and Docker Compose v2 (via Docker Desktop or standalone)
- OpenClaw installed on the host machine ([docs.openclaw.ai](https://docs.openclaw.ai))
- Access to NVIDIA API key (for the AI model)

### Bootstrap

Choose the script for your platform:

- **macOS**: `./scripts/bootstrap-mac.sh`
- **WSL2**: `./scripts/bootstrap-wsl.sh`
- **Linux VPS / private cloud host**: `./scripts/bootstrap-linux.sh`

The script will:
1. Check for Docker and OpenClaw.
2. Copy `.env.example` to `.env` if needed.
3. Provide next steps.

### Using the Stack

After bootstrapping:

1. Edit `.env` to add your NVIDIA API key (and any other required keys).
2. Ensure OpenClaw is running on your host machine.
3. Use `make up` to start any auxiliary services (currently just a placeholder container).
4. Manage the worker sandbox via OpenShell on the host:
   ```bash
   # Create a worker sandbox (if not already created)
   openshell sandbox create --name bmo-tron

   # Upload your OpenClaw config to the sandbox (so it can communicate with the gateway)
   openshell sandbox upload bmo-tron ~/.openclaw/openclaw.json .openclaw/openclaw.json

   # Now you can use the sandbox for isolated work
   openshell sandbox connect bmo-tron
   ```

### Context Synchronization

Keep your host `~/bmo-context` and the repo's `./context` in sync:

- `make sync-context`          # Bidirectional sync (default)
- `make sync-context-host-to-repo` # Host → Repo only
- `make sync-context-repo-to-host` # Repo → Host only

Or run the script directly: `./scripts/sync-context.sh [--host-to-repo|--repo-to-host]`

### Makefile Commands

- `make up` - Start auxiliary services (detached)
- `make down` - Stop and remove auxiliary services
- `make status` - Show status of auxiliary services
- `make logs` - Follow logs of auxiliary services
- `make sync-context` - Bidirectional context sync
- `make sync-context-host-to-repo` - Sync host context to repo
- `make sync-context-repo-to-host` - Sync repo context to host
- `make doctor` - Check system prerequisites and context

### Keeping Context Synced

The `context/` directory in this repo is a copy of your `~/bmo-context`.
- After making changes to the context files in `~/bmo-context`, you can sync them to the repo with `make sync-context-host-to-repo`.
- After making changes to the context files in the repo, you can sync them to the host with `make sync-context-repo-to-host`.
- You can automate this with a cron job or use the provided scripts.

## Important Notes

- Secrets (like API keys) should be placed in `.env` (not committed) or in your host's OpenClaw config.
- The `compose.yaml` currently runs a placeholder container for the worker environment. It does not run the Telegram bot (that runs on the host).
- The sandbox worker is managed by OpenShell on the host, not by Docker Compose. The compose file is for any auxiliary services you might want to add (e.g., a database).

## Top 5 Follow-up Improvements

1. Add a service for a database (e.g., Postgres) to `compose.yaml` for persistent worker data.
2. Create a script to automatically sync context between `~/bmo-context` and `./context` (already done: `scripts/sync-context.sh`).
3. Add a `make sync-context` command to facilitate context synchronization (already done).
4. Improve the bootstrap scripts to optionally install OpenClaw and Docker if missing.
5. Add health checks to the `compose.yaml` services and integrate with `make doctor`.
