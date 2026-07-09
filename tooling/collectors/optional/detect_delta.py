#!/usr/bin/env python3
"""
Detect deltas between the latest snapshot and the prior snapshot per source.

For each source directory under framework-refs/snapshots/ that holds two or
more versioned snapshots, this compares the two newest artifacts and reports a
first-pass classification based on a text-diff heuristic:

  - structural : > 20% of the visible text changed
  - material   : > 5%
  - minor      : > 0.1%
  - editorial  : otherwise (or hashes identical)

This tool is read-only. It never writes DLT-YYYY-NNN records: raising a delta
into framework-refs/currency/deltas/ and classifying it authoritatively is a
human step performed via SOP-102 (impact assessment is confirmation-gated).
The classification here is advisory input to that step.

Copyright 2026 isms contributors
SPDX-License-Identifier: Apache-2.0
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from pathlib import Path

from ruamel.yaml import YAML

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
SNAPSHOTS = REPO_ROOT / "framework-refs" / "snapshots"
yaml = YAML(typ="safe")

_TAG = re.compile(r"<[^>]+>")
_WS = re.compile(r"\s+")


def visible_text(markup: str) -> str:
    """Crude, offline HTML-to-text: strip tags and collapse whitespace."""
    text = _TAG.sub(" ", markup)
    return _WS.sub(" ", text).strip()


def change_fraction(old: str, new: str) -> float:
    """Fraction of text that changed between old and new (0.0 .. 1.0)."""
    if not old and not new:
        return 0.0
    ratio = difflib.SequenceMatcher(a=old, b=new, autojunk=False).ratio()
    return round(1.0 - ratio, 6)


def classify_delta(fraction: float) -> str:
    if fraction > 0.20:
        return "structural"
    if fraction > 0.05:
        return "material"
    if fraction > 0.001:
        return "minor"
    return "editorial"


def _load_meta(meta_path: Path) -> dict:
    with meta_path.open("r") as f:
        return yaml.load(f) or {}


def _artifact_for(meta_path: Path, meta: dict) -> Path | None:
    """Resolve the artifact file a meta describes, else the sibling by stem."""
    files = (meta or {}).get("artifact_files") or {}
    for kind in ("html", "text", "pdf"):
        rel = (files.get(kind) or {}).get("path")
        if rel:
            candidate = REPO_ROOT / rel
            if candidate.is_file():
                return candidate
    stem = meta_path.name[: -len(".meta.yaml")]
    for ext in (".html", ".txt", ".xml"):
        candidate = meta_path.with_name(stem + ext)
        if candidate.is_file():
            return candidate
    return None


def latest_two(source_dir: Path) -> list[tuple[Path, dict]]:
    """The two newest (meta_path, meta) pairs in a source dir, newest first."""
    metas = sorted(source_dir.glob("*.meta.yaml"))
    pairs = [(m, _load_meta(m)) for m in metas]
    # Order by fetched_at when present, else by filename; newest last -> reverse.
    pairs.sort(key=lambda mp: str(mp[1].get("fetched_at") or mp[0].name))
    return list(reversed(pairs))[:2]


def compare_source(source_dir: Path) -> dict | None:
    pairs = latest_two(source_dir)
    if len(pairs) < 2:
        return None
    (new_meta_path, new_meta), (old_meta_path, old_meta) = pairs
    new_art = _artifact_for(new_meta_path, new_meta)
    old_art = _artifact_for(old_meta_path, old_meta)
    if new_art is None or old_art is None:
        return None
    new_hash = (new_meta.get("artifact_files", {}).get("html", {}) or {}).get("sha256")
    old_hash = (old_meta.get("artifact_files", {}).get("html", {}) or {}).get("sha256")
    if new_hash and old_hash and new_hash == old_hash:
        fraction, classification = 0.0, "editorial"
    else:
        fraction = change_fraction(
            visible_text(old_art.read_text(encoding="utf-8", errors="replace")),
            visible_text(new_art.read_text(encoding="utf-8", errors="replace")),
        )
        classification = classify_delta(fraction)
    return {
        "source_id": new_meta.get("source_id", source_dir.name),
        "prior": str(old_art.relative_to(REPO_ROOT)),
        "latest": str(new_art.relative_to(REPO_ROOT)),
        "change_fraction": fraction,
        "classification": classification,
        "requires_impact_assessment": classification in ("material", "structural"),
    }


def find_source_dirs() -> list[Path]:
    return sorted(p.parent for p in SNAPSHOTS.rglob("*.meta.yaml")) if SNAPSHOTS.is_dir() else []


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args()

    if not SNAPSHOTS.is_dir():
        print("NOTE: no snapshots yet; nothing to compare.")
        return 0

    results = []
    for source_dir in dict.fromkeys(find_source_dirs()):
        delta = compare_source(source_dir)
        if delta is not None:
            results.append(delta)

    if args.json:
        print(json.dumps(results, indent=2))
        return 0

    if not results:
        print("No source has two or more versioned snapshots; no deltas to compare.")
        return 0

    print(f"Snapshot deltas ({len(results)} source(s) with prior versions):")
    for d in results:
        flag = "  ** raise impact assessment (SOP-102) **" if d["requires_impact_assessment"] else ""
        print(
            f"  {d['source_id']}: {d['classification']} "
            f"({d['change_fraction']:.1%} changed){flag}"
        )
        print(f"    {d['prior']} -> {d['latest']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
