#!/bin/bash
# E-DE3 battery completion: only the legs missing after the 08:37 daemon drain.
cd ~/workspace/htd-1/builds/ede3
E3=./ede3_bin
FD=../ref-baselines/fulldelib_bin
E5=../ede5/ede5_bin
SN=snapshot.bin
IT=full.manifest
ok=1
for arm in conservative aggressive maximal maximal-aggr cap0; do
  [ -f runs/${arm}_r4.bin ] || { $E3 $arm $SN $IT runs/${arm}_r4.bin || { echo "FAIL ${arm}_r4"; ok=0; }; }
done
[ -f runs/captest_r0.bin ] || { $E3 captest $SN $IT runs/captest_r0.bin || { echo "FAIL captest"; ok=0; }; }
if [ -f "$E5" ]; then
  [ -f runs/e5a_r0.bin ] || { $E5 a $SN $IT runs/e5a_r0.bin || { echo "FAIL e5a"; ok=0; }; }
  [ -f runs/e5b_r0.bin ] || { $E5 b $SN $IT runs/e5b_r0.bin || { echo "FAIL e5b"; ok=0; }; }
else
  echo "NOTE: ede5 binary absent; e5a/e5b head-to-head deferred"
fi
echo "FINISH_DONE ok=$ok"
ls runs/*.bin | wc -l
