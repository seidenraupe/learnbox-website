#!/usr/bin/env python3
"""Erzeugt learnbox-korrekturlesen.pdf: Meta-Übersicht + Seiten im Original-Layout (Bilder, CI)."""
from __future__ import annotations

import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

from bs4 import BeautifulSoup, Tag
from pypdf import PdfWriter

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "docs" / ".korrektur-cache"
OUT_HTML = ROOT / "docs" / "korrekturlesen.html"
OUT_PDF = ROOT / "docs" / "learnbox-korrekturlesen.pdf"
ARTIFACT = Path("/opt/cursor/artifacts/learnbox-korrekturlesen.pdf")
PREVIEW_HOST = "127.0.0.1"
PREVIEW_PORT = 43147
PREVIEW_BASE = f"http://{PREVIEW_HOST}:{PREVIEW_PORT}"

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


def form_to_html(form: Tag) -> str:
    """Kontaktformular-Felder als HTML-Liste für die Meta-Sektion."""
    doc = BeautifulSoup("", "lxml")
    block = doc.new_tag("div")
    block["class"] = "form-proof"
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
        li = doc.new_tag("li")
        li.string = (
            f"Auswahl «Thema»: {opt.get_text(strip=True)} (value: {opt.get('value', '')})"
        )
        ul.append(li)
    btn = form.find("button", type="submit")
    if btn:
        li = doc.new_tag("li")
        li.string = f"Schaltfläche: {btn.get_text(strip=True)}"
        ul.append(li)
    block.append(ul)
    muted = form.find("p", class_="muted")
    if muted:
        block.append(muted)
    return str(block)


def page_meta(soup: BeautifulSoup) -> dict[str, str]:
    title = (soup.title.string or "").strip() if soup.title else ""
    desc = ""
    meta = soup.find("meta", attrs={"name": "description"})
    if meta and meta.get("content"):
        desc = meta["content"].strip()
    return {"title": title, "description": desc}


def preview_url(urlpath: str) -> str:
    if urlpath == "/":
        return f"{PREVIEW_BASE}/"
    return f"{PREVIEW_BASE}{urlpath}"


def collect_sections() -> list[dict]:
    sections: list[dict] = []
    for label, path, urlpath in PAGES:
        if not path.is_file():
            print(f"Warnung: fehlt {path}", file=sys.stderr)
            continue
        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "lxml")
        extra = ""
        if path.name == "kontakt.html":
            form = soup.find("form")
            if form:
                extra = form_to_html(form)
        sections.append(
            {
                "label": label,
                "path": urlpath,
                "meta": page_meta(soup),
                "extra_html": extra,
            }
        )
    return sections


def build_intro_html(sections: list[dict]) -> str:
    today = date.today().strftime("%d.%m.%Y")
    toc_items = "".join(f"<li>{s['label']} <span class='path'>({s['path']})</span></li>" for s in sections)
    meta_blocks = ""
    for i, s in enumerate(sections):
        extra = f"<div class='extra'>{s['extra_html']}</div>" if s.get("extra_html") else ""
        meta_blocks += f"""
      <article class="meta-block" id="meta-{i}">
        <h3>{s["label"]}</h3>
        <p class="path">learnbox.ch{s["path"]}</p>
        <p><strong>Seitentitel (Browser-Tab):</strong> {s["meta"]["title"]}</p>
        <p><strong>Meta-Beschreibung:</strong> {s["meta"]["description"] or "—"}</p>
        {extra}
      </article>
"""

    return f"""<!DOCTYPE html>
<html lang="de-CH">
<head>
  <meta charset="utf-8" />
  <title>learnbox – Korrekturlesen {today}</title>
  <style>
    @page {{ margin: 20mm 16mm 22mm 16mm; }}
    body {{
      font-family: "PT Sans", "Segoe UI", sans-serif;
      font-size: 10.5pt;
      line-height: 1.45;
      color: #14221c;
    }}
    h1 {{ font-size: 22pt; margin: 0 0 0.5rem; color: #0e3d2e; }}
    h2 {{ font-size: 14pt; margin: 1.5rem 0 0.6rem; color: #0e3d2e; page-break-after: avoid; }}
    h3 {{ font-size: 11.5pt; margin: 0 0 0.35rem; color: #0e3d2e; }}
    .cover {{ margin-bottom: 1.5rem; padding-bottom: 0.75rem; border-bottom: 2px solid #0b7a4b; }}
    .cover p, .lede {{ color: #3a4a42; }}
    .lede {{ font-size: 11pt; margin: 0.75rem 0 0; }}
    .toc ul {{ columns: 2; column-gap: 1.5rem; margin: 0.5rem 0 0; padding-left: 1.1rem; }}
    .toc li {{ margin: 0.2rem 0; break-inside: avoid; }}
    .path {{ font-family: ui-monospace, monospace; font-size: 9pt; color: #0b7a4b; }}
    .meta-block {{
      break-inside: avoid;
      background: #f6f1e8;
      border: 1px solid #d9d0c0;
      border-radius: 6px;
      padding: 0.65rem 0.85rem;
      margin: 0 0 0.65rem;
      font-size: 9.5pt;
    }}
    .meta-block p {{ margin: 0.25rem 0; }}
    .meta-block .extra {{ margin-top: 0.35rem; }}
    .meta-block ul {{ margin: 0.35rem 0 0; padding-left: 1.1rem; }}
    .section-break {{ page-break-before: always; break-before: page; }}
    .hint {{
      background: #e8f5ef;
      border-left: 4px solid #0b7a4b;
      padding: 0.6rem 0.85rem;
      margin: 1rem 0;
      font-size: 10pt;
    }}
  </style>
</head>
<body>
  <div class="cover">
    <h1>learnbox.ch – Korrekturlesen</h1>
    <p>Stand: {today}</p>
    <p class="lede">
      Dieses PDF enthält zuerst SEO- und Formular-Metadaten. Ab der nächsten Sektion folgen
      alle Seiten im <strong>Original-Layout</strong> (Farben, Typografie, Bilder) – aus dem
      produktionsnahen Build, analog zur Live-Vorschau im Browser.
    </p>
    <p>Nicole Strähl / learnbox GmbH · Seidenstrasse 47, 8400 Winterthur</p>
  </div>
  <div class="toc">
    <h2>Inhalt (Seitenreihenfolge)</h2>
    <ul>{toc_items}</ul>
  </div>
  <div class="section-break">
    <h2>SEO &amp; Formulartexte</h2>
    <p class="lede">Hier prüfen: Titel, Meta-Beschreibung, Kontaktformular.</p>
    {meta_blocks}
  </div>
  <div class="section-break hint">
    <strong>Website-Darstellung folgt.</strong> Jede der nächsten Seiten entspricht einer
    vollständigen Ansicht der jeweiligen learnbox.ch-Seite (inkl. Kopf- und Fusszeile).
  </div>
</body>
</html>
"""


def run_build() -> None:
    subprocess.run(["npm", "run", "build"], cwd=ROOT, check=True)


def start_preview() -> subprocess.Popen[bytes]:
    return subprocess.Popen(
        ["npm", "run", "preview"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )


def wait_for_preview(proc: subprocess.Popen[bytes], timeout: float = 45) -> None:
    url = f"{PREVIEW_BASE}/"
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if proc.poll() is not None:
            raise RuntimeError("Vite-Preview ist unerwartet beendet worden")
        try:
            with urllib.request.urlopen(url, timeout=2) as resp:
                if resp.status == 200:
                    return
        except (urllib.error.URLError, TimeoutError):
            time.sleep(0.4)
    raise RuntimeError("Vite-Preview nicht erreichbar")


def print_chrome_pdf(source: str, pdf_path: Path, min_size: int = 8_000) -> None:
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    pdf_path.unlink(missing_ok=True)
    cmd = [
        "google-chrome",
        "--headless=new",
        "--disable-gpu",
        "--no-first-run",
        "--no-default-browser-check",
        "--no-pdf-header-footer",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={pdf_path}",
        source,
    ]
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    deadline = time.monotonic() + 120
    last_size = -1
    stable = 0
    try:
        while time.monotonic() < deadline:
            if pdf_path.is_file():
                size = pdf_path.stat().st_size
                if size >= min_size and size == last_size:
                    stable += 1
                    if stable >= 2:
                        break
                else:
                    stable = 0
                last_size = size
            time.sleep(0.45)
        else:
            raise RuntimeError(f"PDF-Erzeugung Zeitüberschreitung: {source}")
        if not pdf_path.is_file() or pdf_path.stat().st_size < min_size:
            raise RuntimeError(f"PDF-Ausgabe fehlt oder zu klein: {pdf_path}")
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


def merge_pdfs(paths: list[Path], destination: Path) -> None:
    writer = PdfWriter()
    for path in paths:
        writer.append(str(path))
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("wb") as f:
        writer.write(f)
    writer.close()


def main() -> int:
    try:
        import bs4  # noqa: F401
    except ImportError as e:
        print("Bitte installieren: pip install beautifulsoup4 lxml pypdf", file=sys.stderr)
        raise SystemExit(1) from e

    sections = collect_sections()
    intro_html = build_intro_html(sections)
    OUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    OUT_HTML.write_text(intro_html, encoding="utf-8")

    print("Build …", file=sys.stderr)
    run_build()

    preview = start_preview()
    part_paths: list[Path] = []
    try:
        wait_for_preview(preview)
        time.sleep(0.8)

        CACHE.mkdir(parents=True, exist_ok=True)
        intro_pdf = CACHE / "00-intro.pdf"
        print_chrome_pdf(OUT_HTML.resolve().as_uri(), intro_pdf, min_size=12_000)
        part_paths.append(intro_pdf)

        for i, s in enumerate(sections):
            url = preview_url(s["path"])
            part = CACHE / f"{i + 1:02d}-page.pdf"
            print(f"Drucke {s['label']} …", file=sys.stderr)
            print_chrome_pdf(url, part, min_size=15_000)
            part_paths.append(part)

        merge_pdfs(part_paths, OUT_PDF)
    finally:
        preview.terminate()
        try:
            preview.wait(timeout=5)
        except subprocess.TimeoutExpired:
            preview.kill()

    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_bytes(OUT_PDF.read_bytes())
    print(f"HTML (Einleitung): {OUT_HTML}")
    print(f"PDF:  {OUT_PDF} ({OUT_PDF.stat().st_size // 1024} KB)")
    print(f"Kopie: {ARTIFACT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
