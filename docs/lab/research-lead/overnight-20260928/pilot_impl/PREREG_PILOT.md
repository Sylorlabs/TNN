# PREREG: H-NEW-3 Continuing-Learner Integration Pilot (Implementation)

Status: PREREG. Frozen before any pilot implementation. No code written.
Design: `d83d53075` (HNEWP3_PILOT_DESIGN.md, DESIGN-COMPLETE).
Plan: `92db50b77` (PILOT_IMPL_PLAN.md, PLANNED).
Date: 2026-09-30 UTC.
Worker: H-NEW-3 Pilot Implementer.

This prereg freezes the eight sections required by the plan (K3), the
retention floors (design section 4), the Arm B control (design section 5),
and the falsifiers (design section 6), transferred verbatim or
strengthened. No section may be altered after results are seen; any
correction requires a transparent amendment committed before the
affected run.

## 1. Frozen workloads (seeds and exact shapes)

All workloads are fixed integer tables compiled into the pilot binary.
There is no RNG anywhere in the pilot; determinism is structural, not
seeded. The word "seed" below therefore means the frozen table, not an
RNG seed.

### E1 vocabulary (DEVANG lineage)

- 6 features, ids 1..6. 12 words, ids 0..11. word w maps to feature
  (w mod 6) + 1. Synonym pairs: (0,6), (1,7), ..., (5,11).
- Word id 12 is the NOT marker (compositional operator, fixed
  researcher-defined semantics, disclosed in section 6: meaning of
  (NOT, w) is the complement mask ALL ^ (1 << (feat(w)-1)), ALL = 63).
- Teach: 48 episodes. Episode e presents pair (w_e, f_e) with
  w_e = e mod 12, f_e = (w_e mod 6) + 1. Episodes 0..47 cover each word
  4 times. Additionally, episodes 48..63 present (NOT, w) for
  w in {0,1,2,3} (4 compositions, each repeated 4 times = 16 episodes).
  Total E1 teach episodes: 64.
- Lexicon update rule (frozen): lex[w] = f, str[w] += 1 on each
  presentation. not_seen[w] = 1 when (NOT, w) presented.
- Probe P1 (16 items, frozen order):
  items 0..11: word w -> expected feature (w mod 6)+1.
  items 12,13: (NOT, 0) -> 63 ^ (1 << (feat(0)-1)); (NOT, 1) -> similar.
  items 14,15: (NOT, 4), (NOT, 5) -- novel negations, never taught.
- Scoring: item correct iff learner output equals expected exactly.
- White-box check W1: lex[w] == (w mod 6)+1 and str[w] > 0 for all
  w in 0..11.

### E2 concept learning (P7/CL2 lineage)

- 4 domains d = 0..3. 8 items per domain, item ids 0..7.
  True class: c(d, i) = d mod 2, except domain 3 item 7 (the noisy
  exception): c(3,7) = 1 - (3 mod 2) = 0.
- Learner (frozen): per domain, count class frequencies over the 8
  taught items; default[d] = majority class; exc[d] = list of item ids
  disagreeing with default[d]. Schema discovered iff all 4 defaults
  set. Accuracy ledger: per-domain correct/total over teach items.
- Retirement trigger (CL2 shape): if a domain's teach accuracy <
  6/8, its schema is retired (live[d] = 0). Frozen workload has all
  domains at >= 7/8, so no retirement fires in the pilot; the trigger
  is implemented and reported (retire_events == 0 expected).
- Probe P2: (a) schema discovered (all defaults set); (b) held-out:
  4 items (d, 8) for d = 0..3, predict via default[d] (exception check
  against exc[d]); accuracy >= 3/4; (c) transfer domain d = 4
  (8 items, classes = 4 mod 2 = 0 with item 3 as exception = 1):
  fresh_writes = 8 (store every item), apply_writes = 1 + |exc[4]|
  (store default + exceptions); floor apply_writes < fresh_writes.
- Delayed probe P2d: predict all 8 trained items of domain 0 via
  schema; floor 8/8 correct and live[0..3] all 1.

### E3 procedure invention (form-inventor lineage, BASELINE mechanism)

- E3 mechanism frozen (plan K2 decision rule applied): BASELINE
  form-inventor. OP-RECRUIT v2 has not landed in ancestry and H-NEW-1
  Phase A has not started; the recruited-operator variant is the named
  follow-up wave (section 8), not a mid-wave substitution.
- Baseline mechanism (generic, no hardcoded threshold): train set of
  12 points, x = 0,2,4,...,22, class = 1 iff x < 13 (T = 13, unknown
  to the learner; the learner never sees the constant 13).
  1. Baseline prediction: majority class of train (0). Compute
     residuals (misclassified points).
  2. Candidate thresholds: sort train by x; for each adjacent pair
     with different classes, candidate t = (x_a + x_b) / 2.
  3. For each candidate t: form IF(x < t, c_lo, c_hi) with c_lo =
     majority class of points with x < t, c_hi = majority of x >= t.
     Score = correct count on train. Pick max score; tie-break
     smallest t.
  4. Adopt iff score == 12/12 (exact). Promote: write node to form
     pool with promoted = 1, form_kind = IF_LT, param = t.
  5. Verification halving (R6): split train into even/odd index
     halves; form must score 6/6 on each.
- Probe P3: (a) train fit 12/12; (b) form pool non-empty, promoted
  flag set, form_kind == IF_LT logged; (c) halving passes on both
  halves.
- The invented form (kind IF_LT, param t = 13) persists in the form
  node pool for E5. The E5 harness may mask the pool (condition F);
  the learner in condition R retrieves kind + param from the pool.

### E4 conflicting evidence (verification lineage)

- Fact store: entries (key, value, source, suspect). Sources:
  SRC_LEARNED = 1, SRC_ORACLE = 2.
- Setup: key K_DOM2 (id 200) holds value 0 (E2 domain-2 default,
  source SRC_LEARNED). In Arm B mode 4, the harness teaches this one
  fact directly (prerequisite setup, disclosed; E4 probe only).
- Lie episode: harness calls observe(CH_FACT, K_DOM2, 1, SRC_ORACLE).
- Frozen learner protocol:
  1. On observe with SRC_ORACLE where stored source is SRC_LEARNED
     and value differs: set contradiction flag for K_DOM2 within
     the same episode (flag_latency == 0 required, floor <= 1).
     Set suspect = 1. Do NOT overwrite the stored value yet.
  2. Emit hedged reply (log line HEDGE) and issue exactly one
     re-observation request: reobs_requests == 1, naming K_DOM2.
  3. Harness answers the single re-observation with the true value
     (0, SRC_ORACLE). Learner: store value 0, source SRC_ORACLE,
     clear suspect to 0, log RESTORED.
- Probe P4: (a) flag_latency <= 1; (b) exactly one HEDGE line and
  reobs_requests == 1 (not 0, not >= 2); (c) final value == 0 and
  suspect == 0.
- Interference probe P4x: re-run P1 (16 items) and the P2 gate
  (schema live[0..3] all 1 and query default[2] == 0). Floor: P1 score
  equals the E1 immediate P1 score exactly; P2 gate passes.

### E5 delayed reuse probe (Q4 C0-D lineage, system level)

- New task, changed surface, same topology: 12 points,
  x = 100,102,...,122, class = 1 iff x < 115 (T' = 115, unknown).
- Condition R (reuse): harness unmasks the form pool. Learner
  retrieves (form_kind, param) = (IF_LT, 13). Refit by bisection on
  the sorted E5 x-values using the retrieved kind: probe the middle
  x, observe class, narrow the flip interval; then verify neighbors.
  Count every (x, class) sample consumed as one intervention.
  Expected: <= 6 interventions to exact fit on all 12 E5 points.
- Condition F (fresh): harness masks the form pool (flag
  form_masked = 1, disclosed). Learner runs the full E3 pipeline
  (steps 1..5) on E5 points, consuming all 12 as interventions.
- Probe P5: reuse_interventions < fresh_interventions (strict) AND
  reuse condition reaches 12/12 on the E5 train points.
- In Arm B mode 5, the harness runs E3 invention first as
  prerequisite setup (disclosed), then E5; only E5 numbers are
  reported for that mode.

## 2. E3 mechanism freeze

Frozen: BASELINE form-inventor (section 1, E3). Citations: L3 bridge
`ebdc4fd3e` (BRIDGE-TESTED) is the lineage mechanism; the pilot uses
a compact re-implementation of the same generic principle
(residual-driven candidate thresholds, greedy gain, promotion,
halving) specialized to the single-threshold family, disclosed in
section 6 as a scope limitation. The recruited-operator variant
(H-NEW-1 Phase A) is the named follow-up wave (section 8).

## 3. Retention floors (frozen, unalterable after results)

Immediate (Arm A, right after each experience):
- F-E1: P1 >= 13/16. White-box W1 must also hold.
- F-E2a: schema discovered (4/4 defaults set). F-E2b: held-out >= 3/4.
  F-E2c: apply_writes < fresh_writes (strict).
- F-E3a: train fit 12/12. F-E3b: form pool has promoted IF_LT node.
  F-E3c: halving 6/6 on both halves.
- F-E4a: flag_latency <= 1. F-E4b: exactly one HEDGE and
  reobs_requests == 1. F-E4c: value == 0 and suspect == 0.
  F-E4x: P1 score == E1 immediate P1 score; P2 gate passes.

Delayed (Arm A, end of pilot):
- F-D1: P1d >= 11/16 (same 16 items as P1).
- F-D2: domain-0 instances 8/8 correct; live[0..3] all 1.
- F-D4: query K_DOM2 == 0.
- F-D5: reuse_interventions < fresh_interventions (strict);
  reuse fit 12/12.

Relative (Arm A delayed vs Arm B immediate):
- F-REL: for each delayed probe with an Arm B immediate counterpart
  (P1d vs P1, P2d vs P2b, F-D4 vs P4c-value): Arm A score >=
  Arm B score - margin, margins frozen: P1: 1 item; P2b: 0 items
  (must equal); P4c: must equal. F-D5 has no Arm B counterpart
  (absolute floor only).

Capacity:
- F-CAP: STATE_E5 <= 4194304 bytes (4 MB); no learn dropped for
  capacity in any experience (drop_count == 0).

## 4. Arm B control

Five binaries from the same `pilot.zag` source with MODE = 1..5
(build-time constant injection, documented in BUILD.sh):
- Mode 1: E1 teach + P1 + W1. Reports P1 score.
- Mode 2: E2 learn + P2 (a,b,c). Reports schema, held-out, writes.
- Mode 3: E3 invent + P3 (a,b,c). Reports fit, form, halving.
- Mode 4: prerequisite (teach K_DOM2 = 0 as SRC_LEARNED) + E4 + P4
  + P4x-with-E1E2-prereq: P4x in mode 4 re-runs a taught P1-equivalent
  (the mode teaches the 12 E1 pairs as prerequisite too, disclosed)
  and the P2 gate on a taught E2 domain-2 default (prerequisite).
  Reports P4a/b/c and P4x.
- Mode 5: E3 invention (prerequisite setup) + E5 (R and F) + P5.
  Reports reuse/fresh interventions and fits.
- Mode 0 (Arm A): E1, E2, E3, E4, E5 in fixed order, one process, no
  resets, no recompilation; immediate probes after each experience;
  delayed battery (P1d, P2d, F-D4 query, P5 already run in E5) at end;
  canary audit.
- Validity: Arm B must hold every immediate floor it measures; else
  that experience's comparison is VOID (disclosed), not passed.
- Determinism: 3/3 byte-identical runs per mode (md5 of stdout).

## 5. Falsifiers (transferred verbatim from design)

- F-INTERFERE: any F-D* or F-REL breached in Arm A while Arm B holds
  the corresponding immediate floor.
- F-CORRUPT: end-of-pilot canary audit fails (any region canary
  altered by a later experience).
- F-REUSE-FAIL: F-D5 breached.
- F-FLOOR: any immediate F-E* breached in Arm A (pilot fails at that
  experience; later experiences still run; report states the break).
- F-LABEL: audit finds cognition received a task label (anything
  beyond D1 channel tags or a reset signal). The episode counter is
  global; subsystems must never branch on it (audit by code inspection
  of the committed source: no reads of g_episode in subsystem logic).
- F-NONDET: any mode not 3/3 byte-identical.
- F-PYTHON: any Python invocation at any stage. Voids the wave.

## 6. Disclosures (D1, partitioning, scope limits)

- D1: observations enter through dispatch_observe(ch, ...)/query with
  ch in {CH_VOCAB=1, CH_CONCEPT=2, CH_FORM=3, CH_FACT=4}. The tag
  routes to the subsystem (sensory routing); no task name, episode
  index, or reset signal reaches cognition. Disclosed as weaker than
  an undifferentiated stream (design 2.2, 9.3).
- Partitioned regions: lexicon, schema, form pool, fact store, and
  reuse scratch are disjoint arrays in one workspace. The pilot
  tests non-interference and retention, explicitly not shared
  representation (design 9.2).
- E1 NOT semantics are a fixed researcher-defined complement rule;
  the pilot does not claim operator invention in E1.
- E3 baseline is specialized to the single-threshold family; the
  candidate generator enumerates adjacent-class-change midpoints.
  Generic within that family (T never supplied); not a general
  form inventor (the L3 bridge is the fuller mechanism).
- E5 reuse retrieves the invented form's kind and refits its
  parameter by bisection; the bisection procedure is
  researcher-authored. What is tested is whether retrieved
  persistent structure reduces later cost (system-level C0-D), not
  invention of the refit procedure.
- E4's oracle and re-observation answers come from the harness; the
  protocol under test is the learner's revision machinery.

## 7. Kill bars (implementation wave)

- K1: this prereg committed strictly before any pilot implementation
  file. (Self-check at report time.)
- K2: Mode 0 runs E1..E5 in one process, no resets, no recompilation
  between experiences, D1 discipline held (F-LABEL silent).
- K3: all floors in section 3 hold (immediate, delayed, relative,
  capacity).
- K4: pure Zag at every stage (compile, run, verify, byte checks via
  shell only); 3/3 byte-identical per mode; zero em-dash bytes;
  canaries intact (F-CORRUPT silent).
- K5: Arm B modes 1..5 run and compared per section 4.

Builder verdict: PILOT-PASS (K1..K5 hold, no falsifier fired) or
PILOT-FAIL (naming the fired falsifier and breached floor). Per-floor
results reported even on pass.

## 8. Upgrade path (named follow-ups, each its own prereg)

1. Recruited-operator E3: re-run pilot with E3 = H-NEW-1 Phase A
   mechanism once OP-RECRUIT v2 lands and Phase A passes gates.
2. Second order: E4 before E2 (revision-before-learning).
3. Scale-up battery (design section 8): causal episode, S9/S10
   memory pressure, distractor interference, E1-targeted
   corrections, larger scale.

## 9. Prereg self-check

- [x] 8 plan sections present (1..8 above).
- [x] Floors frozen with values (section 3).
- [x] Arm B defined with validity conditions (section 4).
- [x] Falsifiers transferred verbatim (section 5).
- [x] No implementation exists yet (this file is the first commit
  under pilot_impl/).
- [x] Zero em-dash bytes (to be shell-verified before commit).
- [x] No Python at any stage of prereg preparation.

Builder label: PREREG-COMPLETE (pending commit).
