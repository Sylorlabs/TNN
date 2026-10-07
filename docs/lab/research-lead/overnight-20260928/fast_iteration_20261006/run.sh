#!/bin/bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
. /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh
D=docs/lab/research-lead/overnight-20260928/fast_iteration_20261006
P=docs/lab/research-lead/overnight-20260928/p6struct/precond.zag
C=docs/lab/research-lead/overnight-20260928/contract_unify/cu_full.zag
tnn_pure_zag_report > "$D/environment.txt"
grep -q 'VERDICT: PURE-ZAG-CLEAN' "$D/environment.txt"
sed '/^fn main()i32 {/,$d' "$P" > "$D/scorer_prefix.txt"
sed '/^\/\/ ============ SECTION: drift harness/,$d' "$C" > "$D/control_prefix.txt"
sed '/^\/\/ ---- problem constants/,$d' "$P" > "$D/method_prefix.txt"
{ git rev-parse HEAD; shasum -a 256 "$TNN_ROOT/.bin/znc" "$P" "$C" "$D/PREREG.md"; } > "$D/provenance.txt"
for p in scorer control method; do
  cat "$D/${p}_prefix.txt" "$D/${p}_driver.zag" > "$D/$p.zag"
  sed '/^\/\/ Appended /,$d' "$D/$p.zag" > "$D/${p}_check.txt"
  cmp "$D/${p}_prefix.txt" "$D/${p}_check.txt"
  rm "$D/${p}_prefix.txt" "$D/${p}_check.txt"
  shasum -a 256 "$D/${p}_driver.zag" "$D/$p.zag" >> "$D/provenance.txt"
  for i in 1 2 3; do
    if znc "$D/$p.zag" > "$D/${p}_compile$i.txt" 2>&1; then
      file "$D/$p" >> "$D/${p}_compile$i.txt"
      file "$D/$p" | grep -q 'Mach-O.*arm64'
      shasum -a 256 "$D/$p" >> "$D/provenance.txt"
      if "$D/$p" > "$D/${p}_run$i.txt" 2>&1; then
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
  shasum -a 256 "$D/${p}_run1.txt" >> "$D/provenance.txt"
  tail -6 "$D/${p}_run1.txt"
done
