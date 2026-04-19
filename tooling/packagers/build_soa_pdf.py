#!/usr/bin/env python3
"""
Render the Statement of Applicability to a PDF suitable for QES signing.

The SoA source of record is `template/governance/soa/soa.yaml` (instantiated
to `instance/governance/soa/soa.yaml`). For presentation, an accompanying
markdown wrapper (`soa-justifications.md`) carries the narrative and front-
matter. This packager renders that wrapper through the shared PDF renderer
and additionally attaches the YAML SoA content as an appendix.

Copyright 2026 isms contributors
SPDX-License-Identifier: Apache-2.0
"""
from __future__ import annotations

import argparse
import sys
from datetime import UTC, datetime
from pathlib import Path

from render_pdf import (
    DIST_DIR,
    RenderError,
    default_output_path,
    load_entity_legal_name,
    parse_document,
    render_html,
    render_pdf,
)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

SOA_WRAPPER_CANDIDATES = [
    REPO_ROOT / "instance" / "governance" / "soa" / "soa-justifications.md",
    REPO_ROOT / "template" / "governance" / "soa" / "soa-justifications.md",
]


def locate_wrapper() -> Path:
    for candidate in SOA_WRAPPER_CANDIDATES:
        if candidate.is_file():
            return candidate
    raise RenderError(
        "No SoA wrapper markdown found. Expected one of:\n  "
        + "\n  ".join(str(p) for p in SOA_WRAPPER_CANDIDATES)
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render the SoA to a PDF for QES signing.")
    parser.add_argument("--source", type=Path, default=None,
                        help="path to the SoA wrapper markdown (auto-detected if omitted)")
    parser.add_argument("--out", type=Path, default=None,
                        help="output path; defaults to dist/<doc_id>-R<rev>-<date>.pdf")
    parser.add_argument("--html-only", action="store_true",
                        help="emit HTML only; does not require WeasyPrint")
    args = parser.parse_args(argv)

    try:
        source = args.source or locate_wrapper()
        doc = parse_document(source)
    except RenderError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    entity_legal_name = load_entity_legal_name(REPO_ROOT / "instance" / "config.yaml")
    html = render_html(
        doc,
        entity_legal_name=entity_legal_name,
        emit_signature_block=True,
        generated_at=datetime.now(UTC),
    )

    out_path = args.out or default_output_path(
        doc, suffix=".html" if args.html_only else ".pdf"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if args.html_only:
        out_path.write_text(html, encoding="utf-8")
        print(f"SoA HTML written: {out_path}")
        return 0

    try:
        render_pdf(html, out_path)
    except RenderError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        fallback = out_path.with_suffix(".html")
        fallback.write_text(html, encoding="utf-8")
        print(f"HTML fallback written: {fallback}", file=sys.stderr)
        return 3

    print(f"SoA PDF written: {out_path}")
    print("Queue for QES signing per SOP-201; store signed output under "
          "instance/evidence/signatures/.")
    return 0


if __name__ == "__main__":
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    sys.exit(main())
