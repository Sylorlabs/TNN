# PREREG: H-PI-REV2 step 7 OOD on fresh sealed adversary worlds (FROZEN)

Status: FROZEN (drafted wave-20261001-2021pdt, HPIREV2-S7 lane;
coordinator commits this document alone before any world file,
implementation file, transcript, binary, or build log for step 7
exists in the lane; commit-order self-check applies; UNVERIFIABLE
ORDERING voids this prereg). No world design, no implementation, no
execution follows this freeze in this wave; execution happens in a
later wave under this text. Any further amendment must be committed
transparently and re-frozen before execution; no bar may be altered
after seeing results. Builders report BUILD-PASS/BUILD-FAIL only.

This prereg defines step 7 of the 11-step promotion pipeline for the
H-PI-REV2 mechanism (pi_revise2/proc_revise2.zag, committed 847a8f10f,
wave-20260929-2321pdt; unchanged), which holds step-5 PASS under the
amended prereg (wave-20261001-2021pdt, 8/8 bars, independent red team:
EVIDENCE HOLDS; original BASELINE-FAIL unchanged; bounded-L2 ceiling,
not L3) and step-6 PASS on re-execution under amendment K-AX2
(wave-20261001-2021pdt, all 13 bars: K-AX1 killed A1, K-AX2 killed A2
with b4b_enumerated=88728 vs 5, K-ABL1 showed the SPECIALIZE template
load-bearing with d1_fails_total=2, 8 step-5 bars preserved,
architecture bars held).

## Provenance and the step-7 choice

Step 6 attacked the two load-bearing step-5 claims on frozen fixtures
and pinned, via K-ABL1, that the researcher-authored SPECIALIZE
template carries the repair. The step-6 design rationale stated this
directly: the ablation determines what OOD should vary and what it
cannot claim. Step 7 therefore varies the template's usage regime
along four dimensions while freezing everything else: the conflict
alphabet and position (family A), the conflict count (family B), the
input length (family C), and the template shape the conflict rule
must compose with (family D). The worlds are designed post-freeze by
an independent adversary, so the mechanism faces byte regimes,
positions, counts, lengths, and shapes it has never seen. Step 7
cannot claim template invention, representational invention, or L3:
the ceiling stays bounded L2, and a PASS here means the bounded-L2
revision mechanism generalizes within the tested regimes, nothing
more.

## The question (one mechanism, one question)

Does the frozen revision mechanism (diagnosis plus SPECIALIZE plus
conflict rule) revise correctly and cheaply on fresh sealed worlds
that vary the dimensions K-ABL1 pinned as load-bearing, or does its
competence collapse outside the frozen fixtures, bounding or killing
the bounded-L2 claim?

## Frozen reference points (not re-decided here)

- Frozen mechanism: proc_revise2.zag at 847a8f10f, byte-identical.
- Frozen fixtures: T = ("abc"->"ccc"), ("xy"->"yy"),
  ("defg"->"gggg"); F1r = ("rab"->"rrr") with adversary byte 114;
  F1r-reuse = ("rqw"->"rrr").
- Frozen fixture alphabet A_frozen = {97,98,99,100,101,102,103,113,
  114,119,120,121}: every byte appearing in any frozen fixture input
  or output.
- Frozen conflict regime: single conflict, pos=0, input length <= 4.
- Frozen solution shape S_frozen (per AMENDMENT_KAX2.md): nested
  IF(byte-equality(0,b), alt, ...) with one branch per diagnosed
  conflict, the frozen alt (first dsearch fit on F alone) in every
  then-branch, and v_old in the final else position. On the frozen
  set this is IF(byte-equality(0,114), alt,
  IF(byte-equality(0,120), alt, v_old)).
- Frozen measured cost: revision_evals=5; blind template-aware
  enumeration needs 88,728 evals on the frozen set (S6C).

## OOD family requirements (the adversary designs the worlds, not this prereg)

Four worlds, one per family. Each world is a directory with five
files: TW.txt (3 base pairs, the T analogue), FW.txt (1 counterexample
pair, the F1r analogue), RW.txt (1 held reuse pair, the F1r-reuse
analogue; sealed from the revision phase until the revision
completes), CONFLICT.txt (the declared conflict set, the intended
rule R_w stated in words, and for family D the intended structure
S_w), EW.txt (exactly 5 expectation pairs: the 3 base pairs as
updated by R_w, plus FW, plus RW; the K-SB4a analogue). Pair notation
matches the frozen fixtures ("abc"->"ccc"), one pair per line.

- Family A (novel conflict alphabet and position): single conflict;
  all input bytes in TW, FW, and RW are disjoint from A_frozen; the
  declared conflict position is not 0; input lengths <= 4. Isolates
  whether the conflict rule generalizes beyond the frozen bytes and
  pos=0. This family is the hardcoding detector: a mechanism with
  pos=0 or byte 114/120 baked in fails here.
- Family B (multi-conflict): FW presents two simultaneous conflicts:
  two distinct declared (pos,byte) pairs in one input; input lengths
  <= 4. R_w: an input matching either declared conflict maps to the
  matched byte repeated to input length; otherwise the base program
  applies. RW's input matches the second declared conflict.
  Isolates single-conflict versus multi-conflict revision.
- Family C (longer inputs): single conflict; every input in TW, FW,
  and RW has length >= 8. Conflict byte and position are the
  adversary's choice, declared in CONFLICT.txt. Isolates whether
  revision cost stays bounded and accuracy holds as length grows.
- Family D (novel template shape): the intended revised structure
  S_w, declared in CONFLICT.txt, must differ structurally from
  S_frozen in at least one respect (branch position other than 0,
  branch count, then-branch program selection, or nesting
  arrangement) while remaining expressible by the frozen
  construction operators (IF byte-equality wrapping, alt selection
  among benum programs, v_old embedding). The red team certifies
  both the structural difference and the expressibility before the
  run. Isolates whether the conflict rule composes with template
  shapes beyond the authored frozen solution shape.

## World validity prechecks (void, never a verdict)

The executor runs these mechanically before any revision execution,
using only frozen baseline code; the red team independently
re-verifies them post-hoc from the committed world files. Any failure
voids that world and the whole step-7 run: no verdict is recorded,
and the remedy is a transparent amendment with a redesigned world,
re-frozen. A malformed world must never be laundered into a FAIL.

- V0 (base learnable): B1 (frozen dsearch over the 1055 benum
  programs) on TW alone achieves first_fit >= 0 with fails-on-TW=0.
  Record w_first_fit_tw.
- V1 (adversary disjointness): bytes(FW input) are disjoint from
  bytes(TW inputs); the declared conflict bytes are a subset of
  bytes(FW input); bytes(RW input) are disjoint from bytes(TW inputs)
  except for declared conflict bytes, and RW's input matches at
  least one declared conflict at its declared position. Family A
  additionally: all TW/FW/RW input bytes disjoint from A_frozen.
- V2 (problem real): v1w (the V0 first fit) mispredicts FW. A world
  with no genuine counterexample is malformed.
- V3 (impossibility recheck, the K-SB4c analogue): B1 over TW+FW
  evaluated against EW restricted to TW+FW enumerates all 1055 benum
  programs with first_fit=-1. A world solvable by plain re-search
  does not isolate revision.
- V4 (expectation consistency, red-team certified pre-run): EW
  equals R_w applied to the 5 check inputs; R_w is a strict
  parametric (families A, B, C) or structural (family D)
  generalization of the frozen conflict-rule form (match
  (pos,byte) maps to byte repeated to input length, else the base
  program). For family D the red team additionally certifies S_w
  differs structurally from S_frozen and is expressible by the
  frozen construction operators.

## Frozen kill bars (per world w in {A,B,C,D}; step-7 PASS requires all of them)

- K-OOD-W1 (correctness, accuracy floor 100 percent): the revised
  procedure achieves fails=0 on all 5 EW pairs. Kill: any
  misprediction (w_fails_total > 0).
- K-OOD-W2 (revision-eval ceiling): revision_evals <= 25, strict.
  Kill: revision_evals > 25. Rationale, frozen here: 5x headroom over
  the frozen 5 evals; S6C measured blind template-aware enumeration
  at 88,728 evals on the frozen set, so 25 stays orders of magnitude
  below any blind-enumeration regime while giving diagnosis room for
  longer inputs and multi-conflict.
- K-OOD-W3 (reuse, the K-SB3 analogue): RW is predicted correctly
  with zero new DIAGNOSIS, PRIMITIVE-CONSTRUCTED, or VERSION lines
  after the reuse check. Kill: any misprediction or any new
  revision marker.
- K-OOD-W4 (determinism): per world, 3/3 runs byte-identical
  (sha256 match), exit 0, zero stderr bytes. Run matrix: 12 runs
  (4 worlds x 3). Kill: any divergence, nonzero exit, or any stderr
  byte.
- K-OOD-W5 (purity and docs): pure Zag only at every stage; zero
  Python; zero em-dash and zero en-dash bytes in all lane files
  (byte-checked). Kill: any Python use or any forbidden byte.

Architecture bars (preserved):

- K-ARCH1 (zero cognition source delta): the frozen mechanism
  source (proc_revise2.zag at 847a8f10f) is byte-identical before
  and after; cognition source delta = 0 exactly. World files and
  test harness code are recorded separately. Kill: any nonzero
  cognition source delta.
- K-ARCH2 (no architecture growth): new_semantic_cases=0,
  new_modes=0, new_bridges=0, new_routers=0, new_handlers=0; no
  protected-core changes. Kill: any nonzero value.

## Bounding and kill semantics (what a FAIL means)

step-7 FAIL names every tripped bar and states the consequence per
this matrix. The step-5 PASS and step-6 PASS records are untouched by
any step-7 outcome.

- Only family B fails (any of W1/W2/W3): the bounded-L2 claim is
  BOUNDED to single-conflict revision. Surviving narrowed claim:
  revision generalizes across bytes, positions, lengths, and
  template shapes, but only for single conflicts.
- Only family C fails: BOUNDED to short-input revision (the frozen
  length regime, input length <= 4).
- Only family D fails: BOUNDED to the authored template-shape class
  (S_frozen); no composition generality beyond the frozen solution
  shape.
- Family A fails, alone or with others: the conflict rule does not
  generalize beyond the frozen alphabet and positions. The
  bounded-L2 claim is KILLED as stated; the honest narrowed residue
  (revision works only within the frozen byte/position regime) is
  not a generality claim and is recorded as such.
- Two or more families fail in any combination not covered above,
  or all four fail: KILLED. The revision mechanism does not
  generalize beyond the frozen fixtures.
- K-OOD-W4, K-OOD-W5, K-ARCH1, or K-ARCH2 trips: step-7 FAIL with
  cause named (determinism, purity, or architecture); no bounding
  claim follows because the failure is in the run's premises, not
  in the mechanism's generality. Recorded as information gained.
- Any validity precheck failure: VOID, never a verdict; transparent
  amendment with a redesigned world, re-frozen.

## Sealed evaluation design and adversary protocol

- The adversary is an independent agent: different from the step-7
  builder/executor and from the step-6 implementers. The adversary
  designs the four worlds post-freeze from this prereg's family
  requirements only.
- Before any execution, the adversary commits sha256 hashes of all
  20 world files to the lane (ADVERSARY_WORLD_HASHES.md). The
  executor verifies hashes at load time. The builder never sees
  world contents before or during the run.
- The independent red team (different agent from adversary and
  builder) certifies each world against V1-V4 and the family
  requirements; the certification report is committed pre-run.
- RW.txt is held from the revision machinery until after the
  revision completes; the phase presenting it must not run before
  the revision ACTIVE marker, mirroring the frozen F1r-reuse rule.
- Per world execution order: V0/V1/V2/V3 prechecks, train v1w,
  present FW, run the frozen revision (record revision_evals),
  score against EW (W1, W2), present RW (W3). Repeat 3x per world
  (W4). 12 runs total.
- Code-sharing disclosure is mandatory in the result doc: the
  executor uses only the frozen mechanism binary and frozen baseline
  code; no world-specific code may appear in the harness; the red
  team audits for leakage.

## Cost accounting (required in the result doc)

Machine-greppable fields, per world w in {A,B,C,D}:
w_first_fit_tw, w_b1w_enumerated, w_revision_evals, w_fails_total,
w_reuse_correct, w_reuse_new_revision_lines, w_wall_ms; plus
binary_bytes (each binary), source_delta_lines (test harness only),
cognition_source_delta (must be 0), new_semantic_cases, new_modes,
new_bridges, new_routers, new_handlers. Kill: any missing field; any
nonzero architecture-growth field; any nonzero
cognition_source_delta.

## Honest boundaries: bounded L2 ceiling, NOT L3

Step 7 does not test representational invention, template invention,
or any L3 criterion. A step-7 PASS means the bounded-L2 revision
mechanism generalizes within the four tested regimes; it is not
evidence toward L3 and must not be claimed as such. A step-7 FAIL
bounds or kills the bounded-L2 claim per the matrix above; it does
not retroactively alter the step-5 or step-6 PASS records. No outcome
here weakens, reinterprets, or re-scores any frozen bar from steps
5 or 6.

## Pipeline position statement

Steps 1-6 established: (1) committed preregistration across frozen
preregs; (2) implementation (F3a3 BUILD-PASS on corrected bars);
(3) sealed evaluation on frozen fixtures with the adversary byte;
(4) independent reproduction (byte-identical transcript match,
independent red-team re-runs); (5) simple-baseline comparison
(step-5 PASS, 8/8 amended bars, EVIDENCE HOLDS, original
BASELINE-FAIL unchanged); (6) alternative-explanation attack plus
ablation (step-6 PASS on re-execution under amendment K-AX2: A1 and
A2 killed, template confirmed load-bearing). Step 7 establishes (7)
the OOD test on fresh sealed adversary-designed worlds. Remaining
for SURVIVES: (9) transfer/reuse test beyond the single reuse probe,
(10) a second independent red team over the full chain, (11)
governance audit. A step-7 verdict is PASS or FAIL on the OOD bars;
it is never SURVIVES.

## Verdict semantics

step-7 PASS: all four worlds pass K-OOD-W1 through K-OOD-W5,
K-ARCH1 and K-ARCH2 hold, and cost accounting is complete. Any kill
bar tripped: step-7 FAIL naming the tripped bars and stating the
bounding or killing consequence per the matrix. Any validity
precheck failure: VOID, no verdict. This prereg governs only the
step-7 execution; no bar may be moved after results are seen.

## Skeptic self-attack (and answers)

Attack: the families are miscalibrated relative to the bounded-L2
claim in both directions at once, because the adversary designs them
with the frozen mechanism's known shape in view. Too easy: families
A and C replicate the frozen solution's structure with renamed bytes
and longer strings, and the mechanism's code is byte-parametric by
construction, so a PASS on A or C is near-tautological and
uninformative. Too hard: family D's "novel template shape" is
whatever the adversary imagines the frozen operators cannot express,
so a FAIL on D is a designed kill, not a measurement. Either way the
verdict measures the adversary's knowledge of the mechanism, not the
mechanism's generality.

Answer, in three parts. First, on too easy: the bounded-L2 claim is
itself a parametric claim (diagnosis finds (pos,byte), the template
instantiates at that (pos,byte), the conflict rule updates matching
records). Testing new parameters is the correct test of a parametric
claim, not a tautology, because the live alternative hypothesis is
constant-hardcoding: the authored template and the frozen fixtures
are consistent with a mechanism that only works at pos=0 with bytes
114 and 120. Family A exists to falsify exactly that hypothesis; a
PASS on A rules out the hardcoding alternative, which is genuine
information given that the template was researcher-authored. Second,
on too hard: family D cannot be a designed kill because V4 puts
expressibility certification in the red team's hands pre-run. A D
world whose intended structure the frozen construction operators
cannot express fails certification and never reaches the mechanism;
what reaches the mechanism is certified expressible but structurally
novel, which is precisely the composition-generality question. Third,
on residual miscalibration in either direction: the verdict
semantics convert it into information anyway. A too-easy PASS is
bounded by the family's stated regime (the PASS claims only the four
tested regimes, never broad generality, and never SURVIVES). A
too-hard FAIL lands in the bounding matrix, which narrows the claim
to the regimes that held. The never-SURVIVES rule and the untouched
step-5/6 records cap what any OOD outcome can inflate. Miscalibration
changes the width of the measured scope, not the honesty of the
measurement.

## Commit-order self-check (binding)

This prereg must be committed ALONE by the coordinator before any
step-7 world file, hash manifest, implementation file, transcript,
binary, or build log exists in the lane. Verification: `git log
--format=%H --
docs/lab/rsi/runs/wave-20261001-2021pdt/HPIREV2/PREREG_PI_REV2_STEP7.md`
must show exactly one commit, and that commit must strictly precede
the first commit adding any step-7 artifact. UNVERIFIABLE ORDERING
voids this prereg. No bar may be altered after results are seen; any
further change requires a new transparent amendment and re-freeze.
Builders report BUILD-PASS/BUILD-FAIL only.

No em-dashes in this documentation.
