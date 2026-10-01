# Discount Adversary Run: Majority-Wrong World

**Verdict: DISCOUNT-ADVRUN-COMPLETE: W3 ENTRENCHES ERROR.**

The discount mechanism (D1+D2+W3+R1) was run against the majority-wrong
adversarial world from DISCOUNT_ADVERSARY.md (`b0cd36859`). The 42-loop
is wrong (self-generated); the 99 is right (genuine). W3 is source-blind
and punished the truth, exactly as the design predicted.

## 1. Method

Unfrozen variant `adv_bin`: `di_variant.zag` from the discount pilot
(`0daaa2ed4`, SHA-256 `99148ffb...` verified identical) with the original
test main replaced by the adversarial driver (`adv_driver.zag`).
Cognition is byte-identical to the validated discount pilot; only the
driver changed. Compiled with the pinned znc. 3/3 byte-identical runs
(SHA-256 `0f3d76d2d115ff19ccea5267dcfe651753b99f3c9826f1b82fbfc4644df0ecb0`).

Battery (single deterministic workspace):
- Phase 1: 3 seeds (1001/1002/1003, r=50, v=42). In this world these are
  misleading (miscalibrated sensors); true value is 99. 4 fresh queries
  (2001-2004) establish the (wrong) loop.
- Phase 2: ONE genuine 99 via `ev_teach(3001,50,99)`. 6 fresh queries
  (2005-2010).
- M1: 10 fresh queries (2011-2020), count 42 vs -2 vs 99.
- M2: inspect the 99-fact's discount.
- M4: count live 42-facts and 99-facts.
- M3: teach 5 more genuine 99s (4001-4005). Query fresh subjects
  (5001+) until flip to 99 or 100 queries max.
- M5: W2 not in pilot (documented).

## 2. Results (3/3 identical)

### Phase 1: wrong loop established
q0..q3 all returned 42. `n42_after_p1=7` (3 seeds + 4 self-generated).
The learner "believes" 42. This belief is false but internally consistent.

### Phase 2: truth suppressed (mechanism identical to original probe)
| Query | Result | 99 discount | Interpretation |
|-------|--------|-------------|----------------|
| b0 | -2 | 0 -> 1 | W3 fires: 5x42 vs 1x99 |
| b1 | -2 | 1 -> 2 | 99 still eligible |
| b2 | -2 | 2 -> 3 | 99 now excluded |
| b3 | 42 | 3 | R1 excludes 99; 42s unanimous |
| b4 | 42 | 3 | wrong loop resumed |
| b5 | 42 | 3 | wrong loop resumed |

The mechanism behaved EXACTLY as in the discount pilot (`0daaa2ed4`),
where the 99 was noise. Here the 99 is truth. The mechanism cannot
distinguish. This is source-blindness made measurable.

### M1: persistence of wrong inference
`M1_c42=10 M1_cm2=0 M1_c99=0`. All 10 fresh queries returned 42 (wrong).
Zero withheld, zero correct. The system is confidently wrong with no
internal hesitation signal.

### M2: truth exclusion depth
`M2_true99_disc=3`. The genuine 99-fact is at discount 3, structurally
excluded from the bootstrap evidence pool by R1. The truth is not merely
outvoted; it is invisible to inference.

### M4: self-generated amplification
`M4_n42=20 M4_n99=1`.
- 42s: 3 seeds + 4 (Phase 1) + 3 (Phase 2 b3-b5) + 10 (M1) = 20.
- 99s: 1 (the suppressed truth).
- Self-generated 42s during Phases 2-M1: 13. The wrong loop actively
  expanded, creating more majority members that future W3 applications
  will protect. This is the amplification the design predicted.

### M3: rehabilitation cost
`M3_flip_at=60 M3_queries_run=66`.
- 5 genuine 99s taught (idx48-52, discount 0 each).
- The loop flipped to 99 at query 60 (0-indexed; the 61st query).
- 6 post-flip queries confirmed persistence (all 99, 6 new 99-facts taught).
- `final_n42=20` (42s persist in store, excluded, not deleted).
- `final_n99=12` (1 original + 5 rehab + 6 post-flip self-generated).
- `final_true99_disc=3` (original 99 remains excluded; rehabilitation
  came from the 5 new 99s, not from rehabilitating the original).

Rehabilitation cost: 5 taught 99-facts + 60 queries. Each of the 20 42s
required 3 W3 applications to reach exclusion (discount 3). 20 x 3 = 60,
exactly matching the observed flip point. The "epistemic immune response"
is quantified: the system's resistance to correction after W3 has
committed to the wrong majority.

### M5: W2 rehabilitation check
W2 (observe-path confirmation decrement) is not implemented in the
D1+D2+W3+R1 pilot. All 99s entered via `ev_teach`; teach performs no
contradiction check. Documented as a design limitation of the pilot,
not a mechanism finding. If W2 existed, `ev_observe` confirmations of
99 could decrement the discount, providing a rehabilitation path.
Without it, rehabilitation requires overwhelming the majority with
new discounted-zero facts.

## 3. Interpretation

### 3.1 W3 is source-blind (confirmed empirically)
The mechanism behaved identically in the original probe (99=noise,
42=self-generated-but-accepted) and the adversarial world (99=truth,
42=wrong). W3 discounts the minority regardless of truth. This is not
a bug; it is the specified behavior. The adversarial world makes the
cost visible and measurable.

### 3.2 Discount can entrench error
Beyond merely failing to correct, W3 actively suppresses correction:
- M1 shows 10/10 confidently wrong inferences (vs. 0/10 in a system
  that withheld).
- M2 shows structural truth exclusion (discount 3, R1-invisible).
- M4 shows the wrong majority amplifying (13 new 42s).
In the no-discount baseline, the single 99 would have permanently
broken the loop via the unanimity gate (no wrong inference, but no
inference at all). With discount, the loop routes around the
correction and infers wrongly. On the "wrong inference" axis, discount
is worse than no-discount. On the "paralysis" axis, discount is better.
The trade is now quantified.

### 3.3 The fragility fix has an epistemic price (quantified)
The discount spec (Section 5.1) states: "discount trades epistemic
purity for robustness." The adversarial world quantifies the price:
- Price of robustness (original probe): 3 wasted queries to recover
  from a noisy contradiction.
- Price of the trade (adversarial world): 10 confidently wrong
  inferences + 60 queries + 5 taught facts to recover from a
  genuine correction when the majority is wrong.
The asymmetry (3 vs 65) reflects the amplification: the wrong majority
grows (M4), increasing the rehabilitation cost.

### 3.4 What this does not prove
1. It does not show discount is net harmful. The baseline (no discount)
   has permanent paralysis from one contradiction. A full evaluation
   needs both scenarios with a judgment about which failure is more
   costly in the target deployment.
2. It does not show the majority is usually wrong. The adversarial world
   is constructed to make the majority wrong. In natural environments,
   the majority heuristic may be well calibrated. This bounds the worst
   case, not the typical case.
3. It does not invalidate W3. The spec includes W3 because teach-path
   contradictions have no other discount write path. This is a known
   limitation to be documented, not a refutation.

### 3.5 Why C6 (source provenance) is the actual fix
With source tags from the first write, W3 could prefer genuine minority
over self-generated majority. Without them, it cannot. The adversarial
world demonstrates the cost of source-blindness: 65 queries of wrongness.
C6 remains the principled fix; discount is the robustness patch with a
measured epistemic price.

## 4. Standing metrics (this run)

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 5 (adversarial world setup,
  phase definitions, M1-M5 metric definitions; estimated in design)
- LEARNER-OWNED STRUCTURAL DECISIONS: per-fact discount values
  (1 99-fact reached discount 3; 20 42-facts reached discount 3 during
  M3; all values experience-driven)
- SOURCE-ENUMERABLE FORMS: 0 new
- SUF DECISIONS: 0
- LEARNER-INTERNAL CRITERIA: 0 (W3 criterion is researcher-authored)
- REUSE EVENTS: 0
- REVISION EVENTS: 0
- COGNITION LINES: 0 added (reused pilot variant; driver is harness-side)
- MODES: 0. BRIDGES: 0. HANDLERS: 0. SEMANTIC CASES: 0.

## 5. Deliverables

All in `docs/lab/research-lead/overnight-20260928/discount_advrun/`:
- `NAMECHECK.md` (Step 0 toolchain guard, scope, provenance)
- `DISCOUNT_ADVRUN.md` (this report)
- `adv_driver.zag` (adversarial battery driver)
- `adv_variant.zag` (verbatim copy of discount pilot cognition,
  SHA-256 `99148ffb...` verified identical to `0daaa2ed4`)
- `adv_full.zag` (compiled unit: variant + driver)
- `adv_bin` (pinned-znc binary)
- `adv_run1.txt`, `adv_run2.txt`, `adv_run3.txt` (3/3 byte-identical,
  SHA-256 `0f3d76d2d115ff19ccea5267dcfe651753b99f3c9826f1b82fbfc4644df0ecb0`)

**Verdict: DISCOUNT-ADVRUN-COMPLETE: W3 ENTRENCHES ERROR.**
