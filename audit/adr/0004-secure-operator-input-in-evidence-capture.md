# 0004. Secure operator input in evidence capture

- Status: accepted (implemented in this audit pass)
- Date: 2026-06-12
- Deciders: audit pass (2026-06-12)

## Context

`tooling/capture.sh` staged a human-captured evidence attestation by writing an
unquoted shell heredoc and by building a `python3 -c` program through string
interpolation of attachment filenames. Reviewer notes containing `$(...)` or
backticks, or an attachment filename containing a single quote, could execute
code as the operator (finding S-001). Evidence filenames and pasted notes are
routinely attacker-influenced data in incident handling.

## Decision

Treat all operator-supplied values as data. Pass them to a Python helper through
the environment and argv, never by interpolation into shell or Python source.
Quote the heredoc delimiter so the Python body is literal. Validate the control id
against `[A-Za-z0-9._-]+` before using it in a filesystem path.

## Consequences

- Filenames and notes can no longer trigger shell or Python execution.
- Output still conforms to `tooling/schemas/attestation.schema.json`.
- `tooling/capture.sh` requires a Python with `ruamel.yaml` available (an
  activated `.venv`), which was already the case for the prior inline `python3`.
- A regression test (`tooling/tests/test_capture_sh.py`) asserts that a malicious
  filename and malicious notes create no side effects and that a traversal control
  id is rejected.

## Evidence

- `tooling/capture.sh` (post-change), `tooling/tests/test_capture_sh.py` (3 tests,
  passing).
