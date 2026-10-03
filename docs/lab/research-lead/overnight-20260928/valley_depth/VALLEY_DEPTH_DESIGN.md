# H-NEW-6 DESIGN: Valley-Depth Characterization Battery

Date: 2026-09-30.
Status: DESIGN ONLY. No implementation. No code written. No valleys constructed.
Authority: H-NEW-6 from FRONTIER_W2 (`1d72eac51`); treadmill watch from the same wave.
Parent context: discovery battery prereg `425f7276d`; frozen GENEXEC2 VM `8d5f58b89`.

## 1. Background and motivation

Hypotheses A (`21d838921`) and C1 (`aae06bac6`) were both falsified on the same
defect: greedy single-operation repair cannot traverse temporarily worse
intermediate states. From the C2 design (`e658766bd`, section 2): building
`[IN0, PUSH 2, MUL, PUSH 1, ADD]` for T0 requires the two-step dependency
PUSH 2 then MUL; no single op appended to any prefix both fixes the current
failing episode and preserves passing episodes along the true path. C1
additionally degenerated into splitting and memorization (T3: 24 splits,
133-op memorization program).

Three non-myopic successors exist:

- B (fragment induction): `B-TESTED`, solved T0-T5 with carried library state
  (`hyp_b/RESULT_HYPB.md`). Mechanism: base route search, kink/probe assembly,
  fragment induction with generality gating, library reuse via CALL.
- D (MAP-Elites / novelty): `D-TESTED`, solved T0, T1, T2; failed T3, T4, T5
  (`hyp_d/HYPD_RESULT.md`). Mechanism: behavior-archive retention of elites,
  single-op mutation. Control validity: VALID.
- C2 (lookahead plus backtracking): design `e658766bd`; implementation in
  progress (`hyp_c2_impl/`). Mechanism: lookahead L=3, net-progress criterion
  (strict pass-count increase), chronological backtracking BMAX=6, splits.

The main battery (T0-T6) measures task solving. It does not isolate the
valley-crossing capability itself: a mechanism can solve a task by avoiding
valleys (C1 on T3 via 24 splits) rather than crossing them. H-NEW-6 isolates
the capability directly: construct valleys of parameterized depth 1..k on the
frozen VM, run B, D, C2 on each, and record the maximum crossable depth per
mechanism against its budget. Output is a tradeoff surface, not a winner.

The treadmill watch (`1d72eac51`, section 8) governs this battery: if all three
mechanisms plateau at budget-shaped depths, stop the lineage and open the
architecture review the standing rules require ("is the current representation
itself wrong?"). This design makes that watch operational: section 9 defines
exactly what counts as budget-shaped, and section 10 defines the trigger.

## 2. Core definitions

All definitions are relative to the frozen VM (`8d5f58b89`) and its frozen op
set: PUSH(c) for c in -9..9, IN0, IN1, ADD, SUB, MUL, DIV, MOD, NEG, DUP, DROP,
SWAP, OVER, LT, EQ, GT, JZ(k), JNZ(k), JMP(k), CALL(f), RET. Program result is
top of stack. DIV by zero yields 0, else truncated a/b. MOD by zero yields 0,
else nonnegative mod_nonneg(a,b). Underflowed stack ops are no-ops.

- Episode set E: a fixed ordered list of (input, target) pairs. Score(P) is the
  count of episodes where program P's top-of-stack equals the target exactly.
- Decoy program P0: a fixed starting program supplied by the harness, with
  score s0 = Score(P0). The mechanism's task is to find a program scoring
  strictly above s0; SOLVED means scoring |E|.
- Canonical path: a fixed op sequence O = [o_1, ..., o_L] such that
  P_k = P0 + O[1..k] (op-list concatenation). The full path solves:
  Score(P_L) = |E|.
- Nominal depth d of an instance: the canonical path has exactly d proper
  prefixes that are non-improving under the strict-greedy rule, i.e.
  Score(P_k) <= s0 for k = 1..d in the instance's canonical segmentation
  (section 3 defines stage segmentation; d counts stages, and every op-level
  proper prefix must also satisfy Score <= s0, verified empirically in
  section 7). At least d-1 of the d prefixes must satisfy Score(P_k) < s0
  strictly; at most one tying prefix (Score == s0) is permitted, and its
  position is frozen in the instance spec.
- Strict-greedy baseline (REF-GREEDY): from P0, repeatedly append the single
  op maximizing Score; ties broken by lowest op index in a frozen ordering;
  a move is taken only on STRICT improvement; stop when no strict improvement
  exists. Fully deterministic, no learning, no memory beyond the incumbent.
- Valley crossing (run-level, mechanism-agnostic): a run CROSSED_EVAL iff it
  solved and at least one candidate evaluated before the first solve scored
  strictly below s0. A run CROSSED_COMMIT iff it solved and the mechanism's
  logged incumbent score dipped strictly below s0 before the first solve.
  A run AVOIDED iff it solved with every pre-solve candidate scoring >= s0.
  These are trajectory proxies (section 14), not proofs of mechanism intent.

## 3. Family K: one-key lock (primary, provable depth)

### 3.1 Specification

- Episodes E_n: x in {0, ..., 2^n - 1}, single input (IN0). |E_n| = 2^n.
- Secret key K with 1 <= K <= 9 and K < 2^n. Target f_K(x) = 1 if x == K else 0.
- Decoy P0 = [PUSH 0]. s0 = 2^n - 1 (correct on every episode except x = K).
- Canonical path: [PUSH 1], then stages j = 0..n-1. Stage j is the bit-test

  [IN0, PUSH 2^j, DIV, PUSH 2, MOD, PUSH k_j, EQ, MUL]

  where k_j is bit j of K. Semantics: PUSH 2^j then DIV computes truncated
  x / 2^j; PUSH 2 then MOD computes (x / 2^j) mod 2 = bit j of x; PUSH k_j
  then EQ tests bit j against the key bit; MUL accumulates the conjunction
  (seeded by the initial PUSH 1). After all n stages the top of stack is 1
  iff every bit of x matches K, i.e. iff x == K. Full path solves: 2^n.

  For n = 5, 2^4 = 16 is not directly pushable (PUSH range is -9..9), so
  stage 4 uses the synthesized constant [PUSH 8, PUSH 2, MUL] in place of
  [PUSH 16]. Semantics are identical; the score proof below is unaffected.

### 3.2 Score-profile proof (stage boundaries)

After j complete stages (1 <= j <= n), the top of stack is the conjunction of
the first j bit-matches: 1 iff the low j bits of x equal the low j bits of K.
Score = #{x : [low-j-bits match] == [x == K]}.

Episodes with low-j-bits matching K: 2^{n-j}. Among them, x == K holds for
exactly 1 (namely K itself). Episodes not matching: 2^n - 2^{n-j}, all with
f_K = 0, all correct. Total: (2^n - 2^{n-j}) + 1 = 2^n - 2^{n-j} + 1.

Compare s0 = 2^n - 1: score < s0 iff 2^{n-j} > 2 iff j <= n-2. Score == s0 iff
j = n-1. Score = 2^n iff j = n (full solve).

Hence the canonical path has exactly n-2 strictly-worse stage prefixes and
one tying stage prefix. Nominal depth d = n - 1, with the single tying
prefix at stage n-1. Strict-greedy (strict improvement only) cannot cross
the tie, so REF-GREEDY fails on every Family K instance by construction.

### 3.3 Parameters

Depth d = 1..4 via n = d+1 = 2..5. Episodes 4, 8, 16, 32. Three key values
per n (frozen): n=2: {1,2,3}; n=3: {1,2,5}; n=4: {1,2,9}; n=5: {1,2,9}.
Reserve keys {4,6,7,8} (frozen order) substitute only if a primary key fails
instance acceptance (section 7); substitution is documented, never silent.

Canonical length: 1 + 8n ops (1 + 10n - 2 for n = 5 with synthesized 16;
stage 4 is 10 ops: the 3-op constant synthesis replaces 1 op).

### 3.4 Worked example (n = 2, d = 1, K = 2)

Episodes x in {0,1,2,3}, target 1 iff x == 2. P0 = [PUSH 0], s0 = 3.
Canonical: [PUSH 1,
  IN0, PUSH 1, DIV, PUSH 2, MOD, PUSH 0, EQ, MUL,   (stage 0: bit0 of K is 0)
  IN0, PUSH 2, DIV, PUSH 2, MOD, PUSH 1, EQ, MUL]  (stage 1: bit1 of K is 1)

After stage 0: top = [bit0(x) == 0]. x=0: 1 vs f=0, wrong. x=1: 0 vs 0,
right. x=2: 1 vs 1, right. x=3: 0 vs 0, right. Score 3 = s0 (tie), matching
2^2 - 2^{1} + 1 = 3. After stage 1: [bit0==0 AND bit1==1] = [x==2] = f.
Score 4, solved.

REF-GREEDY from [PUSH 0]: single appends. IN0 gives [0,x], top x: x=0 right
(0==0), x=1..3 wrong: score 1 < 3. PUSH c: const c; c=0 ties 3 (rejected,
strict); c>=1 scores <= 1. No strict improvement exists: REF-GREEDY fails.

## 4. Known shortcut routes (disclosed limitation)

The one-key family admits a non-canonical solution independent of n:

  [IN0, PUSH K, SUB, PUSH 0, EQ]   (5 ops; K pushable since 1 <= K <= 9)

It computes (x - K) == 0, i.e. x == K, solving fully. Its prefixes score:
[IN0]: #{x == f_K(x)} = [K != 0] + [K == 1], which is 1 for K >= 2 and 2
for K == 1; always < s0 = 2^n - 1 for n >= 2. [IN0, PUSH K]: const K >= 1;
for K >= 2 score 0; for K == 1 score 1 (x == K episode only). [IN0, PUSH K,
SUB]: x - K == f_K(x) has no solutions (x == K gives 0 vs 1; x != K gives
x - K = 0 impossible): score 0. So the shortcut crosses an op-level valley
of 3 strictly-worse prefixes regardless of n.

Consequences, all frozen into the protocol:

1. Nominal depth labels the canonical bit-test route. It is an upper bound
   on what the instance demands, not a lower bound on what solvers need.
2. REF-GREEDY acceptance still holds: strict greedy cannot exploit the
   shortcut (every shortcut prefix is strictly worse than s0).
3. Per-solve diagnostics record winner op-length and a NON_CANONICAL flag,
   set iff winner length < canonical length - 2. Shortcut solves are valid
   solves; the flag keeps the inference honest.
4. Comparative inference across mechanisms remains valid: the VM, the
   instances, and the shortcuts are identical for B, D, and C2.

## 5. Family A: arithmetic valleys from lineage failures (ecological validity)

Family K is adversarial (golf-course landscape, section 14). Family A
anchors the battery to valleys the lineage actually encountered. Instances
are specified schematically; exact canonical paths are validated empirically
at implementation under the acceptance criteria of section 7. If validation
fails for an instance, the instance is DROPPED and documented, never
weakened.

- A1 (T0 constant-trap escape): P0 = [PUSH 1] (C1's trap: first repair on
  T0 episode (0,1)). Episodes: T0 train (x in 0..8, target 2x+1, 9 episodes).
  s0 = 1 (x=0 only). Canonical path: the validated repair sequence that
  C2's design walkthrough used ([IN0, PUSH 1] then [IN0, ADD, ADD] per
  `e658766bd`; the implementer re-derives and validates on the frozen VM).
  Expected nominal depth 2..3.
- A2 (T2 from identity): P0 = [IN0]. Episodes: T2 train (x in 0..16, target
  x mod 3, 17 episodes). s0 = 3 (x in {0,1,2}). Canonical: [PUSH 3, MOD]
  appended (program [IN0, PUSH 3, MOD]). Prefix [IN0, PUSH 3] is const 3,
  score 0 < 3. Nominal depth 1. Note: strict greedy from [IN0] moves to
  [IN0, SUB] (const 0, score 6) then stalls below 17; REF-GREEDY fails, as
  required. This is verified empirically, not assumed.
- A3 (T1 abs from const-0): P0 = [PUSH 0]. Episodes: T1 train (x in -8..8,
  target |x|, 17 episodes). s0 = 1 (x=0). Canonical: validated path toward
  D's discovered [IN0, PUSH -2, IN0, MUL, MOD, NEG, NEG] or equivalent;
  the implementer validates the prefix score profile. Expected depth 2..4.

Family A instances slot into depth levels by their VALIDATED nominal depth.
An instance whose validated depth falls outside 1..4 is reported separately
(characterization data, excluded from max_depth aggregation).

## 6. CAL-0: calibration instance (depth 0)

P0 = [PUSH 0]. Episodes: x in 0..8, target x (identity, 9 episodes). s0 = 1
(x=0). Single improving op exists: append IN0 ([0,x], top x) solves 9/9.
Every mechanism must solve CAL-0. Failure indicates a broken harness or
adapter, not a mechanism defect: the battery run is void until CAL-0 passes.

## 7. Instance acceptance criteria (frozen validation procedure)

Before any mechanism runs on any valley instance, the battery implementer
validates every instance on the frozen VM and commits the validation log.
An instance is ACCEPTED iff all of the following hold; otherwise it is
dropped with documentation:

- V1 (score profile): every op-level proper prefix of the canonical path
  scores <= s0; at least d-1 score strictly < s0; at most one ties; the full
  path scores exactly |E|.
- V2 (greedy fails): frozen REF-GREEDY from P0 does not solve.
- V3 (no shallow shortcut): no program within 2-op edit distance (append,
  replace, or delete, over the straight-line op alphabet of section 2) of
  any canonical prefix solves. Bounded exhaustive check; residual risk
  beyond 2 ops is disclosed (section 4 documents the known 5-op shortcut).
- V4 (falsified-mechanism calibration): the frozen A implementation and the
  frozen C1 implementation are run on the instance; both must FAIL to solve.
  If either solves a depth >= 1 instance, the instance is miscalibrated and
  dropped. (A and C1 are myopic by established verdict; a valley they solve
  is not a valley.)
- V5 (determinism): the validation scores are 3/3 byte-identical.

## 8. Measurement protocol

### 8.1 Harness interface

Each mechanism MUST accept an externally supplied starting program. The
harness preloads P0 as the starting incumbent and reports s0. Mechanism
adapters (one per mechanism, part of the battery implementation, in Zag):

- C2: best_P initialized to P0; counterexample set = episodes P0 fails.
- D: archive seeded with P0 as the initial elite.
- B: base/assembly search initialized from P0 with empty library.

If a mechanism cannot start from P0, that is reported as a mechanism
limitation and the mechanism is excluded from the battery with documentation
(it is not scored zero).

### 8.2 Frozen budget

Per (mechanism, instance): 1,000,000 candidate evaluations OR 300 seconds
wall clock, whichever is reached first. Identical to battery v1 (`425f7276d`,
section 3). One candidate evaluation = one candidate program executed against
the full episode set. Budget exhaustion without SOLVE is FAIL.

### 8.3 Trajectory logging (mandatory, in Zag)

- LOG-1: every candidate evaluation: (seq_idx, program ops, score).
- LOG-2: incumbent improvements: (seq_idx, program ops, score) whenever the
  mechanism's incumbent best changes.
- LOG-3: mechanism-specific commit events with parent pointers (C2: repair
  commits and backtracks; D: elite insertions with parent id; B: induction,
  retrieval, and assembly events).

### 8.4 Derived metrics (computed by the Zag analyzer)

- M1: SOLVED iff some evaluated candidate scores |E|; else FAILED.
- M2: evals_used: seq_idx of first solve, or total evals if failed.
- M3: min_pre_solve: minimum LOG-1 score before first solve (all evals if
  failed).
- M4a: CROSSED_EVAL = SOLVED and min_pre_solve < s0.
- M4b: CROSSED_COMMIT = SOLVED and min LOG-2 incumbent score pre-solve < s0.
- M4c: AVOIDED = SOLVED and every pre-solve LOG-1 score >= s0.
- M5: winner ops, winner length, NON_CANONICAL flag (section 4).

### 8.5 Aggregation: max_depth

Depth levels d = 0..4. Level 0 = {CAL-0}. Level d >= 1 = the 3 accepted
Family K instances at that depth plus accepted Family A instances with
validated nominal depth d.

solve_rate(M, d) = fraction of level-d instances solved by M.
max_depth(M) = largest d with solve_rate(M,d) >= 2/3 AND solve_rate(M,d')
>= 2/3 for all d' < d. Level 0 must be solved (else the run is void per
section 6).

Determinism: 3/3 byte-identical runs per (M, instance) at 1x budget.

## 9. Budget sensitivity and plateau classification

Let d* = max_depth(M) + 1 (first failure level). If max_depth(M) = 4, no
failure was observed: plateau = NONE (ceiling not reached; battery extension
is future work, not a trigger).

Rerun the d* instances at 4x budget (4,000,000 evals / 1200 s) and 16x
budget (16,000,000 evals / 4800 s). Single run per (M, instance) at 4x/16x
is permitted iff the mechanism demonstrated 3/3 determinism at 1x;
otherwise 3/3.

Let s1, s4, s16 be solve rates at 1x, 4x, 16x on the d* instances.

- BUDGET-SHAPED iff (s4 >= 2/3 or s16 >= 2/3) OR (every failed run at 1x,
  4x, and 16x consumed the full eval budget, i.e. the mechanism never
  terminated early by its own stopping rule).
- STRUCTURAL iff s16 < 2/3 AND at least one run at 16x terminated early
  (evals_used < cap) by the mechanism's own frozen stopping rule without
  solving. Supplementary exhaustion signals, logged per mechanism: C2:
  backtracks_used == BMAX with tabu saturated and lookahead finding no
  positive-gain extension; D: no new archive cells in the final 10% of
  evals; B: base search terminated with no induction or retrieval events
  in the final phase. These corroborate but do not replace the early-stop
  rule.
- UNCLEAR otherwise. UNCLEAR never triggers section 10.

## 10. Plateau criteria (the treadmill watch made operational)

Computed after sections 8 and 9 complete for all of B, D, C2:

- T-BUDGET (treadmill): all three mechanisms classify BUDGET-SHAPED.
  Action: STOP the program-discovery lineage. No N+1 hypothesis. Open the
  architecture review. Rationale: compute, not mechanism design, is the
  binding constraint; further search-tuning is the treadmill.
- T-WALL (common structural wall): all three classify STRUCTURAL (UNCLEAR
  does not count) AND max(max_depth) - min(max_depth) <= 1 over the three
  mechanisms. Action: STOP the lineage. Open the architecture review.
  Rationale: three different search mechanisms hit the same structural
  wall; the shared substrate (prefix-appended VM-op construction) is the
  likely binding constraint, which is exactly the standing review question.
- CONTINUE: anything else. The battery has discriminated the mechanisms;
  the lineage continues with the winner(s). In particular, if one mechanism
  structurally dominates (e.g. max_depth 4 vs 1), that is evidence FOR its
  approach, not a trigger.

## 11. Architecture review on trigger

Triggering T-BUDGET or T-WALL opens a new architecture review (a review
document, not a hypothesis). Its frozen question is the standing one: "Is
the current representation itself wrong?" Concrete alternatives on the
table, frozen here so the review cannot drift:

1. Keep prefix-append construction but change the op alphabet to
   learner-recruited operators (the OP-RECRUIT v2 track, `c6ef7ffcf`;
   the C0 integration design `9aa1fb0b5`).
2. Move construction to learner-authored fragments on the generic
   executable VM (the GENEXEC2 program-discovery track that B's fragment
   library points toward).
3. Retire constructive prefix search for valley-crossing and pursue the
   C0INTEG grown-menu discovery architecture instead.

Possible outcomes: adopt an alternative (with its own prereg), amend the
representation within the lineage (transparent amendment, re-freeze), or
retire the lineage. "Try harder with more budget" is not an outcome under
T-BUDGET; "a fourth search tweak" is not an outcome under T-WALL without
answering the frozen question first.

## 12. Governance

- This design freezes nothing executable. A separate battery PREREG must be
  committed BEFORE any valley instance is generated or validated, and
  instance generation plus validation must complete BEFORE any mechanism
  runs on any instance. Commit order verified by ancestry.
- Information barrier: valley instances (keys, canonical paths) must be
  generated AFTER the last mechanism code freeze among {B, D, C2},
  verified by commit ancestry. Any mechanism commit touching search logic
  after the valley-instance freeze voids that mechanism's valley results.
  Rationale: B and D are already frozen; C2 is implementing now; no
  mechanism may be tuned on the valleys.
- Frozen in the prereg: the full instance list (keys, P0 programs, episode
  sets, canonical paths), REF-GREEDY spec, budgets (1x/4x/16x), solve
  thresholds, the section 9 classification rules verbatim, and the
  section 10 trigger rules verbatim. The trigger rules may not be altered
  after results are seen (Micah's literal rule: never alter a kill bar
  after seeing results).
- Determinism: 3/3 byte-identical per (M, instance) at 1x (section 8.5).
- Purity: pure Zag throughout the battery implementation, validation,
  measurement, and analysis. No Python anywhere, including scratch,
  diagnostics, and byte checks. No em dashes in any committed document.
- The paper (`TNN_RESEARCH_PAPER_20260929.md`) remains a contaminated
  internal log: no wave may cite it as evidence for valley claims.

## 13. Kill-bar self-check

- K1 (valleys parameterized): Family K parameterized by n = 2..5 giving
  nominal depths 1..4 with a proved score profile (section 3.2), frozen key
  sets, and a worked n=2 example (section 3.4). Family A gives three
  lineage-grounded instances with empirical validation (section 5). CAL-0
  gives depth 0 (section 6).
- K2 (protocol specified): harness interface with P0 preload (8.1), frozen
  budget matching battery v1 (8.2), mandatory trajectory logging LOG-1/2/3
  (8.3), derived metrics M1-M5 including crossed/avoided (8.4), aggregation
  to max_depth with determinism requirements (8.5), and instance acceptance
  V1-V5 including the falsified-mechanism calibration (section 7).
- K3 (plateau criterion defined): budget sensitivity reruns at frozen 4x
  and 16x multipliers (section 9), exact BUDGET-SHAPED / STRUCTURAL /
  UNCLEAR classification rules, and the T-BUDGET / T-WALL / CONTINUE
  trigger logic with mandated actions (section 10), plus the review's
  frozen question and alternatives (section 11).

## 14. Honest limitations

1. Nominal depth is an upper bound. Shortcuts (section 4) mean a mechanism
   can solve a nominal-d instance while demonstrating shallower crossing.
   The valid inference is comparative across mechanisms, not absolute.
2. Family K is a golf-course landscape: maximally adversarial, minimal
   ecological validity. Real discovery tasks are not combination locks.
   Family A compensates but has only three instances.
3. CROSSED_EVAL / CROSSED_COMMIT / AVOIDED are trajectory proxies. A
   mechanism can evaluate a worse program incidentally (lookahead) without
   depending on it; the metrics do not distinguish dependence from
   exposure. LOG-3 exists for qualitative follow-up.
4. The 2-op neighborhood check (V3) is bounded; deeper shortcuts than the
   documented 5-op SUB route are a residual risk, mitigated by identical
   exposure across mechanisms.
5. Budget multipliers are coarse: 16x wall clock reaches 4800 s per run.
   If prohibitive, the implementer requests a transparent amendment;
   the multipliers are not silently reduced.
6. Canonical paths are straight-line. Mechanisms may use jumps and CALL;
   the battery measures solving, not path fidelity.
7. B starts with an empty library in this battery. B's library-mediated
   valley avoidance (its T4/T5 strategy in the main battery) is therefore
   not measured here; the main battery already covers it.

## 15. References

- Frontier W2 with H-NEW-6 and treadmill watch: `1d72eac51`.
- Discovery battery prereg (budget/metrics conventions): `425f7276d`.
- Frozen GENEXEC2 VM and op set: `8d5f58b89`.
- A falsified (myopia): result `21d838921`, prereg `58c2cc66b`.
- C1 falsified (myopia, splitting): result `aae06bac6`, prereg `5a9ec56e7`.
- C2 design (lookahead, net-progress, backtracking): `e658766bd`.
- B result (B-TESTED, T0-T5 carried): `hyp_b/RESULT_HYPB.md`.
- D result (D-TESTED, T0-T2): `hyp_d/HYPD_RESULT.md`.
- Implications analysis (non-myopic requirement): `bee0f840d`.

---

Builder label: DESIGN-COMPLETE.
