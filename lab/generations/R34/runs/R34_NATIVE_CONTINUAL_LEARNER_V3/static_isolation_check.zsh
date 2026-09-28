#!/bin/zsh
set -u

BASE=${0:A:h}
CORE="$BASE/r34_learner_core.zag"
HARNESS="$BASE/r34_continuing_harness_v3.zag"
fail=0

check_absent() {
  local pattern=$1
  local label=$2
  if rg -n -- "$pattern" "$CORE" >/dev/null 2>&1; then
    print -r -- "FAIL,$label"
    rg -n -- "$pattern" "$CORE"
    fail=$((fail+1))
  else
    print -r -- "PASS,$label"
  fi
}

check_present() {
  local pattern=$1
  local file=$2
  local label=$3
  if rg -n -- "$pattern" "$file" >/dev/null 2>&1; then
    print -r -- "PASS,$label"
  else
    print -r -- "FAIL,$label"
    fail=$((fail+1))
  fi
}

check_present '^@import\("\.\./R33_CONTINUING_LIFE_V1/observation\.zag"\)$' "$CORE" learner_imports_observation_only
check_absent '@import\(".*world\.zag"\)' learner_no_world_import
check_absent '@import\(".*checkpoint\.zag"\)' learner_no_checkpoint_import
check_absent '\bcw_' learner_no_world_calls
check_absent '\bCWOutcome\b' learner_no_world_outcome_type
check_absent '\bcl_checkpoint_' learner_no_outer_checkpoint_calls
check_absent '\bregime\b' learner_no_regime_symbol
check_absent 'R34V3_WORLD_BYTES|R34V3_CHECKPOINT_BYTES' learner_no_world_transport_sizes

check_present '@import\("\.\./R33_CONTINUING_LIFE_V1/world\.zag"\)' "$HARNESS" harness_owns_world
check_present '@import\("\.\./R33_CONTINUING_LIFE_V1/checkpoint\.zag"\)' "$HARNESS" harness_owns_checkpoint
check_present '\bcw_change\b' "$HARNESS" harness_owns_regime_change
check_present '\br34v3_accept\b' "$CORE" learner_accepts_delayed_scalar_outcome
check_present 'action_id!=s\.\*\.pending_action' "$CORE" learner_binds_credit_to_pending_action

print -r -- "R34V3_STATIC_ISOLATION_FAILURES,$fail"
exit $(( fail != 0 ))

