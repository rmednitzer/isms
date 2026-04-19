"""Tests for the template renderer (instantiate.py)."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "tooling"))

from instantiate import (  # noqa: E402
    RenderError,
    load_config,
    render_ifs,
    render_placeholders,
    resolve_dotted,
    should_copy,
)


class TestResolveDotted:
    def test_simple_key(self) -> None:
        assert resolve_dotted({"a": 1}, "a") == 1

    def test_nested_key(self) -> None:
        assert resolve_dotted({"a": {"b": {"c": 42}}}, "a.b.c") == 42

    def test_missing_key(self) -> None:
        assert resolve_dotted({"a": 1}, "b") is None

    def test_missing_nested(self) -> None:
        assert resolve_dotted({"a": {"b": 1}}, "a.c") is None

    def test_non_dict_intermediate(self) -> None:
        assert resolve_dotted({"a": "string"}, "a.b") is None

    def test_empty_dict(self) -> None:
        assert resolve_dotted({}, "a") is None


class TestRenderIfs:
    def test_true_branch(self) -> None:
        cfg = {"flag": True}
        assert render_ifs("{{#if flag}}YES{{else}}NO{{/if}}", cfg) == "YES"

    def test_false_branch(self) -> None:
        cfg = {"flag": False}
        assert render_ifs("{{#if flag}}YES{{else}}NO{{/if}}", cfg) == "NO"

    def test_missing_key_is_falsy(self) -> None:
        assert render_ifs("{{#if missing}}YES{{else}}NO{{/if}}", {}) == "NO"

    def test_no_else(self) -> None:
        cfg = {"flag": True}
        assert render_ifs("{{#if flag}}YES{{/if}}", cfg) == "YES"

    def test_no_else_false(self) -> None:
        cfg = {"flag": False}
        assert render_ifs("{{#if flag}}YES{{/if}}", cfg) == ""

    def test_nested_dotted_key(self) -> None:
        cfg = {"a": {"b": True}}
        assert render_ifs("{{#if a.b}}ON{{else}}OFF{{/if}}", cfg) == "ON"

    def test_surrounding_text_preserved(self) -> None:
        cfg = {"x": True}
        result = render_ifs("before {{#if x}}mid{{/if}} after", cfg)
        assert result == "before mid after"


class TestRenderPlaceholders:
    def test_simple(self) -> None:
        cfg = {"name": "Acme"}
        out, missing = render_placeholders("Hello {{name}}.", cfg, Path("test"))
        assert out == "Hello Acme."
        assert missing == []

    def test_nested(self) -> None:
        cfg = {"entity": {"short_name": "Acme"}}
        out, missing = render_placeholders("{{entity.short_name}}", cfg, Path("t"))
        assert out == "Acme"
        assert missing == []

    def test_missing_reported(self) -> None:
        out, missing = render_placeholders("{{missing.key}}", {}, Path("t"))
        assert "{{missing.key}}" in out
        assert "missing.key" in missing

    def test_multiple_placeholders(self) -> None:
        cfg = {"a": "1", "b": "2"}
        out, missing = render_placeholders("{{a}} and {{b}}", cfg, Path("t"))
        assert out == "1 and 2"
        assert missing == []


class TestShouldCopy:
    def test_gitkeep_skipped(self) -> None:
        assert should_copy(Path(".gitkeep")) is False

    def test_normal_file(self) -> None:
        assert should_copy(Path("policy.md")) is True

    def test_pycache_skipped(self) -> None:
        assert should_copy(Path("tooling/__pycache__/foo.pyc")) is False


class TestLoadConfig:
    def test_missing_config_raises(self, tmp_path: Path) -> None:
        with pytest.raises(RenderError, match="config file not found"):
            load_config(tmp_path / "nonexistent.yaml")

    def test_valid_config_loads(self) -> None:
        cfg = load_config(REPO_ROOT / "instance" / "config.yaml")
        assert cfg["schema_version"] == 1
        assert "entity" in cfg
