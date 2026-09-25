#!/bin/bash
# D2 leg runner: 4 organs x 6 batteries x 3 runs; sha256 determinism check.
set -u
cd ~/workspace/pam_gov_lh/crew5_repairs/d2
mkdir -p runs
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
# rebuild from source for provenance
"$ZNC" d2bar.zag -o d2bar 2>build.log || { echo "BUILD FAILED"; exit 1; }
sha256sum d2bar | tee runs/d2bar.sha256
fail=0
for org in D R W N; do
  for bat in B20 B12 B6 B110 B10x B100x; do
    for r in 0 1 2; do
      out="runs/${org}_${bat}_run${r}.out"
      ./d2bar "${bat}.tsv" exemplars.tsv "$org" memory.tsv > "$out" 2>&1
      rc=$?
      if [ $rc -ne 0 ]; then echo "RC=$rc $org $bat run$r"; fail=1; fi
      sha256sum "$out" >> runs/shas.txt
    done
    # determinism: 3 runs byte-identical
    s0=$(sha256sum "runs/${org}_${bat}_run0.out" | cut -d' ' -f1)
    s1=$(sha256sum "runs/${org}_${bat}_run1.out" | cut -d' ' -f1)
    s2=$(sha256sum "runs/${org}_${bat}_run2.out" | cut -d' ' -f1)
    if [ "$s0" != "$s1" ] || [ "$s0" != "$s2" ]; then
      echo "NONDETERMINISTIC: $org $bat"; fail=1
    fi
    echo "$org $bat $s0 $(tail -1 runs/${org}_${bat}_run0.out)"
  done
done
echo "fail=$fail"
exit $fail
