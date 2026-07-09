#!/usr/bin/env python3
"""
Build an audit pack bundle for an external audit engagement.

Produces dist-audit-pack/<audit_type>-<timestamp>/ with:
  - governance/   (all approved policies, SOPs, standards as rendered)
  - soa/          (Statement of Applicability + justifications)
  - risk/         (risk register, treatment plan, acceptance log)
  - evidence/     (recent attestations + manifests within audit window)
  - audits/       (prior audit records if applicable)
  - reviews/      (management review minutes)
  - README.md     (curated index with auditor orientation)

Copyright 2026 isms contributors
SPDX-License-Identifier: Apache-2.0
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from datetime import UTC, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DIST = REPO_ROOT / "dist-audit-pack"


AUDIT_ARG_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9-]*$")
PLACEHOLDER_RE = re.compile(r"\{\{.*?\}\}")
# Audit types that must not ship draft/placeholder content. A stage-1 (readiness)
# pack may legitimately show a work-in-progress program; a stage-2, surveillance,
# or recertification pack is a certification deliverable and must be complete.
CERTIFICATION_AUDITS = ("stage-2", "surveillance", "recertification")


def copytree_without_symlinks(src: Path, dst: Path, *, ignore=None) -> None:
    if src.is_symlink():
        raise RuntimeError(f"Refusing to package symlinked source directory: {src}")

    for entry in src.rglob("*"):
        if entry.is_symlink():
            raise RuntimeError(f"Refusing to package symlink in audit pack source tree: {entry}")

    shutil.copytree(src, dst, dirs_exist_ok=True, ignore=ignore)


def has_content(directory: Path) -> bool:
    """True if the directory holds at least one non-empty, non-scaffold file.

    A directory that contains only ``.gitkeep`` placeholders (the shipped
    skeleton state before ``make instantiate`` has run) is treated as empty so
    that packaging falls back to the populated ``template/`` layer instead of
    silently shipping an empty section.
    """
    if not directory.is_dir():
        return False
    for entry in directory.rglob("*"):
        if not entry.is_file() or entry.is_symlink():
            continue
        if entry.name == ".gitkeep":
            continue
        try:
            if entry.stat().st_size > 0:
                return True
        except OSError:
            continue
    return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", required=True, help="stage-1 | stage-2 | surveillance-YYYY | recertification-YYYY")
    args = parser.parse_args()

    if not AUDIT_ARG_PATTERN.match(args.audit):
        print(
            f"error: invalid --audit value {args.audit!r}; "
            "expected characters [A-Za-z0-9-] only (e.g. stage-1, surveillance-2026)",
            file=sys.stderr,
        )
        return 2

    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    out = DIST / f"{args.audit}-{stamp}"
    out.mkdir(parents=True, exist_ok=True)

    print(f"Building audit pack: {args.audit}")
    print(f"Output: {out}")

    warnings: list[str] = []

    # Governance / operations / users: prefer the instance-rendered layer, but
    # only when it has actually been instantiated. A bare .gitkeep scaffold must
    # not shadow the populated template layer (that would ship an empty pack).
    for sub in ["governance", "operations", "users"]:
        inst = REPO_ROOT / "instance" / sub
        tmpl = REPO_ROOT / "template" / sub
        if has_content(inst):
            src: Path | None = inst
        elif has_content(tmpl):
            src = tmpl
            if inst.is_dir():
                warnings.append(
                    f"{sub}/: instance layer is an empty scaffold; packaged from template/ "
                    f"instead. Run 'make instantiate' to render the instance before an audit."
                )
        else:
            src = None
            warnings.append(f"{sub}/: no content in instance/ or template/; section omitted from pack.")
        if src is not None:
            copytree_without_symlinks(src, out / sub)

    # Evidence (recent; scope decision is manual per audit type)
    ev_src = REPO_ROOT / "instance" / "evidence"
    if has_content(ev_src):
        copytree_without_symlinks(ev_src, out / "evidence")
    else:
        warnings.append(
            "evidence/: no attestations, manifests, or signed PDFs present; "
            "the pack ships no evidence."
        )

    # Framework refs (law snapshots that the ISMS maps to)
    fr_src = REPO_ROOT / "framework-refs"
    if has_content(fr_src):
        copytree_without_symlinks(
            fr_src,
            out / "framework-refs",
            ignore=shutil.ignore_patterns("*.xml", "*.tar.gz"),
        )
    else:
        warnings.append("framework-refs/: no content; section omitted from pack.")

    # Decisions
    dec_src = REPO_ROOT / "docs" / "decisions"
    if has_content(dec_src):
        copytree_without_symlinks(dec_src, out / "decisions")
    else:
        warnings.append("decisions/: no content; section omitted from pack.")

    # Scan the packaged tree for unresolved {{placeholder}} tokens: a pack full
    # of template placeholders is scaffolding, not an auditor deliverable.
    placeholder_files = sorted(
        str(p.relative_to(out))
        for p in out.rglob("*")
        if p.is_file() and p.suffix in {".md", ".yaml", ".yml"} and PLACEHOLDER_RE.search(
            p.read_text(encoding="utf-8", errors="replace")
        )
    )
    if placeholder_files:
        warnings.append(
            f"{len(placeholder_files)} packaged files contain unresolved "
            "{{placeholder}} tokens (run 'make instantiate' first)."
        )

    banner = ""
    if warnings:
        banner = "\n## ⚠ Readiness warnings\n\nThis pack was built with the following gaps:\n\n"
        banner += "".join(f"- {w}\n" for w in warnings)
        banner += "\nThis indicates a pre-instantiation or draft-stage program.\n"

    readme = out / "README.md"
    readme.write_text(f"""# Audit pack: {args.audit}

Built: {datetime.now(UTC).isoformat()}
Audit type: {args.audit}
{banner}

## Structure

- governance/       ISMS scope, policies, procedures, standards, SoA, risk, controls
- operations/       incidents, changes, audits (prior), exercises, reviews
- users/            roles, separation of duties, people-to-role bindings
- evidence/         attestations, manifests, signed PDFs
- framework-refs/   law snapshots and crosswalks
- decisions/        architectural decision records

## Audit orientation

Start at governance/context/scope-statement.md for the ISMS scope.
Then governance/soa/soa.yaml for the Statement of Applicability.
Then governance/risk/register.yaml for the risk register.
Evidence traces from SoA to evidence/ via controls/evidence-plan.yaml.

## Integrity

All commits signed; see .gitsigners and CODEOWNERS at repo root.
QES-signed PDFs under evidence/signatures/; verify via EU DSS.
""", encoding="utf-8")

    if warnings:
        print("\nWARNINGS:", file=sys.stderr)
        for w in warnings:
            print(f"  - {w}", file=sys.stderr)

    print(f"Audit pack built at {out}")

    # Certification-grade packs must not ship draft/placeholder/empty content.
    if args.audit.startswith(CERTIFICATION_AUDITS) and warnings:
        print(
            f"\nERROR: refusing to certify a '{args.audit}' pack with readiness "
            "warnings (see above). Build a 'stage-1' readiness pack, or complete "
            "instantiation, evidence, and SoA assessment first.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
