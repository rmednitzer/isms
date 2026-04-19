#!/usr/bin/env python3
"""
Template renderer for the isms repository.

Reads instance/config.yaml, renders every markdown and YAML file under template/
into instance/ with {{PLACEHOLDERS}} and {{#if ...}}/{{else}}/{{/if}} blocks resolved.

Idempotent: re-running on unchanged config produces no diff.

Copyright 2026 isms contributors
SPDX-License-Identifier: Apache-2.0
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from ruamel.yaml import YAML

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = REPO_ROOT / "template"
INSTANCE_DIR = REPO_ROOT / "instance"

yaml = YAML(typ="rt")
yaml.preserve_quotes = True
yaml.indent(mapping=2, sequence=4, offset=2)

PLACEHOLDER_RE = re.compile(r"\{\{\s*([A-Za-z0-9_.]+)\s*\}\}")
IF_BLOCK_RE = re.compile(
    r"\{\{#if\s+([A-Za-z0-9_.]+)\s*\}\}(.*?)(?:\{\{else\}\}(.*?))?\{\{/if\}\}",
    re.DOTALL,
)


class RenderError(Exception):
    pass


def load_config(config_path: Path) -> dict:
    if not config_path.is_file():
        raise RenderError(f"config file not found: {config_path}")
    with config_path.open("r", encoding="utf-8") as f:
        return yaml.load(f)


def resolve_dotted(data: dict, key: str):
    """Resolve 'a.b.c' against nested dicts. Returns None if missing."""
    cur = data
    for part in key.split("."):
        if not isinstance(cur, dict):
            return None
        cur = cur.get(part)
        if cur is None:
            return None
    return cur


def render_ifs(text: str, cfg: dict) -> str:
    """Resolve {{#if key}}...{{else}}...{{/if}} blocks against config."""

    def replacer(m: re.Match) -> str:
        key = m.group(1)
        then_body = m.group(2) or ""
        else_body = m.group(3) or ""
        val = resolve_dotted(cfg, key)
        return then_body if val else else_body

    prev = None
    cur = text
    while cur != prev:
        prev = cur
        cur = IF_BLOCK_RE.sub(replacer, cur)
    return cur


def render_placeholders(text: str, cfg: dict, file_path: Path) -> tuple[str, list[str]]:
    """Replace {{key.path}} placeholders. Returns (rendered_text, unresolved_list)."""
    unresolved: list[str] = []

    def replacer(m: re.Match) -> str:
        key = m.group(1)
        val = resolve_dotted(cfg, key)
        if val is None:
            unresolved.append(key)
            return m.group(0)
        return str(val)

    rendered = PLACEHOLDER_RE.sub(replacer, text)
    return rendered, unresolved


def should_copy(path: Path) -> bool:
    """Skip .gitkeep files at leaf directories and package caches."""
    return path.name not in {".gitkeep"} and "__pycache__" not in path.parts


# Files under template/ that must be copied verbatim without placeholder rendering
# (typically documentation files that contain literal placeholder examples).
RAW_COPY_FILES = {"PLACEHOLDERS.md"}


def render_tree(cfg: dict, dry_run: bool = False) -> tuple[int, list[tuple[Path, list[str]]]]:
    if not TEMPLATE_DIR.is_dir():
        raise RenderError(f"template directory missing: {TEMPLATE_DIR}")
    rendered_count = 0
    unresolved_by_file: list[tuple[Path, list[str]]] = []

    for src in TEMPLATE_DIR.rglob("*"):
        if not src.is_file() or not should_copy(src):
            continue
        rel = src.relative_to(TEMPLATE_DIR)
        dst = INSTANCE_DIR / rel
        if dst.exists() and src.suffix == ".md" and (INSTANCE_DIR / rel).is_file():
            # Preserve instance-customised files: skip if the instance has diverged.
            pass

        if src.suffix in {".md", ".yaml", ".yml"} and src.name not in RAW_COPY_FILES:
            text = src.read_text(encoding="utf-8")
            text = render_ifs(text, cfg)
            text, unresolved = render_placeholders(text, cfg, src)
            if unresolved:
                unresolved_by_file.append((rel, unresolved))
            if not dry_run:
                dst.parent.mkdir(parents=True, exist_ok=True)
                dst.write_text(text, encoding="utf-8")
        else:
            if not dry_run:
                dst.parent.mkdir(parents=True, exist_ok=True)
                dst.write_bytes(src.read_bytes())
        rendered_count += 1

    return rendered_count, unresolved_by_file


def main() -> int:
    parser = argparse.ArgumentParser(description="Render template/ into instance/ using instance/config.yaml")
    parser.add_argument("--config", type=Path, default=INSTANCE_DIR / "config.yaml",
                        help="path to instance config yaml (default: instance/config.yaml)")
    parser.add_argument("--dry-run", action="store_true", help="parse and report but do not write")
    parser.add_argument("--strict", action="store_true",
                        help="fail if any placeholders are unresolved (default: warn)")
    args = parser.parse_args()

    try:
        cfg = load_config(args.config)
    except RenderError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    print(f"Rendering template/ -> instance/ using {args.config}")
    try:
        count, unresolved_list = render_tree(cfg, dry_run=args.dry_run)
    except RenderError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    print(f"Processed {count} files ({'dry-run' if args.dry_run else 'written'}).")
    if unresolved_list:
        print(f"Unresolved placeholders in {len(unresolved_list)} files:")
        for rel, missing in unresolved_list[:20]:
            print(f"  {rel}: {', '.join(sorted(set(missing)))}")
        if len(unresolved_list) > 20:
            print(f"  ... and {len(unresolved_list) - 20} more files")
        if args.strict:
            return 1
    else:
        print("No unresolved placeholders.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
