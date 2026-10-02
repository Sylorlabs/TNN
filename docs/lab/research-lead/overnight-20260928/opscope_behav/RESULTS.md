# RESULTS: OpScope Cross-Context Behavioral Validation (FROZEN)

**Date:** 2026-09-30 (PDT). **Prereg:** 82e0e94fd, Amendments 1 (428c00e23),
2 (54c943702). All committed before implementation. **Status:** COMPLETE.

**Verdict:** OPSCOPE-BEHAV-PASS (bounded L2). All K-bars pass.

## K-bar verification

- **K1 (prereg precedence):** Prereg 82e0e94fd committed alone; Amendments 1
  and 2 committed before any implementation file. Verified via git log.
  Implementation (behav_learner.zag, behav_harness.zag, sealed files)
  committed after. PASS.
- **K2 (frozen predictions):** 3 families x 3 runs, byte-identical per family
  (sha256 verified). All P1..P5 match as frozen (see per-family below).
  One rationale deviation noted (B1/P2 "tak": rejected via (i)-fail not
  (ii)-fail; outcome REJECTED matches). PASS.
- **K3 (purity/determinism):** Pure Zag + shell only, zero Python. 3/3
  byte-identical per family. Exit 0, zero stderr. No em/en dashes.
  Contaminated paper untouched. u8-backed cells only. PASS.

## Per-family outcomes

### Family B1 (R1R4 original, FAM=0, SEED=2001)

- CAND w=1 ("not"): mtch=8, acc_base=11/20, acc_with=20/20. (ii) PASSES.
  p*=1, p'=0. Probe: T'=1, P=0 (mismatch, strict (i) FAILS). V_at_p*=3,
  pos_ok=1. FALLBACK: INSTALL with posmask=2 (1<<1). **Matches P1.**
- CAND w=0 ("tak"): mtch=26, acc_base=11/20, acc_with=17/20. (ii) PASSES
  (17>=11). p*=0, p'=1. Probe: T'=37, P=33 (mismatch). V_at_p*=20, pos_ok=0
  (wrong on 3/20). REJECT (i-fail, no fallback). **Matches P2 outcome
  (REJECTED); rationale deviation: (ii) passed, rejected via (i).**
- CAND w=2,3,9,10: (ii) fails (acc_with < acc_base). REJECTED. **Matches P3
  (no spurious installs).**
- TEST_ACC=20/20, T1=3/3, F1=1, F2=1 (T1=3 vs base=0), F4=1 (abl: T1 0/3,
  acc 17/20), F5=1. **Matches P4.**
- OPREC: k=0, trig=1, sig=0, created=100, sup=16, posmask=2. **Matches P5.**
- VERDICT: OPSCOPE-R1R4-PASS.

### Family B2 (Family A confound, FAM=1, SEED=2002)

- CAND w=4 ("grn"): mtch=4, acc_base=20/20, acc_with=5/20. (ii) FAILS
  decisively (5<20). REJECTED outright (no fallback). **Matches P1.**
- CAND w=1 ("not"): INSTALL via FALLBACK, posmask=2. **Matches P2.**
- INSTALLED: w=1(pm=2) only. CONFOUND_GRN_INSTALLED=0.
  TRUE_NOT_INSTALLED=1. TEST_ACC=20/20. **Matches P3.**
- The 5/20 vs 20/20 (ii) comparison is on V=100..119, capturing the harm on
  ep 100..102 ("tak grn cub") and 106..108 ("tak grn sph"). **Matches P4
  (amended).**
- VERDICT: OPSCOPE-R1R4-PASS. **Matches P5.**

### Family B3 (Displacement, FAM=4, SEED=2003)

- CAND w=1 ("not"): mtch=11, acc_base=11/20, acc_with=20/20. (ii) PASSES.
  p*=0, p'=1. Probe: T'=1, P=1 (MATCH). V_at_p*=0 (no V episode with "not"
  at pos 0), pos_ok=1 (vacuous). STRICT (i) PASSES. INSTALL with posmask=0
  (unrestricted). **Matches P1.**
- INSTALLED: w=1(pm=0). **Matches P1 (posmask=0).**
- TEST_ACC=20/20 (up from 17/20 no-operator baseline). T1=3/3 (ep 109..111
  "tak not grn"; the unrestricted operator fires at pos 1 and predicts
  {tak}). **Matches P2 (amended).**
- F4=1 (ablation: T1 3/3->0/3, acc 20/20->17/20). **Matches P3.**
- VERDICT: OPSCOPE-R1R4-PASS. **Matches P4.**
- Honest scope (P5): The position-0-trained operator implements "after not,
  predict {tak}" via rich op-records. On this battery (all NEGs have T={tak})
  it is correct. This is no more degenerate than the position-1 operator;
  both delete the color contribution. Bounded L2.

## Architecture delta (ONE-SYSTEM RULE)

**Cognition source (behav_learner.zag vs opscope_learner.zag):**
- Lines added: 66
- Lines removed: 105
- Net: -39 (ARCHITECTURAL COMPRESSION)
- New hardcoded semantic cases: 0 (DELETION signature, residual grounding,
  reground replay UNCHANGED; no new operator type)
- New modes: 0
- New bridges: 0
- New task-specific handlers: 0 (the behavioral validation is a GENERIC
  candidate-operator admission mechanism, not specific to negation or DELETION)
- Learner-state structures created: 1 (oppos[8] i32, 32 bytes: valid-position
  bitmask per operator, 0=unrestricted)

**What was removed:** proposal_check (six count bars: epc, reclen, sup,
mtch-rate, div, zero-parameter gate), retire_check, gate_pass as admission.
**What was added:** oppos state, find_op posmask check, train_pos helper,
state_copy helper (for tentative grounding).

The redesign REPLACES six position-sensitive distributional bars with one
generic behavioral check. Net source delta is negative. Capability-source
delta approaches zero: the DELETION semantics are untouched; only the
admission criterion changed from counting to doing.

## Honest ceiling

Bounded L2. The redesign does not invent operator semantics; it changes the
admission criterion from distributional (count bars) to behavioral (tentative
installation + validation). The (ii) validation set V doubles as the reporting
set (documented limitation). The (i) probe uses the world oracle for the
counterfactual target (documented limitation). The FALLBACK's positional
restriction is explicit in state (posmask), not hidden. L3 achieved: zero.

## Commits

- 82e0e94fd: Prereg (FROZEN, alone)
- 428c00e23: Amendment 1 (test-episode references)
- 54c943702: Amendment 2 (probe base from training)
- [implementation commit]: behav_learner.zag, behav_harness.zag, behav_world.zag,
  sealed/behav_all_fam*.zag, sealed/*_run*.out, RESULTS.md

## Final recommendation (standing question)

**Question:** "What general semantic-learning process would identify that not
changes meaning regardless of position?"

**Answer:** The behavioral validation in this experiment is still a GATE: it
asks "should this word be an operator?" and answers via trial installation.
It does not learn position-independent MEANING; it learns position-restricted
(or, in B3's case, accidentally position-general) ROUTING.

A general semantic-learning process would need to separate two things the
current DELETION operator conflates:

1. **Scope identification** (WHAT does "not" apply to?): Currently determined
   by linear position (suffix after trigger). A general process would identify
   the scope via learned semantic features (e.g., "the color word", identified
   by its distributional signature, not its index).

2. **Negation application** (WHAT does "not" do to its scope?): Currently
   implemented via residual records (R = T minus prefix). This part is already
   position-independent in principle; the records learn "after not, the target
   is {tak}" regardless of where "not" sits.

The deeper redesign is NOT another gate. It is a change to the operator
SEMANTICS: from positional routing (prefix/suffix split at trigger index) to
semantic routing (scope determined by learned word-type features). The learner
would need to acquire word TYPES (color vs shape vs size) from distributional
evidence, then bind operator scopes to types rather than positions.

This experiment shows that behavioral validation can SELECT among positional
operators, but it cannot CREATE a position-independent operator because the
DELETION semantics themselves are positional. The next step is not a seventh
bar; it is asking whether the existing general architecture (DELETION via
positional routing + residual learning) can learn type-based scope, or whether
a new semantic primitive is required. If the latter, that primitive must be
justified under the ONE-SYSTEM RULE as a general cognitive operation, not a
negation-specific handler.

**The gate lineage stops here.** Cross-context behavioral validation works as
a final admission criterion (it rejects the Family A confound, installs the
true negator, and overcomes the Position-0 Lemma blindness). But it does not
answer the standing question; it only sharpens it.
