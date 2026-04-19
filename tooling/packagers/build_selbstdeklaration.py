#!/usr/bin/env python3
"""
Build NISG 2026 § 33 Selbstdeklaration package.

The Selbstdeklaration is the structured self-declaration that wesentliche and
wichtige Einrichtungen must submit to the Bundesamt für Cybersicherheit by
2027-09-30 (or within 12 months of registration, whichever is later).

This packager produces a DE-language package covering:
  - Unternehmensangaben (from instance/config.yaml)
  - Systemlandschaft (scope, inventory)
  - Risikoanalyse (risk register as DE summary)
  - Lieferkette (supply-chain security)
  - Implementierte Risikomanagementmaßnahmen (per Impl Reg 2024/2690 Annex)

Copyright 2026 isms contributors
SPDX-License-Identifier: Apache-2.0
"""
from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def main() -> int:
    print("Building NISG 2026 § 33 Selbstdeklaration package.")
    stamp = datetime.now().strftime("%Y%m%dT%H%M%SZ")
    out = REPO_ROOT / "dist-selbstdeklaration" / f"selbstdeklaration-{stamp}"
    out.mkdir(parents=True, exist_ok=True)
    (out / "README.md").write_text("# Selbstdeklaration package\n\nStub; implement per SOP-102 and Impl Reg 2024/2690 Annex.\n")
    print(f"Package built at {out}")
    print()
    print("Implementation outline:")
    print("  1. Read instance/config.yaml for entity fields.")
    print("  2. Read template/governance/soa/soa.yaml for applicable controls.")
    print("  3. Read instance/governance/risk/register.yaml for risk summary (DE).")
    print("  4. Read Impl Reg 2024/2690 measures catalogue and map to ISMS implementation.")
    print("  5. Generate PAdES-ready DE PDF via Jinja template; mark for QES via SOP-201.")
    print("  6. Retain unsigned draft until Leitungsorgan signs per signature-policy.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
