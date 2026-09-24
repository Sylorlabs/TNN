#!/bin/bash
# run.sh — WORKSTREAM D three-worlds battery: rebuild from scratch,
# run twice, verify byte-identical reruns, verify against the frozen table.
# Usage: ./run.sh   (from this directory)
set -e
ZNC="$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1"
TMPD="$HOME/workspace/tmp_commit"
mkdir -p "$TMPD"
echo "== compile =="
"$ZNC" tw.zag -o tw_run 2>&1 | grep -E "error|wrote" || true
echo "== run 1 =="
./tw_run > "$TMPD/tw_check1.txt"
echo "== run 2 =="
./tw_run > "$TMPD/tw_check2.txt"
echo "== determinism (K5) =="
sha256sum "$TMPD/tw_check1.txt" "$TMPD/tw_check2.txt"
cmp "$TMPD/tw_check1.txt" "$TMPD/tw_check2.txt" && echo "K5 PASS: byte-identical"
echo "== verify vs frozen table =="
python3 verify.py "$TMPD/tw_check1.txt"
echo "== done =="
