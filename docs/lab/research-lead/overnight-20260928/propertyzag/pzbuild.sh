#!/bin/sh
# pzbuild.sh -- PROPERTY-ZAG build+run harness.
# Shell is orchestration only. All computation is inside the Zag binary.
#
#   pzbuild.sh NAME                 build NAME.zag, run once
#   pzbuild.sh NAME --rep 3         build, run 3x, assert byte-identical
#
# Sources are assembled by concatenating, in order:
#   <frozen core, renamed>  pz_lib.zag  pz_desc.zag  pz_bat.zag
#   pz_act.zag  pz_gen.zag  pz_oracle.zag  pz_meta.zag  exp_<NAME>.zag
#
# Every produced binary asserts emitted-bytes > 0 in-binary (kill bar K1).

set -u
LANE=/Users/Shared/micah/Documents/TNN/.worktrees/propertyzag/docs/lab/research-lead/overnight-20260928/propertyzag
FROZEN=/Users/Shared/micah/Documents/TNN/.worktrees/propertyzag/docs/lab/research-lead/overnight-20260928
BUILD="$LANE/build"
. /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh

mkdir -p "$BUILD"

# ---------------------------------------------------------------- renames
# tnn2 core: 7 symbols renamed so the harness may own z_alloc/get32/set32/main.
sed -E -f "$LANE/ren_t2.sed" "$FROZEN/compression_exec/tnn2_frozen_ref.zag" > "$BUILD/z2_core.zag"
# reverse-rename audit: must reproduce the original byte-for-byte
sed -E -f "$LANE/ren_t2_inv.sed" "$BUILD/z2_core.zag" > "$BUILD/z2_core_undo.zag"
if ! cmp -s "$BUILD/z2_core_undo.zag" "$FROZEN/compression_exec/tnn2_frozen_ref.zag"; then
  echo "[pzbuild] INFRA-FAIL: tnn2 rename round-trip is not byte-identical"
  exit 2
fi
# c8 learner stack: 4 utility symbols renamed (c8_learn has no main)
sed -E -f "$LANE/ren_c8.sed" "$FROZEN/cogops_learnosc2/c8_base.zag" > "$BUILD/z2_c8base.zag"
sed -E -f "$LANE/ren_c8.sed" "$FROZEN/cogops_learnosc2/c8_world.zag" > "$BUILD/z2_c8world.zag"
sed -E -f "$LANE/ren_c8.sed" "$FROZEN/cogops_learnosc2/c8_learn.zag" > "$BUILD/z2_c8learn.zag"
# c15 base is the same content as c8_base; reuse
cp "$BUILD/z2_c8base.zag" "$BUILD/z2_c15base.zag"

COMMON="$LANE/pz_lib.zag $LANE/pz_desc.zag $LANE/pz_bat.zag $LANE/pz_act.zag $LANE/pz_gen.zag $LANE/pz_oracle.zag $LANE/pz_meta.zag"

build_one() {
  NAME="$1"; PRE="$2"; POST="$3"
  SRC="$BUILD/$NAME.zag"
  cat $PRE > "$SRC"
  cat $COMMON >> "$SRC"
  cat "$LANE/exp_$NAME.zag" >> "$SRC"
  if [ -n "${POST:-}" ]; then cat $POST >> "$SRC"; fi
  znc "$SRC" || { echo "[pzbuild] COMPILE-FAIL $NAME"; exit 1; }
}

case "${2:-}" in
  --rep*)
    N="${2#--rep}"; N="${N:-3}"
    BIN="$BUILD/$1"
    TMPD=$(mktemp -d); trap 'rm -rf "$TMPD"' EXIT
    HASHES=""; OK=1
    i=1
    while [ "$i" -le "$N" ]; do
      O=$("$BIN" 2>&1); R=$?
      printf '%s\n' "$O" > "$TMPD/o$i"
      H=$(shasum -a 256 "$TMPD/o$i" | cut -d' ' -f1)
      HASHES="$HASHES $H"
      echo "[run $i] rc=$R bytes=$(wc -c < "$TMPD/o$i" | tr -d ' ') sha=$H"
      i=$((i+1))
    done
    [ "$R" -eq 0 ] || { echo "[pzbuild] NONZERO-RC"; OK=0; }
    U=$(printf '%s\n' $HASHES | sort -u | wc -l | tr -d ' ')
    if [ "$U" = "1" ]; then echo "[pzbuild] DETERMINISM: PASS ($N/$N byte-identical)";
    else echo "[pzbuild] DETERMINISM: FAIL ($U distinct)"; OK=0; fi
    O=$("$BIN" 2>&1); printf '%s\n' "$O"
    [ "$OK" -eq 1 ] || exit 1
    ;;
  *)
    "$BUILD/$1"; R=$?; echo "[pzbuild] rc=$R"; exit $R ;;
esac