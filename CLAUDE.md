# CLAUDE.md

Operating instructions for Claude Code sessions against this repository.

## Mandate

Assist with ISMS operation: drafting, validation, evidence collection, and audit packaging. Do not make governance decisions. Every commit requires explicit human authorisation.

## Hard rules

1. No commits without signed commit configuration verified on the local machine. If `git config commit.gpgsign` or equivalent SSH signing is not set, stop and ask the human to configure it.
2. No changes to files under `instance/evidence/` that modify history. Evidence is append-only. New evidence goes in new dated files, not edits to existing ones.
3. No fabrication of approvals, signatures, or signed PDFs. If a file claims status=approved but no matching record exists in `instance/evidence/signatures/`, flag and stop.
4. No bypassing validator failures. If `make validate` fails, report and stop. Do not suppress errors to "fix" the symptom.
5. No modifications to `.gitsigners`, `.github/workflows/`, `.github/CODEOWNERS`, or `instance/users/roles.yaml` without explicit separate human authorisation per change. These are control-of-controls files.
6. Never draft or submit an incident report on behalf of the human. Incident response operates outside the merge pipeline. Prepare content for the human's review; the human submits.
7. Never commit secrets, API tokens, credentials, private keys, or real personal data of identified individuals. If encountered, stop, recommend redaction and rotation.

## Workflows you can drive

- Instantiating the template for a new deployment: read `instance/config.yaml`, run `python tooling/instantiate.py --config instance/config.yaml`, report placeholder resolution.
- Drafting a new policy or SOP: copy the front-matter template from `docs/document-control.md`, fill sections, mark status=draft, open a branch.
- Revising an existing artefact: bump `revision`, set `status=draft`, add `supersedes_revision` pointing to prior; old file moves to `status=superseded` only after new is approved.
- Running validators: `make validate`, report results, propose fixes for human review.
- Fetching law snapshots: `make snapshot-fetch` if network available; diff against existing snapshots; open a delta record if changes detected.
- Building audit packs: `make pack AUDIT=<stage>` once pre-conditions met.
- Generating control-coverage reports against `template/governance/controls/mapping.yaml` (as rendered into instance).

## Workflows that require explicit human confirmation

- Committing any file with `status=approved`.
- Committing any file under `instance/evidence/signatures/`.
- Changing `framework-refs/sources/registry.yaml`.
- Changing any schema under `tooling/schemas/`.
- Creating or closing an impact assessment under `framework-refs/impact-assessments/`.
- Any change to `.gitsigners`, `.github/CODEOWNERS`, `.github/workflows/`, or role definitions.

## Register

Governance artefacts (policies, SOPs, standards) are read by auditors, not colleagues. Register is formal and precise. Peer-engineering informality belongs in commit messages and internal notes, not in policy text.

## Language

- Internal artefacts: English.
- Authority-facing artefacts (Selbstdeklaration, CERT.at Frühwarnung, Bundesamt correspondence, registration records): German.
- Code and comments: English.
- Commit messages: English, imperative mood, short.

## Formatting

- No em dashes and no double dashes. Use comma, semicolon, period, parenthesis.
- YYYY-MM-DD dates, 24h times, SI units, EUR currency where user-facing.
- Markdown with YAML front-matter per `docs/document-control.md`.
- Code blocks for commands and configuration; fenced with language hint.

## Standalone constraint

Do not introduce runtime dependencies on external skill stacks, MCP servers, or cloud-hosted AI tooling. Fetching law snapshots from public APIs (RIS, EUR-Lex) is allowed. If a task seems to require an external dependency not already present, flag and propose a standalone alternative.

## When in doubt

Ask. One clarifying question is cheaper than an unauthorised commit.
