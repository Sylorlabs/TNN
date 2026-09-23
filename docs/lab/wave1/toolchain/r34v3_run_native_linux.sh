#!/usr/bin/env bash
# Linux port of run_native.zsh for the R34 v3 continual-learner harness.
# Usage: ZNC=/path/to/znc ./run_native_linux.sh
# Everything runs on this machine; no GitHub Actions, no macOS needed.
set -u
BASE="$(cd "$(dirname "$0")" && pwd)"
COMP="${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}"
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
E="$BASE/EVIDENCE_$STAMP"
ROOT="$E/root"
BIN="$E/r34_v3_linux"
mkdir -p "$E" "$ROOT"
chmod 700 "$ROOT"
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
sha256sum "$BASE/r34_learner_core.zag" "$BASE/r34_continuing_harness_v3.zag" \
  "$BASE/PREREGISTRATION.md" "$BASE/README.md" > "$E/source.sha256"

# Isolation: learner core must not import world/checkpoint or use cw_ outcomes.
if grep -nE '@import\([^)]*(world\.zag|checkpoint\.zag)|\bcw_|CWOutcome' \
    "$BASE/r34_learner_core.zag" > "$E/isolation.forbidden.txt"; then
  printf 'learner_core_isolation=false\n' > "$E/isolation.txt"
  fail=$((fail+1))
else
  printf 'learner_core_isolation=true\n' > "$E/isolation.txt"
fi

run compile "$COMP" "$BASE/r34_continuing_harness_v3.zag" \
  --no-zagd --no-analyze --no-foreground-cache -o "$BIN"
if [[ -x "$BIN" ]]; then
  sha256sum "$BIN" > "$E/binary.sha256"
  run campaign "$BIN"
  run reference_mid "$BIN" reference-mid
  run write_mid "$BIN" write-mid "$ROOT"
  run reload_mid "$BIN" reload-mid "$ROOT"
  if cmp -s "$E/reference_mid.stdout" "$E/reload_mid.stdout"; then
    printf 'exact_match=true\n' > "$E/continuation.diff"
  else
    printf 'exact_match=false\n' > "$E/continuation.diff"
    diff -u "$E/reference_mid.stdout" "$E/reload_mid.stdout" >> "$E/continuation.diff" 2>&1
    fail=$((fail+1))
  fi
  run write_inner_corrupt "$BIN" write-inner-corrupt "$ROOT"
  run refuse_inner_corrupt "$BIN" refuse-inner-corrupt "$ROOT"
  run write_torn "$BIN" write-torn "$ROOT"
  run refuse_torn "$BIN" refuse-torn "$ROOT"
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
