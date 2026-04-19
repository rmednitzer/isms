---
doc_id: DOC-001
doc_type: standard
title: Document control specification
revision: 1
status: draft
approved_date: null
approved_by: null
owner: role:ISMS-Manager
classification: internal
supersedes_revision: null
next_review: 2027-01-01
language: en
framework_refs:
  - iso27001:7.5.2
  - iso27001:7.5.3
signature_ref: null
---

# Document control specification

**DOC-001 Revision 1 (DRAFT)**

*Status: draft. Owner: role:ISMS-Manager. Next review: 2027-01-01.*

## 1. Purpose

Specifies the document control model for all governance artefacts in this repository, in conformance with ISO/IEC 27001:2022 clauses 7.5.2 (creating and updating) and 7.5.3 (control of documented information).

## 2. Scope

Applies to every markdown file under `docs/`, `template/governance/`, `template/operations/`, `instance/governance/`, and `instance/operations/` that represents governance intent. Evidence artefacts under `instance/evidence/` are append-only records and do not carry revision front-matter (they carry their own attestation schema).

## 3. Front-matter specification

Every in-scope markdown file begins with YAML front-matter conforming to `tooling/schemas/frontmatter.schema.json`.

| Field | Type | Required | Description |
|---|---|---|---|
| doc_id | string | yes | unique identifier matching the pattern in § 5 |
| doc_type | enum | yes | policy, procedure, standard, record, plan, report |
| title | string | yes | human-readable title |
| revision | integer | yes | monotonic, starts at 1, increments on each approved revision |
| status | enum | yes | draft, under_review, approved, superseded, retired |
| approved_date | date or null | conditional | required iff status=approved; YYYY-MM-DD |
| approved_by | string or null | conditional | role: or person: prefix; required iff status=approved |
| owner | string | yes | role reference, role: prefix |
| classification | enum | yes | public, internal, confidential, restricted |
| supersedes_revision | integer or null | conditional | required on revisions greater than 1 |
| next_review | date | yes | YYYY-MM-DD |
| language | enum | yes | en or de |
| framework_refs | array of strings | yes | control identifiers that must resolve in `template/governance/controls/` |
| signature_ref | string or null | conditional | path to QES-signed PDF under `instance/evidence/signatures/`; required iff status=approved and doc_type in policy or plan |
| interim_signature | boolean | optional | true marks the artefact as approved without QES during the interim posture |

## 4. Visible header

Immediately after front-matter, the first content block is always:

```
# <Title>

**<DOC_ID> Revision <N> - <YYYY-MM-DD>**

*Status: <status>. Owner: <owner>. Next review: <next_review>.*
```

For draft state, the date is replaced by "(DRAFT)":

```
**<DOC_ID> Revision <N> (DRAFT)**
```

For interim signature posture, an additional line follows:

```
*Interim: legal signature pending QES integration. Approved via git-level only.*
```

## 5. Document ID scheme

| Prefix | Type | Range | Purpose |
|---|---|---|---|
| DOC- | repo-level control documents | DOC-001 to DOC-099 | operating rules of the repo itself |
| P- | policy | P-000 to P-099 | top-level and topic policies |
| SOP- | procedure | SOP-001 to SOP-199 | standard operating procedures |
| STD- | standard | STD-001 to STD-099 | technical baselines |
| PLAN- | plan | PLAN-001 to PLAN-099 | BCP, DR, risk treatment, audit plans |
| REC-YYYY- | record | REC-2026-001 | records (audit findings, review minutes) |
| INC-YYYY- | incident | INC-2026-001 | incident records |
| RFC- | change request | RFC-0001 | change requests (monotonic, not year-prefixed) |
| IA-YYYY- | impact assessment | IA-2026-001 | law-change impact assessments |
| DEC-YYYY- | architectural decision | DEC-2026-001 | architectural decision records |
| TMPL- | operational template | TMPL-001 | pre-filled operational templates (e.g. Frühwarnung) |

## 6. Revision rules

- First draft: revision=1, status=draft.
- Submitted for review: status=under_review, revision unchanged.
- Approved: status=approved, approved_date and approved_by populated, signature_ref populated for policies and plans (or interim_signature=true during interim posture).
- Material change: new revision N+1 opened as status=draft with supersedes_revision=N. The previous revision keeps its status until the new revision is approved; at that point the previous revision becomes status=superseded.
- Editorial change (typography, formatting): revision bump not required. Record as editorial commit referencing the original approval commit.
- Retirement: status=retired. File retained in repo. Supersession chain not broken.

## 7. Approval cycle

Two layers per `docs/signature-policy.md`:

1. Git-level: the PR merging the approved state carries a signed commit by a CODEOWNER of the file.
2. Legal-level (policies and plans): PDF export signed with eIDAS-QES by the accountable role, committed under `instance/evidence/signatures/`, referenced in `signature_ref`.

Both layers are required for policies and plans. SOPs, standards, and internal records require git-level only unless a specific policy elevates them.

## 8. Review cycle

- Policies and plans: `next_review` within 12 months of `approved_date`.
- Procedures: `next_review` within 12 months.
- Standards: `next_review` within 24 months.
- Reviews tracked via SOP-006 (internal audit programme) and may produce a new revision or a "reviewed, no change" record with status unchanged and `next_review` advanced.

## 9. Retention

Superseded and retired files remain in the repository indefinitely. Git history is the retention evidence. Exports of superseded signed PDFs retained in `instance/evidence/signatures/archive/` for seven years by default, longer where law requires.

## 10. Validation

`tooling/validators/validate_frontmatter.py` enforces this specification on every in-scope markdown file. Runs in pre-commit and in `.github/workflows/validate.yaml`. Violation blocks commit.

Editorial conventions (register, section structure by `doc_type`, formatting) are governed by `docs/style-guide.md` (DOC-009). PDF presentation is governed by `tooling/packagers/render_pdf.py` and its Jinja template under `tooling/packagers/templates/pdf/`, which regenerates a cover page from the front-matter and preserves the in-body visible header as the internal preview form.

Additional validators:

- `validate_crossrefs.py`: every framework_ref resolves against the control catalogues in `template/governance/controls/`.
- `validate_supersession.py`: revision chains are consistent; no orphaned supersedes_revision references.
- `validate_signatures.py`: signature_ref paths resolve to existing files; signed-commit enforcement on main.
- `validate_doc_type_coverage.py`: every `doc_type` enum value has at least one template under `template/` to guide downstream deployments.

## 11. Revision history

| Rev | Date | Status | Change |
|---|---|---|---|
| 1 | 2026-04-19 | draft | initial draft |
