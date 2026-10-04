#!/bin/bash
# B1 C267 build generator -- blockerfix lane.
#
# Produces a full translation unit for a chosen arena size NN and a chosen
# encoding (legacy threshold vs sign-disjoint).
#
# Layout is DERIVED, not copied: with a 64-byte header and a 40-byte node
# record, nodes occupy [64, 64+NN*40); edges follow at 16 bytes each; the
# 128-entry log follows at 32 bytes each. For NN=65536 this reproduces the
# frozen layout exactly (2621504 / 3670080 / 3674176), which is asserted.
#
# Usage: gen.sh <NN> <legacy|disjoint> <out.zag>
set -eu
NN="$1"; MODE="$2"; OUT="$3"
D="$(cd "$(dirname "$0")" && pwd)"

NODES_END=$((64 + NN * 40))
EDGE_BASE=$NODES_END
LOGBASE=$((EDGE_BASE + NN * 16))
WSZ=$((LOGBASE + 128 * 32))

# 1. re-dimension the base: every 65536 bound is an NN/NE bound, plus the three
#    layout constants. Verified by enumeration in the frozen lane's own report.
sed -e "s/65536/$NN/g" \
    -e "s/^fn WSZ()i32 { return [0-9]*; }/fn WSZ()i32 { return $WSZ; }/" \
    -e "s/^fn eoff(e:i32)i32 { return [0-9]*+e\*16; }/fn eoff(e:i32)i32 { return $EDGE_BASE+e*16; }/" \
    -e "s/^fn loff(l:i32)i32 { return [0-9]*+l\*32; }/fn loff(l:i32)i32 { return $LOGBASE+l*32; }/" \
    "$D/base_64k.zag" > "$D/.gen_base.zag"

# 2. strip the seven functions the patch replaces (Zag concatenates and has no
#    forward declarations, so a redefinition would collide). Legacy keeps the
#    base's own versions and is therefore NOT stripped.
if [ "$MODE" = "disjoint" ]; then
  awk '
    /^fn (res_op|execute|exec_val|t2_guard|t2_set|t2_mov|t2_inc)\(/ {skip=1}
    skip==1 {
      if ($0 ~ /^}/) {skip=0}
      next
    }
    {print}
  ' "$D/.gen_base.zag" > "$D/.gen_base2.zag"
else
  cp "$D/.gen_base.zag" "$D/.gen_base2.zag"
fi

# 3. the workspace allocation in the driver
sed -e "s/z_alloc(3674176)/z_alloc($WSZ)/" "$D/s5000_driver.zag" > "$D/.gen_driver.zag"

# 4. patch file: disjoint replaces 5 writers + 3 interpreter fns; legacy keeps
#    the base's own versions, so for legacy we only re-dimension.
{
  cat "$D/.gen_base2.zag"
  cat "$D/sc_patch_5k.zag"
  if [ "$MODE" = "disjoint" ]; then cat "$D/b1_signdisjoint.zag"; fi
  cat "$D/.gen_driver.zag"
} > "$OUT"

echo "gen NN=$NN mode=$MODE wsz=$WSZ edgebase=$EDGE_BASE logbase=$LOGBASE -> $OUT"