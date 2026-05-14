# Document status

> **Status**: draft
> **Last reviewed**: 2026-05-14

Maturity taxonomy per `CLAUDE.md`:

- **planned**: structure exists, content not authored
- **draft**: content exists, not validated against external-reader gate
- **stable**: passed external-reader gate, within review cadence
- **n/a (canonical text)**: file reproduces verbatim upstream text
  (e.g. an OSI-approved licence text, the Contributor Covenant) where
  the project-side maturity taxonomy does not apply; correctness is
  governed by faithful reproduction of the canonical source, not by
  draft/stable progression.

The repository README declares the overall state as `Skeleton. Content
population proceeds per docs/certification-timeline.md`. The maturity
taxonomy below applies to authored content; planned structures without
content are at `planned`.

## Two-layer split

This repository is split between the reusable framework (`template/`,
`tooling/`, `docs/`, `framework-refs/`) and one concrete deployment
(`instance/`). Maturity applies to the framework layer. Instance-layer
content is confidential to the deploying organisation regardless of
framework licence.

## Template layer

| Section | Path | Status | Last reviewed |
|---|---|---|---|
| Governance templates (structure) | `template/governance/` | planned | 2026-05-14 |
| Operations templates (structure) | `template/operations/` | planned | 2026-05-14 |

## Framework references

| Section | Path | Status | Last reviewed |
|---|---|---|---|
| Source registry | `framework-refs/sources/registry.yaml` | draft | 2026-05-14 |
| Law snapshots | `framework-refs/snapshots/` | draft | 2026-05-14 |
| Regulatory calendar | `framework-refs/calendar/` | draft | 2026-05-14 |

## Tooling

| Section | Path | Status | Last reviewed |
|---|---|---|---|
| Schemas | `tooling/schemas/` | draft | 2026-05-14 |
| Validators | `tooling/validators/` | draft | 2026-05-14 |
| Collectors | `tooling/collectors/` | draft | 2026-05-14 |
| Signers | `tooling/signers/` | draft | 2026-05-14 |
| Packager (audit pack) | `tooling/packager/` | draft | 2026-05-14 |
| Instantiator | `tooling/instantiate.py` | draft | 2026-05-14 |
| Renderer | `tooling/renderer/` | draft | 2026-05-14 |

## Operating documentation

| Section | Path | Status | Last reviewed |
|---|---|---|---|
| Operating contract | `docs/operating-contract.md` | draft | 2026-05-14 |
| Document control | `docs/document-control.md` | draft | 2026-05-14 |
| Signature policy | `docs/signature-policy.md` | draft | 2026-05-14 |
| Certification timeline | `docs/certification-timeline.md` | draft | 2026-05-14 |

## Examples

| Section | Path | Status | Last reviewed |
|---|---|---|---|
| Worked example instance (structure) | `examples/instance-acme/` | planned | 2026-05-14 |

## Instance layer (confidential)

The `instance/` directory holds one concrete deployment. Maturity of
instance content is not declared in this public STATUS.md because the
content is operational and confidential to the deploying organisation.
`docs/document-control.md` governs the instance-vs-framework boundary.

## Repository scaffolding

Files marked `n/a (canonical text)` reproduce upstream canonical text
(an OSI-approved licence text or the Contributor Covenant). The
correctness criterion for those files is faithful reproduction of the
canonical source, not project-side draft/stable maturity.

| Document | Status | Last reviewed |
|---|---|---|
| `README.md` | draft | 2026-05-14 |
| `CLAUDE.md` | stable | 2026-05-14 |
| `CONTRIBUTING.md` | draft | 2026-05-14 |
| `SECURITY.md` | draft | 2026-05-14 |
| `CODE_OF_CONDUCT.md` | n/a (canonical text) | 2026-05-14 |
| `GOVERNANCE.md` | draft | 2026-05-14 |
| `LIMITATIONS.md` | draft | 2026-05-14 |
| `EXTERNAL-READER-PROTOCOL.md` | draft | 2026-05-14 |
| `STATUS.md` | draft | 2026-05-14 |
| `CHANGELOG.md` | draft | 2026-05-14 |
| `NOTICE` | n/a (canonical text) | 2026-05-14 |
| `LICENSE` | n/a (canonical text) | 2026-05-14 |
| `REUSE.toml` | draft | 2026-05-14 |
| `LICENSES/Apache-2.0.txt` | n/a (canonical text) | 2026-05-14 |
| `LICENSES/CC-BY-4.0.txt` | n/a (canonical text) | 2026-05-14 |
| `.github/workflows/ci.yml` | draft | 2026-05-14 |
| `.github/workflows/scorecard.yml` | draft | 2026-05-14 |
| `.github/workflows/dco.yml` | draft | 2026-05-14 |
| `.github/workflows/reuse.yml` | draft | 2026-05-14 |
| `.github/pull_request_template.md` | draft | 2026-05-14 |
| `.github/ISSUE_TEMPLATE/*` | draft | 2026-05-14 |
| `.github/dependabot.yml` | draft | 2026-05-14 |

## Updating this document

When a document is touched, update its `Last reviewed` cell here and the
top-of-file `> **Last reviewed**:` blockquote in the document itself, and
record material changes in `CHANGELOG.md`.
