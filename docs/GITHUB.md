# GitHub-Repository `learnbox-website`

Zum Arbeiten auf dem Windows-PC ist **kein Git** nötig. Ordner aus der ZIP öffnen: [WINDOWS.md](WINDOWS.md).

GitHub ist optional, wenn Sie den Stand versionieren oder Plesk per Git anbinden wollen. **Origin / Cursor-Git nicht verwenden** – die Anmeldung (Benutzername/Passwort) funktioniert mit Google-Login in Cursor nicht.

## Empfohlen: GitHub Desktop

1. Auf [github.com](https://github.com) ein neues **privates** Repository **learnbox-website** anlegen – ohne README, ohne License, ohne `.gitignore`.
2. [GitHub Desktop](https://desktop.github.com) installieren und mit dem GitHub-Konto anmelden.
3. **Add** → **Add existing repository** → den entpackten Ordner `learnbox-web` wählen.
4. Falls GitHub Desktop noch kein Git-Repo erkennt: **Create repository** im selben Ordner, dann unter **Repository → Repository settings → Remote** die URL `https://github.com/IHR-USER/learnbox-website.git` eintragen.
5. Commit und **Push origin**.

Ersetzen Sie `IHR-USER` durch den GitHub-Account, der learnbox gehören soll.

## Variante: GitHub-Website plus Kommandozeile

Nur wenn Git für Windows schon installiert ist und `gh` oder `git` in PowerShell laufen:

```powershell
cd Pfad\zu\learnbox-web
git init
git add .
git commit -m "Learnbox Website"
git branch -M main
git remote add origin https://github.com/IHR-USER/learnbox-website.git
git push -u origin main
```

GitHub fragt dann nach einem **Personal Access Token** oder GitHub Desktop/Git Credential Manager – nicht nach dem Cursor-Passwort.

Das Hilfsskript `scripts/create-github-repo.sh` braucht `gh auth login` (GitHub CLI), ebenfalls unabhängig von Origin.

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
