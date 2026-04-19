---
doc_id: PLAN-002
doc_type: plan
title: Disaster recovery strategy
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
  - iso27002:A.5.29
  - iso27002:A.5.30
  - iso27002:A.8.13
  - iso27002:A.8.14
  - nisg2026:§31(2)(c)
signature_ref: null
---

# Disaster recovery strategy

**PLAN-002 Revision 1 (DRAFT)**

*Status: draft. Owner: role:CISO. Next review: 2027-01-01.*

## 1. Purpose

Defines {{entity.short_name}}'s strategy for recovering information processing from disruptive incidents, supporting continuity of critical services within RTO and RPO targets defined in `bia.yaml` and `rto-rpo.yaml`.

## 2. Strategy

TODO: architectural strategy (hot, warm, cold standby; active-passive; geo-redundancy). Align with `governance/soa/soa.yaml` entries for A.5.29, A.5.30, A.8.13, A.8.14.

## 3. Recovery paths

TODO: per-service recovery sequences, owner, dependencies, test cadence.

## 4. Test programme

Quarterly tabletop; annual full-restore of critical services.

## 5. Revision history

| Rev | Date | Status | Change |
|---|---|---|---|
| 1 | {{entity.draft_date}} | draft | initial draft |
