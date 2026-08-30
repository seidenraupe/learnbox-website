import { defineConfig } from "vite";
import { resolve } from "node:path";

export default defineConfig({
  root: ".",
  publicDir: "public",
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
