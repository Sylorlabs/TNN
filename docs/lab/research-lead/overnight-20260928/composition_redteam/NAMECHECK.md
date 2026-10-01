# NAMECHECK: Composition Memory Red Team

## Step 0: Toolchain Guard

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

Result: `which python3 python` returned nothing. Guard check done.
Safebin active for all subsequent commands.

## Scope

Red-team analysis ONLY. No implementation, no source modification, no
binary built. Read-only inspection of design documents and prior
reports via grep/sed.

## Input provenance

- Composition memory design: `docs/lab/research-lead/overnight-20260928/composition_memory/COMPOSITION_MEMORY_DESIGN.md` (commit `19fa59b6f`, DRAFT-NOT-FROZEN)
- V2 hole probe: `docs/lab/research-lead/overnight-20260928/v2_hole/V2_HOLE.md` (commit `705833a27`, V2-HOLE-COMPLETE: CONFIRMED)
- Verification criterion: `docs/lab/research-lead/overnight-20260928/verification_criterion/VERIFICATION_CRITERION.md` (commit `c2a48bee6`)
- Blame assignment: `docs/lab/research-lead/overnight-20260928/blame_assignment/BLAME_ASSIGNMENT.md` (commit `0917f3e25`)
- Lifetime protocol v2: `docs/lab/research-lead/overnight-20260928/lifetime_protocol/LIFETIME_PROTOCOL_V2.md` (commit `dd745851e`)

## Constraints honored

- No frozen source modified. No sealed worlds opened.
- Research paper untouched.
- Zero em dashes in deliverables (byte-verified before commit).
- Nothing pushed; local commit only.
- Analysis only; the exploit path is demonstrated conceptually, not built.

## Verdict

COMPOSITION-REDTEAM-COMPLETE with verdict VULNERABLE.
