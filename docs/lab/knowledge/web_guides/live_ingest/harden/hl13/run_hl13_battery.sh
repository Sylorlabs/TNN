#!/bin/bash
# HL-13 battery: verdict (baseline) + verdictp (HL-13 gate), 2 reps each.
# Usage: bash run_hl13_battery.sh <outdir>
set -u
cd ~/workspace/liharden/hl13
OUT=${1:-evidence/battery_hl13}
mkdir -p "$OUT" logs
HL13=$PWD/build/hl13_bin
WEBG=~/workspace/rt_bf1/build/bin_webg_bf1
RT=~/workspace/tnn-lab/knowledge/web_guides/live_ingest/redteam_bf1/cases
FXC=~/workspace/liharden/corrob/fixtures
FXR=$PWD/fixtures_rt
jobs=/tmp/hl13_jobs_$$
: > "$jobs"
{
for c in R2_ring2 R3_ring3 R4_ring4 P3_case_variant M1_outnumbered M2b_tie_attack_first M3_false_majority E_LD3_distinct_cites E_TS3_staggered_time; do
  echo "$RT/$c"
done
for c in H1_three_host H2_four_host H3_six_host H4_paraphrase_agree H5_range_format H6_numeric H7_range_agree H8_wire_truth H9_filler_diverse H10_punct_variant H11_claim_second H12_numeric2; do
  echo "$FXC/$c"
done
for c in X_MDIV_full X_MDIV_partial X_MDIV_hard X_HMETA_honest X_MFORGE_frame; do
  echo "$FXR/$c"
done
} | while IFS= read -r path; do
  for m in verdict verdictp; do
    for rep in 1 2; do
      echo "python3 ./run_hl13.py $HL13 $WEBG \"$path\" $OUT $rep $m"
    done
  done
done > "$jobs"
wc -l "$jobs"
xargs -P 8 -I{} sh -c '{}' < "$jobs" > logs/battery_hl13_stdout.txt 2> logs/battery_hl13_stderr.txt
echo "done rc=$?"
