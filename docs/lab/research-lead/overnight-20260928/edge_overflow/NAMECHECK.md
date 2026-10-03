# NAMECHECK: Edge-Overflow Sketcher

## Step 0: Toolchain guard (mandatory)

Executed at task start:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returned nothing. Safebin active with 36
allowed tools. Guard-check-done confirmed.

No forbidden executable was invoked during this task. Scope was
specification sketch only; no compilation, no binary execution, no
implementation.

## Scope

SKETCH ONLY. This task develops the edge-overflow alternative to the
fragment-record node enlargement (40 to 72 bytes) specified in
FRAGMENT_RECORD.md section 2. No implementation, no variant build, no
source modification, no preregistration edit.

## Input provenance

- `docs/lab/research-lead/overnight-20260928/fragment_record/FRAGMENT_RECORD.md`
  (commit `8b7b0f12a`): the 8 design-required scalars, the 40 to 72 byte
  enlargement decision, field layout table, edge types 14/15/16.
- `docs/lab/research-lead/overnight-20260928/arch_audit/ARCH_AUDIT.md`
  (commit `ff13a411d`): the audit finding that the edge-overflow
  alternative "should be sketched before the composition preregistration
  freezes."
- `docs/lab/research-lead/overnight-20260928/fragment_guard/FRAGMENT_GUARD.md`
  (commit `0266321cc`): verified field census (40-byte node, 10 fields,
  offsets 0-36); edge types 1-13 in use in the frozen base.

All inputs were read only. No sealed worlds were opened or created.

## Constraints honored

- Sketch only; nothing built.
- Zero em dashes in all deliverables (byte-verified before commit).
- Research paper untouched.
- Frozen source and frozen preregistrations read-only.
- Nothing pushed (local commit only, explicit pathspecs).
- Verdict: EDGE-OVERFLOW-COMPLETE.
