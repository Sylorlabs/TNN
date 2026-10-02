#!/usr/bin/env bash
# RC3 negative control (F1 liveness, prereg 3d).
# Patched copy miscounts refusals 399 instead of 400; must produce
# RC_FAILURES > 0 with the mismatch on the refusal check. Evidence stays
# out of the trial dir (/tmp/rc3_neg/).
set -u
BASE="$(cd "$(dirname "$0")" && pwd)"
ZNC="${1:-${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}}"
NEG=/tmp/rc3_neg
rm -rf "$NEG"; mkdir -p "$NEG"
cp "$BASE/rc3_trial.zag" "$NEG/rc3_neg.zag"
cp "$BASE/il_core_rc3.zag" "$NEG/il_core_rc3.zag"
ln -sfn "$BASE/substrate" "$NEG/substrate"
# the fault: sim miscounts refusals (399 instead of 400)
sed -i 's/cl_check("refusals_b",ref_b,400)/cl_check("refusals_b",ref_b,399)/' "$NEG/rc3_neg.zag"
grep -c 'refusals_b",ref_b,399' "$NEG/rc3_neg.zag" | grep -q '^1$' || { echo "PATCH FAILED"; exit 1; }
echo "patch=applied (refusals_b expected 399)"
nice -n 10 "$ZNC" "$NEG/rc3_neg.zag" --no-zagd --no-analyze --no-foreground-cache -o "$NEG/rc3_neg_linux" \
  >"$NEG/compile.stdout" 2>"$NEG/compile.stderr" || { echo "COMPILE FAILED"; tail -20 "$NEG/compile.stderr"; exit 1; }
nice -n 10 "$NEG/rc3_neg_linux" >"$NEG/run.stdout" 2>"$NEG/run.stderr"; ec=$?
echo "run_exit=$ec"
grep -E '^RC_FAILURES,' "$NEG/run.stdout"
grep '^CL_CHECK,' "$NEG/run.stdout" | awk -F, '$3 != $4 {print "MISMATCH:", $2, "actual="$3, "expected="$4}'
fline=$(grep -E '^RC_FAILURES,' "$NEG/run.stdout" | head -1 | cut -d',' -f2)
if [ "$fline" = "0" ]; then echo "NEGATIVE CONTROL FAILED: patched trial passed (should have failed)"; exit 1; fi
echo "NEGATIVE CONTROL: PASS — patched trial fails as designed (F1 liveness)"
