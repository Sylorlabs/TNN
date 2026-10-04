# RESULT: DDES V2 steps 7-11 plus t*=0 soundness-hole repair re-run

Wave: wave-20261001-1721pdt. Lane: DDESv2.
Frozen plan: docs/lab/rsi/runs/wave-20261001-1721pdt/DDESv2/
PLAN_DDES_V2_STEPS7_11.md (written before any implementation;
this lane made no commits).

## The three BINDING citation caveats (restated verbatim; the repair
does not remove them)

(1) "a menu of size 2 reproduces the sealed phase-2 outputs"
(2) "World G is signature-identical to F by prereg design"
(3) "the derivation-to-record binding is enforced by offline
reviewer checks only"

Omitting any caveat when citing the frozen V2 BUILD-PASS is
misrepresentation. This lane makes no promotion claim: the verdict
below is BUILD-PASS/BUILD-FAIL on the repair re-run only.

## Evidence-integrity correction (disclosed)

During final verification the worker detected that ddesv2_s7.zag
had been modified after the first binary build: the on-disk
source (RECORD-LOAD emitted only after the class gate passes;
per-field class checks; rec_ok gating records and phase B;
ABL-PROBE-INJECT repositioned after SCAFFOLD-DISCONNECT) no
longer matched the binary that produced the first evidence set
(which emitted RECORD-LOAD before the gate). The first evidence
set is discarded and is not cited anywhere below. The worker
rebuilt the binary from the current source, which matches the
frozen plan on every exact line (notably J: WORLD J /
CLASS-MISMATCH / CONVERGE-FAIL with no RECORD-LOAD line and
zero EXEC lines), re-ran the full battery 3/3, regenerated all
three ablation variants as clean single-edit sed derivations
from the current source (verified by diff: 1, 2, and 1 changed
lines respectively), rebuilt them, and re-ran each 3/3. Every
number, hash, and trace cited below comes from this rebuilt
evidence set, whose binaries were compiled from the exact
source files present in this lane dir. The pre-repair control
binary (ddesv2_pre.zag) was unaffected and its evidence stands
as originally run.

## Verdict: BUILD-PASS (repair re-run)

All nine frozen kill bars (K-R1 through K-R9) pass on the rebuilt
evidence set. Bounded L2 per the frozen honest-boundaries
section; no L3 claim; the frozen V2 BUILD-PASS is neither
promoted nor altered.

## The t*=0 soundness hole and the repair (precise mechanism)

The hole: unrepaired DDES derives target t*=0 on sealed World F,
synthesizes a zero-wait plan [S,OY] (the execution model fires
rules only on W ticks, so OY reads pre-propagation state), while
the analytic predictor (arrival[V*] <= t* = 0) claims pred_h0=1;
the true h0 is eliminated and the trace prints CONVERGE-OK with
no boundary marker. Silent wrong convergence.

The repair (two parts, both generic):

1. Boundary clamp: eff_waits(t*) = max(t*,1), applied in BOTH
   synthesize_plan (the plan performs the waits) and predict
   (the prediction assumes the same wait count). This aligns the
   two models at the boundary instead of branching on any world,
   delay value, or variable id.
2. Loud boundary marker: when the derived target satisfies
   t* == 0, the derivation emits the exact trace line
   FLAG TSTAR-ZERO-BOUNDARY floor=1 between the TARGET line and
   the PLAN line, so the boundary hit is observable, never silent.

Why this closes the hole rather than masking it: the root cause
is a model mismatch (execution fires rules only on W ticks;
prediction assumed observation at raw t*). The clamp removes the
mismatch by making the plan perform the wait count the predictor
assumes, and it does so for every world uniformly. Evidence it
is closure, not masking: (a) the pre-repair control binary
reproduces the silent-wrong pattern on the same sealed World F
(zero-wait plan, no flag, true h0 eliminated, CONVERGE-OK);
(b) the repaired binary converges correctly on F and on a fresh
adversarial world H with a different signature (V*=1, different
rules), where a mask keyed on F's shape could not help;
(c) on red-team world RT2, where the floor genuinely destroys
the discrimination, the same machinery fails LOUDLY
(CONVERGE-FAIL via the p0==p1 predictor alarm) instead of
converging wrongly; (d) the no-clamp ablation keeps the FLAG but
removes the clamp and re-opens silent-wrong convergence,
proving the marker alone is not the closure and the clamp is
load-bearing. A mask would be a branch that detects the world
or the t*==0 value and prints a flag while leaving the
synthesis/prediction mismatch intact; the no-clamp ablation is
exactly that configuration, and it still converges silently
wrong.

## Pre-repair vs post-repair behavior on sealed World F

Pre-repair (ddesv2_pre.zag, 3/3 byte-identical runs, sha256
3226c6f11660db13519f87daa08c92695ded91aa5b9416cede3a0f7ae6313c93):
TARGET V*=2 t*=0 schema=1, NO flag line, PLAN [S,OY],
EXEC real=0, PRED h0=1 h1=0, ELIM h0 (the TRUE h0 in cfg0),
SURVIVE h1 (the false h1), CONVERGE-OK. Silent wrong.

Post-repair (ddesv2_s7.zag, rebuilt, 3/3 byte-identical runs,
sha256
359531a8d94a6fa172597a7d448a14848cb09ba34a60985ed3e607a9a1260743):
TARGET V*=2 t*=0 schema=1, FLAG TSTAR-ZERO-BOUNDARY floor=1,
PLAN [S,W,OY], cfg0 EXEC real=1 PRED h0=1 h1=0 SURVIVE h0
ELIM h1 CONVERGE-OK; cfg1 EXEC real=0 ELIM h0 SURVIVE h1
CONVERGE-OK. Truth survives; convergence is correct.

## Per-step results (steps 7-11), rebuilt evidence set

Step 7 (OOD test):
- World K (identical hypotheses, no frontier): 1
  NO-DISCRIMINATING-PLAN line, 0 convergences claimed. Loud.
- World J (phase-B OOD, stamped class (1,2,3) outside R_F's
  validity class): WORLD J / CLASS-MISMATCH record=(1,2,0)
  world=(1,2,3) / CONVERGE-FAIL, 0 EXEC lines for J (the gate
  refuses before executing; no RECORD-LOAD line, per the frozen
  plan). Loud.
- 0 silent convergences on any OOD world.

Step 8 (ablation), three clean single-edit sed variants of the
current main source (diff line counts vs main: noclamp 1,
noguard 2, zerorecord 1), each 3/3 byte-identical, each built
with exit 0 and 93-byte zagd-only stderr:
- abl_noclamp (clamp line removed, FLAG kept): sha256
  ac0ff81f359edae5b080cc2c8c14f13b296cf57cb97b187899c5f04e129bbcaa.
  On F: FLAG fires, but PLAN [S,OY] (zero waits), EXEC real=0,
  PRED h0=1 h1=0, ELIM h0 (true, cfg0), SURVIVE h1 (false),
  CONVERGE-OK. The marker alone does not close the hole; the
  clamp is load-bearing for soundness.
- abl_noguard (guard condition disabled; phase-2 predict()
  probe injected at the post-disconnect marker, loading its
  own G tables): sha256
  dc2e239e81ee7454c741ead6f1f483a2e5abe04a22cbe2d741b76306dd5430b3.
  1 ABL-PROBE pred=1 line from the phase-2 derivation call,
  0 SCAFFOLD-VIOLATION lines, SCAFFOLD-CALLS 0. Silent scaffold
  bypass demonstrated; the guard is load-bearing for disconnect
  instrumentation.
- abl_zerorecord (record zeroed after write): sha256
  d3c1d19c29ddf078be97caa9d24a90572fe2595a69f3c81d0f34d8a223afa360.
  ABL-ZEROED emitted; phase B on G, I, J: 5 CLASS-MISMATCH
  lines (record=(0,0,0) vs each stamped class) and 5
  CONVERGE-FAIL, 0 EXEC lines in phase B. The record contents
  drive phase B, not hardcoded behavior.

Step 9 (transfer/reuse):
- Sealed World I, both configs, with the adversary-chosen record
  R_H=(schema=1,V*=1,t*=0,tstar_zero=1,pred_h0=1,pred_h1=0):
  RECORD-LOAD-H byte-exact, REPLAN [S,W,OZ], cfg0 EXEC real=1
  PRED-RECORD h0=1 h1=0 SURVIVE h0 ELIM h1 CONVERGE-OK; cfg1
  EXEC real=0 ELIM h0 SURVIVE h1 CONVERGE-OK. The record value
  (V*=1, differing from R_F, frozen in the plan before
  implementation) is carried through the disconnect and drives
  a plan shape ([S,W,OZ]) that differs from F's ([S,W,OY]), so
  hardcoding F's frozen expected values cannot produce these
  lines. This is the protocol-level discriminator the step-6
  attack recommended.

Step 10 (red team round 2):
- RT1 (propagation chain H0=[(X,Z,0),(Z,Y,0)]): both configs
  TARGET V*=1 t*=0 schema=1, FLAG, PLAN [S,W,OZ],
  PRED h0=1 h1=0, truth survives, CONVERGE-OK. The repair's
  single wait suffices on a chain. 2/2 correct.
- RT2 (floor destroys discrimination H0=[(X,Y,1)],
  H1=[(X,Y,0)]): both configs TARGET V*=2 t*=0 schema=1,
  FLAG, PLAN [S,W,OY], PRED h0=1 h1=1, SURVIVE h0, SURVIVE h1,
  CONVERGE-FAIL. The predictor's p0==p1 self-consistency alarm
  converts a would-be silent-wrong case into a loud failure.
  2/2 loud failures, 0 silent wrongs.

Step 11 (governance audit):
- Pure Zag at every stage (implementation, build, run,
  analysis). Toolchain guard Step 0 recorded in NAMECHECK.md;
  `which python3` returns nothing under the safebin PATH.
- Zero em-dash and zero en-dash bytes in all lane files
  (byte-checked per file).
- The three binding caveats are restated verbatim at the top
  of this record; the repair does not remove them.
- Machine-greppable cost fields below; new_semantic_cases=0,
  new_modes=0, new_bridges=0. The class-stamp gate is a generic
  record-vs-environment validity check (no branch on world id,
  delay value, or variable id), of the same machinery class as
  the eff_waits clamp, not a dedicated semantic case.
- Static audit: apply_persisted body contains zero call sites
  of compute_arrivals, compute_frontier, synthesize_plan,
  predict, ddes_world; all five derivation-path functions call
  guard_check on entry; phase-2 trace (after
  SCAFFOLD-DISCONNECT) contains zero derivation markers.
- No commits, no pushes, no wave-lock touch. No promotion
  claims.

## Kill-bar scorecard (rebuilt evidence set)

- K-R1 (compiles): PASS. Pinned znc exit 0 on ddesv2_s7.zag
  and ddesv2_pre.zag; executables produced; build stderr is
  exactly the 93-byte unconditional zagd-availability warning,
  byte-identical to the R2/ddesp2 build evidence.
- K-R2 (hole demonstrated pre-repair): PASS. Frozen
  silent-wrong traces on F, 0 FLAG lines, 2 CONVERGE-OK.
- K-R3 (hole closed post-repair): PASS. 8 derivation targets
  with t*==0, 8 exact FLAG lines, 0 zero-wait plans in the
  repaired trace; truth survives on F and on fresh world H.
- K-R4 (step 7 OOD): PASS. K loud non-convergence; J loud
  CLASS-MISMATCH + CONVERGE-FAIL with 0 EXEC lines and no
  RECORD-LOAD line, per the frozen plan.
- K-R5 (step 8 ablation): PASS. All three ablation
  expectations met exactly as frozen.
- K-R6 (step 9 transfer/reuse): PASS. R_H carried through the
  disconnect; I traces frozen-exact on both configs.
- K-R7 (step 10 red team): PASS. RT1 2/2 correct convergence;
  RT2 2/2 loud failures.
- K-R8 (step 11 governance): PASS. All audit items above.
- K-R9 (determinism): PASS. 5 binaries x 3 runs, all
  byte-identical (sha256 match per binary), exit 0, zero
  stderr bytes on every run.

## Machine-greppable cost fields (K-R8)

binary_bytes=75589
wall_ms_run1=9
wall_ms_run2=10
wall_ms_run3=24
plans_built=10
source_delta_lines=151
new_semantic_cases=0
new_modes=0
new_bridges=0

Source delta is measured against ddesp2.zag (605 lines; this
file 756 lines). The delta is the H/K/RT1/RT2/I/J world
loaders, the second record R_H with rec_ok gating, the
class-stamp gate in apply_persisted, and the extended
two-phase main(); no new dedicated semantic cases, no new
modes, no new bridges. plans_built=10 counts the derivation
plan syntheses (F2, A2, H2, RT1x2, RT2x2); K builds none
(no frontier) and phase B uses REPLAN reconstruction.

## Honest boundaries (unchanged from the frozen plan)

Ceiling remains bounded L2 with persistence: C0-A through C0-D
all fail. The record values are numeric literals in main(),
verified against the derivation trace by exact-line checks
(the step-6 attack-3 finding stands: the surviving statement
is "verified constants persist and are reusable
post-disconnect"); the reconstruction template and the
class-stamp gate are researcher-authored machinery. The repair
does not remove the three binding caveats. RT2's loud failure
is evidence the repair converts a would-be silent-wrong case
into an explicit failure, not evidence of a new capability.
The pre-repair control is a demonstration harness, not a
claim.

## Files (all in docs/lab/rsi/runs/wave-20261001-1721pdt/DDESv2/)

- NAMECHECK.md: toolchain guard Step 0, assignment, lane plan.
- PLAN_DDES_V2_STEPS7_11.md: frozen kill bars (written before
  any implementation).
- ddesv2_s7.zag: main implementation (756 lines, pure Zag).
- ddesv2_pre.zag: pre-repair control (unrepaired derivation).
- abl_noclamp.zag, abl_noguard.zag, abl_zerorecord.zag:
  ablation variants, each a clean single-edit sed derivation
  from the current ddesv2_s7.zag (diff line counts vs main:
  1, 2, 1). Edits: clamp line removed; guard condition
  disabled plus probe injected at // ABL-PROBE-INJECT (loads
  its own G tables, calls predict during phase 2); record
  zeroing injected at // ABL-ZERORECORD-INJECT.
- ddesv2_s7_bin (75589 bytes), ddesv2_pre_bin (29780 bytes),
  abl_noclamp_bin, abl_noguard_bin, abl_zerorecord_bin.
- s7_run1/2/3.txt (sha256
  359531a8d94a6fa172597a7d448a14848cb09ba34a60985ed3e607a9a1260743),
  pre_run1/2/3.txt (sha256
  3226c6f11660db13519f87daa08c92695ded91aa5b9416cede3a0f7ae6313c93),
  abl_noclamp_run1/2/3.txt (sha256
  ac0ff81f359edae5b080cc2c8c14f13b296cf57cb97b187899c5f04e129bbcaa),
  abl_noguard_run1/2/3.txt (sha256
  dc2e239e81ee7454c741ead6f1f483a2e5abe04a22cbe2d741b76306dd5430b3),
  abl_zerorecord_run1/2/3.txt (sha256
  d3c1d19c29ddf078be97caa9d24a90572fe2595a69f3c81d0f34d8a223afa360),
  all byte-identical 3/3 per binary.
- s7_build.stderr / pre_build.stderr / abl_*_build.stderr:
  each exactly the 93-byte zagd-availability warning.
- All run .err files: 0 bytes.
- RESULT_DDES_V2_STEPS7_11.md: this record.
