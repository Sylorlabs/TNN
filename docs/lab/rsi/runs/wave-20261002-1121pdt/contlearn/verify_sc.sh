#!/bin/sh
# verify_sc.sh -- frozen verification for the scheduling exercise (b).
# Prints PASS/FAIL lines. Exits 0 only if every bar passes.
set -u
export PATH="$HOME/safebin"
D="/home/hatch/workspace/tnn-rsi-work/wave-20261002-1121pdt/contlearn/docs/lab/rsi/runs/wave-20261002-1121pdt/contlearn"
cd "$D"
FAIL=0
chk() {
  if [ "$2" = "$3" ]; then echo "PASS $1 (=$2)"; else echo "FAIL $1 (got=$2 want=$3)"; FAIL=1; fi
}
echo "--- B-S0 treat_a: fire unccount=3, 1 PROPOSAL(r=850), episode MAP ---"
for r in 1 2 3; do
  f="out_sc_treat_a_r${r}.txt"
  chk "B-S0[$r] sched_fire" "$(grep -c 'SCHED_FIRE unccount=3 evidx=5 s=98301' $f)" 1
  chk "B-S0[$r] proposal850" "$(grep -c 'PROPOSAL s=[0-9]* r=850 ' $f)" 1
  chk "B-S0[$r] episode_ok" "$(grep -c 'EPISODE_OK 1/1' $f)" 1
  # ans=98321 appears in both the MACHINERY line and the EV line; the bar
  # is that the episode query is answered 98321 (present, correct).
  if grep -q 'ans=98321' "$f"; then echo "PASS B-S0[$r] ans98321 (present)"; else echo "FAIL B-S0[$r] ans98321 (absent)"; FAIL=1; fi
done
echo "--- B-S0 treat_b: fire unccount=3, 1 PROPOSAL(r=850), episode MAP ---"
for r in 1 2 3; do
  f="out_sc_treat_b_r${r}.txt"
  chk "B-S0[$r] sched_fire" "$(grep -c 'SCHED_FIRE unccount=3 evidx=83 s=98301' $f)" 1
  chk "B-S0[$r] proposal850" "$(grep -c 'PROPOSAL s=[0-9]* r=850 ' $f)" 1
  chk "B-S0[$r] episode_ok" "$(grep -c 'EPISODE_OK 1/1' $f)" 1
  if grep -q 'ans=98321' "$f"; then echo "PASS B-S0[$r] ans98321 (present)"; else echo "FAIL B-S0[$r] ans98321 (absent)"; FAIL=1; fi
done
echo "--- B-S1 crux: |evidx_A - evidx_B| = 78 >= 50 ---"
for r in 1 2 3; do
  ea=$(grep -o 'evidx=[0-9]*' "out_sc_treat_a_r${r}.txt" | head -1 | cut -d= -f2)
  eb=$(grep -o 'evidx=[0-9]*' "out_sc_treat_b_r${r}.txt" | head -1 | cut -d= -f2)
  diff=$((eb - ea))
  chk "B-S1[$r] evidx_a" "$ea" 5
  chk "B-S1[$r] evidx_b" "$eb" 83
  chk "B-S1[$r] separation" "$diff" 78
done
echo "--- B-S3 costume: fires at evidx 12 in both, counts 4 vs 0 ---"
for r in 1 2 3; do
  fa="out_sc_costume_a_r${r}.txt"; fb="out_sc_costume_b_r${r}.txt"
  chk "B-S3[$r] costume_a fire" "$(grep -c 'SCHED_FIRE unccount=4 evidx=12 s=98301' $fa)" 1
  chk "B-S3[$r] costume_b fire" "$(grep -c 'SCHED_FIRE unccount=0 evidx=12 s=98301' $fb)" 1
  chk "B-S3[$r] costume_a proposal850" "$(grep -c 'PROPOSAL s=[0-9]* r=850 ' $fa)" 1
  chk "B-S3[$r] costume_b proposal850" "$(grep -c 'PROPOSAL s=[0-9]* r=850 ' $fb)" 1
done
echo "--- B-S4 determinism: 3x byte-identical per binary ---"
for bin in sc_treat_a sc_treat_b sc_costume_a sc_costume_b; do
  h1=$(sha256sum < "out_${bin}_r1.txt" | cut -d' ' -f1)
  h2=$(sha256sum < "out_${bin}_r2.txt" | cut -d' ' -f1)
  h3=$(sha256sum < "out_${bin}_r3.txt" | cut -d' ' -f1)
  if [ "$h1" = "$h2" ] && [ "$h2" = "$h3" ]; then echo "PASS B-S4[$bin] byte-identical sha=$h1"; else echo "FAIL B-S4[$bin] rep mismatch"; FAIL=1; fi
  v1=$(grep '^FNV ' "out_${bin}_r1.txt"); v2=$(grep '^FNV ' "out_${bin}_r2.txt"); v3=$(grep '^FNV ' "out_${bin}_r3.txt")
  if [ "$v1" = "$v2" ] && [ "$v2" = "$v3" ]; then echo "PASS B-S4[$bin] fnv stable"; else echo "FAIL B-S4[$bin] fnv unstable"; FAIL=1; fi
done
echo "--- B-S4 hygiene: rc 0, stderr 0, AUDIT_PASS, CAP_GUARD_OK, event counts ---"
for bin in sc_treat_a sc_costume_a; do
  for r in 1 2 3; do
    f="out_${bin}_r${r}.txt"; e="err_${bin}_r${r}.txt"
    chk "B-S4[$bin r$r] audit" "$(grep -c 'AUDIT_PASS' $f)" 1
    chk "B-S4[$bin r$r] cap" "$(grep -c 'CAP_GUARD_OK' $f)" 1
    chk "B-S4[$bin r$r] stderr" "$(wc -c < $e)" 0
    chk "B-S4[$bin r$r] ev20" "$(grep -c '^EV ' $f)" 20
  done
done
for bin in sc_treat_b sc_costume_b; do
  for r in 1 2 3; do
    f="out_${bin}_r${r}.txt"; e="err_${bin}_r${r}.txt"
    chk "B-S4[$bin r$r] audit" "$(grep -c 'AUDIT_PASS' $f)" 1
    chk "B-S4[$bin r$r] cap" "$(grep -c 'CAP_GUARD_OK' $f)" 1
    chk "B-S4[$bin r$r] stderr" "$(wc -c < $e)" 0
    chk "B-S4[$bin r$r] ev96" "$(grep -c '^EV ' $f)" 96
  done
done
echo "--- K1b: znc log 7 pre-run builds, 0 during runs ---"
chk "K1b log_lines" "$(wc -l < znc_invocations_sc.log)" 7
echo "--- B-S2/K2: driver audit (0 pf_propose/pf_find CALLS in drivers; comments excluded) ---"
for d in sc_driver_a.zag sc_driver_b.zag; do
  chk "B-S2[$d] pf_propose" "$(grep -v '^[[:space:]]*//' $d | grep -c 'pf_propose')" 0
  chk "B-S2[$d] pf_find" "$(grep -v '^[[:space:]]*//' $d | grep -c 'pf_find')" 0
done
echo "--- K3 attribution already recorded; re-confirming totals ---"
for b in k3_scb k3_sct k3_scc; do
  PATH="$HOME/safebin" bash -c "exec -c ./$b" 2>/dev/null | grep -E "^TOTAL" | tr '\n' ' '
  echo "<- $b"
done
if [ $FAIL -eq 0 ]; then echo "ALL SEALED CHECKS PASS"; else echo "SEALED CHECKS FAILED"; fi
exit $FAIL
