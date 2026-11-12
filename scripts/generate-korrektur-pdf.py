#!/usr/bin/env python3
"""Erzeugt learnbox-korrekturlesen.pdf aus allen öffentlichen Website-Inhalten."""
from __future__ import annotations

import re
import subprocess
import sys
import time
from datetime import date
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = Path(__file__).resolve().parents[1]
OUT_HTML = ROOT / "docs" / "korrekturlesen.html"
OUT_PDF = ROOT / "docs" / "learnbox-korrekturlesen.pdf"
ARTIFACT = Path("/opt/cursor/artifacts/learnbox-korrekturlesen.pdf")

# Reihenfolge für Korrekturlesen (wie auf learnbox.ch)
PAGES: list[tuple[str, Path, str]] = [
    ("Startseite", ROOT / "index.html", "/"),
    ("Leistungen", ROOT / "leistungen.html", "/leistungen.html"),
    ("Über uns", ROOT / "ueber.html", "/ueber.html"),
    ("LearnBlog (Übersicht)", ROOT / "blog.html", "/blog.html"),
    (
        "Micro-Learning mit KI",
        ROOT / "blog/micro-learning-mit-ki.html",
        "/blog/micro-learning-mit-ki.html",
    ),
    (
        "KI im eLearning",
        ROOT / "blog/ki-im-elearning-personalisierte-haeppchen.html",
        "/blog/ki-im-elearning-personalisierte-haeppchen.html",
    ),
    (
        "Fünf Minuten am Arbeitsplatz",
        ROOT / "blog/fuenf-minuten-am-arbeitsplatz.html",
        "/blog/fuenf-minuten-am-arbeitsplatz.html",
    ),
    (
        "Schwarm-Intelligenz Vernetzung",
        ROOT / "blog/schwarm-intelligenz-dank-vernetzung.html",
        "/blog/schwarm-intelligenz-dank-vernetzung.html",
    ),
    (
        "Digitalisierung LMS",
        ROOT / "blog/digitalisierung-nicht-verschlafen.html",
        "/blog/digitalisierung-nicht-verschlafen.html",
    ),
    (
        "Internes Wissen",
        ROOT / "blog/internes-wissen-gezielt-foerdern.html",
        "/blog/internes-wissen-gezielt-foerdern.html",
    ),
    (
        "Schwarm-Intelligenz fördern",
        ROOT / "blog/schwarm-intelligenz-foerdern.html",
        "/blog/schwarm-intelligenz-foerdern.html",
    ),
    (
        "Revolution Weiterbildung",
        ROOT / "blog/revolution-in-der-weiterbildung.html",
        "/blog/revolution-in-der-weiterbildung.html",
    ),
    ("Kontakt", ROOT / "kontakt.html", "/kontakt.html"),
    ("Impressum", ROOT / "impressum.html", "/impressum.html"),
    ("Datenschutz", ROOT / "datenschutz.html", "/datenschutz.html"),
]

SKIP_TAGS = {"header", "footer", "script", "style", "nav", "button", "form"}
IMG_NOTE_RE = re.compile(r"Platzhalter|platzhalter")


def strip_chrome(soup: BeautifulSoup) -> Tag | None:
    main = soup.find("main")
    if not main:
        return soup.body
    return main


def inline_text(el: Tag) -> str:
    parts: list[str] = []
    for child in el.descendants:
        if isinstance(child, NavigableString):
            t = str(child).strip()
            if t:
                parts.append(t)
    return " ".join(parts)


def form_to_text(form: Tag, doc: BeautifulSoup) -> Tag:
    """Kontaktformular als lesbare Feldliste für Korrektur."""
    block = doc.new_tag("div")
    block["class"] = "form-proof"
    heading = doc.new_tag("p")
    heading["class"] = "eyebrow"
    heading.string = "Formular (nur Texte zur Korrektur)"
    block.append(heading)
    ul = doc.new_tag("ul")
    for label in form.find_all("label"):
        if label.find("select") or label.find_parent(class_="hp"):
            continue
        label_text = label.get_text(" ", strip=True)
        if not label_text or label_text.lower() == "website":
            continue
        li = doc.new_tag("li")
        li.string = label_text
        ul.append(li)
    for opt in form.find_all("option"):
        val = opt.get("value", "")
        text = opt.get_text(strip=True)
        li = doc.new_tag("li")
        li.string = f"Auswahl «Thema»: {text} (value: {val})"
        ul.append(li)
    btn = form.find("button", type="submit")
    if btn:
        li = doc.new_tag("li")
        li.string = f"Schaltfläche: {btn.get_text(strip=True)}"
        ul.append(li)
    block.append(ul)
    for p in form.find_all("p", class_="muted"):
        block.append(p.extract())
    return block


def simplify_main(main: Tag) -> str:
    """HTML-Fragment ohne Navigation, mit Bild-Hinweisen statt Binärinhalten."""
    clone = BeautifulSoup(str(main), "lxml").find("main") or main
    for form in clone.find_all("form"):
        form.replace_with(form_to_text(form, clone))
    for tag in clone.find_all(list(SKIP_TAGS - {"form"})):
        tag.decompose()
    for img in clone.find_all("img"):
        alt = img.get("alt") or ""
        src = img.get("src") or ""
        note = alt if alt else src
        if "platzhalter" in src.lower() or "leistungen-" in src:
            note = f"Platzhaltergrafik ({Path(src).name})"
        replacement = clone.new_tag("p")
        replacement["class"] = "img-note"
        replacement.string = f"[Bild: {note}]"
        img.replace_with(replacement)
    for a in clone.find_all("a"):
        href = a.get("href", "")
        text = a.get_text(strip=True)
        if href.startswith("/") or href.startswith("mailto:") or href.startswith("tel:"):
            span = clone.new_tag("span")
            span.string = f"{text} ({href})"
            a.replace_with(span)
        elif href.startswith("http"):
            a["target"] = "_blank"
    return "".join(str(c) for c in clone.children)


def page_meta(soup: BeautifulSoup) -> dict[str, str]:
    title = (soup.title.string or "").strip() if soup.title else ""
    desc = ""
    meta = soup.find("meta", attrs={"name": "description"})
    if meta and meta.get("content"):
        desc = meta["content"].strip()
    canon = ""
    link = soup.find("link", rel="canonical")
    if link and link.get("href"):
        canon = link["href"]
    return {"title": title, "description": desc, "canonical": canon}


def build_document(sections: list[dict]) -> str:
    today = date.today().strftime("%d.%m.%Y")
    toc_items = "".join(
        f'<li><a href="#sec-{i}">{s["label"]}</a></li>' for i, s in enumerate(sections)
    )
    body = ""
    for i, s in enumerate(sections):
        body += f"""
    <section class="chapter" id="sec-{i}">
      <div class="chapter-meta">
        <span class="path">learnbox.ch{s["path"]}</span>
        <h2>{s["label"]}</h2>
        <p><strong>Seitentitel (Browser-Tab):</strong> {s["meta"]["title"]}</p>
        <p><strong>Meta-Beschreibung:</strong> {s["meta"]["description"] or "—"}</p>
      </div>
      <div class="chapter-body">
        {s["html"]}
      </div>
    </section>
"""

    return f"""<!DOCTYPE html>
<html lang="de-CH">
<head>
  <meta charset="utf-8" />
  <title>learnbox – Korrekturlesen {today}</title>
  <style>
    @page {{ margin: 22mm 18mm 24mm 18mm; }}
    body {{
      font-family: "PT Sans", "Segoe UI", sans-serif;
      font-size: 11pt;
      line-height: 1.45;
      color: #14221c;
    }}
    h1 {{ font-size: 20pt; margin: 0 0 0.5rem; color: #0e3d2e; }}
    h2 {{ font-size: 15pt; margin: 0 0 0.75rem; color: #0e3d2e; page-break-after: avoid; }}
    h3 {{ font-size: 12pt; margin: 1rem 0 0.35rem; page-break-after: avoid; }}
    .cover {{ margin-bottom: 2rem; padding-bottom: 1rem; border-bottom: 2px solid #0b7a4b; }}
    .cover p {{ color: #3a4a42; }}
    .toc {{ margin: 1.5rem 0 2rem; }}
    .toc ul {{ columns: 2; column-gap: 2rem; margin: 0; padding-left: 1.2rem; }}
    .toc li {{ margin: 0.25rem 0; }}
    .chapter {{
      page-break-before: always;
      break-before: page;
    }}
    .chapter:first-of-type {{ page-break-before: auto; }}
    .chapter-meta {{
      background: #f6f1e8;
      border: 1px solid #d9d0c0;
      border-radius: 8px;
      padding: 0.85rem 1rem;
      margin-bottom: 1rem;
      font-size: 10pt;
    }}
    .chapter-meta .path {{
      font-family: ui-monospace, monospace;
      font-size: 9pt;
      color: #0b7a4b;
    }}
    .chapter-meta p {{ margin: 0.35rem 0; }}
    .chapter-body p {{ margin: 0 0 0.65rem; }}
    .chapter-body ul, .chapter-body ol {{ margin: 0 0 0.75rem; padding-left: 1.2rem; }}
    .img-note {{
      font-style: italic;
      color: #57534e;
      font-size: 9.5pt;
      margin: 0.5rem 0;
    }}
    .eyebrow {{
      text-transform: uppercase;
      letter-spacing: 0.12em;
      font-size: 9pt;
      font-weight: 700;
      color: #0b7a4b;
    }}
    .meta span {{ margin-right: 1rem; }}
  </style>
</head>
<body>
  <div class="cover">
    <h1>learnbox.ch – Korrekturlesen</h1>
    <p>Stand: {today} · Alle Texte der geplanten Website in Lesereihenfolge.</p>
    <p>Nicole Strähl / learnbox GmbH · Seidenstrasse 47, 8400 Winterthur</p>
  </div>
  <div class="toc">
    <h2>Inhalt</h2>
    <ul>{toc_items}</ul>
  </div>
  {body}
</body>
</html>
"""


def collect_sections() -> list[dict]:
    sections: list[dict] = []
    for label, path, urlpath in PAGES:
        if not path.is_file():
            print(f"Warnung: fehlt {path}", file=sys.stderr)
            continue
        raw = path.read_text(encoding="utf-8")
        soup = BeautifulSoup(raw, "lxml")
        main = strip_chrome(soup)
        if not main:
            continue
        sections.append(
            {
                "label": label,
                "path": urlpath,
                "meta": page_meta(soup),
                "html": simplify_main(main),
            }
        )
    return sections


def print_pdf(html_path: Path, pdf_path: Path) -> None:
    html_url = html_path.resolve().as_uri()
    pdf_path.unlink(missing_ok=True)
    cmd = [
        "google-chrome",
        "--headless=new",
        "--disable-gpu",
        "--no-first-run",
        "--no-default-browser-check",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        html_url,
    ]
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    deadline = time.monotonic() + 90
    last_size = -1
    stable = 0
    try:
        while time.monotonic() < deadline:
            if pdf_path.is_file():
                size = pdf_path.stat().st_size
                if size > 20_000 and size == last_size:
                    stable += 1
                    if stable >= 2:
                        break
                else:
                    stable = 0
                last_size = size
            time.sleep(0.5)
        else:
            raise RuntimeError("PDF-Erzeugung: Zeitüberschreitung (Chrome)")
        if not pdf_path.is_file() or pdf_path.stat().st_size < 20_000:
            raise RuntimeError("PDF-Erzeugung: Ausgabedatei fehlt oder ist zu klein")
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


def main() -> int:
    sections = collect_sections()
    html = build_document(sections)
    OUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    OUT_HTML.write_text(html, encoding="utf-8")
    print_pdf(OUT_HTML, OUT_PDF)
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_bytes(OUT_PDF.read_bytes())
    print(f"HTML: {OUT_HTML}")
    print(f"PDF:  {OUT_PDF} ({OUT_PDF.stat().st_size // 1024} KB)")
    print(f"Kopie: {ARTIFACT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
