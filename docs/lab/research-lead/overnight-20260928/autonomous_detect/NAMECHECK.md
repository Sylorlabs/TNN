# NAMECHECK.md -- Autonomous Change Detection Worker

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

Autonomous Change Detection Worker (subagent, 2026-10-02). Mission:
test AUTONOMOUS change detection on top of SPEC-MASK-REVISION-COMPLETE.
In that build the revision trigger was driver-scheduled
re-consolidation (disclosed experimental control). Open question:
can the learner DETECT the world change itself (from its own
observable decision stream, since it has no labels in phase 2) and
TRIGGER the mask revision itself?

Design: the learner keeps a ring buffer of its last 4 exec(M)
decision scores; a driver-scheduled x_record_baseline freezes the
baseline mean/spread from phase-1 test scores; on every later
decision the learner's monitor marks a score surprising when its
absolute deviation from the baseline mean strictly exceeds the
baseline spread; 3 consecutive surprising decisions set
DET_REVISE_REQ in learner state (written only by learner logic).
The driver calls x_maybe_revise after each batch as a standing
generic opportunity (heartbeat); the learner revises only when
DET_REVISE_REQ==1. Decision is the learner's; opportunity is the
driver's. Three arms: ARM-STABLE (no world change, no trigger),
ARM-CHANGE (world change, autonomous revision, recovery),
ARM-NOREVISE (detection fires, revision withheld, stays broken).

## Step 2: Constraints honored

- Unfrozen only. No frozen source touched. Sibling
  spec_mask_revision source read for method reuse, adapted with
  disclosed deltas (detection monitor state at offsets 410..431,
  x_record_baseline, x_maybe_revise, ph=5 stable batch in world).
- Pure Zag. Zero Python invocations (F-PYTHON silent).
- Zero em/en dashes in documentation (byte-verified before commit).
- Paper untouched.
- Nothing pushed. Commits local only on tnn-native-lab, with
  EXPLICIT pathspecs (concurrent workers active).
- 0 modes, 0 handlers, 0 semantic cases; op basis {CPY,ADD,SUB,MAX,MIN}
  frozen in prereg and never expanded (F-OP-EXPAND voids the build).
- ADAPT_ON is a driver-set causal control flag, never written by
  the learner.
- Commit order: prereg committed alone before any implementation
  file exists. No amendments.

## Step 3: Development notes

(To be filled after implementation.)

## Step 4: Determinism

(To be filled after runs: 3/3 byte-identical sha256.)
