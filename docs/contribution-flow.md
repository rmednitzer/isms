---
doc_id: DOC-005
doc_type: standard
title: Contribution flow
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
  - iso27001:8.1
signature_ref: null
---

# Contribution flow

**DOC-005 Revision 1 (DRAFT)**

*Status: draft. Owner: role:ISMS-Manager. Next review: 2027-01-01.*

## 1. Change types

| Type | Trigger | Authority | Flow |
|---|---|---|---|
| Editorial | typo, formatting | PR author | direct PR, CODEOWNER review, merge |
| Minor governance | clarification without meaning change | ISMS Manager | RFC optional, PR, CODEOWNER review, merge, no revision bump |
| Material governance | changes obligation, threshold, scope | ISMS Manager + CISO | RFC required, revision bump, approval ceremony if policy or plan |
| Tooling | schema, validator, collector, packager | SysAdmin + ISMS Manager | RFC optional for schema changes, PR, tests required, merge |
| Structural | repo layout, CI, CODEOWNERS, signature policy | CISO | RFC required, DEC record, dual CODEOWNER approval |

## 2. RFC

Change requests for material and structural changes live under `instance/operations/changes/rfcs/RFC-NNNN.md`. Front-matter per document-control; body sections:

1. Context (what is, why change).
2. Proposal (what, how).
3. Alternatives considered.
4. Impact (CACE analysis: blast radius, dependencies, rollback).
5. Evidence of review (who reviewed, when, outcome).
6. Decision (approved, rejected, deferred).

## 3. Branch and PR

Branches named `<type>/<slug>`, for example `policy/p-005-revision-2`, `tooling/validator-frontmatter-fix`, `law/nisg-2026-verordnung-1-impact`.

PRs must:

- Reference the RFC (if any).
- Carry signed commits.
- Pass `make validate` and `make test`.
- Receive CODEOWNER approval per the paths touched.

## 4. Approval for status=approved transitions

A PR that transitions an artefact from draft or under_review to approved:

- Must include the QES-signed PDF under `instance/evidence/signatures/` (or set `interim_signature: true` if interim posture applies per DOC-002 § 5).
- Must be approved by a CODEOWNER authorised for the role named in `approved_by`.
- Merges with a signed merge commit.

## 5. Revert

Merged changes may be reverted via `git revert` plus a new signed commit. Reverts are not editorial; they require the same CODEOWNER approval as the original change.

## 6. Revision history

| Rev | Date | Status | Change |
|---|---|---|---|
| 1 | 2026-04-19 | draft | initial draft |
