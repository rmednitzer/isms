"""Tests for the PR B substance-gating validators and checks."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "tooling" / "validators"))


def _load(name: str):
    path = REPO_ROOT / "tooling" / "validators" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


# --- validate_soa ---

def _soa_tree(tmp_path: Path, soa_yaml: str) -> tuple[Path, Path]:
    gov = tmp_path / "governance"
    (gov / "soa").mkdir(parents=True)
    (gov / "controls" / "implementation").mkdir(parents=True)
    (gov / "controls" / "implementation" / "A.5.1.md").write_text("impl", encoding="utf-8")
    soa = gov / "soa" / "soa.yaml"
    soa.write_text(soa_yaml, encoding="utf-8")
    annex = tmp_path / "annex.yaml"
    annex.write_text("controls:\n  - id: A.5.1\n    title: t\n    theme: organisational\n", encoding="utf-8")
    return soa, annex


def _run_soa(monkeypatch, soa, annex, repo_root):
    vs = _load("validate_soa")
    monkeypatch.setattr(vs, "SOA_INSTANCE", soa)
    monkeypatch.setattr(vs, "SOA_TEMPLATE", soa)
    monkeypatch.setattr(vs, "ANNEX", annex)
    monkeypatch.setattr(vs, "REPO_ROOT", repo_root)
    return vs.main()


def test_soa_valid_not_assessed(monkeypatch, tmp_path) -> None:
    soa, annex = _soa_tree(
        tmp_path,
        "controls:\n  - id: A.5.1\n    applicable: yes\n    status: not_assessed\n"
        "    implementation_ref: controls/implementation/A.5.1.md\n",
    )
    assert _run_soa(monkeypatch, soa, annex, tmp_path) == 0


def test_soa_assessed_without_justification_fails(monkeypatch, tmp_path) -> None:
    soa, annex = _soa_tree(
        tmp_path,
        "controls:\n  - id: A.5.1\n    applicable: yes\n    status: implemented\n"
        "    implementation_ref: controls/implementation/A.5.1.md\n",
    )
    assert _run_soa(monkeypatch, soa, annex, tmp_path) == 1


def test_soa_excluded_without_exclusion_ref_fails(monkeypatch, tmp_path) -> None:
    soa, annex = _soa_tree(tmp_path, "controls:\n  - id: A.5.1\n    applicable: no\n")
    assert _run_soa(monkeypatch, soa, annex, tmp_path) == 1


def test_soa_missing_control_fails(monkeypatch, tmp_path) -> None:
    soa, annex = _soa_tree(tmp_path, "controls: []\n")
    assert _run_soa(monkeypatch, soa, annex, tmp_path) == 1


def test_soa_bad_impl_ref_fails(monkeypatch, tmp_path) -> None:
    soa, annex = _soa_tree(
        tmp_path,
        "controls:\n  - id: A.5.1\n    applicable: yes\n    status: not_assessed\n"
        "    implementation_ref: controls/implementation/DOES-NOT-EXIST.md\n",
    )
    assert _run_soa(monkeypatch, soa, annex, tmp_path) == 1


# --- validate_no_todo ---

def test_no_todo_clean(monkeypatch, tmp_path) -> None:
    vt = _load("validate_no_todo")
    (tmp_path / "gov").mkdir()
    (tmp_path / "gov" / "clean.md").write_text("real content\n", encoding="utf-8")
    monkeypatch.setattr(vt, "SCAN_ROOTS", (tmp_path / "gov",))
    assert vt.main() == 0


def test_no_todo_catches_sentinel(monkeypatch, tmp_path) -> None:
    vt = _load("validate_no_todo")
    (tmp_path / "gov").mkdir()
    (tmp_path / "gov" / "bad.md").write_text("name: TODO: Example GmbH\n", encoding="utf-8")
    monkeypatch.setattr(vt, "SCAN_ROOTS", (tmp_path / "gov",))
    assert vt.main() == 1


def test_no_todo_catches_placeholder(monkeypatch, tmp_path) -> None:
    vt = _load("validate_no_todo")
    (tmp_path / "gov").mkdir()
    (tmp_path / "gov" / "bad.md").write_text("scope: {{entity.legal_name}}\n", encoding="utf-8")
    monkeypatch.setattr(vt, "SCAN_ROOTS", (tmp_path / "gov",))
    assert vt.main() == 1


# --- crossrefs iso27001 catalogue ---

def test_iso27001_annex_a_validated() -> None:
    vc = _load("validate_crossrefs")
    cat = vc.build_catalogue()
    assert vc._check_framework_ref(Path("x"), "iso27001:A.9.99", cat) is not None
    assert vc._check_framework_ref(Path("x"), "iso27001:A.5.1", cat) is None
    assert vc._check_framework_ref(Path("x"), "iso27001:6.1.2", cat) is None


# --- signatures: PAdES structure + interim window ---

def test_signature_ref_rejects_unsigned_pdf(monkeypatch, tmp_path) -> None:
    vs = _load("validate_signatures")
    sigdir = tmp_path / "sigs"
    sigdir.mkdir()
    monkeypatch.setattr(vs, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(vs, "SIGNATURES_DIR", sigdir.resolve())
    fake = sigdir / "fake.pdf"
    fake.write_bytes(b"%PDF-1.4\nnot really signed\n")
    problem = vs.check_signature_ref("sigs/fake.pdf")
    assert problem is not None and "no embedded PAdES" in problem


def test_signature_ref_accepts_signed_shape(monkeypatch, tmp_path) -> None:
    vs = _load("validate_signatures")
    sigdir = tmp_path / "sigs"
    sigdir.mkdir()
    monkeypatch.setattr(vs, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(vs, "SIGNATURES_DIR", sigdir.resolve())
    signed = sigdir / "ok.pdf"
    signed.write_bytes(b"%PDF-1.4\n/ByteRange [0 1 2 3]\n/SubFilter/ETSI.CAdES.detached\n")
    assert vs.check_signature_ref("sigs/ok.pdf") is None


def test_interim_window_lapsed_fails() -> None:
    vs = _load("validate_signatures")
    assert vs.check_interim_window({"approved_date": "2020-01-01"}) is not None


def test_interim_window_recent_ok() -> None:
    vs = _load("validate_signatures")
    from datetime import date, timedelta

    recent = (date.today() - timedelta(days=5)).isoformat()
    assert vs.check_interim_window({"approved_date": recent}) is None


def test_interim_window_needs_date() -> None:
    vs = _load("validate_signatures")
    assert vs.check_interim_window({}) is not None


# --- instantiate TODO sentinel ---

def test_instantiate_treats_todo_as_unresolved() -> None:
    sys.path.insert(0, str(REPO_ROOT / "tooling"))
    import instantiate

    cfg = {"entity": {"legal_name": "TODO: Example GmbH", "short_name": "Acme"}}
    _, unresolved = instantiate.render_placeholders(
        "{{entity.legal_name}} / {{entity.short_name}}", cfg, Path("x.md")
    )
    assert any("legal_name" in u for u in unresolved)
    assert not any("short_name" in u for u in unresolved)
