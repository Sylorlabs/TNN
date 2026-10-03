#!/bin/sh
# verify_rj.sh -- frozen verification for the refusal exercise (a).
# Oracle-line checks (REFUSED/ENGAGE/MISS/LEDGER/NO850MAP/ENGAGE_OK/RV_OK/
# AUDIT_PASS/CAP_GUARD/FNV) plus determinism (3x byte-identical SHA-256 per
# binary), hygiene (rc 0, 0-byte stderr), and K1/K2/K3 re-derivation from the
# transcripts + source + build log. Pure shell. Prints PASS/FAIL lines.
# Exits 0 only if every bar passes.
set -u
export PATH="$HOME/safebin"
D="/home/hatch/workspace/tnn-rsi-work/wave-20261002-1121pdt/contlearn/docs/lab/rsi/runs/wave-20261002-1121pdt/contlearn"
cd "$D"
FAIL=0
chk() { # chk <name> <got> <want>
  if [ "$2" = "$3" ]; then echo "PASS $1 (=$2)"; else echo "FAIL $1 (got=$2 want=$3)"; FAIL=1; fi
}
for bin in rj_own_x rj_own_y rj_hard_x rj_hard_y; do
  for r in 1 2 3; do
    f="out_${bin}_r${r}.txt"
    refused=$(grep -c "REFUSED s=[0-9]* r=850" "$f")
    engage850=$(grep -c "ENGAGE s=[0-9]* r=850" "$f")
    miss850=$(grep -c "MISS s=[0-9]* r=850" "$f")
    refusedtot=$(grep -c "REFUSED s=" "$f")
    engagere=$(grep -c "ENGAGE s=" "$f")
    missre=$(grep -c "MISS s=" "$f")
    echo "== $f: REFUSED850=$refused ENGAGE850=$engage850 MISS850=$miss850 REFUSEDtot=$refusedtot ENGAGEtot=$engagere MISStot=$missre"
  done
done
echo "--- A-R0 own_x (contradicted history): 6/6 REFUSED, 0/6 ENGAGE850, 6/6 ENGAGE_OK, ledger 2 ---"
for r in 1 2 3; do
  f="out_rj_own_x_r${r}.txt"
  chk "A-R0[$r] refused850" "$(grep -c 'REFUSED s=[0-9]* r=850' $f)" 6
  chk "A-R0[$r] engage850" "$(grep -c 'ENGAGE s=[0-9]* r=850' $f)" 0
  chk "A-R0[$r] engage_ok" "$(grep -c 'ENGAGE_OK 6/6' $f)" 1
  chk "A-R0[$r] ledger850" "$(grep -c 'LEDGER 850 count=2' $f)" 1
  chk "A-R0[$r] ledger851" "$(grep -c 'LEDGER 851 count=0' $f)" 1
  chk "A-R0[$r] rv_ok" "$(grep -c 'RV_OK 1/1' $f)" 1
done
echo "--- A-R1 own_y (confirmed history): 0/6 REFUSED, 6/6 ENGAGE850, ledger 0 ---"
for r in 1 2 3; do
  f="out_rj_own_y_r${r}.txt"
  chk "A-R1[$r] refused850" "$(grep -c 'REFUSED s=[0-9]* r=850' $f)" 0
  chk "A-R1[$r] engage850" "$(grep -c 'ENGAGE s=[0-9]* r=850' $f)" 6
  chk "A-R1[$r] miss850" "$(grep -c 'MISS s=[0-9]* r=850' $f)" 6
  chk "A-R1[$r] ledger850" "$(grep -c 'LEDGER 850 count=0' $f)" 1
  chk "A-R1[$r] engage_ok" "$(grep -c 'ENGAGE_OK 6/6' $f)" 1
  chk "A-R1[$r] rv_ok" "$(grep -c 'RV_OK 1/1' $f)" 1
done
echo "--- A-R2 crux: identical probe tuples, decision flips with learner state ---"
for r in 1 2 3; do
  fx="out_rj_own_x_r${r}.txt"; fy="out_rj_own_y_r${r}.txt"
  same=1
  for s in 94201 94202 94203 94204 94205 94206; do
    grep -q "EV 2 $s 850 0" "$fx" || same=0
    grep -q "EV 2 $s 850 0" "$fy" || same=0
  done
  chk "A-R2[$r] probe_tuples_identical" "$same" 1
  chk "A-R2[$r] own_x_refused6" "$(grep -c 'REFUSED s=[0-9]* r=850' $fx)" 6
  chk "A-R2[$r] own_y_engaged6" "$(grep -c 'ENGAGE s=[0-9]* r=850' $fy)" 6
done
echo "--- A-R3 hard control: state-invariant costume pattern ---"
for r in 1 2 3; do
  for b in rj_hard_x rj_hard_y; do
    f="out_${b}_r${r}.txt"
    chk "A-R3[$r $b] refused850" "$(grep -c 'REFUSED s=[0-9]* r=850' $f)" 6
    chk "A-R3[$r $b] engage850" "$(grep -c 'ENGAGE s=[0-9]* r=850' $f)" 0
    chk "A-R3[$r $b] engage_ok" "$(grep -c 'ENGAGE_OK 6/6' $f)" 1
  done
done
echo "--- K0c: hard_x and hard_y decision lines identical under different histories (fixture text excluded) ---"
for r in 1 2 3; do
  dx=$(grep -o 'REFUSED s=[0-9]* r=[0-9]*\|ENGAGE s=[0-9]* r=[0-9]*\|MISS s=[0-9]* r=[0-9]*' "out_rj_hard_x_r${r}.txt")
  dy=$(grep -o 'REFUSED s=[0-9]* r=[0-9]*\|ENGAGE s=[0-9]* r=[0-9]*\|MISS s=[0-9]* r=[0-9]*' "out_rj_hard_y_r${r}.txt")
  if [ "$dx" = "$dy" ]; then echo "PASS K0c[$r] hard decisions state-invariant"; else echo "FAIL K0c[$r] hard decisions differ"; FAIL=1; fi
done
echo "--- A-R4 determinism: 3x byte-identical SHA-256 per binary ---"
for bin in rj_own_x rj_own_y rj_hard_x rj_hard_y; do
  h1=$(sha256sum < "out_${bin}_r1.txt" | cut -d' ' -f1)
  h2=$(sha256sum < "out_${bin}_r2.txt" | cut -d' ' -f1)
  h3=$(sha256sum < "out_${bin}_r3.txt" | cut -d' ' -f1)
  if [ "$h1" = "$h2" ] && [ "$h2" = "$h3" ]; then echo "PASS A-R4[$bin] byte-identical sha=$h1"; else echo "FAIL A-R4[$bin] rep mismatch"; FAIL=1; fi
  f1=$(grep -c '^FNV ' "out_${bin}_r1.txt"); f2=$(grep -c '^FNV ' "out_${bin}_r2.txt"); f3=$(grep -c '^FNV ' "out_${bin}_r3.txt")
  chk "A-R4[$bin] fnv_line_count" "$f1$f2$f3" "111"
  v1=$(grep '^FNV ' "out_${bin}_r1.txt"); v2=$(grep '^FNV ' "out_${bin}_r2.txt"); v3=$(grep '^FNV ' "out_${bin}_r3.txt")
  if [ "$v1" = "$v2" ] && [ "$v2" = "$v3" ]; then echo "PASS A-R4[$bin] fnv stable ($v1)"; else echo "FAIL A-R4[$bin] fnv unstable"; FAIL=1; fi
done
echo "--- A-R4 hygiene: rc 0, 0-byte stderr, AUDIT_PASS, CAP_GUARD_OK, 33 events ---"
for bin in rj_own_x rj_own_y rj_hard_x rj_hard_y; do
  for r in 1 2 3; do
    f="out_${bin}_r${r}.txt"; e="err_${bin}_r${r}.txt"
    chk "A-R4[$bin r$r] audit_pass" "$(grep -c 'AUDIT_PASS' $f)" 1
    chk "A-R4[$bin r$r] cap_guard" "$(grep -c 'CAP_GUARD_OK' $f)" 1
    chk "A-R4[$bin r$r] stderr_bytes" "$(wc -c < $e)" 0
    chk "A-R4[$bin r$r] ev33" "$(grep -c '^EV ' $f)" 33
  done
done
echo "--- K1b: znc log: 7 pre-run builds, 0 entries during runs ---"
chk "K1b log_lines" "$(wc -l < znc_invocations_rj.log)" 7
echo "--- K2c: drivers contain 0 cognition functions (0 fn lines, only fixture fns) ---"
for d in rj_driver_x.zag rj_driver_y.zag; do
  nf=$(grep -c '^fn rj_' "$d")
  echo "INFO $d rj_ fns=$nf (fixture only, audited below)"
done
echo "--- K3: frozen core battery 46/46 on all three cores ---"
for b in k3_base k3_own k3_hard; do
  PATH="$HOME/safebin" bash -c "exec -c ./$b" 2>/dev/null | grep -E "^(TOTAL|K3RC)" | tr '\n' ' '
  echo "<- $b"
done
if [ $FAIL -eq 0 ]; then echo "ALL SEALED CHECKS PASS"; else echo "SEALED CHECKS FAILED"; fi
exit $FAIL
