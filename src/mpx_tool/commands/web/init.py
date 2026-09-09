"""mpx web init — scaffold an AWA (web automation) skill.

Usage:
  mpx web init <domain>
  mpx web init <slug>@<domain>       # multiple skills for same domain

Creates manifest.json, skill.js, and GUIDE.md in ./<domain>/.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import importlib.resources

from mpx_tool.sdk.auth import get_username_from_token, read_token
from mpx_tool.sdk.gateway import GatewayClient, GatewayError

_RES = importlib.resources.files("mpx_tool.commands.resource.web")


def _read_resource(name: str) -> str:
    ref = _RES / name
    with importlib.resources.as_file(ref) as path:
        # Vendored templates are UTF-8; read explicitly so Windows' default
        # cp1252 codec doesn't raise UnicodeDecodeError on non-ASCII content.
        return Path(path).read_text(encoding="utf-8")


def _prompt(question: str, default: str = "") -> str:
    if not sys.stdin.isatty():
        return default
    hint = f" ({default})" if default else ""
    return input(f"  {question}{hint}: ").strip() or default


def add_web_init_parser(sub: argparse._SubParsersAction) -> None:
    p = sub.add_parser("init", help="Scaffold an AWA (web automation) skill")
    p.add_argument("target", help="Domain (bestbuy.com) or slug@domain")
    p.add_argument("--dir", "-d", default=None, help="Output directory (default: ./<domain>)")


def cmd_web_init(args: argparse.Namespace) -> None:
    raw = args.target

    # Parse slug@domain format
    if "@" in raw and not raw.startswith("@") and not raw.endswith("@"):
        slug, domain = raw.split("@", 1)
    else:
        domain, slug = raw, None

    target_dir = Path(args.dir) if args.dir else Path(raw)
    target_dir = target_dir.resolve()

    if target_dir.exists():
        print(f'❌ Directory "{raw}" already exists.')
        sys.exit(1)

    default_slug = re.sub(r"[^a-zA-Z0-9_-]", "", domain.replace(".", "-"))

    print(f"\n  📋 Scaffolding AWA skill for \"{raw}\"\n")

    if not slug:
        slug = _prompt("Slug (short project identifier)", default_slug)
    title = _prompt("Title", f"{domain} merchant skill")

    # ── Slug collision check against the gateway ──────────────────
    token = read_token()
    if token:
        username = get_username_from_token(token)
        if username:
            try:
                client = GatewayClient(gateway_url=getattr(args, "gateway_url", None))
                resp = client.check_slug(slug, token)
                if resp and resp.get("exists"):
                    print(f'\n  ⚠️  Warning: Slug "{slug}" is already taken by one of your skills.')
                    print("    If you publish, this will conflict with the existing skill.")
                    print(f'    Pick a different slug, or use slug@domain format: "{slug}-variant@{domain}"\n')
            except GatewayError:
                pass  # Gateway unreachable — publish will catch it.

    version = "1.0.0"

    # ── Create directory + files ──────────────────────────────────
    target_dir.mkdir(parents=True, exist_ok=False)

    manifest_content = _read_resource("manifest.json")
    manifest_content = manifest_content.replace("{{DOMAIN}}", domain)
    manifest_content = manifest_content.replace("{{SLUG}}", slug)
    manifest_content = manifest_content.replace("{{VERSION}}", version)
    (target_dir / "manifest.json").write_text(manifest_content, encoding="utf-8")

    skill_content = _read_resource("skill.js").replace("{{DOMAIN}}", domain)
    (target_dir / "skill.js").write_text(skill_content, encoding="utf-8")

    (target_dir / "GUIDE.md").write_text(_read_resource("GUIDE.md"), encoding="utf-8")

    print(f"\n  ✓ Created directory: {raw}/")
    print(f"  ✓ Created: {raw}/manifest.json")
    print(f"  ✓ Created: {raw}/skill.js")
    print(f"  ✓ Created: {raw}/GUIDE.md")
    print()
    print(f'  ✅ AWA skill scaffolded for "{raw}"')
    print()
    print("  Configuration:")
    print(f"    Slug:    {slug}")
    print(f"    Title:   {title}")
    print("    Version: 1.0.0")
    print()
    print("  Next steps:")
    print(f"    cd {raw}")
    print("    # Edit skill.js — implement the handlers for your site")
    print("    # Read GUIDE.md for $awa.* API reference")
    print("    # Test locally:  mpx web up && mpx web seed " + raw)
    print("    # Publish:       mpx login <user> && mpx publish " + raw)
    print()
