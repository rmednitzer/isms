# Changelog

> **Status**: draft
> **Last reviewed**: 2026-05-25

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
- `LICENSES/CC-BY-4.0.txt` (Creative Commons Attribution 4.0
  International) covering the Contributor Covenant 2.1 text in
  `CODE_OF_CONDUCT.md`.
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

- 2026-05-25: executed full repository validation sweep (`make validate test`) in a fresh `.venv`; all validators and 102 tooling tests passed without failures.
- `REUSE.toml` scope corrected: the Apache-2.0 default now applies only
  to framework paths (`template/`, `tooling/`, `docs/`, `framework-refs/`,
  `examples/`, root scaffolding, `.github/`, `LICENSES/`). `instance/**`
  is marked `LicenseRef-Confidential` via an explicit override block per
  `docs/document-control.md`. A CC-BY-4.0 override is added for
  `CODE_OF_CONDUCT.md` (Contributor Covenant 2.1 text).
- `.github/workflows/dco.yml` is now `workflow_dispatch` only pending a
  follow-up PR that replays the bootstrap commits with matching
  Signed-off-by emails; tracked as `LIMITATIONS.md` L8.
- `NOTICE` now includes an explicit maintainer contact line
  (`Roman Mednitzer <r.mednitzer@outlook.com>`).
- `STATUS.md` taxonomy extended with `n/a (canonical text)` for files
  that reproduce upstream canonical text (LICENSE, NOTICE,
  `LICENSES/*.txt`, `CODE_OF_CONDUCT.md`); ambiguous combined
  `planned/draft` cells split into a single status per row.
- `CODE_OF_CONDUCT.md` Enforcement section now points to the direct
  maintainer email (`r.mednitzer@outlook.com`) instead of referencing
  `SECURITY.md` / `NOTICE`.
- `GOVERNANCE.md` security commitment aligned with `SECURITY.md`
  (acknowledge and coordinate per 90-day disclosure window) instead of
  the prior fixed 7-day SLA; maintainer contact line now uses the
  direct email; CODEOWNERS-as-owner phrasing softened (the repository
  does not currently carry a `.github/CODEOWNERS` file).
- `LIMITATIONS.md` L8 (DCO workflow deferral) and L9 (REUSE scope
  correction; `instance/` is `LicenseRef-Confidential`) added.

### Notes

This addition imports governance discipline from the `platform-blueprint`
repository's May 2026 open-source-foundation audit cycle. It does not touch
content under `docs/`, `template/`, `instance/`, `framework-refs/`, or
`tooling/`. `NOTICE` was already present and is preserved (now extended
with the maintainer contact line).
