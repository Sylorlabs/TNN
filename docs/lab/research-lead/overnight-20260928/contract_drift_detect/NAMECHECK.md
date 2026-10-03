# NAMECHECK.md -- Contract Drift Detection Worker

## Step 0: Toolchain Guard (mandatory)

Executed at worker startup, before any other work:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `guard-check-done` printed. `which python3 python` returned
NOTHING. All subsequent work runs with PATH=$HOME/safebin. znc is
present in safebin (pinned build per AGENTS.md toolchain lessons).

No forbidden executable invoked at any point. Pure Zag via the pinned
znc. Shell used only for: safebin setup, file concatenation, znc
invocation, binary runs, sha256sum, read-only greps, and git ops.

## Step 1: Task identity

Contract Drift Detection Worker (subagent, 2026-10-02). Mission: test
AUTONOMOUS detection of CONTRACT drift, distinct from mask drift.
AUTONOMOUS-DETECT-COMPLETE detects mask drift via score surprise. Open
question: can the learner detect when a CONTRACT (a typed promise the
learner commits to and acts on) becomes stale, via its own verification
failures, and trigger contract revision autonomously?

## Step 2: Scope

`docs/lab/research-lead/overnight-20260928/contract_drift_detect/`
only. Frozen assets elsewhere are read only. No paper changes. Nothing
pushed. Pure Zag for all research logic.

## Step 3: Governance notes

- PREREG.md is written and committed BEFORE any implementation file.
- Kill bars are frozen in PREREG.md; no bar moves after results.
- Determinism bar: 3 full runs byte identical (sha256).
- Driver never writes CONTRACT_REVISE_REQ (offset 505). The revision
  request is written only by the learner monitor inside c_verify.
  Static audit: no `st[505]=` assignment appears in driver.zag.
- REVISION_ENABLED is a driver set experimental parameter for the
  disabled arm (arm C), not a cognition mode. Zero modes, bridges,
  handlers in the design.
- Contract type tag CONTRACT_TY is a data type marker on the contract
  struct, not a mode.
