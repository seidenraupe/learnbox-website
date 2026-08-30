# GitHub-Repository `learnbox-website`

**https://github.com/seidenraupe/learnbox-website**

Auf Windows klonen mit GitHub Desktop, nicht mit Origin/Cursor-Git. Anleitung: [WINDOWS.md](WINDOWS.md).

Clone-URL (HTTPS):

```
https://github.com/seidenraupe/learnbox-website.git
```

## Empfohlene Repo-Einstellungen

- Sichtbarkeit: öffentlich, damit GitHub Pages erreichbar ist. Die offizielle Domain bleibt learnbox.ch (KreativMedia).
- Default-Branch: `main`
- **GitHub Pages:** https://seidenraupe.github.io/learnbox-website/ (Workflow `.github/workflows/pages.yml`, bei jedem Push auf `main`)
- Kontaktformular auf Pages sendet nicht (kein PHP); E-Mail und Telefon bleiben. PHP `kontakt.php` gilt für KreativMedia.
- Secrets für den optionalen FTP-Deploy:
  - `FTP_SERVER` (z. B. `ftp.kreativmedia.ch` – exakten Host in Plesk nachsehen)
  - `FTP_USERNAME`
  - `FTP_PASSWORD`
  - `FTP_REMOTE_DIR` (meist `/httpdocs` oder `/httpdocs/`)
- Repository-Variable `ENABLE_FTP_DEPLOY=true`, sonst baut die Action nur und lädt nicht hoch.

Kein zweites Repository. Inhalte, Build und Doku gehören zusammen, sonst driftet die Live-Site vom Vorschlag weg.
