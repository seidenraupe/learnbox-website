# GitHub-Repository `learnbox-website`

Privat, Account **seidenraupe**:

**https://github.com/seidenraupe/learnbox-website**

Auf Windows klonen mit GitHub Desktop, nicht mit Origin/Cursor-Git. Anleitung: [WINDOWS.md](WINDOWS.md).

Clone-URL (HTTPS):

```
https://github.com/seidenraupe/learnbox-website.git
```

## Empfohlene Repo-Einstellungen

- Sichtbarkeit: **privat**, bis der Relaunch öffentlich sein soll; die Website selbst ist öffentlich über learnbox.ch.
- Default-Branch: `main`
- Pages: nicht nötig (Hosting ist KreativMedia, nicht GitHub Pages)
- Secrets für den optionalen FTP-Deploy:
  - `FTP_SERVER` (z. B. `ftp.kreativmedia.ch` – exakten Host in Plesk nachsehen)
  - `FTP_USERNAME`
  - `FTP_PASSWORD`
  - `FTP_REMOTE_DIR` (meist `/httpdocs` oder `/httpdocs/`)
- Repository-Variable `ENABLE_FTP_DEPLOY=true`, sonst baut die Action nur und lädt nicht hoch.

Kein zweites Repository. Inhalte, Build und Doku gehören zusammen, sonst driftet die Live-Site vom Vorschlag weg.
