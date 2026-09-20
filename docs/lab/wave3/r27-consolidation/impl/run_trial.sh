#!/bin/bash
# r27-consolidation trial runner.
# Compile -> learner-core isolation static check -> run -> evidence bundle.
set -e
ZNC="${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}"
cd "$(dirname "$0")"

echo "== compile =="
"$ZNC" trial.zag --no-zagd --no-analyze --no-foreground-cache -o trial

echo "== learner-core isolation (static) =="
# psm.zag is the system: it must not import anything and must not reference
# world/curriculum/truth symbols (t_op/t_param/i_op/cur_ep/Obs belong to the harness).
if grep -n "@import" psm.zag; then echo "ISOLATION_FAIL: psm.zag imports"; exit 1; fi
if grep -n "t_op\|t_param\|i_op\|i_param\|cur_ep\|cur_len\|spurious" psm.zag; then
  echo "ISOLATION_FAIL: psm.zag references harness symbols"; exit 1
fi
echo "learner_core_isolation=true"

echo "== run =="
./trial > run_latest.log 2>&1
echo "exit=$?"
grep -E "^R27C,which=" run_latest.log
grep -E "determinism" run_latest.log

echo "== repeatability (cross-process) =="
./trial > run_repeat.log 2>&1
if cmp -s run_latest.log run_repeat.log; then echo "cross_process_identical=true";
else echo "REPEATABILITY_FAIL"; exit 1; fi

TS=$(date -u +%Y%m%dT%H%M%SZ)
D="EVIDENCE_$TS"; mkdir -p "$D"
cp trial.zag psm.zag run_latest.log run_repeat.log "$D/"
sha256sum trial.zag psm.zag > "$D/SHA256SUMS"
{ echo "r27-consolidation evidence $TS";
  echo "compiler: $("$ZNC" --version 2>/dev/null || echo znc_linux_x86_64_abed8aa1)";
  echo "isolation: true  repeatability: true"; } > "$D/RECEIPT.txt"
echo "evidence: $D"
