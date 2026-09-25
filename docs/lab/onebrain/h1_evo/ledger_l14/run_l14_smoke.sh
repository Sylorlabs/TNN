#!/bin/bash
# run_l14_smoke.sh — composition smoke for H1 ONE-BRAIN EVOLVE, Crew L14.
# Rebuilds nothing (binaries are pinned in bin/); re-runs the FULL battery
# once and verifies: every driver reports OB_FAILURES,0 (except the original
# attacks, whose preregistered divergences are asserted explicitly), and
# every output is byte-identical to its recorded run-1 evidence.
# Exit 0 + SMOKE,PASS only if everything holds.
set -u
L="$HOME/workspace/h1evo/ledger_l14"
cd "$L"
fail=0

chk_zero() { # name file
  grep -q "^OB_FAILURES,0$" "$2" || { echo "FAIL: $1 OB_FAILURES != 0"; grep -h "^OB_FAILURES" "$2"; fail=1; }
}
chk_ident() { # name newfile reffile
  cmp -s "$2" "$3" || { echo "FAIL: $1 not byte-identical to $3"; fail=1; }
}

# ZD suites + R2 (byte-identical vs V0 is asserted via the l14_ run-1 files,
# which were themselves verified byte-identical vs v0_*_1.txt)
for t in ob_test_mem ob_test_arbiter ob_test_fl2 ob_test_pam r2_atk; do
  ./bin/l14_$t > evidence/smoke_$t.txt 2>&1
  chk_zero "$t" evidence/smoke_$t.txt
  chk_ident "$t" evidence/smoke_$t.txt evidence/l14_${t}_1.txt
done

# Hardened L1'-L4' + LH
for t in l1 l2 l3 l4; do
  ./bin/l14_${t}_test > evidence/smoke_l14_$t.txt 2>&1
  chk_zero "l14_$t" evidence/smoke_l14_$t.txt
  chk_ident "l14_$t" evidence/smoke_l14_$t.txt evidence/l14_${t}_1.txt
done
./bin/l14_lh 10 > evidence/smoke_lh10.txt 2>&1
chk_zero "lh10" evidence/smoke_lh10.txt
chk_ident "lh10" evidence/smoke_lh10.txt evidence/l14_lh10_1.txt
./bin/l14_lh 100 > evidence/smoke_lh100.txt 2>&1
chk_zero "lh100" evidence/smoke_lh100.txt
chk_ident "lh100" evidence/smoke_lh100.txt evidence/l14_lh100_1.txt
# prefix consistency re-verified on the smoke outputs
head -10 <(grep "^LH," evidence/smoke_lh100.txt) > /tmp/sm_p100.txt
grep "^LH," evidence/smoke_lh10.txt > /tmp/sm_p10.txt
cmp -s /tmp/sm_p100.txt /tmp/sm_p10.txt || { echo "FAIL: smoke prefix divergence"; fail=1; }

# Original attacks vs hardened code: preregistered divergences
./bin/orig_l1_escape > evidence/smoke_orig_l1.txt 2>&1
grep -q "^L1_FAILURES,0$" evidence/smoke_orig_l1.txt || { echo "FAIL: orig_l1"; fail=1; }
./bin/orig_l2_checkpoint > evidence/smoke_orig_l2.txt 2>&1
n=$(awk -F, '/^L2/ && !/^L2D,/{if($3!=$4)n++}END{print n+0}' evidence/smoke_orig_l2.txt)
[ "$n" = "8" ] || { echo "FAIL: orig_l2 divergence count=$n (want 8)"; fail=1; }
./bin/orig_l3_clock > evidence/smoke_orig_l3.txt 2>&1
n=$(awk -F, '/^L3/ && !/^L3D,/{if($3!=$4)n++}END{print n+0}' evidence/smoke_orig_l3.txt)
[ "$n" = "7" ] || { echo "FAIL: orig_l3 divergence count=$n (want 7)"; fail=1; }
./bin/orig_l4_flood > evidence/smoke_orig_l4.txt 2>&1
# kill legs must be dead: pin applied+audited (expectation mismatches are the repair)
grep -q "^L4c,pin_applied,2,0$" evidence/smoke_orig_l4.txt || { echo "FAIL: orig_l4 pin not applied"; fail=1; }
grep -q "^L4c,pin_audit_trace,1,0$" evidence/smoke_orig_l4.txt || { echo "FAIL: orig_l4 pin not audited"; fail=1; }
grep -q "^L4e,unlogged_verdicts,45,45$" evidence/smoke_orig_l4.txt || { echo "FAIL: orig_l4 ring metric moved"; fail=1; }

if [ "$fail" -ne 0 ]; then echo "SMOKE,FAIL"; exit 1; fi
echo "SMOKE,PASS"
