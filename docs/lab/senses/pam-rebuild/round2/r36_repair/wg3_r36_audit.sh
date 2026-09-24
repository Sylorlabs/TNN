#!/bin/bash
# WG3-R36: source audit for the R-36 repair probe.
# The M-36 attacker class lives between marked lines; the harness must not
# contain the old hardcoded seed, and the attacker must not see harness seed
# material (shi/slo/seedhex/material/digest/ledger).
SRC=r36_probe.zag
echo "=== (a) old hardcoded seed absent from HARNESS sections ==="
awk '/M36-ATTACKER-CLASS-BEGIN/{f=1} /M36-ATTACKER-CLASS-END/{f=0; next} !f{print}' $SRC \
  | grep -n "305419896\|2596069104" && echo "DIRTY (a)" || echo "CLEAN (a): no hardcoded seed in harness"
echo ""
echo "=== (b) harness seed material absent from ATTACKER section ==="
awk '/M36-ATTACKER-CLASS-BEGIN/{f=1; next} /M36-ATTACKER-CLASS-END/{f=0} f{print}' $SRC \
  | grep -nw "shi\|slo\|seedhex\|material\|digest\|ledger\|ns_sha256\|r36_derive_seed" \
  && echo "DIRTY (b)" || echo "CLEAN (b): attacker sees no seed material"
echo ""
echo "=== (c) fixture fns take only scalar args ==="
grep -n "^fn adv36_conf\|^fn adv36_meas\|^fn m36a_precompute" $SRC
echo ""
echo "=== (d) ns_sha256 CODE call sites (must be only r36_derive_seed) ==="
sed 's|//.*||' $SRC | grep -n "ns_sha256(" | grep -v "fn ns_sha256"
echo ""
echo "=== (e) wstep NONCE constants only inside wstep ==="
grep -n "608135816\|2242054355" $SRC | grep -v "fn wstep" || echo "(only in wstep)"
echo ""
echo "=== verdict ==="
A=$(awk '/M36-ATTACKER-CLASS-BEGIN/{f=1} /M36-ATTACKER-CLASS-END/{f=0; next} !f{print}' $SRC | grep -c "305419896\|2596069104" || true)
B=$(awk '/M36-ATTACKER-CLASS-BEGIN/{f=1; next} /M36-ATTACKER-CLASS-END/{f=0} f{print}' $SRC | grep -wc "shi\|slo\|seedhex\|material\|digest\|ledger\|ns_sha256\|r36_derive_seed" || true)
D=$(sed 's|//.*||' $SRC | grep -c "ns_sha256(" )
# exactly one code call site: r36_derive_seed (def lives in the substrate)
if [ "$A" = "0" ] && [ "$B" = "0" ] && [ "$D" = "1" ]; then
  echo "WG3-R36: CLEAN"
else
  echo "WG3-R36: DIRTY (a=$A b=$B ns_sha256_calls=$D)"
  exit 1
fi
