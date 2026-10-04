#!/bin/sh
# C513 lesion-deletion grid generator. Orchestration only.
#
# Sweeps the ONE score template over the frozen 324-cell grid, for BOTH mains:
#   main.zag          = the lesioned battery (C506's own grid)
#   main_nolesion.zag = the SAME battery with the three strat_lesion_sXX
#                       call sites removed
# Only the additive varies between cells. Only the main varies between the
# two halves of the experiment.
#
# Cell (8,1,2,min,on) must reproduce ref/inc_c16.zag byte-for-byte; the
# generator asserts that as a roundtrip check before sweeping.
set -eu
. /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh
D="$(cd "$(dirname "$0")" && pwd)"
cd "$D"
TMPL=ref/tmpl.zag
mkdir -p grid out

# ---- roundtrip check: the grid template IS the c16 template ----
sed -e 's/@P@/8/g' -e 's/@Q@/1/g' -e 's/@D@/2/g' -e 's/@CMP@/</g' "$TMPL" > grid/rt.zag
if cmp -s grid/rt.zag ref/inc_c16.zag; then
  echo "ROUNDTRIP OK: (P=8,Q=1,D=2,min,hedge=on) == ref/inc_c16.zag"
else
  echo "ROUNDTRIP FAIL"; exit 1
fi

emit() {  # P Q D DIR HEDGE MAIN MAINKEY
  P="$1"; Q="$2"; DD="$3"; DIR="$4"; HG="$5"; MAIN="$6"; MK="$7"
  if [ "$DIR" = min ]; then CMP='<'; else CMP='>'; fi
  F=grid/g_${P}_${Q}_${DD}_${DIR}_${HG}.zag
  sed -e "s/@P@/$P/g" -e "s/@Q@/$Q/g" -e "s/@D@/$DD/g" -e "s/@CMP@/$CMP/g" "$TMPL" > "$F"
  if [ "$HG" = off ]; then
    awk '/^  if\(tried==0\)\{$/{d=1;next} d==1{if($0=="  }"){d=0;next};next} {print}' "$F" > "$F.n" \
      && mv "$F.n" "$F"
  fi
  TAG="${MK}_g_${P}_${Q}_${DD}_${DIR}_${HG}"
  ./mk.sh "$F" "$TAG" "$MAIN" > /dev/null 2>&1 || { echo "$TAG BUILD-FAIL"; return 0; }
  echo "$TAG $(wc -c < "out/$TAG.txt" | tr -d ' ')"
}

for MK in L NL; do
  if [ "$MK" = L ]; then MAIN="$D/ref/main.zag"; else MAIN="$D/ref/main_nolesion.zag"; fi
  for DIR in min max; do
   for HG in on off; do
    for DD in 1 2 3; do
     for Q in 0 1 2; do
      for P in 0 1 2 3 4 6 8 12 16; do
        emit "$P" "$Q" "$DD" "$DIR" "$HG" "$MAIN" "$MK"
      done
     done
    done
   done
  done
done