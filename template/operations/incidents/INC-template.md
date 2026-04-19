---
doc_id: INC-2026-000
doc_type: record
title: Incident record template
revision: 1
status: draft
approved_date: null
approved_by: null
owner: role:CISO
classification: confidential
supersedes_revision: null
next_review: 2027-01-01
language: en
framework_refs:
  - iso27002:A.5.24
  - iso27002:A.5.26
  - nisg2026:§32
signature_ref: null
---

# Incident record template

**INC-2026-000 Revision 1 (DRAFT)**

*Status: draft template. Owner: role:CISO. Next review: 2027-01-01.*

## Usage

Copy to `instance/operations/incidents/active/INC-YYYY-NNN.md` at incident open; update status as lifecycle progresses; move to `closed/` on closure. For any significant cybersecurity incident, submit CERT.at Frühwarnung first (24h clock) using TMPL-001, then populate this record.

## Identification

- Incident ID: INC-YYYY-NNN
- Detected at: YYYY-MM-DDTHH:MM:SSZ
- Reported at: YYYY-MM-DDTHH:MM:SSZ
- Detected by: person or system
- Classification: cybersecurity_significant | cybersecurity_minor | privacy_breach | operational | minor | false_positive
- Severity: low | medium | high | critical
- Incident commander: role:ISMS-Manager or role:CISO
- Title: one-line description

## Description

What happened, scope of impact, affected assets, affected services, affected personal data (if any).

## Timeline

| Time (UTC) | Event | Actor |
|---|---|---|
| | detection | |
| | triage complete | |
| | containment | |
| | CERT.at Frühwarnung submitted | |
| | CERT.at 72h notification submitted | |
| | eradication | |
| | recovery | |
| | closure | |

## Regulatory reporting

### CERT.at Frühwarnung (24h)

- Required: yes | no
- Submitted at: YYYY-MM-DDTHH:MM:SSZ
- Reference: CERT.at ticket ID
- Content: attach copy of submission (TMPL-001-filled)

### CERT.at 72h notification

- Required: yes | no
- Submitted at:
- Reference:

### CERT.at final report (1 month)

- Required: yes | no
- Submitted at:
- Reference:

### GDPR Art. 33 notification to DSB (Datenschutzbehörde)

- Applicable: yes | no
- Rationale (if no): risk assessment per Art. 33(1)
- Submitted at:

### Other notifications

- Law enforcement: yes | no
- Customers: yes | no
- Contractual obligations: as applicable

## Root cause analysis

Brief summary, linked to fuller RCA in `instance/operations/incidents/closed/INC-YYYY-NNN/rca.md` if significant.

## Corrective and preventive actions

- CAPA-NNN: action, owner, due date, status

## Lessons learned

Link to lessons-learned record referenced in `lessons_learned_ref` field.

## Closure

- Closed at:
- Closed by: role:CISO
- Post-closure review: tabletop reference or management review reference
