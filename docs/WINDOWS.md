# Website auf den Windows-PC

Kein WSL. Nicht bei Origin oder Cursor-Git anmelden.

## Empfohlen: GitHub Desktop

Das Repo liegt unter **[seidenraupe/learnbox-website](https://github.com/seidenraupe/learnbox-website)**.

1. [GitHub Desktop](https://desktop.github.com) installieren und mit **seidenraupe** anmelden.
2. **File → Clone repository** → `seidenraupe/learnbox-website` wählen.
3. Zielordner z. B. `Dokumente\learnbox-website`.
4. In Cursor: **File → Open Folder** → denselben Ordner.

Im Terminal (PowerShell):

```powershell
npm install
npm run dev
```

Zum Veröffentlichen bei KreativMedia: `npm run build`, Inhalt von `dist\` nach `httpdocs`. Details: [HOSTING.md](HOSTING.md).

## Alternative: ZIP (ohne Git)

Falls GitHub Desktop gerade nicht passt:

1. In der Agent-Vorschau [Download-Seite](http://127.0.0.1:43147/download.html) oder [learnbox-web.zip](http://127.0.0.1:43147/learnbox-web.zip).
2. Entpacken.
3. In Cursor den Ordner `learnbox-web` öffnen.
4. `npm install` und `npm run dev`.

Die ZIP kommt nicht auf learnbox.ch.
