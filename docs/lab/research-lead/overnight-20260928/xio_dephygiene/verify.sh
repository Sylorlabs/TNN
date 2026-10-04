#!/bin/sh
# verify.sh -- check every frozen kill bar K1-K10 against the run outputs.
# Shell only: cmp, sha256sum, grep. Exits nonzero naming the failed bar.
set -u
LANE=$(dirname "$0")
ADAPT="$LANE/../xio_adapters"
HARDER="$LANE/../xio_harder"
F="$LANE/outputs/dephy_full.run1.log"
pass=0; fail=0
chk() { # chk <bar> <description>; reads pattern from stdin check via eval
  desc="$2"
  if eval "$1"; then echo "PASS $desc"; pass=$((pass+1)); else echo "FAIL $desc"; fail=$((fail+1)); fi
}

# K1 liveness
chk "grep -q 'H0 dep_rel(dead m1)=-1 (expect -1)' '$F'" "K1 LIVENESS"
# K2 tombstone
chk "grep -q 'H1 t1-from-m1 pre=3 post=0 tombstoned=6 (expect post=0, tomb>0)' '$F'" "K2 TOMBSTONE-probe"
chk "grep -q 'H1 dep_rel=82 (expect 82)' '$F'" "K2 TOMBSTONE-dep_rel"
chk "grep -q 'H1 nm=27 reused=1' '$F'" "K2 TOMBSTONE-reuse"
# K3 graph filter
chk "grep -q 'H2 stale t1-from-m1=3 (expect >0, not tombstoned)' '$F'" "K3 GRAPH-probe"
chk "grep -q 'H2 dep_rel=82 (expect 82 via graph filter)' '$F'" "K3 GRAPH-dep_rel"
# K4 masked audit
chk "grep -q 'XIO-MASKED-REFUSED s=31 r=93 ans=70' '$F'" "K4 AUDIT-refused"
chk "grep -q 'H34 superseded=1 (expect 1)' '$F'" "K4 AUDIT-superseded"
chk "grep -q 'H34 masked qm=70' '$F'" "K4 AUDIT-qm"
# K5 no poison
chk "grep -q 'H34 unmasked qu=3 (expect 3)' '$F'" "K5 NOPOISON-qu"
chk "grep -q 'H34 live-nonsuperseded-poison=0 (expect 0)' '$F'" "K5 NOPOISON-census"
# K6 legitimate learning
chk "grep -q 'H5a q1=14 q2=14 (expect 14, 14)' '$F'" "K6 LEARN-h5a"
chk "grep -q 'H5b vc=1 (expect 1)' '$F'" "K6 LEARN-vc"
chk "grep -q 'H5b contra(93,2)=0 (expect 0)' '$F'" "K6 LEARN-contra-match"
chk "grep -q 'H5b contra(93,70)=1 (expect 1)' '$F'" "K6 LEARN-contra-contra"
chk "grep -q 'H5b contra(97,5)=0 (expect 0)' '$F'" "K6 LEARN-contra-norel"
# K7/K8 regressions: 3/3 byte-identical to committed baselines
for i in 1 2 3; do
  chk "cmp -s '$LANE/outputs/dephy_c229.run$i.log' '$ADAPT/xio_run1.txt'" "K7 C229-r$i"
  chk "cmp -s '$LANE/outputs/dephy_c235.run$i.log' '$HARDER/xhio_run1.txt'" "K8 C235-r$i"
done
# K9 determinism: 3/3 identical per binary
for b in dephy_full dephy_c229 dephy_c235; do
  chk "cmp -s '$LANE/outputs/$b.run1.log' '$LANE/outputs/$b.run2.log' && cmp -s '$LANE/outputs/$b.run2.log' '$LANE/outputs/$b.run3.log'" "K9 DET-$b"
done
# K10 architecture
tmpd=$(mktemp -d)
sed -n '1,1677p' "$ADAPT/xio_full.zag" > "$tmpd/base_ref.zag"
sed -n '1,1677p' "$LANE/dephy_c229.zag" > "$tmpd/base_got.zag"
chk "cmp -s '$tmpd/base_ref.zag' '$tmpd/base_got.zag'" "K10 ARCH-base-intact"
rm -rf "$tmpd"
if grep -rEi '_mode|mode_|bridge|handler' "$LANE/src/" >/dev/null 2>&1; then
  echo "FAIL K10 ARCH-no-modes (hits found)"; fail=$((fail+1))
else
  echo "PASS K10 ARCH-no-modes"; pass=$((pass+1))
fi

echo "verify: pass=$pass fail=$fail"
[ "$fail" -eq 0 ]
