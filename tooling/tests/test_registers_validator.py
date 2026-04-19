"""Tests for the register validator (schema + cross-register resolution)."""
from __future__ import annotations

import json
import sys
import textwrap
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "tooling" / "validators"))


class TestRegisterSchemas:
    def test_all_register_schemas_load(self) -> None:
        from validate_registers import REGISTERS

        for name, spec in REGISTERS.items():
            assert spec["schema"].is_file(), f"schema missing for {name}"
            with spec["schema"].open() as f:
                json.load(f)

    def test_template_registers_are_schema_valid(self) -> None:
        from validate_registers import REGISTERS, validate_schema

        for name, spec in REGISTERS.items():
            errors = validate_schema(name, spec)
            assert errors == [], f"{name}: {errors}"


class TestCrossRegisterResolution:
    def test_template_crossrefs_resolve(self) -> None:
        from validate_registers import (
            REGISTERS,
            load_ids,
            validate_crossrefs,
        )

        all_ids = {name: load_ids(spec) for name, spec in REGISTERS.items()}
        errors = validate_crossrefs(all_ids)
        assert errors == [], f"unresolved refs in template: {errors}"


class TestInvalidData:
    def test_dangling_asset_location_ref_detected(self, tmp_path, monkeypatch) -> None:
        """Write a fake asset register with an unresolvable location_ref and
        confirm the cross-ref pass flags it."""
        import validate_registers as vr

        bad_register = tmp_path / "bad-register.yaml"
        bad_register.write_text(
            textwrap.dedent("""\
                schema_version: 1
                assets:
                  - id: ASSET-0001
                    name: "dangling"
                    class: information
                    owner_role: role:CISO
                    location_ref: FAC-999
                    in_scope: true
                    lifecycle_status: operational
            """)
        )
        monkeypatch.setitem(vr.REGISTERS["assets"], "instance", bad_register)
        monkeypatch.setitem(vr.REGISTERS["assets"], "template", bad_register)

        all_ids = {name: vr.load_ids(spec) for name, spec in vr.REGISTERS.items()}
        errors = vr.validate_crossrefs(all_ids)
        assert any("FAC-999" in e and "location_ref" in e for e in errors), (
            f"expected dangling FAC-999 location_ref to be flagged, got: {errors}"
        )

    def test_missing_register_file_is_flagged(self, tmp_path, monkeypatch) -> None:
        """A register whose template AND instance files are absent must be a
        schema violation, not a silent pass."""
        import validate_registers as vr

        missing = tmp_path / "does-not-exist.yaml"
        monkeypatch.setitem(vr.REGISTERS["assets"], "instance", missing)
        monkeypatch.setitem(vr.REGISTERS["assets"], "template", missing)

        errors = vr.validate_schema("assets", vr.REGISTERS["assets"])
        assert errors, "missing register file should produce a schema error"
        assert any("not found" in e for e in errors), errors


class TestCrossrefExtension:
    def test_register_ref_fields_declared(self) -> None:
        from validate_crossrefs import REGISTER_REF_FIELDS

        expected = {
            "asset_refs",
            "location_ref",
            "zone_ref",
            "network_ref",
            "supplier_refs",
            "data_refs",
        }
        assert set(REGISTER_REF_FIELDS.keys()) == expected

    def test_extract_register_refs_array(self, tmp_path: Path) -> None:
        from validate_crossrefs import extract_register_refs

        md = tmp_path / "test.md"
        md.write_text(
            textwrap.dedent("""\
                ---
                asset_refs:
                  - ASSET-0001
                  - ASSET-0002
                location_ref: FAC-001
                ---
                Body.
            """)
        )
        refs = extract_register_refs(md)
        assert refs["asset_refs"] == ["ASSET-0001", "ASSET-0002"]
        assert refs["location_ref"] == ["FAC-001"]
