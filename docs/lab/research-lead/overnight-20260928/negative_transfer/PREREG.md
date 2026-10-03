# PREREG: NEG-TRANSFER-1 (NT1) -- Selective Retention Under Sequential Contradictory Training

## 1. Question

When a continuing learner masters task family A and then learns a related
but partially contradictory task family B, does it show SELECTIVE retention
(keep what B does not contradict, revise exactly what B contradicts) or
catastrophic forgetting (B-learning corrupts unrelated A knowledge)? And
does prior A knowledge measurably interfere with learning B (forward
negative transfer), and is that interference bounded?

This tests whether a generic error-driven, evidence-weighted learner memory
is robust or fragile under sequential training. Retention must EMERGE from
the update rule: no protection flags, no task labels, no freeze commands,
no researcher-supplied "don't forget" mechanism anywhere in the learner.

## 2. Subject architectures (frozen rules)

Two learner variants share EVERYTHING except the address map. Both are
domain-neutral: keys and values are bare integers; the learner has no task
semantics.

### 2.1 Shared memory model

- Learner state: a slot table. Each slot holds (key, value, sup, ref):
  sup = support evidence count, ref = refutation evidence count.
- Capacity: 48 slots. If full, evict the slot with globally lowest
  (sup - ref); ties resolve to the lowest slot index. (Predicted: eviction
  count = 0 in all arms; total distinct keys ever stored = 36 < 48.)
- `nt_learn(key, value)`:
  1. Find the slot holding `key`. If absent and table full, evict per rule
     above; then create slot (key, value, sup=1, ref=0).
  2. If present and value equals stored value: sup++.
  3. If present and value differs (contradiction): ref++; if ref > sup,
     REVISE the slot to (key, new value, sup=1, ref=0); else keep old value.
- `nt_predict(key)`: if a slot holds `key` and sup > ref, return its value;
  else return -1 (unknown).
- The update rule is symmetric and entry-local: teaching key k never
  touches any other key's slot. No protection, no task identity, no modes.

### 2.2 ML1 (treatment): dedicated addressing

slot(key) = key - 100. All 36 distinct keys used in the experiment occupy
distinct slots (100..139 -> slots 0..39). No aliasing possible.

### 2.3 ML0 (negative control): overlapping address map

slot(key) = key - 100 for key < 124, else key - 116. The 12 B-novel keys
(128..139) alias onto slots 12..23, i.e. onto the slots of A's U keys
(112..123). A later write to an aliased slot DESTROYS the earlier entry.
Update/read rules are byte-identical to ML1; only the address map differs.
This is a legitimate alternative architecture class (fixed overlapping
storage, the localist-vs-distributed crux), not sabotage: it learns each
family in isolation (no within-family aliasing) but is predicted to forget
aliased A knowledge under B training.

### 2.4 `arm` selector

The driver selects ML1 vs ML0 with an integer `arm` parameter in the
HARNESS (experimental condition selector, 0 = ML1, 1 = ML0). This is not a
cognitive mode: the learner itself has no modes, no task routing, no
conditional behavior on task identity.

## 3. Task families (frozen numeric inventory; opaque identifiers)

Keys are integers 100..139. Values are integers 200..263. No semantic
labels exist anywhere in code or output; sets are defined by numeric
bounds only.

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
- Interference is plausible: B contradicts A on 6 shared keys and
  introduces 12 novel keys competing for the same memory.

## 4. Protocol (frozen)

Deterministic: fixed ascending key order per pass, no RNG. One pass =
teach every key of the train set once in ascending order, then probe.

- `train_to_criterion(set, valfn)`: repeat passes; after each pass probe
  every key of the set. Criterion = 100% correct on all set keys for 2
  consecutive passes. Max 50 passes (fail-safe; hitting it = arm FAIL).
  Returns passes used (TTC).
- Arms (each on a FRESH learner):
  - CONTROL-A (ML1): train SET_A/VA. Records TTC_A_ctrl and proves A
    learnable in isolation.
  - CONTROL-B (ML1): train SET_B/VB. Records TTC_B_ctrl and proves B
    learnable in isolation.
  - SEQ (ML1): train SET_A/VA (TTC_A_seq); probe SET_A (sanity 24/24);
    train SET_B/VB (TTC_B_seq; also record passes until the 6 C keys are
    probe-correct, P_C_seq); probe SET_B (sanity 24/24); RETEST: probe
    the 24 A keys, scoring partitions C/NC/U separately; count FORGET =
    keys answering neither the A-correct nor (for C) the B-correct value.
  - ABLATION (ML0): identical SEQ protocol on a fresh ML0 learner
    (TTC_A_abl, TTC_B_abl, retest partitions, FORGET_abl).
- Forward negative transfer quantity: D = P_C_seq - P_C_ctrl, where
  P_C_ctrl = passes until the 6 C keys probe-correct in CONTROL-B
  (predicted 1: unknown -> created -> correct after pass 1).

## 5. Assembly, build, run (frozen)

- Single source file `nt_full.zag`: canonical helpers (z_alloc, get32,
  set32, o_app, o_i64, o_nl, o_flush; copied verbatim from the frozen
  domain_blindness template), learner fns, oracle fns, protocol fns,
  main. No other source.
- Build: `znc nt_full.zag -o nt_bin` under safebin-only PATH.
- Run `nt_bin` 3 times; outputs `nt_run1.txt`, `nt_run2.txt`,
  `nt_run3.txt`. Require byte-identical (cmp) and record sha256.
- Output lines (all numeric): per-arm TTC values, per-phase probe
  accuracies, retest partition scores (C_VB, NC_OK, U_OK, FORGET),
  eviction counts, and computed K1..K5 verdict bits.
- Compiler-defect workarounds (mandatory, from AGENTS.md): no
  `as *i32`+slice construction (get32/set32 only); dynamic output only
  via the single-buffer cursor helpers + one `_zag_raw_syscall` write
  (never `_zag_print`); no `!(A && B)` in while conditions (De Morgan);
  if-nesting at most 3 deep with hoisted call results; no `[]u8 as *u8`
  casts (thread `_zag_malloc as *u8`).

## 6. Frozen predictions

- ML1 CONTROL-A: TTC_A_ctrl = 2 (pass 1 creates, pass 2 confirms).
- ML1 CONTROL-B: TTC_B_ctrl = 2.
- ML1 SEQ: TTC_A_seq = 2; phase-A probe 24/24; TTC_B_seq = 4
  (C keys: ref=1,2 keep VA on passes 1-2; ref=3 > sup=2 revises to VB
  on pass 3; pass 4 confirms); P_C_seq = 3; phase-B probe 24/24.
- ML1 retest: C_VB = 6/6 (revised), NC_OK = 6/6, U_OK = 12/12,
  FORGET = 0. Evictions = 0.
- Forward transfer: D = 3 - 1 = 2 passes of measurable A-interference on
  contradicted keys, then resolved by evidence. Bounded, finite.
- ML0 ABLATION: TTC_A_abl = 2; TTC_B_abl = 4 (B probe covers only B
  keys, all present); retest: C_VB = 6/6, NC_OK = 6/6, U_OK = 0/12
  (novel keys 128..139 destroyed U entries via aliasing), FORGET_abl
  >= 12 (aliased U keys answer novel-key values).

## 7. Frozen kill bars

- K1 (isolation learnability): TTC_A_ctrl <= 50 AND TTC_B_ctrl <= 50
  with 100% final probe accuracy. Else VOID (families not learnable;
  redesign, do not reinterpret).
- K2 (no wholesale amnesia; retention where B does not contradict):
  ML1 SEQ retest NC_OK = 6/6 AND U_OK = 12/12.
- K3 (selective revision, not erasure): ML1 SEQ retest C_VB >= 5/6 AND
  FORGET = 0 across all 24 A keys.
- K4 (forward negative transfer bounded): D = P_C_seq - P_C_ctrl <= 6.
  (Measures A->B interference; bar requires it finite and small, not zero:
  zero would mean prior knowledge exerted no measurable pull.)
- K5 (discriminative validity): ML0 ABLATION fails K2 or K3
  (predicted: U_OK = 0/12, fails K2). If ML0 passes K2 AND K3, the
  apparatus cannot detect fragility -> verdict INCONCLUSIVE, never PASS.

## 8. Verdict mapping (frozen)

- ML1 passes K1,K2,K3,K4 AND K5 holds (ML0 fails K2 or K3):
  **PASS** -- selective retention emerges from entry-local
  evidence-weighted revision with no protection mechanism; overlapping
  addressing is identified as the fragility source.
- ML1 fails K2 or K3: **FAIL** -- B-learning corrupts non-contradicted A
  knowledge; the memory is fragile. Report which partition degraded.
- ML1 fails K4: **FAIL** -- prior knowledge interference is unbounded
  under the evidence rule (plasticity failure).
- K1 fails: **VOID** -- redesign task families.
- K5 fails (ML0 passes K2 and K3): **INCONCLUSIVE** -- apparatus lacks
  discriminative power; PASS is forbidden.

## 9. General-principle direction (NOT implemented; preregistered follow-up)

If NT1 PASSES: port the winning rule (entry-local evidence revision +
dedicated addressing) to the shared continuing-learner substrate and rerun
the A/B/A protocol there; test whether selective retention survives
capacity pressure (eviction active) and rule-structured (non-memorized)
families. If NT1 FAILS: trace which partition degraded and test whether
any generic (non-protective) update rule achieves K2+K3.

## 10. Honest boundaries (pre-declared)

- ML1/ML0 are MINIMAL SURROGATES for the principle under test
  (entry-local evidence revision vs overlapping addressing), not TNN's
  production memory substrate. A PASS here establishes the principle and
  the measurement apparatus, not that TNN-as-built is robust.
- Families are memorized key-value mappings, not induced rules; the
  experiment measures retention/revision dynamics, not rule learning
  (L1 memorization substrate; no L2/L3 claim).
- Single contradiction magnitude (one alternative value per C key);
  graded/partial contradiction is out of scope.
- No capacity pressure in this battery (eviction predicted 0);
  pressure-driven forgetting is a separate preregistered follow-up.
