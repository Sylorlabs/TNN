#!/usr/bin/env bash
# Determinism proof for the H5 deliberation harness v2 (§12 amendment).
# Rebuilds from source, runs the tiny smoke battery twice per depth config,
# and requires byte-identical outputs (cmp clean). Writes DETERMINISM_LOG.txt.
# Exit 0 only if everything matches.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
LOG="$HERE/DETERMINISM_LOG_V2.txt"
BIN="$HERE/delib_harness_det"
fail=0

log() { printf '%s\n' "$*" | tee -a "$LOG"; }

rm -f "$LOG" "$BIN"
touch "$LOG"
log "H5 delib_harness v2 determinism proof — $(date -u +%Y-%m-%dT%H:%M:%SZ)"
log "source tree: $HERE"

log "--- build ---"
if ! "$HERE/build.sh" "$BIN" >>"$LOG" 2>&1; then
  log "BUILD FAILED"; exit 1
fi
log "build ok: $(sha256sum "$BIN" | cut -d' ' -f1)"

# bonus: rebuild byte-identity of the binary itself (reported, not gated)
"$HERE/build.sh" "$BIN.2" >>"$LOG" 2>&1
if cmp -s "$BIN" "$BIN.2"; then log "binary rebuild: byte-identical"; else log "binary rebuild: DIFFERS (reported only)"; fi
rm -f "$BIN.2"

for cfg in shallow deep adaptive; do
  log "--- config: $cfg ---"
  for run in A B; do
    d="$HERE/det_${run}_${cfg}"
    rm -rf "$d"; mkdir -p "$d"
    "$BIN" "$HERE/smoke_items.jsonl" "$HERE/smoke_${cfg}.cfg" \
      "$d/results.jsonl" "$d/ledger.jsonl" >"$d/stdout.txt" 2>&1
    ec=$?
    log "run $run exit=$ec $(cat "$d/stdout.txt" | tr -d '\n')"
    if [ $ec -ne 0 ]; then log "NONZERO EXIT"; fail=1; fi
  done
  for f in results.jsonl ledger.jsonl; do
    if cmp -s "$HERE/det_A_${cfg}/$f" "$HERE/det_B_${cfg}/$f"; then
      log "cmp $cfg/$f: IDENTICAL"
    else
      log "cmp $cfg/$f: DIFFERS"; fail=1
    fi
  done
  # sanity: correct-counts on the smoke set (reported, not gated)
  correct=$(python3 -c "
import json
n=sum(1 for l in open('$HERE/det_A_${cfg}/results.jsonl') if json.loads(l).get('correct')==1)
print(n)")
  log "smoke accuracy ($cfg): $correct/6 correct"
  log "sha256 results: $(sha256sum "$HERE/det_A_${cfg}/results.jsonl" | cut -d' ' -f1)"
  log "sha256 ledger:  $(sha256sum "$HERE/det_A_${cfg}/ledger.jsonl" | cut -d' ' -f1)"
done

# error-path determinism: malformed item line, twice
log "--- error path ---"
printf '%s\n' '{"id":"BAD1","task_type":"bogus"}' '{"id":"S1","task_type":"admit","input":{"hypotheses":[{"id":"H-A"},{"id":"H-B"}],"evidence":[]},"ground_truth":"H-A"}' > "$HERE/det_err_items.jsonl"
for run in A B; do
  d="$HERE/det_err_$run"; rm -rf "$d"; mkdir -p "$d"
  "$BIN" "$HERE/det_err_items.jsonl" "$HERE/smoke_shallow.cfg" "$d/results.jsonl" "$d/ledger.jsonl" >"$d/stdout.txt" 2>&1
  log "err-run $run exit=$? out=$(tr -d '\n' < "$d/stdout.txt") results=$(tr -d '\n' < "$d/results.jsonl")"
done
if cmp -s "$HERE/det_err_A/results.jsonl" "$HERE/det_err_B/results.jsonl" && cmp -s "$HERE/det_err_A/ledger.jsonl" "$HERE/det_err_B/ledger.jsonl"; then
  log "cmp error-path: IDENTICAL"
else
  log "cmp error-path: DIFFERS"; fail=1
fi
rm -f "$HERE/det_err_items.jsonl"

log "--- verdict ---"
if [ $fail -eq 0 ]; then log "DETERMINISM PROOF: PASS (all cmp clean)"; else log "DETERMINISM PROOF: FAIL"; fi
exit $fail
