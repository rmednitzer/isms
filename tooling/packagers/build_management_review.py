#!/usr/bin/env python3
"""
Generate the management-review input pack per ISO/IEC 27001:2022 clause 9.3.2.

Assembles a structured agenda from committed ISMS data (objectives, KPIs,
risk register and treatment plan, incidents, audit records, interested
parties, control coverage, regulatory changes, and prior review actions).
Sections with no committed records are emitted with an explicit
"to be completed at the review" marker so the pack is honest about gaps
rather than silently empty.

The pack is an *input* for the review meeting; the outputs (decisions,
resource allocations, improvement actions) are recorded separately in the
management-review minutes per clause 9.3.3.

Copyright 2026 isms contributors
SPDX-License-Identifier: Apache-2.0
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

from ruamel.yaml import YAML

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DIST = REPO_ROOT / "dist-management-review"
yaml = YAML(typ="safe")

PERIOD_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9-]*$")


def _default_period() -> str:
    """Current calendar quarter label, e.g. 2026-Q3 (not month-based %m)."""
    now = datetime.now(UTC)
    return f"{now.year}-Q{(now.month - 1) // 3 + 1}"

TODO = "_No committed records found; to be completed at the review._"


def _prefer(repo_root: Path, relative: str) -> Path:
    """Prefer the instance-rendered artefact, but only when it has real content.

    An empty or stub instance file must not shadow a populated template file
    (the same failure class fixed in build_audit_pack).
    """
    inst = repo_root / "instance" / relative
    if inst.is_file() and inst.stat().st_size > 0:
        return inst
    return repo_root / "template" / relative


def _load_yaml(path: Path) -> dict:
    if not path.is_file():
        return {}
    with path.open("r") as f:
        return yaml.load(f) or {}


def _content_files(directory: Path, pattern: str = "*") -> list[Path]:
    if not directory.is_dir():
        return []
    return [p for p in directory.glob(pattern) if p.is_file() and p.name != ".gitkeep"]


def control_coverage(repo_root: Path) -> dict:
    """Summarise SoA applicability, implementation, and evidence binding."""
    soa = _load_yaml(_prefer(repo_root, "governance/soa/soa.yaml"))
    plan = _load_yaml(_prefer(repo_root, "governance/controls/evidence-plan.yaml"))
    controls = soa.get("controls", [])
    bound: set[str] = set()
    for task in plan.get("evidence_tasks", []):
        for cid in task.get("control_ids", []):
            bound.add(cid)
    applicable = [c for c in controls if c.get("applicable") == "yes"]
    assessed = [c for c in applicable if c.get("status") not in (None, "", "not_assessed")]
    with_evidence = [c for c in applicable if c.get("id") in bound]
    return {
        "total": len(controls),
        "applicable": len(applicable),
        "assessed": len(assessed),
        "with_evidence_task": len(with_evidence),
    }


def gather(repo_root: Path) -> dict:
    objectives = _load_yaml(_prefer(repo_root, "governance/objectives/isms-objectives.yaml")).get(
        "objectives", []
    )
    kpis = _load_yaml(_prefer(repo_root, "governance/objectives/kpi-definitions.yaml")).get("kpis", [])
    parties = _load_yaml(_prefer(repo_root, "governance/context/interested-parties.yaml")).get(
        "interested_parties", []
    )
    risk = _load_yaml(_prefer(repo_root, "governance/risk/register.yaml"))
    treatment = _load_yaml(_prefer(repo_root, "governance/risk/treatment-plan.yaml"))

    incidents_active = _content_files(repo_root / "instance/operations/incidents/active")
    incidents_closed = _content_files(repo_root / "instance/operations/incidents/closed")
    audits = _content_files(repo_root / "instance/operations/audits", "**/*")
    prior_reviews = _content_files(repo_root / "instance/operations/reviews", "**/*")
    deltas = _content_files(repo_root / "framework-refs/currency/deltas", "**/*")

    return {
        "objectives": objectives,
        "kpis": kpis,
        "interested_parties": parties,
        "risks": risk.get("risks", []),
        "treatment_plan": treatment.get("treatment_plan", []),
        "incidents_active": incidents_active,
        "incidents_closed": incidents_closed,
        "audits": audits,
        "prior_reviews": prior_reviews,
        "regulatory_deltas": deltas,
        "coverage": control_coverage(repo_root),
    }


def _rel(paths: list[Path], repo_root: Path) -> list[str]:
    return [str(p.relative_to(repo_root)) for p in paths]


def render_markdown(data: dict, period: str, generated_at: str, repo_root: Path) -> str:
    cov = data["coverage"]
    lines: list[str] = []
    lines.append(f"# Management review input pack - {period}")
    lines.append("")
    lines.append(f"Generated: {generated_at}")
    lines.append("Basis: ISO/IEC 27001:2022 clause 9.3.2 (management review inputs).")
    lines.append("")
    lines.append(
        "This is an input pack assembled from committed ISMS data. Review outputs "
        "(decisions, actions, resources) are recorded in the review minutes per clause 9.3.3."
    )
    lines.append("")

    lines.append("## a) Status of actions from previous management reviews")
    lines.append("")
    if data["prior_reviews"]:
        lines.append(f"{len(data['prior_reviews'])} prior review record(s) on file:")
        lines.extend(f"- {p}" for p in _rel(data["prior_reviews"], repo_root))
    else:
        lines.append("No prior review records on file (first review, or none committed). " + TODO)
    lines.append("")

    lines.append("## b) Changes in external and internal issues relevant to the ISMS")
    lines.append("")
    if data["regulatory_deltas"]:
        lines.append("Regulatory/source deltas recorded since last review:")
        lines.extend(f"- {p}" for p in _rel(data["regulatory_deltas"], repo_root))
    else:
        lines.append("No committed regulatory deltas since last review. " + TODO)
    lines.append("")

    lines.append("## c) Changes in needs and expectations of interested parties")
    lines.append("")
    if data["interested_parties"]:
        lines.append("| ID | Party | Key requirements |")
        lines.append("|---|---|---|")
        for p in data["interested_parties"]:
            reqs = "; ".join(p.get("requirements") or []) or "-"
            lines.append(f"| {p.get('id', '-')} | {p.get('name', '-')} | {reqs} |")
    else:
        lines.append(TODO)
    lines.append("")

    lines.append("## d) Information security performance and effectiveness")
    lines.append("")
    lines.append("### d.1 Fulfilment of information security objectives")
    lines.append("")
    if data["objectives"]:
        lines.append("| Objective | Title | Target date |")
        lines.append("|---|---|---|")
        for o in data["objectives"]:
            lines.append(
                f"| {o.get('id', '-')} | {o.get('title', '-')} | {o.get('target_date', '-')} |"
            )
    else:
        lines.append(TODO)
    lines.append("")
    lines.append("### d.2 Monitoring and measurement results (KPIs)")
    lines.append("")
    if data["kpis"]:
        lines.append("| KPI | Measure | Target | Cadence | Latest value |")
        lines.append("|---|---|---|---|---|")
        for k in data["kpis"]:
            lines.append(
                f"| {k.get('id', '-')} | {k.get('measure', '-')} | {k.get('target', '-')} "
                f"| {k.get('cadence', '-')} | _enter at review_ |"
            )
    else:
        lines.append(TODO)
    lines.append("")
    lines.append("### d.3 Control coverage (Statement of Applicability)")
    lines.append("")
    lines.append(f"- Controls in SoA: {cov['total']}")
    lines.append(f"- Applicable: {cov['applicable']}")
    lines.append(f"- Assessed (status not `not_assessed`): {cov['assessed']}")
    lines.append(f"- Applicable controls with an evidence task bound: {cov['with_evidence_task']}")
    lines.append("")
    lines.append("### d.4 Audit results")
    lines.append("")
    if data["audits"]:
        lines.append(f"{len(data['audits'])} audit record(s) on file:")
        lines.extend(f"- {p}" for p in _rel(data["audits"], repo_root))
    else:
        lines.append("No committed audit records in period. " + TODO)
    lines.append("")
    lines.append("### d.5 Nonconformities and corrective actions")
    lines.append("")
    lines.append(
        "Trend in nonconformities and corrective actions to be reported from the "
        "nonconformity register. " + TODO
    )
    lines.append("")
    lines.append("### d.6 Incidents in period")
    lines.append("")
    lines.append(f"- Active incidents: {len(data['incidents_active'])}")
    lines.append(f"- Closed incidents on file: {len(data['incidents_closed'])}")
    if data["incidents_closed"]:
        lines.extend(f"  - {p}" for p in _rel(data["incidents_closed"], repo_root))
    lines.append("")

    lines.append("## e) Feedback from interested parties")
    lines.append("")
    lines.append(TODO)
    lines.append("")

    lines.append("## f) Results of risk assessment and status of the risk treatment plan")
    lines.append("")
    lines.append(f"- Risks in register: {len(data['risks'])}")
    lines.append(f"- Entries in treatment plan: {len(data['treatment_plan'])}")
    if not data["risks"]:
        lines.append("")
        lines.append(
            "Risk register is empty. A risk assessment must be performed and its results "
            "presented here before certification (clause 6.1.2, 8.2)."
        )
    lines.append("")

    lines.append("## g) Opportunities for continual improvement")
    lines.append("")
    lines.append(TODO)
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(
        "Reviewers: role:Management (chair), role:CISO, role:ISMS-Manager, role:DPO. "
        "Record decisions and actions in the review minutes (clause 9.3.3)."
    )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--period",
        default=_default_period(),
        help="review period label, e.g. 2026-H1 or 2026-Q3 (chars [A-Za-z0-9-])",
    )
    parser.add_argument("--dry-run", action="store_true", help="print to stdout, do not write a file")
    args = parser.parse_args()

    if not PERIOD_PATTERN.match(args.period):
        print(
            f"error: invalid --period {args.period!r}; expected characters [A-Za-z0-9-] only",
            file=sys.stderr,
        )
        return 2

    generated_at = datetime.now(UTC).isoformat()
    data = gather(REPO_ROOT)
    markdown = render_markdown(data, args.period, generated_at, REPO_ROOT)

    if args.dry_run:
        print(markdown)
        return 0

    DIST.mkdir(parents=True, exist_ok=True)
    out = DIST / f"management-review-input-{args.period}.md"
    out.write_text(markdown, encoding="utf-8")
    print(f"Management review input pack written to {out}")
    print(
        f"Coverage: {data['coverage']['applicable']} applicable controls, "
        f"{data['coverage']['with_evidence_task']} with evidence tasks; "
        f"{len(data['risks'])} risks; {len(data['incidents_closed'])} closed incidents on file."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
