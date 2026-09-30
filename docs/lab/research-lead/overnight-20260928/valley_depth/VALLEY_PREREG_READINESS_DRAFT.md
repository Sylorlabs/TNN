# VALLEY BATTERY PREREG: READINESS ASSESSMENT (DRAFT PREPARATION NOTES)

Date: 2026-09-30.
Status: DRAFT PREPARATION NOTES. NOT FROZEN. NOT A PREREG.
Purpose: Record the freeze-state check and stage every content block the
future valley-battery prereg will freeze, so the prereg can be cut
immediately once C2's implementation freezes. No instance list is frozen
by this document. No evaluation is authorized by this document.

Authority: H-NEW-6 design `76c7a887c` (VALLEY_DEPTH_DESIGN.md, 433 lines).

## 1. Readiness assessment: C2 is NOT frozen

Mechanism freeze state, verified by commit ancestry on `tnn-native-lab`
(HEAD `9bc64e4cf` at time of check):

- B (fragment induction): FROZEN. Prereg `9e2fbd134` is an ancestor of HEAD.
  Implementation and results committed in `69730b4ab` (swept commit; content
  verified by the B worker, md5 match; prereg strictly precedes). Also in
  HEAD ancestry.
- D (MAP-Elites): FROZEN. `D-TESTED` commit `e2ee0964e` is an ancestor of
  HEAD and of the valley design itself.
- C2 (lookahead plus backtracking): NOT FROZEN. Only two commits touch the
  C2 track: prereg `01336fe83` and v2 amendment `9bc64e4cf` ("Amend C2 prereg
  to Battery v2: GENEXEC2-P for T1/T4/T5, frozen before v2 code"). No
  implementation or results commit exists anywhere in the repo. The files
  `hyp_c2_impl/hyp_c2.zag`, `hyp_c2`, `run1.txt`, `run2.txt`, `run3.txt`,
  and `run_v2_1.txt` exist in the worktree as UNTRACKED files (git status
  `??`). `git log --all -- '*/hyp_c2.zag'` returns nothing.

Kill-bar status:
- K1 (C2 freeze verified): NOT MET. C2's code is uncommitted and its worker
  remains active (redirected to Battery v2 tasks per parent instruction).
- K2 (instances/keys frozen): NOT MET, deliberately. See section 2.
- K3 (barrier verified): CANNOT BE MET YET. The barrier requires the
  instance freeze to come after the last mechanism code freeze.

## 2. Why the prereg must wait

Design section 12 (Governance), information barrier: "valley instances
(keys, canonical paths) must be generated AFTER the last mechanism code
freeze among {B, D, C2}, verified by commit ancestry. Any mechanism commit
touching search logic after the valley-instance freeze voids that
mechanism's valley results."

The prereg freezes the full instance list (keys, P0 programs, episode sets,
canonical paths). If the prereg were committed now, C2's forthcoming
implementation commit would land AFTER the valley-instance freeze and would
void C2's valley results under the design's own rule. Writing the prereg
now would therefore actively damage the battery. The correct action is to
wait for C2's implementation commit, then cut the prereg.

Additional ordering note: the valley design `76c7a887c` is already an
ancestor of C2's v2 amendment `9bc64e4cf`, and the design publishes the
Family K keys in section 3.3. The keys are therefore visible in the repo
before C2's code freezes. The prereg will re-freeze the identical keys, so
no new information is revealed by the prereg itself; the enforceable part
of the barrier is the ancestry rule (no search-logic commits after the
instance freeze) plus the frozen trigger rules of sections 9 and 10.

## 3. Prereg content skeleton (to be frozen verbatim once C2 lands)

### 3.1 Family K instance table (full GENEXEC2, frozen VM `8d5f58b89`)

P0 = [PUSH 0] for all Family K instances. Target f_K(x) = 1 iff x == K.

| n | nominal depth d | episodes | frozen keys | s0 = Score(P0) |
|---|-----------------|----------|-------------|----------------|
| 2 | 1 | 4 (x in 0..3) | {1, 2, 3} | 3 |
| 3 | 2 | 8 (x in 0..7) | {1, 2, 5} | 7 |
| 4 | 3 | 16 (x in 0..15) | {1, 2, 9} | 15 |
| 5 | 4 | 32 (x in 0..31) | {1, 2, 9} | 31 |

Reserve keys (frozen order): {4, 6, 7, 8}. Substitute only if a primary key
fails instance acceptance; substitution is documented, never silent.

Canonical path: [PUSH 1], then stages j = 0..n-1, each stage
[IN0, PUSH 2^j, DIV, PUSH 2, MOD, PUSH k_j, EQ, MUL], where k_j is bit j of
K. For n = 5, stage 4 synthesizes PUSH 16 as [PUSH 8, PUSH 2, MUL].
Canonical length: 1 + 8n ops (1 + 10n - 2 for n = 5).

Score profile (proved, design section 3.2): after j stages,
score = 2^n - 2^{n-j} + 1. Stages 1..n-2 strictly worse than s0, stage n-1
ties s0, stage n solves. Nominal depth d = n - 1 with the single tying
prefix at stage n-1. REF-GREEDY fails on every Family K instance by
construction.

Known shortcut (disclosed, design section 4): [IN0, PUSH K, SUB, PUSH 0, EQ]
(5 ops) solves any one-key instance via a 3-deep op-level valley. Nominal
depth is an upper bound on what the instance demands. Per-solve diagnostics
record winner length and a NON_CANONICAL flag (set iff winner length <
canonical length - 2). Comparative inference across mechanisms remains valid
(identical VM, instances, and shortcuts for B, D, C2).

### 3.2 Family A schemas (validated at implementation, acceptance V1-V5)

- A1 (T0 constant-trap escape): P0 = [PUSH 1]. Episodes: T0 train (x in
  0..8, target 2x+1, 9 episodes). s0 = 1. Canonical: validated repair
  sequence from the C2 design walkthrough (`e658766bd`). Expected depth 2..3.
- A2 (T2 from identity): P0 = [IN0]. Episodes: T2 train (x in 0..16, target
  x mod 3, 17 episodes). s0 = 3. Canonical: [PUSH 3, MOD]. Nominal depth 1.
- A3 (T1 abs from const-0): P0 = [PUSH 0]. Episodes: T1 train (x in -8..8,
  target |x|, 17 episodes). s0 = 1. Canonical: validated path toward D's
  discovered form or equivalent. Expected depth 2..4.

Family A instances slot into depth levels by VALIDATED nominal depth. An
instance whose validated depth falls outside 1..4 is reported separately
and excluded from max_depth aggregation. An instance failing validation is
DROPPED with documentation, never weakened.

### 3.3 CAL-0 (depth 0 calibration)

P0 = [PUSH 0]. Episodes: x in 0..8, target x (identity, 9 episodes). s0 = 1.
Appending IN0 solves 9/9. Every mechanism must solve CAL-0; failure voids
the battery run (harness or adapter fault, not a mechanism result).

### 3.4 REF-GREEDY spec (frozen)

From P0, repeatedly append the single op maximizing Score; ties broken by
lowest op index in a frozen ordering; a move is taken only on STRICT
improvement; stop when no strict improvement exists. Fully deterministic,
no learning, no memory beyond the incumbent.

### 3.5 Budgets (frozen)

Per (mechanism, instance): 1x = 1,000,000 candidate evaluations OR 300 s
wall clock, whichever first. Sensitivity reruns at the first failure level
d*: 4x = 4,000,000 evals / 1200 s; 16x = 16,000,000 evals / 4800 s. One
candidate evaluation = one candidate program executed against the full
episode set. Budget exhaustion without SOLVE is FAIL.

### 3.6 Logging and metrics (frozen)

- LOG-1: every candidate evaluation (seq_idx, program ops, score).
- LOG-2: incumbent improvements (seq_idx, program ops, score).
- LOG-3: mechanism commit events with parent pointers (C2: repairs and
  backtracks; D: elite insertions with parent id; B: induction, retrieval,
  assembly events).
- M1: SOLVED iff some evaluated candidate scores |E|.
- M2: evals_used (first-solve seq_idx, or total if failed).
- M3: min_pre_solve (minimum LOG-1 score before first solve).
- M4a CROSSED_EVAL: SOLVED and min_pre_solve < s0.
- M4b CROSSED_COMMIT: SOLVED and min LOG-2 incumbent pre-solve < s0.
- M4c AVOIDED: SOLVED and every pre-solve LOG-1 score >= s0.
- M5: winner ops, winner length, NON_CANONICAL flag.

### 3.7 Aggregation: max_depth (frozen)

Depth levels d = 0..4. Level 0 = {CAL-0}. Level d >= 1 = accepted Family K
instances at that depth plus accepted Family A instances with validated
nominal depth d. solve_rate(M, d) = fraction of level-d instances solved.
max_depth(M) = largest d with solve_rate(M,d) >= 2/3 AND solve_rate(M,d')
>= 2/3 for all d' < d. Level 0 must be solved or the run is void.
Determinism: 3/3 byte-identical runs per (M, instance) at 1x budget.

### 3.8 Instance acceptance V1-V5 (frozen validation procedure)

V1 (score profile): every op-level proper prefix of the canonical path
scores <= s0; at least d-1 strictly below; at most one ties; full path
scores exactly |E|. V2 (greedy fails): frozen REF-GREEDY from P0 does not
solve. V3 (no shallow shortcut): no program within 2-op edit distance of
any canonical prefix solves. V4 (falsified-mechanism calibration): frozen A
and frozen C1 implementations both FAIL every depth >= 1 instance, else the
instance is miscalibrated and dropped. V5 (determinism): validation scores
3/3 byte-identical.

### 3.9 Section 9 classification rules (frozen verbatim)

Let d* = max_depth(M) + 1 (first failure level). If max_depth(M) = 4,
plateau = NONE (ceiling not reached; extension is future work, not a
trigger). Rerun d* instances at 4x and 16x. Let s1, s4, s16 be solve rates
at 1x, 4x, 16x on the d* instances.

- BUDGET-SHAPED iff (s4 >= 2/3 or s16 >= 2/3) OR (every failed run at 1x,
  4x, and 16x consumed the full eval budget, i.e. the mechanism never
  terminated early by its own stopping rule).
- STRUCTURAL iff s16 < 2/3 AND at least one run at 16x terminated early
  (evals_used < cap) by the mechanism's own frozen stopping rule without
  solving. Corroborating exhaustion signals: C2 backtracks_used == BMAX
  with tabu saturated and no positive-gain lookahead extension; D no new
  archive cells in the final 10 percent of evals; B base search terminated
  with no induction or retrieval events in the final phase.
- UNCLEAR otherwise. UNCLEAR never triggers section 10.

### 3.10 Section 10 triggers (frozen verbatim)

- T-BUDGET (treadmill): all three mechanisms classify BUDGET-SHAPED.
  Action: STOP the program-discovery lineage. No N+1 hypothesis. Open the
  architecture review.
- T-WALL (common structural wall): all three classify STRUCTURAL (UNCLEAR
  does not count) AND max(max_depth) - min(max_depth) <= 1 over the three
  mechanisms. Action: STOP the lineage. Open the architecture review.
- CONTINUE: anything else. The battery has discriminated the mechanisms;
  the lineage continues with the winner(s). Structural dominance by one
  mechanism is evidence FOR its approach, not a trigger.

The trigger rules may not be altered after results are seen.

## 4. Open questions for the parent (decision needed before the prereg)

Q1 (VM scope): The valley design specifies full GENEXEC2 (frozen VM
`8d5f58b89`); the Family K canonical path requires DIV, MOD, and EQ. The
battery v2 redesign (`611e8fa1f`) removed {DIV, MOD, LT, EQ, GT} for the
main battery's T1/T4/T5 (GENEXEC2-P) and redirected the C2 implementer to
GENEXEC2-P. Question: does the valley battery run on full GENEXEC2 as
designed (in which case C2 needs a full-GENEXEC2 implementation or adapter
for valley participation, separate from its GENEXEC2-P main-battery work),
or should the valley battery be re-scoped to GENEXEC2-P (which would
require reworking the Family K canonical path, since DIV/MOD/EQ are
removed)? Recommendation: keep full GENEXEC2 for the valley battery; the
v2 redesign's rationale (the MOD shortcut) does not apply to Family K,
whose canonical route already accounts for shortcuts in section 4. But
this is a parent-level scoping decision.

Q2 (C2 freeze definition): C2's main-battery implementation is being
redirected to GENEXEC2-P. For the valley battery's information barrier,
"the last mechanism code freeze among {B, D, C2}" should be defined as the
commit freezing the code that will actually run on the valley battery
(full GENEXEC2 per Q1's recommended answer). If C2's valley participation
uses an adapter over its main implementation, the adapter commit is the
freeze point.

Q3 (sequencing): After C2's freeze commit lands, the order is: (a) cut the
valley prereg (this skeleton, frozen verbatim); (b) generate and validate
instances, commit the validation log and the validated instance set
(Family A validated paths land here); (c) run mechanisms; (d) run 4x/16x
sensitivity; (e) apply section 10 triggers.

## 5. Limitations carried from the design (not resolved here)

Nominal depth is an upper bound (shortcuts). Family K is a golf-course
landscape with low ecological validity (Family A compensates, three
instances only). CROSSED/AVOIDED are trajectory proxies, not proofs of
dependence. The 2-op V3 check is bounded; deeper shortcuts than the
documented 5-op route are a residual risk with identical exposure across
mechanisms. 16x wall clock reaches 4800 s per run. B runs with an empty
library here; its library-mediated avoidance is covered by the main
battery, not this one.

---

End of draft preparation notes. Awaiting C2 implementation freeze.
Builder label: WAITING-FOR-C2.
