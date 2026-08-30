#!/usr/bin/env bash
# Das Repo existiert: https://github.com/seidenraupe/learnbox-website
set -euo pipefail
cd "$(dirname "$0")/.."

if ! gh auth status >/dev/null 2>&1; then
  echo "Bitte zuerst: gh auth login"
  exit 1
fi

gh repo view seidenraupe/learnbox-website
echo "Clone: https://github.com/seidenraupe/learnbox-website.git"
