#!/bin/bash
# Attitude-from-history runner: K-AT2 determinism (3 reps byte-identical)
# + scored evidence. Decision path pure Zag, zero RNG.
cd ~/workspace/tnn-lab/prose-learning/epistemic_wave/speechact_exp || exit 1
EV=scored_evidence
BIN=./delib_att_bin
fail=0

run_cell() {
  local name="$1" items="$2"
  local outs=()
  for r in 1 2 3; do
    local f="$EV/att_${name}_rep${r}.txt"
    "$BIN" . attitude_history.txt "$items" > "$f" 2>/dev/null
    outs+=("$f")
    ( cd "$EV" && sha256sum "$(basename "$f")" > "$(basename "$f" .txt).sha256" )
  done
  if cmp -s "${outs[0]}" "${outs[1]}" && cmp -s "${outs[1]}" "${outs[2]}"; then
    echo "OK   $name  $(tail -1 "${outs[0]}")"
  else
    echo "FAIL $name  reps differ!"
    fail=1
  fi
}

python3 verify_att.py || fail=1
run_cell spk     s_spk.txt
run_cell spk_utt s_spk_utt.txt
exit $fail
