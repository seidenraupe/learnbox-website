# Learnbox Website

Statische HTML-Website für [learnbox.ch](https://www.learnbox.ch): Beratung für digitales Lernen, blended learning und LMS-Einführung in Unternehmen.

Hausschrift gemäss CI: **PT Sans** (lokal unter `public/fonts/`). Adresse: Seidenstrasse 47, 8400 Winterthur.

Dieses Repository ersetzt den bisherigen Wix-Auftritt. Die gebauten Dateien aus `dist/` werden auf **KreativMedia** (Plesk, `httpdocs`) veröffentlicht.

## Lokal starten

```bash
npm install
npm run dev
```

Die Vorschau läuft auf [http://127.0.0.1:43147](http://127.0.0.1:43147).

```bash
npm run build
```

erzeugt das deploybare Verzeichnis `dist/`.

## GitHub-Repository

Zielname: **`learnbox-website`**.

Solange dieses Projekt noch ohne eigenes GitHub-Repository läuft, können Sie oben in Cursor auf **Create repo** klicken und den Namen `learnbox-website` wählen. Schritt-für-Schritt: [docs/GITHUB.md](docs/GITHUB.md).

## Hosting bei KreativMedia

Kurzanleitung: [docs/HOSTING.md](docs/HOSTING.md).

Kurzfassung:

1. `npm run build`
2. Inhalt von `dist/` nach `httpdocs` (FTP oder Git in Plesk)
3. PHP für `kontakt.php` aktiv lassen
4. Let’s Encrypt SSL in Plesk einschalten
5. DNS der Domain `learnbox.ch` von Wix auf KreativMedia umstellen

## Inhalt und Umsetzung

Der Vorschlag für Informationsarchitektur, Texte, Technik und Go-live steht in [docs/VORSCHLAG.md](docs/VORSCHLAG.md).

## Seiten

| Pfad | Inhalt |
| --- | --- |
| `/` | Start: Nutzen, Leistungen, Kontaktaufruf |
| `/leistungen.html` | Beratungsprozess von Analyse bis Begleitung |
| `/ueber.html` | learnbox GmbH und Nicole Strähl |
| `/blog.html` | LearnBlog-Übersicht |
| `/kontakt.html` | Formular, Adresse, Telefon |
| `/impressum.html` | Pflichtangaben |
| `/datenschutz.html` | Datenschutzerklärung |

Kontaktformular: `public/kontakt.php` (PHP `mail()` auf KreativMedia). Lokal erscheint ein Hinweis, weil PHP im Vite-Dev-Server nicht läuft.
