import { defineConfig } from "vite";
import { createReadStream, existsSync, statSync } from "node:fs";
import { resolve } from "node:path";

function sendFile(res, filePath, contentType, downloadName) {
  const stat = statSync(filePath);
  res.setHeader("Content-Type", contentType);
  res.setHeader("Content-Length", String(stat.size));
  if (downloadName) {
    res.setHeader(
      "Content-Disposition",
      `attachment; filename="${downloadName}"`
    );
  }
  createReadStream(filePath).pipe(res);
}

/** Dev-only: ZIP + Download-Seite, nie Teil von dist/ / learnbox.ch */
function windowsSourceDownload() {
  return {
    name: "windows-source-download",
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        const path = (req.url ?? "").split("?")[0];
        if (path === "/learnbox-web.zip") {
          const zipPath = resolve(__dirname, "learnbox-web.zip");
          if (!existsSync(zipPath)) {
            res.statusCode = 404;
            res.setHeader("Content-Type", "text/plain; charset=utf-8");
            res.end("ZIP fehlt. Bitte scripts/pack-source.sh ausführen.");
            return;
          }
          sendFile(res, zipPath, "application/zip", "learnbox-web.zip");
          return;
        }
        if (path === "/download.html" || path === "/download") {
          sendFile(
            res,
            resolve(__dirname, "scripts/windows-download.html"),
            "text/html; charset=utf-8"
          );
          return;
        }
        next();
      });
    },
  };
}

export default defineConfig({
  root: ".",
  publicDir: "public",
  plugins: [windowsSourceDownload()],
  build: {
    outDir: "dist",
    emptyOutDir: true,
    rollupOptions: {
      input: {
        main: resolve(__dirname, "index.html"),
        leistungen: resolve(__dirname, "leistungen.html"),
        ueber: resolve(__dirname, "ueber.html"),
        blog: resolve(__dirname, "blog.html"),
        kontakt: resolve(__dirname, "kontakt.html"),
        impressum: resolve(__dirname, "impressum.html"),
        datenschutz: resolve(__dirname, "datenschutz.html"),
        "blog-vernetzung": resolve(
          __dirname,
          "blog/schwarm-intelligenz-dank-vernetzung.html"
        ),
        "blog-foerdern": resolve(__dirname, "blog/schwarm-intelligenz-foerdern.html"),
        "blog-revolution": resolve(
          __dirname,
          "blog/revolution-in-der-weiterbildung.html"
        ),
        "blog-lms": resolve(
          __dirname,
          "blog/digitalisierung-nicht-verschlafen.html"
        ),
        "blog-wissen": resolve(
          __dirname,
          "blog/internes-wissen-gezielt-foerdern.html"
        ),
        "blog-micro-ki": resolve(__dirname, "blog/micro-learning-mit-ki.html"),
        "blog-ki-haeppchen": resolve(
          __dirname,
          "blog/ki-im-elearning-personalisierte-haeppchen.html"
        ),
        "blog-fuenf-minuten": resolve(
          __dirname,
          "blog/fuenf-minuten-am-arbeitsplatz.html"
        ),
        notfound: resolve(__dirname, "404.html"),
      },
    },
  },
  server: {
    host: "127.0.0.1",
    port: 43147,
    strictPort: true,
  },
  preview: {
    host: "127.0.0.1",
    port: 43147,
    strictPort: true,
  },
});
