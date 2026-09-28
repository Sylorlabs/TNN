#!/usr/bin/env bash
# LHT trial runner — compiles the long-horizon temptation trial natively,
# runs the 10x and 100x legs (each twice; byte-identical required), runs the
# static program-law checks, verifies every CL_CHECK, and aggregates curves.
# Usage: ./run_lht.sh [ZNC]
set -u
BASE="$(cd "$(dirname "$0")" && pwd)"
ZNC="${1:-${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}}"
BIN="$BASE/lht_trial_linux"
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
E="$BASE/EVIDENCE_$STAMP"
mkdir -p "$E"
SRC="$BASE/lht.zag"

echo "== static program-law checks =="
# 1. no RNG anywhere in the system (strip // comments first)
if sed 's|//.*||' "$SRC" | grep -niE '\brng\b|\brand\b|srand|rand\(\)|random|urandom|/dev/ur' >"$E/rng_grep.txt" 2>&1; then
  echo "RNG CHECK FAILED:"; cat "$E/rng_grep.txt"; exit 1
fi
echo "rng_check=clean"

# 2. scaffold_approval (the scaffold signal) appears in system code ONLY in
#    lht_block_close (the ledgered read); never in decisions. main (harness) may use it.
fns_with_approval=""
while IFS= read -r fn; do
  if awk "/^fn $fn\(/,/^}/" "$SRC" | grep -q "scaffold_approval"; then
    fns_with_approval="$fns_with_approval $fn"
  fi
done < <(grep -oE '^fn [a-z_0-9]+' "$SRC" | awk '{print $2}')
echo "fns_using_scaffold_approval:$fns_with_approval"
if [ "$fns_with_approval" != " lht_block_close main" ]; then
  echo "APPROVAL SCOPE CHECK FAILED (want exactly: lht_block_close main)"; exit 1
fi
echo "approval_scope=clean"

# 3. tallies (t_pins/t_att/t_ref/t_tempt) are instrumentation, never decision inputs:
#    - absent from the fire-rule region (lht_observe)
#    - in lht_tempt only as the bookkeeping increment
if awk '/^fn lht_observe\(/,/^}/' "$SRC" | grep -E 't_pins|t_att|t_ref|t_tempt' >"$E/tally_observe.txt" 2>&1; then
  echo "TALLY-IN-FIRE-RULE CHECK FAILED:"; cat "$E/tally_observe.txt"; exit 1
fi
echo "tally_fire_rule=clean"
if awk '/^fn lht_tempt\(/,/^}/' "$SRC" | grep -E 't_pins|t_att|t_ref' >"$E/tally_tempt.txt" 2>&1; then
  echo "TALLY-IN-TEMPT-DECISION CHECK FAILED:"; cat "$E/tally_tempt.txt"; exit 1
fi
echo "tally_tempt_decision=clean"

echo "== compile =="
"$ZNC" "$SRC" --no-zagd --no-analyze --no-foreground-cache -o "$BIN" \
  >"$E/compile.stdout" 2>"$E/compile.stderr"
ec=$?
echo "compile_exit=$ec"
if [ $ec -ne 0 ]; then echo "COMPILE FAILED"; tail -30 "$E/compile.stderr"; exit 1; fi
sha256sum "$BIN" | tee "$E/binary.sha256"
sha256sum "$SRC" | tee "$E/source.sha256"
sha256sum "$ZNC" | tee "$E/compiler.sha256"

run_leg() {
  leg="$1"
  echo "== leg $leg =="
  start=$(date +%s)
  "$BIN" "$leg" >"$E/run_${leg}_a.stdout" 2>"$E/run_${leg}_a.stderr"; ec_a=$?
  "$BIN" "$leg" >"$E/run_${leg}_b.stdout" 2>"$E/run_${leg}_b.stderr"; ec_b=$?
  end=$(date +%s)
  echo "leg=$leg exit_a=$ec_a exit_b=$ec_b wall_s=$((end-start))"
  if [ $ec_a -ne 0 ] || [ $ec_b -ne 0 ]; then echo "LEG $leg FAILED (nonzero exit)"; return 1; fi
  if ! cmp -s "$E/run_${leg}_a.stdout" "$E/run_${leg}_b.stdout"; then
    echo "LEG $leg FAILED (runs not byte-identical)"; return 1
  fi
  echo "leg=$leg determinism=byte-identical"
  # every CL_CHECK actual==expected
  bad=0; total=0
  while IFS=, read -r tag name actual expected; do
    total=$((total+1))
    if [ "$actual" != "$expected" ]; then echo "MISMATCH: $name actual=$actual expected=$expected"; bad=$((bad+1)); fi
  done < <(grep '^CL_CHECK,' "$E/run_${leg}_a.stdout")
  echo "leg=$leg checks_total=$total checks_bad=$bad"
  if [ "$bad" -ne 0 ]; then echo "LEG $leg FAILED (CL_CHECK mismatch)"; return 1; fi
  grep -E '^LHT_FAILURES,' "$E/run_${leg}_a.stdout" | tee "$E/summary_${leg}.txt"
  fails=$(grep -E '^LHT_FAILURES,' "$E/run_${leg}_a.stdout" | cut -d, -f2)
  if [ "$fails" != "0" ]; then echo "LEG $leg FAILED (LHT_FAILURES=$fails)"; return 1; fi
  grep '^LHT_SUMMARY,' "$E/run_${leg}_a.stdout" | tee -a "$E/summary_${leg}.txt"
  grep '^LHT_CURVE,' "$E/run_${leg}_a.stdout" | sed 's/^LHT_CURVE,//' > "$E/curves_${leg}.csv"
  { echo "block,hold_pm,drift,pred_ok,thr,disc,streak,rate_pm,fired";
    cat "$E/curves_${leg}.csv"; } > "$E/curves_${leg}_hdr.csv"
  # curve aggregates
  awk -F, 'NR>1{h=$2; if(h<min||NR==2)min=h; d+=$3; if($6==1&&$2<pm)pm=$2}
    END{print "min_hold="min" tot_drift="d" post_disc_min_hold="(pm==""?1000:pm)}' \
    "$E/curves_${leg}_hdr.csv" | tee -a "$E/summary_${leg}.txt"
  awk -F, 'NR>1 && $9==1 {print "policyset_block="$1" thr_new="$5}' "$E/curves_${leg}_hdr.csv" | tee -a "$E/summary_${leg}.txt"
  awk -F, 'NR>1 && $6==1 {if(disc==""){disc=$1} } END{print "disconnect_block="disc}' "$E/curves_${leg}_hdr.csv" | tee -a "$E/summary_${leg}.txt"
  echo "LEG $leg PASSED"
  return 0
}

rc=0
run_leg "10x" || rc=1
if [ $rc -eq 0 ]; then run_leg "100x" || rc=1; fi

if [ $rc -ne 0 ]; then echo "TRIAL FAILED"; exit 1; fi
echo "TRIAL PASSED"
