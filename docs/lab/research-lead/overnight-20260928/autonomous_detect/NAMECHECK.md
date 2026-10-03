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

1. The prereg hand derivations were done before any implementation
   existed. The first full build reproduced every one with zero
   source changes after the initial pre-run cleanup (one unused
   driver local `ereq` removed; it only triggered a B0103 warning).
2. Build: `cat learner.zag world.zag driver.zag > ad_full.zag`
   (1210 lines), then `znc ad_full.zag -o ad_bin`. Build exit 0.
   Only diagnostics: the benign zagd-unavailable notice plus three
   A0101 off-by-one heuristic warnings in x_revise_masks/x_recall
   (analyzer cannot prove the bounds; indices are provably in
   range, same as the spec_mask_revision build).
3. Output path follows the AGENTS.md stdout workaround: numbers
   formatted directly into one preallocated 64KB buffer with
   cursor-returning helpers (ob_app/ob_i32), single
   `_zag_raw_syscall(1,1,ptr,len)` write loop. No `_zag_print`
   anywhere. Stdout verified: 187 lines, 0 NUL bytes (tr/cmp
   check), ends with AUTONOMOUS-DETECT-END.
4. State uses u8 buffers with get32/set32 only; no `as *i32` slice
   construction. Register file is an 8-byte scratch (2 registers).
   Mask bit tests use integer division, not bitwise ops.
5. Key result shape: baseline mean=9 spread=4 from phase-1 test
   scores [13,5,13,5]; stable phase-5 scores deviate exactly 4,
   never strictly exceeding, so no false trigger; stale-mask
   scores collapse to 0 (deviation 9 > 4) and the learner sets
   DET_REVISE_REQ at the 3rd consecutive surprise (ZT id=23 line
   shows surp=1 req=1); x_maybe_revise swaps masks 48<->12 to
   12/48 with REV_PTR 24 and revs=1; Z-CHANGE 4/4 with M1 reused.
   The NOREVISE control shows detection without revision stays at
   2/4, attributing recovery to the learner-triggered revision.

## Step 4: Determinism

- No RNG anywhere. Fixed candidate order, first-max tie-breaking,
  ascending threshold sweeps, deterministic monitor logic.
- ad_run1/2/3.txt sha256 identical:
  33a7b29f15194c2d8a031642f7e80276c15d4ccc38968c51a69cecdf92a055c6
  (all three). K-AD-7 PASS.
