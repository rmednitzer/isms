# External-reader protocol

> **Status**: draft
> **Last reviewed**: 2026-05-14

The external-reader test is the gate before any document is promoted from
`draft` to `stable` per `STATUS.md`. It also gates major refactors of the
template-vs-instance boundary, the tooling contract, or the operating
contract.

## Purpose

The repository is authored by a maintainer and AI assistants operating
under `CLAUDE.md` and `docs/operating-contract.md`. Both are inside the
framing the repository expresses. An external reader can identify whether
the two-layer (template/instance) ISMS structure, the ISO 27001:2022 +
NISG 2026 framing, and the evidence layering (Git / eIDAS QES / continuous
collection) are comprehensible and trustworthy from cold read.

## When the test runs

- **Pre-promotion**: before any document moves from `draft` to `stable`.
- **Major refactor**: any change to the template-vs-instance boundary, the
  tooling contract (`tooling/instantiate.py` and `tooling/schemas/`), the
  signature policy, or the operating contract.
- **Recurring**: at minimum every 12 months.

## Who qualifies as external reader

The reader must be:

- not the maintainer;
- not currently part of the maintainer's day-to-day peer group;
- competent in at least one of: ISO/IEC 27001:2022 implementation and audit
  practice; NISG 2026 / NIS2 implementing-act practice in Austria; Austrian
  DSG / GDPR compliance practice; eIDAS / eIDAS 2 QES practice; or ISMS
  tooling and evidence-pipeline engineering;
- willing to read with sufficient time and attention.

Readers strong in ISO 27001 audit practice are particularly valuable.

The reader's identity and findings remain confidential to the maintainer
unless the reader consents to attribution.

## What the reader is asked

1. **Structure**. From `README.md` and `STATUS.md`, can you predict what is
   in the repository and where to find it? Is the two-layer split
   immediately legible?
2. **Audience**. Is the framework usable by an organisation pursuing ISO
   27001 certification under an Austrian jurisdiction, NISG 2026 compliance,
   or both?
3. **Template-vs-instance boundary**. Read `docs/document-control.md`. Is
   the boundary clear enough that a contributor would know which side any
   given file belongs on?
4. **Tooling contract**. Read `tooling/instantiate.py` documentation and
   the schemas. Could you instantiate a new deployment from `template/`
   plus a fresh `instance/config.yaml`?
5. **Evidence layering**. Read the description of the three evidence
   layers (Git integrity, eIDAS QES, continuous collection). Do they
   compose into a defensible evidence chain?
6. **Signature policy**. Read `docs/signature-policy.md`. Is the
   distinction between Git-signed commits and eIDAS QES tight enough that
   an auditor would not conflate them?
7. **Standalone operation**. The README claims `make validate` and
   `make pack` complete offline. Does the rest of the documentation
   support that claim, or does it presuppose external services?
8. **NISG 2026 alignment**. Read the references to § 33 Selbstdeklaration
   and CERT.at incident reporting. Are they current to the law text and
   the implementing-act state as of the snapshot date?
9. **Caveats**. Is the "Skeleton. Content population proceeds per
   certification timeline" framing honest? Does the repository undersell or
   oversell its current state?
10. **Trust**. Would you trust this repository as a framework for an
    Austrian-jurisdiction ISMS pursuing ISO 27001 certification? Why or
    why not?

The reader may raise concerns not covered by the questions.

## Pass criteria

The test passes when the reader's answers support:

- structure and the two-layer split are comprehensible from cold read;
- the tooling contract is usable;
- the evidence layering is defensible;
- caveats and the skeleton-state framing are honest;
- the reader's trust answer is positive or conditionally positive.

## Fail response

If the test fails, the maintainer:

1. Records the findings.
2. Categorises as structural / substantive / opinion.
3. Remediates structural findings before re-running.

## How findings are recorded

Responses are recorded under `docs/reviews/` or in the maintainer's evidence
repository.

## Maintainer's obligations to the reader

- compensate the reader's time appropriately;
- not press the reader to soften negative findings;
- not retaliate against honest negative findings;
- thank the reader in `CHANGELOG.md` with consent.

## Limitations

This protocol is a maintainer's discipline, not a substitute for:

- ISO 27001 certification by an accredited certification body (CIS, TÜV
  AUSTRIA, Quality Austria);
- NISG 2026 supervisory determination by the Bundesamt für Cybersicherheit;
- legal review by qualified counsel for reliance on the regulatory
  cross-references.
