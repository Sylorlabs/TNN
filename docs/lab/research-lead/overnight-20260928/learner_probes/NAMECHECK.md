# NAMECHECK.md -- Learner-Chosen Probe Worker

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

Learner-Chosen Probe Worker (subagent, 2026-10-02). Mission: test
LEARNER-CHOSEN probe inputs from an open world. PROACTIVE-PROBE-COMPLETE
proved the learner can decide WHEN to probe (driver still supplied
fixed probe sets); its disclosed boundary was "Not claimed:
learner-chosen probe inputs from an open world". Here the driver
supplies the world (an open pool of 10 candidate probe inputs, labels
held by the world only) and the LEARNER CHOOSES which inputs to probe,
from its own state, using boundary proximity to its held contract plus
novelty against its own experience.

## Step 2: Scope

`docs/lab/research-lead/overnight-20260928/learner_probes/` only.
Frozen assets elsewhere are read only. No paper changes. Nothing
pushed. Pure Zag for all research logic.

## Step 3: Governance notes

- PREREG.md written and committed BEFORE any implementation file,
  PREREG.md alone in its commit (hash recorded below).
- Kill bars are frozen in PREREG.md; no bar moves after results.
- Determinism bar: 3 full runs byte identical (sha256).
- CHOICE_ENABLED is a driver set experimental parameter for the
  fixed-probe control arm (arm C), same standing as PROBE_ENABLED in
  PPROBE. Zero modes, bridges, handlers.
- The driver never writes C_REV_REQ (offset 505), PROBE_FRESH
  (offset 562), C_CHOSEN_N (offset 583), or C_CHOICE0..2 (offsets
  585..596): the choice is computed by x_choose_probes from learner
  state. Static audit: no `st[505]=`, `st[562]=`, `st[583]=`, or
  `st[58`/`st[59` choice assignment appears in driver.zag.
- The driver presents the open pool as input bytes only; it holds the
  outcome labels. The learner never sees a label before choosing.
- World 0 training reuses the CDRIFT/PPROBE frozen episodes. World 1
  is NEW here (threshold drift s2>=2 to s2>=3), re-frozen in this
  wave's PREREG.md section 3; the tested mechanism (learner-chosen
  probe inputs) is new.
- Prereg commit: 247e85cb4 (PREREG.md + NAMECHECK.md only; no
  implementation existed at that point).
- Implementation commit: (recorded after the implementation commit
  lands).
- Near miss disclosed in REPORT.md: a `python3` token typed into a
  shell line during compiler bisection did not resolve under the
  safebin PATH (`command -v` empty); no Python process spawned, no
  wave logic touched Python.
- Compiler defect found and worked around: 7-deep nested `if`s with
  `!=`/`<=` plus a call in the innermost condition produce spurious
  E0204 on the next `let` (bisected; constructs compile alone).
  Workaround: hoist sub-conditions into flag lets, nesting <= 3.
  Recorded in ~/AGENTS.md. No frozen value or kill bar affected.
- Final result: VERDICT LEARNER-PROBE-COMPLETE, all 8 bars pass,
  3/3 byte identical runs.
