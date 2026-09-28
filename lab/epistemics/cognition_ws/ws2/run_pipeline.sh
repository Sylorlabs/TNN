#!/bin/bash
# WS2-C deterministic rerun harness. Runs the full pipeline (deliberation + sealed bar)
# three times and checks byte-identity. Pure Zag, zero RNG.
set -e
DELIB=${DELIB:-~/workspace/cognition_ws/ws2/build/delib}
WS2=~/workspace/cognition_ws/ws2
MORG=~/workspace/tnn-lab/memory_org
RUN=$1
if [ -z "$RUN" ]; then echo "usage: run_pipeline.sh R1|R2|R3"; exit 2; fi
RD=$WS2/runs/$RUN
rm -rf "$RD"
mkdir -p "$RD/work" "$RD/bar"
cd "$RD/work"
cp $WS2/fixtures/probe_corpus.txt .
cp $WS2/fixtures/probe_queries.txt .
cp $MORG/corpus.txt morg_corpus.txt
cp $MORG/queries.txt morg_queries.txt
cp $WS2/evidence.md .
$DELIB deliberate "$RD/work"
cd "$RD/bar"
cat $MORG/corpus.txt $MORG/corpus_holdout.txt > bar_corpus.txt
cp $MORG/queries_holdout.txt bar_queries.txt
$DELIB bar "$RD/work/out/scheme.json" bar_corpus.txt bar_queries.txt out || true
echo "=== $RUN done ==="
find "$RD" -type f | sort | xargs sha256sum > "$RD/SHASUMS.txt"
cat "$RD/SHASUMS.txt"
