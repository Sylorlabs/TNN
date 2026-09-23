#!/bin/bash
# run_w1.sh — build + run the W1 harness twice; enforce K1 (byte-identical
# reruns). Usage: run_w1.sh <data-dir> <out-dir>
# Exit 0 iff: build OK, both runs exit 0, transcripts byte-identical.
set -u
DATADIR="${1:?usage: run_w1.sh <data-dir> <out-dir>}"
OUTDIR="${2:?usage: run_w1.sh <data-dir> <out-dir>}"
HERE="$(cd "$(dirname "$0")" && pwd)"
OUTDIR="$(cd "$OUTDIR" 2>/dev/null && pwd || (mkdir -p "$OUTDIR" && cd "$OUTDIR" && pwd))"
ZNC="$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1"
mkdir -p "$OUTDIR"

"$ZNC" "$HERE/w1.zag" --no-zagd --no-analyze --no-foreground-cache \
    -o "$OUTDIR/w1_bin" || { echo "W1_BUILD_FAIL"; exit 10; }

(cd "$HERE" && "$OUTDIR/w1_bin" "$DATADIR" > "$OUTDIR/run_a.txt" 2> "$OUTDIR/run_a.err")
rc_a=$?
(cd "$HERE" && "$OUTDIR/w1_bin" "$DATADIR" > "$OUTDIR/run_b.txt" 2> "$OUTDIR/run_b.err")
rc_b=$?
echo "run_a_exit=$rc_a run_b_exit=$rc_b"
[ "$rc_a" -eq 0 ] && [ "$rc_b" -eq 0 ] || { echo "K1_RUN_EXIT_FAIL"; exit 11; }

sa=$(sha256sum "$OUTDIR/run_a.txt" | cut -d' ' -f1)
sb=$(sha256sum "$OUTDIR/run_b.txt" | cut -d' ' -f1)
echo "sha_a=$sa"
echo "sha_b=$sb"
if [ "$sa" != "$sb" ]; then echo "K1_DETERMINISM_FAIL"; exit 12; fi
echo "K1_DETERMINISM_PASS"

# every CHECK line must have actual==expected in both runs
for f in run_a.txt run_b.txt; do
  bad=$(awk -F, '/^CHECK/{if($3!=$4){print}}' "$OUTDIR/$f" | wc -l)
  echo "$f bad_checks=$bad"
  [ "$bad" -eq 0 ] || { echo "CHECK_FAIL in $f"; exit 13; }
done
echo "W1_RUN_PASS"
