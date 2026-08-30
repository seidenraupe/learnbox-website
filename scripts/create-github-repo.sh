#!/usr/bin/env bash
# Legt das GitHub-Repository learnbox-website an, sobald gh angemeldet ist.
set -euo pipefail
cd "$(dirname "$0")/.."

if ! gh auth status >/dev/null 2>&1; then
  echo "Bitte zuerst lokal ausführen: gh auth login"
  exit 1
fi

gh repo create learnbox-website --private --source=. --remote=github --push --description "Statische Website learnbox.ch (HTML, KreativMedia)"
echo "Repository: $(gh repo view learnbox-website --json url -q .url)"
