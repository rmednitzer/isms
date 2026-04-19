---
doc_id: STD-005
doc_type: standard
title: Data Classification Standard
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
  - iso27002:A.5.12
  - iso27002:A.5.13
  - iso27002:A.5.14
  - iso27002:A.8.10
  - iso27002:A.8.11
  - iso27002:A.8.12
  - gdpr:Art.5
  - gdpr:Art.32
signature_ref: null
---

# Data Classification Standard

**STD-005 Revision 1 (DRAFT)**

*Status: draft. Owner: role:ISMS-Manager. Next review: 2028-04-19.*

## 1. Purpose

Defines the classification scheme used across {{entity.short_name}} for
information and data (as distinct from artefact classification under DOC-001,
which governs classification of governance documents themselves). Every
asset entry, data inventory entry, and supplier entry carries a
classification value drawn from this standard.

## 2. Scope

Applies to all data processed, transmitted, or stored within the ISMS scope
per `governance/context/scope-statement.md`. Applies to all assets in the
asset register and all processing activities in the data inventory.

## 3. Levels

Four levels. Classification is determined by the impact of unauthorised
disclosure, modification, or loss of availability.

### 3.1 public

Data intended or approved for unrestricted public disclosure. No
confidentiality impact on disclosure.

Examples: published marketing material, public financial statements,
published job postings.

### 3.2 internal

Default level for organisational data not approved for external disclosure.
Minor adverse impact if disclosed. Not sensitive in a legal or regulatory
sense.

Examples: internal memos, organisational charts, non-confidential meeting
minutes, internal process documentation.

### 3.3 confidential

Data whose disclosure would cause material damage: commercial harm,
contractual breach, loss of competitive position, or breach of a specific
confidentiality obligation. Includes personal data under GDPR in the
ordinary course.

Examples: customer personal data (contact, billing, usage), commercial
contracts, pricing strategy, source code, internal risk assessments.

### 3.4 restricted

Data whose disclosure would cause severe damage: regulatory breach,
substantial financial harm, substantial harm to data subjects, or
operational risk to critical services. Includes Article 9 special category
personal data, authentication secrets, cryptographic keys, classified
material under applicable regimes.

Examples: GDPR Article 9 special categories, authentication credentials,
private keys, pre-publication financial results, incident-response
investigation content, security control configuration where disclosure
enables bypass.

## 4. Handling rules

Rules are cumulative: a higher level inherits the rules of lower levels and
adds requirements.

### 4.1 Storage at rest

| Level        | Storage requirements                                        |
|--------------|-------------------------------------------------------------|
| public       | No specific requirements                                    |
| internal     | Storage on approved systems                                 |
| confidential | Encrypted at rest; access restricted to authorised roles    |
| restricted   | Encrypted at rest with HSM-managed keys; access logged      |

### 4.2 Transport

| Level        | Transport requirements                                      |
|--------------|-------------------------------------------------------------|
| public       | No specific requirements                                    |
| internal     | Internal networks or encrypted external transport           |
| confidential | TLS 1.2 or higher for all external transit                  |
| restricted   | TLS 1.3 or higher; mTLS where party-to-party; VPN for admin |

### 4.3 Access control

| Level        | Access control                                              |
|--------------|-------------------------------------------------------------|
| public       | No restrictions                                             |
| internal     | Authenticated access only                                   |
| confidential | Role-based access; MFA for remote access                    |
| restricted   | Named-individual access; MFA required; access logged and reviewed monthly |

### 4.4 Media handling

| Level        | Media handling                                              |
|--------------|-------------------------------------------------------------|
| public       | No specific requirements                                    |
| internal     | Label on removable media                                    |
| confidential | Label; secure transport; encrypted media                    |
| restricted   | Label; witnessed transport or eIDAS-QES-signed chain of custody; encrypted media; secure destruction at end of life per A.7.14 |

### 4.5 Retention and disposal

Retention periods are set per processing activity in the data inventory
(DATA-NNN entries). Disposal follows A.8.10. For restricted, disposal
produces an attestation under the evidence plan.

### 4.6 Third-party disclosure

| Level        | Disclosure to third parties                                 |
|--------------|-------------------------------------------------------------|
| public       | Permitted                                                   |
| internal     | Only with explicit business justification                   |
| confidential | Under signed confidentiality agreement; entry in supplier register if ongoing |
| restricted   | Under signed confidentiality agreement AND DPA (where personal data); CISO approval per instance |

## 5. Labelling

Physical media carrying confidential or restricted data carries a visible
label with the classification level. Digital labelling convention for file
and object stores is declared per system and enumerated in the asset
register `notes` field when relevant.

## 6. Relationship to other classifications

This standard classifies **data**. It is distinct from:

- **Artefact classification** under DOC-001, which applies to governance
  documents (this standard is itself classified `internal` as a governance
  document).
- **Zone classification** under the facilities register
  (`zone_class` in `tooling/schemas/facilities-register.schema.json`), which
  applies to physical spaces.
- **Trust-level classification** under the network register
  (`trust_level` in `tooling/schemas/network-register.schema.json`), which
  applies to network segments.

These three classification axes compose: an asset has a data
classification, sits in a zone of a given class, and is attached to a
network of a given trust level. Controls are derived from the combination.

## 7. Review

Reviewed annually by role:ISMS-Manager. Material change triggers a revision
bump; editorial changes do not.

## 8. Revision history

| Rev | Date       | Status | Change        |
|-----|------------|--------|---------------|
| 1   | {{entity.draft_date}} | draft  | initial draft |
