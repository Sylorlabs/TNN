#!/bin/bash
# WS2-A probe battery run. Usage: run_battery.sh <rundir>
# Deterministic: rebuild + ingest + choose + census + trace. Zero RNG.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
RUNDIR="$1"
if [ -z "$RUNDIR" ]; then echo "usage: run_battery.sh <rundir>"; exit 1; fi
rm -rf "$RUNDIR"
mkdir -p "$RUNDIR/stores" "$RUNDIR/out"
B="$HERE/build"
CORPUS="$HERE/fixtures/probe_corpus.txt"
QUERIES="$HERE/fixtures/probe_queries.txt"
# ingest (kind: 2=flat 1=imposed 0=self)
"$B/arm_flat" ingest "$CORPUS" "$RUNDIR/stores/flat" 2
"$B/arm_imposed" ingest "$CORPUS" "$RUNDIR/stores/imposed" 1
"$B/arm_self" ingest "$CORPUS" "$RUNDIR/stores/self" 0
cp "$HERE/fixtures/calib.txt" "$RUNDIR/stores/self/calib.txt"
"$B/arm_self" choose "$RUNDIR/stores/self"
# census pre
"$B/probe" census "$RUNDIR/stores/flat" "$RUNDIR/out/census_flat_pre.txt"
"$B/probe" census "$RUNDIR/stores/imposed" "$RUNDIR/out/census_imposed_pre.txt"
"$B/probe" census "$RUNDIR/stores/self" "$RUNDIR/out/census_self_pre.txt"
# trace
"$B/probe" trace "$RUNDIR/stores/flat" "$QUERIES" "$RUNDIR/out/trace_flat.txt" 2
"$B/probe" trace "$RUNDIR/stores/imposed" "$QUERIES" "$RUNDIR/out/trace_imposed.txt" 1
"$B/probe" trace "$RUNDIR/stores/self" "$QUERIES" "$RUNDIR/out/trace_self.txt" 0
# census post (no mutation expected)
"$B/probe" census "$RUNDIR/stores/flat" "$RUNDIR/out/census_flat_post.txt"
"$B/probe" census "$RUNDIR/stores/imposed" "$RUNDIR/out/census_imposed_post.txt"
"$B/probe" census "$RUNDIR/stores/self" "$RUNDIR/out/census_self_post.txt"
echo "RUN $RUNDIR DONE"
sha256sum "$RUNDIR"/out/*.txt
