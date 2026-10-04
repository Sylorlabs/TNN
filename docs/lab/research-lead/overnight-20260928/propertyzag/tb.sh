set -u
LANE=/Users/Shared/micah/Documents/TNN/.worktrees/propertyzag/docs/lab/research-lead/overnight-20260928/propertyzag
FROZEN=/Users/Shared/micah/Documents/TNN/.worktrees/propertyzag/docs/lab/research-lead/overnight-20260928
BUILD="$LANE/build"
. /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh
mkdir -p "$BUILD"
sed -E -f "$LANE/ren_t2.sed" "$FROZEN/compression_exec/tnn2_frozen_ref.zag" > "$BUILD/z2_core.zag"
sed -E -f "$LANE/ren_c8.sed" "$FROZEN/cogops_learnosc2/c8_base.zag" > "$BUILD/z8_base.zag"
sed -E -f "$LANE/ren_c8.sed" "$FROZEN/cogops_learnosc2/c8_world.zag" > "$BUILD/z8_world.zag"
sed -E -f "$LANE/ren_c8.sed" "$FROZEN/cogops_learnosc2/c8_learn.zag" > "$BUILD/z8_learn.zag"
cp "$BUILD/z8_base.zag" "$BUILD/z2_c15base.zag"
N="${1:-pz_bat}"
PRE="${2:-$BUILD/z2_core.zag}"
cat $PRE > "$BUILD/$N.zag"
cat "$LANE/pz_lib.zag" "$LANE/pz_desc.zag" "$LANE/pz_bat.zag" "$LANE/pz_act.zag" "$LANE/pz_gen.zag" "$LANE/pz_oracle.zag" "$LANE/pz_meta.zag" >> "$BUILD/$N.zag"
cat "$LANE/exp_$N.zag" >> "$BUILD/$N.zag"
znc "$BUILD/$N.zag" || exit 1
"$BUILD/$N"
echo "ROUNDTRIP-OK tnn2 rename round-trip byte-identical"
