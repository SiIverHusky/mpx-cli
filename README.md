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
mpx update-manifest [dir]   # edit manifest.json metadata (also: mpx move|web update-manifest)

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

## Scaffolding

`mpx move init` and `mpx web init` share one contract — same flags, prompts,
file writer, slug-collision check, exit codes and console summary:

```bash
mpx move init <name> --lang c|wat|ts      # WASM project (README.md, Makefile, src/, include/)
mpx web init <domain> | <slug>@<domain>   # AWA project (manifest.json, skill.js, GUIDE.md, README.md)

# shared flags
--dir/-d DIR      output directory (default: ./<target>)
--slug/-s SLUG    marketplace slug (default: derived from name/domain)
--title/-t TITLE  marketplace title
--version V       initial version (default: 1.0.0, must be X.Y.Z)
--yes/-y          accept defaults, never prompt
```

Without `--yes` (and on a TTY) both prompts for slug → title → version, and both
warn when the slug is already taken on the gateway. An existing target directory
fails with exit code `1`.

## Project metadata

Every scaffolded project has a `manifest.json` that `mpx publish` reads — `slug`,
`title`, `version`, `readme`, `skill_type`, `source_language` (plus `domain`,
`actions`, `capabilities`, `urls`, `timeout`, `memoryLimitMB` for web skills).

Generated `README.md` (move) and `GUIDE.md` (web) each embed an
**"Updating this README and the manifest metadata"** section: the field table,
a checklist of what to update when behavior changes, and how to re-publish.

Edit metadata from the CLI instead of by hand:

```bash
mpx move update-manifest .        # or: mpx web update-manifest . / mpx update-manifest .
```

It prompts per field with the current value as the default; pass
`--slug/--title/--version/--readme/--domain` for scripted updates, `--dry-run`
to preview. Keep the README/GUIDE prose in sync manually — no generator rewrites it.

## Prerequisites

- Python ≥ 3.10 (no external packages — stdlib only)
- Docker (toolchain image for `mpx move build`; AWA worker + GCS for `mpx web`)

## Design

See `docs/001-consolidated-cli-design.md`.
