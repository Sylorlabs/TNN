#!/bin/sh
# build.sh — compile the R0 harness driver.
# Output goes to /tmp (or $1); NOTHING compiled is committed (no binaries,
# no .zagd, no .zag-cache, no corpora in the repo — see README.md).
# Usage: build.sh [output-path]
set -u
HERE="$(dirname "$0")"
ZNC="${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}"
OUT="${1:-/tmp/harness_bin}"
cd "$HERE" || exit 2
"$ZNC" driver.zag -o "$OUT" --no-zagd --no-analyze --no-foreground-cache
rc=$?
if [ $rc -eq 0 ]; then
  echo "BUILD_OK out=$OUT"
  sha256sum "$OUT"
else
  echo "BUILD_FAIL rc=$rc"
fi
exit $rc
