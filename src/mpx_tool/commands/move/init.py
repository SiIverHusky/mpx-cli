"""mpx move init — scaffold a robot (WASM) skill project."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import importlib.resources

_RES = importlib.resources.files("mpx_tool.commands.resource.move")


def _read_resource(name: str) -> str:
    ref = _RES / name
    with importlib.resources.as_file(ref) as path:
        return Path(path).read_text()


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.lstrip("\n"))
    try:
        rel = path.relative_to(Path.cwd())
    except ValueError:
        rel = path.resolve()
    print(f"  📝 Created {rel}")


def add_move_init_parser(sub: argparse._SubParsersAction) -> None:
    p = sub.add_parser("init", help="Scaffold a robot skill development project")
    p.add_argument("name", help="Skill name (e.g. my_skill)")
    p.add_argument(
        "--lang", "-l",
        choices=["c", "wat", "ts"],
        default="c",
        help="Language: c (default), wat, or ts (AssemblyScript)",
    )
    p.add_argument("--dir", "-d", default=None, help="Output directory (default: ./<name>)")


def cmd_move_init(args: argparse.Namespace) -> None:
    name = args.name
    lang = args.lang
    out_dir = Path(args.dir) if args.dir else Path(name)

    if out_dir.exists():
        print(f"❌ Directory '{out_dir}' already exists")
        return

    ext_map = {"c": "c", "wat": "wat", "ts": "ts"}
    ext = ext_map[lang]

    print(f"🚀 Initializing robot skill project '{name}' in {out_dir}/")
    print()

    src_dir = out_dir / "src"
    src_dir.mkdir(parents=True, exist_ok=True)

    templates = {
        "c": _read_resource("skill.c.template"),
        "wat": _read_resource("skill.wat.template"),
        "ts": _read_resource("skill.ts.template"),
    }
    _write(src_dir / f"{name}.{ext}", templates[lang].format(name=name))

    include_dir = out_dir / "include"
    include_dir.mkdir(parents=True, exist_ok=True)
    if lang == "c":
        _write(include_dir / "mpx_host.h", _read_resource("mpx_host.h"))
    elif lang == "ts":
        _write(include_dir / "mpx_env.ts", _read_resource("mpx_env.ts"))
    elif lang == "wat":
        _write(include_dir / "host_functions.md", _read_resource("host_functions_wat.md"))

    readme_templates = {
        "c": "README_c.md.template",
        "wat": "README_wat.md.template",
        "ts": "README_ts.md.template",
    }
    _write(out_dir / "README.md", _read_resource(readme_templates[lang]).format(name=name))

    makefile = (
        f"# {name} — MPX-Dog WASM Skill\n"
        f"# Convenience wrapper around mpx.\n\n"
        f"MPX_HOST ?= 192.168.2.1\n"
        f"SRC := src/{name}.{ext}\n"
        f"WASM := build/{name}.wasm\n\n"
        f".PHONY: build upload run clean\n\n"
        f"build:\n"
        f"\tmpx move build $(SRC)\n\n"
        f"upload:\n"
        f"\tmpx move upload $(WASM) --ip $(MPX_HOST)\n\n"
        f"run:\n"
        f"\tmpx move run {name}.wasm --ip $(MPX_HOST)\n\n"
        f"clean:\n"
        f"\trm -f build/*.wasm\n"
    )
    _write(out_dir / "Makefile", makefile)

    manifest = {
        "slug": name,
        "title": f"{name} — MPX-Dog skill",
        "skill_type": "WASM",
        "version": "1.0.0",
        "readme": f"A WASM skill for the MPX-Dog quadruped robot.",
    }
    _write(out_dir / "manifest.json", json.dumps(manifest, indent=2) + "\n")

    build_dir = out_dir / "build"
    build_dir.mkdir(parents=True, exist_ok=True)

    print()
    print(f"✅ Project '{name}' initialized! See {out_dir / 'README.md'} to get started.")
    print("   Next: mpx move build " + f"{out_dir / 'src' / (name + '.' + ext)}")
