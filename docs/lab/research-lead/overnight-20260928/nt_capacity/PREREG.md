# PREREG: NT-CAPACITY (NT2) -- Selective Retention Under Capacity Pressure

## 1. Question

NT1 (NEG-TRANSFER-1, PASS) proved selective retention emerges from
entry-local error-driven evidence revision with no protection mechanism,
but under no capacity pressure (nevict=0 both arms; eviction implemented
but untested). This battery tests the preregistered follow-up: does the
retention principle survive REAL memory pressure, with eviction active?

Three sub-questions, frozen:

- Q1: Does selective retention (retain NC/U, revise C) survive eviction?
- Q2: What gets evicted -- and is it the right thing? The eviction
  policy must be generic and domain-neutral: no protection flags, no
  importance scores, no task labels, no researcher-supplied "don't
  forget" logic.
- Q3: Does the evidence-revision rule interact correctly with eviction,
  or does eviction preempt revision?

## 2. Subject architectures (frozen rules)

Two learner variants share EVERYTHING except the address map. Both are
domain-neutral: keys and values are bare integers; the learner has no
task semantics. The update rule is NT1's rule verbatim.

### 2.1 Shared memory model

- Learner state: a slot table. Each slot holds (key, value, sup, ref):
  sup = support evidence count, ref = refutation evidence count.
- Capacity: CAP = 30 slots. Rationale (frozen): the B family has 24
  keys and A-union-B has 36 distinct keys, so 24 <= 30 < 36. A stable
  all-B solution EXISTS (all 24 B keys fit simultaneously), so any
  failure to converge under pressure is attributable to the
  eviction/revision interaction, not to impossibility. Pressure begins
  when B's 7th novel key arrives (only 6 free slots after phase A).
- Eviction rule (NT1's implemented-but-untested rule, verbatim): if the
  table is full, evict the slot with globally lowest (sup - ref); ties
  resolve to the lowest slot index. Generic: operates only on
  entry-local evidence counters; no task identity, no importance flags,
  no protection, no modes.
- `nt_learn(key, value)`:
  1. Find the slot holding `key`. If absent and table full, evict per
     rule above (increment nevict and the evicted key's histogram bin);
     if absent and not full, take the first empty slot. Create slot
     (key, value, sup=1, ref=0).
  2. If present and value equals stored value: sup++.
  3. If present and value differs (contradiction): ref++; if ref > sup,
     REVISE the slot to (key, new value, sup=1, ref=0); else keep old value.
- `nt_predict(key)`: if a slot holds `key` and sup > ref, return its
  value; else return -1 (unknown).
- Measurement-only instrumentation: a per-key eviction histogram
  (40 bins, keys 100..139) counts evictions per key. It does not affect
  behavior; it answers Q2 directly.

### 2.2 ML1 (treatment): dedicated addressing, associative under capacity

NT1's ML1 used the fixed map slot(key) = key - 100, which cannot address
36 distinct keys in 30 slots. The dedicated-addressing PRINCIPLE (a key's
entry is never silently destroyed by another key's write; only eviction
frees a slot) is preserved via associative lookup: find = linear scan
for the key; insert = first empty slot, or the eviction victim's slot.
No aliasing is possible. Update/read rules are byte-identical to NT1.

### 2.3 ML0 (negative control): overlapping address map

slot(key) = key - 100 for key < 124, else key - 116 (NT1's map verbatim).
The 12 B-novel keys alias onto the slots of A's U keys (112..123). A
later write to an aliased slot DESTROYS the earlier entry. Update/read
rules are byte-identical to ML1; only the address map differs. With
CAP=30 the map touches only slots 0..23, so ML0 never fills the table
(max 24 entries) and never evicts: its fragility mode is pure aliasing,
distinct from ML1's eviction mode. This gives K5 discriminative power.

### 2.4 `arm` selector

The driver selects ML1 vs ML0 with an integer `arm` parameter in the
HARNESS (experimental condition selector, 0 = ML1, 1 = ML0). This is not
a cognitive mode: the learner itself has no modes, no task routing, no
conditional behavior on task identity.

## 3. Task families (frozen numeric inventory; opaque identifiers)

Identical to NT1, verbatim. Keys are integers 100..139. Values are
integers 200..263. No semantic labels exist anywhere in code or output;
sets are defined by numeric bounds only.

- VA(k) = 200 + ((k*37 + 11) mod 64), for all k. (Oracle for family A.)
- Family A train set SET_A: keys 100..123 (24 keys), values VA(k).
- Family B train set SET_B: keys 100..111 (12 shared) + keys 128..139
  (12 novel), 24 keys. VB(k) = VA(k) for k in 106..111 and 128..139;
  for contradicted keys k in 100..105: VB(k) = 200 + (((VA(k)-200)+32)
  mod 64), which is GUARANTEED different from VA(k).
- Retest partition of A's 24 keys:
  - C (contradicted): 100..105 (6 keys). B teaches a different value.
    Correct retest answer: VB(k) (revised).
  - NC (non-contradicted, agreed): 106..111 (6 keys). B teaches the same
    value. Correct retest answer: VA(k) = VB(k) (retained).
  - U (untouched): 112..123 (12 keys). B never mentions them.
    Correct retest answer: VA(k) (retained).

## 4. Protocol (frozen)

Deterministic: fixed ascending key order per pass, no RNG. One pass =
teach every key of the train set once in ascending order, then probe.

- `train_to_criterion(set, valfn)`: repeat passes; after each pass probe
  every key of the set. Criterion = 100% correct on all set keys for 2
  consecutive passes. Max 50 passes (fail-safe; hitting it = arm FAIL).
  Returns passes used (TTC).
- Phase B uses FIXED passes, not to-criterion: under pressure the
  full-B criterion may be unreachable by construction, and demanding it
  would conflate "criterion unreachable" with the retention question.
  Fixed P = 6 B passes (1.5x NT1's TTC_B_seq = 4; generous: in NT1,
  contradicted keys completed revision by pass 3).
- Arms (each on a FRESH learner):
  - CONTROL-A (ML1): train SET_A/VA to criterion. Records TTC_A_ctrl,
    probe accuracy, nevict (predicted 0: 24 keys <= 30 slots).
  - CONTROL-B (ML1): train SET_B/VB to criterion. Records TTC_B_ctrl,
    probe accuracy, nevict (predicted 0: 24 keys <= 30 slots).
  - SEQ (ML1): train SET_A/VA to criterion (TTC_A_seq); probe SET_A
    (sanity 24/24); 6 fixed passes of SET_B/VB; probe SET_B (accB);
    RETEST: probe the 24 A keys, scoring partitions C/NC/U separately;
    count FORGET = keys answering neither the A-correct nor (for C) the
    B-correct value; record nevict, nentries, and the eviction histogram.
  - ABLATION (ML0): identical protocol on a fresh ML0 learner
    (TTC_A_abl, accB_abl, retest partitions, FORGET_abl, nevict_abl,
    nalias_abl, nentries_abl).

### What "correct" eviction looks like (frozen)

A correct generic eviction policy under this pressure: (i) evicts only
as forced -- 12 novel keys minus 6 free slots = exactly 6 evictions,
no churn (nevict == 6); (ii) contradicted keys still complete revision
(C_VB >= 5/6); (iii) nothing is forgotten that the table could have kept
(FORGET = 0). I.e., pressure costs exactly the 6 slots' worth of
entries, and the NT1 selective-retention pattern is otherwise preserved.

## 5. Assembly, build, run (frozen)

- Single source file `nt2_full.zag`: canonical helpers (z_alloc, get32,
  set32, o_app, o_i64, o_nl, o_flush; copied verbatim from the NT1
  template), learner fns, oracle fns, protocol fns, main. No other source.
- Build: `znc nt2_full.zag -o nt2_bin` under safebin-only PATH.
- Run `nt2_bin` 3 times; outputs `nt2_run1.txt`, `nt2_run2.txt`,
  `nt2_run3.txt`. Require byte-identical (cmp) and record sha256.
- Output lines (all numeric): per-arm TTC values, per-phase probe
  accuracies, retest partition scores (C_VB, NC_OK, U_OK, FORGET),
  eviction counts, the nonzero eviction-histogram bins, and computed
  K1..K5 verdict bits.
- Compiler-defect workarounds (mandatory, from AGENTS.md): no
  `as *i32`+slice construction (get32/set32 only); dynamic output only
  via the single-buffer cursor helpers + one `_zag_raw_syscall` write
  (never `_zag_print`); no `!(A && B)` in while conditions (De Morgan);
  if-nesting at most 3 deep with hoisted call results; no `[]u8 as *u8`
  casts (thread `_zag_malloc as *u8`).

## 6. Frozen predictions

Hand-derived by tracing the frozen rules (two independent traces;
mechanism, not just numbers):

- CONTROL-A: TTC_A_ctrl = 2, acc = 24/24, nevict = 0.
- CONTROL-B: TTC_B_ctrl = 2, pc = 1, acc = 24/24, nevict = 0.
- SEQ: TTC_A_seq = 2; phase-A probe 24/24; after 6 B passes,
  accB = 18/24 (C 0/6, NC 6/6, novel 12/12); nevict = 41, nentries = 30.
- SEQ retest: C_VB = 0/6, NC_OK = 6/6, U_OK = 12/12, FORGET = 6.
- SEQ eviction histogram (key=count, nonzero only): 100=6, 101=5,
  102=5, 103=5, 104=5, 105=5, 134=1, 135=1, 136=1, 137=1, 138=1, 139=5;
  all other keys 0.
- ABLATION (ML0): TTC_A_abl = 2; accB_abl = 24/24; nevict_abl = 0;
  nalias_abl = 12; nentries_abl = 24; retest C_VB = 6/6, NC_OK = 6/6,
  U_OK = 0/12, FORGET_abl = 12.

### Predicted mechanism (Q1/Q2/Q3)

The generic lowest-net eviction rule does NOT preserve selective
retention under pressure; it PREEMPTS revision. Mechanism, traced:

1. Contradicted C keys accumulate ref, depressing net to 1 (sup=2,
   ref=1), tying them for globally-lowest with just-inserted novel
   keys (sup=1, ref=0, net=1).
2. The tie-break (lowest slot index) then evicts the actively-revising
   C keys (slots 0..5) to make room for novel keys -- and, within each
   pass, each new novel key evicts the previously inserted one.
3. Evicted C keys are re-inserted FRESH (sup=1, ref=0) on the next pass,
   so ref never exceeds sup: revision never completes. The churn is a
   stable cycle (nevict grows 7/pass from pass 2 on), not a transient.
4. The evicted set is exactly the entries current experience is about
   (revising C keys, incoming novel keys); the untouched U keys
   (net=2, never reinforced during B) are never eviction candidates.
   Eviction cannibalizes the working set of ongoing learning while
   preserving the untouched past.

Predicted verdict: FAIL (K2 and K4 fail; K1, K3, K5 hold). This is a
boundary result, not a defect report: it maps the exact envelope in
which the NT1 principle holds, and names the interaction that breaks it.

## 7. Frozen kill bars

- K1 (learning intact under capacity; else VOID): TTC_A_ctrl in 1..50
  AND acc 24/24; TTC_B_ctrl in 1..50 AND acc 24/24; TTC_A_seq in 1..50
  AND accA 24/24. Else VOID (capacity itself broke learning; redesign,
  do not reinterpret).
- K2 (eviction minimal, no churn): nevict_seq == 6. (12 novel keys
  minus 6 free slots = forced evictions; anything more is churn.)
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

- K1..K5 all hold: **PASS** -- selective retention survives capacity
  pressure under the generic eviction rule; eviction is minimal and
  revision completes.
- K1 fails: **VOID** -- redesign.
- K1 holds, K5 fails: **INCONCLUSIVE** -- apparatus lacks
  discriminative power; PASS is forbidden.
- K2 or K4 fail (K1, K3, K5 hold): **FAIL** -- the retention principle
  does not survive capacity pressure. Report the failed bars with the
  mechanism: K2-fail = eviction churn (revision preempted, nevict grows
  per pass); K4-fail = contradicted keys never complete revision under
  pressure (C_VB collapse, FORGET > 0).

## 9. General-principle direction (NOT implemented; preregistered follow-up)

If NT2 PASSES: port the pressure-tested rule to the shared
continuing-learner substrate and scale the pressure (larger families,
tighter capacity ratios). If NT2 FAILS (predicted): the failure is
diagnostic, not a patch request. Do NOT patch the tie-break or add
protection. The preregistered next step is to test whether ANY generic
(non-protective) eviction policy preserves revision under pressure --
candidate hypotheses to preregister separately: (H1) evict by lowest
TOTAL evidence (sup+ref) rather than net; (H2) recency-weighted
eviction; (H3) revision that preserves accumulated evidence instead of
resetting to sup=1. Each must be preregistered with its own kill bars;
no policy may reference task identity or importance.

## 10. Honest boundaries (pre-declared)

- ML1/ML0 are MINIMAL SURROGATES for the principle under test
  (entry-local evidence revision vs addressing/eviction interactions),
  not TNN's production memory substrate. A result here characterizes
  the principle and the measurement apparatus, not TNN-as-built.
- Families are memorized key-value mappings, not induced rules; the
  experiment measures retention/revision/eviction dynamics, not rule
  learning (L1 memorization substrate; no L2/L3 claim).
- Single capacity point (CAP=30, ratio 36/30 = 1.2x over capacity);
  scaling the pressure ratio is out of scope.
- Single contradiction magnitude (one alternative value per C key);
  graded/partial contradiction is out of scope.
- The eviction histogram is measurement-only instrumentation; it does
  not influence any learner decision.

## 11. Amendment record (transparent; committed before implementation)

- A1 (2026-10-03): K5's nalias literal corrected 72 -> 12, and the
  Section 6 prediction likewise. The original 72 was a hand-trace
  arithmetic error in the prereg, not a rule: under the frozen Section
  2 rules, each B-novel key aliases its ML0 slot exactly ONCE (pass 1);
  from pass 2 on the novel key owns that slot, so nt_find hits and the
  update path runs instead of the alias path. Corroborating precedent:
  NT1's ML0 arm recorded nalias=12 under 4 B passes for the same
  reason. The bar's stated intent is unchanged (pure alias signature,
  distinct from ML1's eviction signature); the literal now matches the
  frozen rules. Original text preserved in git history (commit
  eb74184). No other prereg content altered.
