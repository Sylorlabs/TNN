# PREREG: NT-D1 -- Preserve evidence across eviction/re-insertion

## 1. Question

H3 (C416 FAIL, null result, output byte-identical to NT2) proved the
revision rule is dead code under NT2's lowest-net eviction:
contradiction depresses net to the insertion baseline (sup=2, ref=1 ->
net=1 = fresh key) BEFORE ref can exceed sup, so keys are evicted
mid-revision and re-inserted fresh (sup=1, ref=0). The breaking
interaction is EVICTION-PREEMPTING-REVISION, and the reset that matters
is the EVICTION-REINSERTION reset, which H3 was barred from touching
("only the revision rule changes"). H1 and NT2 fail at different
interaction points; no single revision-rule change fixes both.

D1: when a key is evicted and later re-inserted, RESTORE its prior
(sup, ref, value) instead of starting fresh (sup=1, ref=0). Rationale:
eviction is about capacity, not about forgetting; the evidence should
survive. This is the minimal change H3's diagnosis points to, and the
one H3 froze.

Frozen question: does D1 let revision complete under capacity
pressure, with minimal evictions and nothing needlessly forgotten?

## 2. Subject (frozen rules + the single D1 change)

NT2's ML1/ML0, oracles, protocol, capacity, and every rule are frozen
verbatim EXCEPT the insertion rule, which gains D1. Keys and values are
bare integers (opaque identifiers); the learner has no task semantics.

### 2.1 D1 rule (precise, frozen)

- Each learner holds a CHECKPOINT TABLE: 40 entries (keys 100..139),
  each (valid: i32, value: i32, sup: i32, ref: i32), zero-initialized
  with the learner. This is learner state, not instrumentation: it
  records only what the learner itself experienced (no oracle or task
  information), and it never influences any decision except restoring
  a re-inserted key's own prior evidence.
- On EVICTION of key hk from slot e (ML1, table full): BEFORE the
  slot is overwritten, write checkpoint[hk] = (valid=1,
  value=slot.value, sup=slot.sup, ref=slot.ref). Then proceed with the
  frozen eviction bookkeeping (nevict++, per-key histogram).
- On INSERTION of an absent key k: if checkpoint[k].valid == 1,
  install slot = (k, ck.value, ck.sup, ck.ref), then process the taught
  value through the FROZEN update step (value match -> sup++; mismatch
  -> ref++, then the frozen revise check ref > sup -> revise to (new
  value, sup=1, ref=0)). If checkpoint[k].valid == 0, install (k,
  taught value, sup=1, ref=0) exactly as before.
- Checkpoint entries are overwritten on each eviction (latest state
  wins). They are never cleared on restore: a stale entry is
  unreachable, because re-insertion requires absence, absence requires
  a prior eviction, and eviction overwrites the entry.
- ML0: the checkpoint table exists but is never written (ML0 never
  evicts; nevict = 0 identically), so ML0 behavior is byte-identical
  to NT2. The restore path is gated on checkpoint validity, which only
  eviction can set.

### 2.2 Everything else frozen (NT2 PREREG Section 2 verbatim)

- Slot table: (key, value, sup, ref); CAP = 30. Rationale unchanged:
  B has 24 keys, A-union-B has 36 distinct keys, 24 <= 30 < 36, so a
  stable all-B solution exists and failure is attributable to the
  eviction/revision interaction, not impossibility.
- Eviction rule: globally lowest (sup - ref); ties resolve to the
  lowest slot index. Entry-local counters only; no protection, no
  importance, no task identity. H1's total-evidence comparator is NOT
  adopted (that is D2 territory, a separate hypothesis).
- `nt_learn` update: present and value matches -> sup++; present and
  value differs -> ref++, and if ref > sup REVISE to (key, new value,
  sup=1, ref=0). The revision RESET is untouched (H3's change is not
  adopted; D1 changes only the insertion rule).
- `nt_predict`: slot holds key and sup > ref -> value; else -1.
- ML1: associative lookup (linear scan), insert at first empty slot or
  the eviction victim's slot. ML0: NT1's overlapping map verbatim
  (slot(key) = key-100 for key < 124 else key-116); aliased writes
  destroy; never fills (24 entries max), never evicts.
- Measurement-only eviction histogram (40 bins, keys 100..139).

## 3. Task families (frozen numeric inventory; opaque identifiers)

Identical to NT1/NT2, verbatim. Keys are integers 100..139. Values are
integers 200..263. No semantic labels anywhere.

- VA(k) = 200 + ((k*37 + 11) mod 64), for all k. (Oracle, family A.)
- SET_A: keys 100..123 (24 keys), values VA(k).
- SET_B: keys 100..111 (12 shared) + keys 128..139 (12 novel).
  VB(k) = VA(k) for k in 106..111 and 128..139; for contradicted keys
  k in 100..105: VB(k) = 200 + (((VA(k)-200)+32) mod 64), guaranteed
  different from VA(k).
- Retest partition of A's 24 keys: C (contradicted) 100..105, correct
  VB(k); NC (non-contradicted, agreed) 106..111, correct VA(k)=VB(k);
  U (untouched) 112..123, correct VA(k).

## 4. Protocol (frozen; NT2 Section 4 verbatim)

Deterministic: fixed ascending key order per pass, no RNG. One pass =
teach every key of the train set once in ascending order, then probe.

- `train_to_criterion(set, valfn)`: repeat passes; after each pass
  probe every key of the set. Criterion = 100% correct on all set keys
  for 2 consecutive passes. Max 50 passes (fail-safe; hitting it = arm
  FAIL). Returns passes used (TTC).
- Phase B uses FIXED passes: 6 B passes (1.5x NT1's TTC_B_seq = 4).
- Arms (each on a FRESH learner):
  - CONTROL-A (ML1): train SET_A/VA to criterion. Records TTC_A_ctrl,
    probe accuracy, nevict (predicted 0).
  - CONTROL-B (ML1): train SET_B/VB to criterion. Records TTC_B_ctrl,
    pc (passes until C correct), probe accuracy, nevict (predicted 0).
  - SEQ (ML1): train SET_A/VA to criterion (TTC_A_seq); probe SET_A
    (sanity 24/24); 6 fixed passes of SET_B/VB; probe SET_B (accB);
    RETEST: probe the 24 A keys, scoring C/NC/U separately; count
    FORGET = keys answering neither the A-correct nor (for C) the
    B-correct value; record nevict, nentries, eviction histogram.
  - ABLATION (ML0): identical protocol on a fresh ML0 learner.

### What "correct" looks like under D1 (frozen)

A correct outcome: (i) evictions at the pigeonhole minimum (Section 5),
no churn; (ii) contradicted keys complete revision; (iii) nothing is
forgotten that the table could have kept (FORGET = 0). I.e., D1
preserves the NT1 selective-retention pattern under pressure, with
pressure costing only the forced minimum.

## 5. Correct kill bars: pigeonhole derivation (replaces NT2/H1/H3 K2)

NT2, H1, and H3 all used K2: nevict == 6 ("12 novel keys minus 6 free
slots"). H3's REPORT (item 4) showed this is arithmetically impossible
jointly with K3+K4. The correct bound, derived from 36 keys vs 30
slots:

- 36 distinct keys are active (24 A-union + 12 B-novel); CAP = 30.
- Lemma: FORGET = 0 requires all 12 U keys (112..123) to survive phase
  B. Proof: U keys are never taught during B; an evicted U key can
  never be re-inserted; it would answer -1 (unknown) at retest, so
  FORGET >= 1.
- Hence under FORGET = 0, the 12 U keys pin 12 slots throughout B.
- Pass 1: phase A filled 24 slots, 6 free. Teaching 100..111 hits;
  teaching the 12 novel keys 128..139: 6 fill the free slots, 6 force
  evictions. Exactly 6 evictions; fewer is impossible.
- Passes 2..6: the table is full (30/30; nentries never decreases).
  At pass start, s shared keys (100..111) + n novel keys (128..139) +
  12 U keys = 30 residents, so s + n = 18. Absent teachings in the
  pass: every shared key outside the resident s is taught while
  absent (>= 12 - s), and every novel key outside the resident n is
  taught while absent (>= 12 - n). Total absent teachings >= 24 - 18
  = 6. Each absent teaching into a full table forces exactly one
  eviction. So each of passes 2..6 has >= 6 evictions.
- Total: nevict >= 6 + 5*6 = 36.

Therefore the correct "eviction minimal, no churn" bar is:

- K2: nevict_seq == 36.

The bound is tight: 36 is achievable iff every pass has exactly 6
evictions with no cascading re-evictions. Any excess over 36 is churn
(keys evicted that need not have moved). Note the >= 36 derivation
assumes the FORGET = 0 regime (U pinned); K4 enforces FORGET = 0
independently, and K2 measures churn against the forced minimum.

Consequences for the old bars: nevict == 6 is impossible (it would
require 30 slots to hold 36 keys' worth of insertions with only 6
displacements while retaining all 24 A keys). Any future bar must use
36, not 6.

## 6. Frozen predictions (hand-derived by tracing the frozen D1 rules)

Two independent hand-traces of Sections 2-4; mechanism, not just
numbers. Slot order after phase A: keys 100..123 in slots 0..23, each
(VA, sup=2, ref=0).

- B pass 1: 100..105 contradicted -> (VA,2,1), net=1. 106..111 match
  -> sup=3. 128..133 fill slots 24..29 (VB,1,0), net=1. 134..139:
  table full; lowest net=1 ties C keys (slots 0..5) vs 128..133
  (slots 24..29); lowest slot index evicts 100..105 one by one;
  checkpoint (VA,2,1) each. nevict=6.
- B pass 2: 100..105 absent -> evict 134..139 (slots 0..5, net=1,
  lowest index), checkpoint (VB,1,0); restore (VA,2,1), taught VB ->
  ref=2, not > sup=2, keep VA: (VA,2,2), net=0. 106..111 -> sup=4.
  128..133 match -> sup=2. 134..139 absent -> evict 100..105 (net=0,
  unique minimum), checkpoint (VA,2,2); restore (VB,1,0), match ->
  sup=2. nevict=18.
- B pass 3: 100..105 absent -> evict 134..139 (net=2, slots 0..5 win
  the tie at net=2 against U slots 12..23 and 128..133 slots 24..29),
  checkpoint (VB,2,0); restore (VA,2,2), taught VB -> ref=3 > sup=2 ->
  REVISE to (VB,1,0). 106..111 -> sup=5. 128..133 -> sup=3. 134..139
  absent -> evict 100..105 (net=1, unique minimum), checkpoint
  (VB,1,0); restore (VB,2,0), match -> sup=3. nevict=30.
- B pass 4: 100..105 absent -> lowest net is now the never-reinforced
  U keys (net=2, slots 12..23; churning keys are at net>=3);
  evict 112..117 (slots 12..17), checkpoint (VA,2,0); restore
  (VB,1,0), taught VB -> match -> sup=2. 106..111 -> sup=6. 128..139
  all present -> sup=4/5. nevict=36.
- B passes 5-6: every taught key present; no evictions. nevict=36.

Frozen numeric predictions:

- CONTROL-A: TTC_A_ctrl = 2, acc = 24/24, nevict = 0. (D1 never
  triggers; no eviction possible.)
- CONTROL-B: TTC_B_ctrl = 2, pc = 1, acc = 24/24, nevict = 0.
- SEQ: TTC_A_seq = 2; phase-A probe 24/24; after 6 B passes,
  accB = 24/24; nevict = 36, nentries = 30.
- SEQ retest: C_VB = 6/6, NC_OK = 6/6, U_OK = 6/12, FORGET = 6
  (keys 112..117).
- SEQ eviction histogram (key=count, nonzero only): 100=3, 101=3,
  102=3, 103=3, 104=3, 105=3, 112=1, 113=1, 114=1, 115=1, 116=1,
  117=1, 134=2, 135=2, 136=2, 137=2, 138=2, 139=2; all others 0.
  (Sum = 18+6+12 = 36.)
- ABLATION (ML0): TTC_A_abl = 2; accB_abl = 24/24; nevict_abl = 0;
  nalias_abl = 12; nentries_abl = 24; retest C_VB = 6/6, NC_OK = 6/6,
  U_OK = 0/12, FORGET_abl = 12. (D1 never triggers; NT2-identical.)

### Predicted mechanism

D1 lets ref accumulate across eviction boundaries: C keys reach
ref=3 > sup=2 in B pass 3 and revise (C_VB 0/6 -> 6/6); the
eviction-preempting-revision cycle is broken. Evictions hit the
pigeonhole minimum (41 -> 36, no churn: exactly 6 per pass). But the
revised C keys collapse to net=1 under the UNTOUCHED revision reset,
so returning novel keys evict them; when the C keys return in pass 4,
the lowest-net victims are the never-reinforced U keys (net=2, frozen
while every taught key's net grows). Six U keys (112..117) are
displaced in pass 4 and, never taught in B, never return. Forgetting
is conserved by capacity (36 keys vs 30 slots) but RELOCATED: from the
contradicted keys (NT2) to untouched keys (D1).

Predicted verdict: FAIL (K3 and K4 fail; K1, K2, K5 hold). D1 fixes
revision-preemption and churn, but the frozen lowest-net comparator
punishes staleness, which D1 does not touch -- so FORGET = 0 is not
achieved. The predicted signature (revision completes, minimal
evictions, U-keys forgotten) discriminates D1's mechanism from NT2's
(C forgotten), H1's (1 key forgotten via revolving door), and H3's
(null).

## 7. Frozen kill bars

- K1 (learning intact under capacity; else VOID): TTC_A_ctrl in 1..50
  AND acc 24/24; TTC_B_ctrl in 1..50 AND acc 24/24; TTC_A_seq in 1..50
  AND accA 24/24. Else VOID (capacity itself broke learning; redesign,
  do not reinterpret).
- K2 (eviction at pigeonhole minimum, no churn): nevict_seq == 36.
  (Section 5 derivation. The NT2/H1/H3 literal of 6 is arithmetically
  impossible jointly with FORGET = 0 and is retired.)
- K3 (uncontested retention survives): SEQ retest NC_OK = 6/6 AND
  U_OK = 12/12.
- K4 (revision survives pressure): SEQ retest C_VB >= 5/6 AND
  FORGET = 0 across all 24 A keys.
- K5 (discriminative validity): ML0 ABLATION shows the pure alias
  signature (U_OK_abl = 0/12 AND nevict_abl = 0 AND nalias_abl = 12)
  AND ML1's signature differs (nevict_seq != nevict_abl). If ML0's
  signature matched ML1's, the apparatus cannot distinguish fragility
  modes -> verdict INCONCLUSIVE, never PASS.

## 8. Verdict mapping (frozen)

- K1..K5 all hold: PASS -- D1 preserves selective retention under
  capacity pressure: revision completes, evictions are minimal (36),
  nothing needlessly forgotten.
- K1 fails: VOID -- redesign.
- K1 holds, K5 fails: INCONCLUSIVE -- apparatus lacks discriminative
  power; PASS is forbidden.
- K2 fails (K1, K3, K4, K5 hold): FAIL -- churn persists beyond the
  forced minimum; D1 did not stabilize eviction.
- K3 or K4 fail (K1, K2, K5 hold): FAIL -- D1 does not preserve the
  retention pattern: K3-fail = uncontested keys lost under pressure;
  K4-fail = contradicted keys never complete revision (C_VB collapse)
  or keys forgotten (FORGET > 0).
- (Predicted: K3 and K4 fail; K1, K2, K5 hold -> FAIL with the
  Section 6 signature.)

## 9. Follow-up direction (NOT implemented; preregistered)

- If D1 PASSES: port the pressure-tested rule to the shared
  continuing-learner substrate and scale the pressure ratio.
- If D1 FAILS as predicted (revision completes but U keys forgotten):
  the failure is diagnostic. Do NOT patch D1's restore or add
  protection. The preregistered next hypothesis is D2: an eviction
  comparator that does not punish staleness/contradiction (it must
  distinguish "low evidence because new" from "low net because
  contested" from "low net because untouched"), each needing its own
  prereg with kill bars derived from Section 5. A D1+H1-total-evidence
  compound is a two-change hypothesis, not a D1 repair.
- If D1 FAILS with a different signature (e.g. churn persists, or
  revision still preempted): re-derive the mechanism from the binary
  before theorizing; the Section 6 trace may have an error.

## 10. Honest boundaries (pre-declared)

- ML1/ML0 are MINIMAL SURROGATES for the principle under test
  (entry-local evidence revision vs eviction interactions), not TNN's
  production memory substrate. A result here characterizes the
  principle and the measurement apparatus, not TNN-as-built.
- Families are memorized key-value mappings, not induced rules; the
  experiment measures retention/revision/eviction dynamics, not rule
  learning (L1 memorization substrate; no L2/L3 claim).
- Single capacity point (CAP=30, ratio 36/30 = 1.2x over capacity);
  scaling the pressure ratio is out of scope.
- Single contradiction magnitude (one alternative value per C key);
  graded/partial contradiction is out of scope.
- The eviction histogram and the checkpoint table: the histogram is
  measurement-only instrumentation and influences no learner
  decision. The checkpoint table IS learner state (it restores the
  learner's own prior evidence); it contains no oracle/task
  information and is written only by the learner's own eviction
  events.
- The tie-break (lowest slot index) is part of the frozen generic
  rule, not a tuned choice; per the no-patch-treadmill rule it is not
  patched here whatever the outcome.

## 11. Amendment record (transparent; committed before implementation)

(None.)
