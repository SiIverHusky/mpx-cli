# mpx

**One developer CLI for MPX skills** — scaffold, build, test and publish robot skills
(WASM, the `move` family) and merchant web skills (AWA, the `web` family).

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
mpx publish [dir]           # reads manifest.json to pick the skill family
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

Both `init` commands follow one contract: same flags, same prompt order, same
slug-collision check, same exit codes, same console summary.

```bash
mpx move init <name> --lang c|wat|ts      # -> Makefile, src/, include/, GUIDE.md
mpx web init <domain> | <slug>@<domain>   # -> manifest.json, skill.js, GUIDE.md
```

Flags shared by both:

```bash
--dir/-d DIR      output directory (default: ./<target>)
--slug/-s SLUG    marketplace slug (default: derived from name/domain)
--title/-t TITLE  marketplace title
--version V       initial version (default: 1.0.0, must be X.Y.Z)
--yes/-y          accept defaults, never prompt
```

On a TTY without `--yes`, both prompt for slug → title → version and warn when the
slug is already taken on the gateway. An existing target directory fails with
exit code `1`.

## Project metadata

Each scaffolded project has a `manifest.json` that `mpx publish` reads:

- **Both families** — `slug`, `title`, `version`, `readme`, `skill_type`,
  `source_language`
- **Web only** — `domain`, `actions`, `capabilities`, `urls`, `timeout`,
  `memoryLimitMB`

The generated `GUIDE.md` documents its family's fields and ends with an
**"Updating this GUIDE and the manifest metadata"** section: the field table, a
checklist for behavior changes, and how to re-publish.

Edit metadata through the CLI rather than by hand:

```bash
mpx update-manifest .        # or: mpx move update-manifest . / mpx web update-manifest .
```

It prompts per field with the current value as the default. For scripted updates
pass `--slug/--title/--version/--readme/--domain`, and `--dry-run` to preview.
Keep the GUIDE prose in sync manually — no generator rewrites it.

## Prerequisites

- Python ≥ 3.10 (stdlib only, no external packages)
- Docker (toolchain image for `mpx move build`; AWA worker + GCS for `mpx web`)

## Design

See `docs/001-consolidated-cli-design.md`.
