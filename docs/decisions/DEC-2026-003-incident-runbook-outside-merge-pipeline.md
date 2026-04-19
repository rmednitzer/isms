---
doc_id: DEC-2026-003
doc_type: record
title: "Incident runbook outside merge pipeline"
revision: 1
status: approved
approved_date: 2026-04-19
approved_by: role:CISO
owner: role:CISO
classification: internal
supersedes_revision: null
next_review: 2028-04-19
language: en
framework_refs:
  - iso27001:7.5.3
signature_ref: null
interim_signature: true
---

# Incident runbook outside merge pipeline

**DEC-2026-003 Revision 1 - 2026-04-19**

*Status: approved. Owner: role:CISO. Next review: 2028-04-19.*

*Interim: legal signature pending QES integration. Approved via git-level only.*

## Context

A 24-hour regulatory reporting clock cannot pass through PR review. The Frühwarnung begins when staff recognise a significant cybersecurity incident, not when a maintainer merges a commit. Making the report a PR dependency would systematically breach § 32 NISG 2026.

## Decision

CERT.at Frühwarnung (24 hours) and downstream notifications execute as direct operational actions, not pull requests. The incident record is created in the repo post-event.

## Alternatives considered

Alternative 1: PR-first incident recording. Rejected per above.
Alternative 2: bot-automated Frühwarnung submission. Rejected because CERT.at platform is designed for human judgement on significance classification and cross-border impact.

## Consequences

Pre-filled Frühwarnung template (TMPL-001) exists in the repo and is approved, QES-signed, and ready to copy into the CERT.at platform. Post-event the incident record captures what was submitted and when.

## Revision history

| Rev | Date | Status | Change |
|---|---|---|---|
| 1 | 2026-04-19 | approved | initial record |
