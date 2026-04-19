# Security policy

## Reporting

Security concerns about this repository template (tooling bugs, schema flaws, validator bypass) should be reported by opening a private security advisory via GitHub's Security tab, or by contacting the maintainer listed in `.github/CODEOWNERS`.

## Scope

This policy covers the template and tooling in this repository. Instance-specific security (the actual ISMS of the deploying organisation) is out of scope here and lives under `instance/` with its own `P-005-incident-management.md` and `SOP-001-incident-response.md`.

## Secrets

No secrets belong in this repository at any time. Credentials, API tokens, private keys, and authentication material live outside the repository, referenced by `instance/config.yaml` via environment variable names or secret-manager paths. The `detect-private-key` pre-commit hook is a backstop, not a substitute for discipline.

## Signed commits

All commits to `main` must be signed per `docs/signature-policy.md`. Unsigned commits are rejected by branch protection. Commits by unregistered keys are rejected by `tooling/validators/validate_signatures.py`.

## Dependency updates

Tooling dependencies are pinned in `tooling/pyproject.toml`. Dependabot or equivalent should be enabled on each deployment to track security updates. Dependency updates follow the standard RFC + review flow per `docs/contribution-flow.md`.

## Responsible disclosure

Please allow 90 days for vulnerabilities to be fixed before public disclosure, or coordinate a shorter timeline with the maintainer if active exploitation is observed.
