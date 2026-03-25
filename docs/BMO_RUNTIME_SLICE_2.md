# BMO Runtime Slice 2

## What this adds

This additive slice extends the runtime introduced in PR #53 with:

- Nemotron-first profile helper
- local vs cloud task router
- STT adapter with optional wake-word gate
- richer terminal face helper
- runtime launch flow
- runtime slice 2 env example

## Recommended model split

For the current Intel Mac with 8GB RAM:

- local default: `nemotron-mini:4b-instruct-q2_K`
- local quality bump: `nemotron-mini:4b-instruct-q4_K_M`
- cloud target: `nemotron-3-super`

## Commands

Apply a slice-2 profile:

```bash
python3 scripts/apply-bmo-runtime-profile-v2.py dev
python3 scripts/apply-bmo-runtime-profile-v2.py snappy
python3 scripts/apply-bmo-runtime-profile-v2.py robust
```

Route a task:

```bash
python3 scripts/bmo-model-router.py --task "review the prismtek-site migration route map"
```

Capture one STT turn:

```bash
python3 scripts/bmo-stt-listen.py --once "hello bmo"
```

Dry-run the launch flow:

```bash
python3 scripts/bmo-runtime-launch.py --dry-run --once "hello bmo"
```

Render the richer face:

```bash
python3 scripts/bmo-face-rich.py idle
```

## Notes

The cloud route is only considered available when `BMO_CLOUD_TEXT_ENDPOINT` is set.

The launch flow currently expects the selected route endpoint to be `Ollama /api/generate` compatible.

This slice is additive. It does not replace the existing runtime entrypoints on master.
