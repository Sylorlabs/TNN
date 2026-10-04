# NAMECHECK.md -- Proactive Probe Worker

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

Proactive Probing Worker (subagent, 2026-10-02). Mission: test
PROACTIVE contract self-probing: the learner tests its contract on a
low-stakes probe BEFORE committing to a high-stakes decision, and
revises before the commitment if the probe fails. This is the follow-on
to CONTRACT-DRIFT-DETECT-COMPLETE, whose disclosed boundary is
reactive detection (failures must occur before revision).

## Step 2: Scope

`docs/lab/research-lead/overnight-20260928/proactive_probe/` only.
Frozen assets elsewhere are read only. No paper changes. Nothing
pushed. Pure Zag for all research logic.

## Step 3: Governance notes

- PREREG.md written and committed BEFORE any implementation file,
  PREREG.md alone in its commit (hash recorded below).
- Kill bars are frozen in PREREG.md; no bar moves after results.
- Determinism bar: 3 full runs byte identical (sha256).
- PROBE_ENABLED is a driver set experimental parameter for the
  reactive control arm (arm C), not a cognition mode; same standing as
  REVISION_ENABLED in CDRIFT. Zero modes, bridges, handlers.
- The driver never writes C_REV_REQ (offset 505) or PROBE_FRESH
  (offset 562): both are learner written via c_verify, x_probe_end,
  and x_maybe_revise. Static audit: no `st[505]=` or `st[562]=`
  assignment appears in driver.zag.
- Training episodes reuse the CDRIFT frozen sets, re-frozen in this
  wave's PREREG.md section 3; the tested mechanism (proactive probing
  before high-stakes commitment) is new.
- Prereg commit: 06b649a5f (PREREG.md only; a concurrent worker's
  already-staged learner_wiring files were swept into the same commit
  by git, no implementation of this wave existed at that point).
