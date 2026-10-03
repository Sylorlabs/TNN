# PREREG: H-CTXPAIR-1 — ctx-aware used-pair set for the SUF probe strategy

**Status: PREREG-FROZEN 2026-10-03.** Hypothesis only. No implementation
exists, none is authorized by this document, and none may be built under
this prereg without a separate parent-approved builder task. This document
is never edited after freezing; any change requires a new prereg
(H-CTXPAIR-2, ...). Commit-order self-check: the freeze commit contains
ONLY PREREG.md and NAMECHECK.md under l3_ctx_pair_hypothesis/.

**Worker:** L3-CTX-PAIR-HYPOTHESIS (subagent, depth 2/2, 2026-10-03).
**Task type:** non-ledger (claim minting paused). Hypothesis generation,
not implementation, not a benchmark.

**Governance position:** this prereg is INPUT to the parent's pending
decision on L3-SUF-2. It does not preempt that decision, does not weaken
any frozen bar, and does not authorize touching frozen L3-SUF-1 code
(frozen verdicts BUILD-PASS / REDTEAM-SURVIVES / scaling envelope stand
unmodified). It exists to keep a 20+ hypothesis frontier live.

## 0. Meta-preregistration: frozen criteria for a good hypothesis

Frozen BEFORE the hypothesis content in sections 1-8. The hypothesis is
held against these criteria in the self-check table at the end of this
section. That ordering is the "prereg before hypothesis" discipline for
a single-document task: the acceptance criteria exist first, the
hypothesis must satisfy them.

- **H-CRIT-1 Precision.** The hypothesis names the exact data-structure
  change, the exact probe-algorithm change, and the exact budget
  treatment. Check: a builder with no other context can implement the
  V1a/V1b/V2 learner variants from section 3 alone.
- **H-CRIT-2 Testability.** Every prediction names a world battery,
  seed discipline, learner variants, and numeric bars. Check: sections
  4 and 6 contain no untestable sentence of the form "should generally
  improve".
- **H-CRIT-3 Falsifiability.** Every falsifier names an observable
  outcome that kills the hypothesis or a clause of it, including the
  null (tiebreak-luck) and the cheaper competing explanations. Check:
  section 5 covers no-gain, safety-regression, volume-not-allocation,
  budget-starvation, luck, wrong-attribution, and marking-interaction.
- **H-CRIT-4 Implementability without privilege.** Testable without the
  sealed adversary KEY.md, without editing frozen L3-SUF-1 src/, and
  under the worker toolchain guard (pure Zag, safebin, pinned znc).
  Check: section 6 uses only the worker's own scaling worlds plus
  fresh-seed variants.
- **H-CRIT-5 Honest uncertainty.** Unknowns and competing explanations
  are stated before any result exists. Check: section 7 lists U1-U5,
  A1-A3, and a sketched competing hypothesis H-CTXPAIR-2.
- **H-CRIT-6 Governance-clean.** Does not preempt L3-SUF-2, does not
  move any frozen bar, does not authorize implementation. Check:
  Status header and T5.

Self-check verdict: H-CRIT-1 PASS (M1-M4, V1a/V1b/V2 specified);
H-CRIT-2 PASS (H-P1..H-P7, H-K1..H-K7); H-CRIT-3 PASS (H-F1..H-F7,
A1-A3); H-CRIT-4 PASS (T1-T6); H-CRIT-5 PASS (U1-U5, A1-A3,
H-CTXPAIR-2); H-CRIT-6 PASS (Status, T5, section 8).

## 1. Background: the defect being hypothesized about

Grounded in L3-SUF-1-SCALING REPORT.md (2026-10-03), finding (a):

- The frozen learner's probe phase (`l_probe_phase`,
  l3_suf_intermediate/src/learner2.zag) has two stages. (a) Slot-varying:
  for each training triple (s0,x,y), TEST the lifted form's prediction at
  every OTHER context; a knowledge-prediction (fb==0) REJECT triggers an
  immediate flipped-value follow-up (PVARY2) "so the repair build has
  positive evidence for this context"; a fabrication-prediction (fb!=0)
  REJECT gets NO follow-up. (b) Staged both-values: build a used-pair set
  from TRAINING triples only, indexed `usedp[p1*40+p2]` (pair only, no
  context); for each pair NOT in the set, TEST both values 0 and 1 at ALL
  contexts.
- A pairs (agreeing pairs, scale_world.zag line 187/268) are trained at
  ONE random context. The ctx-blind used-pair set marks an A pair "used"
  from its single training context, so stage (b) never staged-probes it
  at the other context; stage (a) only TESTs the form's (fabricated)
  prediction there with no flipped-value follow-up on REJECT.
- Consequence: off-context determined pairs carry NO positive evidence
  at the queried (s0,x,y). The sole-survivor rule then honestly ABSTAINs
  (Case B: obs=0, test_acc=0 at the queried element; verified by the
  post-prereg diagnostic). At S3 ABS this produced cdet=5/8 < 7/8 with
  0 wrong predictions: 3 abstains on off-ctx A pairs. The REPORT reads
  the S3 SC-K3 FAIL as tiebreak-luck on off-ctx queries under a
  ctx-blind probe strategy, not mechanism failure.
- Scale anchors: S3 = nent 30, |D| 40, |U| 12, |A| 24, ntrain 104;
  S4 = nent 40, |A| 32, ntrain 152 (slot-varying consumes the full 150
  setup budget; staged coverage comes only from escalation probe-more).
  Budgets frozen: 150 setup / 500 escalation probe-more / 2000 total.
  Contexts: 2 (ids 61/62 in the scaling worlds).

## 2. Hypothesis H-CTXPAIR-1 (statement)

A learner whose probe-phase bookkeeping tracks evidence coverage per
(PAIR, CONTEXT) tuple rather than per pair, and whose staged probing
covers the cross product of pairs x training-contexts (subject to the
frozen probe budgets), will eliminate the Case-B honest-abstention
shortfall on off-context determined pairs: on the frozen S3 ABS battery
it achieves cdet=8/8 where the ctx-blind learner got 5/8, with 0 wrong
predictions and 100% U-abstention preserved, and with no increase to the
frozen probe budgets. The predicted gain comes from evidence ALLOCATION
(ctx-aware coverage), not from probe volume.

## 3. Mechanism specification (implementable from this section alone)

New learner variants; the marking / sole-survivor rule is UNTOUCHED
(probe-side change only). V0 = frozen L3-SUF-1 learner, byte-identical
control (frozen src sha256-verified, linked read-only, as in
L3-SUF-1-SCALING).

- **M1. Ctx-aware coverage structure.** Replace `usedp[p1*40+p2]` with a
  structure keyed by (pair, context). Concretely: reuse the
  distinct-context list `ctxs` (already built in l_probe_phase);
  allocate `usedpc` of `ne*ne*nc` bytes (or equivalent (p1,p2,ci)
  records); mark tuple (p1,p2,ci) COVERED when any of these touches it:
  (i) a training triple at that context; (ii) any probe
  (PVARY/PVARY2/TEST) at that context. Canonical entity order and the
  p1<=p2 normalization are kept.
- **M2. Staged probing over tuples.** Stage (b) iterates over (pair, ci)
  tuples, not pairs: for each pair in canonical order and each context
  ci, if the tuple is uncovered and budget remains, TEST both values
  (0; then 1 iff 0 REJECTed) at that context. Pairs wholly unseen in
  training are probed at ALL contexts (as now); pairs seen at one
  context are staged-probed at the OTHER context(s) as well.
- **M3 (fallback variant only). Fabrication-REJECT follow-up.** In stage
  (a), on a slot-varying TEST where the form's prediction was a
  fabrication (fb!=0) and the TEST REJECTs, perform the same
  flipped-value follow-up now done only for knowledge REJECTs (PVARY2).
  M3 is NOT in the primary variant; it is preregistered as V1b for use
  only if V1a triggers H-F4 (budget starvation), since M3 banks the
  off-ctx evidence earlier (in stage a) at the cost of more stage-(a)
  probes.
- **M4. Budget discipline unchanged.** 150 setup / 500 escalation
  probe-more / 2000 total. Probe order: stage (a) slot-varying first
  (unchanged), then stage (b) over (pair,ci) tuples in canonical order.
  No budget increase: the hypothesis claims the gain is ALLOCATION, not
  volume. (This is what makes the H-K5 budget-control discriminating.)
- **Variants.** V1a = V0 + M1 + M2 (primary). V1b = V0 + M1 + M2 + M3
  (fallback, only if V1a hits H-F4). V2 = V0 + exactly K extra probes,
  where K = V1a's measured extra probe count at S3, allocated CTX-BLIND
  (builder preregisters the allocation rule before running V2, e.g.
  staged both-values on K/2 randomly chosen additional pairs, or
  repeated part-(b) probes at already-covered contexts; the rule must
  not use context information about which tuples are uncovered).

## 4. Testable predictions

- **H-P1 (primary, completeness).** V1a on the frozen S3 ABS battery
  (identical seeds to L3-SUF-1-SCALING): cdet=8/8 (vs 5/8 for V0),
  0 wrong predictions on heldout, 100% ABSTAIN on undetermined (U)
  heldout.
- **H-P2 (mechanism trace).** The Case-A/Case-B diagnostic (same
  diag_main.zag logic: per over-marked determined stakes query, report
  obs/test_acc at the queried (s0,x,y)) shows 0 Case-B off-ctx abstains
  on determined heldout at S3 under V1a; the 3 formerly abstained A
  pairs now carry positive TEST-ACCEPT evidence at the queried
  (s0,x,y).
- **H-P3 (no regression).** V1a replicates V0 on S1/S2/S4 ABS+INV under
  the frozen bars: S4 ABS cdet stays 8/8, 0 wrong everywhere, 100%
  U-abstain everywhere, SC-K4 budget bars hold.
- **H-P4 (bounded cost).** V1a's extra probe volume at scale S is at
  most 2x|A| (staged both-values on uncovered off-ctx A tuples; e.g.
  <=48 at S3 with |A|=24), and total TESTs stay <=2000 at every scale
  (SC-K4 preserved).
- **H-P5 (attribution).** V2 (ctx-blind + K matched extra probes) does
  NOT reach cdet=8/8 on S3 ABS: the gain is from ctx-aware ALLOCATION,
  not probe volume.
- **H-P6 (replication vs tiebreak-luck).** On >=3 fresh-seeded S3 ABS
  worlds (new seeds for A-pair context assignment and pair sampling),
  V1a reaches cdet=8/8 on >=2/3 AND beats V0 on the same seeds by
  >=2/8 on >=2/3.
- **H-P7 (diagnostic signature).** Across all scales, the fraction of
  determined-heldout queries that are Case-B (no positive evidence),
  off-ctx, and UNRESOLVED-marked goes to 0 under V1a. The fix removes
  exactly the Case-B off-ctx class, nothing else.

## 5. Falsifiers

- **H-F1 (no completeness gain).** V1a S3 ABS cdet <=5/8 on the frozen
  seeds (no better than V0) AND the diagnostic confirms the off-ctx
  (pair,ctx) tuples WERE staged-probed within budget. Then ctx-blindness
  was not the binding constraint; the causal claim is wrong. (If the
  tuples were NOT reached, that is H-F4, not H-F1.)
- **H-F2 (safety regression).** V1a yields >0 wrong predictions on any
  heldout query, or U-abstention <100%, at any scale. The "without
  weakening safety invariants" clause is falsified; the fix is rejected
  even if cdet improves.
- **H-F3 (volume, not allocation).** V2 ALSO reaches cdet=8/8 on S3.
  The gain was a probe-volume effect; the ctx-awareness mechanism claim
  is falsified (a weaker "more probes help" claim survives; redirect to
  budget research, not to M1/M2).
- **H-F4 (budget starvation).** V1a's stage (b) reaches <100% of the
  uncovered off-ctx A tuples at S3 within frozen budgets. The defect
  diagnosis is correct but infeasible under frozen budgets; the
  actionable conclusion becomes "ctx-aware coverage needs a
  prioritization policy or a budget change", and V1b (M3) may be tried
  once under this same prereg.
- **H-F5 (luck, not mechanism).** V1a hits 8/8 on frozen S3 seeds but
  fails H-P6 on fresh seeds (<=1/3 reach 8/8, or no systematic edge over
  V0). The frozen-seed result was tiebreak-luck redistribution; the
  hypothesis fails the replication bar.
- **H-F6 (wrong mechanism attribution).** V1a reaches 8/8 but the
  diagnostic shows the new correct predictions did NOT come from staged
  (pair,ctx) coverage (e.g. they came from fabrication-luck in stage
  (a), or from changed marking behavior). Outcome held, mechanism claim
  falsified; a new hypothesis is required.
- **H-F7 (marking interaction).** V1a increases Case-A over-marking
  (R-SUF-1 defect: TEST-ACCEPTs discarded after a fabrication REJECT)
  on determined heldout vs V0 by >2 queries at any scale. The added
  probes interact adversely with the sole-survivor marking rule; the
  "probe-side only" framing is insufficient.

## 6. Test protocol (for the future builder, parent-approved)

- **T1 Worlds.** The frozen scale_world.zag S1-S4 ABS+INV batteries at
  identical seeds (V0 replication); PLUS >=3 fresh-seeded S3 ABS worlds
  (vary the A-pair context-assignment seed and the pair-sampling seed;
  builder records all seeds in runs/).
- **T2 Variants.** V0 (frozen, read-only, sha256-verified), V1a
  (M1+M2), V1b (M1+M2+M3, only on H-F4), V2 (V0 + K matched extra
  probes, ctx-blind allocation preregistered before V2 runs).
- **T3 Bars.** H-K1: V1a S3 ABS cdet=8/8, 0 wrong, 100% U-abstain.
  H-K2: V1a matches V0 on S1/S2/S4 (SC-K1..SC-K4, SC-K6 as in the
  scaling prereg). H-K3: total TESTs <=2000 every run; extra probes
  <=2x|A| per scale (H-P4). H-K4: 0 Case-B off-ctx abstains on
  determined heldout (diagnostic). H-K5: V2 cdet <8/8 on S3.
  H-K6: fresh-seed replication per H-P6. H-K7: 3/3 byte-identical per
  run; sha256 digests recorded. ALSO score the completeness-adjusted
  bar for V0 and V1a (cdet over determined pairs the learner COULD have
  evidenced, i.e. on-ctx or staged-probed tuples): this discriminates
  alternative A2 (section 7).
- **T4 Diagnostics.** Reuse the Case-A/Case-B decomposition
  (diag_main.zag logic): for each over-marked determined stakes query,
  report obs and test_acc at the queried (s0,x,y); classify Case A
  (positive evidence discarded) vs Case B (no positive evidence).
- **T5 Governance.** V1a/V1b/V2 are NEW learner variants. Frozen
  L3-SUF-1 verdicts stand. This prereg does not authorize editing
  frozen code and does not decide L3-SUF-2.
- **T6 Toolchain.** Pure Zag, safebin, pinned znc; shell only for
  invoking znc, running binaries, git ops, file moves, sha256sum. Any
  forbidden-interpreter invocation is PROCESS-FAIL for that wave.

## 7. Uncertainties and alternative explanations (honest, pre-result)

- **U1 Budget fit at S4.** At S4 slot-varying consumes the full 150
  setup budget and |A|=32 (<=64 extra probes); whether escalation
  probe-more (500) has headroom is unknown. H-F4 is the honest failure
  mode. (S4 already passes 8/8 by luck; the S4 prediction is
  no-regression, not gain.)
- **U2 Marking-rule interaction.** More probes mean more REJECT events
  in the consequence log, which may shift UNRESOLVED marking (Case-A
  growth). The sole-survivor rule was tuned on the ctx-blind probe
  distribution. H-F7 guards this; magnitude and direction are genuinely
  uncertain.
- **U3 Granularity / generality.** (pair,ctx) brute-force coverage
  costs |pairs|x|C| probes; with many contexts it is infeasible. A
  deeper L3 learner might instead LEARN per-form context-(in)variance
  from stage-(a) slot-varying outcomes (e.g. "form F survived
  slot-varying on k/k probed pairs, treat F as context-invariant, reuse
  on-ctx evidence off-ctx"). That is a COMPETING hypothesis, sketched
  as H-CTXPAIR-2 below, not claimed here. H-CTXPAIR-1 is deliberately
  the minimal bookkeeping fix and does not by itself constitute
  representational invention.
- **U4 Sealed-world dependence.** The S3 5/8 finding is on the worker's
  own scaling worlds, not the adversary's sealed worlds (KEY.md not
  inspected, per VOID). If the sealed battery contains no off-ctx
  determined pairs, H-P1 has no sealed analogue; the fresh-seed worlds
  (T1) are the generality check available to the builder.
- **U5 Two contexts only.** All quantitative predictions assume |C|=2.
  M1/M2 generalize to nc contexts; the cost predictions do not. |C|>=3
  is future work.
- **A1 Tiebreak-luck null (the REPORT's own reading).** "The frozen
  T2(ii) bar (>=7/8) demands tiebreak-luck on such queries at scale."
  Under A1, V0 reruns on fresh seeds scatter around 5-6/8 and V1a does
  no better systematically. H-P6/H-F5 are designed to kill A1; if H-F5
  fires, A1 stands and the S3 FAIL stays a bar-calibration matter.
- **A2 Bar-calibration alternative (the REPORT's suggested follow-up).**
  Score T2(ii) only over pairs the learner could have evidenced
  (on-ctx or staged-probed). Under A2 the right fix is the BAR, not the
  learner: V0 would PASS the adjusted bar at S3 and H-CTXPAIR-1 would be
  unnecessary machinery. T3 requires scoring the adjusted bar for both
  V0 and V1a; if V0 passes it and V1a adds nothing beyond it, A2 is the
  preferred conclusion (architecture compression: do not add machinery
  the bar did not need).
- **A3 Fabrication-follow-up only.** Perhaps M3 alone (flipped-value
  follow-up on fabrication REJECTs, no ctx-aware set) suffices, since
  stage (a) already visits off-ctx tuples of trained pairs. The
  V1a-vs-V1b comparison discriminates: if V1b succeeds where V1a
  starves, A3's cheaper fix deserves its own prereg. Note M3 alone
  cannot help pairs where the form makes no prediction (v=-1) at the
  off context; the ctx-aware set is the general fix, A3 partial.

**H-CTXPAIR-2 (sketch, NOT preregistered here).** The learner learns a
per-form context-invariance predicate from stage-(a) outcomes and reuses
on-ctx evidence off-ctx for forms that survive slot-varying, instead of
probing every (pair,ctx) tuple. Testable (predicts sublinear probe cost
in |C| with cdet preserved), falsifiable (a context-gated form like
PARITY misclassified as invariant yields wrong predictions, H-F2
analogue), but a larger mechanism change; left for a future prereg.

## 8. VOID (terminal) and non-goals

- Any edit to frozen L3-SUF-1 src/ or the adversary's sealed
  worlds/KEY.md (this worker did not inspect them; the builder must
  not).
- Any change to the marking / sole-survivor rule inside V1 variants
  (probe-side only; H-F7 exists precisely to detect if that boundary
  fails).
- Any forbidden-interpreter invocation in the future build/test wave.
- Any 3/3 byte-identical divergence in T3 runs.
- Redefining H-K bars after seeing results; amending this prereg
  instead of writing H-CTXPAIR-2.
- Non-goals: fixing the nent=41 usedp buffer ceiling (separate scaling
  finding); the R-SUF-1 Case-A coarseness (with the red team for
  SUF-K10); transfer/reuse/revision/retirement; |C|>=3.

## Meta-criteria self-check (from section 0)

H-CRIT-1 PASS: M1-M4 name the data structure (usedpc over
ne*ne*nc, coverage-marking events), the algorithm (stage (b) over
(pair,ci) tuples in canonical order; M3 fallback), the budget treatment
(frozen 150/500/2000, stage (a) first), and all three variants
(V1a/V1b/V2 with V2's allocation rule preregistered by the builder).
H-CRIT-2 PASS: H-P1..H-P7 each name battery, seeds, variants, numbers;
H-K1..H-K7 are frozen bars. H-CRIT-3 PASS: H-F1..H-F7 plus A1-A3 cover
no-gain, safety-regression, volume-confound, starvation, luck,
misattribution, marking-interaction, and the cheaper alternatives.
H-CRIT-4 PASS: T1 uses only worker-owned worlds + fresh seeds; T5/T6
forbid sealed/frozen edits and non-Zag tooling. H-CRIT-5 PASS: U1-U5,
A1-A3, H-CTXPAIR-2 sketch. H-CRIT-6 PASS: Status header, T5, section 8;
no implementation authorized; L3-SUF-2 not preempted.
