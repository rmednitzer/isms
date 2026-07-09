#!/usr/bin/env python3
"""
Shared structure for provider-API evidence collectors (identity, vulnerability
management, backup, monitoring).

Design goals:
  - config-driven: connection details come from the `providers` block of
    instance/config.yaml, never hard-coded;
  - honest offline behaviour: with --dry-run, an unconfigured provider, or a
    missing endpoint/credential, the collector emits a schema-valid
    `not_collected` attestation rather than fabricating findings;
  - real live path: when configured, it performs an authenticated HTTP pull,
    hashes the raw response, and records it as evidence. Semantic parsing of
    provider-specific findings is a documented per-deployment extension; the
    timestamped, hashed API capture is itself valid evidence of the pull.

Output always conforms to tooling/schemas/attestation.schema.json.

Copyright 2026 isms contributors
SPDX-License-Identifier: Apache-2.0
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path

from ruamel.yaml import YAML

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
DEFAULT_CONFIG = REPO_ROOT / "instance" / "config.yaml"
yaml = YAML(typ="safe")


def load_provider(config_path: Path, category: str) -> dict:
    """Return the providers.<category> block from a config file, or {}."""
    if not config_path.is_file():
        return {}
    with config_path.open("r") as f:
        data = yaml.load(f) or {}
    providers = data.get("providers") or {}
    return providers.get(category) or {}


def build_attestation(
    *,
    control_id: str,
    attestation_type: str,
    collected_by: str,
    collection_method: str,
    source_system: str,
    observations: dict,
    source_endpoint: str | None = None,
    raw_hash: str | None = None,
) -> dict:
    att: dict = {
        "schema_version": 1,
        "control_id": control_id,
        "attestation_type": attestation_type,
        "collected_at": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "collected_by": collected_by,
        "collection_method": collection_method,
        "source_system": source_system,
        "observations": observations,
    }
    if source_endpoint:
        att["source_endpoint"] = source_endpoint
    if raw_hash:
        att["raw_snapshot_hash"] = raw_hash
    return att


def run_collector(
    *,
    category: str,
    control_id: str,
    attestation_type: str,
    source_system_default: str,
    collector_path: str,
    argv: list[str] | None = None,
) -> int:
    """Argparse + config-load + emit. Returns a process exit code."""
    parser = argparse.ArgumentParser(description=f"{attestation_type} evidence collector")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG), help="path to instance config.yaml")
    parser.add_argument("--dry-run", action="store_true", help="emit a not_collected attestation, no network")
    args = parser.parse_args(argv)

    provider = load_provider(Path(args.config), category)
    name = provider.get("name") or source_system_default
    configured = bool(provider.get("name"))
    endpoint_env = provider.get("endpoint_env")
    endpoint = os.environ.get(endpoint_env) if endpoint_env else None

    if args.dry_run or not configured or not endpoint:
        if args.dry_run:
            reason = "dry-run requested"
        elif not configured:
            reason = f"providers.{category} not configured in instance/config.yaml"
        else:
            reason = f"endpoint env {endpoint_env!r} not set in environment"
        att = build_attestation(
            control_id=control_id,
            attestation_type=attestation_type,
            collected_by=collector_path,
            collection_method="automated_test",
            source_system=name,
            observations={
                "status": "not_collected",
                "reason": reason,
                "provider_category": category,
            },
        )
        print(json.dumps(att, indent=2))
        return 0

    try:
        import requests
    except ImportError:  # pragma: no cover - requests is a declared dependency
        print("ERROR: requests not available for live pull", file=sys.stderr)
        return 1

    cred_env = provider.get("credential_env")
    token = os.environ.get(cred_env) if cred_env else None
    headers = {"User-Agent": "isms-evidence-collector/1.0", "Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        resp = requests.get(endpoint, timeout=60, headers=headers)
        resp.raise_for_status()
    except Exception as exc:
        print(f"ERROR: {name} pull from {endpoint} failed: {exc}", file=sys.stderr)
        return 1

    body = resp.text
    raw_hash = hashlib.sha256(body.encode("utf-8")).hexdigest()
    att = build_attestation(
        control_id=control_id,
        attestation_type=attestation_type,
        collected_by=collector_path,
        collection_method="api_pull",
        source_system=name,
        source_endpoint=endpoint,
        raw_hash=raw_hash,
        observations={
            "status": "collected",
            "http_status": resp.status_code,
            "response_bytes": len(body),
            "note": (
                "Raw API response captured and hashed. Provider-specific parsing "
                "of findings is a per-deployment extension of this collector."
            ),
        },
    )
    print(json.dumps(att, indent=2))
    return 0
