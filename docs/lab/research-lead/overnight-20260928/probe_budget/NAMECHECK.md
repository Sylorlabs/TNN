# NAMECHECK.md -- Probe Budget Worker

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
znc for all research logic. Shell used only for: safebin setup, file
writes, znc invocation, binary runs, sha256sum, read-only greps, and
git ops. One read-only `/bin/df` call (absolute path, not research
logic) for the disk status below.

Disk status: /home has 7.4G available (3% used). No full disk risk.

## Step 1: Task identity

Probe Budget Worker (subagent, 2026-10-02). Mission: test
EXPERIENCE-SET probe budgets: the learner manages a LIMITED probe
budget and must allocate wisely across time. Parent context:
LEARNER-PROBE-COMPLETE proved the learner can choose WHICH inputs to
probe from an open pool; its disclosed boundary was "Not claimed:
experience-set probe budgets". This wave tests that boundary: 5
probes total across a 30 step stream containing a regime drift.

## Step 2: Scope

`docs/lab/research-lead/overnight-20260928/probe_budget/` only.
Frozen assets elsewhere are read only. No paper changes. Nothing
pushed. Pure Zag for all research logic. Zero modes, bridges,
handlers.

## Step 3: Governance notes

- PREREG.md written and committed BEFORE any implementation file,
  PREREG.md + NAMECHECK.md alone in the prereg commit (hash recorded
  below). No implementation existed at that point.
- Kill bars are frozen in PREREG.md; no bar moves after results.
- Determinism bar: 3 full runs byte identical (sha256, shell
  verified).
- The learner sees only the free surface signal s(t). Hidden info
  values info(t) are world held and revealed only when the learner
  spends a probe. Static audit: pb_learner and pb_learn never call
  pb_info; only the driver resolves info after a spent probe.
- The probe budget (5) is a frozen experimental parameter, not set
  by the learner. What IS learner owned: the spend/no-spend decision
  each step, from learner state alone (prediction, surprise mean,
  remaining budget).
- Prereg commit: 2ae81480a (PREREG.md + NAMECHECK.md only; no
  implementation existed at that point). Disclosure: the commit swept
  in two other workers' already staged files
  (truncate_theorem/PREREG_AMENDMENT1.md and a 4 line
  learner_probes/NAMECHECK.md touch); unrelated to this wave, left
  untouched.
- Implementation commit: (recorded after commit)
