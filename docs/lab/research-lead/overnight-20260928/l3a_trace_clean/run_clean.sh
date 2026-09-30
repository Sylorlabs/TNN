#!/bin/sh
# run_clean.sh -- build and verify the L3A-TRACE clean rebuild.
# POSIX shell only. No Python at any stage.
#
# Does: compile l3a_trace_clean.zag with the pinned znc, run the battery
# 3 times, require 3/3 byte-identical stdout, empty stderr, exit 0;
# require the VERDICT line to be L3A-TRACE-CLEAN-BUILD-PASS; run the
# shell-only dash check over all owned docs; record sha256 sums.
#
# Usage: sh run_clean.sh
# Exit 0 iff the battery passes on all 3 runs.

ZNC=/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1
D=/home/hatch/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/l3a_trace_clean
SNIP=/home/hatch/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh
BIN=/tmp/l3a_clean_bin
SRC=l3a_trace_clean.zag

cd "$D" || exit 1

if [ ! -x "$ZNC" ]; then
  echo "ZNC-MISSING $ZNC" >&2
  exit 1
fi

"$ZNC" "$SRC" -o "$BIN" || { echo "COMPILE-FAIL" >&2; exit 1; }
echo "COMPILE-OK"

"$BIN" > run1.log 2> run1.err; c1=$?
"$BIN" > run2.log 2> run2.err; c2=$?
"$BIN" > run3.log 2> run3.err; c3=$?
echo "exit codes: $c1 $c2 $c3"
if [ "$c1" != "0" ] || [ "$c2" != "0" ] || [ "$c3" != "0" ]; then
  echo "EXIT-NONZERO" >&2
  exit 1
fi

if cmp -s run1.log run2.log && cmp -s run2.log run3.log; then
  echo "DET-OK 3/3 byte-identical stdout"
else
  echo "DET-FAIL" >&2
  exit 1
fi

if [ -s run1.err ] || [ -s run2.err ] || [ -s run3.err ]; then
  echo "STDERR-NONEMPTY" >&2
  exit 1
fi
echo "STDERR-EMPTY"

v=$(grep -c "VERDICT L3A-TRACE-CLEAN-BUILD-PASS" run1.log)
if [ "$v" = "1" ]; then
  echo "VERDICT-OK L3A-TRACE-CLEAN-BUILD-PASS"
else
  echo "VERDICT-FAIL" >&2
  grep "VERDICT" run1.log >&2
  exit 1
fi

sh "$SNIP" "$SRC" NAMECHECK.md PREREG_NOTE.md L3A_TRACE_CLEAN_RESULT.md run_clean.sh \
  && echo "DASH-OK"

sha256sum run1.log run2.log run3.log
echo "RUN-CLEAN-DONE"
