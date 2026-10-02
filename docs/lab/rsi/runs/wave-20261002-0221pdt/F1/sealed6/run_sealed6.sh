#!/bin/bash
# run_sealed6.sh - sealed evaluation runs for the F1 POLICY-C wave.
# Runs every invocation 3 times (repetitions 1,2,3) for byte-identical
# determinism verification. Pure shell invoking compiled Zag binaries.
# Usage: run_sealed6.sh  (run from the F1 lane directory)

set -u
LANE="docs/lab/rsi/runs/wave-20261002-0221pdt/F1"
NEWBIN="$LANE/impl/f1_learn_c"
OLDBIN="docs/lab/rsi/runs/wave-20261001-2321pdt/F1/impl/f1_learn"
S6="$LANE/sealed6"
SP="$LANE/sealed6"
TP="docs/lab/rsi/runs/wave-20261001-2321pdt/F1/sealed"
T21="docs/lab/rsi/runs/wave-20261001-2021pdt/F1/sealed"
S5="docs/lab/rsi/runs/wave-20261001-2321pdt/F1-REPAIR2/sealed5"
RUNS="$LANE/runs6"

# verify frozen binaries before running
echo "$NEWBIN" | grep -q . || exit 2
NEW_SHA=$(sha256sum "$NEWBIN" | awk '{print $1}')
OLD_SHA=$(sha256sum "$OLDBIN" | awk '{print $1}')
echo "NEWBIN sha256=$NEW_SHA"
echo "OLDBIN sha256=$OLD_SHA"
if [ "$NEW_SHA" != "772e9e2776fc6b1e681676fb4b122c57db05a0b8aff4e3d2b56d2df72d43c6a0" ]; then
  echo "FATAL: new binary hash mismatch"; exit 2
fi
if [ "$OLD_SHA" != "6f2b155b233a95ad1a8323e8565b9a798dc822db6eff57e065b71b5be8882847" ]; then
  echo "FATAL: control binary hash mismatch"; exit 2
fi

# run_one <name> <binary> <episodes> <state_in>
# <state_in> may contain {R}, replaced by the repetition number so each
# repetition chains from its own train state.
run_one() {
  local name="$1" bin="$2" ep="$3" sin="$4"
  local r
  for r in 1 2 3; do
    local d="$RUNS/$r"
    local s="${sin//\{R\}/$r}"
    "$bin" "$ep" "$s" "$d/$name.state" "$d/$name.trace" "$d/$name.pred" \
      > "$d/$name.stdout" 2> "$d/$name.stderr"
    echo "$?" > "$d/$name.rc"
  done
}

mkdir -p "$RUNS/1" "$RUNS/2" "$RUNS/3"

# ---- fresh sparse fixtures (new binary) ----
run_one sF_train  "$NEWBIN" "$S6/sF_train.ep"   "-"
run_one sF_hid    "$NEWBIN" "$S6/sF_hidden.ep"  "$RUNS/{R}/sF_train.state"
run_one sF_abl    "$NEWBIN" "$S6/sF_hidden.ep"  "-"
run_one sG_train  "$NEWBIN" "$S6/sG_train.ep"   "-"
run_one sG_hid    "$NEWBIN" "$S6/sG_hidden.ep"  "$RUNS/{R}/sG_train.state"
run_one sG_abl    "$NEWBIN" "$S6/sG_hidden.ep"  "-"
run_one c0        "$NEWBIN" "$S6/c0_clean.ep"   "-"

# ---- gap-premise control (old windowed binary on fresh sparse trains) ----
run_one sF_trainW "$OLDBIN" "$S6/sF_train.ep"   "-"
run_one sG_trainW "$OLDBIN" "$S6/sG_train.ep"   "-"

# ---- clean worlds (new binary) ----
run_one cA        "$NEWBIN" "$TP/cA_clean.ep"   "-"
run_one cB_tr     "$NEWBIN" "$TP/cB_train.ep"   "-"
run_one cB_cl     "$NEWBIN" "$TP/cB_clean.ep"   "$RUNS/{R}/cB_tr.state"
run_one cC_tr     "$NEWBIN" "$TP/cC_train.ep"   "-"
run_one cC_cl     "$NEWBIN" "$TP/cC_clean.ep"   "$RUNS/{R}/cC_tr.state"

# ---- dense interleaving regression (new binary) ----
for p in tA tB tC tD; do
  run_one "${p}_tr"  "$NEWBIN" "$TP/${p}_train.ep"  "-"
  run_one "${p}_hid" "$NEWBIN" "$TP/${p}_hidden.ep" "$RUNS/{R}/${p}_tr.state"
done

# ---- law-change and overfit controls (new binary) ----
run_one rW3_tr  "$NEWBIN" "$TP/rW3_train.ep"  "-"
run_one rW3_hid "$NEWBIN" "$TP/rW3_hidden.ep" "$RUNS/{R}/rW3_tr.state"
run_one rW2_tr  "$NEWBIN" "$TP/rW2_train.ep"  "-"
run_one rW2_hid "$NEWBIN" "$TP/rW2_hidden.ep" "$RUNS/{R}/rW2_tr.state"

# ---- original 2021pdt passing families (new binary) ----
run_one w2_tr  "$NEWBIN" "$T21/w2_train.ep"  "-"
run_one w2_hid "$NEWBIN" "$T21/w2_hidden.ep" "$RUNS/{R}/w2_tr.state"
run_one w3_tr  "$NEWBIN" "$T21/w3_train.ep"  "-"
run_one w3_hid "$NEWBIN" "$T21/w3_hidden.ep" "$RUNS/{R}/w3_tr.state"

# ---- 7300-series corpus (new binary) ----
i=0
while [ $i -lt 24 ]; do
  run_one "s5_${i}_tr"  "$NEWBIN" "$S5/s5_train_${i}.ep"  "-"
  run_one "s5_${i}_hid" "$NEWBIN" "$S5/s5_hidden_${i}.ep" "$RUNS/{R}/s5_${i}_tr.state"
  i=$((i + 1))
done

echo "ALL RUNS DONE"
