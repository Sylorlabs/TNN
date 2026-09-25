#!/bin/bash
# WI-3 cert re-derivation harness (thincert/arena only; no rngscan).
# Independent re-run of the 2026-09-20 thin-certifier gate evidence through
# the fresh arena binary (2/2-identical build). Mirrors rerun_all.sh's run_tc
# for the T1/T2/T3 cases. Output: results TSV + per-case attestations.
set -u
E=~/workspace/tnn-lab/wave12/step1a-v2/gate-expansion/evidence/cert-rederivation/work
R=$E/reruns
TCN=$E/build1/thincert_arena
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
LAB=~/workspace/tnn-lab/wave12/step1a-v2
rm -rf $R; mkdir -p $R
RES=$R/results.tsv
printf 'case\tstored\tnew\tnew==stored\tfull_bytes\tclass\n' > $RES

verdict_tc() { grep -h '^verdict=' "$1" 2>/dev/null | cut -d= -f2; }

run_tc() { # name manifest builddir binary evidence stored
  local name=$1 man=$2 bdir=$3 bin=$4 ev=$5 stored=$6
  local d=$R/$name; mkdir -p $d
  "$TCN" "$man" "$bdir" "$bin" "$ev" "$d/new.txt" >/dev/null 2>&1; local rc=$?
  local s=$(verdict_tc "$stored") n=$(verdict_tc "$d/new.txt")
  local ms="NO"; [ "$n" = "$s" ] && ms="YES"
  local fb="DIFF"
  if [ -f "$stored" ] && [ -f "$d/new.txt" ] && cmp -s "$stored" "$d/new.txt"; then fb="IDENTICAL"; fi
  local cl="CONFIRMED"
  [ "$ms" != "YES" ] && cl="FLIP"
  printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$name" "$s" "$n" "$ms" "$fb" "$cl" >> $RES
  echo "$name: stored=$s new=$n(rc=$rc) verdict_match=$ms bytes=$fb class=$cl"
}

echo "############ T1: k2prime plants ############"
for NN in 01 02 03 04 05 06 08 09 10 11 12 13 14 15 16 17 18 19 20; do
  d=$R/t1_plant$NN/tree; mkdir -p $d
  cp $LAB/thin-certifier/k2prime-redteam/plants/plant$NN/*.zag $LAB/thin-certifier/k2prime-redteam/plants/plant$NN/MANIFEST.txt $d/
  ( cd $d && $ZNC build variation.zag -o variation.bin >/dev/null 2>&1 )
  man=$LAB/thin-certifier/k2prime-redteam/scoring/plant$NN/MANIFEST.work
  ev=$LAB/thin-certifier/k2prime-redteam/scoring/plant$NN/replay_interim.evidence
  stored=$LAB/thin-certifier/k2prime-redteam/scoring/plant$NN/attestation.txt
  run_tc "t1_plant$NN" "$man" "$d" "$d/variation.bin" "$ev" "$stored"
done

echo "############ T2: armc plants ############"
for p in dirty1_urandom dirty2_clock dirty3_uninit dirty5_ptrleak; do
  pd=$LAB/armc-rerun-2026-09-21/thincert/plants/$p
  d=$R/t2_$p; mkdir -p $d
  cp $pd/variation.zag $pd/R33_NATIVE_IO_V1.zag $d/ 2>/dev/null
  ( cd $d && $ZNC build variation.zag -o plant.bin >/dev/null 2>&1 )
  run_tc "t2_$p" "$pd/MANIFEST.txt" "$pd" "$d/plant.bin" "$pd/evidence.txt" "$pd/attestation.txt"
done

echo "############ T3: armc rerun + k3 ############"
rb=$LAB/armc-rerun-2026-09-21/thincert/repbuild_run
d=$R/t3_repbuild; mkdir -p $d
cp $rb/variation.zag $rb/R33_NATIVE_IO_V1.zag $d/
( cd $d && $ZNC build variation.zag -o variation.bin >/dev/null 2>&1 )
evd=$LAB/armc-rerun-2026-09-21/thincert/evidence
run_tc "t3_rerun" "$rb/MANIFEST.txt" "$d" "$d/variation.bin" "$evd/rerun_evidence.txt" "$evd/rerun_attestation.txt"
run_tc "t3_k3" "$rb/MANIFEST.txt" "$d" "$d/variation.bin" "$evd/k3_rerun_evidence.txt" "$evd/k3_rerun_attestation.txt"

echo "############ plant07 disposition ############"
pd7=$R/plant07; mkdir -p $pd7
kp=$LAB/thin-certifier/k2prime-redteam
cp $kp/plants/plant07/*.zag $kp/plants/plant07/MANIFEST.txt $pd7/ 2>/dev/null
( cd $pd7 && $ZNC build variation.zag -o variation.bin > $pd7/build.log 2>&1 ); brc=$?
echo "plant07: znc build rc=$brc (expect nonzero = BUILDFAIL reproduced); no binary => no evidence => no attestation => INCONCLUSIVE"
printf 't1_plant07\tMISSING\t-\t-\t-\tINCONCLUSIVE(plant07 build fails with pinned toolchain, rc=%s; no binary/evidence/attestation)\n' "$brc" >> $RES

echo "############ DONE ############"
cat $RES
