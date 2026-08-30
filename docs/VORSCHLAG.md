# Vorschlag: Inhalt und Umsetzung learnbox.ch

Stand: 30. August 2026. Grundlage ist der aktuelle Wix-Auftritt [www.learnbox.ch](https://www.learnbox.ch), Firmenangaben aus dem Handelsregister (learnbox GmbH, CHE-227.823.082) und das gewünschte Ziel: **HTML auf KreativMedia**, Versionierung auf **GitHub unter `learnbox-website`**.

## 1. Ausgangslage

Die bestehende Site ist ein Wix-Einseiter plus LearnBlog. Sie erklärt den Nutzen von digitalem Lernen, listet sechs Leistungen und bietet ein Kontaktformular. Das ist klar und ehrlich – aber typisch Wix: langsam, schwer zu pflegen, ohne Impressum/Datenschutz, mit veralteten Blog-URLs und einer starken Produktbindung an ein einzelnes LMS in älteren Beiträgen.

**Was bleibt:** Ton (Sie-Form, fachlich, Winterthur), Claim «spielerisch erfolgreich lernen», Leistungszyklus Analysieren → Begleiten, Blogtexte von Nicole Strähl, Telefon +41 79 323 56 23, E-Mail nicole.straehl@learnbox.ch.

**Was sich ändert:** Statisches HTML statt Baukasten, Schweizer Hosting, Git als Quelle der Wahrheit, eigenes Impressum, Kontakt per PHP auf dem Hoster, LMS-Beratung ohne Alleinstellung eines Herstellers auf der Startseite.

## 2. Inhaltskonzept

Zielgruppe sind Ausbildungs-Verantwortliche in KMU und Institutionen, die eine Lernplattform einführen oder Inhalte professionalisieren wollen. Die Site soll ein Erstgespräch auslösen, nicht ein LMS verkaufen.

### Informationsarchitektur

| Seite | Rolle |
| --- | --- |
| Start | Nutzen in drei Sätzen, Leistungsüberblick, Blog-Teaser, CTA |
| Leistungen | Die sechs Schritte plus Ergebnis (Akademie, LMS-Auswahl) |
| Über uns | GmbH, Nicole Strähl, Haltung «Wissen teilen» |
| LearnBlog | Fünf bestehende Beiträge, stabile Pfade |
| Kontakt | Formular + Adresse + Telefon |
| Impressum / Datenschutz | Pflicht, bisher auf Wix fehlend |

### Textliche Leitplanken

- **Behalten:** «Digital lernen heisst vernetzt lernen», Gamifizierung mit Punkten und Zertifikaten, unverbindliche Analyse.
- **Schärfen:** Klare CTAs («Unverbindlich analysieren»), Zahlen nur wo belegt (Gründung 2016, sechs Schritte).
- **Lockern:** Docebo nicht als «beste und preis-vernünftigste Lösung aus Italien» auf der Marketingseite. Im Blog historisch belassen, auf Leistungen als ein mögliches Werkzeug erwähnen.
- **Ergänzen:** Person und Hintergrund (Journalismus, CAS eLearning) – das fehlt auf Wix und schafft Vertrauen.

### Offene Punkte vor Go-live (bitte gegenlesen)

1. **Fotos:** Aktuell Wortmarke und Initialen, kein Portrait. Ein Bild von Nicole Strähl würde «Über uns» tragen.
2. **Blog-Daten:** Zwei Beiträge auf Wix ohne sichtbares Datum; im HTML als LearnBlog ohne erfundene Daten.
3. **E-Mail-Absender:** `kontakt.php` sendet an nicole.straehl@learnbox.ch, From `noreply@learnbox.ch`. Mailkonto auf KreativMedia anlegen.

Die Adresse im Auftritt ist **Seidenstrasse 47, 8400 Winterthur** (Stand nach Adressänderung).

## 3. Technische Umsetzung

**Stack:** HTML, CSS, wenig JavaScript, Vite nur als lokaler Dev-Server und Bundler. Kein CMS, keine Datenbank. Das passt zu KreativMedia-Webhosting (Apache, PHP, FTP, optional Git in Plesk).

**Warum nicht WordPress:** Der Inhalt ändert selten. WordPress wäre Update- und Plugin-Pflege für eine Visitenkarten-Site. HTML bleibt schnell, versionierbar und unabhängig von Wix *und* vom Website-Builder von KreativMedia.

**Kontakt:** `public/kontakt.php` nutzt PHP `mail()`. Honeypot-Feld gegen Bots. Lokal schlägt der Versand fehl (kein PHP in Vite) – der Hinweis im Formular ist Absicht.

**SEO und Umleitung:** `sitemap.xml`, Canonical-Tags, Schema.org ProfessionalService. `.htaccess` leitet alte Wix-Pfade (`/dienstleistungen`, `/learnblog`, `/post/...`) 301 auf die neuen HTML-Dateien.

**Schriften:** Hausschrift gemäss CI ist **PT Sans** (Regular, Italic, Bold, Bold Italic). Die Dateien liegen lokal unter `public/fonts/` (SIL OFL). Es gibt keinen Aufruf zu Google Fonts.

**SSL und DNS:** Let’s Encrypt in Plesk. Domain `learnbox.ch` / `www` von Wix-Nameservern auf KreativMedia umstellen, sobald `httpdocs` die neuen Dateien enthält. E-Mail parallel auf KreativMedia (MX) planen, sonst bricht der Posteingang beim DNS-Wechsel.

## 4. GitHub `learnbox-website`

Ein Repository reicht. Name: **learnbox-website**.

Empfohlene Einrichtung:

1. In Cursor **Create repo** wählen und `learnbox-website` nennen, **oder** auf GitHub ein leeres privates Repo `learnbox-website` anlegen und dieses Projekt pushen (siehe [GITHUB.md](GITHUB.md)).
2. Branch `main` ist die Quelle für Produktion.
3. Optional: GitHub Action «FTP Deploy» mit Secrets des KreativMedia-FTP (Vorlage unter `.github/workflows/deploy-ftp.yml`).
4. Alternative ohne GitHub Actions: in Plesk Git auf das GitHub-Repo zeigen und nach `httpdocs` auschecken, danach `dist/` als Document Root oder die gebauten Dateien direkt ins Repo legen.

Für KreativMedia ohne Node auf dem Server: **lokal oder in CI bauen**, nur `dist/` hochladen. Das Workflow-File macht genau das.

## 5. Go-live-Reihenfolge

1. Texte und Adresse gegengelesen.
2. `npm run build`, `dist/` auf Staging-Subdomain (z. B. `neu.learnbox.ch`) bei KreativMedia.
3. Formular testen (E-Mail kommt an).
4. SSL, www-Redirect, alte Wix-URLs prüfen.
5. DNS umstellen, Wix-Site auf «weiterleiten» oder kündigen, sobald die neue Site 48 Stunden stabil ist.
6. Search Console / Indexierung mit der neuen Sitemap.

## 6. Was diese erste Version liefert

Ein vollständiger, lauffähiger Auftritt: Start, Leistungen, Über uns, fünf Blogbeiträge, Kontakt, Impressum, Datenschutz, Favicon in Grün/Schwarz wie bisher, Redirects, Hosting- und GitHub-Anleitung. Kein CMS-Baukasten, kein zweites Framework.
