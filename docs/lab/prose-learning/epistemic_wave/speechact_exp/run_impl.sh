#!/bin/bash
# Implicature-context runner: K-IM2 determinism (3 reps byte-identical)
# + scored evidence. Decision path pure Zag, zero RNG.
cd ~/workspace/tnn-lab/prose-learning/epistemic_wave/speechact_exp || exit 1
EV=scored_evidence
BIN=./delib_impl2_bin
fail=0

for r in 1 2 3; do
  f="$EV/impl_ctx_rep${r}.txt"
  "$BIN" . impl_situations.txt impl_ctx.txt > "$f" 2>/dev/null
  ( cd "$EV" && sha256sum "$(basename "$f")" > "$(basename "$f" .txt).sha256" )
done
if cmp -s "$EV/impl_ctx_rep1.txt" "$EV/impl_ctx_rep2.txt" && cmp -s "$EV/impl_ctx_rep2.txt" "$EV/impl_ctx_rep3.txt"; then
  echo "OK   ctx  $(tail -1 "$EV/impl_ctx_rep1.txt")"
else
  echo "FAIL ctx  reps differ!"
  fail=1
fi

python3 verify_impl.py || fail=1
exit $fail
