#!/bin/bash
# run_dev.sh - F1 development battery (dev scaffolding only).
# Runs the builder's own development tests, strictly separate from any sealed
# protocol. All tools are the compiled Zag binaries in bin/. Deterministic:
# rerunning this script must produce byte-identical outputs (verified in T8).
# Usage: bash run_dev.sh   (run from the dev/ directory)
set -u
BIN=bin
W=work
LOG=$W/dev_battery.log
: > "$LOG"
say() { echo "$@" | tee -a "$LOG"; }
run() { echo "\$ $*" >> "$LOG"; "$@" 2>&1 | tee -a "$LOG"; }

say "=== F1 dev battery $(date -u +%FT%TZ) ==="

say "--- worlds ---"
run $BIN/f1_devgen dbl 0 10 train $W/d1_train.ep
run $BIN/f1_devgen dbl 10 20 hide  $W/d1_hidden.ep
run $BIN/f1_devgen dbl 10 20 truth $W/d1_hidden.truth
run $BIN/f1_devgen dbl -9 0 hide   $W/d1_neg.ep
run $BIN/f1_devgen dbl -9 0 truth  $W/d1_neg.truth
run $BIN/f1_devgen tpl 0 10 train  $W/d2_contra.ep
run $BIN/f1_devgen tpl 10 20 hide  $W/d2_contra_hidden.ep
run $BIN/f1_devgen tpl 10 20 truth $W/d2_contra_hidden.truth
run $BIN/f1_devgen alt 0 30 train  $W/d3_alt.ep
run $BIN/f1_devgen eq 0 10 train   $W/eq_train.ep
run $BIN/f1_devgen eq 10 20 hide   $W/eq_hidden.ep
run $BIN/f1_devgen eq 10 20 truth  $W/eq_hidden.truth
cat $W/d1_train.ep $W/d2_contra.ep > $W/d12_combined.ep
say "combined dbl+tpl episodes: $(wc -l < $W/d12_combined.ep)"

say "--- T1 experience: dbl train, fresh state ---"
run $BIN/f1_learn $W/d1_train.ep - $W/d1_state.txt $W/d1_trace.txt $W/d1_pred.txt

say "--- T2 hidden: dbl 10..19, trained state, truth masked ---"
run $BIN/f1_learn $W/d1_hidden.ep $W/d1_state.txt $W/d1_state_h.txt $W/d1_trace_h.txt $W/d1_pred_h.txt
run $BIN/f1_score acc $W/d1_pred_h.txt $W/d1_hidden.truth

say "--- T3 ablation: hidden with FRESH state (seed only) ---"
run $BIN/f1_learn $W/d1_hidden.ep - $W/abl_state.txt $W/abl_trace.txt $W/abl_pred.txt
run $BIN/f1_score acc $W/abl_pred.txt $W/d1_hidden.truth

say "--- T4 memorizer control on hidden ---"
run $BIN/f1_score mem $W/d1_train.ep $W/d1_hidden.truth

say "--- T5 transfer: negated inputs, trained state ---"
run $BIN/f1_learn $W/d1_neg.ep $W/d1_state.txt $W/d1_state_t.txt $W/d1_trace_t.txt $W/d1_pred_t.txt
run $BIN/f1_score acc $W/d1_pred_t.txt $W/d1_neg.truth
run $BIN/f1_score exec $W/d1_trace_t.txt main

say "--- T6a revision: contra (3x) loading D1 state ---"
run $BIN/f1_learn $W/d2_contra.ep $W/d1_state.txt $W/d2_state.txt $W/d2_trace.txt $W/d2_pred.txt
run $BIN/f1_learn $W/d2_contra_hidden.ep $W/d2_state.txt $W/d2_state_h.txt $W/d2_trace_h.txt $W/d2_pred_h.txt
run $BIN/f1_score acc $W/d2_pred_h.txt $W/d2_contra_hidden.truth

say "--- T6b revision under law change inside one run (dbl then tpl) ---"
run $BIN/f1_learn $W/d12_combined.ep - $W/d12_state.txt $W/d12_trace.txt $W/d12_pred.txt
say "construct/stall/supersede lines:"
grep -c CONSTRUCT $W/d12_trace.txt | tee -a "$LOG"
grep -c STALL $W/d12_trace.txt | tee -a "$LOG"
grep -c SUPERSEDE $W/d12_trace.txt | tee -a "$LOG"

say "--- T7 supersession stress: alternating law ---"
run $BIN/f1_learn $W/d3_alt.ep - $W/d3_state.txt $W/d3_trace.txt $W/d3_pred.txt
say "supersede lines:"
grep SUPERSEDE $W/d3_trace.txt | tee -a "$LOG"
say "exec counts after supersession (old graphs must show 0 new executions):"
grep "^EXEC" $W/d3_trace.txt | tee -a "$LOG"

say "--- T8 determinism: rerun T1+T2 twice, cmp byte-identical ---"
run $BIN/f1_learn $W/d1_train.ep - $W/d1_state.r2.txt $W/d1_trace.r2.txt $W/d1_pred.r2.txt
run $BIN/f1_learn $W/d1_hidden.ep $W/d1_state.r2.txt $W/d1_state_h.r2.txt $W/d1_trace_h.r2.txt $W/d1_pred_h.r2.txt
cmp $W/d1_state.txt $W/d1_state.r2.txt && say "determinism: state byte-identical" || say "determinism: STATE DIFFERS"
cmp $W/d1_trace.txt $W/d1_trace.r2.txt && say "determinism: trace byte-identical" || say "determinism: TRACE DIFFERS"
cmp $W/d1_pred_h.txt $W/d1_pred_h.r2.txt && say "determinism: hidden pred byte-identical" || say "determinism: PRED DIFFERS"

say "--- C1 menu control (NC-A): dbl train+hidden ---"
run $BIN/f1_ncmenu $W/d1_train.ep $W/ncmenu_pred_train.txt
run $BIN/f1_ncmenu $W/d1_hidden.ep $W/ncmenu_pred_h.txt
run $BIN/f1_score acc $W/ncmenu_pred_h.txt $W/d1_hidden.truth
run $BIN/f1_score exec /dev/null main || true

say "--- C2 kit control (NC-B): eq world (home turf) and dbl (away) ---"
run $BIN/f1_nckit $W/eq_train.ep $W/nckit_pred_train.txt
run $BIN/f1_nckit $W/eq_hidden.ep $W/nckit_pred_h.txt
run $BIN/f1_score acc $W/nckit_pred_h.txt $W/eq_hidden.truth
run $BIN/f1_nckit $W/d1_hidden.ep $W/nckit_pred_dbl.txt
run $BIN/f1_score acc $W/nckit_pred_dbl.txt $W/d1_hidden.truth

say "--- sig comparisons ---"
run $BIN/f1_score sig $W/d1_state.txt $W/d1_state.r2.txt
run $BIN/f1_score sig $W/d1_state.txt $W/d2_state.txt

say "=== battery complete ==="
