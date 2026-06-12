"""Security and correctness tests for tooling/capture.sh.

These assert that operator-supplied data (attachment filenames and reviewer
notes) is treated as data, not code (finding S-001), that path-traversal inputs
and out-of-enum capture methods are rejected, and that the collected-by identity
degrades to a well-formed default.

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


def _stdin(
    *,
    control_id: str = "A.8.13",
    source: str = "TestSystem v1",
    instance: str = "host-1.example",
    method: str = "manual_export",
    notes: str = MALICIOUS_NOTES,
) -> str:
    return "\n".join([control_id, source, instance, method, notes]) + "\n"


def _init_repo(workdir: Path, *, set_user: bool = True, isolate_global: bool = False) -> dict[str, str]:
    env = dict(os.environ)
    env["PATH"] = str(Path(sys.executable).parent) + os.pathsep + env.get("PATH", "")
    if isolate_global:
        env["GIT_CONFIG_GLOBAL"] = os.devnull
        env["GIT_CONFIG_SYSTEM"] = os.devnull
    subprocess.run(["git", "init", "-q"], cwd=workdir, check=True, env=env)
    if set_user:
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=workdir, check=True, env=env)
        subprocess.run(["git", "config", "user.email", "t@example.com"], cwd=workdir, check=True, env=env)
    return env


def _run(
    workdir: Path,
    et: str,
    *,
    env: dict[str, str],
    attachment: Path | None = None,
    stdin: str | None = None,
) -> subprocess.CompletedProcess[str]:
    args = ["bash", str(CAPTURE_SH), et]
    if attachment is not None:
        args.append(str(attachment))
    return subprocess.run(
        args, cwd=workdir, env=env, input=stdin if stdin is not None else _stdin(),
        capture_output=True, text=True, timeout=60,
    )


def _find_attestation(workdir: Path) -> Path:
    matches = list((workdir / "instance" / "evidence").rglob("*.yaml"))
    assert len(matches) == 1, f"expected one attestation, found {matches}"
    return matches[0]


@pytest.mark.skipif(not CAPTURE_SH.is_file(), reason="capture.sh not present")
def test_malicious_attachment_filename_does_not_execute(tmp_path: Path) -> None:
    env = _init_repo(tmp_path)
    attachment = tmp_path / MALICIOUS_FILENAME
    attachment.write_bytes(b"screenshot-bytes")

    result = _run(tmp_path, "ET-001", env=env, attachment=attachment)
    assert result.returncode == 0, result.stderr

    # No injected side effect, whether the payload would have run as Python or shell.
    for marker in ("PY_PWNED", "NOTES_PWNED", "BACKTICK_PWNED"):
        assert not (tmp_path / marker).exists(), f"injection marker {marker} was created"

    doc = YAML(typ="safe").load(_find_attestation(tmp_path).read_text(encoding="utf-8"))
    assert doc["captured_files"][0]["path"] == MALICIOUS_FILENAME
    assert len(doc["captured_files"][0]["sha256"]) == 64
    assert doc["reviewer_notes"] == MALICIOUS_NOTES


@pytest.mark.skipif(not CAPTURE_SH.is_file(), reason="capture.sh not present")
def test_attestation_matches_schema(tmp_path: Path) -> None:
    env = _init_repo(tmp_path)
    attachment = tmp_path / "ok.png"
    attachment.write_bytes(b"bytes")

    result = _run(tmp_path, "ET-002", env=env, attachment=attachment)
    assert result.returncode == 0, result.stderr

    doc = YAML(typ="safe").load(_find_attestation(tmp_path).read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(doc))
    assert errors == [], [e.message for e in errors]


@pytest.mark.skipif(not CAPTURE_SH.is_file(), reason="capture.sh not present")
def test_control_id_path_traversal_rejected(tmp_path: Path) -> None:
    env = _init_repo(tmp_path)
    result = _run(tmp_path, "ET-003", env=env, stdin=_stdin(control_id="../../etc/evil"))
    assert result.returncode == 2
    assert "invalid control id" in result.stderr


@pytest.mark.skipif(not CAPTURE_SH.is_file(), reason="capture.sh not present")
def test_evidence_task_id_traversal_rejected(tmp_path: Path) -> None:
    env = _init_repo(tmp_path)
    result = _run(tmp_path, "../../etc/evil", env=env)
    assert result.returncode == 2
    assert "invalid evidence task id" in result.stderr
    assert not (tmp_path / "instance" / "evidence").exists()


@pytest.mark.skipif(not CAPTURE_SH.is_file(), reason="capture.sh not present")
def test_invalid_capture_method_rejected(tmp_path: Path) -> None:
    env = _init_repo(tmp_path)
    result = _run(tmp_path, "ET-004", env=env, stdin=_stdin(method="rm_minus_rf"))
    assert result.returncode == 2
    assert "invalid capture method" in result.stderr


@pytest.mark.skipif(not CAPTURE_SH.is_file(), reason="capture.sh not present")
def test_collected_by_defaults_when_user_name_unset(tmp_path: Path) -> None:
    env = _init_repo(tmp_path, set_user=False, isolate_global=True)
    attachment = tmp_path / "ok.png"
    attachment.write_bytes(b"bytes")

    result = _run(tmp_path, "ET-005", env=env, attachment=attachment)
    assert result.returncode == 0, result.stderr

    doc = YAML(typ="safe").load(_find_attestation(tmp_path).read_text(encoding="utf-8"))
    assert doc["collected_by"] == "person:unknown"
