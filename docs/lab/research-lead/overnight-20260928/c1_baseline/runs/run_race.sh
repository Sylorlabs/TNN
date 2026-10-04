#!/bin/bash
# run_race.sh - shell-only sequencer for the lifetime-learning race.
# Usage: run_race.sh <world_dir> <contestant_bin> <run_out_dir>
# Drives the contestant through turns.jsonl, resolves tool calls, scores queries.
set -u
WORLD_DIR="$1"
BIN="$2"
OUT="$3"
mkdir -p "$OUT"
TURNS="$WORLD_DIR/turns.jsonl"
KEY="$WORLD_DIR/key.json"
STATE="$OUT/state"
mkdir -p "$STATE"
rm -f "$STATE"/state.txt "$STATE"/checksum.txt "$STATE"/rss.txt "$STATE"/ledger.txt

TG=$(grep -o '"true_graph":[0-9]' "$KEY" | head -1 | grep -o '[0-9]$')
BP=0; BQ=0; BR=0
N_OBS=0; N_Q=0; N_TOOL=0; N_CORRECT=0; N_ASK=0; N_INT=0
SYNTH_TURN=900000
: > "$OUT/scores.jsonl"
: > "$OUT/replies.jsonl"

jget() { # jget <json> <key> -> value of "key":"val" (first match)
  printf '%s' "$1" | grep -o "\"$2\":\"[^\"]*\"" | head -1 | sed 's/^"[^"]*":"//; s/"$//'
}
jgeti() { # jgeti <json> <key> -> value of "key":123 (first match, may be negative)
  printf '%s' "$1" | grep -o "\"$2\":-*[0-9][0-9]*" | head -1 | sed 's/^"[^"]*"://'
}
causal_sim() { # tg bp bq br dv vv -> prints "p q r"
  local tg=$1 p=$2 q=$3 r=$4 dv=$5 vv=$6
  case "$dv" in P) p=$vv;; Q) q=$vv;; R) r=$vv;; esac
  case "$tg" in
    0) [ "$dv" != Q ] && q=$p
       [ "$dv" != R ] && r=$q ;;
    1) [ "$dv" != R ] && r=$p
       [ "$dv" != Q ] && q=$r ;;
    2) [ "$dv" != P ] && p=$q
       [ "$dv" != R ] && r=$p ;;
  esac
  printf '%s %s %s' "$p" "$q" "$r"
}
expected_for() { # qid -> expected answer from key.json queries
  local qid=$1
  grep -o "\"$qid\":\"[^\"]*\"" "$KEY" | head -1 | sed 's/^"[^"]*":"//; s/"$//'
}

START_MS=$(date +%s%3N)
while IFS= read -r line; do
  kind=$(jget "$line" kind)
  printf '%s' "$line" > "$OUT/turn.json"
  reply=""
  case "$kind" in
    brief|save|load|end)
      reply=$("$BIN" "$OUT/turn.json" "$STATE")
      ;;
    obs)
      N_OBS=$((N_OBS+1))
      if [ "$(jget "$line" t)" = "cobs" ]; then
        ev=$(printf '%s' "$line" | grep -o '"ev":{[^}]*}')
        BP=$(jgeti "$ev" P); BQ=$(jgeti "$ev" Q); BR=$(jgeti "$ev" R)
      fi
      reply=$("$BIN" "$OUT/turn.json" "$STATE")
      ;;
    query)
      N_Q=$((N_Q+1))
      qid=$(jget "$line" qid)
      reply=$("$BIN" "$OUT/turn.json" "$STATE")
      ans=$(jget "$reply" answer)
      exp=$(expected_for "$qid")
      if [ "$exp" = "DYNAMIC" ]; then
        q=$(printf '%s' "$line" | grep -o '"q":{[^}]*}')
        dov=$(jget "$q" do); dovv=$(jgeti "$q" val); askv=$(jget "$q" ask)
        set -- $(causal_sim "$TG" "$BP" "$BQ" "$BR" "$dov" "$dovv")
        case "$askv" in P) exp=$1;; Q) exp=$2;; R) exp=$3;; esac
      fi
      correct=0
      [ "$ans" = "$exp" ] && correct=1
      N_CORRECT=$((N_CORRECT+correct))
      printf '{"qid":"%s","expected":"%s","answer":"%s","correct":%d}\n' "$qid" "$exp" "$ans" "$correct" >> "$OUT/scores.jsonl"
      ;;
    act)
      aqid=$(jget "$line" qid)
      budget=3
      while [ "$budget" -gt 0 ]; do
        reply=$("$BIN" "$OUT/turn.json" "$STATE")
        [ -z "$reply" ] && break
        if printf '%s' "$reply" | grep -q '"tool"'; then
          N_TOOL=$((N_TOOL+1))
          tool=$(jget "$reply" tool)
          tqid=$(jget "$reply" qid)
          result=""
          if [ "$tool" = "ask" ]; then
            N_ASK=$((N_ASK+1))
            obj=$(grep -o "\"$tqid\":{[^}]*}" "$KEY" | head -1 | sed 's/^"[^"]*": //; s/^"[^"]*"://')
            # obj is like {"t":"fact",...} after stripping the key
            result="$obj"
          elif [ "$tool" = "intervene" ]; then
            N_INT=$((N_INT+1))
            var=$(jget "$reply" var); val=$(jgeti "$reply" val)
            set -- $(causal_sim "$TG" "$BP" "$BQ" "$BR" "$var" "$val")
            BP=$1; BQ=$2; BR=$3
            result=$(printf '{"t":"cobs","P":%s,"Q":%s,"R":%s,"do":"%s","val":%s}' "$1" "$2" "$3" "$var" "$val")
          else
            result='{"t":"none"}'
          fi
          SYNTH_TURN=$((SYNTH_TURN+1))
          printf '{"turn":%d,"kind":"toolresult","qid":"%s","result":%s}' "$SYNTH_TURN" "$tqid" "$result" > "$OUT/turn.json"
          _ack=$("$BIN" "$OUT/turn.json" "$STATE")
          if [ "$(jget "$result" t)" = "cobs" ]; then
            BP=$(jgeti "$result" P); BQ=$(jgeti "$result" Q); BR=$(jgeti "$result" R)
          fi
          printf '%s' "$line" > "$OUT/turn.json"
          budget=$((budget-1))
        else
          break
        fi
      done
      ;;
  esac
  printf '%s\n' "$reply" >> "$OUT/replies.jsonl"
done < "$TURNS"
END_MS=$(date +%s%3N)
WALL_MS=$((END_MS-START_MS))

# stage scores
: > "$OUT/stage_scores.txt"
for stg in A B C D E F G H T K L; do
  tot=$(grep -o "\"qid\":\"$stg[0-9]*\"" "$OUT/scores.jsonl" | wc -l)
  ok=$(grep "\"qid\":\"$stg[0-9]*\"" "$OUT/scores.jsonl" | grep -c '"correct":1')
  printf '%s %d/%d\n' "$stg" "$ok" "$tot" >> "$OUT/stage_scores.txt"
done

STATE_BYTES=0
[ -f "$STATE/state.txt" ] && STATE_BYTES=$(wc -c < "$STATE/state.txt")
RSS_KB=0
[ -f "$STATE/rss.txt" ] && RSS_KB=$(cat "$STATE/rss.txt")
{
  printf 'world=%s\n' "$(basename "$WORLD_DIR")"
  printf 'queries=%d correct=%d\n' "$N_Q" "$N_CORRECT"
  printf 'obs=%d tools=%d ask=%d intervene=%d\n' "$N_OBS" "$N_TOOL" "$N_ASK" "$N_INT"
  printf 'wall_ms=%d\n' "$WALL_MS"
  printf 'state_bytes=%d\n' "$STATE_BYTES"
  printf 'peak_rss_kb=%d\n' "$RSS_KB"
  [ -f "$STATE/ledger.txt" ] && cat "$STATE/ledger.txt"
} > "$OUT/costs.txt"
cat "$OUT/costs.txt"
cat "$OUT/stage_scores.txt"
