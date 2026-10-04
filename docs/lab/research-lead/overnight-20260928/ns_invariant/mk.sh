#!/bin/bash
# mk.sh -- assemble every translation unit in this lane from its sources.
#
# SOURCE OF TRUTH:
#   tnn2_control.zag  byte-identical copy of the frozen engine (never edited)
#   tnn2_control_base.zag  control minus its own main
#   tnn2_ns.zag       the fixed engine (no main)
#   drv_*_src.zag     driver sources (each defines exactly one main)
#
# Generated (never edited by hand):
#   tnn2_control_base.zag, tnn2_ns_base.zag  engine + its own test main
#   drv_ctl.zag, drv_ns.zag                   base + drv_fx1_src.zag
#   drv_fx3.zag                               ns base + drv_fx3_src.zag
#   drv_big.zag                               redimensioned ns base + drv_fx4_src.zag
#
# Rationale: an earlier hand-assembled driver silently carried a STALE engine
# copy, which made a real fix look ineffective. Everything is derived here.
set -eu
cd "$(dirname "$0")"
CTL=tnn2_control.zag
NS=tnn2_ns.zag
STRIP='fn main()i32 { return run_all(); }'

# 0. the control must still be byte-identical to the frozen original
EXPECT=a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd
GOT=$(shasum -a 256 "$CTL" | cut -d' ' -f1)
[ "$GOT" = "$EXPECT" ] || { echo "mk: CONTROL MODIFIED ($GOT != $EXPECT)"; exit 1; }

grep -v "^$STRIP\$" "$CTL" > tnn2_ctl_body.zag
{ cat tnn2_ctl_body.zag; echo "$STRIP"; } > tnn2_control_base.zag

[ -f tnn2_ns_base.zag ] && cp tnn2_ns_base.zag /dev/null 2>/dev/null || true
cp "$NS" tnn2_ns_base.zag
echo "$STRIP" >> tnn2_ns_base.zag

cat tnn2_ctl_body.zag drv_fx1_src.zag > drv_ctl.zag
cp "$NS" drv_ns.zag
cat drv_ns.zag drv_fx1_src.zag > /tmp/_drv_ns && mv /tmp/_drv_ns drv_ns.zag
cat "$NS" drv_fx3_src.zag > drv_fx3.zag

if [ -f drv_fx4_src.zag ]; then
  # FX4: redimension node/edge arenas. This is a MECHANICAL capacity change:
  # NN() and NE() are the only two lines that differ from tnn2_ns.zag, and the
  # arena offsets (EBASE/LBASE/PBASE/WSZ) are all DERIVED from them, so they
  # cannot desynchronise. Verified by re-running the 46-test battery at the
  # frozen size (tnn2_ns_base.zag) and by the LAYOUT line the driver prints.
  sed -e 's|^fn NN()i32 { return 1024; }$|fn NN()i32 { return 8192; }|' \
      -e 's|^fn NE()i32 { return 4096; }$|fn NE()i32 { return 32768; }|' \
      "$NS" > tnn2_big_body.zag
  if cmp -s tnn2_big_body.zag "$NS"; then
    echo "mk: WARNING redimension sed matched nothing; FX4 would silently be NN=1024"
    exit 1
  fi
  cat tnn2_big_body.zag drv_fx4_src.zag > drv_big.zag
fi
echo "mk: assembled: tnn2_control_base.zag tnn2_ns_base.zag drv_ctl.zag drv_ns.zag drv_fx3.zag drv_big.zag"
echo "mk: control sha256 $GOT (frozen original, unmodified)"
