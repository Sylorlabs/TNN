#!/bin/zsh
set -u

ROOT=${0:A:h:h}
cd "$ROOT" || exit 90

fail=0
run_lane() {
  local label=$1
  shift
  print -r -- "[$label] $*"
  "$@"
  local ec=$?
  print -r -- "[$label] exit=$ec"
  if (( ec != 0 )); then fail=$((fail+1)); fi
  return 0
}

# Keep the frontier sequence deterministic: qualify the isolated learner first,
# then continue the two historical recovery lanes. None of these steps opens
# learn, mutates canonical R27, or executes Python/foreign ML runtimes.
if [[ -e Research/R34_NATIVE_CONTINUAL_LEARNER_V3/core_probe_bin ]]; then
  unlink Research/R34_NATIVE_CONTINUAL_LEARNER_V3/core_probe_bin || fail=$((fail+1))
fi
if [[ -e Research/R34_NATIVE_CONTINUAL_LEARNER_V3/r34_v3_test ]]; then
  unlink Research/R34_NATIVE_CONTINUAL_LEARNER_V3/r34_v3_test || fail=$((fail+1))
fi
run_lane R34_V3_STATIC zsh Research/R34_NATIVE_CONTINUAL_LEARNER_V3/static_isolation_check.zsh
run_lane R34_V3 zsh Research/R34_NATIVE_CONTINUAL_LEARNER_V3/run_native.zsh
run_lane N17_R25_R26 zsh Research/R33_REMEDIATION_20260915T2152Z/run_exact_archive_sweep.zsh
run_lane V91 zsh Research/R33_NATIVE_N17_R27_CONTINUITY/V91_SEMANTIC_KAT/run_v91_text_recovery_scan.zsh

latest_v3=$(ls -dt Research/R34_NATIVE_CONTINUAL_LEARNER_V3/EVIDENCE_* 2>/dev/null | head -1)
report=Research/TNN_FRONTIER_LATEST_RESULT.md
{
  print -r -- '# TNN frontier latest result'
  print -r -- ''
  print -r -- "Generated UTC: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  print -r -- ''
  print -r -- "Aggregate lane failures: $fail"
  print -r -- ''
  if [[ -n ${latest_v3:-} ]]; then
    print -r -- '## R34 V3 latest evidence'
    print -r -- ''
    print -r -- "Evidence directory: \`$latest_v3\`"
    print -r -- ''
    if [[ -f "$latest_v3/RECEIPT.txt" ]]; then
      print -r -- '```text'
      cat "$latest_v3/RECEIPT.txt"
      print -r -- '```'
    fi
    if [[ -f "$latest_v3/continuation.diff" ]]; then
      print -r -- ''
      print -r -- 'Fresh-process continuation:'
      print -r -- '```text'
      cat "$latest_v3/continuation.diff"
      print -r -- '```'
    fi
    if [[ -f "$latest_v3/campaign.stdout" ]]; then
      print -r -- ''
      print -r -- 'Campaign tail:'
      print -r -- '```text'
      tail -45 "$latest_v3/campaign.stdout"
      print -r -- '```'
    fi
  fi
  print -r -- ''
  print -r -- '## Claim boundary'
  print -r -- ''
  print -r -- 'No learner authority, successor promotion, canonical R27 mutation, scientific exposure, or LLM-superiority claim is implied by this runner.'
} > "$report"

print -r -- "$report"
exit $(( fail != 0 ))
