---
doc_id: P-007
doc_type: policy
title: Secure Development Policy
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
  - iso27002:A.8.25
  - iso27002:A.8.26
  - iso27002:A.8.27
  - iso27002:A.8.28
  - iso27002:A.8.29
  - iso27002:A.8.30
  - iso27002:A.8.31
  - iso27002:A.8.32
  - iso27002:A.8.33
signature_ref: null
---

# Secure Development Policy

**P-007 Revision 1 (DRAFT)**

*Status: draft. Owner: role:ISMS-Manager. Next review: 2027-01-01.*

## 1. Purpose

Security in development life cycle: design, coding, testing, change management.

## 2. Scope

Applies to {{entity.short_name}} and to all information, systems, personnel, and third parties within the ISMS scope per `governance/context/scope-statement.md`.

## 3. Policy statements
### 3.1 Principle

Security shall be designed into information systems and software across the development
lifecycle, from requirements through secure coding, testing, and change management
(A.8.25).

### 3.2 Requirements

- Secure development rules and secure coding principles shall be defined and applied
  (A.8.25, A.8.28).
- Security requirements shall be specified for new systems and for changes (A.8.26).
- Secure system architecture and engineering principles shall be followed (A.8.27).
- Development, test, and production environments shall be separated (A.8.31).
- Changes shall follow change management, test data shall be protected, and security
  testing shall be performed in development and acceptance (A.8.29, A.8.32, A.8.33).
- Outsourced development shall be directed, monitored, and reviewed (A.8.30).

### 3.3 Prohibitions

- Production data shall not be used as test data unless protected per A.8.33.
- Unreviewed changes shall not be promoted to production.

### 3.4 Responsibilities

- role:CISO owns the secure-development rules; development teams apply them; change
  approvers gate promotion to production.

### 3.5 Exceptions

Exceptions shall be risk-accepted per SOP-005 and recorded against the affected system.

## 4. Roles and responsibilities

Per `users/roles.yaml`. Key accountability: role:ISMS-Manager.

## 5. Related documents

- Parent policy: `governance/policy/P-000-information-security-policy.md`
- Supporting procedures: SOP references to be added as they are drafted.
- Supporting standards: STD references to be added as they are drafted.

## 6. Compliance

Non-compliance is addressed per the applicable disciplinary procedure. Exceptions require risk acceptance per SOP-005.

## 7. Revision history

| Rev | Date | Status | Change |
|---|---|---|---|
| 1 | {{entity.draft_date}} | draft | initial draft |
