# 0006. Prune unused runtime dependencies

- Status: proposed
- Date: 2026-06-12
- Deciders: pending maintainer decision

## Context

Three of the seven declared runtime dependencies in `tooling/pyproject.toml` are
imported in zero source files: `lxml`, `cryptography`, and `python-dateutil`
(finding Q-005). Only `ruamel.yaml`, `jsonschema`, `jinja2`, and `requests` are
used. `lxml` and `cryptography` are large compiled packages with their own CVE
histories, so declaring them unnecessarily inflates the install and attack
surface.

## Decision (proposed)

Remove the three unused packages from runtime dependencies. If any is reserved for
planned work, keep it but move it behind an optional extra and add a comment
naming the intended use:

- `cryptography`: potentially QES or local signature verification (currently the
  signers shell out to `gpg`/`ssh-keygen`, and `verify_qes.py` is a stub).
- `lxml`: potentially EUR-Lex XML parsing (currently `fetch_eurlex.py` stores
  responses without XML parsing).
- `python-dateutil`: potentially date math (currently the code uses the standard
  library `datetime`).

## Consequences

- Smaller, faster installs and a smaller dependency attack surface.
- A maintainer decision is required because these may be deliberate placeholders;
  removing a reserved dependency would have to be reintroduced later.

## Status of evidence

Usage was determined by import grep across `tooling/`. The "reserved for" notes
are inference from stub modules, not documented intent.
