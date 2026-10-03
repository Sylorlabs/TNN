#!/usr/bin/env bash
# RT-2 DEFENSE trial runner — corroborated-elimination defense vs the R3
# spoof schedule (D3) + genuine-shift control (D3b).
# Static gates -> compile -> 2 runs (byte-identical) -> RT2D_CHECK lines.
# Usage: ./run_rt2d.sh [ZNC]
set -u
BASE="$(cd "$(dirname "$0")" && pwd)"
ZNC="${1:-${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}}"
BIN="$BASE/rt2_dtrial_linux"
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
E="$BASE/../evidence/EVIDENCE_RT2D_$STAMP"
mkdir -p "$E"

# Static check 1: no RNG token in any defense-trial decision path.
if grep -nEi 'rng|rand\(|srand|random' "$BASE"/rt2_def.zag "$BASE"/rt2_dtrial.zag "$BASE"/rt2_common.zag | grep -vE ':[0-9]+:[[:space:]]*//'; then
  echo "STATIC CHECK FAILED: RNG token in defense trial source"
  exit 1
fi
echo "static_no_rng=pass"

# Static check 2: the defended substrate keeps the structural guarantee —
# action selection takes no signal parameter and its region carries no
# signal token (same bar as wave4 scaffold-release).
if grep -n 'signal' "$BASE/rt2_def.zag" | sed -n '/SELECT-REGION-BEGIN/,/SELECT-REGION-END/p' | grep -q .; then
  :
fi
python3 - "$BASE/rt2_def.zag" <<'EOF'
import sys, re
s=open(sys.argv[1]).read()
a=s.index('// SELECT-REGION-BEGIN'); b=s.index('// SELECT-REGION-END')
region=s[a:b]
# strip // comments: the guarantee is about code, not prose
code="\n".join(line.split('//')[0] for line in region.splitlines())
assert 'signal' not in code, "signal token inside select region code"
print("static_select_no_signal=pass")
EOF

cp "$BASE"/rt2_def.zag "$BASE"/rt2_dtrial.zag "$BASE"/rt2_common.zag "$E/"

"$ZNC" "$BASE/rt2_dtrial.zag" --no-zagd --no-analyze --no-foreground-cache -o "$BIN" \
  >"$E/compile.stdout" 2>"$E/compile.stderr"
ec=$?
echo "compile_exit=$ec"
if [ $ec -ne 0 ]; then echo "COMPILE FAILED"; tail -30 "$E/compile.stderr"; exit 1; fi

"$BIN" >"$E/run1.stdout" 2>"$E/run1.stderr"
ec1=$?
"$BIN" >"$E/run2.stdout" 2>"$E/run2.stderr"
ec2=$?
echo "run1_exit=$ec1 run2_exit=$ec2"
if ! cmp -s "$E/run1.stdout" "$E/run2.stdout"; then
  echo "DETERMINISM FAILED: run outputs differ"; exit 1
fi
echo "determinism=byte-identical"
cat "$E/run1.stdout"

bad=0; total=0
while IFS=, read -r tag name actual expected; do
  total=$((total+1))
  if [ "$actual" != "$expected" ]; then
    echo "MISMATCH: $name actual=$actual expected=$expected"
    bad=$((bad+1))
  fi
done < <(grep '^RT2D_CHECK,' "$E/run1.stdout")
echo "checks_total=$total checks_bad=$bad"
grep -E '^RT2D_VERDICT,' "$E/run1.stdout" | tee "$E/summary.txt"
(cd "$E" && sha256sum run1.stdout run2.stdout rt2_def.zag rt2_dtrial.zag rt2_common.zag > SHA256SUMS)
if [ "$bad" -ne 0 ] || [ "$ec1" -ne 0 ]; then echo "DEFENSE TRIAL FAILED"; exit 1; fi
echo "DEFENSE TRIAL PASSED"
