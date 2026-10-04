#!/usr/bin/env bash
# LH-5 runner: reward-corruption ramp for the R34 v3 delayed-credit learner.
# Compiles lh5_corruption_harness.zag, runs the 0/10/25/50% ramp twice
# (determinism check), plus documented supplementary corruption seeds,
# and assembles an EVIDENCE_<stamp> bundle. Nothing pushes to git.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
BASE="$HERE/toolchain/r34v3"
COMP="${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}"
ORIG_LEARNER="$HOME/workspace/tnn-lab/toolchain/r34v3/r34_learner_core.zag"
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
E="$HERE/EVIDENCE_$STAMP"
BIN="$E/lh5_linux"
mkdir -p "$E"
fail=0

run() {
  local label=$1; shift
  printf '%s' "$*" > "$E/$label.command"
  "$@" > "$E/$label.stdout" 2> "$E/$label.stderr"
  local ec=$?
  printf '%s' "$ec" > "$E/$label.exit"
  if (( ec != 0 )); then fail=$((fail+1)); fi
}

sha256sum "$COMP" > "$E/compiler.sha256"
sha256sum "$BASE/lh5_corruption_harness.zag" "$BASE/r34_learner_core.zag" \
  > "$E/source.sha256"

# Law 4: learner core unmodified (byte-identical to toolchain original) and
# structurally isolated (no world/checkpoint imports, no cw_ references).
if cmp -s "$BASE/r34_learner_core.zag" "$ORIG_LEARNER"; then
  printf 'learner_core_unmodified=true\n' > "$E/isolation.txt"
else
  printf 'learner_core_unmodified=false\n' > "$E/isolation.txt"
  fail=$((fail+1))
fi
if grep -nE '@import\([^)]*(world\.zag|checkpoint\.zag)|\bcw_|CWOutcome' \
    "$BASE/r34_learner_core.zag" > "$E/isolation.forbidden.txt"; then
  printf 'learner_core_isolation=false\n' >> "$E/isolation.txt"
  fail=$((fail+1))
else
  printf 'learner_core_isolation=true\n' >> "$E/isolation.txt"
fi

run compile "$COMP" "$BASE/lh5_corruption_harness.zag" \
  --no-zagd --no-analyze --no-foreground-cache -o "$BIN"
if [[ -x "$BIN" ]]; then
  sha256sum "$BIN" > "$E/binary.sha256"
  run ramp_run1 "$BIN"
  run ramp_run2 "$BIN"
  if cmp -s "$E/ramp_run1.stdout" "$E/ramp_run2.stdout"; then
    printf 'deterministic_runs_equal=true\n' > "$E/determinism.diff"
  else
    printf 'deterministic_runs_equal=false\n' > "$E/determinism.diff"
    diff -u "$E/ramp_run1.stdout" "$E/ramp_run2.stdout" >> "$E/determinism.diff" 2>&1
    fail=$((fail+1))
  fi
  # Supplementary sensitivity: extra corruption seeds at 10% and 25%.
  run supp_r10_s7777 "$BIN" rate 10 7777
  run supp_r10_s4242 "$BIN" rate 10 4242
  run supp_r25_s7777 "$BIN" rate 25 7777
fi

printf 'failures=%s\n' "$fail" > "$E/RECEIPT.txt"
printf 'scientific_exposure=0\n' >> "$E/RECEIPT.txt"
printf 'canonical_r27_mutated=false\n' >> "$E/RECEIPT.txt"
printf 'learner_authority_granted=false\n' >> "$E/RECEIPT.txt"
printf 'learn_opened=false\n' >> "$E/RECEIPT.txt"
printf 'successor_promoted=false\n' >> "$E/RECEIPT.txt"
printf 'foreign_ml_runtime_used=false\n' >> "$E/RECEIPT.txt"
printf 'platform=linux-x86_64\n' >> "$E/RECEIPT.txt"
(cd "$E" && find . -type f ! -name SHA256SUMS -print | LC_ALL=C sort | \
  while IFS= read -r f; do sha256sum "$f"; done) > "$E/SHA256SUMS"
printf '%s\n' "$E"
exit $(( fail != 0 ))
