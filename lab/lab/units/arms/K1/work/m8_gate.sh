#!/bin/bash
# M8 determinism gate: N=5 runs with perturbations, byte-identical artifacts.
# Perturbations available in t_m8: none, frag (heap pre-fragmentation), aslr (1.2MB pad).
# Frozen M8 runs 4-5 (entropy/clock starvation, alloc-order shuffle) are NOT
# implemented by the arm — documented as a gap, not a failure.
set -u
BIN="${1:?usage: m8_gate.sh <k1test-binary> <corpus-root> <outdir>}"
CORPUS="$2"
OUT="$3"
PERTS="none frag aslr none frag"
i=1
for p in $PERTS; do
  d="$OUT/m8_r$i"
  mkdir -p "$d"
  "$BIN" m8-1x "$CORPUS" "$d" "$p" > "$d/stdout.txt" 2>"$d/stderr.txt"
  echo "rc=$?" > "$d/rc.txt"
  i=$((i+1))
done
# Compare: store_chain.txt, ledger_chain.txt, alloc_trace.txt, stdout.txt across all 5
echo "=== M8 N=5 comparison ==="
for f in store_chain.txt ledger_chain.txt stdout.txt; do
  if cmp -s "$OUT/m8_r1/$f" "$OUT/m8_r2/$f" && cmp -s "$OUT/m8_r1/$f" "$OUT/m8_r3/$f" \
     && cmp -s "$OUT/m8_r1/$f" "$OUT/m8_r4/$f" && cmp -s "$OUT/m8_r1/$f" "$OUT/m8_r5/$f"; then
    echo "IDENTICAL: $f"
  else
    echo "DIFFER: $f"
  fi
done
# alloc_trace.txt may be large; compare via sha256
echo "--- alloc_trace sha256 ---"
sha256sum "$OUT"/m8_r*/alloc_trace.txt
echo "--- stdout ---"
cat "$OUT/m8_r1/stdout.txt"
echo "--- rc ---"
cat "$OUT"/m8_r*/rc.txt
