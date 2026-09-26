#!/bin/bash
# Build + run the seg_fill_holes regression test (pure Zag, zero RNG).
# Assembles the test exactly like the fusion4 amalgamation:
#   head -1582 composer_base.zag   (real prelude: nio_alloc, h_put64, ...)
# + chunks/fz1.zag                 (REAL seg_fill_holes under test)
# + tests/test_segfill.zag         (test main; differential vs an independent
#                                   sweep-to-fixpoint reference implementation)
# so the test exercises the committed chunk code, not a copy.
#
# Usage: ./build_segfill_test.sh [--znc /path/to/znc]
# Exit 0 iff the test binary prints SEG_FILL_REGRESSION_PASS.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
SRC="$HERE/../src"
ZNC="${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}"
for a in "$@"; do
  case "$a" in
    --znc) shift; ZNC="$1"; shift;;
  esac
done
[ -x "$ZNC" ] || { echo "znc not found: $ZNC (set \$ZNC)"; exit 2; }
for f in "$SRC/composer_base.zag" "$SRC/chunks/fz1.zag" "$HERE/test_segfill.zag"; do
  [ -f "$f" ] || { echo "missing: $f"; exit 2; }
done
WORK="$(mktemp -d "${TMPDIR:-$HOME/workspace}/segfill_test.XXXXXX")"
mkdir -p "$WORK/w/src"
# The prelude's @import("../../tnn-lab/toolchain/...") resolves relative to
# the build cwd, so mirror the layout: w/src + w/tnn-lab -> repo checkout root.
# Repo root is 5 levels above tests/: tests -> step5 -> imagination -> lab -> docs -> root.
ROOT="$HERE/../../../../.."
if [ ! -f "$ROOT/toolchain/R33_NATIVE_IO_V1.zag" ]; then
  for cand in "$HOME/workspace/tnn-lab" "$HOME/workspace/selfpam_run/tnn-lab"; do
    if [ -f "$cand/toolchain/R33_NATIVE_IO_V1.zag" ]; then ROOT="$cand"; break; fi
  done
fi
ln -sfn "$ROOT" "$WORK/tnn-lab"
head -1582 "$SRC/composer_base.zag" > "$WORK/w/src/test_segfill_full.zag"
cat "$SRC/chunks/fz1.zag" >> "$WORK/w/src/test_segfill_full.zag"
cat "$HERE/test_segfill.zag" >> "$WORK/w/src/test_segfill_full.zag"
( cd "$WORK/w/src" && "$ZNC" test_segfill_full.zag -o test_segfill --no-analyze ) 2>&1 | grep -v "zagd unavailable"
[ -x "$WORK/w/src/test_segfill" ] || { echo "BUILD_FAILED"; rm -rf "$WORK"; exit 3; }
"$WORK/w/src/test_segfill"
RC=$?
rm -rf "$WORK"
exit $RC
