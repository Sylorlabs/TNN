#!/bin/bash
# R2-11-R29 battery runner: one (fork, shard, run, mode).
# Usage: run_one.sh <a|b> <0|1> <r1|r2|r3> <emit|noemit>
# Pure glue. Deterministic: identical inputs -> identical outputs.
FORK=$1; SHARD=$2; RUN=$3; MODE=$4
BASE=~/workspace/tnn-lab/senses/pam-rebuild/round2/forks/R2-11-R29
UF=$(echo "$FORK" | tr '[:lower:]' '[:upper:]')
BIN=$BASE/src/fork${UF}/sense_${FORK}
OUT=$BASE/work/runs/fork${UF}_${RUN}_sh${SHARD}
mkdir -p "$OUT"
LOG="$OUT/RUNLOG.txt"
{
echo "fork=$FORK shard=$SHARD run=$RUN mode=$MODE start=$(date -u +%FT%TZ)"
echo "binary: $(sha256sum "$BIN" | cut -d' ' -f1)"
echo "shard: $(sha256sum "$BASE/work/shards/shard${SHARD}.tsv" | cut -d' ' -f1)"
"$BIN" batch "$BASE/work/shards/shard${SHARD}.tsv" "$OUT" "$MODE"
echo "binary_rc=$?"
echo "end=$(date -u +%FT%TZ)"
sha256sum "$OUT/percepts.tsv" "$OUT/LEDGER.jsonl" "$OUT/failed.tsv"
} > "$LOG" 2>&1
