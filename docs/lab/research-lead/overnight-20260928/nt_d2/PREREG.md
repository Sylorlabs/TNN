# PREREG: NT-D2 -- Evict the Youngest (LIFO): a staleness-blind, contradiction-blind comparator

## 1. Question

The NT series has now produced four cleanly discriminated signatures from
one apparatus (ledger C407/C412/C416/C427):

- NT2 (C407 FAIL): lowest-net (sup-ref) eviction preempts revision.
  Contradicted keys accumulate ref, depressing net to the insertion
  baseline, and are evicted mid-revision. nevict=41, c_vb=0/6,
  forget=6 (contradicted keys).
- H1 (C412 FAIL): lowest-total (sup+ref) eviction protects keys DURING
  revision (H1's rationale: contested keys carry high total evidence)
  but fails AT revision: the frozen revision reset collapses the
  revised key to (sup=1, ref=0), total=1, the global minimum, and the
  slot-index tie-break sacrifices it. Revolving door concentrates the
  churn. nevict=40, c_vb=5/6, forget=1.
- H3 (C416 FAIL, null): evidence-preserving revision is dead code under
  lowest-net; the breaking reset is the EVICTION-reinsertion reset, not
  the revision reset.
- D1 (C427 FAIL, informative): preserving evidence across
  eviction/re-insertion (restore prior sup/ref/value) lets revision
  complete (c_vb 0/6 -> 6/6) and cuts evictions 41 -> 32 -- but
  forgetting RELOCATES to 6 untouched U keys (112..117). The frozen
  lowest-net comparator punishes staleness: U keys at frozen net=2
  become the global minimum once every taught key's net grows past 2.

D1's preregistered next hypothesis (REPORT Section "Recommended
follow-up"): an eviction comparator that does not punish
staleness/contradiction. This lane tests it.

D2 question: does D1's preserve-evidence PLUS a comparator that is
blind to staleness and blind to contradiction preserve the full NT1
selective-retention pattern under capacity pressure -- revision
completes, nothing needlessly forgotten, evictions minimal?

### 1.1 Why the comparator must use temporal metadata (necessity argument)

A pure (sup, ref) comparator CANNOT satisfy the three requirements
simultaneously. Proof sketch from the frozen battery:

1. "Low net because untouched" vs "reinforced novel" are
   entry-locally IDENTICAL: a U key (VA, sup=2, ref=0) and a novel key
   taught twice (VB, sup=2, ref=0) have the same counters. No function
   of (sup, ref) separates them. (This is D1's failure: lowest-net
   eventually ranks both at net=2 and the tie-break eats the U keys.)
2. "Revised" vs "new" are entry-locally IDENTICAL after the frozen
   revision reset: both are (value, sup=1, ref=0). No function of
   (sup, ref) separates them; the tie-break then decides, and every
   tie-break kills something (slot-index kills low-slot C keys -- H1;
   most-recent kills just-inserted C keys; least-recent kills stale U
   keys -- traced, see 1.2).
3. Therefore any comparator meeting "don't punish staleness, don't
   punish contradiction, evict the genuinely low-value" MUST consult a
   signal beyond (sup, ref). The minimal such signal is temporal:
   insertion age. A new entry is young BY DEFINITION; a contested
   entry and an untouched entry are both old (inserted before the
   current teaching episode). Age separates exactly the categories the
   counters conflate.

### 1.2 Rejected alternatives (traced pre-registration, not implemented)

- D1 + H1-total-evidence compound ("the obvious two-change
  hypothesis"): hand-traced under lowest-(sup+ref) with D1 restore.
  Fails directionally: the revised key collapses to total=1 = global
  minimum at the revise moment and is evicted (H1's failure mode
  persists -- restore cannot help because the checkpoint captures the
  POST-revise state); re-inserted C keys tie with novel keys at
  (VB,k,0) and churn against them; U keys are displaced once taught
  keys' totals exceed 2. Does not converge to revision-complete +
  forget-free. Rejected: it reintroduces an evidence-primary ranking,
  which Section 1.1 shows cannot work.
- Lowest-net/sup/total with a "don't evict ref>0" carve-out: that is a
  protection rule, barred by the series' no-protection governance (NT2
  PREREG Section 9: "Do NOT patch the tie-break or add protection").
  D2 protects contested keys WITHOUT a protection rule, via the
  generic age ordering (contested entries are old).
- FIFO (evict oldest): the other temporal comparator; it MAXIMALLY
  punishes staleness (U keys evicted first). It is the anti-D2 and is
  rejected by the task statement itself.

### 1.3 The D2 comparator: evict the youngest (LIFO)

Victim = the occupied slot with the greatest installation sequence
number (most recently installed). Rationale:

- Does NOT punish staleness: age is protective. Untouched entries are
  the OLDEST, hence the LAST evicted, never the first. Staleness can
  never make an entry the victim.
- Does NOT punish contested keys: a key under revision was installed
  before the contradiction began, so it is old; contradiction
  depresses net and raises total, but NEITHER affects age. H1's
  rationale (contested keys must not become evictable) is satisfied
  structurally rather than by evidence arithmetic, and the revision
  reset cannot expose the key (the reset does not touch age).
- DOES evict genuinely low-value entries: the youngest entries are
  the just-(re-)installed ones -- least opportunity to accumulate
  evidence, and in a continual-teaching regime they are exactly the
  entries currently being taught, so re-insertion cost is minimal
  (they return on the next teaching anyway). The criterion is
  "least-established claim on its slot," measured by tenure.

The comparator is generic and domain-neutral: it uses only insertion
order (standard cache-policy metadata, entry-local), no task identity,
no importance flags, no protection rules, no modes. It does not know
which keys are novel, contested, or untouched; the battery VERIFIES
that age aligns with the right victims.

## 2. Subject (frozen rules + the single D2 change)

D1's ML1/ML0, oracles, protocol, capacity, revision rule (INCLUDING
the reset), D1 restore rule, and every other rule are frozen verbatim.
Keys and values are bare integers (opaque identifiers); the learner
has no task semantics.

### 2.1 D2 rule (precise, frozen)

- Each slot gains a fifth field `ins` (i32): the installation
  sequence number. The arena holds an `ins_seq` counter (i32),
  zero-initialized with the learner.
- On EVERY installation of a key into a slot (fresh insert AND D1
  checkpoint-restore re-insert): `ins_seq++`, `slot.ins = ins_seq`.
  Revision in place does NOT touch `ins` (the entry is not
  re-installed). Eviction does not touch survivors' `ins`.
- Eviction rule (replaces D1 PREREG Section 2.2's lowest-net rule
  verbatim): if the table is full and the taught key is absent, evict
  the occupied slot with MAXIMUM `ins` (most recently installed).
  `ins` values are unique per installation, so no tie-break is needed
  or specified.
- The rule remains generic: it operates only on entry-local
  installation order; no task identity, no importance, no protection,
  no modes, no researcher-supplied "don't forget" logic.

Minimal-change commitment: the implementation is D1's
`nt_d1_full.zag` transcribed verbatim with exactly these changes:
slot stride 16 -> 20 bytes (new `ins` field), arena offsets shifted
accordingly, `ins_seq` counter added, `nt_evict_lowest` replaced by
`nt_evict_youngest` (max `ins`), `nt_insert` stamps `ins` on every
installation, K2 literal 36 -> 41 (Section 5), header comments. No
other source line changes in meaning. `diff` against D1 will be
verified.

### 2.2 Everything else frozen (D1 PREREG Section 2 verbatim, except 2.1)

- Slot table: (key, value, sup, ref, ins); CAP = 30. B has 24 keys,
  A-union-B has 36 distinct keys, 24 <= 30 < 36: a stable all-B
  solution exists; failure is attributable to the rules, not
  impossibility.
- D1 restore: on eviction, checkpoint (valid=1, value, sup, ref);
  on insertion of an absent key with a valid checkpoint, install the
  checkpointed (value, sup, ref), then run the frozen update step;
  else fresh (key, taught value, 1, 0). (The `ins` stamp is applied in
  both cases per 2.1.)
- `nt_learn` update: present and value matches -> sup++; present and
  value differs -> ref++, and if ref > sup REVISE to (key, new value,
  sup=1, ref=0). The revision RESET is untouched.
- `nt_predict`: slot holds key and sup > ref -> value; else -1.
- ML1: associative lookup (linear scan), install at first empty slot
  or the victim's slot. ML0: NT1's overlapping map verbatim
  (slot(key) = key-100 for key < 124 else key-116); aliased writes
  destroy; never fills (24 entries max), never evicts (comparator
  never fires for ML0).
- Measurement-only eviction histogram (40 bins, keys 100..139).

## 3. Task families (frozen numeric inventory; opaque identifiers)

Identical to NT1/NT2/D1, verbatim. Keys are integers 100..139.
Values are integers 200..263. No semantic labels anywhere.

- VA(k) = 200 + ((k*37 + 11) mod 64), for all k. (Oracle, family A.)
- SET_A: keys 100..123 (24 keys), values VA(k).
- SET_B: keys 100..111 (12 shared) + keys 128..139 (12 novel).
  VB(k) = VA(k) for k in 106..111 and 128..139; for contradicted keys
  k in 100..105: VB(k) = 200 + (((VA(k)-200)+32) mod 64), guaranteed
  different from VA(k).
- Retest partition of A's 24 keys: C (contradicted) 100..105, correct
  VB(k); NC (non-contradicted, agreed) 106..111, correct VA(k)=VB(k);
  U (untouched) 112..123, correct VA(k).

## 4. Protocol (frozen; D1 Section 4 verbatim)

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

### What "correct" looks like under D2 (frozen)

A correct outcome: (i) evictions at the D2 minimum (Section 5), no
A-key ever evicted; (ii) contradicted keys complete revision;
(iii) FORGET = 0: nothing is forgotten that the table could have kept.
I.e., D1+D2 preserve the NT1 selective-retention pattern under
pressure, with pressure costing only the forced churn among novel
keys.

## 5. Kill-bar K2: pigeonhole bound, forget regime stated, D2 minimum

D1 PREREG Section 5 derived nevict >= 36 UNDER THE FORGET = 0 REGIME
(U keys pinned: 12 U pin 12 slots; per pass >= 6 absent teachings;
6 passes -> >= 36). That derivation is adopted unchanged; it is a
LOWER bound, and K4 enforces FORGET = 0 independently.

D2's predicted count is 41, not 36, for a traced reason (Section 6):
the revolving door. Each pass 2..6, the re-inserted novel key 133
displaces the current newest entry (139), which must itself be
re-inserted -- one extra eviction per pass over the pigeonhole 36.
All 41 victims are novel keys (128..139); no A-key (100..123) is ever
evicted. The +5 is FORGET-FREE churn confined to keys re-taught every
pass.

Therefore the correct K2 bar, with the forget regime explicit, is:

- K2 (eviction minimal, FORGET = 0 regime): nevict_seq == 41.
  (36 = pigeonhole lower bound under FORGET = 0; +5 = traced
  revolving-door overhead, all victims novel keys, zero forgetting.
  Any excess over 41 is untraced churn; any shortfall with FORGET = 0
  would be a welcome surprise but is not predicted.)

## 6. Frozen predictions (hand-derived by tracing the frozen D2 rules)

Slot order after phase A: keys 100..123 in slots 0..23, each
(VA, sup=2, ref=0), ins 1..24. nevict=0.

- B pass 1: 100..105 contradicted -> (VA,2,1). 106..111 match ->
  sup=3. 128..133 fill free slots 24..29 (VB,1,0), ins 25..30.
  134..139: table full; victim = max ins -> 133 (ins 30), then the
  just-installed key each time (revolving door on slot 29); victims
  133,134,135,136,137,138, each checkpointed (VB,1,0). End: slot 29
  = 139 (VB,1,0, ins 36). nevict=6.
- B pass 2: 100..105 -> ref=2, (VA,2,2). 106..111 -> sup=4.
  128..132 hits -> sup=2. 133 absent -> restore (VB,1,0); victim =
  newest = 139 (ins 36); 133 at slot 29 (ins 37) -> match ->
  (VB,2,0). 134..139 absent -> restore; each evicts the current
  newest at slot 29 (victims 133,134,135,136,137,138); 139 ends at
  slot 29 (ins 43) -> (VB,2,0). 7 evictions. nevict=13.
- B pass 3: 100..105 -> ref=3 > sup=2 -> REVISE -> (VB,1,0) IN
  PLACE (ins 1..6 unchanged; the comparator never sees the reset).
  106..111 -> sup=5. 128..132 -> sup=3. 133 absent -> restore
  (VB,2,0); victim = 139 (newest); -> (VB,3,0). 134..139: revolving
  door on slot 29 (7 evictions). nevict=20. No C key, no U key, no
  NC key is ever a victim: all are older than every novel key.
- B pass 4: 100..105 match -> sup=2. Revolving door (7 evictions).
  nevict=27.
- B pass 5: 100..105 -> sup=3. 7 evictions. nevict=34.
- B pass 6: 100..105 -> sup=4. 7 evictions. nevict=41.
- End state: slots 0..5 = 100..105 (VB,4,0); 6..11 = 106..111
  (VA,8,0); 12..23 = 112..123 (VA,2,0), never evicted, never taught
  in B; 24..28 = 128..132 (VB,6,0); slot 29 = 139 (VB,6,0);
  133..138 absent (evicted this pass, re-taught next -- but there is
  no next pass).

Frozen numeric predictions:

- CONTROL-A: TTC_A_ctrl = 2, acc = 24/24, nevict = 0. (Comparator
  never fires; no eviction possible.)
- CONTROL-B: TTC_B_ctrl = 2, pc = 1, acc = 24/24, nevict = 0.
- SEQ: TTC_A_seq = 2; phase-A probe 24/24; after 6 B passes,
  accB = 18/24 (100..111 = 12/12, 128..132 = 5/5, 139 = 1/1,
  133..138 absent = 0/6); nevict = 41, nentries = 30.
- SEQ retest: C_VB = 6/6, NC_OK = 6/6, U_OK = 12/12, FORGET = 0.
- SEQ eviction histogram (key=count, nonzero only): 133=6, 134=6,
  135=6, 136=6, 137=6, 138=6, 139=5; all other keys 0 (in
  particular 100..123 = 0: NO A-key is ever evicted). Sum = 41.
- ABLATION (ML0): TTC_A_abl = 2; accB_abl = 24/24; nevict_abl = 0;
  nalias_abl = 12; nentries_abl = 24; retest C_VB = 6/6, NC_OK = 6/6,
  U_OK = 0/12, FORGET_abl = 12. (Comparator never fires for ML0;
  NT2/D1-identical.)

### Predicted mechanism (directional prediction: PASS)

D1's restore lets ref accumulate across eviction boundaries so
revision fires (pass 3); D2's LIFO comparator then protects the
revised entries STRUCTURALLY: the revised C keys are old (ins 1..6),
so they are never eviction candidates, and the revision reset is
invisible to the comparator (it does not touch `ins`). Untouched U keys
(ins 13..24, installed in phase A, never re-installed) are likewise
far older than any novel key and are never candidates -- staleness is
protective, never punished.
All churn concentrates on the novel keys 128..139, which are re-taught
every pass: evicting them is forget-free by construction. The NT1
selective-retention pattern (retain the uncontested, revise the
contradicted, forget nothing the table could keep) survives capacity
pressure with both fixes. Predicted signature discriminates D2 from
all predecessors: nevict=41 WITH forget=0 and c_vb=6/6 (NT2: 41 with
forget=6, c_vb=0/6; H1: 40, forget=1; D1: 32, forget=6 U-keys).

Predicted verdict: PASS (K1-K5 all hold). This would be the first PASS
in the NT series: the NT1 principle survives capacity pressure with
D1's preserve-evidence and D2's staleness-blind comparator combined.

## 7. Frozen kill bars (forget regime stated explicitly)

- K1 (learning intact under capacity; else VOID): TTC_A_ctrl in 1..50
  AND acc 24/24; TTC_B_ctrl in 1..50 AND acc 24/24; TTC_A_seq in 1..50
  AND accA 24/24. Else VOID (capacity itself broke learning; redesign,
  do not reinterpret).
- K2 (eviction minimal, no churn, FORGET = 0 regime): nevict_seq ==
  41. (Section 5: 36 = pigeonhole lower bound under FORGET = 0; +5 =
  traced revolving-door overhead among novel keys. K4 enforces the
  FORGET = 0 regime independently.)
- K3 (uncontested retention survives): SEQ retest NC_OK = 6/6 AND
  U_OK = 12/12.
- K4 (revision survives pressure, FORGET = 0 regime): SEQ retest
  C_VB >= 5/6 AND FORGET = 0 across all 24 A keys.
- K5 (discriminative validity): ML0 ABLATION shows the pure alias
  signature (U_OK_abl = 0/12 AND nevict_abl = 0 AND nalias_abl = 12)
  AND ML1's signature differs (nevict_seq != nevict_abl). If ML0's
  signature matched ML1's, the apparatus cannot distinguish fragility
  modes -> verdict INCONCLUSIVE, never PASS.

## 8. Verdict mapping (frozen)

- K1..K5 all hold: PASS -- D1+D2 preserve selective retention under
  capacity pressure: revision completes, evictions are minimal (41 =
  36 forced + 5 forget-free door overhead), nothing needlessly
  forgotten (FORGET = 0).
- K1 fails: VOID -- redesign.
- K1 holds, K5 fails: INCONCLUSIVE -- apparatus lacks discriminative
  power; PASS is forbidden.
- K2 fails (K1, K3, K4, K5 hold): FAIL -- churn beyond the traced
  minimum; D2 did not stabilize eviction as predicted.
- K3 or K4 fail (K1, K2, K5 hold): FAIL -- the retention pattern did
  not survive: K3-fail = uncontested keys lost under pressure
  (staleness still punished); K4-fail = contradicted keys never
  complete revision or keys forgotten.
- (Predicted: K1-K5 all hold -> PASS.)

## 9. Follow-up direction (NOT implemented; preregistered)

- If D2 PASSES: the NT1 principle survives capacity pressure with both
  fixes. Next: (a) port D1+D2 to the shared continuing-learner
  substrate; (b) scale the pressure ratio (36/30 = 1.2x -> higher)
  with the same bars; (c) test whether LIFO's protection generalizes
  when novel keys are NOT re-taught every pass (the "genuinely
  low-value" criterion's boundary).
- If D2 FAILS with the predicted-signature direction wrong (e.g. U
  keys evicted, or revision preempted): re-derive the mechanism from
  the binary before theorizing; the Section 6 trace may have an error.
  Do NOT patch the comparator or add protection in this lane; the
  FAIL is diagnostic.
- If D2 FAILS on K2 only (count != 41) with K3+K4 holding: the
  retention principle survived but the churn model was wrong; publish
  the actual histogram and re-derive.

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
- The eviction histogram, the checkpoint table, and the `ins`
  sequence: the histogram is measurement-only instrumentation and
  influences no learner decision. The checkpoint table and `ins` are
  learner state (own prior evidence / own installation order); they
  contain no oracle/task information. `ins` is written only by the
  learner's own installation events.
- LIFO is a generic cache-policy ordering, not a tuned choice for
  this battery: it was selected by the Section 1.1 necessity argument
  (temporal metadata is REQUIRED; FIFO is the anti-D2), not by fitting
  the battery. The frozen numeric predictions (Section 6) are what the
  battery checks.

## 11. Amendment record (transparent; committed before implementation)

(None.)
