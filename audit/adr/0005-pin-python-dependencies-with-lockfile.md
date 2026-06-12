# 0005. Pin Python dependencies with a lockfile

- Status: proposed
- Date: 2026-06-12
- Deciders: pending maintainer decision

## Context

`tooling/pyproject.toml` declares lower-bound-only dependencies and the repository
has no lockfile or constraints file. Installs resolve to whatever PyPI currently
serves (this audit observed pip 26, mypy 2.1, cryptography 48). `make bootstrap`
also upgrades pip unpinned. `docs/standalone-charter.md` and DEC-2026-001 make
"an auditor's clone plus `make bootstrap` reproduces all evidence" a contract;
floating versions weaken that contract (finding Q-004).

## Decision (proposed)

Add a pinned lockfile or constraints file (for example via `pip-compile` or
`uv lock`), consume it from `make bootstrap` and CI, and let Renovate maintain it
(the existing `renovate.json5` already enables lockfile maintenance, but there is
no lockfile for it to maintain).

## Consequences

- Reproducible installs across clones and over time, aligning with the standalone
  charter.
- A maintenance burden: the lockfile must be refreshed and reviewed.
- CI must install from the lockfile to gain the benefit.

## Alternatives

- Pin exact versions directly in `pyproject.toml`: simpler but couples runtime and
  dev pins and loses hash pinning.
- Status quo (floating): least effort, weakest reproducibility.
