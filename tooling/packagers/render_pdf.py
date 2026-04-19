#!/usr/bin/env python3
"""
Render a governance markdown document to a PDF suitable for QES signing.

Input contract: a markdown file with YAML front-matter conforming to
`tooling/schemas/frontmatter.schema.json` (see DOC-001). Output: a
print-ready PDF whose cover page and running headers reflect the document
control specification (DOC-001) and the editorial style guide (DOC-009).

Pipeline:
  markdown + front-matter
      -> parsed front-matter (ruamel.yaml)
      -> body HTML (markdown -> HTML)
      -> Jinja2 template render (templates/pdf/document.html.j2 + styles.css)
      -> WeasyPrint PDF render

Design notes:
  - Front-matter is the source of truth for cover/header/footer metadata.
    The visible header block inside the markdown body is kept as-is; it is
    the internal-preview form. The PDF cover supersedes it for external
    presentation.
  - WeasyPrint is an optional runtime dependency (install with
    `pip install -e tooling/[pdf]`). When it is not importable, this tool
    falls back to writing HTML next to the requested output and returns a
    non-zero exit code so CI catches the gap. The HTML is renderable by any
    browser and is byte-reproducible (no timestamps inside the HTML body
    beyond the explicit `--generated-at` value).
  - No network access. No external services. Standalone per DEC-2026-001.

Copyright 2026 isms contributors
SPDX-License-Identifier: Apache-2.0
"""
from __future__ import annotations

import argparse
import io
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from jinja2 import ChainableUndefined, Environment, FileSystemLoader, select_autoescape
from ruamel.yaml import YAML

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TEMPLATE_DIR = Path(__file__).resolve().parent / "templates" / "pdf"
DIST_DIR = REPO_ROOT / "dist"

DOC_TYPES_REQUIRING_QES = {"policy", "plan"}

_FRONT_MATTER_RE = re.compile(r"\A---\n(.*?)\n---\n(.*)\Z", re.DOTALL)

_yaml = YAML(typ="safe")


class RenderError(Exception):
    """Raised for any unrecoverable rendering error."""


@dataclass
class ParsedDoc:
    front_matter: dict
    body_md: str
    source_path: Path


def parse_document(path: Path) -> ParsedDoc:
    if not path.is_file():
        raise RenderError(f"source file not found: {path}")
    raw = path.read_text(encoding="utf-8")
    m = _FRONT_MATTER_RE.match(raw)
    if not m:
        raise RenderError(f"no YAML front-matter found in {path}")
    fm = _yaml.load(m.group(1)) or {}
    if not isinstance(fm, dict):
        raise RenderError(f"front-matter is not a mapping in {path}")
    return ParsedDoc(front_matter=fm, body_md=m.group(2), source_path=path)


def markdown_to_html(md_text: str) -> str:
    """Convert markdown body to HTML.

    Prefers the `markdown` library (optional dep); falls back to a minimal
    converter that handles the subset used by the ISMS templates: ATX
    headings, paragraphs, unordered and ordered lists, GFM tables, fenced
    code blocks, inline code, bold, italic, and links.
    """
    try:
        import markdown  # type: ignore

        return markdown.markdown(
            md_text,
            extensions=["tables", "fenced_code", "sane_lists", "toc"],
            output_format="html5",
        )
    except ImportError:
        return _minimal_markdown(md_text)


def _escape_html(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def _inline(s: str) -> str:
    # Inline code first so bold/italic do not eat its backticks.
    s = re.sub(r"`([^`]+)`", lambda m: f"<code>{_escape_html(m.group(1))}</code>", s)
    # Links: [text](url)
    s = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda m: f'<a href="{_escape_html(m.group(2))}">{_escape_html(m.group(1))}</a>',
        s,
    )
    # Bold then italic.
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    return s


def _minimal_markdown(md_text: str) -> str:
    """Very small markdown -> HTML converter for fallback use only.

    Handles ATX headings, paragraphs, unordered/ordered lists, fenced code
    blocks (``` ... ```), and pipe tables with a header separator row.
    """
    lines = md_text.splitlines()
    out: list[str] = []
    i = 0
    in_code = False
    code_buf: list[str] = []

    def flush_paragraph(buf: list[str]) -> None:
        if not buf:
            return
        text = " ".join(buf).strip()
        if text:
            out.append(f"<p>{_inline(_escape_html(text))}</p>")
        buf.clear()

    para: list[str] = []

    while i < len(lines):
        line = lines[i]

        if line.startswith("```"):
            flush_paragraph(para)
            if not in_code:
                in_code = True
                code_buf = []
            else:
                out.append("<pre><code>" + _escape_html("\n".join(code_buf)) + "</code></pre>")
                in_code = False
            i += 1
            continue
        if in_code:
            code_buf.append(line)
            i += 1
            continue

        heading = re.match(r"^(#{1,6})\s+(.*)$", line)
        if heading:
            flush_paragraph(para)
            level = len(heading.group(1))
            out.append(f"<h{level}>{_inline(_escape_html(heading.group(2).strip()))}</h{level}>")
            i += 1
            continue

        if re.match(r"^\s*[-*]\s+", line):
            flush_paragraph(para)
            out.append("<ul>")
            while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
                item = re.sub(r"^\s*[-*]\s+", "", lines[i])
                out.append(f"<li>{_inline(_escape_html(item))}</li>")
                i += 1
            out.append("</ul>")
            continue

        if re.match(r"^\s*\d+\.\s+", line):
            flush_paragraph(para)
            out.append("<ol>")
            while i < len(lines) and re.match(r"^\s*\d+\.\s+", lines[i]):
                item = re.sub(r"^\s*\d+\.\s+", "", lines[i])
                out.append(f"<li>{_inline(_escape_html(item))}</li>")
                i += 1
            out.append("</ol>")
            continue

        if line.strip().startswith("|") and i + 1 < len(lines) and re.match(
            r"^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)+\|?\s*$", lines[i + 1]
        ):
            flush_paragraph(para)
            header_cells = [c.strip() for c in line.strip().strip("|").split("|")]
            i += 2
            out.append("<table><thead><tr>")
            for c in header_cells:
                out.append(f"<th>{_inline(_escape_html(c))}</th>")
            out.append("</tr></thead><tbody>")
            while i < len(lines) and lines[i].strip().startswith("|"):
                row_cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                out.append("<tr>")
                for c in row_cells:
                    out.append(f"<td>{_inline(_escape_html(c))}</td>")
                out.append("</tr>")
                i += 1
            out.append("</tbody></table>")
            continue

        if line.strip() == "":
            flush_paragraph(para)
            i += 1
            continue

        para.append(line.strip())
        i += 1

    flush_paragraph(para)
    return "\n".join(out)


_FRONTMATTER_DEFAULTS: dict = {
    "doc_id": "",
    "doc_type": "record",
    "title": "",
    "revision": 1,
    "status": "draft",
    "approved_date": None,
    "approved_by": None,
    "owner": "",
    "classification": "internal",
    "supersedes_revision": None,
    "next_review": "",
    "language": "en",
    "framework_refs": [],
    "signature_ref": None,
    "interim_signature": False,
    "bilingual": False,
}


def normalize_frontmatter(fm: dict) -> dict:
    """Fill absent optional fields so the template can reference them directly."""
    out = dict(_FRONTMATTER_DEFAULTS)
    out.update({k: v for k, v in fm.items() if v is not None or k in out})
    for k, v in _FRONTMATTER_DEFAULTS.items():
        if out.get(k) is None and not isinstance(v, (list, dict)):
            out[k] = v
    return out


def build_environment() -> Environment:
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        autoescape=select_autoescape(enabled_extensions=("html", "j2")),
        undefined=ChainableUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    return env


def render_html(
    doc: ParsedDoc,
    *,
    entity_legal_name: str | None,
    emit_signature_block: bool | None,
    generated_at: datetime,
) -> str:
    fm = normalize_frontmatter(doc.front_matter)
    doc_type = fm.get("doc_type", "record")
    if emit_signature_block is None:
        emit_signature_block = doc_type in DOC_TYPES_REQUIRING_QES

    stylesheet = (TEMPLATE_DIR / "styles.css").read_text(encoding="utf-8")
    env = build_environment()
    tpl = env.get_template("document.html.j2")

    try:
        source_rel = doc.source_path.resolve().relative_to(REPO_ROOT)
    except ValueError:
        source_rel = doc.source_path

    body_html = markdown_to_html(doc.body_md)

    return tpl.render(
        fm=fm,
        body_html=body_html,
        stylesheet=stylesheet,
        entity_legal_name=entity_legal_name,
        emit_signature_block=emit_signature_block,
        source_rel_path=str(source_rel),
        generated_utc=generated_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
        generated_date=generated_at.strftime("%Y-%m-%d"),
    )


def render_pdf(html: str, out_path: Path) -> None:
    try:
        from weasyprint import HTML  # type: ignore
    except ImportError as exc:
        raise RenderError(
            "WeasyPrint is not installed. Install the PDF extras with "
            "`pip install -e tooling/[pdf]` (or use --html-only to emit HTML)."
        ) from exc
    HTML(string=html, base_url=str(REPO_ROOT)).write_pdf(str(out_path))


def load_entity_legal_name(config_path: Path | None) -> str | None:
    if config_path is None or not config_path.is_file():
        return None
    with config_path.open("r", encoding="utf-8") as f:
        cfg = _yaml.load(f) or {}
    entity = cfg.get("entity") if isinstance(cfg, dict) else None
    if isinstance(entity, dict):
        return entity.get("legal_name")
    return None


def default_output_path(doc: ParsedDoc, *, suffix: str) -> Path:
    fm = doc.front_matter
    doc_id = fm.get("doc_id", doc.source_path.stem)
    rev = fm.get("revision", 1)
    date_part = fm.get("approved_date") or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return DIST_DIR / f"{doc_id}-R{rev}-{date_part}{suffix}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Render an ISMS markdown document to a PDF (or HTML).",
    )
    parser.add_argument("source", type=Path, help="path to a markdown file with front-matter")
    parser.add_argument(
        "--out", type=Path, default=None,
        help="output path; defaults to dist/<doc_id>-R<rev>-<date>.pdf (or .html)",
    )
    parser.add_argument(
        "--html-only", action="store_true",
        help="emit HTML instead of PDF; does not require WeasyPrint",
    )
    parser.add_argument(
        "--signature-block", choices=("auto", "on", "off"), default="auto",
        help="include trailing signature page (auto: on for policies and plans)",
    )
    parser.add_argument(
        "--config", type=Path, default=REPO_ROOT / "instance" / "config.yaml",
        help="path to instance/config.yaml for entity name; optional",
    )
    parser.add_argument(
        "--generated-at", type=str, default=None,
        help="ISO-8601 UTC timestamp to stamp as generation time (for reproducible builds)",
    )
    args = parser.parse_args(argv)

    try:
        doc = parse_document(args.source)
    except RenderError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    if args.generated_at:
        try:
            generated_at = datetime.fromisoformat(args.generated_at.replace("Z", "+00:00"))
        except ValueError:
            print(f"ERROR: invalid --generated-at value: {args.generated_at}", file=sys.stderr)
            return 2
        if generated_at.tzinfo is None:
            generated_at = generated_at.replace(tzinfo=timezone.utc)
    else:
        generated_at = datetime.now(timezone.utc)

    sig_map = {"auto": None, "on": True, "off": False}
    emit_sig = sig_map[args.signature_block]

    entity_legal_name = load_entity_legal_name(args.config)

    html = render_html(
        doc,
        entity_legal_name=entity_legal_name,
        emit_signature_block=emit_sig,
        generated_at=generated_at,
    )

    out_path = args.out or default_output_path(
        doc, suffix=".html" if args.html_only else ".pdf"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if args.html_only:
        out_path.write_text(html, encoding="utf-8")
        print(f"HTML written: {out_path}")
        return 0

    try:
        render_pdf(html, out_path)
    except RenderError as e:
        fallback = out_path.with_suffix(".html")
        fallback.write_text(html, encoding="utf-8")
        print(f"ERROR: {e}", file=sys.stderr)
        print(f"HTML fallback written: {fallback}", file=sys.stderr)
        return 3

    print(f"PDF written: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
