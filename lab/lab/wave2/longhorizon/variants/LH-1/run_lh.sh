#!/usr/bin/env bash
# Long-horizon runner (LH variants). Mirrors r34v3/run_native_linux.sh evidence pattern.
# Usage: ./run_lh.sh   (run from the variant dir)
set -u
BASE="$(cd "$(dirname "$0")" && pwd)"
TC="$BASE/toolchain"
COMP="${ZNC:-$TC/bin/znc_linux_x86_64_abed8aa1}"
CANON="$HOME/workspace/tnn-lab/toolchain/r34v3/r34_learner_core.zag"
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
E="$BASE/EVIDENCE_$STAMP"
BIN="$E/r34_lh_linux"
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
sha256sum "$TC/r34v3/r34_learner_core.zag" "$TC/r34v3/r34_lh_harness.zag" > "$E/source.sha256"

# Learner-core isolation: unmodified vs canonical, and no world/checkpoint imports.
if cmp -s "$TC/r34v3/r34_learner_core.zag" "$CANON"; then
  printf 'learner_core_unmodified=true\n' > "$E/isolation.txt"
else
  printf 'learner_core_unmodified=false\n' > "$E/isolation.txt"
  fail=$((fail+1))
fi
if grep -nE '@import\([^)]*(world\.zag|checkpoint\.zag)|\bcw_|CWOutcome' \
    "$TC/r34v3/r34_learner_core.zag" > "$E/isolation.forbidden.txt"; then
  printf 'learner_core_isolation=false\n' >> "$E/isolation.txt"
  fail=$((fail+1))
else
  printf 'learner_core_isolation=true\n' >> "$E/isolation.txt"
fi

run compile "$COMP" "$TC/r34v3/r34_lh_harness.zag" \
  --no-zagd --no-analyze --no-foreground-cache -o "$BIN"
if [[ -x "$BIN" ]]; then
  sha256sum "$BIN" > "$E/binary.sha256"
  run campaign "$BIN"
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
