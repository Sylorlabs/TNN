# IMPLICATIONS ANALYSIS: What Hypothesis A's Falsification Means for B, C, D

Date: 2026-09-30.
Status: ANALYSIS. No implementation. Design review only.
Authority: analyzes `arch_review/ARCHITECTURE_REVIEW.md` (18be93c3e),
`discovery_battery/PREREG_BATTERY.md` (425f7276d), `hyp_a/HYP_A_RESULT.md`
(21d838921), `hyp_c/PREREG_HYP_C.md`, `hyp_d/PREREG_HYPD.md`.
No hyp_b prereg was committed at time of writing; B is analyzed from the
frozen review specification.

## 0. A's flaw, stated precisely

Hypothesis A (residual driven construction) was falsified by A-F1: it
failed T0 (2x+1) and T2 (mod3), both predicted SOLVE.

Trace (T0): after P=[IN0], residual R=[1,2,3,4,5,6,7,8,9],
complexity=9000008. The predicted next step PUSH 2 gives
P=[IN0, PUSH 2], R=[-1,1,3,5,7,9,11,13,15], complexity=9000016,
which is WORSE. Greedy single op selection never takes it. The
constant residual signal (which would dictate PUSH 1, ADD after
[IN0, PUSH 2, MUL]) is unreachable via monotonic complexity
reduction.

Trace (T2): the empty program already achieves minimal complexity
(3 distinct values, range 2). No single op improves it. A cannot
even start, because IN0 (the necessary first step toward
[IN0, PUSH 3, MOD]) makes the residual worse.

General principle: **a greedy single step criterion cannot traverse
a valley where the intermediate step scores worse on the local
objective.** Multi step dependencies (PUSH 2 then MUL; PUSH 3 then
MOD) require tolerating intermediate states that do not improve the
myopic measure. A forbade this. A died.

A-F2 did NOT fire: the trace shows genuine single trajectory
construction, not a renamed beam. A was genuinely different from
beam search and genuinely ineffective. The review's assessment
(discovery is the defect, not the VM) stands.

## 1. Hypothesis B (semantic fragment induction): impact analysis

B's mechanism has three parts: (i) a base constructor finding
straight line programs, (ii) an inducer extracting sub task
fragments with behavioral semantic signatures from traces, (iii) a
composer retrieving fragments by behavioral match and composing
with CALL.

Does B rely on monotonic improvement? The induction and composition
machinery does NOT. Fragment proposal is by semantic match to task
substructure, not by a monotonic score. Retrieval is by behavioral
similarity, not by ranking. The novelty of B (behavioral signatures,
semantic dedup, retrieval driven composition) is orthogonal to A's
flaw.

BUT: part (i), the base constructor, is specified in the review as
"any adequate discoverer; B's novelty is not the base." This is the
load bearing ambiguity. B's predictions on T0, T2, T3 (straight
line tasks) are staked as SOLVE "via the base constructor" with "no
fragment needed." If the implementer chooses a greedy monotonic
base (residual driven like A, or score ranked like the banned beam),
B inherits A's flaw exactly on the adequacy gate tasks.

Consequences:
- If B's base is myopic, B fails T0 the way A did. That would be an
  implementation choice failure, not a falsification of the
  induction and composition idea. B-F1 through B-F3 (the frozen
  falsifiers) do not cover base constructor failure; the battery
  outcome table stakes SOLVE on T0 without a base specific
  falsifier.
- B's genuine predictions (retrieval events and 2+ CALLs to ABS on
  T4; induction event with semantic signature on T1) are only
  testable if B survives the straight line tasks first. The
  mechanism level discrimination against C on T4 depends on B
  reaching T4 with an induced ABS fragment.
- The sharpest risk for B is sequencing: it must solve T0 before
  its novelty is even exercised.

Verdict on B: **A's flaw does not touch B's core idea, but B's
unstated base constructor is at high risk of reintroducing the
same flaw.** Survival is conditional on the implementer selecting a
non myopic base. If the base is D like (novelty retained) or
exhaustive within budget, B can reach T4 and its fragment
predictions become testable. If the base is A like, B dies on T0.

## 2. Hypothesis C (counterexample driven structural growth): impact analysis

C's mechanism: state is program P plus counterexample set. Repair:
search single op appends in deterministic op order for one that
fixes the first failing episode e while breaking no currently
passing episode (verified by re evaluation). Take the FIRST that
works; no ranking. If no repair exists, split on a probe from the
frozen family, recurse on each partition.

Does C's repair require monotonicity? It does not use a complexity
measure. But it has a myopic correctness criterion: **each repair
step must fix the current failing episode immediately.** This is
the same FAMILY of flaw as A (greedy single step decisions cannot
cross valleys), manifesting differently.

Trace argument (T0, from the frozen prereg mechanism):
- P=[]. Episodes (0,1),(1,3),... First failing e=(0,1).
- Repair tries IN0 first: [IN0] on (0,1) gives 0, not 1. Rejected
  (does not fix e).
- Repair tries PUSH 1: [PUSH 1] gives 1. Fixes e. Passing set under
  [] is empty, so nothing breaks. ACCEPTED. P=[PUSH 1].
- Now passing={(0,1)}, failing e=(1,3). Repair needs a single op
  appended to [PUSH 1] giving 3 on x=1 and 1 on x=0. No such op
  exists (IN0 gives x; PUSH k gives constant k; stack ops are
  no ops on single element). No repair.
- C splits. But T0 is a single straight line function (true region
  count 1). Continued myopic repair (PUSH 3, PUSH 5, ...) plus
  splitting yields one region per episode. This is C-F3: split
  count grows with episode count rather than true regions.

The structural point: IN0 is never a valid first repair on T0,
because IN0 does not fix any single T0 episode (2x+1=x has no
solution in the train set). C's repair can therefore never begin a
program with IN0 on T0. Any IN0 first program is unreachable via
C's repair from empty P. The predicted "short repair chain" for T0
in the review does not exist under the specified mechanism.

Same valley argument (T2): C's first repair on T2 IS IN0 (it fixes
(1,1) while preserving (0,0)), so P=[IN0]. Then e=(3,0): no single
op appended to [IN0] implements mod 3 while preserving (0,0),(1,1).
The two step dependency (PUSH 3 then MOD) is unreachable because
the intermediate [IN0, PUSH 3] (constant 3) does not fix (3,0).
This is exactly A's valley (PUSH 2 then MUL), with "does not fix
e" playing the role of "increases complexity."

On the split tasks (T1, T4, T5), the myopia is also present: the
first repair is always a constant (PUSH c), because a constant is
the first op in deterministic order that fixes any single episode,
while structural ops (IN0) fix no single episode on these tasks
either. Each branch of a split re grows from scratch and repeats
the myopic constant fit, then splits again. The split operator,
which is C's correct mechanism for piecewise structure, is reached
only after a myopic dead end, and the recursion re introduces the
myopia.

Verdict on C: **C's repair operator suffers from the same family
of flaw as A.** "Must fix the current failing episode now" is a
greedy local criterion that forbids intermediate structural steps
(IN0, PUSH 3) which do not immediately pay off. It manifests as
systematic constant fitting bias (PUSH c first), dead ends, and
pathological splitting. C-F1 (fails T0) and C-F3 (split count
tracks episodes, not regions) are both at high risk under the
mechanism as specified in the frozen prereg. The review's C
predictions (SOLVE via repair chain on T0; clean single split on
T1) appear optimistic given the specified repair semantics.

Caveat: this analysis is of the mechanism as written in
PREREG_HYP_C.md. The implementer is bound by that prereg. If the
analysis is correct, the falsification would be of the specific
myopic repair operator, not of counterexample driven growth in
principle. A repaired C (multi op repair lookahead, softer repair
criterion such as reducing the failing count, or explicit
scaffolding steps) remains a live direction.

## 3. Hypothesis D (MAP-Elites control): impact analysis

D's mechanism: archive indexed by (length bucket, score, behavior
hash). A candidate is retained if its niche is empty (novelty) or
its score beats the niche elite. No global ranking. Mutation by
append, replace, delete in deterministic order.

Does D rely on monotonic improvement? **No.** This is the central
point. Retention on empty niche explicitly preserves candidates
regardless of score. The deceptive prefix [IN0, PUSH 2, MUL, PUSH 1]
occupies its own niche (behavior constant 1, length bucket 4,
score 0) and survives independent of its poor score; mutation then
appends ADD. The intermediate [IN0, PUSH 2], which A rejected for
increasing complexity, is retained in D if its behavior hash niche
is empty. There is no monotonicity requirement anywhere in D's
retention rule.

Valley crossing check (T0): the chain [IN0] -> [IN0, PUSH 2] ->
[IN0, PUSH 2, MUL] -> [IN0, PUSH 2, MUL, PUSH 1] -> SOLVE is
preserved step by step because each link has a distinct behavior
(identity, constant 2, doubling, constant 1) and therefore a
distinct niche. D crosses exactly the valley that killed A.

One subtlety: the behavior hash is a discretized sign vector
(trits of output sign per episode). On T0 (x in 0..8), [IN0, PUSH 2]
(constant 2, all positive) and [IN0, PUSH 2, MUL, PUSH 1]
(constant 1, all positive) share the same sign pattern, hence the
same hash. They are disambiguated by length bucket (2 vs 4), so
both are retained. The length bucket component of the niche is
load bearing here; without it these two stepping stones would
collide.

D's predictions are modest (SOLVE on straight line T0/T2/T3, FAIL
on conditional T1/T4/T5, where its op set has no comparison, jump,
or CALL). The FAIL predictions are control behavior, not
falsifiers. D-F1 (fails T0) would indicate misconfiguration; the
mechanism as specified looks sound for the straight line tasks.

Verdict on D: **A's flaw does not affect D. D's novelty retention
is an explicit antidote to myopic pruning.** D is the most likely
of the four to match its frozen predictions exactly, because its
mechanism is simple, its retention criterion is orthogonal to the
objective, and its predictions do not overreach its machinery.

## 4. Survival predictions

Ranked by probability of matching frozen battery predictions:

1. **D (MAP-Elites): highest.** Mechanism sound for its modest
   predictions. Novelty retention crosses the valley that killed
   A. Expected: SOLVE T0/T2/T3, FAIL T1/T4/T5, all CONFIRMED or
   correct control behavior. Risk is configuration (niche
   collisions, budget), not mechanism.

2. **B (fragments): medium, conditional.** The induction and
   composition idea is untouched by A's flaw. Survival depends
   entirely on the unspecified base constructor. With a non myopic
   base, B can reach T4 and its retrieval and CALL predictions
   become testable; the B vs C mechanism discrimination on T4
   (CALLs plus retrieval vs splits plus zero CALLs) remains the
   sharpest experiment in the battery. With a myopic base, B dies
   on T0 and its novelty is never exercised.

3. **C (counterexample growth): low as specified.** The repair
   operator's "must fix e now" criterion is greedy in the same
   family as A's "must reduce complexity now." It induces
   constant fitting bias, dead ends, and pathological splitting.
   C-F1 and C-F3 are at high risk. If falsified, the lesson is
   about the repair operator specifically; counterexample driven
   splitting with a non myopic repair remains viable.

4. **A: falsified.** A-F1 fired. The residual complexity driver is
   inadequate.

## 5. What a successful discovery mechanism needs

From A's falsification and the B/C/D analysis, five requirements:

1. **Valley crossing.** The mechanism must tolerate intermediate
   states that score worse (or no better) on the local objective.
   A forbade this via monotonic complexity; C forbids it via
   must fix now; score ranked beams forbid it via pruning. D
   allows it via novelty; B allows it via behavioral matching.
   Any successful mechanism needs a retention or proposal
   criterion orthogonal to the immediate objective.

2. **Multi step credit assignment.** PUSH 2 is valuable because it
   enables MUL, not because it helps alone. Mechanisms that
   evaluate single steps in isolation (A's greedy pick, C's
   single op repair) cannot see this. Requirements: either
   preserve intermediates regardless of immediate payoff (D's
   archive, B's trace induction), or search explicitly over multi
   step sequences (bounded lookahead in repair).

3. **Separation of proposal from retention.** A's flaw was
   conflating "what to try next" (complexity reducing op) with
   "what is valuable" (eventual solution). D separates them:
   propose by mutation, retain by novelty. B separates them:
   propose fragments by behavioral match, retain by semantic
   dedup. Successful mechanisms keep these distinct.

4. **Non myopic repair (for counterexample driven methods).** A
   repair operator that must fix the current failing episode in
   one step will always prefer constants over structural ops.
   Repair needs lookahead (2-3 ops), a softer criterion (reduce
   failing count, improve a secondary measure), or explicit
   scaffolding moves that are exempt from the fix requirement.

5. **An adequate base remains the open problem.** B delegates
   straight line discovery to "any adequate discoverer," but
   adequate discoverers are what the battery is testing. D
   currently supplies the only demonstrated non myopic straight
   line mechanism among the four. The most promising composition
   suggested by this analysis: D like novelty retention for the
   base, B like semantic induction for composition, C like
   splitting (with repaired repair) for piecewise structure.

## 6. Kill bars

- K1: PASS. A's flaw analyzed for B/C/D impact (sections 1-3).
- K2: PASS. Survival predictions with reasoning (section 4).
- K3: PASS. Success requirements specified (section 5).

## 7. Governance

Analysis only; no implementation, no binaries. No Python used or
invoked. No em dashes in this document (byte verified before
commit). Committed local only, owned path
`docs/lab/research-lead/overnight-20260928/discovery_implic/`,
with pathspec commit. Prereg discipline not applicable (analysis,
not experiment); no thresholds frozen or weakened.
