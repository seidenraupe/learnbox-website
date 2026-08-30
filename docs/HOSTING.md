# Hosting bei KreativMedia

KreativMedia-Webhosting (Plesk, Schweizer Rechenzentrum, Let’s Encrypt, FTP, PHP) reicht für diese Site. Empfohlenes Paket: **Webhosting Star** – Speicher und PHP sind für statisches HTML plus ein Kontakt-Skript mehr als genug. Der Website-Builder von KreativMedia wird **nicht** gebraucht.

## Was auf den Server kommt

Nach `npm run build` liegt die Site in `dist/`:

- HTML-Seiten
- `/assets/*.css` und `/assets/*.js` (von Vite gehashed)
- `kontakt.php`
- `.htaccess`, `robots.txt`, `sitemap.xml`, Favicons

Diesen Ordnerinhalt nach `httpdocs` kopieren (nicht den Ordner `dist` selbst als Unterordner).

## Weg 1: FTP (einfach)

1. In Plesk FTP-Benutzer notieren.
2. Mit FileZilla oder `lftp` den Inhalt von `dist/` nach `httpdocs` laden.
3. PHP für die Domain einschalten (Standard).
4. SSL: «Let’s Encrypt» für `learnbox.ch` und `www.learnbox.ch`.

Optional automatisiert: GitHub Action `.github/workflows/deploy-ftp.yml`.

## Weg 2: Git in Plesk

1. Remote: `https://github.com/seidenraupe/learnbox-website.git` (privat, Account seidenraupe).
2. In Plesk bei der Domain **Git** → Remote-Repository (HTTPS oder Deploy-Key).
3. Deployment-Verzeichnis: nicht roh auf `httpdocs` zeigen, wenn dort der Quellcode inkl. `src/` landen würde.
4. Saubere Variante: CI baut `dist/` und pusht nur das Artefakt, **oder** lokal bauen und einen `deploy`-Branch mit dem Inhalt von `dist/` pflegen.

Für learnbox ist **FTP oder CI → FTP** die unkomplizierteste Lösung, weil Node auf Shared Hosting nicht vorausgesetzt wird.

## Domain und E-Mail

- Domain liegt heute bei Wix. Zum Stichtag Nameserver oder A-Record auf KreativMedia setzen (Werte im Plesk-Dashboard).
- `www` und Apex (`learnbox.ch`) auf dieselbe `httpdocs`.
- Mailbox `nicole.straehl@learnbox.ch` und `noreply@learnbox.ch` in Plesk anlegen **bevor** die MX-Records weg von Wix zeigen.
- SPF/DKIM in Plesk aktivieren, damit `kontakt.php` nicht im Spam landet.

## Formular

`kontakt.php` erwartet POST von `/kontakt.html`. Empfänger standardmässig `nicole.straehl@learnbox.ch`. Überschreiben in Plesk über Umgebungsvariable `LEARNBOX_MAIL_TO`, falls Plesk das für die Domain anbietet; sonst die Adresse in der PHP-Datei anpassen.

Test: Formular auf der Staging-Domain absenden und Posteingang prüfen.

## Checkliste vor DNS-Umstellung

- [ ] Site unter temporärer URL erreichbar
- [ ] HTTPS ohne Zertifikatswarnung
- [ ] Kontaktmail kommt an
- [ ] `/dienstleistungen` leitet auf `/leistungen.html`
- [ ] `/learnblog` leitet auf `/blog.html`
- [ ] Mobilmenü und Formular auf dem Handy geprüft
- [ ] Impressum-Adresse bestätigt
