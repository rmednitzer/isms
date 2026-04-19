---
doc_id: REC-2026-800
doc_type: report
title: Report template
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
  - iso27001:9.1
  - iso27001:9.3
signature_ref: null
---

# Report template

**REC-2026-800 Revision 1 (DRAFT)**

*Status: draft template. Owner: role:ISMS-Manager. Next review: 2027-01-01.*

## Usage

Copy to `instance/operations/<area>/<REC-YYYY-NNN>.md` when issuing a
standalone report (KPI report, control-coverage report, audit findings
summary, regulatory-watch digest). Section structure follows DOC-009
section 7.6.

## 1. Purpose and audience

State the purpose of the report and the primary audience (for instance,
management review attendees, external auditor, Bundesamt).

## 2. Scope of the reported period

- Period covered: YYYY-MM-DD to YYYY-MM-DD
- Systems, services, units in scope: TODO
- Systems, services, units explicitly excluded: TODO

## 3. Method and data sources

Explain how the data was collected. Reference collector scripts under
`tooling/collectors/` and manifests under `instance/evidence/manifests/`.

## 4. Findings

| ID | Finding | Severity | Control | Evidence |
|---|---|---|---|---|
| F-001 | TODO | low \| medium \| high \| critical | e.g. A.5.24 | path |

## 5. Risk and control implications

Describe how the findings affect the risk register (`instance/governance/risk/register.yaml`)
and the Statement of Applicability. Flag any control whose effectiveness
is in question.

## 6. Recommendations and CAPA

- CAPA-NNN: action, owner, due date, status

## 7. Distribution list

- role:CISO
- role:ISMS-Manager
- role:Management
- TODO additional recipients

## 8. Revision history

| Rev | Date | Status | Change |
|---|---|---|---|
| 1 | {{entity.draft_date}} | draft | initial draft |
