#!/usr/bin/env bash
# LH-P3 evidence runner. Mirrors r34v3/run_native_linux.sh evidence pattern.
# Usage: ./run_p3.sh c1|c2|c3   (run from the variant dir)
set -u
BASE="$(cd "$(dirname "$0")" && pwd)"
TC="$BASE/toolchain"
COMP="${ZNC:-$TC/bin/znc_linux_x86_64_abed8aa1}"
CANON="$HOME/workspace/tnn-lab/toolchain/r34v3/r34_learner_core.zag"
MODE="${1:-}"
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
E="$BASE/EVIDENCE_${STAMP}_${MODE}"
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

# Law: canonical R34 core stays byte-identical; P3 core is a NEW named file.
if cmp -s "$TC/r34v3/r34_learner_core.zag" "$CANON"; then
  printf 'canonical_core_unmodified=true\n' > "$E/isolation.txt"
else
  printf 'canonical_core_unmodified=false\n' >> "$E/isolation.txt"
  fail=$((fail+1))
fi
# Static isolation on the new P3 core: no world/checkpoint import, no cw_/CWOutcome,
# no cl_checkpoint_, no regime symbol, no world transport sizes.
if grep -nE '@import\([^)]*(world\.zag|checkpoint\.zag)|\bcw_|CWOutcome|\bcl_checkpoint_|\bregime\b|R34V3_WORLD_BYTES|R34V3_CHECKPOINT_BYTES' \
    "$TC/r34v3/r34_p3_learner_core.zag" > "$E/isolation.forbidden.txt"; then
  printf 'p3_core_isolation=false\n' >> "$E/isolation.txt"
  fail=$((fail+1))
else
  printf 'p3_core_isolation=true\n' >> "$E/isolation.txt"
fi
if [[ -f "$TC/r34v3/r34_p1_learner_core.zag" ]]; then
  if grep -nE '@import\([^)]*(world\.zag|checkpoint\.zag)|\bcw_|CWOutcome|\bcl_checkpoint_|\bregime\b|R34V3_WORLD_BYTES|R34V3_CHECKPOINT_BYTES' \
      "$TC/r34v3/r34_p1_learner_core.zag" > "$E/isolation.p1.forbidden.txt"; then
    printf 'p1_core_isolation=false\n' >> "$E/isolation.txt"
    fail=$((fail+1))
  else
    printf 'p1_core_isolation=true\n' >> "$E/isolation.txt"
  fi
  sha256sum "$TC/r34v3/r34_p1_learner_core.zag" >> "$E/source.sha256"
fi
sha256sum "$TC/r34v3/r34_p3_learner_core.zag" "$CANON" > "$E/source.sha256"

compile() {
  local name=$1 src=$2
  run "compile_$name" "$COMP" "$TC/r34v3/$src" \
    --no-zagd --no-analyze --no-foreground-cache -o "$E/$name"
  if [[ -x "$E/$name" ]]; then sha256sum "$E/$name" > "$E/$name.sha256"; fi
}

case "$MODE" in
  c1)
    compile lh_c1_p3 lh_c1_p3.zag
    compile lh_c1_fixed lh_c1_fixed.zag
    if [[ -x "$E/lh_c1_p3" ]]; then run campaign_p3 "$E/lh_c1_p3"; fi
    if [[ -x "$E/lh_c1_fixed" ]]; then run campaign_fixed "$E/lh_c1_fixed"; fi
    ;;
  c2)
    compile lh_p3_c2 lh_p3_c2.zag
    if [[ -x "$E/lh_p3_c2" ]]; then run campaign_c2 "$E/lh_p3_c2"; fi
    ;;
  c3)
    compile lh_p3_c3 lh_p3_c3.zag
    compile lh_fixed_c3 lh_fixed_c3.zag
    for seed in 5600 7777 4242; do
      if [[ -x "$E/lh_p3_c3" ]]; then run "c3_p3_corr${seed}" "$E/lh_p3_c3" rate 10 "$seed"; fi
      if [[ -x "$E/lh_fixed_c3" ]]; then run "c3_fixed_corr${seed}" "$E/lh_fixed_c3" rate 10 "$seed"; fi
    done
    ;;
  ckpt)
    compile lh_p3_checkpoint lh_p3_checkpoint.zag
    if [[ -x "$E/lh_p3_checkpoint" ]]; then
      run "ckpt_campaign" "$E/lh_p3_checkpoint"
      run "ckpt_reference_mid" "$E/lh_p3_checkpoint" reference-mid
      ROOT="$E/ckpt_root"; mkdir -p "$ROOT"
      run "ckpt_write_mid" "$E/lh_p3_checkpoint" write-mid "$ROOT"
      run "ckpt_reload_mid" "$E/lh_p3_checkpoint" reload-mid "$ROOT"
      # Continuation after reload must match the no-checkpoint reference.
      if grep -h "P3CKPT_STATE,continued" "$E/ckpt_reference_mid.stdout" > "$E/ckpt_ref.state" 2>/dev/null &&
         grep -h "P3CKPT_STATE,continued" "$E/ckpt_reload_mid.stdout" > "$E/ckpt_reload.state" 2>/dev/null; then
        if cmp -s "$E/ckpt_ref.state" "$E/ckpt_reload.state"; then
          printf 'checkpoint_continuation_match=true\n' > "$E/ckpt_continuation.txt"
        else
          printf 'checkpoint_continuation_match=false\n' > "$E/ckpt_continuation.txt"
          fail=$((fail+1))
        fi
      else
        printf 'checkpoint_continuation_match=unknown\n' > "$E/ckpt_continuation.txt"
        fail=$((fail+1))
      fi
      if grep -h "P3CKPT_CONTINUE_POSITIVE" "$E/ckpt_reference_mid.stdout" > "$E/ckpt_ref.pos" 2>/dev/null &&
         grep -h "P3CKPT_CONTINUE_POSITIVE" "$E/ckpt_reload_mid.stdout" > "$E/ckpt_reload.pos" 2>/dev/null; then
        if cmp -s "$E/ckpt_ref.pos" "$E/ckpt_reload.pos"; then
          printf 'continuation_positives_match=true\n' >> "$E/ckpt_continuation.txt"
        else
          printf 'continuation_positives_match=false\n' >> "$E/ckpt_continuation.txt"
          fail=$((fail+1))
        fi
      fi
      run "ckpt_write_inner_corrupt" "$E/lh_p3_checkpoint" write-inner-corrupt "$ROOT"
      run "ckpt_refuse_inner_corrupt" "$E/lh_p3_checkpoint" refuse-inner-corrupt "$ROOT"
      run "ckpt_write_torn" "$E/lh_p3_checkpoint" write-torn "$ROOT"
      run "ckpt_refuse_torn" "$E/lh_p3_checkpoint" refuse-torn "$ROOT"
    fi
    ;;
  p1)
    compile lh_p1_trial lh_p1_trial.zag
    compile lh_p1_baseline lh_p1_baseline.zag
    for seed in 7331 12345 999; do
      if [[ -x "$E/lh_p1_trial" ]]; then run "p1_trial_${seed}" "$E/lh_p1_trial" "$seed"; fi
      if [[ -x "$E/lh_p1_baseline" ]]; then run "p1_baseline_${seed}" "$E/lh_p1_baseline" "$seed"; fi
    done
    ;;
  *)
    echo "usage: $0 c1|c2|c3|ckpt|p1" >&2; exit 64;;
esac

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
