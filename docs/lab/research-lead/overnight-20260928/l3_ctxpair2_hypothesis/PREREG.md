# PREREG: H-CTXPAIR-2 — learned per-form context-invariance for the SUF probe strategy

**Status: PREREG-FROZEN 2026-10-03.** Hypothesis only. No implementation
exists, none is authorized by this document, and none may be built under
this prereg without a separate parent-approved builder task. This document
is never edited after freezing; any change requires a new prereg
(H-CTXPAIR-3, ...). Commit-order self-check: the freeze commit contains
ONLY PREREG.md and NAMECHECK.md under l3_ctxpair2_hypothesis/.

**Worker:** L3-CTXPAIR-2-HYPOTHESIS (subagent, depth 2/2, 2026-10-03).
**Task type:** non-ledger (claim minting paused). Hypothesis generation,
not implementation, not a benchmark.

**Governance position:** this prereg is INPUT to the parent's pending
decision on L3-SUF-2, alongside H-CTXPAIR-1
(l3_ctx_pair_hypothesis/PREREG.md). It does not preempt that decision,
does not weaken any frozen bar, and does not authorize touching frozen
L3-SUF-1 code (frozen verdicts BUILD-PASS / REDTEAM-SURVIVES / scaling
envelope stand unmodified). It exists to keep a 20+ hypothesis frontier
live, and to give the parent two genuinely competing hypotheses rather
than one bookkeeping fix.

## 0. Meta-preregistration: frozen criteria for a good hypothesis

Frozen BEFORE the hypothesis content in sections 1-8. The hypothesis is
held against these criteria in the self-check table at the end of this
section. That ordering is the "prereg before hypothesis" discipline for
a single-document task: the acceptance criteria exist first, the
hypothesis must satisfy them.

- **H2-CRIT-1 Precision.** The hypothesis names the exact new learner
  state (invariance ledger: fields, update events, reset rule), the
  exact stage-(a) probe substitution (trigger condition, tested value,
  tags, follow-up), the exact invariance decision rule (formula,
  frozen threshold), the exact stage-(b) policy change, the exact
  repair-build change, and all four learner variants. Check: a builder
  with no other context can implement V0/V1/V2a/V2b from section 3
  alone.
- **H2-CRIT-2 Testability.** Every prediction names a world battery,
  seed discipline, learner variants, and numeric bars. Check: sections
  4 and 6 contain no untestable sentence of the form "should generally
  improve"; probe-count predictions are relational where the baseline
  is measured (H2-P4) and absolute where it is constructed (H2-P6).
- **H2-CRIT-3 Falsifiability.** Every falsifier names an observable
  outcome that kills the hypothesis or a clause of it, including the
  null (tiebreak-luck), the substrate hypothesis winning outright, and
  the predicted misclassification boundary. Check: section 5 covers
  no-gain, safety-regression, no-efficiency-gain, ledger-misfire,
  completeness-loss, misclassification, luck, and wrong-attribution.
- **H2-CRIT-4 Implementability without privilege.** Testable without the
  sealed adversary KEY.md, without editing frozen L3-SUF-1 src/, and
  under the worker toolchain guard (pure Zag, safebin, pinned znc).
  Check: section 6 uses only the worker's own scaling worlds, fresh-seed
  variants, and builder-constructed |C|=4 worlds (spec in T1; no sealed
  material).
- **H2-CRIT-5 Honest uncertainty.** Unknowns, competing explanations,
  the L3-boundary assessment, and the predicted failure mode are stated
  before any result exists. Check: section 7 lists U1-U6, A1-A4, the
  L3 note, and the domain-blindness test.
- **H2-CRIT-6 Governance-clean.** Does not preempt L3-SUF-2, does not
  move any frozen bar, does not authorize implementation. Check:
  Status header and T5.

Self-check verdict: H2-CRIT-1 PASS (S0, M1-M4, V0/V1/V2a/V2b specified);
H2-CRIT-2 PASS (H2-P1..H2-P8, H2-K1..H2-K8); H2-CRIT-3 PASS (H2-F1..H2-F8,
A1-A4); H2-CRIT-4 PASS (T1 uses worker-owned + builder-built worlds only;
T5/T6 forbid sealed/frozen edits and non-Zag tooling); H2-CRIT-5 PASS
(U1-U6, A1-A4, L3 note, D4); H2-CRIT-6 PASS (Status, T5, section 8).

## 1. Background: the defect, and why brute force is not the end

Grounded in L3-SUF-1-SCALING REPORT.md (2026-10-03), finding (a), and in
H-CTXPAIR-1 PREREG.md (2026-10-03):

- The frozen probe phase (`l_probe_phase`, learner2.zag) runs stage (a)
  slot-varying (TEST each training triple's form prediction at every
  other context; knowledge-REJECT triggers a flipped-value PVARY2
  follow-up; fabrication-REJECT gets no follow-up) and stage (b) staged
  both-values over a ctx-blind used-pair set (`usedp[p1*40+p2]`).
- A pairs (agreeing across contexts, scale_world.zag) are trained at ONE
  random context. D pairs (disagreeing) are trained at BOTH contexts, so
  training contains contradictions and `l_build_direct` builds a kind1
  (per-s0 guarded) form. For an A pair trained at s0, the form has an
  entry guarded by s0 only; at the other context `l_predict2` finds no
  entry and falls back to the tiebreak fabrication (fb==1). When that
  fabrication REJECTs, no follow-up banks positive evidence at the off
  context: the sole-survivor rule then honestly ABSTAINs (Case B: obs=0,
  test_acc=0 at the queried (s0,x,y)). At S3 ABS this gave cdet=5/8
  with 0 wrong: 3 abstains on off-ctx A pairs.
- H-CTXPAIR-1 answers with brute force: a ctx-aware (pair,ctx) coverage
  ledger and staged probing over (pair,ctx) tuples at ALL contexts.
  Cost scales as |pairs| x |C|. It is deliberately the minimal
  bookkeeping fix and, by its own U3, "does not by itself constitute
  representational invention."

H-CTXPAIR-2 starts from a different observation: the learner already
performs the experiment that decides context-invariance, in stage (a),
for free. When the form's on-context knowledge value v0 is TESTed at an
off context and ACCEPTs, the learner has observed that this form's claim
transfers across contexts. When the form's own entries for one pair
disagree across s0 guards, the learner has observed that it does not.
A learner that LEDGERS these observations into a persistent,
defeasible per-form invariance belief can (a) project knowledge across
contexts instead of testing tiebreak fabrications (fixing Case B inside
stage (a), with no extra probes), and (b) once invariance is established,
probe each pair ONCE and propagate the evidence, instead of brute-forcing
(pair,ctx) tuples. The belief is learner-created state: it is formed
after experience, stored in learner state, governs future probing,
revises on counterevidence, and is described only in learned properties
(prediction agreement, probe outcomes), never in human domain labels.

## 2. Hypothesis H-CTXPAIR-2 (statement)

A learner that (M1) in stage (a) projects a form's on-context knowledge
value to contexts where the form has no entry, testing the projected
value instead of the tiebreak fabrication; (M2) maintains a persistent
per-form context-invariance ledger fed by structural entry disagreement
and by knowledge-probe outcomes at off contexts, with a frozen
one-way decision rule; (M3) under INVARIANT status staged-probes each
pair at a single context; and (M4) under INVARIANT status propagates
probe TEST-ACCEPTs across contexts in the repair build, will:

(i) on the frozen S3 ABS battery reach cdet=8/8 with 0 wrong and 100%
U-abstention, using strictly fewer total probes than H-CTXPAIR-1's
brute-force variant (the Case-B evidence is banked in stage (a), not
stage (b));

(ii) on builder-constructed uniformly context-invariant |C|=4 worlds,
match H-CTXPAIR-1's cdet exactly while using at most 40% of its staged
probes (sublinear probe cost in |C|);

(iii) on mixed (invariant + context-gated) worlds, read VARIANT and
behave identically to H-CTXPAIR-1 (safety parity; the brute-force
substrate is the fallback, not the casualty).

The predicted gain over H-CTXPAIR-1 is probe EFFICIENCY via a learned
belief, not completeness: where H-CTXPAIR-1 buys coverage with probes,
H-CTXPAIR-2 earns it with evidence.

## 3. Mechanism specification (implementable from this section alone)

New learner variants; the marking / sole-survivor rule is UNTOUCHED.
V0 = frozen L3-SUF-1 learner, byte-identical control (frozen src
sha256-verified, linked read-only, as in L3-SUF-1-SCALING).
V1 = V0 + H-CTXPAIR-1 (its PREREG M1+M2), the brute-force competitor.

- **S0. Substrate (shared with H-CTXPAIR-1).** H-CTXPAIR-2 assumes the
  ctx-aware coverage ledger of H-CTXPAIR-1 M1, with one disambiguation
  (see cross-prereg note below): tuple (pair,ci) is COVERED iff (a) a
  training triple exists for the pair at ci, OR (b) a TEST-ACCEPT
  (kd==1, oc==1) is logged for the pair at ci. REJECTed probes do NOT
  cover. Canonical entity order and p1<=p2 normalization are kept. All
  probe tags in this prereg (PINV/PINV2/TEST/PVARY) mark coverage on
  ACCEPT under this rule. The hypotheses compete on PROBE POLICY and
  the invariance belief, not on bookkeeping.
- **M1. Invariance projection in stage (a).** In the slot-varying loop,
  for each training triple (s0,x,y) and each other context c: compute
  the form prediction at c, (v,fb), AND the form prediction at the
  training context s0, (v0,fb0). If fb==1 (fabrication at c: the form
  has no entry guarded by c for this pair) and fb0==0 (knowledge at
  s0; holds for training triples of a training-consistent form):
  TEST (c,x,y,v0) with fab=0 and tag "PINV" INSTEAD of
  TEST (c,x,y,v) with fab=1/"PVARY". (The tested value is the form's
  knowledge, not the tiebreak guess; when v0==v the probe is identical
  to frozen except for tag/ledger.) If the PINV TEST REJECTs (rr==0)
  and budget remains: follow up with TEST (c,x,y,1-v0), fab=0, tag
  "PINV2" (mirrors the frozen PVARY2 gating). Ledger (M2) updates on
  every performed PINV/PINV2 probe. M1 is inert for kind0 forms (fb is
  never 1 for covered pairs: `l_form_find` ignores s0) and for kind2
  forms (fb is always 0); it fires exactly for single-guard pairs of
  kind1 forms, i.e. the Case-B shape. Probe-budget treatment: M1 uses
  the same stage-(a) probe slots as frozen (one TEST per
  (triple, other-ctx) with a prediction); PINV2 follow-ups are charged
  exactly like PVARY2.
- **M2. Per-form invariance ledger.** New persistent learner state per
  form generation: (inv_ok:i32, inv_bad:i32, gen:i32). Update events:
  (i) STRUCTURAL SEEDING at form build/rebuild: for each canonical
  pair with entries at >=2 distinct s0 guards holding different d,
  inv_bad += 1 (the form observably encodes context-dependence; free,
  no probes). (ii) BEHAVIORAL: any off-ctx TEST of a form KNOWLEDGE
  prediction (fb==0; tags PVARY or PINV; staged TEST both-values probes
  are excluded since they test no form prediction): ACCEPT -> inv_ok
  += 1; REJECT -> inv_bad += 1. Fabrication outcomes never touch the
  ledger. Frozen decision rule, evaluated when stage (b) begins and
  when the repair build runs: INVARIANT iff inv_bad==0 AND
  inv_ok>=KINV with KINV=3 frozen; VARIANT iff inv_bad>=1; else
  UNKNOWN. Revision is ONE-WAY within a generation (INVARIANT->VARIANT
  on the first inv_bad; never back). The ledger RESETS (0,0,new gen)
  whenever the form object is rebuilt (`l_form_new(f,..)` or
  copy-into-f from a rebuilt sc, including escalation re-expansions).
  The ledger persists across `l_probe_phase` invocations within a run
  otherwise.
- **M3. Stage-(b) policy under the belief.** Status read at stage-(b)
  entry. If INVARIANT: iterate pairs in canonical order; for each pair
  with any uncovered tuple, staged-probe at the LOWEST-INDEXED
  uncovered context ci only (both-values: TEST 0; TEST 1 iff 0
  REJECTed, budget permitting); skip all other contexts for that pair.
  If VARIANT or UNKNOWN: H-CTXPAIR-1 behavior (staged both-values at
  every context with an uncovered tuple). M3 never probes U
  (unprobeable) pairs differently than frozen: their probes cannot
  ACCEPT, so coverage and abstention are unchanged.
- **M4. Repair-build evidence propagation.** While the CURRENT form
  generation's status is INVARIANT, `l_guard_reexpand` and
  `l_union_reexpand` enter each probe TEST-ACCEPT (kd==1, oc==1 log
  entry) at ALL contexts in `ctxs`, not just its own s0 (duplicate
  (s0,a,b) entries still suppressed by the existing found-check).
  Training triples are NEVER propagated. M4 is what makes "one probe
  suffices" true for cdet: the (s0,x,y)-indexed predictor sees positive
  evidence at the queried context. M4 applies in both re-expand paths;
  the builder verifies the kind0->kind1 expansion branch too (U3).
- **Variants.** V2a = V0 + S0 + M1 (projection only; stage (b) is V1's
  all-context staged tuples; no ledger, no M3, no M4). V2b = V2a + M2
  + M3 + M4 (full H-CTXPAIR-2). V1 = V0 + H-CTXPAIR-1 M1+M2 (with the
  S0 disambiguation).
- **Budgets.** Frozen 150 setup / 500 escalation probe-more / 2000
  total on S1-S4. For builder-built |C|=4 worlds: B(|C|) = frozen x
  |C|/2, i.e. 300 / 1000 / 4000, preregistered by the builder before
  running (T1).

Cross-prereg note (flagged, not decided here): H-CTXPAIR-1 M1(ii) as
written ("any probe marks covered") would mark the 3 Case-B off-ctx
tuples covered via their stage-(a) fabrication-REJECT probes, in which
case its own H-P2 (positive TEST-ACCEPT evidence at the queried
(s0,x,y)) cannot hold. The S0 disambiguation (REJECTs do not cover) is
the coherent reading required by H-CTXPAIR-1's H-P2/H-P4. If the
H-CTXPAIR-1 builder implements literal "any probe covers", V1 cannot
reach 8/8 and the comparison in section 6 must be re-baselined; the
L3-SUF-2 decision should require the disambiguated semantics.

## 4. Testable predictions

- **H2-P1 (primary, completeness).** V2a on the frozen S3 ABS battery
  (identical seeds to L3-SUF-1-SCALING): cdet=8/8 (vs 5/8 for V0),
  0 wrong predictions on heldout, 100% ABSTAIN on U heldout.
- **H2-P2 (mechanism trace).** The Case-A/Case-B diagnostic shows 0
  Case-B off-ctx abstains on determined heldout at S3 under V2a; the 3
  formerly abstained A pairs carry PINV-ACCEPT evidence (tag "PINV",
  stage (a)) at the queried (s0,x,y), and their tuples are marked
  covered BEFORE stage (b) begins. V1's fix, by contrast, carries
  "TEST"-tagged stage-(b) evidence: the evidence SOURCE attributes the
  fix to the competing mechanism.
- **H2-P3 (no regression).** V2a and V2b replicate V0 on S1/S2/S4
  ABS+INV under the frozen bars: S4 ABS cdet 8/8, 0 wrong everywhere,
  100% U-abstention everywhere, SC-K4 budget bars hold.
- **H2-P4 (efficiency at |C|=2).** On S3: V2a total TESTs <= V1 total
  TESTs - 2R, where R (>=3, read off V1's trace) is the number of
  off-ctx A tuples with fabrication-REJECT under V1 (each such tuple
  costs V1 up to 2 staged TESTs and costs V2a 0, its PINV-ACCEPT having
  covered it). V2a stage-(a) TEST count == V1 stage-(a) TEST count
  (same slots); PINV2 follow-ups <= 4 at S3.
- **H2-P5 (ledger discipline on mixed worlds).** On the frozen S3
  battery V2b is EXACTLY V2a in cdet, total probes, and per-tuple
  coverage: the ledger must read VARIANT (structural seeding gives
  inv_bad >= |D| = 40 > 0), so M3/M4 are inert. Any divergence is a
  ledger misfire (H2-F4).
- **H2-P6 (sublinear cost, pure-invariant |C|=4).** On >=3
  builder-built uniformly context-invariant |C|=4 worlds (T1): V1
  cdet >= 7/8 and V2b cdet == V1 cdet exactly with 0 wrong for both;
  V2b staged TESTs <= 0.4 x V1 staged TESTs. (At |C|=4 the brute-force
  staged cost is ~4x per pair; one-context probing plus M4 propagation
  is ~1x.)
- **H2-P7 (safety parity, mixed |C|=4).** On >=3 builder-built mixed
  |C|=4 worlds: V2b cdet == V1 cdet exactly, 0 wrong for both; the
  ledger trace shows VARIANT on every run (H2-F7 if not).
- **H2-P8 (domain-blindness).** On fresh-seed S3 worlds with context
  ids permuted (61<->62) and on |C|=4 worlds with rotated ctx ids,
  V2b's (cdet, total probes, ledger status) are identical to the
  unpermuted runs: the mechanism branches only on guard agreement and
  probe outcomes, never on ctx identity.

## 5. Falsifiers

- **H2-F1 (projection does not fix Case B).** V2a S3 ABS cdet <= 5/8 on
  frozen seeds AND the diagnostic confirms PINV-ACCEPTs were logged at
  the 3 queried (s0,x,y). Then banked PINV evidence does not survive
  the marking/repair path; the Case-B diagnosis or the probe-side
  framing is wrong.
- **H2-F2 (safety regression).** Any variant yields >0 wrong
  predictions or U-abstention <100% at any scale/world. In particular:
  V2b wrong predictions on any mixed world falsify the "without
  weakening safety invariants" clause outright (M4 mispropagation is
  the suspected cause; the fix is rejected even if probe counts win).
- **H2-F3 (no efficiency gain).** V2a total TESTs >= V1 total TESTs on
  S3. The "one probe suffices / evidence earned in stage (a)" claim
  fails at |C|=2; only the completeness claim (shared with V1) would
  survive.
- **H2-F4 (ledger misfire).** V2b diverges from V2a on S3 in cdet,
  total probes, or coverage (i.e. the ledger did NOT read VARIANT, or
  M3/M4 fired anyway). The decision rule or the structural seeding is
  falsified.
- **H2-F5 (propagation loses completeness).** Pure-invariant |C|=4:
  V2b cdet < V1 cdet. M4 propagation is not a faithful substitute for
  per-context probing.
- **H2-F6 (sublinear claim fails).** Pure-invariant |C|=4: V2b staged
  TESTs > 0.4 x V1 staged TESTs. The probe-cost scaling claim is
  falsified (possible cause: UNKNOWN status from KINV too high, U2).
- **H2-F7 (misclassification).** The ledger reads INVARIANT on any
  mixed world (fresh-seed S3 or mixed |C|=4). Per-form granularity is
  too coarse; the research redirects to per-entry-group granularity
  (H-CTXPAIR-3 sketch, section 7), and H-CTXPAIR-1 is favored for
  L3-SUF-2 on robustness grounds.
- **H2-F8 (luck, not mechanism).** V2a reaches 8/8 on <=1/3 fresh-seed
  S3 worlds, or shows no systematic total-probe edge over V1 across
  them. The frozen-seed result was tiebreak-luck redistribution.

## 6. Test protocol (for the future builder, parent-approved)

- **T1 Worlds.** (a) Frozen scale_world.zag S1-S4 ABS+INV at identical
  seeds (V0 replication) PLUS >=3 fresh-seed S3 ABS worlds (vary A-pair
  context-assignment and pair-sampling seeds; record all seeds).
  (b) Builder-built |C|=4 worlds, pure Zag, mirroring scale_world.zag:
  nent=30, |D|=40, |U|=12, |A|=24. Truth: pure-invariant family uses a
  context-independent truth (all contexts ORD(perm)); mixed family uses
  contexts {0,1}=ORD(perm), {2,3}=PARITY (pairs agreeing within groups
  form A; disagreeing across form D). Training: D pairs at ALL
  contexts, A pairs at one random context, U unprobeable/undetermined
  exactly as in scale_world.zag. Stakes: 8 determined queries (mix of
  on-ctx/off-ctx A and D pairs) + 4 U abstain queries, mirroring S3.
  >=3 fresh seeds per family. Budgets 300/1000/4000 (section 3).
  Builder commits the world builder BEFORE running any variant on it.
- **T2 Variants.** V0 (frozen, read-only, sha256-verified), V1
  (H-CTXPAIR-1 M1+M2 with the S0 disambiguation; the builder records
  which reading was implemented), V2a (S0+M1), V2b (S0+M1+M2+M3+M4).
- **T3 Bars.** H2-K1: V2a S3 cdet=8/8, 0 wrong, 100% U-abstain.
  H2-K2: V2a/V2b match V0 on S1/S2/S4 (SC-K1..K4, K6). H2-K3: frozen
  budgets hold every run; PINV2 <= 4 at S3. H2-K4: 0 Case-B off-ctx
  abstains under V2a; evidence tags PINV (V2a) vs TEST (V1) as in
  H2-P2. H2-K5: V2b == V2a exactly on S3 (cdet, probes, coverage).
  H2-K6: |C|=4 pure-invariant: V2b cdet == V1 cdet (>=7/8), 0 wrong,
  staged TESTs <= 0.4x. H2-K7: |C|=4 mixed: cdet parity, 0 wrong,
  ledger VARIANT every run. H2-K8: 3/3 byte-identical per run; sha256
  digests recorded. Robustness (not a bar): re-run the |C|=4
  pure-invariant family at KINV in {2,5}; report cdet and probe counts.
- **T4 Diagnostics.** (i) Case-A/Case-B decomposition (diag_main.zag
  logic) per over-marked determined stakes query. (ii) Evidence-tag
  attribution: for each determined heldout query predicted correctly,
  the tag of the earliest ACCEPT that the repair build consumed
  (PINV/PINV2/PVARY/TEST/training). (iii) Ledger trace: per form
  generation, (inv_ok, inv_bad, status) at stage-(b) entry and at each
  repair build, plus the structural-seeding count. (iv) Probe
  accounting: stage-(a) vs stage-(b) TEST counts per variant.
- **T5 Governance.** V1/V2a/V2b are NEW learner variants. Frozen
  L3-SUF-1 verdicts stand. This prereg does not authorize editing
  frozen code and does not decide L3-SUF-2. The parent's decision rule
  (input, not verdict): build V2b iff H2-K1, H2-K4, H2-K5, H2-K6,
  H2-K7 all hold (H-CTXPAIR-2 subsumes the brute force); build V1 iff
  H2-F4, H2-F6, or H2-F7 fires (robustness favors brute force;
  invariance needs finer granularity); re-open the diagnosis iff
  H2-F1 or H2-F8 fires.
- **T6 Toolchain.** Pure Zag, safebin, pinned znc; shell only for
  invoking znc, running binaries, git ops, file moves, sha256sum. Any
  forbidden-interpreter invocation is PROCESS-FAIL for that wave.
- **D1..D4 Discrimination battery** (H-CTXPAIR-1 vs H-CTXPAIR-2):
  D1 = S3 frozen: V1 vs V2a on (cdet, total probes, evidence tags).
  Favors H-CTXPAIR-2 iff cdet parity AND V2a probes < V1 probes AND
  the Case-B evidence is PINV-tagged (mechanism attribution, not just
  outcome). D2 = |C|=4 pure-invariant: V1 vs V2b on (cdet, staged
  probes). Favors H-CTXPAIR-2 iff cdet parity AND staged probes <=
  0.4x. D3 = |C|=4 mixed: V1 vs V2b on (cdet, wrong). Favors
  H-CTXPAIR-1 iff V2b shows any wrong-prediction excess or cdet
  shortfall (robustness). D4 = domain-blindness: ctx-id permutation;
  any metric change under permutation falsifies the
  domain-independence claim of whichever variant changes.

## 7. Uncertainties and alternative explanations (honest, pre-result)

- **U1 Marking-rule interaction.** PINV is logged as a knowledge TEST
  (fab=0, kd==1), so a PINV REJECT enters the same path as a PVARY
  knowledge-REJECT, which the R-SUF-1 defect analysis implicates in
  Case-A over-marking (TEST-ACCEPTs discarded after a REJECT). At S3,
  A pairs agree so PINV REJECTs should be ~0 and M1 additionally
  REMOVES fabrication-REJECT events (replaced by PINV-ACCEPTs), which
  may DECREASE Case-A marking; but on variant pairs the PINV2 path is
  new REJECT/ACCEPT traffic through that machinery. Direction and
  magnitude are genuinely uncertain; H2-F2 and the T4(i) diagnostic
  guard it.
- **U2 KINV sensitivity.** KINV=3 is a frozen guess. Too high ->
  UNKNOWN on pure-invariant worlds (H2-F6 fires though the idea is
  right); too low -> premature INVARIANT (H2-F7). The preregistered
  {2,5} robustness run (T3) measures the slope; it is not a bar.
- **U3 M4 vs both re-expand paths.** M4 must apply in
  `l_guard_reexpand` AND `l_union_reexpand`, including the kind0->kind1
  expansion branch. The builder verifies propagation in both; a path
  miss shows up as H2-F5 on one escalation arm only.
- **U4 |C|>=3 world construction.** The |C|=4 families are new
  artifacts. If the builder's truth/training/stakes construction
  deviates from the T1 spec (e.g. D pairs not trained at all contexts),
  H2-P6/H2-P7 are uninterpretable. Mitigation: builder commits the
  world builder first; parent reviews the spec, not the outputs.
- **U5 Ledger across escalation generations.** Frozen: reset on every
  form rebuild (conservative; invariance learned in round 1 does not
  carry to round 2). A continuing-learner design would carry it with
  provenance; that is future work, not this prereg.
- **U6 Gated-but-untrained pairs.** The ledger only sees trained
  pairs' guards and probe outcomes. A world with context-gated pairs
  that are NEVER trained could read INVARIANT and mispropagate under
  M4: that is a PREDICTED failure mode of per-form granularity, not a
  surprise, and such worlds are out of scope for this prereg (T1
  requires all D pairs trained, as in scale_world.zag).
- **A1 Tiebreak-luck null.** Same as H-CTXPAIR-1 A1: V0 reruns scatter
  5-6/8 and neither V1 nor V2a does systematically better. H2-F8 (and
  H-CTXPAIR-1 H-F5) kill it.
- **A2 Bar-calibration alternative.** Same as H-CTXPAIR-1 A2: score
  T2(ii) over evidenced pairs only; V0 passes and both hypotheses are
  unnecessary machinery. T3 scores the adjusted bar for V0/V1/V2a; if
  V0 passes it, A2 is preferred (architecture compression).
- **A3 "M1 is just H-CTXPAIR-1 M3 by another name."** H-CTXPAIR-1's
  fallback M3 tests the FLIPPED FABRICATION value after a fabrication
  REJECT; M1 tests the ON-CONTEXT KNOWLEDGE value as the primary
  hypothesis and banks invariance evidence. They differ exactly where
  it matters: on the Case-B pairs the tiebreak value is wrong (else
  there would be no Case B), so M3's flipped-tiebreak test banks the
  wrong value's complement only by luck, while M1 tests d directly.
  The V1b-vs-V2a comparison (if V1b is ever built) discriminates; the
  evidence-tag diagnostic (T4(ii)) discriminates regardless.
- **A4 Structural shortcut.** "Read invariance off the form kind:
  kind0 ⇒ invariant, no ledger needed." Counter: a kind0 form's
  prediction can still be REJECTed off-ctx (world-gated pair under a
  contradiction-free training sample); the behavioral ledger is doing
  the real work, and the S3 form is kind1 anyway. If the builder finds
  kind alone predicts the ledger's verdict on all T1 worlds, A4
  collapses M2 to a kind-check and this prereg's M2 is over-machinery.

**L3-boundary note (honest).** The invariance ledger is learner-created
persistent state: formed after experience (not enumerated pre-hoc),
stored in learner state (not source semantics), governs future probing
(reused across pairs via the per-form flag), revises on counterevidence
(one-way to VARIANT), and is described in learned properties only
(guard agreement, probe outcomes) with no human domain labels; it would
behave identically under permuted ctx ids (D4). That is L3-shaped. But
the decision rule (KINV, one-way revision, structural seeding formula)
is researcher-authored, and per-form granularity may be too coarse for
mixed worlds (H2-F7 is the honest boundary). Claim: L2+ with an
L3-shaped component; NOT an L3 representational-invention claim. The
per-entry-group refinement this boundary points at is sketched as
H-CTXPAIR-3 (not preregistered here): invariance ledger per canonical
(x,y) entry-group instead of per form, so one form can hold invariant
and variant pairs simultaneously.

## 8. VOID (terminal) and non-goals

- Any edit to frozen L3-SUF-1 src/ or the adversary's sealed
  worlds/KEY.md (this worker did not inspect them; the builder must
  not).
- Any change to the marking / sole-survivor rule inside V1/V2a/V2b
  (U1 exists precisely to detect if that boundary fails).
- Propagating TRAINING triples across contexts (M4 covers probe
  TEST-ACCEPTs only).
- Any forbidden-interpreter invocation in the future build/test wave.
- Any 3/3 byte-identical divergence in T3 runs.
- Redefining H2-K bars after seeing results; amending this prereg
  instead of writing H-CTXPAIR-3.
- Non-goals: the nent=41 usedp buffer ceiling (separate scaling
  finding); R-SUF-1 Case-A coarseness (with the red team for SUF-K10);
  carrying the ledger across form generations (U5); |C| not in {2,4};
  transfer/reuse/revision/retirement of the invariance belief itself.

## Meta-criteria self-check (from section 0)

H2-CRIT-1 PASS: S0 names the coverage structure and its covered-rule;
M1 names the trigger (fb==1 at c, fb0==0 at s0), the tested value
(v0), tags (PINV/PINV2), fab=0 logging, and budget treatment; M2 names
the ledger fields, all update events, the frozen rule
(inv_bad==0 && inv_ok>=3 -> INVARIANT; inv_bad>=1 -> VARIANT; else
UNKNOWN), one-way revision, and the reset rule; M3 names the
single-context policy and its fallback; M4 names the propagation rule
and its training exclusion; V0/V1/V2a/V2b are all specified.
H2-CRIT-2 PASS: H2-P1..H2-P8 each name battery, seeds, variants,
numbers; H2-K1..H2-K8 are frozen bars; D1..D4 name the favoring
conditions. H2-CRIT-3 PASS: H2-F1..H2-F8 plus A1-A4 cover no-gain,
safety-regression, no-efficiency-gain, ledger-misfire,
completeness-loss, misclassification, luck, misattribution, and the
cheaper alternatives. H2-CRIT-4 PASS: T1 uses worker-owned, fresh-seed,
and builder-built worlds only (world-builder committed before use);
T5/T6 forbid sealed/frozen edits and non-Zag tooling. H2-CRIT-5 PASS:
U1-U6, A1-A4, the L3-boundary note, H-CTXPAIR-3 sketch, D4.
H2-CRIT-6 PASS: Status header, T5 (decision rule is input, not
verdict), section 8; no implementation authorized; L3-SUF-2 not
preempted.
