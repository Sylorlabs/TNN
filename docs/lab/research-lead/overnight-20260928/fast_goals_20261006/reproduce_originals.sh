#!/bin/bash
# Post-prereg sanity controls, not new learner results.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
. /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh
D=docs/lab/research-lead/overnight-20260928/fast_goals_20261006
C=docs/lab/research-lead/overnight-20260928/contract_unify/cu_full.zag
L=docs/lab/research-lead/overnight-20260928/learned_contracts/src/lcont.zag
# Replace only host-inert output tail; retain all science and original main.
sed '/^  let wrc:i64=_zag_raw_syscall/,$d' "$C" > "$D/original_contract.zag"
printf '  _zag_print(OUT[0..cur]);\n  return 0;\n}\n' >> "$D/original_contract.zag"
sed '/^  let ptr:i64=(_zag_slice_ptr(ob) as i64);/,$d' "$L" > "$D/original_lcont.zag"
printf '  _zag_print(ob[0..at]);\n  if(all!=1){return 1;}\n  return 0;\n}\n' >> "$D/original_lcont.zag"
for p in original_contract original_lcont; do
  for i in 1 2 3; do
    if "$TNN_ROOT/.bin/znc" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache "$D/$p.zag" > "$D/${p}_compile$i.txt" 2>&1; then
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
done
# Compare full raw output to archived outputs; no reliance on run exit alone.
cmp "$D/original_contract_run1.txt" docs/lab/research-lead/overnight-20260928/contract_unify/cu_run1.txt
cmp "$D/original_lcont_run1.txt" docs/lab/research-lead/overnight-20260928/learned_contracts/runs/lcont-run1.txt
{ shasum -a 256 "$D/original_contract.zag" "$D/original_lcont.zag" "$D/original_contract_run1.txt" "$D/original_lcont_run1.txt"; } > "$D/original_provenance.txt"
echo 'Original scenario raw outputs reproduced byte-for-byte with output-only host shims.'
