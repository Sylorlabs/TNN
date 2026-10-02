#!/bin/sh
# verify_xk.sh -- frozen verification for the cross-kind rebind (c).
# Prints PASS/FAIL lines. Exits 0 only if every bar passes.
set -u
export PATH="$HOME/safebin"
D="/home/hatch/workspace/tnn-rsi-work/wave-20261002-1121pdt/contlearn/docs/lab/rsi/runs/wave-20261002-1121pdt/contlearn"
cd "$D"
FAIL=0
chk() {
  if [ "$2" = "$3" ]; then echo "PASS $1 (=$2)"; else echo "FAIL $1 (got=$2 want=$3)"; FAIL=1; fi
}
echo "--- C-R0/C-R1/C-R2/C-R4 full battery ---"
for r in 1 2 3; do
  f="out_xk_full_r${r}.txt"
  chk "C-R0[$r] countmap" "$(grep -c 'COUNTMAP_OK 6/6' $f)" 1
  chk "C-R1[$r] chainmap" "$(grep -c 'CHAINMAP_OK 6/6' $f)" 1
  chk "C-R2[$r] sig_count" "$(grep -c 'SIG_COUNT_OK 6/6' $f)" 1
  chk "C-R2[$r] sig_rebind" "$(grep -c 'SIG_REBIND_OK 6/6' $f)" 1
  chk "C-R4[$r] retention" "$(grep -c 'RETENTION_OK 6/6' $f)" 1
  chk "C-R4[$r] factstable" "$(grep -c 'FACTSTABLE 18/18' $f)" 1
done
echo "--- C-R3 control ---"
for r in 1 2 3; do
  f="out_xk_nophase_r${r}.txt"
  chk "C-R3[$r] miss" "$(grep -c 'CONTROL_MISS_OK 6/6' $f)" 1
  chk "C-R3[$r] nomap" "$(grep -c 'CONTROL_NOMAP 6/6' $f)" 1
done
echo "--- C-R5 determinism ---"
for bin in xk_full xk_nophase; do
  h1=$(sha256sum < "out_${bin}_r1.txt" | cut -d' ' -f1)
  h2=$(sha256sum < "out_${bin}_r2.txt" | cut -d' ' -f1)
  h3=$(sha256sum < "out_${bin}_r3.txt" | cut -d' ' -f1)
  if [ "$h1" = "$h2" ] && [ "$h2" = "$h3" ]; then echo "PASS C-R5[$bin] byte-identical sha=$h1"; else echo "FAIL C-R5[$bin] rep mismatch"; FAIL=1; fi
  v1=$(grep '^FNV ' "out_${bin}_r1.txt"); v2=$(grep '^FNV ' "out_${bin}_r2.txt"); v3=$(grep '^FNV ' "out_${bin}_r3.txt")
  if [ "$v1" = "$v2" ] && [ "$v2" = "$v3" ]; then echo "PASS C-R5[$bin] fnv stable"; else echo "FAIL C-R5[$bin] fnv unstable"; FAIL=1; fi
done
echo "--- C-R5 hygiene ---"
for r in 1 2 3; do
  f="out_xk_full_r${r}.txt"; e="err_xk_full_r${r}.txt"
  chk "C-R5[full r$r] audit" "$(grep -c 'AUDIT_PASS' $f)" 1
  chk "C-R5[full r$r] cap" "$(grep -c 'CAP_GUARD_OK' $f)" 1
  chk "C-R5[full r$r] stderr" "$(wc -c < $e)" 0
  chk "C-R5[full r$r] ev99" "$(grep -c '^EV ' $f)" 99
  f="out_xk_nophase_r${r}.txt"; e="err_xk_nophase_r${r}.txt"
  chk "C-R5[nophase r$r] audit" "$(grep -c 'AUDIT_PASS' $f)" 1
  chk "C-R5[nophase r$r] cap" "$(grep -c 'CAP_GUARD_OK' $f)" 1
  chk "C-R5[nophase r$r] stderr" "$(wc -c < $e)" 0
  chk "C-R5[nophase r$r] ev69" "$(grep -c '^EV ' $f)" 69
done
chk "K1b log_lines" "$(wc -l < znc_invocations_xk.log)" 2
if [ $FAIL -eq 0 ]; then echo "ALL SEALED CHECKS PASS"; else echo "SEALED CHECKS FAILED"; fi
exit $FAIL
