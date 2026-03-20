# SYSTEMMAP

Main parts of the ecosystem:
- Prismbot-BMO
- Prismtek.dev
- omni-bmo
- nemoclaw
- council (Prismo, BMO, NEPTR, etc.)

Confirmed facts:
- omni-bmo is the local-first / edge-agent project.
- Prismtek.dev is the public-facing site.
- nemoclaw provides sandboxed execution in OpenShell.
- Host OpenClaw handles Telegram.
- bmo-tron is the worker sandbox.
- Council agents: Prismo (chief orchestrator), BMO (front-facing), NEPTR (verification), Finn (implementation), etc.

Assumptions:
- Prismbot-BMO is the broader system / coordination repo.
- Some patterns in this setup were adapted from the PrismBot repos.

Current operating model:
- Host: conversation handling (Telegram via OpenClaw), Prismo orchestration, BMO front-facing.
- ~/bmo-context = persistent truth source (canonical context).
- bmo-tron sandbox = worker / execution surface for specialist agents (Finn, etc.) under Prismo's direction.
- NEPTR performs verification in the sandbox before BMO claims completion.