#!/usr/bin/env python3
"""
Privileged-access evidence collector (identity provider, e.g. Keycloak).

Evidence for A.8.2 Privileged access rights: pulls the current privileged-role
membership from the configured identity provider. Config: providers.identity in
instance/config.yaml. Offline/unconfigured runs emit a not_collected attestation.

Copyright 2026 isms contributors
SPDX-License-Identifier: Apache-2.0
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _provider_common import run_collector


def main() -> int:
    return run_collector(
        category="identity",
        control_id="A.8.2",
        attestation_type="privileged_access_review",
        source_system_default="identity-provider",
        collector_path="tooling/collectors/optional/keycloak_privileged_access.py",
    )


if __name__ == "__main__":
    sys.exit(main())
