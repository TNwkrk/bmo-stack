.PHONY: up down status logs doctor sync-context sync-context-host-to-repo sync-context-repo-to-host

# Docker Compose file
COMPOSE_FILE=compose.yaml

up:
	docker compose -f $(COMPOSE_FILE) up -d

down:
	docker compose -f $(COMPOSE_FILE) down

status:
	docker compose -f $(COMPOSE_FILE) ps

logs:
	docker compose -f $(COMPOSE_FILE) logs -f

sync-context:
	./scripts/sync-context.sh

sync-context-host-to-repo:
	./scripts/sync-context.sh --host-to-repo

sync-context-repo-to-host:
	./scripts/sync-context.sh --repo-to-host

doctor:
	@echo "Checking Docker and Docker Compose..."
	@which docker >/dev/null 2>&1 || { echo "Error: docker not found"; exit 1; }
	@which docker compose >/dev/null 2>&1 || { echo "Error: docker compose not found"; exit 1; }
	@echo "Docker and Docker Compose are available."
	@echo "Checking OpenClaw binary..."
	@which openclaw >/dev/null 2>&1 || { echo "Error: openclaw binary not found"; exit 1; }
	@echo "OpenClaw binary found."
	@echo "Checking OpenShell binary..."
	@which openshell >/dev/null 2>&1 || { echo "Error: openshell binary not found"; exit 1; }
	@echo "OpenShell binary found."
	@echo "Checking OpenClaw gateway config on host..."
	@if [ -f $$HOME/.openclaw/openclaw.json ]; then \
		echo "OpenClaw config found."; \
	else \
		echo "Warning: OpenClaw config not found at $$HOME/.openclaw/openclaw.json"; \
	fi
	@echo "Checking ~/bmo-context exists..."
	@if [ -d $$HOME/bmo-context ]; then \
		echo "~/bmo-context exists."; \
	else \
		echo "Error: ~/bmo-context does not exist"; \
		exit 1; \
	fi
	@echo "Checking context files in repo..."
	@if [ -d ./context ] && [ -f ./context/BOOTSTRAP.md ]; then \
		echo "Context files present."; \
	else \
		echo "Error: Context files missing in repo."; \
		exit 1; \
	fi
	@echo "All checks passed."