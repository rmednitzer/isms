#!/usr/bin/env python3
"""
Log-integrity evidence collector (SIEM/monitoring provider, e.g. Wazuh).

Evidence for A.8.15 Logging: pulls log-source coverage and integrity state from
the configured monitoring provider. Config: providers.monitoring in
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
        category="monitoring",
        control_id="A.8.15",
        attestation_type="log_integrity",
        source_system_default="monitoring-provider",
        collector_path="tooling/collectors/optional/wazuh_log_integrity.py",
    )


if __name__ == "__main__":
    sys.exit(main())
