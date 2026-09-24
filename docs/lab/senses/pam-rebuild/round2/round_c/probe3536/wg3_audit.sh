#!/bin/bash
# WG3: source audit — fixture/adversary fns must not receive W/NONCE/CAP params.
SRC=hpam3536_probe.zag
echo "=== adversary/fixture fn definitions (param lists) ==="
grep -n "^fn adv_\|^fn forge\|^fn oracle" $SRC
echo ""
echo "=== call sites passing W-state or NONCE/CAP constants ==="
echo "--- wstep call sites (harness-only fn):"
grep -n "wstep(bs" $SRC | grep -v "^.*fn wstep" | head -30
echo "--- CAP constants 2654435769/2135587861 passed only to tag fns (never adv_/forge):"
grep -n "2654435769\|2135587861" $SRC | grep -v "fn tag_half\|fn vec_tag_half\|verify_high\|declassify\|premise_keyed\|vec_tag" | head
echo "--- NONCE constants 608135816/2242054355 appear only inside wstep:"
grep -n "608135816\|2242054355" $SRC
echo ""
echo "=== verdict: ==="
BAD=$(grep -n "adv_low\|adv36_\|forge(" $SRC | grep -i "whi\|wlo\|nonce\|cap" | grep -v "^\s*//" || true)
if [ -z "$BAD" ]; then echo "CLEAN: no W/NONCE/CAP material reaches adversary fixture fns"; else echo "DIRTY:"; echo "$BAD"; fi
