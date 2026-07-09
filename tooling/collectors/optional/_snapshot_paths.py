#!/usr/bin/env python3
"""
Path-containment helper shared by the law-snapshot fetchers.

`local_reference` values come from framework-refs/sources/registry.yaml, which
is a control-of-controls file at the process level but is not cryptographically
protected. A careless or malicious edit (or a compromised upstream source list)
must not be able to steer a fetch write outside the snapshots tree. This helper
resolves the target directory and refuses anything that escapes
framework-refs/snapshots/.

Copyright 2026 isms contributors
SPDX-License-Identifier: Apache-2.0
"""
from __future__ import annotations

from pathlib import Path


def resolve_snapshot_dir(repo_root: Path, local_reference: str | None) -> Path:
    """Resolve a registry local_reference to a directory inside the snapshots tree.

    Raises RuntimeError if the reference is empty or escapes
    ``framework-refs/snapshots/`` (e.g. via ``..`` segments or an absolute path).
    """
    snapshots_root = (repo_root / "framework-refs" / "snapshots").resolve()
    rel = str(local_reference or "").strip("/")
    if not rel:
        raise RuntimeError("local_reference is empty; refusing to write to repo root")
    target = (repo_root / rel).resolve()
    if target != snapshots_root and not target.is_relative_to(snapshots_root):
        raise RuntimeError(
            f"local_reference escapes framework-refs/snapshots/: {local_reference!r}"
        )
    return target
