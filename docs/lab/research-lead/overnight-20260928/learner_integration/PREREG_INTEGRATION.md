# PREREG: Continuing-Learner Integration (FROZEN)

Date: 2026-09-30 PDT. Worker: Continuing-Learner Integration Worker.
Owned path: docs/lab/research-lead/overnight-20260928/learner_integration/
Status: FROZEN. Committed alone before any implementation exists.

## 1. Goal

Compose the continuing learner (LEARNER-STRESS-PASS, daa9bf2fc) and the
DDES adaptive intervention planner (REVERT-ADAPT-PASS, 00e9a766e) into
ONE learner binary with ONE persistent state, which (a) runs the frozen
8-phase stress lifetime with no regression, and (b) encounters causal
ambiguity DURING the lifetime, resolves it by adaptive intervention,
persists the resolution as learner state, and reuses it after further
memory pressure. Adopt the recency-guarded earning discipline
(RECENCY-GUARD-CONTAINED, 68c5796d4) as the standing earning rule.

Neither part alone had this capability: the stress learner never
performed causal intervention; the DDES planners never ran inside a
continuing lifetime with memory pressure, corrections, and interference.

## 2. Composition design

### 2.1 One state, two regions

One `W:[]u8` allocation of 32768 bytes. The stress rule store uses
W[0..8192] exactly as in stress_learn.zag (store base 64, tick at W[0],
foundation-evict flag at W[8], collateral slots at W[2000..2048]).
The DDES hypothesis ledger is the slice W[16384..32768] (16384 bytes;
entries at e*1152 need 9216 bytes), passed as `ws` to the DDES
functions. No overlapping offsets. One allocation, one process, one
main(), no resets.

### 2.2 Function merge

stress_learn.zag (387 lines) and ddes_revert.zag (799 lines) are wired
together, not rebuilt. Overlapping helpers (z_alloc, emit, get32,
set32, i64s) are kept in one copy; they are byte-identical or
compatible. The name clash `query` is resolved by renaming the DDES
causal query to `dquery` (signature ws,e,v,t); the stress `query`
(subj,rel,expected) is unchanged. All DDES derivation functions
(compute_arrivals, frontier_surv, synthesize_plan_gen, predict_gen,
world_step_gen, feed_ep, adapt_ep, oneshot_ep, case loaders) are kept
verbatim. All stress store functions (learn, query, twohop, evict_c,
importance_c, found_probe, coll_record, coll_changes, emit_stage_hash)
are kept verbatim.

### 2.3 Ambiguity trigger

P9 loads the frozen M1 ambiguous case (e2: 3 hypotheses, true=h2) into
the ledger and calls feed_ep in ADAPT mode with the frozen passive
observation (v=1,t=2)->1. feed_ep emits AMBIGUOUS (3 survivors) and the
ADAPT round loop chains interventions conditioned on real outcomes,
exactly as in REVERT-ADAPT-PASS. The trigger is visible in the output:
AMBIGUOUS followed by ADAPT rounds followed by RESOLVED. No task label
reaches the learner; the case index is a harness loader, as in the
frozen DDES batteries.

### 2.4 Persistence of the resolution

After ADAPT resolves, main() writes three causal-fact entries to the
rule store and earns each immediately (query to bump importance above
1), because a full store cannibalizes unproven newcomers (each teaching
evicts the lowest-index importance-1 slot, which the new item then
becomes):
- learn(W,900,1,2): M1 winner is h2
- learn(W,901,1,2): M1 resolved in 2 rounds
- learn(W,902,1,0): M1 round 1 eliminated h0
Each followed by query(W,90x,1,expected) to earn importance 11.

### 2.5 Recency-guarded earning discipline

The inter-wave earning function `earn_guarded` queries surviving
rel=99 junk to importance 11 EXCEPT it skips the highest-subj survivor
(the most recent arrival; needs no door knowledge). This is the adopted
discipline from the closed retention lane. Its efficacy (9/10 sleeper
retention across 3 episodes vs 7/10 unguarded) was established there
(RECENCY-GUARD-CONTAINED) and is cited, not re-proven: a full store
cannot host multiple unproven sleepers (proven consequence of the
eviction rule), so the guard's mechanism-active check here is the EARN
log plus door absorption, per section 4, bar C4.

## 3. Phase plan

P1-P8: verbatim from stress_learn.zag main(). Emits "=== STRESS
COMPLETE ===" at the end of P8, exactly as the frozen battery.

P9 (causal ambiguity inside the lifetime):
- Emit "PHASE P9".
- Load M1 (load_e2), feed_ep ADAPT with passive (1,2)->1.
- Frozen expectation: status ACTIVE(1), winner h2 (index 2), rounds 2.
- Write and earn the three causal facts (900,901,902).
- Emit "P9_RESOLVED winner=2 rounds=2".
- emit_stage_hash(W,9).

P10 (pressure wave 3 + guarded earning + delayed probes):
- Emit "PHASE P10".
- Teach 20 junk (subj 500..519, rel 99, obj=subj). Evictions expected;
  door absorbs after the first.
- earn_guarded: earn all surviving rel=99 junk except the highest-subj
  survivor. Emit "EARN_SKIPPED <subj>" and "EARNED <n>".
- Frozen expectation: EARN_SKIPPED 519 (the last taught junk, highest
  subj, survives at the door).
- Delayed probes:
  - Causal: query(W,900,1,2), query(W,901,1,2), query(W,902,1,0).
    Expect 3/3 (P10_CAUSAL).
  - Foundation: found_probe(W,8,180). Expect 8/8 (P10_FOUNDATION).
  - Corrections: query(W,2,10,8), query(W,5,11,180). Expect 2/2
    (P10_CORR).
- Emit STATEHASH P10 with strictly increasing tick.
- Emit "=== INTEGRATION COMPLETE ===".

## 4. Frozen bars

### Regression (K2-a): P1-P8 byte-identical
The output from "=== STRESS" through "=== STRESS COMPLETE ===" is
byte-identical to the committed STRESS_RAW_OUTPUT.txt at daa9bf2fc,
verified by cmp. This entails K-S1 (P1_RECALL 8/8), K-S2 (P4_CORR 5/5,
5/5; P4_COLL 0/12), K-S3 (P5_CORR 4/4; P5_RECALL 8/8), K-S4 (P6_TWOHOP
5/5; P8_RECALL 8/8; P8_CORR 2/2; FOUND_EVICT 0), and P1-P8 STATEHASH
ticks 16,64,108,153,201,211,231,241.

### New capability (K2-b)
- C1: P9_RESOLVED winner=2 rounds=2. The ADAPT planner resolves the
  M1 ambiguity inside the continuing lifetime (status ACTIVE, winner
  h2, 2 rounds, matching the frozen REVERT-ADAPT-PASS expectations
  for e2/mode=2).
- C2: P10_CAUSAL 3/3. The intervention resolution, written as learner
  state in P9, is retrieved correctly after P10's 20-item pressure
  wave. Delayed reuse of causal knowledge through pressure.
- C3: P10_FOUNDATION 8/8 and P10_CORR 2/2. The causal episode and
  third pressure wave cause no regression to foundation or corrections.
- C4: EARN_SKIPPED 519. The recency guard is active: the highest-subj
  survivor is skipped by earn_guarded (emitted value must equal 519).
  The guard's efficacy is cited from the closed lane, not re-proven.

### Determinism (K3)
3/3 byte-identical runs (sha256 recorded), exit 0, zero stderr. Pure
Zag at every step: pinned znc build, shell/grep/awk/cmp/sha256sum
analysis only. No em or en dashes (shell-only check_no_dash.sh).
STATEHASH P1-P10 ticks strictly increasing.

## 5. Kill bars

K1: this prereg strictly precedes implementation (merge-base verified);
  no implementation file exists in the owned path at prereg commit time.
K2: (a) P1-P8 output byte-identical to the committed baseline via cmp;
  (b) C1 winner=2 rounds=2; C2 3/3; C3 8/8 and 2/2; C4 EARN_SKIPPED 519.
K3: pure Zag, zero Python, 3/3 byte-identical, dash-clean, one learner,
  one state, no resets, no task labels.

## 6. Honest scope

Bounded L2. The candidate graphs are researcher-supplied (frozen M1
case); the learner authors the chaining, the conditioned targets, and
the persistence of the outcome, but not the hypothesis space. The "one
continuing learner" goal is approached, not claimed: vocabulary growth,
OpScope operators, and L3B program growth are not yet integrated. The
C1 law-revert fix is not in this composition (STATIC pathology
demonstrated separately). No L3 claim. No SURVIVES claim (pipeline
steps 4-11 not run on the composition).
