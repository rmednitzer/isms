"""Security tests for tooling/capture.sh.

These assert that operator-supplied data (attachment filenames and reviewer
notes) is treated as data, not code. The pre-hardening script interpolated
filenames into a Python ``-c`` program and field values into an unquoted shell
heredoc, both of which allowed code execution (finding S-001).

The script invokes a bare ``python3`` and imports ruamel.yaml, so the test puts
the test interpreter's directory first on PATH (mimicking an activated venv).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker
from ruamel.yaml import YAML

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CAPTURE_SH = REPO_ROOT / "tooling" / "capture.sh"
SCHEMA_PATH = REPO_ROOT / "tooling" / "schemas" / "attestation.schema.json"

# Single quotes break a Python string literal; ``$(...)`` is a shell command
# substitution. A safe implementation must execute neither.
MALICIOUS_FILENAME = "x'+__import__('os').system('touch PY_PWNED')+'y.png"
MALICIOUS_NOTES = "benign note $(touch NOTES_PWNED) `touch BACKTICK_PWNED` end"


def _run_capture(workdir: Path, et: str, attachment: Path | None) -> subprocess.CompletedProcess[str]:
    subprocess.run(["git", "init", "-q"], cwd=workdir, check=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=workdir, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=workdir, check=True)

    env = dict(os.environ)
    env["PATH"] = str(Path(sys.executable).parent) + os.pathsep + env.get("PATH", "")

    stdin = "\n".join(["A.8.13", "TestSystem v1", "host-1.example", "manual_export", MALICIOUS_NOTES]) + "\n"
    args = ["bash", str(CAPTURE_SH), et]
    if attachment is not None:
        args.append(str(attachment))
    return subprocess.run(args, cwd=workdir, env=env, input=stdin, capture_output=True, text=True, timeout=60)


def _find_attestation(workdir: Path) -> Path:
    matches = list((workdir / "instance" / "evidence").rglob("*.yaml"))
    assert len(matches) == 1, f"expected one attestation, found {matches}"
    return matches[0]


@pytest.mark.skipif(not CAPTURE_SH.is_file(), reason="capture.sh not present")
def test_malicious_attachment_filename_does_not_execute(tmp_path: Path) -> None:
    attachment = tmp_path / MALICIOUS_FILENAME
    attachment.write_bytes(b"screenshot-bytes")

    result = _run_capture(tmp_path, "ET-001", attachment)
    assert result.returncode == 0, result.stderr

    # No injected side effect, whether the payload would have run as Python or shell.
    for marker in ("PY_PWNED", "NOTES_PWNED", "BACKTICK_PWNED"):
        assert not (tmp_path / marker).exists(), f"injection marker {marker} was created"

    att = _find_attestation(tmp_path)
    doc = YAML(typ="safe").load(att.read_text(encoding="utf-8"))
    assert doc["captured_files"][0]["path"] == MALICIOUS_FILENAME
    assert len(doc["captured_files"][0]["sha256"]) == 64
    assert doc["reviewer_notes"] == MALICIOUS_NOTES


@pytest.mark.skipif(not CAPTURE_SH.is_file(), reason="capture.sh not present")
def test_attestation_matches_schema(tmp_path: Path) -> None:
    attachment = tmp_path / "ok.png"
    attachment.write_bytes(b"bytes")

    result = _run_capture(tmp_path, "ET-002", attachment)
    assert result.returncode == 0, result.stderr

    att = _find_attestation(tmp_path)
    doc = YAML(typ="safe").load(att.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(doc))
    assert errors == [], [e.message for e in errors]


@pytest.mark.skipif(not CAPTURE_SH.is_file(), reason="capture.sh not present")
def test_control_id_path_traversal_rejected(tmp_path: Path) -> None:
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=tmp_path, check=True)

    env = dict(os.environ)
    env["PATH"] = str(Path(sys.executable).parent) + os.pathsep + env.get("PATH", "")
    stdin = "\n".join(["../../etc/evil", "sys", "host", "manual_export", "note"]) + "\n"

    result = subprocess.run(
        ["bash", str(CAPTURE_SH), "ET-003"],
        cwd=tmp_path, env=env, input=stdin, capture_output=True, text=True, timeout=60,
    )
    assert result.returncode == 2
    assert "invalid control id" in result.stderr
