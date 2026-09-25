#!/bin/bash
# WS2-B2 full evidence run: fresh init, official 51, B2 15, maintenance 7.
# Usage: run_b2_evidence.sh <rundir>
# All outputs are deterministic; hash them for the byte-identity check.
set -e
RUNDIR="$1"
B=~/workspace/cognition_ws/ws2/bdir_ws2b2/tocb
W=~/workspace/cognition_ws/ws2
mkdir -p "$RUNDIR"
# --- official battery (51) ---
$B init $W/fixtures/probe_corpus.txt "$RUNDIR/store" > "$RUNDIR/init.log"
$B lookup "$RUNDIR/store" $W/fixtures/probe_queries.txt $W/exp/k_probe.txt "$RUNDIR/out.txt" "$RUNDIR/rep.txt"
$B grade $W/exp/answers_probe.txt "$RUNDIR/out.txt" $W/fixtures/probe_queries.txt "$RUNDIR/grade.txt"
# --- B2 battery (15: fresh 6 + distractor 6 + abstention 3) ---
$B lookup "$RUNDIR/store" $W/fixtures/probe_queries_b2.txt $W/fixtures/k_b2.txt "$RUNDIR/out_b2.txt" "$RUNDIR/rep_b2.txt"
$B grade $W/fixtures/answers_b2.txt "$RUNDIR/out_b2.txt" $W/fixtures/probe_queries_b2.txt "$RUNDIR/grade_b2.txt"
# --- maintenance leg (7) ---
$B init $W/exp/maint/corpus.txt "$RUNDIR/mstore" > /dev/null
$B install "$RUNDIR/mstore" $W/WS2B_MAINT_items.txt > /dev/null
$B lookup "$RUNDIR/mstore" $W/exp/maint/q123.txt $W/exp/maint/k123.txt "$RUNDIR/m_o123.txt" "$RUNDIR/m_r123.txt"
$B revise "$RUNDIR/mstore" NW01 $W/WS2B_MAINT_revise.txt > /dev/null
$B lookup "$RUNDIR/mstore" $W/exp/maint/q45.txt $W/exp/maint/k45.txt "$RUNDIR/m_o45.txt" "$RUNDIR/m_r45.txt"
$B delete "$RUNDIR/mstore" NW02 > /dev/null
$B lookup "$RUNDIR/mstore" $W/exp/maint/q67.txt $W/exp/maint/k67.txt "$RUNDIR/m_o67.txt" "$RUNDIR/m_r67.txt"
# --- hashes of all graded outputs ---
cd "$RUNDIR"
sha256sum out.txt rep.txt grade.txt out_b2.txt rep_b2.txt grade_b2.txt m_o123.txt m_o45.txt m_o67.txt > hashes.txt
grep -h "TOTAL" grade.txt grade_b2.txt
echo RUN_DONE
