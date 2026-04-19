---
doc_id: DOC-002
doc_type: standard
title: Signature policy
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
  - iso27001:A.5.1
  - iso27001:A.5.15
  - iso27001:A.8.4
  - eidas:Art.25
  - eidas:Art.26
signature_ref: null
---

# Signature policy

**DOC-002 Revision 1 (DRAFT)**

*Status: draft. Owner: role:CISO. Next review: 2027-01-01.*

## 1. Two signature layers

### 1.1 Layer 1: Git integrity and authorship

- All commits to any branch are signed with GPG or SSH-sig.
- Keys registered in `.gitsigners`, bound to role and person in `instance/users/people/`.
- Branch protection on `main`: signed commits required, direct push disabled, pull request required, at least one CODEOWNER approval required, linear history preferred.
- Purpose: authenticity of change authorship, integrity of history, internal audit trail. This is not an eIDAS electronic signature.

### 1.2 Layer 2: eIDAS Qualified Electronic Signature (QES) on governance artefacts

- Provider: a Qualified Trust Service Provider (QTSP) listed on the EU Trusted List. For Austrian deployments, A-Trust is the primary domestic option; cross-border QTSPs (D-Trust, GlobalSign qualified, DigiCert QuoVadis) are equivalently valid under eIDAS.
- Format: PAdES (PDF Advanced Electronic Signatures, ETSI EN 319 142).
- Scope: policies, plans, Statement of Applicability, risk treatment plan, management review minutes, audit statements, Selbstdeklaration per NISG 2026 § 33.
- Mechanism: document rendered to PDF at approval; QES applied via QTSP service; signed PDF stored at `instance/evidence/signatures/<doc_id>-R<revision>-<YYYY-MM-DD>.pdf`; SHA-256 hash plus signer certificate fingerprint recorded in the source markdown's `signature_ref`.
- Verification: via EU DSS (Digital Signature Service by European Commission) or the QTSP's verification portal.

## 2. Scope matrix

| Artefact type | Git-sig | QES |
|---|---|---|
| Policies (P-NNN) | yes | yes |
| Plans (PLAN-NNN) | yes | yes |
| Statement of Applicability | yes | yes |
| Risk treatment plan | yes | yes |
| Management review minutes | yes | yes |
| External audit statements received | yes | verify QES on received artefact |
| Selbstdeklaration (NISG 2026 § 33) | yes | yes |
| Procedures (SOP-NNN) | yes | no (unless elevated) |
| Standards (STD-NNN) | yes | no |
| Incident records | yes | no |
| Change records (RFC) | yes | no |
| Evidence attestations | yes (manifest level) | no |
| Architectural decision records (DEC) | yes | no |

## 3. Signing roles

| Role | Git-sig | QES | Notes |
|---|---|---|---|
| Management (Leitungsorgan) | yes | yes | Ultimate accountability; signs P-000 and annual management review per ISO 27001 clause 5 and § 31 NISG 2026 |
| CISO | yes | yes | SoA, risk treatment plan, CISO-owned policies |
| ISMS Manager | yes | yes | Day-to-day policy and SOP approval |
| DPO | yes | yes | Privacy-specific artefacts, GDPR records |
| SysAdmin | yes | no | Technical SOPs, evidence commits, standards |
| Internal Auditor | yes | no | Findings, CAPA |
| External Auditor | no | verify only | Read-only access during audit; their report arrives QES-signed externally |

## 4. Signing ceremony

Per SOP-201. A "ceremony" is the scripted, witnessed, evidenced procedure by which a QES is applied. The term follows standard PKI practice (for instance, the DNSSEC Root Zone Key Signing Key ceremonies run by ICANN since 2010) and signals that QES application is not a routine commit.

Scripted steps:

1. Artefact frozen in repo at revision N, status=under_review.
2. Rendered to PDF by `tooling/packagers/build_<type>_pdf.py`.
3. Pre-signing SHA-256 hash of PDF recorded.
4. Signer authenticates to QTSP (A-Trust Signatur-Box or equivalent).
5. QES applied in PAdES format.
6. Signed PDF downloaded; post-signing hash verified.
7. Signed PDF committed to `instance/evidence/signatures/<doc_id>-R<N>-<YYYY-MM-DD>.pdf`.
8. Source markdown front-matter updated: status=approved, approved_date, approved_by, signature_ref.
9. PR merged with signed commit.

The ceremony record (pre-hash, post-hash, timestamp, QTSP transaction ID) is captured as an attestation alongside the signed PDF.

## 5. Interim posture

Until a QTSP contract is active and the signing pipeline tested, artefacts marked status=approved may set `interim_signature: true` in their front-matter. The visible header includes:

```
*Interim: legal signature pending QES integration. Approved via git-level only.*
```

Surveillance-audit window for closing interim: 90 days from first approval. After that, artefacts still in interim posture are an audit finding.

## 6. Revocation and re-signing

Git key compromise or role change:

- Git key: revoked in `.gitsigners`, replaced with new key. Historical commits are not re-signed.
- QES certificate: revocation per QTSP procedures. Affected artefacts re-signed by the successor role-holder within 30 days. Re-signed PDF committed alongside original (both retained). Front-matter updated to point to the new signature. A record of the revocation and re-sign event is committed to `instance/operations/audits/` as an incident.

## 7. External signatures received

External audit reports, QES-signed external correspondence, and QES-signed contracts received from suppliers are stored under `instance/evidence/received/` with verification records. Verification uses EU DSS or the QTSP's verification portal; results recorded.

## 8. Relationship to ISO 27001 and NISG 2026

- ISO 27001 clause 7.5.3 "control of documented information" requires approval for suitability and adequacy. QES evidences approval with non-repudiation. Git-level signing evidences authorship and integrity.
- ISO 27001 A.5.1 topic-specific policies require approval at appropriate level of management. QES by Management for P-000 establishes this clearly.
- NISG 2026 § 31 Leitungsorgan obligations: QES by Management on the top-level policy evidences the Leitungsorgan's approval and accountability.
- eIDAS Art. 25(2): a QES has the equivalent legal effect of a handwritten signature. Git-signed commits do not.

## 9. Revision history

| Rev | Date | Status | Change |
|---|---|---|---|
| 1 | 2026-04-19 | draft | initial draft |
