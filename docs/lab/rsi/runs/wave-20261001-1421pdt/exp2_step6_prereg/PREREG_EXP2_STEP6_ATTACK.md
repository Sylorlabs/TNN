# PREREG: H-EXP2 v2 step-6 attack (identifiability discrimination plus first-vs-argmax)

Wave: wave-20261001-1421pdt. Worker: EXP2 step-6 attack (prereg draft).
Date: 2026-10-01. Status: DRAFT. This prereg is NOT frozen until the
coordinator commits it (alone, before any implementation or evaluation
work). Nothing here is a verdict.

## Provenance

This is step 6 (alternative-explanation attack) of the 11-step frontier
promotion pipeline, applied to H-EXP2 v2 (BUILD-PASS, wave-20261001-0221pdt,
frozen prereg docs/lab/rsi/runs/wave-20260930-1121pdt/exp2/PREREG_H_EXP2_V2.md).
Prior: docs/lab/rsi/runs/wave-20261001-1121pdt/exp2/STEP6_STALL_DIAGNOSIS.md.
Its finding: the 08:21 sweep's systematic B=2 stall (4/4 runs stall at
round 6) is a law-family IDENTIFIABILITY property, not a baseline artifact,
proven by behavioral equivalence (under B=2, action 2 always sets p=1 and
no other action references A or B, so the four A hypotheses are
observationally identical under every probe of any length; verified
against both expworld.zag and altexp.zag). The frozen mechanism correctly
identified the identifiable part (B=2) and stalled honestly.
Interim alt-baseline evidence (08:21 wave, recorded, no verdict): "first"
(splitting probe, no argmax) IDENTIFIED both sealed worlds W-A/W-B (rounds
5/6); enum and fixed BUDGET-EXHAUSTED; rnd split. Reading: the
informativeness filter plus pruning does the work; argmax maximization is
not load-bearing on W-A/W-B.

This attack has two axes. Axis I (identifiability discrimination): sealed
worlds that discriminate "the mechanism correctly stalls on unidentifiable
structure" from "the mechanism fails to identify identifiable structure".
Axis II (simpler explanation): the first-vs-argmax comparison as the
central question, with the identifiability caveat above.

## 1. Frozen identifiability assumption

- ID-1: Under the fixed 6-action interface and the shared action dynamics,
  hypotheses (0,2), (1,2), (2,2), (3,2) are behaviorally identical under
  every action, hence under every probe of any length. Proof: the block
  condition for pressurize is (t==A or A==3) AND (l==B or B==3); under
  B=2, l is always 0 or 1 so l==B is never true and B==3 is false, hence
  the block condition is never true and action 2 always sets p:=1 for
  every B=2 hypothesis and for the true law; actions 0,1,3,4,5 never
  reference A or B in either implementation. Parameter A is unidentifiable
  when B=2. No mechanism, however guided, can distinguish the four through
  this interface; probe enumeration length caps are irrelevant.
- ID-2: Consequently, on any world with B=2, STALLED with exactly the
  4-member B=2 survivor set is the correct terminal behavior. Any
  IDENTIFIED emission on such a world is unjustified by evidence and
  scores as misidentification, even if the emitted pair happens to equal
  the sealed law. BUDGET-EXHAUSTED on such a world scores as failure to
  recognize unidentifiability.
- ID-3: The attack's identifiable worlds have B in {0,3}, outside the
  unidentifiable class, and each is the UNIQUE hypothesis with its block
  behavior, hence fully identifiable in principle. Proof for W-C (3,0):
  its block behavior is (l==0); any hypothesis (A,B) with A in {0,1,2}
  has block behavior (t==A) AND (l==B or B==3), which varies with t and
  cannot equal (l==0); with A==3 the behavior is (l==B or B==3), which
  equals (l==0) only for B=0. So (3,0) is unique. Proof for W-D (3,3):
  its block behavior is (always); any other pair has a behavior that
  varies with t or l (A in {0,1,2} gives a t-dependent term; A==3 with
  B in {0,1} gives an l-dependent term; B==2 gives never-blocked). So
  (3,3) is unique. A stall on W-C or W-D therefore cannot be excused as
  unidentifiability; it scores as mechanism weakness.

## 2. Attack design

### 2.1 Subjects (all binaries frozen before this prereg; no rebuild permitted)

- S-argmax: docs/lab/rsi/runs/wave-20261001-0221pdt/exp2/expseq_bin
  (H-EXP2 v2 BUILD-PASS learner). Interface: argv = history file, state
  file. Per round prints ROUND k, SURVIVORS s [pairs], then one of
  IDENTIFIED A B / PROBE n a0 ... plus SCORE sc / STALLED / INCONSISTENT.
  Selection: top probe by score DESC, length ASC, lexicographic ASC, where
  score = number of DISTINCT predicted outcome trajectories across the
  surviving hypotheses (score < 2 is never chosen; STALLED iff best
  score < 2 while more than one hypothesis survives).
- S-first: docs/lab/rsi/runs/wave-20261001-0821pdt/exp2/altexp_bin mode
  "first" seed 0 (08:21 alt baseline). Same interface, same pruning
  machinery, same scoring function, same length<=4 enumeration
  (1554 candidates), same score>=2 informativeness filter. The ONLY
  difference from S-argmax: probe selection is the first probe in
  enumeration order (length ASC 1..4, lexicographic ASC within length)
  scoring >= 2 (satisficing), with no argmax maximization; STALLED iff no
  probe scores >= 2. This isolates the maximization step as the single
  varying factor for Axis II.
- S-enum: same altexp_bin mode "enum" seed 0 (round-robin over the 1554
  probes, zero scoring). Negative control for world triviality.

The true world in every run is the frozen
docs/lab/rsi/runs/wave-20261001-0221pdt/exp2/expworld_bin (sole reader of
the sealed law file). Subjects never receive the law path. The subject
binaries were frozen before the sealed laws below are created, so no leak
path is constructible; the v2 K-X5 source audit stands.

### 2.2 Sealed worlds (committed with the frozen prereg; law contents frozen)

Law file format: `LAW <A> <B>` then `INIT <t> <p> <l>`. Files live under
prereg/ and are written by the coordinator at freeze time with exact
contents and recorded sha256:

- W-C (identifiable, structurally unlike W-A/W-B): LAW 3 0, INIT 0 0 0.
  Block iff l==0 (A vacuous, latch-gated). Neither W-A (2,3: t-only,
  B vacuous) nor W-B (2,1: t+l conjunction) has vacuous A; this is a new
  structure class for the mechanism.
- W-D (identifiable, structurally unlike W-A/W-B): LAW 3 3, INIT 0 0 0.
  Block always (A and B vacuous). A second new structure class.
- W-T (trap: stalling is the correct behavior): LAW 1 2, INIT 0 0 0.
  B=2, inside the provably unidentifiable class (ID-1). Correct behavior
  is the honest stall of ID-2. Trap for over-eager identification: any
  subject that "identifies" here is guessing, not inferring.

### 2.3 What each world discriminates

- W-C, W-D: "fails to identify identifiable structure" (Axis I, positive
  direction) and the argmax-vs-first comparison (Axis II). Both laws are
  provably uniquely identifiable (ID-3) and structurally unlike W-A/W-B,
  so success here is evidence the mechanism handles novel identifiable
  structure, not just the two sealed v2 worlds.
- W-T: "correctly stalls on unidentifiable structure" (Axis I, negative
  direction). The only correct terminal state is STALLED with exactly the
  four B=2 survivors. Any IDENTIFIED is misidentification by construction.

## 3. Frozen kill bars (ALL conjuncts must hold for PASS; bars never move)

Notation: p(S,W) = probes executed by subject S on world W = number of H
lines in history.txt at termination (deterministic per cell; 3/3 runs
byte-identical per section 4, so p is a single value).

- K-A1 (argmax identifies novel identifiable structure W-C): S-argmax on
  sealed W-C emits a line matching ^IDENTIFIED 3 0 with p <= 12; the
  emitted pair equals the sealed law file; the log contains zero
  BUDGET-EXHAUSTED, zero STALLED, zero INCONSISTENT lines; all 3 runs
  byte-identical.
- K-A2 (argmax identifies novel identifiable structure W-D): S-argmax on
  sealed W-D emits ^IDENTIFIED 3 3 with p <= 12; same exclusions and
  determinism as K-A1.
- K-A3 (argmax stalls honestly on the trap W-T): S-argmax on sealed W-T:
  the final terminal line matches ^STALLED; the final ROUND's SURVIVORS
  line is exactly `SURVIVORS 4 0,2 1,2 2,2 3,2`; the log contains zero
  lines matching ^IDENTIFIED (any IDENTIFIED line is automatic FAIL, even
  if the pair equals the sealed law, per ID-2); zero BUDGET-EXHAUSTED;
  zero INCONSISTENT; p <= 12; all 3 runs byte-identical.
- K-A4 (first identifies W-C): S-first on sealed W-C emits ^IDENTIFIED
  3 0 with p <= 12; same exclusions and determinism as K-A1. (Baseline
  bar; feeds the Axis II decision rule.)
- K-A5 (first identifies W-D): S-first on sealed W-D emits ^IDENTIFIED
  3 3 with p <= 12; same exclusions and determinism.
- K-A6 (first stalls honestly on the trap W-T): S-first on sealed W-T
  meets every conjunct of K-A3.
- K-A7 (worlds are non-trivial: unguided probing does not solve them):
  S-enum on W-C emits no ^IDENTIFIED line with the correct sealed pair
  within p <= 12, AND S-enum on W-D emits no ^IDENTIFIED line with the
  correct sealed pair within p <= 12. (Expected outcome:
  BUDGET-EXHAUSTED on both. A wrong-pair IDENTIFIED also satisfies this
  bar's letter and is recorded as misidentification.) Decision rule: if
  K-A7 fails on a world, that world is declared non-discriminating, is
  excluded from the Axis II verdict, and the exclusion is recorded; the
  remaining world's comparisons still stand.
- K-A8 (integrity and determinism): for every (subject, world) cell the
  3 rounds.log files are byte-identical (cmp); every run's stderr is
  empty; sha256 of all 24 rounds.log files is recorded; the three sealed
  law files' sha256 after the last run equal their freeze-time values.

## 4. Frozen evaluation protocol

- Terminal state definitions (frozen): IDENTIFIED A B = a line matching
  ^IDENTIFIED A B, emitted iff exactly one hypothesis survives pruning.
  STALLED = a line matching ^STALLED, emitted iff no probe scores >= 2
  while more than one hypothesis survives. BUDGET-EXHAUSTED = the shell
  loop appends BUDGET-EXHAUSTED when 12 probes have been executed without
  IDENTIFIED. INCONSISTENT = a line matching ^INCONSISTENT, emitted iff
  history refutes all 16 hypotheses.
- Run matrix (frozen): (S-argmax, W-C), (S-argmax, W-D), (S-argmax, W-T),
  (S-first, W-C), (S-first, W-D), (S-first, W-T), (S-enum, W-C),
  (S-enum, W-D). Three runs per cell. Total 24 sealed runs. maxprobes=12
  in every cell (each probe at most 4 actions).
- Orchestration: the v2 shell loops (run_exp2.sh for S-argmax,
  run_alt.sh for S-first/S-enum) unchanged except maxprobes=12 and the
  new law files. Shell does orchestration only (invoke binaries, pipe
  files); zero decision logic in shell.
- Determinism requirement: 3/3 byte-identical rounds.log per cell (K-A8).
  Any nondeterminism voids the affected cell (single re-run permitted;
  persistent nondeterminism blocks the attack with a tooling verdict, not
  a mechanism verdict).
- Commit order (frozen): the coordinator commits this prereg plus the
  three sealed law files (exact contents in 2.2, hashes recorded) ALONE,
  before any implementation or evaluation commit. Prereg-first-commit
  strictly precedes all evaluation commits (self-check at evaluation
  time). Any evaluation work before the freeze commit voids the run.
- Subject freeze: S-argmax, S-first, S-enum binaries are used as frozen;
  no source edits, no rebuilds. Any rebuild voids the attack.

## 5. Frozen verdict logic

Evaluate K-A1..K-A8, then:

- D1 (identifiability competence): if K-A1, K-A2, and K-A3 all PASS, the
  mechanism discriminates identifiable from unidentifiable structure on
  novel structure classes (it identifies what is identifiable and stalls
  honestly where stalling is correct). If any of K-A1..K-A3 FAILS, the
  verdict is ATTACK-SUCCEEDS-MECHANISM-WEAKNESS, naming the failed bar
  and axis: K-A1 or K-A2 failure = "fails to identify identifiable
  structure"; K-A3 failure = "fails to stall honestly on unidentifiable
  structure" (subdivided in the report as misidentification if any
  IDENTIFIED line appears, premature stall if the survivor set is not
  exactly the B=2 quadruple, or budget exhaustion).
- D2 (simpler explanation; evaluated only if D1 passes): let W' =
  {W-C, W-D} minus any world failing K-A7. If W' is empty, D2 is
  UNDECIDED (worlds too easy; recorded; the D1 verdict stands alone). If
  K-A4 and K-A5 PASS on every world in W', K-A6 PASSES, and for every
  world W in W' the inequality p_first(W) - p_argmax(W) <= 2 holds, the
  verdict is ATTACK-SUCCEEDS-SIMPLER-EXPLANATION: the informativeness
  filter (score >= 2) plus the shared pruning machinery accounts for the
  identification performance, and argmax maximization is not load-bearing.
  Otherwise the verdict is ATTACK-FAILS-MECHANISM-SURVIVES: argmax
  maximization is load-bearing beyond filter plus pruning (in particular
  if first fails to identify any world where argmax identifies, or first
  needs more than 2 extra probes on any world in W').
- Precedence: a K-A8 integrity failure voids the affected cells (single
  re-run; persistent failure = BLOCKED on tooling, no mechanism verdict).
  D1 is evaluated before D2; a D1 failure short-circuits to
  ATTACK-SUCCEEDS-MECHANISM-WEAKNESS regardless of D2 (with a note if the
  simpler baseline succeeded where the mechanism failed).
- Reported verdict format: "D1: <outcome>; D2: <outcome>", with the exact
  frozen bar (K-A1..K-A8) named for every claim.

## 6. Toolchain (pure Zag; Python voids on sight)

Every program written or run under this prereg is Zag compiled with the
pinned znc. Zero Python anywhere: no glue, no analysis scripts, no
scorers, no verifiers, no harnesses. Shell is used only to invoke znc,
run binaries, and move or copy files. The worker toolchain guard applies
(safebin activation recorded in NAMECHECK.md Step 0; `which python3`
prints nothing). Any Python invocation by the implementation or
evaluation worker voids that wave's work on sight (PROCESS-FAIL per
governance) and the affected runs are discarded, never repaired in place.

## 7. Honest boundaries (declared before implementation)

Authored: the 16-hypothesis family, the shared action dynamics, the
length<=4 probe bound, the distinct-trajectory scoring rule, the
tie-break orders, the probe budgets, the three sealed laws, the subject
set. NOT authored: the per-round probe choices (functions of pruned
hypotheses and evolved state), the number of rounds, the terminal
outcomes.

What a pass would establish:

- (D1 pass) The frozen mechanism's B=2 stall is identifiability-honest:
  on sealed structure classes it has never seen, it identifies the
  provably identifiable laws (W-C, W-D) within budget and stalls exactly
  on the provably unidentifiable class (W-T), never misidentifying.
- (D2 attack-succeeds) The argmax maximization step is not the active
  ingredient: filter plus pruning suffices, and the v2 novelty claim is
  reframed accordingly (BUILD-PASS stands; credit moves to the filter and
  pruning machinery).
- (D2 attack-fails) The argmax maximization is load-bearing: it buys
  identifications (or materially fewer probes) that satisficing
  first-probe selection cannot match, with the maximization step isolated
  as the single varying factor.

What a pass would NOT establish:

- L3 or representational invention: the hypothesis family is
  researcher-enumerated (fails C0-B open form); no new representation is
  created and semantics are not learner-defined (C0-A not met).
- Generality beyond the (A,B) law family, other action interfaces, or
  larger hypothesis spaces. W-C and W-D are two structure classes, not a
  generality proof.
- That the mechanism would identify every identifiable law in the family
  (only W-C and W-D are tested here; the 08:21 sweep covered 12/16).
- Transfer, OOD robustness, ablation beyond the first-vs-argmax
  isolation, or integration into a continuing learner (later pipeline
  steps).

Consequence note: ATTACK-SUCCEEDS-SIMPLER-EXPLANATION does not overturn
the H-EXP2 v2 BUILD-PASS (K-X1..K-X6 were met under their frozen prereg);
it reframes which component deserves credit. ATTACK-SUCCEEDS-
MECHANISM-WEAKNESS triggers the no-patch-treadmill rule: failures are
clustered by shared architectural cause before TNN-3; benchmark-specific
handlers and per-world opcodes are rejected.
