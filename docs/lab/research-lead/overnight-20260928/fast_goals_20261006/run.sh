#!/bin/bash
# Shell orchestration only; every scientific comparison runs inside Zag.
set -euo pipefail
ROOT=$(git rev-parse --show-toplevel)
cd "$ROOT"
. /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh
D=docs/lab/research-lead/overnight-20260928/fast_goals_20261006
C=docs/lab/research-lead/overnight-20260928/contract_unify/cu_full.zag
L=docs/lab/research-lead/overnight-20260928/learned_contracts/src/lcont.zag
tnn_pure_zag_report > "$D/environment.txt"
grep -q 'VERDICT: PURE-ZAG-CLEAN' "$D/environment.txt"
sed '/^\/\/ ============ SECTION: drift harness/,$d' "$C" > "$D/contract_prefix.txt"
sed '/^fn main()i32 {/,$d' "$L" > "$D/flat_prefix.txt"
for p in contract flat; do
  cat "$D/${p}_prefix.txt" "$D/${p}_driver.zag" > "$D/${p}_probe.zag"
  sed '/^\/\/ Appended /,$d' "$D/${p}_probe.zag" > "$D/${p}_check.txt"
  cmp "$D/${p}_prefix.txt" "$D/${p}_check.txt"
  rm "$D/${p}_check.txt" "$D/${p}_prefix.txt"
done
{ git rev-parse HEAD; shasum -a 256 "$TNN_ROOT/.bin/znc" "$C" "$L" "$D/PREREG.md" "$D/contract_driver.zag" "$D/flat_driver.zag" "$D/contract_probe.zag" "$D/flat_probe.zag"; } > "$D/provenance.txt"
for p in contract flat; do
  for i in 1 2 3; do
    if "$TNN_ROOT/.bin/znc" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache "$D/${p}_probe.zag" > "$D/${p}_compile$i.txt" 2>&1; then
      file "$D/${p}_probe" >> "$D/${p}_compile$i.txt"
      file "$D/${p}_probe" | grep -q 'Mach-O.*arm64'
      shasum -a 256 "$D/${p}_probe" >> "$D/provenance.txt"
      if "$D/${p}_probe" > "$D/${p}_run$i.txt" 2>&1; then
        test -s "$D/${p}_run$i.txt"
      else
        cat "$D/${p}_run$i.txt"; exit 1
      fi
    else
      cat "$D/${p}_compile$i.txt"; exit 1
    fi
  done
  cmp "$D/${p}_run1.txt" "$D/${p}_run2.txt"
  cmp "$D/${p}_run1.txt" "$D/${p}_run3.txt"
  shasum -a 256 "$D/${p}_run1.txt" "$D/${p}_run2.txt" "$D/${p}_run3.txt" >> "$D/provenance.txt"
done
cat "$D/contract_run1.txt"
grep '^flat_summary\|^instrumentation_unexpected' "$D/flat_run1.txt"
echo 'Build/run interface completed: inspect measured metrics, not just exit status.'
