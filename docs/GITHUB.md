# GitHub-Repository `learnbox-website`

Dieses Projekt ist als **ein** Git-Repository vorbereitet: statische Site, Dokumentation, Deploy-Vorlage. Das GitHub-Repository **learnbox-website** ist angelegt; Commits in dieser Umgebung gehen auf den verknüpften `main`-Branch.

Falls Sie das Repo lokal klonen oder einen zweiten Remote setzen wollen:

## Variante A – Cursor

Oben auf **Create repo** klicken und den Namen `learnbox-website` wählen (privat empfohlen). Danach ist GitHub die Fernkopie dieses Stands.

## Variante B – GitHub-Website

1. Auf GitHub ein neues Repository **learnbox-website** anlegen (ohne README, ohne License).
2. Remote setzen und pushen:

```bash
git remote add github git@github.com:IHR-USER/learnbox-website.git
git push -u github main
```

Ersetzen Sie `IHR-USER` durch den GitHub-Account, der learnbox gehören soll (Firma oder Nicole Strähl / Thomas Giger).

## Variante C – GitHub CLI (lokal, einmalig)

```bash
gh auth login
gh repo create learnbox-website --private --source=. --remote=github --push
```

Das Hilfsskript `scripts/create-github-repo.sh` macht denselben Aufruf, sobald `gh` angemeldet ist.

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
