# F-RECFOLD: Second Adversary Family for Q4 (H-NEW-2)

## 1. Purpose and status

This document designs the second independent adversary family for the Q4
explanatory-variable discovery line (H-NEW-2 from FRONTIER_W2.md, commit
1d72eac51).

First C0-C data point: F-PARCOND (conditional family). Adversary spec
b4e9b6a14, prereg ad4284269, implementation and result 5f56cc491
(BUILD-PASS), independent reproduction 121b6d5aa (prereg def897971),
baseline comparison 757442c40 (prereg 98ece92e4).

Criterion C0-C requires multiple unforeseen forms, with at least one
evaluation family designed by an independent adversary after the mechanism
freeze. F-PARCOND was the first such family. F-RECFOLD is designed here as
the second. This design does not by itself close C0-C; a third family
remains future work.

Status: DESIGN ONLY. Nothing is frozen in this document. Kill bars B1-B4
and falsifiers F-SEAL, F-MEM, F-NOREP, F-OVERBUDGET are PROPOSED here; the
future evaluation prereg (P) freezes them, possibly amended with
transparent justification. No implementation was performed. No empirical
claims are made.

## 2. Family specification: F-RECFOLD

### 2.1 Common ground

Six binary observables X1..X6. The target D is a Boolean function of all
six. The composition language is frozen exactly as in the Q4 design
(docs/lab/research-lead/overnight-20260928/q4_design/Q4_DESIGN.md):
terminals {X1, X2, X3, X4, X5, X6, 0, 1}, operators {AND, OR, NOT, XOR}
with standard Boolean semantics, evaluated by a generic interpreter.
The F4 treadmill guard applies: the alphabet is fixed before the sealed
draw and may not be extended to meet the family.

Every instance in this family has a canonical compact form of exactly 5
operators (section 2.4), inside the 7-operator KB2 bound.

### 2.2 Subfamily R1: flat k-fold repetition (REPEAT)

The adversary draws:
- a motif m from {AND, OR, XOR} (2-input operator),
- a top operator T from {AND3, OR3, XOR3} (3-input; e.g. AND3(u,v,w)
  = AND(AND(u,v),w), 2 operators),
- a pairing P: a partition of {1,2,3,4,5,6} into 3 unordered disjoint
  pairs (15 possibilities; enumeration in Appendix B).

Target: D = T( m(Xa,Xb), m(Xc,Xd), m(Xe,Xf) ) where (a,b), (c,d), (e,f)
are the drawn pairs.

Canonical compact form: 3 motif applications (1 operator each) plus the
3-input top (2 operators) = 5 operators.

Instance count: 3 motifs x 3 tops x 15 pairings = 135.

### 2.3 Subfamily R2: nested fold (RECURSE)

The adversary draws:
- a motif m from {AND, OR, XOR},
- a permutation pi of (1,2,3,4,5,6) (720 possibilities; lexicographic
  enumeration with index 0 = identity).

Target: D = m(m(m(m(m(X_pi1, X_pi2), X_pi3), X_pi4), X_pi5), X_pi6),
the left-nested iteration of the motif over the permuted variables.

Canonical compact form: 5 nested motif applications = 5 operators.

Instance count: 3 motifs x 720 permutations = 2160.

Total family size: 135 + 2160 = 2295 instances.

### 2.4 Fairness: every instance is solvable in principle

(a) Operator budget. R1: 3x1 + 2 = 5 operators. R2: 5x1 = 5 operators.
Both use only {AND, OR, XOR}; NOT is never required. 5 <= 7, the frozen
KB2 bound. The fairness gate (section 5.4) re-verifies this mechanically
per drawn instance; failure is impossible by construction, and any
failure halts the wave for investigation rather than triggering a silent
redraw.

(b) Statistical detectability. In R1 the motif input-output pattern
repeats on 3 disjoint variable pairs across the 64-row truth table; in
R2 it iterates 5 times along the permutation. The repetition is present
in any unbiased sample and in intervention responses. The structure is
not hidden by construction, only by the sealed pairing/permutation.

(c) KB1 admissibility. The Q4 design requires the best single observable
to predict D at no more than 0.80 over all 64 combinations. Verified for
every (motif, top) combination in Appendix A: the maximum is 0.78125
(OR motif, AND3 top); XOR-motif instances are exactly 0.5 (each variable
independent of D); R2 folds are at most 0.516. All satisfy the bound.

### 2.5 Difficulty tiers and the frozen battery structure

The battery is 3 instances with the following frozen structure. All
within-instance parameters are drawn sealed per section 5.5.

- Instance 1 (easy, calibration): R1, motif drawn from {AND, OR}, top
  drawn from {AND3, OR3, XOR3}, pairing sealed. Strong first-order
  signal. Purpose: verifies the protocol discriminates at all; a failure
  here indicates a broken harness, not a hard instance.
- Instance 2 (medium): R2, motif drawn from {AND, OR}, permutation
  sealed. Tests nested iteration of the induced unit with signal present.
- Instance 3 (hard): R1, motif = XOR (fixed), top = XOR3 (fixed),
  pairing sealed. This is 6-way parity over 3 sealed pairs. Every single
  variable is independent of D (zero marginal signal, Appendix A). The
  strongest discriminator in the family.

## 3. Material difference from F-PARCOND (K2)

F-PARCOND is D = IF X1 THEN (X2 XOR X3) ELSE (X2 AND X3): a gated
conditional where one variable selects between two different
computations. F-RECFOLD differs materially on five points:

1. No selector variable; symmetric variable roles. F-PARCOND assigns X1
   a gating role outside the branch computations. In F-RECFOLD every
   variable is a symmetric leaf; there is nothing to gate on. Structure
   must be discovered through pairing (R1) or ordering (R2), not gating.

2. Self-similar repetition instead of branching computation.
   F-PARCOND branches into two different operations (XOR vs AND).
   F-RECFOLD applies one motif repeatedly: 3 disjoint applications (R1)
   or 5 nested iterations (R2). The cognitive demand is inducing a
   reusable unit, not selecting a branch.

3. Zero-marginal-signal members. F-PARCOND's selector X1 carries strong
   first-order signal that guides discovery. Instance 3 (and the R2/XOR
   region generally) has exactly zero first-order signal: no single
   variable, and no myopic residual statistic, points at the structure.
   Discovery must operate at the pair level or higher. This directly
   attacks the greedy/myopic defect that falsified discovery hypotheses
   A (A-F1, result 21d838921) and C (C-F1, result aae06bac6).

4. Sealed partition/permutation induction. The pairing (15 possibilities)
   or permutation (720 possibilities) is drawn sealed after the learner
   freeze. No training family required discovering which variables group
   together: CONJ, XOR, THRESH, MUX, NEST (catalogued in the F-PARCOND
   adversary spec b4e9b6a14) all present their variable roles openly,
   and F-PARCOND's roles are fixed by its form.

5. Within-episode unit reuse. The motif must be induced once and applied
   thrice (R1) or iterated five times (R2). This is a miniature of the
   C0-D (cognitive reuse) direction inside a single discovery episode,
   whereas F-PARCOND tested reuse only across phases (D reused in
   D XOR X4).

## 4. Adversarial hardness (why this is a genuine test)

- The hard instance defeats myopic search by construction (zero marginal
  signal). Any beam that cannot cross a signal valley fails it; this is
  the same valley-crossing demand now carried by discovery hypotheses B,
  D, and the C2 repair design.
- The sealed pairing/permutation cannot be guessed a priori; the learner
  must induce it from evidence.
- The biased passive evidence (section 5.6) gives memorization controls
  the same misleading correlations that F-PARCOND's controls faced; the
  F-MEM falsifier voids instances that do not discriminate discovery
  from memorization.
- The post-reveal structural audit with F-NOREP (section 5.9) ensures the
  *form* was discovered, not merely the truth table: a 64/64
  memorization-shaped or branch-shaped solution fails the C0-C form claim
  even at perfect accuracy.

## 5. Sealed evaluation protocol S1 (K3)

### 5.1 Learner freeze (L)

The Q4 discovery mechanism (source, generic VM, discovery parameters,
growth-trace instrumentation) is committed at L. L must be an ancestor
of every commit below. No learner change is permitted after L; any
change restarts the protocol from this step.

### 5.2 Evaluation prereg (P)

An independent prereg commit P, strictly after L, freezes: the arms
(5.7), budgets (5.6), KB1-KB4 criterion values, the proposed bars B1-B4
(5.10, frozen here with any transparent amendment), the falsifiers
F-SEAL, F-MEM, F-NOREP, F-OVERBUDGET plus Q4 standard F1-F5, the baseline
suite, and SHA256(seed) for the sealed draw. The prereg's first commit
must strictly precede the draw and the implementation (prereg
commit-order self-check, per loop governance).

### 5.3 Adversary independence

The sealed draw is performed by an agent who did not build the Q4
learner, with no shared working state. The draw transcript (drawn
parameters, truth tables, LCG log) is committed by the adversary. The
parameter triple per instance (subfamily, motif/top, pairing/permutation,
decoy, Phase-2 Xj) is sealed: its SHA256 is published in the transcript
while the contents are revealed only after all scoring is complete.

### 5.4 Fairness gate

Per drawn instance, mechanically verify that the canonical compact form
uses at most 7 operators from {AND, OR, NOT, XOR}. True by construction
(5 operators, section 2.4); the gate runs and logs regardless. On
failure: halt the wave and investigate. Silent redraw is forbidden.

### 5.5 Deterministic draw procedure

All draws use one LCG stream: s_{n+1} = (1664525 * s_n + 1013904223)
mod 2^32, with s_0 = seed (nonzero u32; the adversary guarantees
nonzero). Each draw advances the state once and takes value mod m.
Rejection draws advance and retry, and every rejection is logged.

Draw order for the battery:

Instance 1 (easy, R1):
1. motif: v = s mod 3; accept 0 -> AND, 1 -> OR; reject 2 (retry).
2. top: s mod 3 -> {AND3, OR3, XOR3}.
3. pairing: s mod 15 (Appendix B enumeration).
4. decoy Xd: (s mod 6) + 1.
5. Phase-2 Xj: (s mod 6) + 1.

Instance 2 (medium, R2):
1. motif: v = s mod 3; accept 0 -> AND, 1 -> OR; reject 2 (retry).
2. permutation: s mod 720 (lexicographic, index 0 = identity).
3. decoy Xd: (s mod 6) + 1.
4. Phase-2 Xj: (s mod 6) + 1.

Instance 3 (hard, R1):
1. motif = XOR (fixed); top = XOR3 (fixed).
2. pairing: s mod 15.
3. decoy Xd: (s mod 6) + 1.
4. Phase-2 Xj: (s mod 6) + 1.

All draw tooling is shell and Zag only (sha256sum for commitments, a
small Zag or shell implementation of the LCG above). Zero Python at
every stage, including scratch and verification.

### 5.6 Evidence interface (adapts Q4 design section 4)

Per phase, the harness supplies 8 passive (x, y) samples with selection
bias: 6 of the 8 satisfy Xd = Y for the sealed decoy variable Xd, the
remaining 2 drawn uniformly. The learner may then perform up to 24
adaptive interventions (do-operator: SET any combination of Xi to 0/1,
then read Y), choosing each intervention from prior evidence.

Documented deviation from the Q4 standard: the standard confound is X6,
but X6 is causal in this family, so the confound role is played by the
sealed decoy Xd drawn uniformly from {X1..X6}. The function is
preserved: positing must be driven by interventional evidence, not by
passive correlation. Honest note: for XOR-motif instances the decoy is
at chance over all 64 combinations (a pure trap); for AND/OR-motif
instances it carries real but overstated correlation, and the 6/8 bias
still overstates it. In both cases interventions dissociate the decoy.

Information barrier: learner code sees only the passive samples and its
own intervention results. The 64-row truth table and all sealed
parameters are harness-side. Any leak of sealed parameters to the
learner before scoring fires F-SEAL and voids the wave.

### 5.7 Arms

- A-LEARN: Q4 discovery, Phase 1 (posit and keep D), then Phase 2 reuse
  with a fresh 8 passive samples and fresh 24-intervention budget;
  candidate growth may use the kept library. Phase-2 target:
  C' = D XOR Xj with the sealed Xj.
- A-SCRATCH: Phase-2 target C' from scratch (kept D unavailable), same
  budgets; 24 interventions recorded for any side failing to reach
  criterion (Q4 standard).
- A-BASE: memorization, 1-nearest-neighbor, linear, and random
  baselines on the same evidence (mirrors the F-PARCOND step-5
  comparison, result 757442c40).

### 5.8 Scoring (KB1-KB4, Q4 standard)

- KB1: true accuracy of kept D over all 64 combinations >= 0.95;
  admissibility requires best single observable <= 0.80 (verified
  family-wide in Appendix A).
- KB2: operator count of kept D <= 7; growth trace shows incremental
  construction (harness-independent check on committed artifacts).
- KB3: Phase-2 intervention counts; reuse_count <= 0.5 * scratch_count.
- KB4: 3/3 byte-identical stdout, pure Zag at every stage, zero Python
  invocations, zero em dash bytes.

### 5.9 Post-reveal structural audit (form check)

After all runs complete and sealed parameters are revealed, audit the
kept Phase-1 tree per instance:

- Define a motif instance semantically: a subtree with exactly 2
  distinct variable leaves whose evaluated truth table equals the drawn
  motif's truth table on that variable pair. Semantic (not syntactic),
  so associativity and commutativity variants are accepted.
- R1 instances: require at least 2 motif instances on disjoint variable
  pairs.
- R2 instances: require a nesting chain of depth at least 2 (a motif
  instance with a motif-instance child) using the drawn motif.
- Implementable as a Zag tree walk plus truth-table evaluation; this
  design specifies the check, the evaluation worker implements it.

### 5.10 Proposed bars (P freezes; proposed here)

- B1: true accuracy 64/64 on each of the 3 instances. Rationale: every
  instance is exactly representable in 5 operators; F-PARCOND reached
  64/64, so the bar is demonstrated-achievable, not aspirational.
- B2: kept D <= 7 operators with incremental growth trace (KB2).
- B3: margin over the best baseline >= 0.15 on the hard instance,
  >= 0.10 on easy/medium. Rationale: mirrors the Q4 KB1 margin clause
  (>= 0.15 over best observable) and F-PARCOND's observed 64 vs 40 gap.
- B4: structural audit (5.9) passes on all 3 instances.

### 5.11 Proposed falsifiers (P freezes; proposed here)

- F-SEAL: sealed parameters reach learner code or harness-visible state
  before scoring completes -> VOID the wave.
- F-MEM: the memorization baseline reaches 64/64 within budget on an
  instance -> that instance does not discriminate discovery from
  memorization -> VOID the instance; redraw with continued LCG state and
  log the void.
- F-NOREP: 64/64 accuracy achieved but the structural audit (5.9)
  fails -> the C0-C form claim FAILS for that instance. Accuracy is
  still reported; the form was not discovered.
- F-OVERBUDGET: kept D uses more than 7 operators -> FAIL (KB2).
- Q4 standard F1-F5 (per the F-PARCOND adversary spec b4e9b6a14) apply
  per phase unchanged.

### 5.12 Verdict

Against the frozen bars in P, per instance and for the battery. F-SEAL
voids the wave. F-MEM voids the affected instance. F-NOREP or
F-OVERBUDGET fail the C0-C form claim for the affected instance. A pass
on all 3 instances constitutes the second C0-C data point for the Q4
line; it does not close C0-C and starts no SURVIVES claim (promotion
steps 4-11 remain).

## 6. Independence and non-vacuity

- The adversary agent is independent of the Q4 learner builder; the draw
  transcript is the audit trail; no shared working state.
- The family is unforeseen by construction: 2295 instances, parameters
  sealed until scoring. None of the training families (CONJ, XOR,
  THRESH, MUX, NEST) nor F-PARCOND required pair-partition induction,
  permutation induction, repeated-unit induction, or nested iteration
  of an induced unit.

## 7. What this does not claim

- This is the second C0-C data point, not closure of C0-C. A third
  materially different family is still required.
- No SURVIVES claim is started; the 11-step promotion pipeline
  (reproduction, baselines, alternative-explanation attack, OOD,
  ablation, transfer/reuse, red team, governance audit) remains.
- The bars in 5.10 and falsifiers in 5.11 are proposals; P freezes them.

## 8. Honest risks and limitations

- Instance 1 is a calibration point, not a discriminator; a pass there
  carries little information beyond harness sanity.
- The R2 structural check is strict: flat equivalents (e.g. AND of six
  variables) exist within budget and would be 64/64-accurate but fail
  F-NOREP. This strictness is deliberate: it is the teeth of the form
  claim. A FAIL here is informative (accuracy OK, recursive form
  missed), not a harness bug.
- The decoy-variable adaptation (5.6) deviates from the Q4 X6-confound
  standard; the deviation and its rationale are documented above.
- Possible future cross-use of hard instances as discovery-battery tasks
  (valley-crossing tests for hypotheses B, D, C2) is flagged here and
  left out of scope: this design serves Q4 C0-C only.
- Governance: design only; zero Python used or specified at any stage;
  zero em dash bytes (byte-verified before commit); local commits only
  on tnn-native-lab; owned path with pathspec commits; nothing pushed.
  The F-PARCOND adversary spec carries a flagged Python-mirror process
  violation (see its Governance section); this design was produced
  without Python to avoid repeating that contamination.

## Appendix A: marginal-signal computations

Setup: 64 rows uniform over X1..X6. R1 target D = TOP(m12, m34, m56)
with disjoint pairs; by symmetry every variable has the same marginal
relationship to D. "Best single" = accuracy of the best single-variable
predictor D = Xi (or its negation) over all 64 rows. KB1 admissibility
needs best single <= 0.80.

Notation: q = P(motif = 1); q1 = P(motif = 1 | X1 = 1).

Motif AND: q = 1/4, q1 = 1/2 (given X1=1, m12=1 iff X2=1).
- TOP=AND3: P(D=1) = 1/64. "D=X1": P(D=1,X1=1) = q1*q*q = 1/32;
  P(D=0,X1=0) = 1/2 (D=1 requires X1=1). Accuracy = 1/32 + 1/2 = 17/32
  = 0.53125.
- TOP=OR3: P(D=1) = 1-(3/4)^3 = 37/64. "D=X1": P(D=0|X1=1) =
  (1/2)(3/4)(3/4) = 9/32, so P(D=1,X1=1) = 23/64. P(D=1|X1=0) =
  1-(1)(3/4)(3/4) = 7/16, so P(D=0,X1=0) = 1/2-7/32 = 9/32.
  Accuracy = 23/64 + 18/64 = 41/64 = 0.640625.
- TOP=XOR3: P(D=1) = 3q(1-q)^2 + q^3 = 27/64 + 1/64 = 28/64 = 7/16.
  Given X1=1, m12 ~ Bern(1/2): P(D=1|X1=1) = (1/2)(10/16) + (1/2)(6/16)
  = 1/2, so P(D=1,X1=1) = 1/4. Given X1=0, m12=0: D = m34 XOR m56,
  P = 2(1/4)(3/4) = 3/8, so P(D=1,X1=0) = 3/16. P(D=0,X1=0) = 5/16.
  Accuracy = 4/16 + 5/16 = 9/16 = 0.5625.

Motif OR: q = 3/4; given X1=1, q1 = 1; given X1=0, P(m12=1) = 1/2.
- TOP=AND3: P(D=1) = 27/64. "D=X1": P(D=1,X1=1) = (1/2)(3/4)(3/4) =
  9/32; P(D=1,X1=0) = 0; P(D=0,X1=0) = 1/2. Accuracy = 9/32 + 16/32 =
  25/32 = 0.78125. This is the family maximum, still <= 0.80.
- TOP=OR3: P(D=1) = 63/64. "D=X1": P(D=1,X1=1) = 1/2; P(D=1|X1=0) =
  1-(1/2)(1/4)(1/4) = 31/32, so P(D=1,X1=0) = 31/64; P(D=0,X1=0) =
  1/64. Accuracy = 32/64 + 1/64 = 33/64 = 0.515625.
- TOP=XOR3: P(D=1) = 3(3/4)(1/16) + 27/64 = 36/64 = 9/16. Given X1=1,
  m12=1: D = NOT(m34 XOR m56), P = (1/4)^2 + (3/4)^2 = 10/16, so
  P(D=1,X1=1) = 10/32 = 5/16. Given X1=0, m12 ~ Bern(1/2):
  P(D=1|X1=0) = 1/2, so P(D=1,X1=0) = 1/4; P(D=0,X1=0) = 1/4.
  Accuracy = 5/16 + 4/16 = 9/16 = 0.5625.

Motif XOR: q = 1/2 and each pair-motif is independent of each single
variable (given X1, X1 XOR X2 ~ Bern(1/2)). Hence D is independent of
every single Xi for every top: best single = 0.5 exactly. In
particular the hard instance (XOR, XOR3: 6-way parity) has zero marginal
signal.

R2 folds: AND-fold = AND of all six: "D=X1" gives P(D=1,X1=1) = 1/64,
P(D=0,X1=0) = 1/2, accuracy 33/64 = 0.515625. OR-fold symmetric:
33/64. XOR-fold = 6-way parity: 0.5.

Conclusion: best single observable is at most 0.78125 across the whole
family, satisfying KB1 admissibility (<= 0.80). The hard instance sits
at exactly 0.5.

## Appendix B: pairing enumeration (R1) and permutation convention (R2)

The 15 pair partitions of {1,2,3,4,5,6}, indexed 0..14. Pairs are
unordered; within the listing each partition is written with pairs
sorted and ordered by least element:

0:  (1,2)(3,4)(5,6)
1:  (1,2)(3,5)(4,6)
2:  (1,2)(3,6)(4,5)
3:  (1,3)(2,4)(5,6)
4:  (1,3)(2,5)(4,6)
5:  (1,3)(2,6)(4,5)
6:  (1,4)(2,3)(5,6)
7:  (1,4)(2,5)(3,6)
8:  (1,4)(2,6)(3,5)
9:  (1,5)(2,3)(4,6)
10: (1,5)(2,4)(3,6)
11: (1,5)(2,6)(3,4)
12: (1,6)(2,3)(4,5)
13: (1,6)(2,4)(3,5)
14: (1,6)(2,5)(3,4)

Check: 5 choices for 1's partner x 3 pairings of the remainder = 15.

R2 permutations: lexicographic enumeration of all 720 permutations of
(1,2,3,4,5,6); index 0 = (1,2,3,4,5,6). The draw takes s mod 720 as the
index. The evaluation worker implements the standard lexicographic
unranking (factorial number system) in Zag or shell.
