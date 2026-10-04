#!/bin/bash
# Sealed run matrix for the F1 adversary battery.
# Each frozen-binary invocation is executed 3 times (runs/1, runs/2, runs/3).
# Corresponding outputs must be byte-identical across the three repetitions.
# Shell only invokes the frozen binary, cmp, sha256sum, mkdir.
set -u
export PATH="$HOME/safebin"
F1=/home/hatch/workspace/tnn-rsi/docs/lab/rsi/runs/wave-20261001-2021pdt/F1
BIN=$F1/dev/bin/f1_learn
S=$F1/sealed

run() { # name episodes state_in
  local name="$1" eps="$2" sin="$3"
  local R="$S/runs/$K"
  "$BIN" "$S/$eps" "$sin" "$R/${name}_state.txt" "$R/${name}_trace.txt" "$R/${name}_pred.txt" > "$R/${name}.log" 2>&1
}

for K in 1 2 3; do
  R="$S/runs/$K"
  mkdir -p "$R"
  # C0-B probes (train-only, seed in)
  run b1 b1_sum.ep -
  run b2 b2_fivex.ep -
  run b3 b3_select.ep -
  run b4 b4_order.ep -
  # C0-C families
  for w in w1 w2 w3 w4; do
    run ${w}_train ${w}_train.ep -
    run ${w}_hidden ${w}_hidden.ep "$R/${w}_train_state.txt"
    run ${w}_abl ${w}_hidden.ep -
  done
  # K-C0D transfer (treatment uses the W2-trained state)
  run tw2_treat tw2_transfer.ep "$R/w2_train_state.txt"
  run tw2_ctrl tw2_transfer.ep -
  # K-REV counterexample (starts from the W2-trained state)
  run r1_train r1_train.ep "$R/w2_train_state.txt"
  run r1_hidden r1_hidden.ep "$R/r1_train_state.txt"
done
echo "runs complete"
