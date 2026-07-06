#!/usr/bin/env bash
# Rebuild the standalone distributable zip from the bundle sources.
# Run from anywhere: ./build-zip.sh
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"
mkdir -p dist
OUT="dist/loop-maker-skill-standalone.zip"
rm -f "$OUT"
zip -r -X "$OUT" install.sh README.md loop-maker \
  -x '*.DS_Store' -x '*/__pycache__/*' >/dev/null
echo "✓ Built $OUT"
unzip -l "$OUT" | tail -1
