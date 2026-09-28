#!/bin/bash
# rerun_all.sh — baseline (old certifier) + diff (new certifier) over every
# historical certification artifact. Per PREREG KB-FLIP.
set -u
CR=~/workspace/certrebuild
W=$CR/work
R=$W/reruns
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
LAB=~/workspace/tnn-lab/wave12/step1a-v2
TCO=$W/thincert/thincert_old
TCN=$W/thincert/thincert_new
RSO=$W/rngscan/rngscan_old
RSN=$W/rngscan/rngscan_new
rm -rf $R; mkdir -p $R/thincert $R/rngscan
RES=$R/results.tsv
printf 'case\tstored\told\tnew\told==stored\tclass\n' > $RES

verdict_tc() { grep -h '^verdict=' "$1" 2>/dev/null | cut -d= -f2; }
verdict_rs() { grep -o '"verdict": *"[^"]*"' "$1" 2>/dev/null | head -1 | cut -d'"' -f4; }

run_tc() { # name manifest builddir binary evidence stored
  local name=$1 man=$2 bdir=$3 bin=$4 ev=$5 stored=$6
  local d=$R/thincert/$name; mkdir -p $d
  "$TCO" "$man" "$bdir" "$bin" "$ev" "$d/old.txt" >/dev/null 2>&1; local rco=$?
  "$TCN" "$man" "$bdir" "$bin" "$ev" "$d/new.txt" >/dev/null 2>&1; local rcn=$?
  local s=$(verdict_tc "$stored") o=$(verdict_tc "$d/old.txt") n=$(verdict_tc "$d/new.txt")
  local ms="NO"; [ "$o" = "$s" ] && ms="YES"
  local cl="CONFIRMED"
  if [ "$o" != "$n" ]; then
    if [ "$o" = "PASS" ] && [ "$n" = "FAIL" ]; then cl="VOID"
    elif [ "$o" = "FAIL" ] && [ "$n" = "PASS" ]; then cl="ARTIFACT-FAIL"
    else cl="OTHER-FLIP"; fi
  fi
  printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$name" "$s" "$o" "$n" "$ms" "$cl" >> $RES
  echo "$name: stored=$s old=$o(rc=$rco) new=$n(rc=$rcn) match=$ms class=$cl"
}

run_rs() { # name module.zag module-bin evidence stored
  local name=$1 mod=$2 mbin=$3 ev=$4 stored=$5
  local d=$R/rngscan/$name; mkdir -p $d
  "$RSO" "$mod" "$mbin" "$ev" "$d/old.json" >/dev/null 2>&1; local rco=$?
  "$RSN" "$mod" "$mbin" "$ev" "$d/new.json" >/dev/null 2>&1; local rcn=$?
  local s=$(verdict_rs "$stored") o=$(verdict_rs "$d/old.json") n=$(verdict_rs "$d/new.json")
  local ms="NO"; [ "$o" = "$s" ] && ms="YES"
  local cl="CONFIRMED"
  if [ "$o" != "$n" ]; then
    if [ "$o" = "PASS" ] && [ "$n" = "FAIL" ]; then cl="VOID"
    elif [ "$o" = "FAIL" ] && [ "$n" = "PASS" ]; then cl="ARTIFACT-FAIL"
    else cl="OTHER-FLIP"; fi
  fi
  printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$name" "$s" "$o" "$n" "$ms" "$cl" >> $RES
  echo "$name: stored=$s old=$o(rc=$rco) new=$n(rc=$rcn) match=$ms class=$cl"
}

echo "############ T1: k2prime plants ############"
for NN in 01 02 03 04 05 06 08 09 10 11 12 13 14 15 16 17 18 19 20; do
  d=$R/thincert/t1_plant$NN/tree; mkdir -p $d
  cp $LAB/thin-certifier/k2prime-redteam/plants/plant$NN/*.zag $LAB/thin-certifier/k2prime-redteam/plants/plant$NN/MANIFEST.txt $d/
  ( cd $d && $ZNC build variation.zag -o variation.bin >/dev/null 2>&1 )
  man=$LAB/thin-certifier/k2prime-redteam/scoring/plant$NN/MANIFEST.work
  ev=$LAB/thin-certifier/k2prime-redteam/scoring/plant$NN/replay_interim.evidence
  stored=$LAB/thin-certifier/k2prime-redteam/scoring/plant$NN/attestation.txt
  run_tc "t1_plant$NN" "$man" "$d" "$d/variation.bin" "$ev" "$stored"
done
printf 't1_plant07\tMISSING\t-\t-\t-\tINCONCLUSIVE\n' >> $RES
echo "t1_plant07: no stored attestation -> INCONCLUSIVE"

echo "############ T2: armc plants ############"
for p in dirty1_urandom dirty2_clock dirty3_uninit dirty5_ptrleak; do
  pd=$LAB/armc-rerun-2026-09-21/thincert/plants/$p
  d=$R/thincert/t2_$p; mkdir -p $d
  cp $pd/variation.zag $pd/R33_NATIVE_IO_V1.zag $d/ 2>/dev/null
  ( cd $d && $ZNC build variation.zag -o plant.bin >/dev/null 2>&1 )
  run_tc "t2_$p" "$pd/MANIFEST.txt" "$pd" "$d/plant.bin" "$pd/evidence.txt" "$pd/attestation.txt"
done

echo "############ T3: armc rerun + k3 ############"
rb=$LAB/armc-rerun-2026-09-21/thincert/repbuild_run
d=$R/thincert/t3_repbuild; mkdir -p $d
cp $rb/variation.zag $rb/R33_NATIVE_IO_V1.zag $d/
( cd $d && $ZNC build variation.zag -o variation.bin >/dev/null 2>&1 )
evd=$LAB/armc-rerun-2026-09-21/thincert/evidence
run_tc "t3_rerun" "$rb/MANIFEST.txt" "$d" "$d/variation.bin" "$evd/rerun_evidence.txt" "$evd/rerun_attestation.txt"
run_tc "t3_k3" "$rb/MANIFEST.txt" "$d" "$d/variation.bin" "$evd/k3_rerun_evidence.txt" "$evd/k3_rerun_attestation.txt"

echo "############ R1: rngscan_v3 modules ############"
RD=$R/rngscan/rmod; mkdir -p $RD/modules $RD/substrate
cp $LAB/rngscan-v3/modules/harness.zag $RD/modules/
cp $LAB/rngscan-v3/substrate/*.zag $RD/substrate/
for m in clean2 dirty1_urandom dirty2_clock dirty3_uninit dirty4_eveninit dirty5_entryset dirty6_mutablepin dirty7_clockintrinsic dirty8_alias; do
  src=$m.zag; [ "$m" = "clean2" ] && src=clean2_pinned.zag
  cp $LAB/rngscan-v3/modules/$src $RD/modules/
  ( cd $RD/modules && $ZNC build $src -o $RD/modules/$m.bin >/dev/null 2>&1 )
  ev=$LAB/rngscan-v3/results/${m}_evidence.txt
  stored=$LAB/rngscan-v3/attestations/${m}_att.txt
  run_rs "r1_$m" "$RD/modules/$src" "$RD/modules/$m.bin" "$ev" "$stored"
done
echo "############ DONE ############"
cat $RES
