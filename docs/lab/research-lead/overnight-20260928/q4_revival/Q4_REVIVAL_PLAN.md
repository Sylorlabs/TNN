# Q4 Revival Plan: R1-R4 Experiments

Status: PLAN ONLY. No implementation, no new measurements. This document
designs the four revival experiments defined in Q4_CLAIM_REVISION.md
(commit a0cb66e15) and specifies their prereg requirements, seed hygiene,
and sequencing. Kill bars for this plan: K1 (R1-R4 designed), K2 (prereg
requirements specified), K3 (sequence defined).

## 0. What revival means, and what it does not

The revision's honest Q4 claim: "bounded L2 structural learning with a
real adversary-family solve and a real reuse measurement, where the
discovery component is underdetermined-evidence plus researcher-authored
simplicity bias plus single-seed luck, and the active-intervention
component is decorative at the tested budget."

R1-R4, if ALL met, revive the Q4 DISCOVERY claim: the learner robustly
discovers explanatory structure (multi-seed, on a genuinely complex
target, with a genuinely active intervention policy and thick reuse).

Revival is CONJUNCTIVE: R1 AND R2 AND R3 AND R4 must all PASS. Any
single FAIL means revival fails; the honest bounded-L2 claim stands;
the failed R localizes the weakness and becomes the defined next
target. There is no partial revival and no weakening of bars.

SCOPE LIMIT. R1-R4 revive discovery robustness WITHIN Q4. They do NOT
revive L3 or Criterion 0. Even a full revival leaves C0-A blocked (the
beam, the 200/opc tax, and the IV policies are researcher-authored) and
C0-B blocked (the vocabulary {AND, OR, NOT, XOR} is closed and frozen).
A successful revival upgrades Q4 from "bounded L2 with luck" to
"bounded L2 with robust discovery." The C0 blockers remain separate
work (OP-RECRUIT v2, the L3 bridge, C0INTEG).

## 1. R1: Multi-seed robustness

### 1.1 Question
Does the beam reach true 64/64 on fresh seeds when the evidence covers
all 8 combos, defeating the underdetermination reading?

### 1.2 Design
- Target: F-PARCOND (the family the discovery claim is about).
- Mechanism: the frozen Q4 discovery mechanism (same freeze L as the
  F-RECFOLD evaluation; no mechanism change permitted).
- IV policy: the R4-winning policy (see section 6 for sequencing). The
  R1 prereg names the policy explicitly once R4 lands.
- Seeds: 5 fresh seeds S1..S5, fixed in the prereg or SHA256-committed
  before any run. Disjoint from R4's seeds and from the tainted
  exploratory seeds {11, 22, 33, 44, 55}.
- Per seed: 8 passive samples (original bias protocol) + up to 24 IVs
  chosen by the named policy + the frozen beam search.
- Determinism: 3/3 byte-identical runs per seed (loop standard).

### 1.3 Bar
R1-PASS: on at least 4 of the 5 seeds, BOTH (a) the IV policy achieves
8/8 combo coverage AND (b) the beam's kept expression reaches true
64/64.

Rationale: with 8/8 coverage the ENUM result gives TIES=1,
TRUEUNIQUE=1 (attack result 73d9637a2). The evidence then uniquely
determines D and the 200/opc tax has no tie to break, so a 64/64 is
attributable to evidence plus search rather than to luck.

### 1.4 Falsifiers and diagnostics
- F-R1: fewer than 4 seeds satisfy (a) and (b) jointly. R1 FAILS.
- Required diagnostic per seed (non-governing but mandatory to
  report): tax-off ranking. Rank the beam's finalists by accuracy
  alone, ignoring the 200/opc tax, and report whether the top is
  unique. Under 8/8 coverage this must be unique; a tie indicates a
  harness or beam defect and invalidates the seed.
- Failure localization (reported per seed: coverage, evidence fit,
  true accuracy, tax-off uniqueness): a coverage shortfall implicates
  the policy; an evidence-fit shortfall implicates the beam (the
  SEED=55 mode: 23/32 fit at 8/8 coverage); an accuracy shortfall at
  full coverage implicates generalization.

### 1.5 Prereg requirements (R1-P)
The R1 prereg must freeze: the 5 seeds (or their SHA256 commitment);
the named IV policy with its frozen spec; the passive-sample protocol;
the 24-round budget; the beam configuration (width, tax, keep bars);
the bar (section 1.3); the falsifier F-R1; the mandatory diagnostics;
the determinism standard; and the purity clause (pure Zag, zero
Python). Its first commit strictly precedes any R1 run.

## 2. R2: No compact analytic alternative

### 2.1 Question
Is the discovered target genuinely complex, defeating the
vocabulary-coverage reading ("the frozen vocabulary covered it")?

### 2.2 Why R2 cannot run on F-PARCOND
F-PARCOND admits a 4-op analytic form, D = (x1 ^ (x2 & x3)) & (x2 | x3).
The target is simple, so the vocabulary-coverage reading survives any
R2 run on F-PARCOND regardless of the discovered form's op count. R2
therefore targets the F-RECFOLD hard instance (R1 subfamily, XOR motif,
XOR3 top, sealed pairing): 6-way parity over 3 sealed pairs, with zero
marginal signal (design 808ed196d, Appendix A).

### 2.3 R2-proof (preregister now): analytic lower bound
- Claim: any TREE expression over {AND, OR, NOT, XOR} computing 6-way
  parity uses at least 5 binary operators.
- Proof: NOT is unary and never combines distinct variables'
  influence. Contract all NOT nodes; the contracted tree has g binary
  nodes and L leaves with L = g + 1 (standard: nodes - 1 = edges =
  2g + u where u is the unary count, so L = g + 1 regardless of u).
  Each leaf is a literal. Parity depends on all 6 variables, so all 6
  must appear as leaves; hence g + 1 >= 6 and g >= 5.
- Corollary: for any discovered tree with total op count n <= 9,
  floor(n/2) <= 4 < 5, so NO expression at or below half its operator
  count computes the target. The R2 criterion is satisfied
  analytically for every reasonably compact discovery.
- Mechanical check (preregistered, trivial): a Zag program that takes
  the discovered n and asserts floor(n/2) < 5 given the proven bound.
  (Brute-force enumeration of alternative trees was considered and
  rejected: trees with up to 4 binary ops over 6 variables number in
  the hundreds of millions before semantic dedup. The analytic proof
  is primary and airtight for trees.)
- Caveat (preregistered): the bound is for trees. The Q4 beam produces
  trees. If a future mechanism emits DAGs with shared subexpressions,
  the bound must be revisited before R2 can be claimed.

### 2.4 R2-form (after the F-RECFOLD evaluation lands)
- Input: the F-RECFOLD hard-instance kept D (artifact of the H-NEW-2
  line), its F-NOREP structural-audit outcome, and its total op count
  n.
- Checks: (i) true accuracy 64/64; (ii) F-NOREP passes (the kept form
  is a parity chain, not a memorization-shaped or branch-shaped
  accident); (iii) n <= 9, so the R2-proof corollary applies.
- R2-PASS: R2-proof verified AND checks (i)-(iii) hold.
- R2-FAIL: any check fails. Two informative modes: if the hard
  instance run never reaches 64/64, R2-form cannot be evaluated and
  R2 FAILS (the mechanism cannot discover genuinely complex forms);
  if n >= 10, R2 FAILS (the known 5-op canonical parity chain is a
  compact analytic alternative at or below half the discovered count,
  so the discovery was bloated).

### 2.5 Prereg requirements
- R2-proof prereg: the claim, the proof text, the mechanical-check
  procedure, the pass criterion, the DAG caveat. Seed-independent;
  no runs needed beyond the check program.
- R2-form prereg: written after the F-RECFOLD result lands; names the
  kept-D artifact, its n, and checks (i)-(iii). (May live as a section
  of the F-RECFOLD post-evaluation analysis prereg; this is a
  coordination point with the H-NEW-2 line, not a duplication of it.)

## 3. R3: Reuse beyond the installed perfect terminal

### 3.1 Question
Does the kept structure improve later cognition when it is NOT an
installed perfect terminal?

### 3.2 Fixed kept component
The committed 7-op D from 5f56cc491 (as corrected by cffc56e5b).
Correct (64/64 true) and non-minimal (a 5-op solution and a 4-op
analytic form exist). R3 reuses this artifact; no Phase-1 re-run is
needed, so R3 is independent of R1/R4 seeds.

### 3.3 Arms (one prereg, three Phase-2 arms)
- Arm 1 (R3a, non-minimal robustness): component D_10, the 7-op D
  padded to 10 ops with identity wrappers (x AND 1), (x XOR 0),
  still exactly 64/64. Target C' = D_10 XOR X4 (same shape as the
  original Phase 2). Contrast A-REUSE (D_10 installed as terminal)
  vs A-SCRATCH. Bar: 64/64 and reuse_ivs <= 0.5 * scratch_ivs.
  Rationale: tests that the reuse advantage does not depend on the
  component being the learner's own sleek discovery. This arm is a
  robustness control; it is expected to pass if Phase 2 is sound.
- Arm 2 (R3-embed, non-trivial composition): component the 7-op D as
  terminal. Target E = (D AND Y1) OR ((NOT D) AND Y2) over fresh
  observables Y1..Y6 with a fresh decoy/confound arrangement. D is
  EMBEDDED as a subexpression, not top-level. Contrast A-REUSE vs
  A-SCRATCH. Bar: 64/64, reuse_ivs <= 0.5 * scratch_ivs, AND a
  structural check that the solution tree contains D as a
  subexpression. Rationale: reuse must cover discovering the
  embedding, a genuinely compositional task beyond one-step XOR.
- Arm 3 (R3b, changed surface; EXTENSION-GATED): component the 7-op D
  exposed as STRUCTURE (its tree, not an opaque terminal). Target
  D' = IF Y5 THEN (Y2 XOR Y4) ELSE (Y2 AND Y4) over new Y1..Y6: the
  same conditional-computation SHAPE as D with permuted variable
  roles and fresh distractors. The X-variable terminal cannot be
  pasted (it computes the wrong function on Y). The learner must
  re-derive D' guided by D's structure (variable remapping).
  Bar: 64/64, reuse_ivs <= 0.5 * scratch_ivs, AND an isomorphism
  check: the solution tree is isomorphic to D's shape under variable
  renaming. This arm REQUIRES a preregistered "structured library"
  mechanism extension (subtree grafting and remapping). If the
  extension is not built, Arm 3 is marked DEFERRED, not failed.

### 3.4 Verdict and falsifiers
- R3-PASS: Arms 1 and 2 meet their bars; Arm 3 passed or deferred.
- R3-FAIL: Arm 1 or Arm 2 fails its bar.
- F-R3-THIN: Arm 2's solution lacks D as a subexpression. The run is
  reported as re-derivation, not reuse; the arm fails the reuse bar.
- F-R3-SEAL: Phase-2 hidden parameters leak to the learner before
  scoring (same standard as the F-RECFOLD F-SEAL). Voids the arm.

### 3.5 Prereg requirements (R3-P)
The R3 prereg must freeze: the kept-D artifact (commit hash); the
D_10 construction procedure; the Arm 2 and Arm 3 hidden causes
(including the Y-variable layouts, decoys, and confounds, committed
but sealed from the learner); the isomorphism-check definition for
Arm 3; the arms, budgets (8 passive + 24 IVs per arm, same as Q4
Phase 2), and bars of section 3.4; the falsifiers; the determinism
standard; the purity clause. For Arm 3, the structured-library
extension spec must be preregistered first (separate prereg, strictly
earlier); without it Arm 3 stays deferred.

## 4. R4: Active-policy advantage

### 4.1 Question
Does the disagreement-IV policy beat random interventions, reviving
the "active" component or retiring it honestly?

### 4.2 Design
- Target: F-PARCOND (the family where the "decorative" finding was
  made; R4 directly adjudicates it).
- Policies, both frozen in the prereg: P-DIS, the original
  disagreement-IV policy; P-RAND, deterministic random
  unused-input selection (the attack's RANDIV spec, result
  73d9637a2).
- Seeds: 12 fresh seeds T1..T12, disjoint from R1's seeds and from
  the tainted exploratory seeds. Paired design: both policies run on
  each seed with the same 8 passive samples and the same 24-round
  budget.
- Primary metric: combo coverage (of the 8 X1-X3 combos) after 24
  rounds. Coverage is a pure policy output; it isolates the policy
  from beam fit-failure modes (the SEED=55 mode: 23/32 fit at 8/8
  coverage).
- Secondary metrics (reported, non-governing): best evidence fit
  (/32), kept-expression true accuracy, op count.

### 4.3 Bar (dual)
R4-PASS requires BOTH:
(a) mean coverage(P-DIS) - mean coverage(P-RAND) >= 0.75 combos;
(b) P-DIS wins the paired per-seed coverage comparison on at least
8 of the 12 seeds.

Rationale: 0.75 combos is about 9 percent of the 8-combo space, and
one full combo is the difference between determined (8/8) and
underdetermined (7/8) evidence. A smaller margin does not buy
determinacy, so it does not revive the "active" claim. (Note: the
win-rate bar alone has about a 19 percent null rate at n=12; the
dual bar is the operative gate.)

### 4.4 Falsifiers and special cases
- F-R4: mean coverage(P-RAND) >= mean coverage(P-DIS). R4 FAILS and
  the disagreement policy is HONESTLY RETIRED: the mechanism becomes
  passive plus random-IV discovery and the claim is updated
  accordingly. (R1 then runs with P-RAND; see section 6.)
- INCONCLUSIVE, not a pass: both policies reach 8/8 on at least 10
  of 12 seeds. The 24-round budget is too generous to discriminate;
  the preregistered follow-up re-runs with a 12-round budget.
- Accuracy-without-coverage: if the policies tie on coverage but
  differ on kept-expression accuracy, that is a beam effect, not a
  policy effect. Reported, non-governing.

### 4.5 Prereg requirements (R4-P)
The R4 prereg must freeze: the 12 seeds (or their SHA256 commitment);
the frozen specs of P-DIS and P-RAND; the passive-sample protocol;
the 24-round budget; the primary and secondary metrics; the dual bar
(section 4.3); F-R4 and the inconclusive rule; the determinism
standard; the purity clause. Its first commit strictly precedes any
R4 run.

## 5. Seed hygiene and cross-experiment independence

- Tainted seeds {11, 22, 33, 44, 55} (exploratory robust probe,
  73d9637a2) are never reused in any revival experiment.
- R1 seeds {S1..S5} and R4 seeds {T1..T12} are pairwise disjoint,
  fixed in their preregs or SHA256-committed before runs.
- R3 uses the fixed committed D artifact; its Phase-1 needs no
  seeds. Arm 2/3 Y-variable draws use fresh hash-committed draws,
  disjoint from all other seeds.
- R2-proof is seed-independent. R2-form uses the F-RECFOLD sealed
  draw; no new seeds.
- Rationale: R1 and R4 both probe F-PARCOND discovery; shared seeds
  would let policy tuning on R4 leak into R1's "fresh seed" claim.

## 6. Sequencing

- Phase A (parallel, now): R4 prereg + run; R3 prereg + Arms 1-2 run
  (Arm 3 deferred pending the structured-library extension);
  R2-proof prereg + mechanical check.
- Phase B (after R4 lands): R1 prereg + run, with the IV policy named
  as the R4 winner: P-DIS if R4 passes, P-RAND if R4 fails and the
  disagreement policy is retired.
- Phase C (after the F-RECFOLD evaluation result lands): R2-form
  prereg + check against the hard-instance kept D.
- Phase D: revival verdict (section 7).

Rationale for R4-before-R1: R1 tests the mechanism-plus-policy
jointly. Running R1 first with P-DIS and then having R4 retire P-DIS
would waste the R1 run. (The parallel alternative was considered and
rejected on those grounds.)

## 7. Revival verdict

After Phase C, evaluate the conjunction R1 AND R2 AND R3 AND R4.

- ALL PASS: the Q4 discovery claim is REVIVED, stated as: "bounded
  L2 structural learning with robust discovery: multi-seed 64/64
  under full combo coverage on F-PARCOND; discovery of a genuinely
  complex (parity, analytically incompressible) form on the
  F-RECFOLD hard instance; an intervention policy with preregistered
  advantage over random; and reuse of kept structure beyond an
  installed perfect terminal." Still bounded L2. NOT L3, NOT C0
  (section 0).
- ANY FAIL: revival fails. The honest bounded-L2 claim from the
  revision stands unchanged. The failed R is the localized weakness
  and the defined next target. No partial revival, no bar
  weakening, no retroactive reinterpretation.

## 8. Governance

- Every R has its own prereg; every prereg's first commit strictly
  precedes its implementation (commit-order self-check, loop
  governance).
- Pure Zag at every stage: build, run, verification, analysis. Zero
  Python anywhere, including scratch and byte checks. Zero em/en
  dash bytes (byte-verified before commit).
- Determinism: 3/3 byte-identical runs per experiment (loop
  standard).
- Owned paths only, pathspec commits, local commits only, nothing
  pushed.
- This plan alters no committed result and weakens no frozen bar.

Verdict: PLANNED
