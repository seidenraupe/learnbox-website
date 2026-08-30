#!/usr/bin/env bash
# Packt den Website-Quellcode als ZIP für Windows (ohne Git, ohne node_modules).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT

mkdir -p "$STAGE/learnbox-web"
tar -C "$ROOT" \
  --exclude=".git" \
  --exclude="node_modules" \
  --exclude="dist" \
  --exclude="*.zip" \
  --exclude="learnbox-web.zip" \
  -cf - . | tar -C "$STAGE/learnbox-web" -xf -

rm -f "$ROOT/learnbox-web.zip" "$ROOT/public/learnbox-web.zip"
(cd "$STAGE" && zip -r -q "$ROOT/learnbox-web.zip" learnbox-web)

echo "Geschrieben: $ROOT/learnbox-web.zip"
ls -lh "$ROOT/learnbox-web.zip"
