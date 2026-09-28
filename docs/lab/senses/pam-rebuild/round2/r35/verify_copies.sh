#!/bin/bash
# verify_copies.sh — prove the R-35 drivers' mechanism functions are
# byte-identical to the repaired probe source, and the attack logic is
# byte-identical to RT-JKLM's frozen J-35 class.
# Usage: run from the r35 dir.
set -e
D="$(dirname "$0")"
PROBE="$D/hpam3536_r35.zag"
RTJ="$D/../rt_jklm/drive35.zag"

# 1. mechanism copies vs repaired probe
python3 "$D/extract_r35.py" "$PROBE" "$D/copy35_r35.check.zag"
if cmp -s "$D/copy35_r35.check.zag" "$D/copy35_r35.zag"; then
  echo "copy35_r35.zag: BYTE-IDENTICAL to repaired probe functions"
else
  echo "copy35_r35.zag: MISMATCH — FAIL"; exit 1
fi
rm "$D/copy35_r35.check.zag"

# 2. driver regeneration vs committed driver
python3 "$D/gen_drive35_r35.py" "$D/drive35_r35.check.zag"
if cmp -s "$D/drive35_r35.check.zag" "$D/drive35_r35.zag"; then
  echo "drive35_r35.zag: REGENERATION-IDENTICAL (attack logic frozen)"
else
  echo "drive35_r35.zag: MISMATCH — FAIL"; exit 1
fi
rm "$D/drive35_r35.check.zag"

# 3. attack functions byte-identical to RT-JKLM's frozen class
for FN in run_j run_k run_l run_m run_honest; do
  A=$(python3 - "$RTJ" "$FN" <<'EOF'
import sys
src, name = sys.argv[1], sys.argv[2]
lines = open(src).read().split("\n")
def is_b(l):
    s=l.strip(); return s.startswith("fn ") or (s.startswith("//") and ("===" in s or "---" in s))
st=[i for i,l in enumerate(lines) if l.startswith("fn "+name) and l[3+len(name):4+len(name)]=="("][0]
en=len(lines)
for j in range(st+1,len(lines)):
    if is_b(lines[j]): en=j; break
print("\n".join(lines[st:en]).rstrip())
EOF
)
  B=$(python3 - "$D/drive35_r35.zag" "$FN" <<'EOF'
import sys
src, name = sys.argv[1], sys.argv[2]
lines = open(src).read().split("\n")
def is_b(l):
    s=l.strip(); return s.startswith("fn ") or (s.startswith("//") and ("===" in s or "---" in s))
st=[i for i,l in enumerate(lines) if l.startswith("fn "+name) and l[3+len(name):4+len(name)]=="("][0]
en=len(lines)
for j in range(st+1,len(lines)):
    if is_b(lines[j]): en=j; break
print("\n".join(lines[st:en]).rstrip())
EOF
)
  if [ "$A" == "$B" ]; then
    echo "$FN: BYTE-IDENTICAL to RT-JKLM frozen class"
  else
    echo "$FN: MISMATCH vs RT-JKLM — FAIL"; exit 1
  fi
done
echo "ALL COPY CHECKS PASS"
