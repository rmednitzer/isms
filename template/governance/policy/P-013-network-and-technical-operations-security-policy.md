---
doc_id: P-013
doc_type: policy
title: Network and Technical Operations Security Policy
revision: 1
status: draft
approved_date: null
approved_by: null
owner: role:CISO
classification: internal
supersedes_revision: null
next_review: 2027-01-01
language: en
framework_refs:
  - iso27002:A.5.7
  - iso27002:A.8.1
  - iso27002:A.8.6
  - iso27002:A.8.7
  - iso27002:A.8.9
  - iso27002:A.8.12
  - iso27002:A.8.19
  - iso27002:A.8.20
  - iso27002:A.8.21
  - iso27002:A.8.22
  - iso27002:A.8.23
signature_ref: null
---

# Network and Technical Operations Security Policy

**P-013 Revision 1 (DRAFT)**

*Status: draft. Owner: role:CISO. Next review: 2027-01-01.*

## 1. Purpose

Security of networks, user endpoint devices, and technical operations: threat
intelligence, malware protection, capacity, configuration management, data
leakage prevention, software installation, and network segregation and filtering.

## 2. Scope

Applies to {{entity.short_name}} and to all information, systems, personnel, and third parties within the ISMS scope per `governance/context/scope-statement.md`.

## 3. Policy statements
### 3.1 Principle

Networks, endpoints, and technical operations shall be secured, hardened, and
monitored to protect the confidentiality, integrity, and availability of
information across its processing environment.

### 3.2 Requirements

- Threat intelligence relevant to the organisation shall be collected, analysed, and
  fed into risk assessment and protective measures (A.5.7).
- Information on user endpoint devices shall be protected through configuration,
  hardening, and endpoint controls (A.8.1).
- Resource use shall be monitored and capacity projected to meet performance and
  availability requirements (A.8.6).
- Protection against malware shall be implemented and supported by user awareness (A.8.7).
- Secure configurations of hardware, software, services, and networks shall be
  established, documented, monitored, and reviewed (A.8.9).
- Data leakage prevention measures shall be applied to systems, networks, and devices
  handling sensitive information (A.8.12).
- Software installation on operational systems shall be managed through controlled
  procedures (A.8.19).
- Networks and network devices shall be secured, managed, and monitored, with network
  services security requirements defined (A.8.20, A.8.21).
- Groups of information services, users, and systems shall be segregated in networks,
  and access to external websites managed to reduce exposure to malicious content
  (A.8.22, A.8.23).

### 3.3 Prohibitions

- Unapproved software shall not be installed on operational systems (A.8.19).
- Endpoints and network devices shall not be connected to in-scope networks without the
  required security configuration (A.8.1, A.8.9).

### 3.4 Responsibilities

- role:CISO owns the network and technical-operations security requirements;
  role:SysAdmin implements and operates them.

### 3.5 Exceptions

Exceptions shall be risk-accepted per the risk acceptance process (`governance/risk/methodology.md`, logged in `governance/risk/acceptance-log.md`) with a remediation date.

## 4. Roles and responsibilities

Per `users/roles.yaml`. Key accountability: role:CISO.

## 5. Related documents

- Parent policy: `governance/policy/P-000-information-security-policy.md`
- Related policies: `governance/policy/P-002-access-control-policy.md`, `governance/policy/P-011-logging-and-monitoring-policy.md`, `governance/policy/P-007-secure-development-policy.md`
- Supporting procedures: SOP references to be added as they are drafted.
- Supporting standards: STD references to be added as they are drafted.

## 6. Compliance

Non-compliance is addressed per the applicable disciplinary procedure. Exceptions require risk acceptance per the risk acceptance process (`governance/risk/methodology.md`, logged in `governance/risk/acceptance-log.md`).

## 7. Revision history

| Rev | Date | Status | Change |
|---|---|---|---|
| 1 | {{entity.draft_date}} | draft | initial draft |
