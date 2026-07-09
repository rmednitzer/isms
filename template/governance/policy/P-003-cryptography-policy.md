---
doc_id: P-003
doc_type: policy
title: Cryptography Policy
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
  - iso27002:A.8.24
signature_ref: null
---

# Cryptography Policy

**P-003 Revision 1 (DRAFT)**

*Status: draft. Owner: role:ISMS-Manager. Next review: 2027-01-01.*

## 1. Purpose

Use of cryptography: key management, algorithm selection, crypto-agility.

## 2. Scope

Applies to {{entity.short_name}} and to all information, systems, personnel, and third parties within the ISMS scope per `governance/context/scope-statement.md`.

## 3. Policy statements
### 3.1 Principle

Cryptography shall be used to protect the confidentiality, integrity, and authenticity
of information according to its classification and applicable legal requirements
(A.8.24).

### 3.2 Requirements

- Approved algorithms and key lengths shall meet current recognised standards, and only
  vetted implementations shall be used.
- Information classified confidential or higher shall be encrypted in transit and at rest.
- Cryptographic keys shall be managed across their full lifecycle (generation,
  distribution, storage, rotation, revocation, destruction) with access restricted to
  authorised roles.
- An algorithm inventory shall be maintained to support crypto-agility and timely
  migration away from weakened primitives.

### 3.3 Prohibitions

- Deprecated or unapproved algorithms shall not be used for new processing.
- Keys shall not be stored in plaintext alongside the data they protect, nor committed
  to the repository.

### 3.4 Responsibilities

- role:CISO approves the approved-algorithm standard; role:SysAdmin operates key
  management.

### 3.5 Exceptions

Exceptions shall be risk-accepted per the risk acceptance process (`governance/risk/methodology.md`, logged in `governance/risk/acceptance-log.md`) with a defined remediation date.

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
