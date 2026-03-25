# BMO Site Caretaker

## Purpose

Inventory the legacy `prismtek-site` donor and the `prismtek-site-replica` React/Vite candidate, then emit a controlled migration plan artifact.

## Commands

Basic run:

```bash
python3 scripts/bmo-site-caretaker.py
```

Explicit paths:

```bash
python3 scripts/bmo-site-caretaker.py \
  --site-dir ~/prismtek-site \
  --replica-dir ~/prismtek-site-replica
```

If the default paths do not exist, the helper searches under the discovery root and reports candidate paths:

```bash
python3 scripts/bmo-site-caretaker.py --discovery-root ~
```

You can also set:

- `BMO_SITE_DIR`
- `BMO_SITE_REPLICA_DIR`
- `BMO_SITE_DISCOVERY_ROOT`

## Output

Writes `workflows/bmo-site-caretaker.json` containing:

- site inventory
- replica inventory
- discovery candidates when paths are missing
- route-level migration plan
