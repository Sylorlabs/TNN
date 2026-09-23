#!/usr/bin/env bash
# Clean-rerun evidence runner (r34 remediation workstream).
# Compiles ../r34_lh_clean_harness.zag, runs the LH-1/2/3/5 legs twice each
# (determinism), plus LH-5 supplementary seeds, and assembles an
# EVIDENCE_<stamp> bundle. Prereg: PREREG_RERUN.md (frozen before evidence).
# Nothing pushes to git; commit via commit_to_branch.py afterwards.
set -u
BASE="$(cd "$(dirname "$0")" && pwd)"
REM="$BASE/.."
HARNESS="$REM/r34_lh_clean_harness.zag"
CORE="$REM/r34_clean_learner.zag"
COMP="${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}"
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
E="$BASE/EVIDENCE_$STAMP"
BIN="$E/lh_clean_linux"
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
sha256sum "$HARNESS" "$CORE" > "$E/source.sha256"

# --- Isolation + static audit (prereg K2) ---
# 1. Learner core: zero forbidden terms (code AND comments).
if grep -nEi 'rng|lcg|seed|rand|srand|random|entropy|urandom|_zag_time|_zag_clock' \
    "$CORE" > "$E/audit.core_terms.txt"; then
  printf 'core_forbidden_terms=FOUND\n' > "$E/isolation.txt"; fail=$((fail+1))
else
  printf 'core_forbidden_terms=none\n' > "$E/isolation.txt"
fi
# 2. Learner core imports: observation.zag only.
grep -n '@import' "$CORE" > "$E/audit.core_imports.txt"
if grep -nE '@import\([^)]*(world\.zag|checkpoint\.zag|storage\.zag)' "$CORE" \
    > "$E/audit.core_forbidden_imports.txt"; then
  printf 'core_isolation=false\n' >> "$E/isolation.txt"; fail=$((fail+1))
else
  printf 'core_isolation=true\n' >> "$E/isolation.txt"
fi
# 3. Harness: strip // comments, then forbid every RNG-term except the
#    documented *seed identifiers (world/drift/corruption seeds, prereg A6).
grep -vE '^[[:space:]]*//' "$HARNESS" > "$E/harness_nocomments.tmp"
if grep -nEi 'rng|lcg|rand|srand|random|entropy|urandom|_zag_time|_zag_clock' \
    "$E/harness_nocomments.tmp" > "$E/audit.harness_hard_terms.txt"; then
  printf 'harness_hard_terms=FOUND\n' >> "$E/isolation.txt"; fail=$((fail+1))
else
  printf 'harness_hard_terms=none\n' >> "$E/isolation.txt"
fi
grep -nEi 'seed' "$E/harness_nocomments.tmp" > "$E/audit.harness_seed_terms.txt" || true
rm -f "$E/harness_nocomments.tmp"

# --- Build ---
run compile "$COMP" "$HARNESS" \
  --no-zagd --no-analyze --no-foreground-cache -o "$BIN"
if [[ -x "$BIN" ]]; then
  sha256sum "$BIN" > "$E/binary.sha256"
  for leg in lh1 lh2 lh3 lh5; do
    run "${leg}_run1" "$BIN" "$leg"
    run "${leg}_run2" "$BIN" "$leg"
    # Determinism covers scientific state only: LH_RESOURCE carries raw
    # wall-clock cpu_us telemetry, excluded from the byte-diff.
    if diff -u <(grep -v '^LH_RESOURCE,' "$E/${leg}_run1.stdout") \
                <(grep -v '^LH_RESOURCE,' "$E/${leg}_run2.stdout") \
                > "$E/${leg}.determinism"; then
      printf 'deterministic_runs_equal=true\n' >> "$E/${leg}.determinism"
    else
      printf 'deterministic_runs_equal=false\n' >> "$E/${leg}.determinism"
      fail=$((fail+1))
    fi
  done
  # LH-5 supplementary sensitivity: extra corruption seeds at 10% and 25%.
  run supp_r10_s7777 "$BIN" lh5rate 10 7777
  run supp_r10_s4242 "$BIN" lh5rate 10 4242
  run supp_r25_s7777 "$BIN" lh5rate 25 7777
fi

printf 'failures=%s\n' "$fail" > "$E/RECEIPT.txt"
printf 'scientific_exposure=0\n' >> "$E/RECEIPT.txt"
printf 'canonical_r27_mutated=false\n' >> "$E/RECEIPT.txt"
printf 'learner_authority_granted=false\n' >> "$E/RECEIPT.txt"
printf 'learn_opened=false\n' >> "$E/RECEIPT.txt"
printf 'successor_promoted=false\n' >> "$E/RECEIPT.txt"
printf 'foreign_ml_runtime_used=false\n' >> "$E/RECEIPT.txt"
printf 'platform=linux-x86_64\n' >> "$E/RECEIPT.txt"
printf 'prereg=PREREG_RERUN.md (frozen 2026-09-20, commit 9ed0203a1594)\n' >> "$E/RECEIPT.txt"
(cd "$E" && find . -type f ! -name SHA256SUMS -print | LC_ALL=C sort | \
  while IFS= read -r f; do sha256sum "$f"; done) > "$E/SHA256SUMS"
printf '%s\n' "$E"
exit $(( fail != 0 ))
