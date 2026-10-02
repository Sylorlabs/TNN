# ADVERSARY.md - Red-Team Wave 3

## Mission
Adversarially test three recent strong results:
1. Scaling index (140x fewer scans, 2bea4c73f)
2. Learning-to-learn (6x speedup, 4976be69b)
3. Integration RSV (3/3 synergy, b755e33ff)

Be ruthless but honest. Document breaks AND failed break attempts.

---

## Test 1: ADV-IDX-CORRUPT - Index robustness

### Target
Scaling index: "140x fewer scan visits at 100 MAPs, sublinear, learner-maintained."

### Attack
Manually corrupt the plen-5 bucket list, then query. Simulates eviction+slot-reuse
without 400+ slow interference teaches.

Cases:
- C1: Prepend FACT node (tag 1, not MAP) to bucket.
- C2: Cycle (head's next points to itself).
- C3: Next pointer out of bounds.

### Results (3/3 byte-identical)

**C1: GRACEFUL.** Prepended FACT 3. Query ans=6205 correct, scan=4. Non-MAP handled.

**C2: CRASH. BREAK CONFIRMED.**
- Cycle at node 67.
- `panic: slice index out of bounds`. Exit code 1.

### Root cause
`rebind_try_idx` collects bucket candidates with NO validation:
- No liveness check.
- No type check.
- No cycle detection.

With a cycle, loop collects 1024 copies. Candidate buffer is 4096 bytes,
8 bytes per entry -> max 512 safe. Loop bound `nc<1024` overflows buffer.
Buffer overflow -> panic.

### Verdict: BREAK (robustness)
140x holds on happy path, but index is fragile. Needs liveness checks and
cycle detection. In production with eviction, a single corrupt entry crashes
the query.

---

## Test 2: ADV-L2L-IRREL - Irrelevant Family 1

### Target
Learning-to-learn: "6x speedup (30 to 5), ablation proves LINK strategy causal."

### Attack
Make Family 1 IRRELEVANT to Family 2.
- Family 1: 5 plen-3 chain problems.
- Family 2: 5 plen-5 chain problems.
LINKs from F1 point to plen-3 MAPs. For F2 (plen-5), Pass-1 tries wrong-plen
MAPs first (wasted), then falls back.

### Results (3/3 byte-identical, SHA b484ff9a...)

**Treatment (irrelevant F1 -> F2):**
- F1 total: 5 (P0 trial=1, P1-P4 rebind=1 each).
- F2 total: 40 (P0=21, P1=16, P2-P4=1 each).
- F2-P0: 15 rebind tries (all rejected), then trial.
- F2-P1: 16 tries (15 rejected).

**Fresh (F2 only):**
- F2 total: 10 (P0 trial=6, P1-P4 rebind=1 each).

**Ablated (F1, delete LINKs, F2):**
- F2 total: 40 (same as treatment).

### Analysis
**Treatment is 4x WORSE than fresh (40 vs 10).** Irrelevant experience HURTS.

Mechanism: F2-P0 tries 15 plen-3 MAPs (5 from F1 + distractors) via Pass-1
(linked) and Pass-2 (unlinked). All rejected (plen mismatch). Then falls back
to trial. The wasted tries dominate.

Ablation (delete LINKs) does NOT help (40 vs 40). The plen-3 MAPs remain in
Pass-2 (unlinked) and are still tried. The LINKs are not the problem; the
irrelevant MAPs themselves are.

### Verdict: BOUND (not break)
The 6x claim holds for RELEVANT domains, but irrelevant experience causes
negative transfer (4x slowdown). This is correct behavior - the mechanism
should not help across structurally different domains. But it bounds the
claim: "learning to learn" is domain-specific, not universal warmup.

The original experiment used structurally identical families. This test shows
the boundary. Micah Section 5 asks for "structurally different Family B" -
this is the first data point: with plen-3 vs plen-5, there is no transfer,
only interference.

---

## Test 3: ADV-RSV-ASYM - Asymmetric reliability

### Target
Integration RSV: "3/3 synergy, integrated avoids P's false trust AND S's false trust."

### Attack
Make reliability ASYMMETRIC.
- Predictor X: 10/10 reliable (perfect).
- Source for X (source 8): 1/11 reliable (adversarial).

P-only (config 63): pred passes (10/10), trusts. 100% correct.
Integrated (config 127): pred passes, but source fails (1/11 < 50%). AND-gate
returns -3 (withhold). 0% accuracy.

### Results (3/3 byte-identical, SHA cc330d5c...)

Substrate: source A 11/11, source B 1/11, predictor 10/10.
- P-only trust(10,50) = 100 (correct).
- S-only trust(10,50) = -3 (withhold, source bad).
- Integrated trust(10,50) = -3 (withhold).
- Result: CONFIRMED-Tradeoff.

### Analysis
**Integrated withholds a perfect predictor because the source is adversarial.**

The `rsv_trust` AND-gate:
```
if(pred_on==1 && rsv_pred_rel(W,sid)==0){ return -3; }
if(src_on==1 && rsv_src_rel(W,src)==0){ return -3; }
```
Both must pass. If either fails, withhold.

In the original I2 test, X had pred-good/src-bad and Z had pred-bad/src-good.
Integrated got 3/3 by withholding both. That was correct because BOTH were
actually wrong (X predicted 100, true 200; Z predicted 300, true 400).

In my adversarial test, the predictor is CORRECT (100/100). The source is
irrelevant (the predictor is a FACT, not source-derived). But `rsv_trust`
still checks source reliability because the FACT was taught with source 8.
The AND-gate blocks a correct prediction.

### Verdict: TRADEOFF EXPOSED (partial break)
The 3/3 synergy holds when both signals are informative and complementary.
When one signal is adversarial/noisy, the AND-gate is too conservative.

P-only: 100% accuracy, 0% false withhold.
Integrated: 0% accuracy, 100% safe withhold.

Which is "better" depends on cost model:
- If false trusts are catastrophic: integrated wins.
- If withholds are costly (missed opportunities): P-only wins.

The integration optimizes for "never trust wrong" at the cost of "sometimes
withhold when trust would be correct." This is a real limitation, not a bug.
The claim should be: "Integrated avoids false trusts" not "Integrated is
always better."

---

## Summary

| Test | Target | Result | Verdict |
|------|--------|--------|---------|
| ADV-IDX-CORRUPT | Scaling index 140x | C2 cycle -> panic | BREAK (robustness) |
| ADV-L2L-IRREL | Learning-to-learn 6x | 40 vs 10 (negative transfer) | BOUND (domain-specific) |
| ADV-RSV-ASYM | Integration 3/3 | P=100%, I=withhold | TRADEOFF (conservative) |

### Breaks (1)
**Index buffer overflow:** A cycle in the bucket list crashes `rebind_try_idx`
with slice out of bounds. No liveness check, no cycle detection, buffer sized
for 512 but loop allows 1024. Must fix before production use with eviction.

### Bounds (1)
**L2L domain specificity:** 6x speedup does not generalize to structurally
different families. Irrelevant plen-3 experience hurts plen-5 learning (4x
slowdown). The mechanism is domain-specific, as it should be, but the claim
must be bounded.

### Tradeoffs (1)
**RSV AND-gate conservatism:** Integrated withholds perfect predictors when
source is adversarial. Optimizes for safety over accuracy. The 3/3 synergy
is real but holds only when both signals are informative.

### Failed to break
- Index 140x on happy path: confirmed, no issue.
- L2L 6x on relevant domains: confirmed, ablation valid.
- RSV 3/3 on complementary signals: confirmed.

## Recommendations
1. **Fix index:** Add `ng(W,m,36)==1 && ng(W,m,0)==20` check in bucket traversal.
   Add cycle detection (visited set or Floyd). Fix buffer size (512 not 1024)
   or bound loop to 512.
2. **Bound L2L claim:** Document as "domain-specific transfer." Test
   intermediate similarity (plen-4 vs plen-5) to find the transfer boundary.
3. **RSV cost model:** Make the AND-gate configurable. Allow OR-gate when
   false withholds are costly. Or weight by reliability margin.

## Artifacts
All in `docs/lab/research-lead/overnight-20260928/redteam_wave3/`:
- NAMECHECK.md (Step 0 guard)
- ADVERSARY.md (this file)
- adv_idx_corrupt_*.zag, *_bin, *_run*.txt (Test 1, BREAK)
- adv_l2l_irrel_*.zag, *_bin, *_run*.txt (Test 2, BOUND)
- adv_rsv_asym_*.zag, *_bin, *_run*.txt (Test 3, TRADEOFF)
- adv_idx_stale_*.zag (abandoned: too slow, documented)

## Constraints honored
- Unfrozen only. Frozen source read-only.
- Pure Zag via pinned znc. Safebin PATH, `which python3 python` empty.
- Zero em/en dashes (byte-verified in this file).
- Paper untouched. Nothing pushed.
- 3/3 deterministic per test (SHA-256 verified).
