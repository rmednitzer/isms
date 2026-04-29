# ISMS

Information Security Management System repository.

## Frameworks in scope

- ISO/IEC 27001:2022 (primary certification target)
- NISG 2026 (Austria, BGBl. I Nr. 94/2025; entry into force 2026-10-01)
- Implementing Regulation (EU) 2024/2690 (NIS2 technical measures)
- GDPR Art. 32 (technical and organisational measures)
- Extensible to ISO/IEC 27701:2025 (privacy information management)

## Jurisdiction

Austria primary. Multi-jurisdiction sources tracked in `framework-refs/sources/registry.yaml`. Instance-specific jurisdiction declared in `instance/config.yaml`.

## Languages

- English: primary language for internal artefacts.
- German: authority-facing artefacts (Selbstdeklaration per NISG 2026 § 33, CERT.at Frühwarnung, registration correspondence).

## Standalone operation

This repository runs without dependencies on external skill stacks, MCP servers, or platform-specific tooling. `make validate` and `make pack` complete offline against committed files. Network access is required only for `make snapshot-fetch` (law updates from RIS and EUR-Lex).

## Structure

Two-layer design. The template layer is the reusable framework; the instance layer holds one concrete deployment.

```
isms/
├── docs/             operating rules for the repository itself
├── template/         reusable framework (governance, operations templates)
├── instance/         one concrete deployment, driven by instance/config.yaml
├── framework-refs/   authoritative source law snapshots, registry, regulatory calendar
└── tooling/          schemas, validators, collectors, signers, packagers, renderer
```

A second deployment (client engagement, sister entity) uses the same `template/` and `tooling/` with a fresh `instance/`.

## Three evidence layers

1. Git integrity: signed commits, branch protection, CODEOWNERS enforcement.
2. eIDAS Qualified Electronic Signature (QES): PAdES-signed PDFs for policies, Statement of Applicability, management review minutes, audit statements, Selbstdeklaration. PDFs and hashes committed under `instance/evidence/signatures/`.
3. Continuous evidence collection: three collector modes (API-pull, agent-push, human-captured) writing to `instance/evidence/`.

Git-signed commits attest integrity and authorship within the ISMS. They are not eIDAS electronic signatures. Legal signatures for governance artefacts use qualified electronic signatures per `docs/signature-policy.md`.

## Audit and supervisory interfaces

- ISO/IEC 27001 certification: accredited body (CIS, TÜV AUSTRIA, Quality Austria).
- NISG 2026 supervisory authority: Bundesamt für Cybersicherheit.
- NIS2 incident reporting: https://nis2.cert.at (24h Frühwarnung, 72h notification, 1 month final report).
- Cyber Trust Austria Platinum evaluated as § 33 evidence vehicle; decision per DEC-2026-006.

## Entry points

| I want to... | Start at |
|---|---|
| understand how this repo operates | `docs/operating-contract.md` |
| see what a populated deployment looks like | `examples/instance-acme/` |
| deploy this template for an organisation | `instance/config.yaml` and `tooling/instantiate.py` |
| write a new policy or SOP | `docs/document-control.md`, then copy from `template/governance/` |
| track a new law | `framework-refs/sources/registry.yaml` and SOP-101 |
| log an incident | `instance/operations/incidents/` AND the pre-filled Frühwarnung template |
| prepare for audit | `make pack AUDIT=<stage>` |
| submit NISG 2026 Selbstdeklaration | `make selbstdeklaration` |

## Quickstart

```bash
make bootstrap                # install tooling into .venv
# Edit instance/config.yaml for your organisation
python tooling/instantiate.py --config instance/config.yaml
make validate                 # run all offline validators
make currency-check           # check snapshot ages and reference coverage
make snapshot-fetch           # refresh law snapshots (requires network)
make pack AUDIT=stage-1
```

## License

Apache License 2.0. See LICENSE.

Governance content classification per `docs/document-control.md`. Instance-specific content (actual policies, SoA, risk register, evidence) is confidential to the deploying organisation regardless of the Apache licence on the framework tooling.

## Status

Skeleton. Content population proceeds per `docs/certification-timeline.md`.
