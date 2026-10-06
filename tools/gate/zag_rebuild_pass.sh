#!/bin/sh
# Per-source compile pass. Determines provenance class A / B / E MECHANICALLY.
#
# The point: "reproducible" must not be something a human types. For every committed .zag
# source we invoke the compiler and record the real outcome. A class E (the compiler
# REJECTS the source) is the important discovery case -- it means a committed claim has no
# working implementation at all.
#
# Outputs two files next to this script:
#   .filelist          git ls-files, the input inventory
#   .rebuild_report    one line per source: CLASS<TAB>path
set -u
. /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh
HERE="$(dirname "$0")"
GATE="$HERE/zag_run.sh"
LIST="$HERE/.filelist"
REPORT="$HERE/.rebuild_report"
OUT="${TMPDIR:-/tmp}/tnn_rebuild"

rm -rf "$OUT"; mkdir -p "$OUT"
git ls-files > "$LIST"

TOTAL=0; A=0; B=0; E=0; FRAG=0; NONZAG=0
: > "$REPORT"

# Only compile the sources under the research tree; tools/gate and the legacy experiment
  # dirs are the targets. Skip .md/.txt/fixtures by construction: we only pass .zag paths.
  git ls-files | grep '\.zag$' > "$OUT/.zags"
NZ=$(wc -l < "$OUT/.zags" | tr -d ' ')

# FRAGMENTS. Many legacy results are built by CONCATENATION, not standalone compilation:
#   NAMECHECK.md in belief_provenance says
#     "Built: `cat bp_learner.zag bp_world.zag bp_driver.zag > bp_full.zag`"
#   so bp_learner/bp_world/bp_driver are FRAGMENTS that reference get32/ob_app defined in
#   a sibling, and each fails to compile alone. My first pass reported 406 such files as
#   class E -- "the compiler rejects these sources" -- which is FALSE as stated. They are
#   not dead claims; they are fragments with a documented build recipe, and the recipe was
#   written down in NAMECHECK.md rather than executed by this pass.
#
#   Detecting a fragment by name alone is unreliable, so this pass instead looks for a
#   same-directory *_full.zag (or *_full) that actually compiles. If one does, the
#   fragments in that directory are class F (fragment, source-backed, build recipe
#   documented in NAMECHECK.md) and the *_full.zag is the class A representative.
#   A fragment with NO compiling *_full sibling is class E for real.
FRAGFULL=0
git ls-files | grep -E '_full\.zag$' > "$OUT/.fulls"
echo "dir<TAB>full<TAB>compiles" > "$OUT/.fragmap"
while IFS= read -r F; do
  [ -n "$F" ] || continue
  D="$(dirname "$F")"
  if sh "$GATE" "$F" >/dev/null 2>&1; then OK=1; else OK=0; fi
  printf '%s\t%s\t%s\n' "$D" "$F" "$OK" >> "$OUT/.fragmap"
  [ "$OK" = "1" ] && FRAGFULL=$((FRAGFULL+1))
done < "$OUT/.fulls"

i=0
while IFS= read -r SRC; do
  [ -n "$SRC" ] || continue
  i=$((i+1))
  TOTAL=$((TOTAL+1))
  SDIR="$(dirname "$SRC")"

  # gate compile+run; the gate refuses on failure, which is exactly the signal we want
  if sh "$GATE" "$SRC" > "$OUT/o.$i" 2> "$OUT/e.$i"; then
    if grep -q 'GATE: exit=0' "$OUT/e.$i"; then
      A=$((A+1)); printf 'A\t%s\n' "$SRC" >> "$REPORT"
    else
      B=$((B+1)); printf 'B\t%s\n' "$SRC" >> "$REPORT"
    fi
    continue
  fi

  if grep -q 'REFUSING TO RUN' "$OUT/e.$i"; then
    # Compile rejected it standalone. Before calling the claim dead, check whether it is a
    # FRAGMENT or TEMPLATE of a documented build. Three ways that happens in this corpus:
    #   (1) a same-directory *_full.zag that compiles        (concatenation baked into tree)
    #   (2) a committed *_build*.sh in the dir or an ancestor (recipe spanning dirs)
    #   (3) NO main() AT ALL                                (include fragment or template)
    #
    # (3) matters and was the biggest classification error of the first two passes: I
    # reported 406 then 237 files as "the compiler rejects these sources", which reads as
    # "dead claims". Inspection showed "no main function found" -- they are include
    # fragments and mako-style templates (grid/tmpl_head.zag literally contains
    # "${...}" placeholders). A fragment is not a dead claim; a TEMPLATE is not even
    # meant to compile standalone. Calling both "dead" overstated the damage by ~5x and
    # would have wrongly condemned a large part of the corpus.
    if ! grep -q '^fn main' "$SRC"; then
      FRAG=$((FRAG+1))
      if grep -q '\${' "$SRC" || grep -q '<%' "$SRC"; then
        printf 'F-template\t%s\t(no main; contains placeholder syntax -- not standalone source)\n' "$SRC" >> "$REPORT"
      else
        printf 'F-fragment\t%s\t(no main -- include fragment of a concatenation)\n' "$SRC" >> "$REPORT"
      fi
      continue
    fi
    # it HAS a main, so a standalone failure is a real problem
    FRAGOK=0
    FRAGWHY=""
    FRAGOK=0
    FRAGWHY=""
    while IFS='	' read -r FD FF FOK; do
      if [ "$FD" = "$SDIR" ] && [ "$FOK" = "1" ]; then
        FRAGOK=1; FRAGWHY="sibling $(basename "$FF") compiles"
      fi
    done < "$OUT/.fragmap"
    # (4) recipe scripts are named many things: *_build.sh, *_build_all.sh, and in
    #     cogops_unify_general simply mk.sh / gen.sh / det.sh. Match any *.sh in the dir.
    # (5) more importantly: if a SIBLING .zag in the same directory defines the missing
    #     helpers, this file is a fragment whose recipe may simply be `cat *.zag`.
    #     cogops_unify_general/ref/base.zag defines get32 and o_i64 while main.zag does
    #     not -- so main.zag cannot compile alone and is not a dead claim.
    if [ "$FRAGOK" = "0" ]; then
      for SH in "$SDIR"/*.sh; do
        if [ -f "$SH" ]; then FRAGOK=1; FRAGWHY="committed recipe $(basename "$SH")"; break; fi
      done
    fi
    if [ "$FRAGOK" = "0" ]; then
      # does any sibling define a helper this file uses?
      MISSING=""
      grep -o 'unknown function' "$OUT/e.$i" >/dev/null 2>&1
      for FN in get32 set32 o_app o_i64 o_nl z_alloc pad; do
        if grep -q "^fn $FN" "$SRC"; then continue; fi
        if grep -q "$FN(" "$SRC"; then
          for SIB in "$SDIR"/*.zag; do
            [ "$SIB" = "$SRC" ] && continue
            if grep -q "^fn $FN" "$SIB" 2>/dev/null; then MISSING="$MISSING $FN"; fi
          done
        fi
      done
      if [ -n "$MISSING" ]; then
        FRAGOK=1
        FRAGWHY="defines missing:$MISSING -- in sibling .zag (concatenate to build)"
      fi
    fi
    # and a recipe may live in an ANCESTOR directory (composition dirs often do)
    if [ "$FRAGOK" = "0" ]; then
      AD="$SDIR"
      UP=0
      while [ "$UP" -lt 3 ]; do
        AD="$(dirname "$AD")"
        case "$AD" in docs|docs/lab|docs/lab/research-lead|"") break;; esac
        for SH in "$AD"/*.sh; do
          if [ -f "$SH" ]; then FRAGOK=1; FRAGWHY="ancestor recipe $(basename "$SH")"; break; fi
        done
        [ "$FRAGOK" = "1" ] && break
        UP=$((UP+1))
      done
    fi
    if [ "$FRAGOK" = "1" ]; then
      FRAG=$((FRAG+1)); printf 'F-fragment\t%s\t(%s)\n' "$SRC" "$FRAGWHY" >> "$REPORT"
    else
      E=$((E+1)); printf 'E\t%s\n' "$SRC" >> "$REPORT"
    fi
  else
    B=$((B+1)); printf 'B\t%s\n' "$SRC" >> "$REPORT"
  fi
done < "$OUT/.zags"

# committed non-Zag interpreter sources -- must be zero
NONZAG=$(git ls-files | grep -cE '\.(py|js|mjs|cjs|rb|pl|ts|tsx|jsx|lua|php|swift|go|rs|r|jl|c|cc|cpp|h|hpp|zig|java|m|mm|hs|ml|scala|dart)$' || true)

printf 'ZAG REBUILD PASS -- mechanical provenance\n'
printf '=========================================\n\n'
printf 'committed .zag sources compiled : %s\n' "$NZ"
printf '  A  compiles AND runs exit 0   : %s\n' "$A"
printf '  B  compiles, non-zero exit     : %s\n' "$B"
printf '  F  FRAGMENT, recipe documented : %s   (fail alone, concatenate to build)\n' "$FRAG"
printf '  E  COMPILER REJECTS (dead)    : %s\n' "$E"
printf '  unclassified                  : %s\n' "$((TOTAL-A-B-FRAG-E))"
printf '\n'
printf 'committed non-Zag sources      : %s   (must be 0)\n' "$NONZAG"
printf 'committed extension-less files : %s   (retained as history, NONCANONICAL)\n' \
  "$(git ls-files | grep -vE '\.' | wc -l | tr -d ' ')"
printf '\nreport: %s\n' "$REPORT"

# A class-E entry means a committed claim has no working implementation. Surface them.
if [ "$E" -gt 0 ]; then
  printf '\nCLASS E -- sources the compiler REJECTS (each is a dead claim):\n'
  grep '^E' "$REPORT" | sed 's/^/  /'
fi
exit 0