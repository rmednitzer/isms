"""
Shared helpers for the validator scripts.

Centralises front-matter extraction, repository root discovery, and the standard
list of scan roots so each validator does not redefine them.

Copyright 2026 isms contributors
SPDX-License-Identifier: Apache-2.0
"""
from __future__ import annotations

import datetime as _dt
import re
from collections.abc import Iterable, Iterator
from pathlib import Path

from ruamel.yaml import YAML

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

# YAML loader shared across validators. Safe loader by design.
_yaml = YAML(typ="safe")

# Default markdown scan roots for governance artefacts.
GOVERNANCE_SCAN_ROOTS: tuple[Path, ...] = (
    REPO_ROOT / "docs",
    REPO_ROOT / "template" / "governance",
    REPO_ROOT / "template" / "operations",
    REPO_ROOT / "instance" / "governance",
    REPO_ROOT / "instance" / "operations",
)

# Path fragments that always indicate a transient/build artefact, never a
# governance file.  Matched as substrings of the absolute path.
_EXCLUDE_FRAGMENTS = ("/.venv/", "/__pycache__/", "/dist-audit-pack/")


def normalise_dates(value):
    """Recursively serialise date and datetime values to ISO strings.

    JSON Schema's format=date / date-time validators expect strings, but
    ruamel.yaml's safe loader returns datetime.date / datetime.datetime objects
    for dates without quotes.
    """
    if isinstance(value, _dt.datetime):
        return value.isoformat()
    if isinstance(value, _dt.date):
        return value.isoformat()
    if isinstance(value, dict):
        return {k: normalise_dates(v) for k, v in value.items()}
    if isinstance(value, list):
        return [normalise_dates(v) for v in value]
    return value


def parse_frontmatter(path: Path, *, normalise: bool = False) -> dict | None:
    """Return the parsed YAML front-matter for a markdown file, or None.

    When normalise=True, datetime values are converted to ISO strings so the
    result is suitable for JSON Schema validation with format checkers.
    """
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    data = _yaml.load(m.group(1))
    if data is None:
        return None
    if not isinstance(data, dict):
        return None
    return normalise_dates(data) if normalise else data


def iter_markdown(roots: Iterable[Path]) -> Iterator[Path]:
    """Yield every .md file under each root, skipping transient directories."""
    for root in roots:
        if not root.is_dir():
            continue
        for md in root.rglob("*.md"):
            s = str(md)
            if any(frag in s for frag in _EXCLUDE_FRAGMENTS):
                continue
            yield md


def iter_markdown_repo() -> Iterator[Path]:
    """Yield every .md file across the whole repository (excluding transient dirs)."""
    yield from iter_markdown([REPO_ROOT])


def iter_frontmatter(roots: Iterable[Path]) -> Iterator[tuple[Path, dict]]:
    """Yield (path, front-matter dict) for each markdown file with valid YAML."""
    for md in iter_markdown(roots):
        fm = parse_frontmatter(md)
        if fm is not None:
            yield md, fm
