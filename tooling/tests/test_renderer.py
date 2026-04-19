"""Renderer smoke test: placeholder substitution works."""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "tooling"))

from instantiate import render_ifs, render_placeholders  # noqa: E402


def test_placeholder_substitution() -> None:
    cfg = {"entity": {"short_name": "Acme"}}
    text = "Hello {{entity.short_name}}."
    out, missing = render_placeholders(text, cfg, Path("test"))
    assert "Hello Acme." in out
    assert missing == []


def test_missing_placeholder_reported() -> None:
    cfg = {}
    text = "Hello {{entity.short_name}}."
    out, missing = render_placeholders(text, cfg, Path("test"))
    assert "{{entity.short_name}}" in out
    assert missing == ["entity.short_name"]


def test_if_block_true() -> None:
    cfg = {"feature_flags": {"use_qes": True}}
    text = "{{#if feature_flags.use_qes}}ON{{else}}OFF{{/if}}"
    assert render_ifs(text, cfg) == "ON"


def test_if_block_false() -> None:
    cfg = {"feature_flags": {"use_qes": False}}
    text = "{{#if feature_flags.use_qes}}ON{{else}}OFF{{/if}}"
    assert render_ifs(text, cfg) == "OFF"
