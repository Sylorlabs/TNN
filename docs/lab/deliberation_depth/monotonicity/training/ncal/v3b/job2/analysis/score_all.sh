#!/usr/bin/env bash
# Score v3b JOB2 variants: sim validation, leg conversion, full bars, T1/T3, T2.
set -e
J=~/workspace/nec_v3b/job2
A=$J/analysis
W=$J/work
N=~/workspace/selfpam_run/tnn-lab/docs/lab/deliberation_depth/monotonicity/training/ncal
cd $W
# inputs the analyses expect in the workdir
cp -n $N/necc_input.tsv $W/necc_input.tsv 2>/dev/null || true
cp -n $N/q2_traps/trap_t3_truth.tsv $W/trap_t3_truth.tsv 2>/dev/null || true
cp -n $N/q2_traps/trap_t1.tsv $W/trap_t1.tsv 2>/dev/null || true

echo "=== sim byte-exact validation (m24/m25 vs Zag binaries) ==="
for v in 24 25; do
  sch=$J/src/schema_k$([ $v = 24 ] && echo a || echo b).tsv
  python3 $A/sim_v2d_v3b.py m$v $N/necc_input.tsv $sch > /tmp/sim_m${v}.tsv
  if cmp -s /tmp/sim_m${v}.tsv $W/m${v}_s1_A.tsv; then echo "OK sim m$v == binary (matrix s1)"; else echo "FAIL sim m$v != binary"; exit 1; fi
  python3 $A/sim_v2d_v3b.py m$v $N/q2_traps/trap_t3.tsv $sch > /tmp/sim_m${v}_t3.tsv
  if cmp -s /tmp/sim_m${v}_t3.tsv $W/m${v}_t3_A.tsv; then echo "OK sim m$v == binary (trap_t3)"; else echo "FAIL sim m$v != binary (trap_t3)"; exit 1; fi
  python3 $A/sim_v2d_v3b.py m$v $N/q2_traps/trap_t1.tsv $sch > /tmp/sim_m${v}_t1.tsv
  if cmp -s /tmp/sim_m${v}_t1.tsv $W/m${v}_t1_A.tsv; then echo "OK sim m$v == binary (trap_t1)"; else echo "FAIL sim m$v != binary (trap_t1)"; exit 1; fi
done

echo "=== convert 6-col -> analyzer legs ==="
for v in 24 25; do
  for s in s1 s10 s100; do
    rm -rf legs_m${v}_${s}
    python3 $A/to_analyzer.py m${v}_${s}_A.tsv legs_m${v}_${s} $v > /dev/null
  done
done

echo "=== full bars ==="
for v in 24 25; do
  for s in s1 s10 s100; do
    echo "--- m$v $s ---"
    python3 $A/bars_full.py legs_m${v}_${s} $v m${v}_${s}_A.tsv \
      $([ $s = s1 ] && echo $N/necc_input.tsv || echo ~/workspace/nec_v2d/work/necc_input_${s}.tsv)
  done
done > bars_v3b.txt 2>&1
cat bars_v3b.txt

echo "=== T1/T3 ==="
python3 $A/t13_v3b.py $W | tee t13_v3b.txt
echo "=== T2 ==="
python3 $A/t2_v3b.py $W | tee t2_v3b.txt
echo "=== SCORING COMPLETE ==="
