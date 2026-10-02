# NAMECHECK: H2-v2 Prereg Designer

## Step 0: Toolchain Guard (mandatory)

Date: 2026-10-01 (UTC). Worker: H2-v2 Prereg Designer (subagent).

Safebin activation performed before any work:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum \
         git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `guard-check-done` with NO python3/python paths printed.
Forbidden executables are not resolvable in this worker's PATH.

## Scope Declaration

**PREREG DESIGN ONLY.** This worker designs the H2-v2 preregistration.
It does not implement drivers, does not build worlds, does not run
TNN-2, does not modify frozen cognition, does not open any sealed
world file. Any forbidden executable invocation would be PROCESS-FAIL;
none occurred.

## Authorization Chain

- H2 evaluation VOID: commit `72173fe11` (H2-EVAL-VOID).
- H2 prereg frozen (VOID, historic): commit `c15a47d63`.
- Micah's H2-v2 directive: 2026-10-01 (fresh wave; frozen cognition
  unchanged; evaluator-side t2_sig correction permitted; fresh prereg;
  fresh sealed worlds; worlds must omit direct query FACTs;
  TRIAL_ENTERED > 0 prerequisite; no trial execution means no H2
  verdict; original H2 worlds and results remain VOID historically).

## Files Produced

- `H2V2_PREREG.md` (DRAFT, to be frozen; freeze must precede world building)
- `NAMECHECK.md` (this file)

## Constraints Honored

- Frozen TNN-2 cognition untouched (source only read, never modified).
- Pure shell for file operations; no computational executables used.
- Zero em dashes in all documentation.
- Paper untouched (`docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md` not opened).
- Nothing pushed (local commit only).
- No sealed world files opened (none exist yet for H2-v2).

## Verdict

**H2V2-PREREG-COMPLETE.** Design delivered; DRAFT prereg committed.
Freeze and world building belong to later workers under the freeze
procedure in section 15 of the prereg.
