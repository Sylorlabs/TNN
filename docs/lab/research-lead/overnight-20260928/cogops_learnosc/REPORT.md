# REPORT: COGOPS-LEARNOSC (follow-up to COGOPS-PERIOD C459)

Date: 2026-10-03. Worker: COGOPS-LEARNOSC.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_learnosc/`
Prereg: frozen commit (PREREG.md + NAMECHECK.md, committed alone
before any implementation file existed). No amendments after
implementation began; erratum E1 below is a post-execution
correction, not a prereg change. Implementation commit follows
this report.

## Verdict: BUILD-PASS (K1..K9 all PASS)

The learner invents an oscillation response from its own
trajectory/outcome record, and the handling works on new
oscillatory goals. On the training oscillation (goal 818, world
D) the learner-owned driver halts after 4 passes (generic cap is
16; quiescence is unreachable) and emits the 2-phase cycle it
constructed from its trajectory, after its own confirm pass
verified the cycle predicts. On a fresh period-2 oscillation
with a new relation and new phases (goal 820, world E) it
invents a new response from the new trajectory (4 passes,
phases 771/772, not replayed). On a fresh period-3 oscillation
(goal 821, world E) it discovers lag 3 and emits 3 phases
(5 passes): the handling is not hardcoded to period-2. The
convergent control (goal 816, world C) is untouched by the
invention path: no recurrence in 6 passes, generic fallback,
passes=9, oracle agree=1, byte-exact C6 behavior. On
re-presentation of goal 818 the outcome record drives reuse:
2 passes, cycle byte-identical to the invented one.

## Note on the C459 source material

COGOPS-PERIOD's REPORT.md (C459) could not be located in the
workspace: the `cogops_period` lane directory exists but is
empty, and no file in the reachable trees mentions C459 or
OSC-STATE. This worker designed from the parent handoff facts
(period-detection halting vocabulary demonstrated; the
detector is generic machinery; learner-owned: trajectory
history, outcome record, oscillating procedures) plus the
verified c5/c6 lineage sources. If the C459 report surfaces,
its OSC-STATE format should be cross-checked against the
OUTC/OSC-STATE record defined here.

## Kill bar assessment (observed vs frozen prediction)

| Bar | Frozen prediction | Observed | Result |
|-----|-------------------|----------|--------|
| K1 | S3: `Q id=S3 goal=818 how=1 passes=4`, exact OSC-CYCLE (phases 661/662), `OSC-CONFIRM goal=818 ok=1`, `SPECCHK goal=818 spec=1`, `OSC-STATE goal=818 lag=2 nph=2 src=0` | byte-exact on all five lines | PASS |
| K2 | S5: `Q id=S5 goal=820 how=1 passes=4`, OSC-CYCLE with phases 771/772, confirm ok=1, spec=1, `OSC-STATE goal=820 lag=2 nph=2 src=0` | byte-exact | PASS |
| K3 | S6: `Q id=S6 goal=821 how=1 passes=5`, OSC-CYCLE lag=3 phases 781/782/783, confirm ok=1, spec=1, `OSC-STATE goal=821 lag=3 nph=3 src=0` | byte-exact | PASS |
| K4 | S8: `Q id=S8 goal=816 how=0 passes=9`, `AGREE id=S8 a=1` | byte-exact | PASS |
| K5 | S9: `Q id=S9 goal=818 how=2 passes=2`, OSC-CYCLE byte-identical to S3's, `OSC-REUSE goal=818 match=2`, spec=1, `OSC-STATE goal=818 lag=2 nph=2 src=0` | byte-exact | PASS |
| K6 | 3/3 byte-identical stdout, stderr empty | sha256 f0d1cf5f x3; .err 0 bytes | PASS |
| K7 | c7_base cmp-identical to c6_base; c7_learn = c6_learn ++ additive (prefix cmp); zero world literals in c7_learn | all verified (one documented idiom, see below) | PASS |
| K8 | safebin, no python, pure Zag, pinned znc | verified | PASS |
| K9 | zero em/en dash bytes in lane docs | byte-verified clean | PASS |

K7 note: the only word-boundary numeric collisions in
c7_learn.zag are three `z_alloc(640)` buffer-size literals
(two frozen, one in the additive section, same idiom): byte
counts for the OUTS buffer, not world references. Every
other literal in the additive section is structural (L
offsets, strides, small ints).

Per-query detail (all lines byte-exact vs PREREG Section 7):
- S3: how=1 passes=4; cycle ph0=[1,611][1,661][1,661]
  ph1=[1,611][1,662][1,662]; confirm ok=1; spec=1;
  outcome src=0 (invented).
- S5: how=1 passes=4; cycle phases [1,771]/[1,772];
  confirm ok=1; spec=1; src=0. The phases differ from
  S3's: constructed from the new trajectory, not replayed.
- S6: how=1 passes=5; lag=3; phases
  [1,781]/[1,782]/[1,783]; confirm ok=1; spec=1; src=0.
- S8: how=0 passes=9; agree=1 (oracle_cyc816).
- S9: how=2 passes=2; cycle byte-identical to S3;
  match=2; spec=1; outcome entry still src=0.
- SUMMARY-LOSC: agree=1 plans_built=4 plans_loaded=2
  trials=6 declines=0.

## Erratum E1 (transparent; prereg NOT silently amended)

The frozen prediction said `EP ep=7 vfy v=1`; observed
`EP ep=7 vfy v=0`. Hand-trace error by the worker: the
default verify chain's second step (614,603,629) matches no
world-A fact (rel 603 objects at subject 614 are 623 and
633). The binary is correct: c6's own recorded run prints
`EP ep=7 vfy v=0` for the identical episode, byte for byte.
No kill bar involves EP lines. This is the direct analog of
C6's erratum E1: a hand-computation gap, behavior as
designed.

## Toolchain disclosure

safebin active for every command (PATH=$HOME/safebin exported
per invocation; the lane's safebin_setup script does not
exist in this checkout, so the pre-existing $HOME/safebin
was verified directly: 49 entries, no python3/python;
substance of the guard satisfied and recorded in NAMECHECK
Step 0). `which python3` / `which python` return nothing
before and after; pinned znc
`src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(2026.07.0-dev) for the single build. All computation pure
Zag; shell only for znc/binary/git/assembly/byte
verification. Zero forbidden-executable invocations, no
near-misses. New Zag scanned for the `while.*!(` negated
conjunction pattern: clean. Git writes via /usr/bin/git
absolute path, explicit pathspecs, current branch only,
nothing pushed.

## Evidence detail

Invention, not detection (K1): on goal 818 the learner runs
passes 0..2 through its own spec procedures (ret_spec id 2,
vfy_spec id 3; SPECCHK flag stays 1), snapshots each pass,
and at pass 2 its review finds snapshot[2]==snapshot[0]
(nearest-first; lag 2, not the fixpoint lag 1). It then
runs a confirm pass predicting snapshot[3]==snapshot[1];
the prediction holds, so it stores the outcome entry and
emits the constructed cycle. The emitted phases are
byte-exact copies of its observed recurring states. Passes
used: 4 vs the 16-pass generic cap.

Transfer, not replay (K2): goal 820 uses a fresh relation
(613) with fresh phases. No outcome entry exists, so the
learner re-runs the invention path on the new trajectory
and constructs a different cycle (771/772). If the
handling were a memorized answer, the phases would match
S3's; they do not.

Not hardcoded to period-2 (K3): goal 821's 3-cycle yields
no recurrence at passes 2 (snapshots all distinct), lag 3
at pass 3, confirm at pass 4, 3-phase emission. The lag is
discovered; the source contains no period constant.

No false positive (K4): goal 816's walk (612..618) shows no
recurrence in 6 passes and no lag-1 snapshot equality, so
the learner invents nothing and returns 0; the generic
composer reproduces C6 exactly (passes=9, agree=1).

Causal reuse (K5): on re-presentation the learner finds the
stored entry, runs 2 passes, matches the stored phase
prefix twice, and emits the stored cycle without
re-inventing. 2 passes < 4 (invention) < 16 (cap): the
outcome record drives behavior; without it the handling
would cost the full invention path.

## What this establishes (and does not)

Establishes: the learner can construct an oscillation
response from its own trajectory and outcome record (L2
structural learning). The response (which lag, which
phases, what answer, for which goal) exists only in learner
state after experience; a different oscillation yields a
different response; the source holds no
oscillation-specific semantics beyond the domain-blind
recurrence scan. The handling is verified by the learner's
own prediction (confirm pass), not by an oracle, and every
handling step executes learner-owned spec procedures.

Does not establish: learner-invented oscillation DETECTION
(the recurrence primitive remains generic machinery, same
class as the quiescence check); L3 representational
invention (no new representation, primitive, or procedure
form; the 12-criterion bar is not claimed); divergent or
3+ node cycles; lag above 3 (declined by design); scaling;
behavior under a different cap. The C459 detector
comparison rests on the handoff summary, since the C459
report was not found (see note above).

## Deliverables

All in `docs/lab/research-lead/overnight-20260928/cogops_learnosc/`:
PREREG.md (frozen), NAMECHECK.md (Step 0), c7_base.zag
(cmp-identical to c6_base.zag), c7_world.zag (c6 world plus
world E: rels 613/614 2-cycle, 615/616 3-cycle; goals 820,
821), c7_learn.zag (c6_learn prefix cmp-identical plus the
additive osc_handle section), c7_main.zag, c7_build.sh,
c7_full.zag (assembled; exactly one `fn main`), c7_bin,
c7_compile.txt, c7_run1/2/3.txt (sha256 f0d1cf5f x3) +
.err (empty), REPORT.md (this file).

## Recommended follow-ups (for the parent, not decided here)

1. Learner-invented DETECTION (the stated C459 future
   work): the recurrence scan is still generic machinery.
   The trajectory/outcome record built here is the
   substrate it would learn from.
2. Lag above 3, 3+ node cycles, divergent (growing)
   trajectories: untested; the current driver declines
   them to the generic fallback.
3. Cross-goal transfer of the response: S9 reuses the
   stored cycle for the same goal; whether a stored
   response can bootstrap handling of a structurally
   similar but new oscillation (analogy, not replay) is
   open.
4. Full ablation of the outcome record (zero it and
   re-run S9) to complete the causal story K5 starts.
5. Locate or reconstruct the C459 report to cross-check
   the OSC-STATE record format against C459's L outcome
   record.
