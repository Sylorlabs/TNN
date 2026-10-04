#!/bin/bash
# p1falsifier build + watchdog run + determinism. Shell is orchestration only.
set -u
D=/Users/Shared/micah/Documents/TNN/.worktrees/p1falsifier/docs/lab/research-lead/overnight-20260928/p1falsifier
cd "$D" || exit 2
W=/Users/Shared/micah/Documents/TNN/TNN/tools/tnnwatch.sh
. /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh
tnn_pure_zag_report | tail -1
echo "--- frozen file sha256 (must match lane/p1mech @2162252f2) ---"
shasum -a 256 frz.zag sup.zag wld.zag life.zag hlp.zag
cat frz.zag sup.zag wld.zag life.zag hlp.zag fx_main.zag > fx.zag
echo "--- build (zbuild removes any stale binary first) ---"
/Users/Shared/micah/Documents/TNN/TNN/tools/zbuild.sh ./fx.zag || { echo "BUILD-FAIL"; exit 1; }
echo "--- three watchdog runs, 900 s limit, never extended ---"
H=""
for i in 1 2 3; do
  $W reg p1falsifier 900 ./fx > /tmp/p1f_run$i.txt 2>&1
  RC=$?
  S=$(shasum -a 256 /tmp/p1f_run$i.txt | cut -d' ' -f1)
  B=$(wc -c < /tmp/p1f_run$i.txt | tr -d ' ')
  echo "run$i rc=$RC bytes=$B sha=$S"
  H="$H $S"
done
echo "sha triple:$H"
U=$(printf '%s\n' $H | sort -u | wc -l | tr -d ' ')
if [ "$U" = "1" ]; then echo "DETERMINISM: PASS 3/3 byte-identical"; else echo "DETERMINISM: FAIL ($U distinct)"; fi
cp /tmp/p1f_run1.txt "$D/fx_run1.txt"
$W status
