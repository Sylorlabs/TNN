#!/bin/bash
# KPROD shakedown — THROWAWAY inputs only, never battery material.
# Usage: shake_main.sh <outdir>
# Runs the full shakedown sequence; re-running with a fresh outdir must be
# byte-identical (item 8). Logs contain no absolute paths or timestamps.
set -u
OUT="$1"
KPROD="$HOME/workspace/tnn-lab/knowledge/web_guides/live_ingest/kprod"
BIN="$KPROD/bin/instrument_kprod"
BF1="$KPROD/shake/bf1build/webg_bf1"
SH="$KPROD/shake"
IN="$SH/inputs"
mkdir -p "$OUT"

note() { echo "### $*" >> "$OUT/LOG.txt"; }
# run <label> <outfile> <cmd...>: stdout -> outfile, rc -> outfile.rc
run() {
  local label="$1" out="$2"; shift 2
  note "$label -> $out"
  "$@" > "$OUT/$out" 2>&1
  local rc=$?
  echo "$rc" > "$OUT/$out.rc"
  note "$label RC=$rc"
}
dump() { # dump <label> <statefile> : copy a store file into OUT
  local label="$1" f="$2"
  note "$label"
  if [ -f "$f" ]; then cp "$f" "$OUT/$label"; else echo "(absent)" > "$OUT/$label"; fi
}

K="$OUT/k"; N="$OUT/n"; K7="$OUT/k7"
mkdir -p "$K" "$N" "$K7"

note "== teach =="
run "teach-k" teach-k.txt "$BIN" teach "$SH/guides" "$K"
run "teach-n" teach-n.txt "$BIN" teach "$SH/guides" "$N"
run "teach-k7" teach-k7.txt "$BIN" teach "$SH/guides" "$K7"
dump installed-k.txt "$K/installed.txt"

note "== item1: kbcommit append + rejections =="
run "kbcommit-A" kbcommit-A.txt "$BIN" kbcommit "$IN/claimsA.txt" "$K"
run "kbcommit-B" kbcommit-B.txt "$BIN" kbcommit "$IN/claimsB.txt" "$K"
dump knowledge-after-AB.txt "$K/knowledge.txt"
run "kbcommit-pipe" kbcommit-pipe.txt "$BIN" kbcommit "$IN/claims_pipe.txt" "$K"
run "kbcommit-short" kbcommit-short.txt "$BIN" kbcommit "$IN/claims_short.txt" "$K"
dump knowledge-after-reject.txt "$K/knowledge.txt"

note "== item2: prior paths =="
run "verdict-agree" verdict-agree.txt "$BIN" verdict "$K" "$IN/need.txt" "$IN/pages_agree.txt" FACT "test moon orbits planet 27 days 999"
run "verdict-contra" verdict-contra.txt "$BIN" verdict "$K" "$IN/need.txt" "$IN/pages_contra.txt" FACT "test moon orbits planet 27 days 999"
run "verdict-novel-N" verdict-novel-N.txt "$BIN" verdict "$N" "$IN/need.txt" "$IN/pages_novel.txt" FACT "copper pot simmers stove"

note "== item4: pending diversion + dedup; N-arm frozen identity =="
run "verdict-novel-K" verdict-novel-K.txt "$BIN" verdict "$K" "$IN/need.txt" "$IN/pages_novel.txt" FACT "copper pot simmers stove"
dump pending-after-P1.txt "$K/pending.txt"
run "verdict-novel-K-dedup" verdict-novel-K-dedup.txt "$BIN" verdict "$K" "$IN/need.txt" "$IN/pages_novel.txt" FACT "copper pot simmers stove"
dump pending-after-dedup.txt "$K/pending.txt"
run "verdict-novel2-K" verdict-novel2-K.txt "$BIN" verdict "$K" "$IN/need.txt" "$IN/pages_novel2.txt" FACT "wooden bridge spans river"
dump pending-after-P2.txt "$K/pending.txt"
# N-arm vs frozen BF1 on identical inputs (same state dir)
run "bf1-novel" bf1-novel.txt "$BF1" verdict "$N" "$IN/need.txt" "$IN/pages_novel.txt" FACT "copper pot simmers stove"
run "kprod-novel-N" kprod-novel-N.txt "$BIN" verdict "$N" "$IN/need.txt" "$IN/pages_novel.txt" FACT "copper pot simmers stove"
run "bf1-agree-N" bf1-agree-N.txt "$BF1" verdict "$N" "$IN/need.txt" "$IN/pages_agree.txt" FACT "test moon orbits planet"
run "kprod-agree-N" kprod-agree-N.txt "$BIN" verdict "$N" "$IN/need.txt" "$IN/pages_agree.txt" FACT "test moon orbits planet"
run "bf1-single-N" bf1-single-N.txt "$BF1" verdict "$N" "$IN/need.txt" "$IN/pages_single.txt" FACT "lone page test"
run "kprod-single-N" kprod-single-N.txt "$BIN" verdict "$N" "$IN/need.txt" "$IN/pages_single.txt" FACT "lone page test"

note "== item5: kbtest lifecycle =="
run "kbtest-true" kbtest-true.txt "$BIN" kbtest "$K" 1 true
dump knowledge-after-promote.txt "$K/knowledge.txt"
dump pending-after-promote.txt "$K/pending.txt"
run "verdict-prom-paraphrase" verdict-prom-paraphrase.txt "$BIN" verdict "$K" "$IN/need.txt" "$IN/pages_prom.txt" FACT "copper pot simmers stove"
run "kbtest-false" kbtest-false.txt "$BIN" kbtest "$K" 2 false
dump resolved-after-false.txt "$K/resolved.txt"
dump pending-after-false.txt "$K/pending.txt"
run "verdict-reingest-resolved" verdict-reingest-resolved.txt "$BIN" verdict "$K" "$IN/need.txt" "$IN/pages_novel2.txt" FACT "wooden bridge spans river"
run "kbtest-badpseq" kbtest-badpseq.txt "$BIN" kbtest "$K" 99 true
run "verdict-P3" verdict-P3.txt "$BIN" verdict "$K" "$IN/need.txt" "$IN/pages_P3.txt" FACT "silver train crosses bridges"
run "verdict-P4" verdict-P4.txt "$BIN" verdict "$K" "$IN/need.txt" "$IN/pages_P4.txt" FACT "green tractor pulls carts"
dump pending-P3P4.txt "$K/pending.txt"
run "kbtest-badverdict" kbtest-badverdict.txt "$BIN" kbtest "$K" 2 maybe
dump pending-after-badverdict.txt "$K/pending.txt"

note "== item6: kbcommit auto-resolve =="
run "kbcommit-contra3" kbcommit-contra3.txt "$BIN" kbcommit "$IN/contra3.txt" "$K"
dump pending-after-autofalse.txt "$K/pending.txt"
dump resolved-after-autofalse.txt "$K/resolved.txt"
run "kbcommit-agree4" kbcommit-agree4.txt "$BIN" kbcommit "$IN/agree4.txt" "$K"
dump pending-after-autopromote.txt "$K/pending.txt"
dump knowledge-final.txt "$K/knowledge.txt"
dump resolved-final.txt "$K/resolved.txt"

note "== item7: resolved-false precedence (knowledge wins) =="
run "k7-kbcommit-U" k7-kbcommit-U.txt "$BIN" kbcommit "$IN/claimsU.txt" "$K7"
run "k7-verdict-R" k7-verdict-R.txt "$BIN" verdict "$K7" "$IN/need.txt" "$IN/pages_agree.txt" FACT "test moon orbits planet"
run "k7-kbtest-false" k7-kbtest-false.txt "$BIN" kbtest "$K7" 1 false
run "k7-kbcommit-C1" k7-kbcommit-C1.txt "$BIN" kbcommit "$IN/claimsC1.txt" "$K7"
run "k7-verdict-Cstar" k7-verdict-Cstar.txt "$BIN" verdict "$K7" "$IN/need.txt" "$IN/pages_Cstar.txt" FACT "test moon orbits planet"
dump k7-resolved.txt "$K7/resolved.txt"
dump k7-knowledge.txt "$K7/knowledge.txt"

note "== done =="
