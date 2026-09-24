#!/bin/bash
# run_tsl.sh — T-SL decider gate runner (D2 + D6), modeled on run_gl.sh.
# Static checks -> compile -> 2 executions -> byte-identity -> check audit.
set -e
cd "$(dirname "$0")"
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1

echo "== static checks =="
python3 static_check.py || { echo "STATIC FAIL"; exit 1; }

echo "== compile =="
"$ZNC" t_sl.zag --no-zagd --no-analyze --no-foreground-cache -o t_sl_run 2>&1 | grep -v "external tools" || true

echo "== run 1 =="
./t_sl_run > evidence/gate_run1.txt
rc1=$?
echo "== run 2 =="
./t_sl_run > evidence/gate_run2.txt
rc2=$?
echo "exit codes: $rc1 $rc2"
if [ $rc1 -ne 0 ] || [ $rc2 -ne 0 ]; then echo "RUN FAILURE"; exit 1; fi

echo "== byte identity =="
sha256sum evidence/gate_run1.txt evidence/gate_run2.txt | tee evidence/gate_sha256.txt
if ! cmp -s evidence/gate_run1.txt evidence/gate_run2.txt; then
  echo "BYTE IDENTITY FAIL"; exit 1
fi
echo "BYTE-IDENTICAL OK"

echo "== check audit =="
python3 - <<'EOF'
bad=0; total=0; budgets=True
for line in open('evidence/gate_run1.txt'):
    line=line.strip(); parts=line.split(',')
    if len(parts)==3 and (parts[0].startswith('TSL_D2') or parts[0].startswith('TSL_D6') or parts[0].startswith('TSL_det')):
        total+=1
        if parts[1]!=parts[2]:
            print("MISMATCH:",line); bad+=1
    if parts[0].endswith('_audit_total') and len(parts)==2:
        if int(parts[1])>2048:
            print("AUDIT BUDGET EXCEEDED:",line); budgets=False
print(f"checks: {total}, mismatched: {bad}, budget_ok: {budgets}")
fail_line=[l for l in open('evidence/gate_run1.txt') if l.startswith('TSL_FAILURES,')]
print("exit line:",fail_line[0].strip() if fail_line else "MISSING")
assert bad==0 and budgets and fail_line and fail_line[0].strip()=='TSL_FAILURES,0'
EOF
echo "== GATE PASS =="
