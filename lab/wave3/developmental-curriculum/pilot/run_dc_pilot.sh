#!/usr/bin/env bash
# DC-1 pilot runner — compiles the developmental-curriculum Stage-1 pilot
# natively, runs both scale legs (s1, s4) twice each (P5 determinism:
# byte-identical stdout), and verifies every CL_CHECK line has
# actual==expected. Usage: ./run_dc_pilot.sh [ZNC]
set -u
BASE="$(cd "$(dirname "$0")" && pwd)"
ZNC="${1:-${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}}"
BIN="$BASE/dc_pilot_linux"
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
E="$BASE/EVIDENCE_$STAMP"
mkdir -p "$E"
echo "znc=$ZNC" > "$E/compile.command"
echo "znc dc_pilot.zag --no-zagd --no-analyze --no-foreground-cache -o dc_pilot_linux" >> "$E/compile.command"

"$ZNC" "$BASE/dc_pilot.zag" --no-zagd --no-analyze --no-foreground-cache -o "$BIN" \
  >"$E/compile.stdout" 2>"$E/compile.stderr"
ec=$?
echo "compile_exit=$ec"
if [ $ec -ne 0 ]; then echo "COMPILE FAILED"; tail -30 "$E/compile.stderr"; exit 1; fi
sha256sum "$ZNC" "$BASE/dc_pilot.zag" "$BASE/dc_ctx_core.zag" "$BIN" > "$E/SHA256SUMS"

fail=0
for leg in s1 s4; do
  "$BIN" "$leg" >"$E/run_${leg}_1.stdout" 2>"$E/run_${leg}_1.stderr"; ec1=$?
  "$BIN" "$leg" >"$E/run_${leg}_2.stdout" 2>"$E/run_${leg}_2.stderr"; ec2=$?
  echo "leg=$leg run1_exit=$ec1 run2_exit=$ec2"
  if ! cmp -s "$E/run_${leg}_1.stdout" "$E/run_${leg}_2.stdout"; then
    echo "P5 DETERMINISM FAILED ($leg): run outputs differ"; fail=1
  else
    echo "leg=$leg determinism=byte-identical"
  fi
  bad=0; total=0
  while IFS=, read -r tag name actual expected; do
    total=$((total+1))
    if [ "$actual" != "$expected" ]; then
      echo "MISMATCH ($leg): $name actual=$actual expected=$expected"
      bad=$((bad+1))
    fi
  done < <(grep '^CL_CHECK,' "$E/run_${leg}_1.stdout")
  echo "leg=$leg checks_total=$total checks_bad=$bad"
  grep -E '^DC_FAILURES,' "$E/run_${leg}_1.stdout"
  if [ "$bad" -ne 0 ] || [ "$ec1" -ne 0 ]; then echo "LEG $leg FAILED"; fail=1; fi
  (cd "$E" && sha256sum "run_${leg}_1.stdout" "run_${leg}_2.stdout" >> SHA256SUMS)
done

cat > "$E/RECEIPT.txt" <<EOF
DC-1 pilot receipt
stamp=$STAMP (UTC)
compiler_sha256=$(sha256sum "$ZNC" | cut -d' ' -f1)
binary_sha256=$(sha256sum "$BIN" | cut -d' ' -f1)
legs=s1 s4 (each run twice; P5 determinism via cmp)
result_fail=$fail
EOF
if [ "$fail" -ne 0 ]; then echo "PILOT FAILED"; exit 1; fi
echo "PILOT PASSED"
