#!/bin/bash
# WHY-SARCASM wave runner: 16 cells x 3 reps, byte-identical verification.
cd ~/workspace/tnn-lab/prose-learning/epistemic_wave/speechact_exp || exit 1
EV=scored_evidence
BIN=./delib_sarc_bin
fail=0

run_cell() {
  # $1=name $2=mode $3=items [$4=speakers]
  local name="$1" mode="$2" items="$3" spk="$4"
  local outs=()
  for r in 1 2 3; do
    local f="$EV/sarc_${name}_rep${r}.txt"
    if [ -n "$spk" ]; then
      "$BIN" . "$mode" "$items" "$spk" > "$f" 2>/dev/null
    else
      "$BIN" . "$mode" "$items" > "$f" 2>/dev/null
    fi
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

run_cell repro_bare   b c70.txt
run_cell base_bare     b s_bare.txt
run_cell notruth_bare  n s_bare.txt
run_cell base_litfalse b s_litfalse.txt
run_cell layered_bare  l s_bare.txt
run_cell layered_gen   l s_genuine.txt
run_cell base_gen      b s_genuine.txt
run_cell marked_marked m s_marked.txt
run_cell base_marked   b s_marked.txt
run_cell marked_gen    m s_genuine.txt
run_cell speaker_spk   s s_spk.txt speakers.txt
run_cell base_spkutt   b s_spk_utt.txt
run_cell ctx_ctx       c s_ctx.txt
run_cell base_ctxutt   b s_ctx_utt.txt
run_cell inv_marked    i s_marked.txt
run_cell inv_gen       i s_genuine.txt

echo "---"
[ $fail -eq 0 ] && echo "ALL CELLS BYTE-IDENTICAL ACROSS REPS" || echo "DETERMINISM FAILURES PRESENT"
exit $fail
