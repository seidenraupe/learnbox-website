# GitHub auf den neuesten Stand bringen

Die Cloud-Agents können auf **GitHub** nicht direkt pushen (Token ohne Schreibrecht). Der aktuelle Stand liegt auf **Cursor Origin** (`main`, Commit-Stempel siehe `git log -1`).

## Variante A – Git Bundle (19 Commits gegenüber GitHub)

1. Repo klonen (oder bestehenden Ordner nutzen):
   ```text
   C:\Users\thoma\inspiroo gmbh\KI-Projekte - Projekte\learnbox-website
   ```
2. Datei **`learnbox-github-update.bundle`** in diesen Ordner legen (vom Agent-Download oder `docs/` nach erneutem Erzeugen).
3. In **Git Bash** oder PowerShell im Repo:

   ```bash
   cd "C:/Users/thoma/inspiroo gmbh/KI-Projekte - Projekte/learnbox-website"
   git fetch ../learnbox-github-update.bundle main:main
   ```
   Oder wenn `main` schon existiert:

   ```bash
   git pull "C:/Users/thoma/inspiroo gmbh/KI-Projekte - Projekte/learnbox-website/learnbox-github-update.bundle" main
   ```

4. **GitHub Desktop** → **Push origin** (oder `git push origin main`).

5. Unter [Actions](https://github.com/seidenraupe/learnbox-website/actions) laufen **GitHub Pages** und ggf. **FTP-Deploy** automatisch.

## Variante B – Neu von Cursor Origin

Falls Thomas Zugriff auf das Cursor-Repo hat:

```bash
git clone https://origin.cursor.com/git/thomas-giger/learnbox-web.git learnbox-website
cd learnbox-website
git remote add github https://github.com/seidenraupe/learnbox-website.git
git push github main
```

## Bundle neu erzeugen (im Cloud-Projekt)

```bash
git fetch github
git bundle create docs/learnbox-github-update.bundle github/main..main
```