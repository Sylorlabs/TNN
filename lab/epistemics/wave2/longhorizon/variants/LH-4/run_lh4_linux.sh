#!/usr/bin/env bash
# LH-4 runner: multi-return curriculum A->B->A->B... (12 visits x 24 train).
# Usage: ZNC=/path/to/znc ./run_lh4_linux.sh   (run from the variant dir)
set -u
BASE="$(cd "$(dirname "$0")" && pwd)"
TOOL="$BASE/toolchain"
COMP="${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}"
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
E="$BASE/EVIDENCE_$STAMP"
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
sha256sum "$TOOL/r34v3/r34_learner_core.zag" "$TOOL/r34v3/r34_lh4_harness.zag" \
  "$BASE/PREREG.md" > "$E/source.sha256" 2>/dev/null || \
sha256sum "$TOOL/r34v3/r34_learner_core.zag" "$TOOL/r34v3/r34_lh4_harness.zag" > "$E/source.sha256"

# Isolation: learner core must not import world/checkpoint or use cw_ outcomes.
if grep -nE '@import\([^)]*(world\.zag|checkpoint\.zag)|\bcw_|CWOutcome' \
    "$TOOL/r34v3/r34_learner_core.zag" > "$E/isolation.forbidden.txt"; then
  printf 'learner_core_isolation=false\n' > "$E/isolation.txt"
  fail=$((fail+1))
else
  printf 'learner_core_isolation=true\n' > "$E/isolation.txt"
fi
# Isolation: LH-4 harness must not touch learner-core internals beyond its public fns.
if grep -nE '\.s00|\.s01|\.s10|\.s11|\.rng=|\.updates=' \
    "$TOOL/r34v3/r34_lh4_harness.zag" | grep -v 's\.\*\.updates\|s\.\*\.pending' \
    > "$E/harness_internalsexposure.txt"; then :; fi

run compile_lh4 "$COMP" "$TOOL/r34v3/r34_lh4_harness.zag" \
  --no-zagd --no-analyze --no-foreground-cache -o "$E/lh4_linux"
BIN="$E/lh4_linux"
if [[ -x "$BIN" ]]; then
  sha256sum "$BIN" > "$E/binary.sha256"
  run campaign_lh4_run1 "$BIN"
  run campaign_lh4_run2 "$BIN"
  if cmp -s "$E/campaign_lh4_run1.stdout" "$E/campaign_lh4_run2.stdout"; then
    printf 'determinism_same_seed=true\n' > "$E/determinism.txt"
  else
    printf 'determinism_same_seed=false\n' > "$E/determinism.txt"
    diff -u "$E/campaign_lh4_run1.stdout" "$E/campaign_lh4_run2.stdout" \
      >> "$E/determinism.txt" 2>&1
    fail=$((fail+1))
  fi
  printf 'lh4_failures_run1=%s\n' "$(grep -oE 'LH4_FAILURES,[0-9]+' "$E/campaign_lh4_run1.stdout" | cut -d, -f2)" \
    > "$E/lh4_failures.txt"
  grep -E '^LH4_RETURN_A' "$E/campaign_lh4_run1.stdout" > "$E/return_counts.txt"
  grep -E '^LH4_VISIT' "$E/campaign_lh4_run1.stdout" > "$E/visit_counts.txt"
else
  fail=$((fail+1))
fi

# Matched control: original R34 v3 campaign re-runs failures=0 with same compiler.
run compile_control "$COMP" "$TOOL/r34v3/r34_continuing_harness_v3.zag" \
  --no-zagd --no-analyze --no-foreground-cache -o "$E/r34v3_control"
if [[ -x "$E/r34v3_control" ]]; then
  run control_campaign "$E/r34v3_control"
  grep -E '^R34V3_FAILURES' "$E/control_campaign.stdout" > "$E/control_failures.txt" || true
fi

(cd "$E" && sha256sum -- *) > "$E/SHA256SUMS" 2>/dev/null
printf 'failures=%s\n' "$fail" > "$E/RECEIPT.txt"
printf 'scientific_exposure=0\n' >> "$E/RECEIPT.txt"
printf 'variant=LH-4\nstamp=%s\n' "$STAMP" >> "$E/RECEIPT.txt"
printf 'evidence_dir=%s\n' "$E" >> "$E/RECEIPT.txt"
echo "failures=$fail evidence=$E"
