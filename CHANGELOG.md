# Changelog

> **Status**: draft
> **Last reviewed**: 2026-05-14

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This repository is documentation and tooling rather than a versioned product;
material changes are dated. Instance-level changes are recorded in the
deploying organisation's instance, not here.

## [Unreleased]

### Added

- `CODE_OF_CONDUCT.md` (Contributor Covenant 2.1).
- `REUSE.toml` and `LICENSES/Apache-2.0.txt` for REUSE 3.3 compliance at
  the aggregate level. Per-file SPDX retrofit deferred (see
  `LIMITATIONS.md` L6). Note: only framework content is in scope;
  `instance/` is confidential.
- `STATUS.md` recording document maturity per template / tooling /
  framework-refs / docs section, with the instance layer explicitly
  declared out of scope for public maturity declarations.
- `LIMITATIONS.md` recording the known limits (L1 skeleton state,
  L2 template-vs-instance boundary not CI-enforced, L3 eIDAS QES depends
  on external QTSP, L4 NISG 2026 transposition state, L5 drift-watch
  partial, L6 REUSE per-file retrofit, L7 multi-jurisdiction extension
  is structural only).
- `GOVERNANCE.md` recording single-maintainer governance, the
  template-vs-instance authority split, and the contributor pathway.
- `EXTERNAL-READER-PROTOCOL.md` defining the qualified-human-reader gate,
  with questions adapted to ISO 27001 / NISG 2026 / Austrian DSG / eIDAS
  competence.
- `.github/workflows/scorecard.yml` for OpenSSF Scorecard.
- `.github/workflows/dco.yml` enforcing DCO sign-off.
- `.github/workflows/reuse.yml` verifying REUSE 3.3 compliance.

### Changed

- None in this entry beyond additions.

### Notes

This addition imports governance discipline from the `platform-blueprint`
repository's May 2026 open-source-foundation audit cycle. It does not touch
content under `docs/`, `template/`, `instance/`, `framework-refs/`, or
`tooling/`. `NOTICE` was already present and is preserved.
