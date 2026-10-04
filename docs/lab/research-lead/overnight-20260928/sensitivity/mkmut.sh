#!/bin/bash
# mkmut.sh -- build a single-defect mutant from E_FIX (iv_tnn2.zag).
#
#   mkmut.sh OUT.zag NAME:fn_FUNCNAME [NAME2:fn_FUNCNAME ...]
#        or    mkmut.sh OUT.zag NAME:LINES_A-B ...
#
# Range specs are applied in DESCENDING start-line order so an earlier edit
# never shifts the line numbers of a later one.  A `fn_` spec resolves to the
# whole function body: its `fn` line through the first line that is exactly `}`.
# A mutant is ONE defect; it may need more than one edit when the fix spanned
# more than one site (the call site of a tombstoned rule, say).  The fragment
# names record that.  Nothing else in the core is touched.
set -eu
D=$(cd "$(dirname "$0")" && pwd)
OUT="$1"; shift
rm -f "$OUT" "$(basename "$OUT" .zag)" 2>/dev/null || true
cp "$D/iv_tnn2.zag" "$OUT"
CORE="$D/iv_tnn2.zag"

fn_end() {  # fn_end STARTLINE FILE -> line number of the closing brace
  awk -v s="$1" 'NR>=s && $0 ~ /^}$/ {print NR; exit}' "$2"
}

SPECS=""
for SPEC in "$@"; do SPECS="$SPECS $SPEC"; done

TMPL=$(mktemp)
for S in $SPECS; do
  R="${S#*:}"
  case "$R" in
    fn_*) NAMEF="${R#fn_}"
          A=$(grep -n "^fn $NAMEF(" "$CORE" | head -1 | cut -d: -f1)
          B=$(fn_end "$A" "$CORE") ;;
    *)    A="${R%%-*}"; B="${R##*-}" ;;
  esac
  echo "$A $B $S"
done > "$TMPL"

sort -rn "$TMPL" | while read -r A B S; do
  NAME="${S%%:*}"
  F="$D/frag/$NAME.zag"
  [ -f "$F" ] || { echo "[mkmut] missing fragment $F"; exit 1; }
  T=$(mktemp)
  head -n $((A-1)) "$OUT" > "$T"
  cat "$F" >> "$T"
  tail -n +$((B+1)) "$OUT" >> "$T"
  mv "$T" "$OUT"
  echo "[mkmut] $NAME  replaced iv_tnn2.zag[$A-$B]  -> $(wc -l < "$OUT" | tr -d ' ') lines"
done
rm -f "$TMPL"
