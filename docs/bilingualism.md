---
doc_id: DOC-008
doc_type: standard
title: Bilingualism (DE and EN)
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
signature_ref: null
---

# Bilingualism (DE and EN)

**DOC-008 Revision 1 (DRAFT)**

*Status: draft. Owner: role:ISMS-Manager. Next review: 2027-01-01.*

## 1. Primary language rules

| Context | Language |
|---|---|
| Repository tooling, code, comments | English |
| Template governance artefacts | English (rendered content may be German per instance) |
| Instance governance artefacts | per `instance/config.yaml` (default English) |
| Authority-facing artefacts (Selbstdeklaration, CERT.at Frühwarnung, Bundesamt correspondence, registration records) | German |
| Commit messages, PR descriptions | English |
| Audit responses to external certification bodies | as required by the body (typically English in Austria; confirm per engagement) |

## 2. Parity requirement

When an artefact is declared bilingual (front-matter field `bilingual: true`, not default), both language versions live side by side as `<doc_id>.<lang>.md` and must be kept in parity. The validator `validate_bilingual.py` checks presence of both and flags divergence in section counts.

## 3. Authoritative language

For authority-facing artefacts, German is authoritative. The English version (if provided) is convenience only. Conflicts resolve in favour of the German text.

## 4. Citations

Legal citations use the original language: German for Austrian federal law (§, Abs., Z.), English for EU law (Art., para.). Translations of legal text are explicit paraphrases, not authoritative.

## 5. Revision history

| Rev | Date | Status | Change |
|---|---|---|---|
| 1 | 2026-04-19 | draft | initial draft |
