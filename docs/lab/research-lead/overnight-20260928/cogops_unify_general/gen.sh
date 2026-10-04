#!/bin/sh
# gen.sh -- M2 parameter-grid generator (orchestration only).
#
# Sweeps the ONE score template over the preregistered grid and builds each
# cell against the frozen base/world/prefix/main. Emits one line per cell:
#   <tag> <P> <Q> <D> <dir> <hedge> <SUMMARY-DET capability score> <stdout sha12>
#
# The template roundtrip is verified: grid(P=8,Q=1,D=2,min,hedge=on) is
# byte-identical to ref/inc_c16.zag, i.e. the cell (8,1,2,min,on) IS
# incumbent c16 and its capability score is therefore an incumbent score.
set -eu
. /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh
D="$(cd "$(dirname "$0")" && pwd)"
cd "$D"
TMPL=grid/tmpl_c16.zag

emit() {  # P Q D DIR HEDGE
  P="$1"; Q="$2"; DD="$3"; DIR="$4"; HG="$5"
  if [ "$DIR" = min ]; then CMP='<'; else CMP='>'; fi
  F=grid/g_${P}_${Q}_${DD}_${DIR}_${HG}.zag
  sed -e "s/@P@/$P/g" -e "s/@Q@/$Q/g" -e "s/@D@/$DD/g" -e "s/@CMP@/$CMP/g" "$TMPL" > "$F"
  if [ "$HG" = off ]; then
    # delete the hedge block: the single "if(tried==0){" ... matching "  }"
    awk '/^  if\(tried==0\)\{$/{d=1;next} d==1{if($0=="  }"){d=0;next};next} {print}' "$F" > "$F.n" && mv "$F.n" "$F"
  fi
  TAG="g_${P}_${Q}_${DD}_${DIR}_${HG}"
  ./mk.sh "$F" "$TAG" > /dev/null 2>&1 || { echo "$TAG BUILD-FAIL"; return 0; }
  SUM=$(grep '^SUMMARY-DET' "out/$TAG.txt" | sed 's/SUMMARY-DET //')
  SHA=$(shasum -a 256 "out/$TAG.txt" | cut -c1-12)
  printf '%-22s P=%-2s Q=%s D=%s %-3s hedge=%-3s | %s | %s\n' "$TAG" "$P" "$Q" "$DD" "$DIR" "$HG" "$SUM" "$SHA"
}

for DIR in min max; do
 for HG in on off; do
  for DD in 1 2 3; do
   for Q in 0 1 2; do
    for P in 0 1 2 3 4 6 8 12 16; do
      emit "$P" "$Q" "$DD" "$DIR" "$HG"
    done
   done
  done
 done
done
