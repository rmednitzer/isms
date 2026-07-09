---
doc_id: P-012
doc_type: policy
title: Privacy and Data Protection Policy
revision: 1
status: draft
approved_date: null
approved_by: null
owner: role:DPO
classification: internal
supersedes_revision: null
next_review: 2027-01-01
language: en
framework_refs:
  - iso27001:A.5.34
  - gdpr:Art.5
  - gdpr:Art.24
  - gdpr:Art.25
  - gdpr:Art.32
  - gdpr:Art.33
  - gdpr:Art.35
signature_ref: null
---

# Privacy and Data Protection Policy

**P-012 Revision 1 (DRAFT)**

*Status: draft. Owner: role:DPO. Next review: 2027-01-01.*

## 1. Purpose

Privacy obligations: lawful basis, data minimisation, DPIA, data subject rights, security of processing.

## 2. Scope

Applies to {{entity.short_name}} and to all information, systems, personnel, and third parties within the ISMS scope per `governance/context/scope-statement.md`.

## 3. Policy statements
### 3.1 Principle

Personal data shall be processed lawfully, fairly, and transparently, and protected by
appropriate technical and organisational measures, in accordance with the GDPR and the
Austrian DSG (GDPR Art. 5, Art. 24; A.5.34).

### 3.2 Requirements

- Processing activities shall have a documented lawful basis and shall be recorded in the
  Article 30 records of processing (`governance/data/inventory.yaml`).
- Data protection by design and by default shall be applied to new processing and systems
  (GDPR Art. 25).
- Data minimisation, purpose limitation, accuracy, and storage limitation shall be
  observed (GDPR Art. 5).
- A data protection impact assessment shall be performed where processing is likely to
  result in high risk (GDPR Art. 35).
- Security of processing shall be ensured through measures proportionate to risk
  (GDPR Art. 32), and data subject rights shall be supported.
- Personal data breaches shall be handled through P-005 and notified to the
  Datenschutzbehörde within 72 hours where required (GDPR Art. 33).

### 3.3 Prohibitions

- Personal data shall not be processed without a lawful basis or beyond the stated purpose.
- Personal data shall not be transferred to a third country without an adequate transfer
  mechanism.

### 3.4 Responsibilities

- role:DPO oversees data protection compliance; process owners maintain records of
  processing; role:CISO ensures security of processing.

### 3.5 Exceptions

There are no exceptions to statutory data-protection obligations. Processing-specific risk
decisions shall be recorded via a DPIA and risk acceptance per the risk acceptance process (`governance/risk/methodology.md`, logged in `governance/risk/acceptance-log.md`).

## 4. Roles and responsibilities

Per `users/roles.yaml`. Key accountability: role:DPO.

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
