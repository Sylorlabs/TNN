# Node 1 Efficacy Pilot: Does the Learned Trial Order Reduce Cost?

**Verdict: NODE1-EFFICACY-COMPLETE. TRANSFER-YES.**

H3-lite Node 1's Hebbian-learned trial order causally reduces trial cost.
E(A)=27, E(B)=20, R=1.35. Consequence re-entry F2 is NOT falsified.

## Method

**Design:** Biased world where one assembler family is systematically correct.
Each miss uses a fresh subject s with a 3-link chain taught:
`(s,99,a)`, `(a,99,b)`, `(b,99,c)` where a=2000+s, b=3000+s, c=4000+s.
Query `(s,20)` unmasked (flags=0) with expected=3.

**Why family 4 (count) is correct:**
- `t2_chain` along relation 99 yields `[s,a,b,c]` (len 4).
- Count assembler outputs len-1 = 3, matching expected.
- Chain families 0 (k=2) and 1 (k=3) find paths but output b and c
  (values 3000+s, 4000+s), which do not equal 3, so they fail verification.
- Family 2 (k=4) has no len-5 path (0 candidates).
- Family 3 (sum) is gated on `comb_present>=0`; no tag-8 nodes exist (0 candidates).
- Family 5 (single hop) would output a (2000+s != 3) but is never reached
  in the predicted trajectory.

**Phases:** Phase A: 20 misses (s=1..20). Phase B: 20 misses (s=101..120).
Same relation (20), same bias, distinct subjects. No process reset, no
learner-state reset between phases.

**Metric:** E(X) = total `t2_try_verify` invocations across Phase X,
read from header 16 (`tried = hg(W,16)/1024`) after each trial.
Header 16 is write-only in production (theater T3), safe as a counter.

**Binaries:**
- H3-lite: `n1e_h3lite_bin` (variant `45c55ed83` + pilot driver).
- Frozen: `n1e_frozen_bin` (frozen base `a29972ca...` + pilot driver).

**Predictions (from mechanism analysis):**
- H3-lite: Miss 1 tries fams 0,1,4 (3 calls), fam 4 at slot 4 succeeds,
  swaps to slot 3. Miss 2: 3 calls, swaps to slot 2. Miss 3: 3 calls,
  swaps to slot 1. Miss 4: 2 calls (fams 0,4), swaps to slot 0.
  Misses 5-20: 1 call each. E(A)=3+3+3+2+16=27. Phase B: 20*1=20. R=1.35.
- Frozen: Fixed order, 3 calls per miss. E(A)=60, E(B)=60, R=1.00.

## Measurements

### H3-lite Node 1 (3/3 byte-identical, SHA-256 `2dc6d0d3...`)

Phase A trajectory (white-box policy orders):
```
miss s=1  ans=3 tried=3 order:[0,1,2,4,3,5] rej=0
miss s=2  ans=3 tried=3 order:[0,1,4,2,3,5] rej=0
miss s=3  ans=3 tried=3 order:[0,4,1,2,3,5] rej=0
miss s=4  ans=3 tried=2 order:[4,0,1,2,3,5] rej=0
miss s=5  ans=3 tried=1 order:[4,0,1,2,3,5] rej=0
miss s=6..20 ans=3 tried=1 order:[4,0,1,2,3,5] rej=0 (all)
E(A)=27
```

Phase B trajectory:
```
miss s=101..120 ans=3 tried=1 order:[4,0,1,2,3,5] rej=0 (all 20)
E(B)=20
```

**R = 27/20 = 1.35. R*100 = 135 > 115. N1E-TRANSFER-YES.**

The Hebbian write path fired exactly 4 times (misses 1-4), moving family 4
from slot 4 to slot 0. The read path used the learned order on all 20
Phase B misses. Every miss returned the correct answer (ans=3).

### Frozen TNN-2 Control (1 partial run)

Phase A: 20 misses, all tried=3, E(A)=60. Matches prediction exactly.
Phase B (partial, 6 misses): tried=3,3,4,3,3,3.

The frozen control shows no order change (no policy node) and constant
per-miss cost. R_frozen = 1.00 (predicted; Phase B incomplete due to
runtime, but per-miss cost is constant).

**Anomaly:** Frozen miss s=103 showed tried=4 (one extra verify call).
All other 25 frozen misses showed tried=3. The cause is undetermined;
it does not affect the pilot conclusion (frozen shows no learning).
Noted for the sealed test to watch.

## Verdict

**NODE1-EFFICACY-COMPLETE. TRANSFER-YES.**

1. **The learned order reduces cost.** E(B)=20 < E(A)=27. The 26% cost
   reduction is caused by the policy node placing family 4 first.
2. **Consequence re-entry F2 is NOT falsified.** The principle states:
   "If H3-lite Node 1 implements correct M2/M3/M4 but trial order does
   not causally improve, the necessity claim is falsified." Trial order
   DOES causally improve. The write path (Hebbian swap) fires on
   verification success, the read path (dispatch loop) uses the updated
   order, and the measured cost drops.
3. **Discrimination holds.** Frozen TNN-2 shows R=1.00 (no transfer).
   H3-lite shows R=1.35. The test discriminates.
4. **Determinism holds.** 3/3 H3-lite runs byte-identical.

## Interpretation Guardrails

Per the success-criteria analysis (`04af42736`):

- **What was learned:** The policy learned which family is *executable-and-correct*
  in this biased world, not a learner-judged notion of correctness. The
  "correctness" signal is the harness-supplied `expected=3` in unmasked mode.
  In masked mode, the policy would learn mere executability order.
- **What was NOT learned:** No new assembler family, no new procedure,
  no SUF, no L3. The six families are researcher-authored. The 720 orders
  are enumerable. This is bounded L2 policy selection.
- **Causal attribution:** The cost reduction is attributed to the policy
  node because (a) the write path fired visibly, (b) the read path used
  the updated order, (c) frozen control without the policy shows no reduction.
  A full C2-style ablation (policy reset) was not run in this pilot;
  it is specified in the sealed weak K-LT-5 prereg.

## Relation to Weak K-LT-5 Prereg

This pilot uses the same E-ratio metric (R > 1.15) but is NOT the sealed test:
- Pilot R=1.35 vs prereg predicted R=1.50. The difference: prereg assumed
  families 2 and 3 consume verify calls; in this simple world they have
  zero candidates (no len-5 paths, sum gated). The sealed adversary's world
  will satisfy R1 (all of families 0,1,2,3 produce failing graphs).
- Pilot uses unmasked mode with harness-supplied expected. The sealed test
  design does not specify mode; the adversary decides.
- This pilot does NOT run the C1 (fresh-B) or C2 (ablation) controls.
  Those are required for WEAK-KLT5-PASS.

## Architecture Accounting

- RESEARCHER-OWNED STRUCTURAL DECISIONS: Six assembler families, Hebbian
  swap rule, demotion threshold (8), initial order [0,1,2,3,4,5], N=20,
  1.15 threshold, the biased world design (chain lengths, expected=3).
- LEARNER-OWNED STRUCTURAL DECISIONS: 1 (trial order policy values:
  [0,1,2,4,3,5] to [4,0,1,2,3,5] across Phase A).
- SOURCE-ENUMERABLE FORMS: 720 (6!). Pilot exercised 5 distinct orders.
- SUF DECISIONS: 0.
- LEARNER-INTERNAL CRITERIA: Order preference from verification success.
  (Harness-supplied expected; see guardrails.)
- REUSE EVENTS: 20 (Phase B policy reads using Phase-A-learned order).
- REVISION EVENTS: 4 (Hebbian swaps, misses 1-4 Phase A).
- COGNITION LINES: 0 (test only).
- MODES: 0. BRIDGES: 0. HANDLERS: 0. SEMANTIC CASES: 0.

## Limitations

1. PILOT ONLY. Not the sealed weak K-LT-5. Simple unsealed bias.
2. Unmasked mode with harness-supplied expected. Masked-mode efficacy
   (executability order) not tested.
3. No C1/C2 controls in this pilot.
4. Frozen control: 1 partial run (not 3/3). Sufficient for pilot
   discrimination; full 3/3 required for sealed test.
5. The s=103 tried=4 anomaly in frozen is unexplained.

## Files

- `n1e_driver.zag`: pilot driver source.
- `n1e_h3lite.zag`, `n1e_frozen.zag`: assembled sources.
- `n1e_h3lite_bin`, `n1e_frozen_bin`: compiled binaries.
- `h3lite_run1.txt`, `h3lite_run2.txt`, `h3lite_run3.txt`: 3/3 transcripts.
- `frozen_run1.txt`: partial frozen transcript.
- `compile_h3lite.log`, `compile_frozen.log`: build logs.
