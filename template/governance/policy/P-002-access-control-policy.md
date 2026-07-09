---
doc_id: P-002
doc_type: policy
title: Access Control Policy
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
  - iso27002:A.5.15
  - iso27002:A.5.16
  - iso27002:A.5.17
  - iso27002:A.5.18
  - iso27002:A.8.2
  - iso27002:A.8.3
  - iso27002:A.8.4
  - iso27002:A.8.5
signature_ref: null
---

# Access Control Policy

**P-002 Revision 1 (DRAFT)**

*Status: draft. Owner: role:ISMS-Manager. Next review: 2027-01-01.*

## 1. Purpose

Access control for information and systems: identity, authentication, authorisation, review.

## 2. Scope

Applies to {{entity.short_name}} and to all information, systems, personnel, and third parties within the ISMS scope per `governance/context/scope-statement.md`.

## 3. Policy statements
### 3.1 Principle

Access to information and information processing facilities shall be granted on the
basis of business need, least privilege, and need to know, and shall be authorised,
recorded, and reviewed (A.5.15).

### 3.2 Requirements

- Access shall be provisioned and de-provisioned through a formal process tied to the
  user lifecycle (A.5.16, A.5.18).
- Privileged access rights shall be restricted, individually attributable, and reviewed
  at least quarterly (A.8.2).
- Authentication shall use secure methods; multi-factor authentication shall be required
  for privileged and remote access (A.8.5).
- Information access shall be restricted in line with topic-specific access-control rules
  and the classification of the information (A.5.15, A.8.3).
- Access rights shall be reviewed at planned intervals and revoked promptly on role
  change or termination (A.5.18).

### 3.3 Prohibitions

- Shared or generic accounts shall not be used for privileged actions.
- Access shall not persist after the business need ends.

### 3.4 Responsibilities

- role:ISMS-Manager owns the access-control rules; system owners approve access;
  role:SysAdmin implements and reviews it.

### 3.5 Exceptions

Exceptions shall be risk-accepted per the risk acceptance process (`governance/risk/methodology.md`, logged in `governance/risk/acceptance-log.md`) with an expiry date and reviewed at the
next access review.

## 4. Roles and responsibilities

Per `users/roles.yaml`. Key accountability: role:ISMS-Manager.

## 5. Related documents

- Parent policy: `governance/policy/P-000-information-security-policy.md`
- Supporting procedures: SOP references to be added as they are drafted.
- Supporting standards: STD references to be added as they are drafted.

## 6. Compliance

Non-compliance is addressed per the applicable disciplinary procedure. Exceptions require risk acceptance per the risk acceptance process (`governance/risk/methodology.md`, logged in `governance/risk/acceptance-log.md`).

## 7. Revision history

| Rev | Date | Status | Change |
|---|---|---|---|
| 1 | {{entity.draft_date}} | draft | initial draft |
