#!/bin/bash
# Round-2 render campaign driver. Usage: run_renders.sh <batch>
# Batches: h1 | h2 | h3 | gx
# All deterministic; progress to its own log. Run each batch in background.
set -u
R=/home/hatch/workspace/tnn-lab/imagination_discovery/aud/continuity_round2/work/renders
R2G=/home/hatch/workspace/tnn-lab/imagination_discovery/aud/continuity_round2/work/r2g/r2g_bin
R2B=/home/hatch/workspace/tnn-lab/imagination_discovery/aud/continuity_round2/work/r2b/r2b_bin
GB=/home/hatch/workspace/tnn-lab/imagination_discovery/aud/b_gamma
RB=/home/hatch/workspace/tnn-lab/imagination_discovery/aud/continuity_round2/work/r2b
mkdir -p $R/h1 $R/h2 $R/h3 $R/g1 $R/g2 $R/g3

batch=${1:?batch required}
LOG=$R/batch_$batch.log
exec > >(tee -a $LOG) 2>&1
echo "=== batch $batch started $(date -u +%FT%TZ) ==="

if [ "$batch" = "h1" ]; then
  cd $RB
  for k in $(seq 0 19); do
    seed=$((20260922 + k*7919))
    for mode in 0 1 2; do
      out=$R/h1/h1_k${k}_m${mode}.wav
      log=$R/h1/h1_k${k}_m${mode}.log
      [ -f "$out" ] && [ -f "$log" ] && { echo "skip k$k m$mode"; continue; }
      ./r2b_bin kids "$out" "" $seed $mode "$log" || echo "FAIL k$k m$mode rc=$?"
      echo "done k$k m$mode $(sha256sum $out | cut -c1-12)"
    done
  done
fi

if [ "$batch" = "h2" ]; then
  cd $GB
  for s in $(seq 1 30); do
    for bm in 0 1; do
      out=$R/h2/h2_s${s}_b${bm}.wav
      log=$R/h2/h2_s${s}_b${bm}.log
      [ -f "$out" ] && [ -f "$log" ] && { echo "skip s$s b$bm"; continue; }
      $R2G kids study_out/gamma.grpk "$out" $s $bm "$log" || echo "FAIL s$s b$bm rc=$?"
      echo "done s$s b$bm $(sha256sum $out | cut -c1-12)"
    done
  done
fi

if [ "$batch" = "h3" ]; then
  cd $GB
  for cls in 0 1 2; do
    for idx in 0 1 2 3; do
      for bedm in 0 1; do
        out=$R/h3/h3_c${cls}_i${idx}_d${bedm}.wav
        log=$R/h3/h3_c${cls}_i${idx}_d${bedm}.log
        [ -f "$out" ] && [ -f "$log" ] && { echo "skip c$cls i$idx d$bedm"; continue; }
        $R2G h3 study_out/gamma.grpk "$out" 0 0 "$log" $cls $idx $bedm || echo "FAIL c$cls i$idx d$bedm rc=$?"
        echo "done c$cls i$idx d$bedm $(sha256sum $out | cut -c1-12)"
      done
    done
  done
fi

if [ "$batch" = "gx" ]; then
  cd $GB
  for r in 1 2 3; do
    out=$R/g1/g1_oceanwf_r${r}.wav
    [ -f "$out" ] || $R2G oceanwf study_out/gamma.grpk "$out" 0 0 ""
    echo "g1 r$r $(sha256sum $out | cut -c1-16)"
  done
  for r in 1 2 3; do
    out=$R/g2/g2_long180_r${r}.wav
    [ -f "$out" ] || $R2G long180 study_out/gamma.grpk "$out" 0 0 ""
    echo "g2 r$r $(sha256sum $out | cut -c1-16)"
  done
  for r in 1 2 3; do
    for bm in 0 2; do
      out=$R/g3/g3_kids_b${bm}_r${r}.wav
      [ -f "$out" ] || $R2G kids study_out/gamma.grpk "$out" 0 $bm ""
      echo "g3 b$bm r$r $(sha256sum $out | cut -c1-16)"
    done
  done
fi

echo "=== batch $batch finished $(date -u +%FT%TZ) ==="
