# Website ohne Git auf den Windows-PC

Origin und Cursor-Git verlangen oft Benutzername und Passwort. Mit Google-Anmeldung in Cursor funktioniert das **nicht**. WSL und Origin-CLI sind dafür nicht nötig.

**Weg: ZIP herunterladen, Ordner in Cursor öffnen.** Genau so, als läge das Projekt schon lokal – ohne Clone, ohne Login.

## 1. ZIP holen

In der laufenden Vorschau dieser Umgebung:

[http://127.0.0.1:43147/download.html](http://127.0.0.1:43147/download.html)

Dort **Quellcode herunterladen** klicken. Datei: `learnbox-web.zip`.

Direktlink: [http://127.0.0.1:43147/learnbox-web.zip](http://127.0.0.1:43147/learnbox-web.zip)

Die ZIP liegt **nicht** auf der späteren Live-Site (learnbox.ch). Sie wird nur in der lokalen Vorschau angeboten.

## 2. Entpacken

1. Im Explorer die ZIP doppelklicken oder Rechtsklick → **Alle extrahieren**.
2. Ziel z. B. `Dokumente\learnbox-web`.
3. Im Ordner müssen `package.json`, `index.html` und der Ordner `src` sichtbar sein.

## 3. In Cursor öffnen

1. Cursor Desktop (Windows, ohne WSL).
2. **File → Open Folder** (Datei → Ordner öffnen).
3. Den entpackten Ordner `learnbox-web` wählen.

Kein Git-Remote, kein Clone, keine Anmeldung.

## 4. Vorschau lokal

Im integrierten Terminal von Cursor (PowerShell reicht):

```powershell
npm install
npm run dev
```

Browser: [http://127.0.0.1:43147](http://127.0.0.1:43147)

Zum Veröffentlichen bei KreativMedia:

```powershell
npm run build
```

Den Inhalt von `dist\` per FTP nach `httpdocs` laden. Details: [HOSTING.md](HOSTING.md).

## Optional später: GitHub

Wenn Sie die Dateien versionieren wollen, geht das **über GitHub**, nicht über Origin:

1. Auf [github.com](https://github.com) ein privates Repo `learnbox-website` anlegen (leer, ohne README).
2. [GitHub Desktop](https://desktop.github.com) installieren und mit dem GitHub-Konto anmelden.
3. **Add → Add existing repository** auf den Ordner `learnbox-web`.
4. Remote setzen und pushen.

Schritt-für-Schritt: [GITHUB.md](GITHUB.md).
