# Contributing

## What this repository is

A template and tooling for running an ISMS under ISO 27001:2022 and NISG 2026. The template layer is reusable; the instance layer is per-deployment.

## Contribution scope

Contributions are welcome in the following areas:

- Tooling improvements (schemas, validators, collectors, packagers).
- Template refinements (policy structure, SOP clarity, standard updates).
- Framework references (law snapshots, crosswalks, regulatory calendar).
- Documentation and examples.

Instance-specific content (the actual policies and evidence of a deploying organisation) is never contributed upstream. It stays in the forked instance.

## Flow

1. Open an issue describing the change.
2. Fork, branch, implement.
3. Run `make validate` locally; it must pass.
4. Run `make test`; it must pass.
5. Open a PR against `main`. Signed commits required.
6. At least one CODEOWNER must approve.
7. PR merged with signed merge commit.

## Style

- English for code, comments, and template content.
- German for authority-facing templates where German is the authoritative language.
- No em dashes and no double dashes; use comma, semicolon, period, parenthesis.
- YYYY-MM-DD dates, 24h times.
- Apache-2.0 header on new tooling files.

## Governance-artefact contributions

Edits to files under `template/governance/` touch the framework consumed by downstream deployments. Propose changes as if they were a policy amendment: revision bump, rationale, migration notes for existing instances.

## Tooling contributions

New schemas, validators, or collectors: include tests under `tooling/tests/`, update `Makefile` if adding a target, document in the relevant `docs/` file.

## Reporting issues

Bugs, schema flaws, validator gaps, or framework-reference errors: GitHub issues. Security concerns: see `SECURITY.md`.
