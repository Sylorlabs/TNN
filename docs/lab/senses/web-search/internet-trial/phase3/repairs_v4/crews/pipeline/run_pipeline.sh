#!/bin/bash
# hell-hole V4 full-pipeline run. Usage: run_pipeline.sh <outdir>
# Runs the complete chain from frozen inputs to scored ledgers, deterministically.
# Verdict path is pure Zag binaries; Python is assembly/scoring harness only.
set -e
P=/home/hatch/workspace/scratch-hellhole/crews/pipeline
W=$P/work
HH=/home/hatch/workspace/scratch-hellhole/hellhole
R12=/home/hatch/workspace/scratch-hellhole/crews/integ/r12_v4
LOGIC=/home/hatch/workspace/scratch-hellhole/crews/c2/logic_bin
mkdir -p "$1"
OUT="$(cd "$1" && pwd)"
cd "$OUT"

# 1. R6 propositions (mechanical seed->mlogic mapping) + native logic verdicts
python3 $W/build_r6.py r6_v4_input.tsv > /dev/null
$LOGIC r6_v4_input.tsv > r6_v4_out.txt

# 2. R12 stance tags over v3 evidence (72) + helper observations (9)
$R12 $HH/ev_r12_input.tsv > r12_v4_72.tsv
$R12 $W/helper_r12_input.tsv > r12_v4_helper.tsv

# 3. Joke intents over the 4 v3 joke claims (repaired classifier)
$W/joke_v4 > joke_v4_out.txt

# 4. Assemble driver inputs (columns derived mechanically, see script header)
python3 $W/assemble_v4.py "$OUT" > "$OUT/assemble.log" 2>&1

# 5. Trial driver, both arms (pure Zag, pipeline order R3->R6->JOKE->R5)
$W/v3_trial candidates_v4.tsv votes_solo.tsv jokes_solo.tsv solo > ledger_solo.tsv
$W/v3_trial candidates_v4.tsv votes_helper.tsv jokes_helper.tsv helper > ledger_helper.tsv

# 6. Score vs frozen oracles
python3 $W/score_v4.py "$OUT" > "$OUT/score.log" 2>&1 || { cat "$OUT/score.log"; exit 1; }

echo "run complete: $OUT"
