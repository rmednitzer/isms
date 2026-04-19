---
doc_id: DOC-009
doc_type: standard
title: Editorial style guide
revision: 1
status: draft
approved_date: null
approved_by: null
owner: role:ISMS-Manager
classification: internal
supersedes_revision: null
next_review: 2028-04-19
language: en
framework_refs:
  - iso27001:7.5.2
  - iso27001:7.5.3
signature_ref: null
---

# Editorial style guide

**DOC-009 Revision 1 (DRAFT)**

*Status: draft. Owner: role:ISMS-Manager. Next review: 2028-04-19.*

## 1. Purpose

Sets the editorial conventions every governance artefact follows. DOC-001
governs document control (IDs, revisions, front-matter, visible header);
this document governs register, structure by document type, and formatting.
Where the two overlap, DOC-001 is authoritative for control fields and this
document is authoritative for prose and section structure.

## 2. Scope

Applies to every markdown artefact in scope of DOC-001 plus the rendered
PDF outputs produced by `tooling/packagers/render_pdf.py`.

## 3. Register

Governance artefacts are read by auditors, legal reviewers, and the
Leitungsorgan. They are not peer-engineering notes.

- Use formal, precise English (or formal German for authority-facing text
  per `docs/bilingualism.md`).
- Use the imperative mood for procedure steps ("Raise a ticket. Record the
  outcome.") and the declarative mood for policy statements ("The
  organisation maintains an incident register.").
- Prefer the active voice unless the actor is deliberately unspecified by
  policy.
- Avoid jargon outside the domain being regulated. Define acronyms on first
  use per document.
- Avoid marketing language and hedging. If a requirement is mandatory, say
  "shall" or "must"; if recommended, "should"; if permitted, "may"; if
  prohibited, "shall not". These terms match ISO/IEC Directives Part 2.

## 4. Formatting

- UTF-8 source. Unix line endings.
- No em dashes, no double dashes. Use comma, semicolon, period, parenthesis.
- Dates `YYYY-MM-DD`. Times 24h, seconds optional, timezone where relevant
  (prefer UTC, use `Z` suffix). SI units with a non-breaking space between
  value and unit. Currency in EUR unless otherwise specified.
- Headings ATX (`#`, `##`). One `#` per document (the title), supplied by
  the visible header block from DOC-001 section 4.
- Numbered top-level sections (1., 2., 3.).
- Tables in GFM with header separator.
- Code blocks fenced with language hint for shell, yaml, json, python.
- Lists: `- ` for unordered, `1. ` for ordered. No trailing punctuation on
  list items unless the item is a full sentence.
- Line length: soft-wrap at 100 where practical; do not hard-wrap inside
  sentences that carry legal or regulatory quotations.

## 5. Language

- Internal artefacts: English unless the document declares `language: de`.
- Authority-facing artefacts (Selbstdeklaration, CERT.at Fruehwarnung,
  Bundesamt correspondence, registration records): German is authoritative.
- Bilingual parity is required when `bilingual: true`; validator
  `validate_bilingual.py` enforces structural parity.

## 6. Visible header

Per DOC-001 section 4. The PDF renderer regenerates a cover page from the
front-matter and preserves the in-body visible header as internal preview
form. Do not edit the in-body header to depart from the front-matter.

## 7. Section skeleton by document type

Every artefact of a given `doc_type` uses the structure below unless the
template for that artefact provides a clearly documented override (for
example, cert-at-fruehwarnung-template is authority-formatted DE).

Validator alignment: `tooling/validators/validate_frontmatter.py` covers
control fields; reviewers check section skeleton during PR review against
the checklist in section 10.

### 7.1 Policy (P-NNN)

1. Purpose
2. Scope
3. Policy statements (Principle, Requirement, Prohibition,
   Responsibilities, Exceptions)
4. Roles and responsibilities
5. Related documents
6. Compliance
7. Revision history

### 7.2 Procedure (SOP-NNN)

1. Purpose
2. Scope
3. Roles
4. Inputs
5. Procedure (numbered steps with trigger, action, actor, output, evidence)
6. Outputs
7. Frequency
8. Metrics and KPIs
9. Related documents
10. Revision history

### 7.3 Standard (STD-NNN)

1. Purpose
2. Scope
3. Requirements (minimum parameters, preferred parameters, prohibited
   configurations, applicability by system class)
4. Verification
5. Exceptions
6. Revision history

### 7.4 Plan (PLAN-NNN)

1. Purpose
2. Scope
3. Objectives and success criteria
4. Assumptions and constraints
5. Activities, milestones, schedule
6. Roles and responsibilities
7. Resources and budget (where applicable)
8. Risks and mitigations
9. Monitoring and review
10. Revision history

### 7.5 Record (REC-YYYY-NNN, INC-YYYY-NNN, DEC-YYYY-NNN, IA-YYYY-NNN, RFC-NNNN)

Records are append-only facts of what happened. Structure varies by record
sub-type; the minimum is:

1. Identification (IDs, dates, actors)
2. Context or trigger
3. Substance (incident facts, decision, assessment outcome, change detail)
4. Outcome or decision
5. Evidence pointers (to `instance/evidence/`)
6. Revision history

### 7.6 Report (REC-YYYY-NNN with doc_type=report)

1. Purpose and audience
2. Scope of the reported period
3. Method and data sources
4. Findings
5. Risk and control implications
6. Recommendations and CAPA
7. Distribution list
8. Revision history

## 8. Cross-references

- Use backtick-fenced repo-relative paths (e.g. `template/governance/policy/P-000-information-security-policy.md`).
- Use document IDs (P-000, SOP-001, STD-001) in prose. The renderer does
  not auto-link; reviewers verify the ID exists.
- Framework references use the `<framework>:<identifier>` schema defined
  in `tooling/schemas/frontmatter.schema.json`, for example
  `iso27001:A.5.1`, `nisg2026:§32`, `gdpr:Art.32`.

## 9. Classification marking

Per DOC-001. The PDF renderer marks the classification in the top-right
page header and in the cover meta block. Confidential and restricted
artefacts receive warning-tone colour; public and internal stay muted.

## 10. Review checklist

A reviewer applies this checklist before approving a PR that introduces or
revises a governance artefact:

- [ ] Front-matter validates (`make validate`).
- [ ] Visible header matches DOC-001 section 4 and the front-matter.
- [ ] `doc_type` matches the section skeleton (section 7 of this document).
- [ ] Register is formal, imperative or declarative as appropriate.
- [ ] No em dashes, no double dashes, no marketing language, no hedging.
- [ ] Dates, times, units follow section 4.
- [ ] Framework references resolve against the control catalogues.
- [ ] Revision history is updated.
- [ ] If approved and doc_type in (policy, plan): `signature_ref` or
      `interim_signature: true` is set.

## 11. Revision history

| Rev | Date | Status | Change |
|---|---|---|---|
| 1 | 2026-04-19 | draft | initial draft, consolidating editorial rules previously split across CLAUDE.md and CONTRIBUTING.md |
