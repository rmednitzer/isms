# Governance

> **Status**: draft
> **Last reviewed**: 2026-05-14

This document records the governance of `isms` at the current
single-maintainer scale. It is honest about what the governance is and is
not, so external contributors can calibrate expectations.

## Maintainer authority

The repository has one maintainer, named in `NOTICE`. The maintainer holds
final authority on:

- merging pull requests into `main`;
- approval of changes to `CLAUDE.md`, `docs/operating-contract.md`, and
  `docs/document-control.md`;
- approval of changes to `tooling/instantiate.py`, schemas in
  `tooling/schemas/`, and validators in `tooling/validators/`;
- approval of changes to `framework-refs/sources/registry.yaml`,
  `framework-refs/calendar/`, and any framework template under
  `template/`;
- approval of branch-protection changes and CI workflow changes;
- coordination of the external-reader cadence per
  `EXTERNAL-READER-PROTOCOL.md`.

The maintainer does not have authority over content under `instance/`. That
content is operational and belongs to the deploying organisation. The
maintainer reviews instance-layer PRs only for: framework boundary
violations (instance content leaking into framework files); tooling
misuse; and PRs that mistakenly target the public repository when they
should target a private fork.

## Decision-making

At single-maintainer scale, decisions are recorded as artefacts:

- `CLAUDE.md` and `docs/operating-contract.md` for operating-contract
  decisions;
- `STATUS.md` for document maturity decisions;
- `CHANGELOG.md` for material change records;
- `LIMITATIONS.md` for declared limits;
- pull request descriptions and commit messages for change rationale;
- `docs/certification-timeline.md` for content-population sequence.

Decision records for instance-level decisions (e.g. DEC-2026-006 in the
README) live in the deploying organisation's instance, not in the public
repository.

## Contributor pathway

External contributors are welcome under the discipline encoded in
`CONTRIBUTING.md` and `CLAUDE.md`:

1. Read `CLAUDE.md`, `CONTRIBUTING.md`, and `docs/document-control.md` to
   understand the template-vs-instance boundary.
2. Open an issue for substantive content additions, especially when
   crossing the template/instance boundary.
3. Submit a PR with DCO sign-off. PRs that mix framework and instance
   content will be rejected.
4. Respond to maintainer review.

## Escalation

Disputes that cannot be resolved in issues escalate to email to the
maintainer at the address in `NOTICE`. There is no committee, no board,
no foundation.

## Code of conduct

The Contributor Covenant 2.1 governs project-space behaviour. See
`CODE_OF_CONDUCT.md`. The maintainer is the enforcement contact.

## Security policy

`SECURITY.md` governs security-relevant disclosure. The maintainer is the
recipient.

## Sustainability commitments

At the current scale the maintainer commits to:

- responding to security disclosures within 7 calendar days;
- recording material changes in `CHANGELOG.md`;
- preserving the operating contract's discipline.

The maintainer does not commit to:

- a fixed release cadence;
- an SLA on non-security issues;
- indefinite maintainership.

## License

Framework content (template/, tooling/, docs/, framework-refs/, examples/)
is licensed under the Apache License 2.0. Instance content under
`instance/` is confidential to the deploying organisation regardless of
the framework licence. By contributing you certify under the Developer
Certificate of Origin and license your contribution under the same
Apache-2.0 terms.

## Updating this document

Material changes to governance are recorded in `CHANGELOG.md`.
