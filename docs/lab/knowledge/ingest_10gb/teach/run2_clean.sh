#!/bin/bash
# run2_clean.sh — repeat ALL cleanings independently for the determinism gate.
# Same staged inputs as run-1, fresh output dirs (*_r2), same methods/params.
# Run AFTER the run-1 merge. Sequential (box is contended).
set -u
W=~/workspace/scratch_10gb_work
T=~/workspace/tnn-lab/knowledge/ingest_10gb/teach
LOG=$W/logs/run2_clean.log
cd "$W" || exit 1
echo "[run2] start $(date -u)" | tee "$LOG"

# Gutenberg (batched, 9 subsets x 100 files) — same as run-1
python3 $T/clean_batched.py $W/stage/raw/gb_A $W/stage/gb_A_r2 100 >> "$LOG" 2>&1
echo "[run2] gb_A rc=$?" | tee -a "$LOG"
python3 $T/clean_batched.py $W/stage/raw/gb_B $W/stage/gb_B_r2 100 >> "$LOG" 2>&1
echo "[run2] gb_B rc=$?" | tee -a "$LOG"

# OpenStax, SE bio, SE chem (monolithic clean2.py) — same as run-1
python3 $T/clean2.py --raw $W/stage/ostx_in --out $W/stage/ostx_r2 >> "$LOG" 2>&1
echo "[run2] ostx rc=$?" | tee -a "$LOG"
python3 $T/clean2.py --raw $W/stage/se_bio_in --out $W/stage/se_bio_r2 >> "$LOG" 2>&1
echo "[run2] se_bio rc=$?" | tee -a "$LOG"
python3 $T/clean2.py --raw $W/stage/se_chem_in --out $W/stage/se_chem_r2 >> "$LOG" 2>&1
echo "[run2] se_chem rc=$?" | tee -a "$LOG"

# SE physics (batched, 8 subsets x 2 files)
python3 $T/clean_batched.py $W/stage/se_phys_in $W/stage/se_phys_r2 2 >> "$LOG" 2>&1
echo "[run2] se_phys rc=$?" | tee -a "$LOG"

# SE math (batched, 18 subsets x 5 files)
python3 $T/clean_batched.py $W/stage/se_math_in $W/stage/se_math_r2 5 >> "$LOG" 2>&1
echo "[run2] se_math rc=$?" | tee -a "$LOG"

# Wiki (batched, 10 subsets; PER computed from consolidated count)
N=$(ls $W/stage/wiki_in/wikipedia 2>/dev/null | wc -l)
if [ "$N" -eq 0 ]; then echo "[run2] wiki_in MISSING — run wiki splits first"; exit 1; fi
PER=$(( (N + 9) / 10 ))
python3 $T/clean_batched.py $W/stage/wiki_in $W/stage/wiki_r2 $PER >> "$LOG" 2>&1
echo "[run2] wiki rc=$?" | tee -a "$LOG"

echo "[run2] all cleanings done $(date -u)" | tee -a "$LOG"
echo "=== per-source SHA comparison (run-1 vs run-2) ===" | tee -a "$LOG"
python3 - "$LOG" << 'EOF' | tee -a "$LOG"
import json, sys
pairs=[("gb_A","stage/gb_A_run1","stage/gb_A_r2"),("gb_B","stage/gb_B_run1","stage/gb_B_r2"),
 ("ostx","stage/ostx_run2","stage/ostx_r2"),("se_bio","stage/se_bio_run2","stage/se_bio_r2"),
 ("se_chem","stage/se_chem_run1","stage/se_chem_r2"),("se_phys","stage/phys_run1","stage/se_phys_r2"),
 ("se_math","stage/se_math_run1","stage/se_math_r2"),("wiki","stage/wiki_run1","stage/wiki_r2")]
ok=True
for name,r1,r2 in pairs:
    s1=json.load(open(f'/home/hatch/workspace/scratch_10gb_work/{r1}/MANIFEST.json'))['facts_dat_sha256']
    s2=json.load(open(f'/home/hatch/workspace/scratch_10gb_work/{r2}/MANIFEST.json'))['facts_dat_sha256']
    match = (s1==s2); ok = ok and match
    print(f"{name}: {'MATCH' if match else 'DIFFER'} {s1[:16]} vs {s2[:16]}")
print("ALL MATCH" if ok else "MISMATCHES FOUND")
EOF
