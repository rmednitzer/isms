#!/usr/bin/env python3
"""
Fetch law snapshots from the Austrian RIS (Rechtsinformationssystem des Bundes)
OpenData API. Stub implementation with defensive structure; full RIS API binding
depends on which laws are in scope per framework-refs/sources/registry.yaml.

Documentation: https://www.data.gv.at (search "RIS") and https://www.ris.bka.gv.at

Copyright 2026 isms contributors
SPDX-License-Identifier: Apache-2.0
"""
from __future__ import annotations

import argparse
import hashlib
import sys
from datetime import UTC, datetime
from pathlib import Path

import requests
from ruamel.yaml import YAML

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
REGISTRY = REPO_ROOT / "framework-refs" / "sources" / "registry.yaml"
yaml = YAML(typ="rt")


def _safe_version(source: dict, fetched_tag: str) -> str:
    raw = source.get("current_version") or source.get("version") or fetched_tag
    cleaned = "".join(ch if ch.isalnum() or ch in {"-", "_", "."} else "-" for ch in str(raw))
    while "--" in cleaned:
        cleaned = cleaned.replace("--", "-")
    return cleaned.strip("-") or fetched_tag


def _latest_meta(path: Path, current_meta: Path) -> str | None:
    metas = sorted(path.glob("*.meta.yaml"))
    if not metas:
        return None
    for meta in reversed(metas):
        if meta != current_meta:
            return str(meta.relative_to(REPO_ROOT))
    return None


def _write_snapshot(source: dict) -> None:
    source_id = source.get("id", "unknown")
    url = source.get("authoritative_url")
    if not url:
        raise RuntimeError(f"{source_id}: missing authoritative_url")

    now = datetime.now(UTC)
    fetched_at = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    fetched_tag = now.strftime("%Y%m%dT%H%M%SZ")
    version = _safe_version(source, fetched_tag)

    target_dir = REPO_ROOT / str(source.get("local_reference", "")).strip("/")
    target_dir.mkdir(parents=True, exist_ok=True)
    html_file = target_dir / f"{version}.html"
    meta_file = target_dir / f"{version}.meta.yaml"

    response = requests.get(
        str(url),
        timeout=60,
        headers={"User-Agent": "isms-snapshot-fetcher/1.0", "Accept": "text/html,application/xhtml+xml"},
    )
    response.raise_for_status()
    body = response.text
    html_file.write_text(body, encoding="utf-8")
    digest = hashlib.sha256(body.encode("utf-8")).hexdigest()

    meta = {
        "source_id": source_id,
        "fetched_at": fetched_at,
        "fetch_method": source.get("fetch_method", "ris_api"),
        "source_url": str(url),
        "version_identifier": version,
        "artifact_files": {
            "html": {
                "path": str(html_file.relative_to(REPO_ROOT)),
                "sha256": digest,
            }
        },
    }
    supersedes = _latest_meta(target_dir, meta_file)
    if supersedes is not None:
        meta["supersedes"] = supersedes

    field_mapping = {"current_version_date": "version_date", "entry_into_force": "entry_into_force"}
    for source_field, meta_field in field_mapping.items():
        if source.get(source_field):
            meta[meta_field] = str(source[source_field])

    with meta_file.open("w", encoding="utf-8") as f:
        yaml.dump(meta, f)
    print(f"Fetched {source_id} -> {html_file.relative_to(REPO_ROOT)}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-id", help="fetch specific source only (default: all with fetch_method=ris_api)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not REGISTRY.is_file():
        print(f"NOTE: registry not found: {REGISTRY}")
        return 0
    with REGISTRY.open("r") as f:
        data = yaml.load(f)
    sources = data.get("sources", []) if isinstance(data, dict) else []
    ris_sources = [s for s in sources if s.get("fetch_method") == "ris_api"]
    if args.source_id:
        ris_sources = [s for s in ris_sources if s.get("id") == args.source_id]

    if not ris_sources:
        print("No RIS-API sources configured; nothing to fetch.")
        return 0

    print(f"Configured RIS sources: {len(ris_sources)}")
    selected = [s for s in ris_sources if s.get("tracking_mode") == "full_text"]
    if not selected:
        print("No RIS full_text sources configured; nothing to fetch.")
        return 0
    print(f"Fetching {len(selected)} RIS full_text sources:")
    for s in selected:
        print(f"  {s.get('id')}: {s.get('authoritative_url')}")

    if args.dry_run:
        return 0

    failures = 0
    for source in selected:
        try:
            _write_snapshot(source)
        except Exception as exc:
            failures += 1
            print(f"ERROR: failed to fetch {source.get('id')}: {exc}", file=sys.stderr)

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
