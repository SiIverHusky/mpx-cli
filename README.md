# mpx

**One developer CLI for MPX skills** — build, test, and publish both robot skills (WASM, the `move` family) and merchant web skills (AWA, the `web` family).

## Install

```bash
pipx install mpx            # recommended, works on Windows/macOS/Linux
```

## Command surface

```bash
# Account & marketplace (shared)
mpx signup <username>
mpx login <username>
mpx logout
mpx publish [dir]           # auto-detects skill family from manifest.json
mpx search [query]
mpx info <skill_id>
mpx versions <skill_id>

# Robot skills (WASM)
mpx move init <name> --lang c|wat|ts
mpx move build <src> [--validate] [--inspect]
mpx move upload <x.wasm>
mpx move run <skill>
mpx move list
mpx move delete <skill>

# Web skills (AWA)
mpx web init <domain>
mpx web up                  # start worker + GCS (auto-pull Docker Hub images)
mpx web seed <domain>
mpx web session start <skill_id> --robot <uuid>
mpx web session list | get | action | end
mpx web list
mpx web readme <skill_id>
mpx web delete <domain>
mpx web down
```

## Prerequisites

- Python ≥ 3.10 (no external packages — stdlib only)
- Docker (toolchain image for `mpx move build`; AWA worker + GCS for `mpx web`)

## Design

See `docs/001-consolidated-cli-design.md`.
