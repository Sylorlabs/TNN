#!/bin/bash
# B-battery driver for arm T adjudication (marathon crew U10).
# Runs batt_bin for (t,x) x (prose,code), N=5 reruns each; requires
# byte-identical stdout per config (B7 determinism gate); then emits
# verdict ratios. Exits nonzero on any determinism failure.
set -u
cd "$(dirname "$0")"
BIN=./batt_bin
CORP=~/workspace/tnn-lab/corpora
[ -x "$BIN" ] || { echo "FATAL: $BIN missing; build first"; exit 2; }

declare -A DIGESTS
fail=0
for arm in t x; do
  for corp in prose code; do
    if [ "$corp" = prose ]; then path="$CORP/pg100.txt"; else path="$CORP/sqlite3.c"; fi
    for r in 1 2 3 4 5; do
      out="ev_${arm}_${corp}_r${r}.txt"
      "$BIN" "$arm" "$path" "$corp" > "$out" || { echo "FATAL: run failed $out"; exit 2; }
      h=$(sha256sum "$out" | cut -d' ' -f1)
      key="${arm}_${corp}"
      if [ "$r" = 1 ]; then DIGESTS[$key]="$h"; else
        if [ "${DIGESTS[$key]}" != "$h" ]; then
          echo "DETERMINISM FAIL: $out digest $h != ${DIGESTS[$key]}"; fail=1
        fi
      fi
    done
    echo "config ${arm}/${corp}: 5 runs byte-identical (sha256 ${DIGESTS[${arm}_${corp}]})"
  done
done
[ "$fail" = 1 ] && { echo "B7 GATE: FAIL"; exit 1; }
echo "B7 GATE: PASS (all 20 runs byte-identical within config)"

# verdict ratios via python3 (exact rational arithmetic)
python3 - <<'EOF'
import re
def load(arm, corp):
    d = {}
    with open(f"ev_{arm}_{corp}_r1.txt") as f:
        for line in f:
            m = re.match(r"([a-z0-9_]+)=(\d+)", line.strip())
            if m: d[m.group(1)] = int(m.group(2))
    return d
out = []
for corp in ("prose", "code"):
    T, X = load("t", corp), load("x", corp)
    b2t, b2x = T["b2_mat"]/T["b2_rec"], X["b2_mat"]/X["b2_rec"]
    b4t, b4x = T["b4_served"]/T["b4_total"], X["b4_served"]/X["b4_total"]
    b5t, b5x = T["b5_rekeyed"]/T["b5_edits"], X["b5_rekeyed"]/X["b5_edits"]
    b9t, b9x = T["b9_mat"]/T["b9_rec"], X["b9_mat"]/X["b9_rec"]
    sub = T["subep"]/T["totalq"]
    out.append(f"== {corp} (n_T={T['n']} n_X={X['n']}) ==")
    out.append(f"B1: T {T['b1_ok']}/{T['b1_total']}  X {X['b1_ok']}/{X['b1_total']}")
    out.append(f"B2 cost/byte: T={b2t:.4f} X={b2x:.4f} ratio_T/X={b2t/b2x:.6f}  kill(i) fires if ratio<=2")
    out.append(f"B4 reuse: T={b4t:.4f} X={b4x:.4f}  T_beats_X={b4t>b4x}")
    out.append(f"B5 rekeyed/edit: T={b5t:.1f} X={b5x:.1f}  T_beats_X={b5t<b5x}")
    out.append(f"B9 cost/byte: T={b9t:.4f} X={b9x:.4f} ok T {T['b9_ok']}/{T['b9_total']} X {X['b9_ok']}/{X['b9_total']}  T_beats_X={b9t<b9x}")
    out.append(f"(ii) sub-episode query fraction (T): {sub:.4f}  fires if >0.80")
    # kill evaluation
    k1 = (b2t/b2x) <= 2.0
    k2 = sub > 0.80
    beats = {"B2": b2t < b2x, "B4": b4t > b4x, "B5": b5t < b5x, "B9": b9t < b9x}
    k4 = not all(beats.values())
    out.append(f"KILL (i) B2 within 2x of X: {'FIRES' if k1 else 'no'}")
    out.append(f"KILL (ii) >80% sub-episode: {'FIRES' if k2 else 'no'}")
    out.append(f"KILL (iv) floor (must beat X on B2/B4/B5/B9): {'FIRES' if k4 else 'no'}  beats={beats}")
    out.append("")
with open("VERDICT_NUMBERS.txt", "w") as f:
    f.write("\n".join(out) + "\n")
print("\n".join(out))
EOF
