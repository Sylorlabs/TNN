# PREREG: COGOPS-LEARNOSC (follow-up to COGOPS-PERIOD C459)

Date: 2026-10-03. Worker: COGOPS-LEARNOSC.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_learnosc/`
Status: FROZEN on commit (this file + NAMECHECK.md committed alone
before any implementation file exists). No amendments after
implementation begins.

## 1. Research question

COGOPS-PERIOD (C459, BUILD-PASS) demonstrated a period-detection
halting vocabulary, with the honest boundary that the detector is
generic machinery (same class as the quiescence check): the learner
did not invent it. What is learner-owned: trajectory history,
outcome record, oscillating procedures. Learner-invented
oscillation detection remains future work.

This worker asks the follow-up the C459 report suggested: can the
learner invent its own oscillation HANDLING from its L outcome
record (the OSC-STATE lines), rather than being handed a
researcher-written detector plus a fixed response? This is the L3
direction: learner-invented, not researcher-provided.

## 2. Design

### 2.1 What is generic machinery (researcher-provided, domain-blind)

- Per-pass trajectory recording: after each execution pass, every
  need's output record is snapshotted into a learner-state region
  (TRAJ). This is mechanical recording, same class as the LSTATE
  dumps: it records, it does not interpret.
- Record equality on integer sequences (already generic:
  the out_eq_snap family).
- Recurrence scan over a recorded integer sequence
  (osc_review): "does the current whole-state snapshot equal an
  earlier one, and at what lag?" This is a domain-blind sequence
  operation. It encodes no oscillation semantics: it would do the
  same on any recorded sequence.
- Single-step plan execution (exec_step_iter, frozen from C442/C6).
- An install/consult hook: the learner-owned driver decides, per
  pass, whether to halt and what answer to emit. The hook itself
  is opaque plumbing.

### 2.2 What is learner-created (from experience, in learner state)

- The trajectory contents: which phases, in which order, for
  which goal. Not in the source.
- The outcome record entries (OSC-STATE lines): per goal, the
  measured lag, the phase records, and whether the entry was
  invented from a fresh trajectory or reused from the record.
- The emitted cycle answer: constructed per goal from its own
  trajectory, open form (lag and phases discovered, never
  enumerated). A period-2 goal and a period-3 goal yield
  structurally different answers.
- The recognition event and the halt decision: computed from the
  learner's own recorded data on the current run.
- The stored association (goal signature to cycle response) that
  drives faster handling on re-presentation.

### 2.3 The honest boundary (what this does NOT claim)

- The learner does NOT invent the concept of oscillation
  detection. The recurrence-scan primitive is generic machinery.
  Learner-invented DETECTION remains future work, as C459 stated.
- The claim is L2 structural learning, not L3 representational
  invention: the learner constructs a new response STRUCTURE
  (per-goal cycle plus halt decision plus stored association)
  from its trajectory, reuses it, and the handling works on new
  oscillatory goals. No new representation, primitive, or
  procedure form is invented; the 12-criterion L3 bar is not
  claimed.
- The difference from C459's detector: C459's detector is a
  FIXED halting condition in generic machinery (researcher
  semantics: periodicity implies halt with a flag), identical for
  every goal. Here the RESPONSE (which lag, which phases, what
  answer, for which goal) exists only in learner state after
  experience. A different oscillation yields a different
  response; the source contains no oscillation-specific
  semantics, no phase values, no period constants, no
  emit-the-cycle rule conditioned on oscillation. The only
  oscillation-adjacent operation in source is the domain-blind
  recurrence scan.
- Red-team note (pre-registered): the attack "osc_handle is a
  researcher-written handler; the learner merely fills in
  lag/phases" is answered three ways. (a) The ret_spec analogy:
  specialize_ret/ret_spec are researcher-written, but the INDEX
  (which facts for which relations) is learner-built from
  episodes and does the cognitive work; likewise here the CYCLE
  is learner-built from the trajectory and does the cognitive
  work (halt plus answer). (b) Causal: without the learner's
  outcome record the handling disappears (the cap fires at 16
  passes); the handling is downstream of the learner's own
  recorded experience. (c) Open form: lag and phases are
  discovered per goal (period-2 vs period-3 produce different
  structures), never selected from a researcher menu.

### 2.4 The learner-owned driver (osc_handle)

New entry point in the additive section of c7_learn.zag. Returns:
-1 = declined (a need is unbindable; mirrors compose_iter),
0 = no handling invented (caller falls back to the generic
compose_iter: quiescence plus the frozen 16-pass cap),
1 = handled by a response invented from this run's trajectory,
2 = handled by a stored response from the outcome record.

Procedure:
1. Plan setup: plan_find, else learn_bindings plus topo_g plus
   plan_new (same as compose_iter). On learn_bindings failure,
   return -1.
2. Stored-response check: look up the goal tag in the outcome
   record. If present, run up to 2 passes via exec_step_iter,
   snapshotting each pass; after each pass compare the snapshot
   to the stored phase prefix (generic equality). On 2
   consecutive matches, emit the STORED cycle and return 2. On
   any mismatch, fall through to step 3 (re-invention may
   overwrite the entry).
3. Invention path: for passes 0..5, run all needs in plan order
   via exec_step_iter, snapshot the whole OUTS state into TRAJ.
   From pass 2 on, run the learner-owned review: nearest-first
   scan for an earlier equal whole-state snapshot.
   - lag 1 means quiescence (a fixpoint, not an oscillation):
     return 0 without inventing anything.
   - lag in 2..3 means oscillation: run ONE confirm pass and
     check the predicted recurrence (snapshot[pass+1] equals
     snapshot[q+1]). If it holds, store the outcome entry
     (goal tag, lag, phase records, src=invention), emit the
     constructed cycle, return 1. If the confirm fails, return 0.
   - lag above 3: decline (out of scope, honest boundary).
   If no recurrence appears by pass 5, return 0.
4. Every step of the handling runs the learner-owned spec
   versions (ret_spec id 2 / vfy_spec id 3); a SPECCHK flag is
   cleared if any executed step falls back to a generic version.

The emitted cycle is verified by the learner's own prediction
(confirm pass), not by an oracle: learner commitment, world
consequence, learner-owned evaluation. For oscillatory goals
there is no oracle agreement bar (C6 established the intended
answer is ill-defined); correctness is internal: the emitted
phases are byte-exact copies of the learner's observed
recurring states, the confirm pass verified the cycle predicts,
and on new goals the phases differ from the training goal's
phases (constructed from new experience, not replayed).

### 2.5 Learner-state layout (additive, no frozen region moved)

L is 16384 bytes; existing use ends at 13276. New regions:
- TRAJ at 13300: [ntraj]; snapshots at 13304+(pass*4+ni)*36,
  pass<8, ni<4; per-need snapshot is [n, v0..v7] (9 i32).
- OUTC at 14500: [nout]; up to 3 entries of 464 bytes at
  14504+e*464: [goal_tag, lag, nph, src, 0,0,0,0, phases:
  up to 3 phases x 4 needs x 9 i32].

### 2.6 Worlds and goals (c7_world.zag = c6_world.zag plus:)

- setup_worldE: world A plus rel 613 seed (771,613,770) and
  2-cycle (772,613,771), (771,613,772); rel 614 markers
  (771,614,770), (772,614,770); rel 615 seed (781,615,780)
  and 3-cycle (782,615,781), (783,615,782), (781,615,783);
  rel 616 markers (781,616,780), (782,616,780), (783,616,780).
  68 facts total.
- ret_ep_pat ids 9..15: (613,770), (613,771), (613,772),
  (615,780), (615,781), (615,782), (615,783).
- vfy_ep_chain ids 7, 8: (771,614,770), (781,616,780).
- mk_goal820_E0: oscillatory self-loop on rel 613 (goal tag
  820): need0 P=(601,621) carrier; need1 P=(613,770) with
  kind-1 SELF-link; need2 T=(S,614,770) via kind-2 fan-out
  from need1. New relation, new phases: the transfer goal.
- mk_goal821_E1: period-3 self-loop on rel 615 (goal tag 821):
  need1 P=(615,780) SELF-link; need2 T=(S,616,780) fan-out.
  Tests the handling is not hardcoded to period-2.
- mk_goal818_D0 (world D, tag 818) and mk_goal816_C0
  (world C, tag 816) are reused unchanged as the training
  oscillation and the convergent control.

### 2.7 Battery stages (c7_main.zag)

- S1A RET-LEARN (world A): ret episodes ids 0..3,
  specialize_ret, SPEC-RET, LSTATE-RET.
- S1B VFY-LEARN (world A): vfy episodes ids 0..3,
  specialize_vfy, SPEC-VFY, LSTATE-VFY.
- S2 OSC-LEARN-D (world D): ret episodes ids 6,7,8,2,
  specialize_ret; vfy episode id 6, specialize_vfy; SPEC and
  LSTATE lines.
- S3 OSC-D0 (goal 818, world D): osc_handle. Predicted:
  invention, how=1, passes=4, lag=2, phases 661/662,
  confirm ok=1, outcome src=0.
- S4 OSC-LEARN-E (world E): ret episodes ids 9..15,2,
  specialize_ret; vfy episodes ids 7,8, specialize_vfy.
- S5 OSC-E0 (goal 820, world E): osc_handle. Predicted:
  invention, how=1, passes=4, lag=2, phases 771/772
  (different values from S3: constructed from new
  experience), confirm ok=1, src=0.
- S6 OSC-E1 (goal 821, world E): osc_handle. Predicted:
  invention, how=1, passes=5, lag=3, phases 781/782/783,
  confirm ok=1, src=0.
- S7 CYCLE-LEARN-C (world C): ret episodes ids 4,5,2,
  specialize_ret; vfy episode id 4, specialize_vfy.
- S8 CONV-816 (goal 816, world C): osc_handle returns 0
  (no recurrence in 6 passes; the walk reaches its fixpoint
  at pass 7..8), fallback compose_iter. Predicted: how=0,
  passes=9, agree=1 vs the carried oracle_cyc816 (byte-exact
  C6 control reproduction: no false positive, no regression).
- S9 REUSE-818 (goal 818, world D again): setup_worldD,
  re-specialize ret/vfy on world D (no new episodes; the
  index is a per-world performance structure, the knowledge
  persists), osc_handle. Predicted: stored-response reuse,
  how=2, passes=2, cycle byte-identical to S3's, match=2,
  outcome entry still src=0. Fewer passes than S3's
  invention run: the outcome record causally drives behavior.
- SUMMARY-LOSC.

Output vocabulary (all dynamic content through the single
preallocated buffer, one flush; no world literals in
c7_learn.zag):
- `Q id=<qn> goal=<gt> how=<0|1|2> passes=<p>`
  (0=generic fallback, 1=invented, 2=reused from record)
- `OSC-CYCLE goal=<gt> lag=<k> nph=<k>
  ph0=[n,v..][n,v..]... ph1=...` (phases in need-index order)
- `OSC-CONFIRM goal=<gt> ok=1`
- `OSC-REUSE goal=<gt> match=2`
- `OSC-STATE goal=<gt> lag=<k> nph=<k> src=<0|1>`
  (the learner-written outcome record line)
- `SPECCHK goal=<gt> spec=1` (every handling step ran a
  learner-owned spec version)
- `AGREE id=S8 a=1` (convergent control vs oracle_cyc816)
- EP / SPEC-RET / SPEC-VFY / LSTATE-RET / LSTATE-VFY /
  STAGE / SUMMARY-LOSC lines as in C6.

## 3. Kill bars (frozen)

- K1 (invention): S3 prints `Q id=S3 goal=818 how=1
  passes=4`, the exact OSC-CYCLE line of Section 7,
  `OSC-CONFIRM goal=818 ok=1`, `SPECCHK goal=818 spec=1`,
  `OSC-STATE goal=818 lag=2 nph=2 src=0`.
- K2 (new oscillatory goal): S5 prints `Q id=S5 goal=820
  how=1 passes=4`, the exact OSC-CYCLE line of Section 7
  with phases 771/772 (different values from S3, proving
  construction from new experience), `OSC-CONFIRM
  goal=820 ok=1`, `SPECCHK goal=820 spec=1`,
  `OSC-STATE goal=820 lag=2 nph=2 src=0`.
- K3 (period-3, not hardcoded): S6 prints `Q id=S6
  goal=821 how=1 passes=5`, the exact OSC-CYCLE line of
  Section 7 with lag=3 and phases 781/782/783,
  `OSC-CONFIRM goal=821 ok=1`, `SPECCHK goal=821 spec=1`,
  `OSC-STATE goal=821 lag=3 nph=3 src=0`.
- K4 (no false positive, no regression): S8 prints `Q
  id=S8 goal=816 how=0 passes=9` and `AGREE id=S8 a=1`
  (byte-exact C6 control behavior).
- K5 (outcome record reuse): S9 prints `Q id=S9 goal=818
  how=2 passes=2`, the OSC-CYCLE line byte-identical to
  S3's, `OSC-REUSE goal=818 match=2`, `SPECCHK goal=818
  spec=1`, `OSC-STATE goal=818 lag=2 nph=2 src=0`.
- K6: 3/3 byte-identical stdout across runs, stderr empty.
- K7: c7_base.zag cmp-identical to c6_base.zag; the first
  <len(c6_learn.zag)> bytes of c7_learn.zag cmp-identical to
  c6_learn.zag (purely additive); word-boundary grep for
  every world/goal/relation identifier empty in
  c7_learn.zag (comments included: no literals anywhere).
- K8: safebin active for every command, PATH=$HOME/safebin,
  `which python3` / `which python` empty, all computation
  pure Zag, pinned znc only.
- K9: zero em/en dash bytes in all lane docs.

Verdict rule: BUILD-PASS requires K1..K9 all PASS. Any
deviation is reported with the observed bytes; a miss on
K1..K5 is INFORMATIVE-FAIL (mechanism), on K6..K9 is
PROCESS-FAIL.

## 4. Implementation plan (post-freeze)

- c7_base.zag: byte copy of c6_base.zag (cmp-verified).
- c7_world.zag: byte copy of c6_world.zag plus the world E
  section (setup_worldE, new pattern ids, mk_goal820_E0,
  mk_goal821_E1). Environment only; all literals live here.
- c7_learn.zag: byte copy of c6_learn.zag plus one additive
  section (TRAJ/OUTC regions, traj_log, traj_state_eq,
  osc_review, osc_confirm, outc_find, outc_store,
  emit helpers, osc_handle). No frozen function modified.
- c7_main.zag: new driver per Section 2.7 (harness; may
  reference pattern/goal ids like c6_main.zag did).
- c7_build.sh: assemble (base+world+learn+main), compile
  with the pinned znc
  `~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`,
  run 3x, cmp, sha256.
- Name the binary's exact expected stdout per Section 7;
  any post-freeze correction follows the transparent
  pre-implementation erratum convention (no silent edits).

## 5. Governance notes

- Pure Zag. safebin mandatory from the first command.
- Opaque identifiers throughout; zero world literals in
  c7_learn.zag (K7).
- Commits local, never pushed, explicit pathspecs only,
  on the current branch; no other lane touched.
- This prereg is adopted as frozen without modification.
  If hand-trace errors are found before implementation,
  they are corrected transparently pre-implementation with
  the correction committed before any implementation file
  exists (the C6 precedent: commit 9c46ce2c7).

## 6. What success would establish (and not)

Would establish: the learner can construct an oscillation
response from its own trajectory/outcome record (L2
structural learning): invention on the training oscillation
(K1), construction from new experience on a new
oscillation with different phases (K2), non-hardcoded lag
discovery on period-3 (K3), no false positives on
convergence (K4), and causal reuse of the outcome record
(K5). The handling is learner-built per goal, not a fixed
researcher detector plus flag.

Would not establish: learner-invented oscillation
DETECTION (the recurrence primitive stays generic
machinery); L3 representational invention; divergent or
3+ node cycles; scaling; behavior under a different cap.

## 7. Frozen exact predictions

Every stdout line the battery prints, in order. (EP counts
and LSTATE/SPEC lines are hand-traced from the world
definitions and the specialize provenance; Q/OSC lines
from the pass-by-pass traces in the worker's design notes.)

```
STAGE S1A RET-LEARN
EP ep=0 ret n=1
EP ep=1 ret n=1
EP ep=2 ret n=1
EP ep=3 ret n=1
SPEC-RET rev=1 nrel=2 ep0=0 ep1=3 nfacts=56
LSTATE-RET nrel=2 ids=601,602 cnts=16,16 prov=0,0,3,56 rev=1
STAGE S1B VFY-LEARN
EP ep=4 vfy v=1
EP ep=5 vfy v=1
EP ep=6 vfy v=1
EP ep=7 vfy v=1
SPEC-VFY rev=1 nrel=3 ep0=4 ep1=7 nfacts=56
LSTATE-VFY nrel=3 ids=601,602,603 cnts=16,16,16 prov=1,4,7,56 rev=1
STAGE S2 OSC-LEARN-D
EP ep=8 ret n=1
EP ep=9 ret n=1
EP ep=10 ret n=1
EP ep=11 ret n=1
SPEC-RET rev=2 nrel=3 ep0=8 ep1=11 nfacts=61
LSTATE-RET nrel=3 ids=601,602,606 cnts=16,16,3 prov=0,8,11,61 rev=2
EP ep=12 vfy v=1
SPEC-VFY rev=2 nrel=4 ep0=12 ep1=12 nfacts=61
LSTATE-VFY nrel=4 ids=601,602,603,608 cnts=16,16,16,2 prov=1,12,12,61 rev=2
STAGE S3 OSC-D0
Q id=S3 goal=818 how=1 passes=4
OSC-CYCLE goal=818 lag=2 nph=2 ph0=[1,611][1,661][1,661] ph1=[1,611][1,662][1,662]
OSC-CONFIRM goal=818 ok=1
SPECCHK goal=818 spec=1
OSC-STATE goal=818 lag=2 nph=2 src=0
STAGE S4 OSC-LEARN-E
EP ep=13 ret n=1
EP ep=14 ret n=1
EP ep=15 ret n=1
EP ep=16 ret n=1
EP ep=17 ret n=1
EP ep=18 ret n=1
EP ep=19 ret n=1
EP ep=20 ret n=1
SPEC-RET rev=3 nrel=5 ep0=13 ep1=20 nfacts=68
LSTATE-RET nrel=5 ids=601,602,606,613,615 cnts=16,16,0,3,4 prov=0,13,20,68 rev=3
EP ep=21 vfy v=1
EP ep=22 vfy v=1
SPEC-VFY rev=3 nrel=6 ep0=21 ep1=22 nfacts=68
LSTATE-VFY nrel=6 ids=601,602,603,608,614,616 cnts=16,16,16,0,2,3 prov=1,21,22,68 rev=3
STAGE S5 OSC-E0
Q id=S5 goal=820 how=1 passes=4
OSC-CYCLE goal=820 lag=2 nph=2 ph0=[1,611][1,771][1,771] ph1=[1,611][1,772][1,772]
OSC-CONFIRM goal=820 ok=1
SPECCHK goal=820 spec=1
OSC-STATE goal=820 lag=2 nph=2 src=0
STAGE S6 OSC-E1
Q id=S6 goal=821 how=1 passes=5
OSC-CYCLE goal=821 lag=3 nph=3 ph0=[1,611][1,781][1,781] ph1=[1,611][1,782][1,782] ph2=[1,611][1,783][1,783]
OSC-CONFIRM goal=821 ok=1
SPECCHK goal=821 spec=1
OSC-STATE goal=821 lag=3 nph=3 src=0
STAGE S7 CYCLE-LEARN-C
EP ep=23 ret n=1
EP ep=24 ret n=1
EP ep=25 ret n=1
SPEC-RET rev=4 nrel=6 ep0=23 ep1=25 nfacts=72
LSTATE-RET nrel=6 ids=601,602,606,613,615,604 cnts=16,16,0,0,0,8 prov=0,23,25,72 rev=4
EP ep=26 vfy v=1
SPEC-VFY rev=4 nrel=7 ep0=26 ep1=26 nfacts=72
LSTATE-VFY nrel=7 ids=601,602,603,608,614,616,605 cnts=16,16,16,0,0,0,8 prov=1,26,26,72 rev=4
STAGE S8 CONV-816
Q id=S8 goal=816 how=0 passes=9
AGREE id=S8 a=1
STAGE S9 REUSE-818
SPEC-RET rev=5 nrel=6 ep0=8 ep1=11 nfacts=61
LSTATE-RET nrel=6 ids=601,602,606,613,615,604 cnts=16,16,3,0,0,0 prov=0,8,11,61 rev=5
SPEC-VFY rev=5 nrel=7 ep0=12 ep1=12 nfacts=61
LSTATE-VFY nrel=7 ids=601,602,603,608,614,616,605 cnts=16,16,16,2,0,0,0 prov=1,12,12,61 rev=5
Q id=S9 goal=818 how=2 passes=2
OSC-CYCLE goal=818 lag=2 nph=2 ph0=[1,611][1,661][1,661] ph1=[1,611][1,662][1,662]
OSC-REUSE goal=818 match=2
SPECCHK goal=818 spec=1
OSC-STATE goal=818 lag=2 nph=2 src=0
SUMMARY-LOSC agree=1 plans_built=4 plans_loaded=2 trials=6 declines=0
```
