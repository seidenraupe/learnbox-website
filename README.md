# Learnbox Website

Statische HTML-Website für [learnbox.ch](https://www.learnbox.ch): Beratung für digitales Lernen, blended learning und LMS-Einführung in Unternehmen.

Hausschrift gemäss CI: **PT Sans** (lokal unter `public/fonts/`). Adresse: Seidenstrasse 47, 8400 Winterthur.

Dieses Repository ersetzt den bisherigen Wix-Auftritt. Die gebauten Dateien aus `dist/` werden auf **KreativMedia** (Plesk, `httpdocs`) veröffentlicht.

## Windows: ohne Git, ohne Origin-Login

Cursor-Git und Origin verlangen Zugangsdaten, die mit der Google-Anmeldung nicht passen. **ZIP laden und den Ordner in Cursor öffnen** – kein Clone, kein WSL.

In der Agent-Vorschau: [Download-Seite](http://127.0.0.1:43147/download.html) oder direkt [learnbox-web.zip](http://127.0.0.1:43147/learnbox-web.zip).

Anleitung: [docs/WINDOWS.md](docs/WINDOWS.md).

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

## GitHub-Repository (optional)

Zielname: **`learnbox-website`**. Nicht nötig, um die Site lokal zu öffnen oder bei KreativMedia zu veröffentlichen.

Wenn Sie versionieren wollen: Repo auf github.com anlegen und mit **GitHub Desktop** pushen (Google/GitHub-Login, nicht Origin). Details: [docs/GITHUB.md](docs/GITHUB.md).

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
| `/blog.html` | LearnBlog (acht Beiträge, inkl. Micro-Learning und KI) |
| `/kontakt.html` | Formular, Adresse, Telefon |
| `/impressum.html` | Pflichtangaben |
| `/datenschutz.html` | Datenschutzerklärung |

Kontaktformular: `public/kontakt.php` (PHP `mail()` auf KreativMedia). Lokal erscheint ein Hinweis, weil PHP im Vite-Dev-Server nicht läuft.
