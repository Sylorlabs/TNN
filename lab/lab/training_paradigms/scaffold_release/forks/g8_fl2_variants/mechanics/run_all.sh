#!/bin/bash
# run_all.sh — G8 FL2 mechanics trials runner.
# Builds each variant for WORLD=0,1,2,3 (RT binaries via sed-swap, not committed),
# runs each twice, verifies byte-identical SHA256, saves outputs.
# Usage: ./run_all.sh [outdir]
set -u
MECH="$(cd "$(dirname "$0")" && pwd)"
ZNC="$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1"
OUT="${1:-$MECH/evidence}"
mkdir -p "$OUT"
# temp sed-swapped sources are build artifacts; never commit them
trap 'rm -f "$MECH"/.tmp_v_*_w*.zag' EXIT
VARIANTS="c1 a0 a1 a2 a3 b1 b2 c2 c3 c4"
WORLDS="0 1 2 3"
FAIL=0
for v in $VARIANTS; do
  for w in $WORLDS; do
    tag="v_${v}_w${w}"
    src="$MECH/v_${v}.zag"
    # sed-swap WORLD const into a temp build file beside g8base.zag
    # (@import is relative); removed by trap on exit. Not committed.
    buildsrc="$MECH/.tmp_${tag}.zag"
    sed "s/const WORLD:i32=0;/const WORLD:i32=${w};/" "$src" > "$buildsrc"
    if ! grep -q "const WORLD:i32=${w};" "$buildsrc"; then
      echo "WORLD swap failed for $tag" >&2; FAIL=1; continue
    fi
    bin="/tmp/g8_${tag}"
    if ! "$ZNC" "$buildsrc" --no-zagd --no-analyze --no-foreground-cache -o "$bin" >/dev/null 2>&1; then
      echo "BUILD FAIL $tag" >&2; FAIL=1; continue
    fi
    "$bin" > "$OUT/${tag}_r1.txt" 2>&1
    "$bin" > "$OUT/${tag}_r2.txt" 2>&1
    s1=$(sha256sum "$OUT/${tag}_r1.txt" | cut -d' ' -f1)
    s2=$(sha256sum "$OUT/${tag}_r2.txt" | cut -d' ' -f1)
    if [ "$s1" != "$s2" ]; then
      echo "NON-DETERMINISTIC $tag" >&2; FAIL=1; continue
    fi
    echo "$s1  ${tag}_r1.txt" >> "$OUT/SHA256SUMS.txt"
    if [ "$w" = "0" ]; then
      tf=$(grep '^TN_FAILURES,' "$OUT/${tag}_r1.txt" | cut -d, -f2)
      echo "$tag: TN_FAILURES=$tf sha=$s1"
      if [ "$tf" != "0" ]; then FAIL=1; fi
    else
      echo "$tag: sha=$s1"
    fi
  done
done
# static checks: forbidden tokens absent from .zag sources
# (no payoff-channel token; no accumulator tokens per prereg §6)
if grep -rqni "rewar[a-z]" "$MECH" --include="*.zag"; then
  echo "FORBIDDEN token found" >&2; FAIL=1
fi
for tok in "csu[m]" "ccn[t]"; do
  if grep -rq "$tok" "$MECH"/v_*.zag "$MECH"/g8base.zag "$MECH"/tn.zag; then
    echo "FORBIDDEN token in variant source" >&2; FAIL=1
  fi
done
exit $FAIL
