# CORE-FREEZE-1/2/3 PREREG (charters 59, 60, 216; 61, 62, 63)

Lane: `corefreeze/`. Prereg frozen BEFORE any implementation exists.
Frozen core, hashed, NOT MODIFIED by this lane:

| file | lines | sha256 |
|---|---|---|
| `cogops_learnosc2/c8_learn.zag` | 1331 | `750cb01d086f0f4eeb29d0a8481e36941a7551396e5c514429a0dffc7aa4b4e8` |
| `cogops_rescueaware/c15_base.zag` | 174 | `fc1f6e73c43ae8e4ea2b7af50f1606cc4b6c5353992bd5d4411cb4c9a3b73e61` |
| `hook_phase1/hq_module.zag` | 326 | `4200e21fea5fa75d774f8f9785637d2305eccfa3d9b8486f27b7ac287b10b30d` |

All three hashes are re-verified at the end of the wave; a change in any of
them voids the wave.

## 0. HYPOTHESIS

H1. The frozen core is a *goal-record interpreter*. Its entire generic
interface is `compose_iter(L,A,G,K,ans,vbuf)` (plus `osc_handle`, plus the
three episode entry points). It contains zero goal tags, zero need tags, zero
relation ids, zero world literals. Therefore, if a new capability can be
expressed as (a) a fact table and (b) a goal record, it is obtainable with
ZERO cognition-source change.

H2. The corollary is the actual danger and the actual thing to measure:
because the goal record carries the *structure* (needs, arities, link kinds,
wiring), most "new capabilities" obtained this way are **re-encodings authored
by the researcher**, not capabilities acquired by the learner. H2 predicts a
LOW Tier-A count (capability from learner state alone, same goal record).

H3. The frozen core is *competence-insensitive* to learner state: with zero
episodes and zero plans, competence is identical, and only COST (fact checks)
and REUSE (plan loads, stored oscillation responses) change.

## 1. FROZEN ARCHITECTURE, AS READ (this is the accounting basis)

From `c8_learn.zag`:

* Learner state `L` = 16384 bytes: three coverage tables (RET/VFY/CNT, 16
  relations each, 64 fact-index buckets each), a BIND table (8 slots,
  `[need_tag, family]`), a PLAN table (4 slots, 56 bytes: goal_tag, nneeds,
  then per step `[need_index, need_tag, family]`), a stats block at 13224, a
  TRAJ region at 13300 (8 passes x 4 needs x 9 cells) and an OUTC region at
  14500 (3 entries x 464 bytes).
* Seed procedures (in `c15_base.zag`): `ret_gen` id 0, `vfy_gen` id 1,
  `cnt_gen` id 4. All are linear scans over the whole fact arena.
* Episodes: `ret_episode`, `vfy_episode`, `cnt_episode` log relation ids into
  the coverage tables. They do NOT build an index.
* Specialization: `specialize_ret/vfy/cnt` build per-relation fact-index
  buckets from the CURRENT arena.
* Version selection per step, from coverage only: `ret_version` in {0,2},
  `vfy_version` in {1,3} (3 iff every relation in the chain is covered),
  `cnt_version` in {4,5}. No mode flags.
* `learn_bindings` assigns each unseen need tag to a family by trying all
  three and accepting the first that fits the need's shape, then never
  retried (the binding is permanent).
* `topo_g` = Kahn with stall fallback. `apply_kind1_g` = scalar copy from a
  non-empty source. `apply_kind3` = concatenate ALL incoming kind-3 source
  output lists in link order into one subject list.
* `execute_plan_iter` = change-driven iteration, all needs start dirty,
  successors of a changed need re-dirty, halts on quiescence or a 16-pass
  cap. `vbuf[20]` = passes used.
* `osc_handle` = up to 6 passes of `osc_one_pass`; nearest-first recurrence
  scan (`osc_review`) over trajectory snapshots; lag 1 -> how=0; lag in 2..3
  confirmed by one more pass -> `outc_store` and how=1; on a later
  presentation, replay check over 2 passes -> how=2.

HARD ARCHITECTURAL BOUNDS discovered by reading (to be reported, not fixed):
BOUND-1 the PLAN table has **4 slots**. `plan_new` returns -1 when full and
`execute_plan` then reads `L+12948`, i.e. OUT OF RANGE. So a lifetime may
hold at most 4 distinct goal tags that reach `plan_new`.
BOUND-2 the BIND table has **8 slots**; `bind_new` returns -1 when full and
`bind_find(-1)` then makes `learn_bindings` return 0 (a spurious decline).
BOUND-3 coverage tables hold 16 relations each, 64 buckets each.
BOUND-4 `ret_spec/vfy_spec/cnt_spec` read the arena THROUGH the bucket, so a
stale index after an arena rebuild returns a STALE ANSWER. There is no
staleness check and no contradiction trigger anywhere in the core.
BOUND-5 `plan_find` keys on goal tag only. A goal presented under an existing
tag is executed with the STORED plan (stored nneeds, stored step indices,
stored families) and the NEW goal record's fields and links. A shape change
under a live tag is therefore silently executed with the old plan.
BOUND-6 `clear_plans` is the only in-core way to release plan slots.

The battery is DESIGNED to respect BOUND-1/2/3 (exactly 4 goal tags and 4
need tags per lifetime) so that BOUND-1/2 never fire as confounds. They are
reported as bounds, not tested.

## 2. THE DRIVER ARCHITECTURE (this is the experimental control)

FOUR FILES. Concatenation order is `cf_base.zag`, `cf_data.zag`,
`cf_engine.zag`, then the three frozen files.

* `cf_base.zag`: `z_alloc`, `get32`, `set32`, `world_new`, `fact_add`,
  `chain_*`, `ret_gen`, `vfy_gen`, `cnt_gen`, `o_app`, `o_i64`, `o_nl`,
  `o_flush`. This file MUST be byte-identical to `c15_base.zag` except for
  the single `o_flush` body, which is replaced by `_zag_print(b[0..c])`
  because `_zag_raw_syscall` is INERT on this host (brief section 4.0/4.1).
  The substitution is diffed and reported.
* `cf_data.zag`: DATA ONLY. Fact tables, episode tables, goal-record byte
  tables, and expected-answer tables. World identifiers, relation
  identifiers, goal tags, need tags, and every expected value live here.
* `cf_engine.zag`: the GENERIC ENGINE. One `main`. It contains NO world
  identifier, NO relation identifier, NO goal tag, and NO need tag. It
  contains exactly one dispatch, on the episode `kind` field, over the three
  seed families the core itself defines. Everything else is a table walk.
* `c8_learn.zag`: byte-identical frozen cognition, hash-verified at build.
* `c15_base.zag`: NOT concatenated (its `o_flush` would collide with
  `cf_base.zag`'s). Proven equal to `cf_base.zag` modulo the one-line output
  substitution by `diff`.
* `hq_module.zag`: byte-identical frozen, concatenated unchanged, NOT CALLED.
  It contributes zero capability and is carried only so its hash is exercised.

K-A (architecture kill bar): `cf_engine.zag` contains zero occurrences of any
world relation id, goal tag, or need tag. Enforced by a grep audit at the
end of the wave and reported. Any occurrence = the driver has task-specific
logic and no CF claim in this wave counts.

## 3. FROZEN FACTS AND GOALS (all identifiers opaque; insertion order is
significant because `ret_gen` returns subjects in arena order)

### W1 ALPHA, 19 facts
```
(101,11,111) (102,11,111) (103,11,111)
(101,12,121) (104,12,121)
(101,13,131) (105,13,131) (106,13,131) (107,13,131)
(111,17,181) (121,19,191) (111,19,192)
(201,14,200) (200,14,201) (201,15,200) (200,15,200)
(109,20,220) (109,20,109) (109,15,109)
```
W1 episodes, in order: ret (11,111); ret (12,121); ret (14,200);
ret (20,220); vfy [(101,12,121)]; vfy [(201,15,200),(200,15,200)];
vfy [(109,15,109)]; cnt (11,101).
Then `specialize_ret(0,7)`, `specialize_vfy(0,7)`, `specialize_cnt(0,7)`.
Coverage after W1: RET nrel 4 {11,12,14,20}; VFY nrel 3 {12,15};
CNT nrel 1 {11}. Relations 13, 17, 19 have facts but NO coverage.

W1 goals (goal tags 7001..7004, need tags 901 RETRIEVE / 902 VERIFY /
903 COUNT):

* G7001 = 1 need: 901, nf 2, [11,111]. Expected answer `3 101 102 103`,
  versions `[2]`.
* G7002 = diamond, 3 needs: 901 nf 2 [11,111]; 902 nf 7
  [2, 0,12,121, 0,13,131]; 903 nf 3 [11,1,0]; links kind2 (dst1,src0),
  kind3 (dst2,src0). Expected `3 101 102 103 1 101 1 1`, versions `[2,1,5]`.
* G7003 = multi-source fan-in, 3 needs: 901 nf 2 [12,121]; 901 nf 2
  [12,121]; 903 nf 3 [13,1,0]; links kind3 (dst2,src0), kind3 (dst2,src1).
  Expected `2 101 104 2 101 104 1 1`, versions `[2,2,4]`.
* G7004 = self-walk + fan-out VERIFY, 3 needs: 901 nf 2 [11,111] (carrier);
  901 nf 2 [14,200] with kind1 SELF link (src out slot0 -> dst field1);
  902 nf 4 [1,0,15,200] with kind2 from need1. Under `osc_handle` this is
  expected how=1 (invented), lag 2.
* G7004c = same shape, convergent field values: need0 901 nf 2 [20,220];
  self kind1; need1 902 nf 4 [1,0,15,109] kind2 from need1. Expected
  how=0 (converges, no oscillation) and answer `1 109 1 109`, versions
  `[2,3]`.
* G7001u = G7001 shape on an uncovered relation that HAS facts:
  901 nf 2 [13,131]. Expected `4 101 105 106 107`, versions `[0]` (generic
  fallback). This is the specialization-coverage boundary.
* G7003w = G7003 shape on W1: need0 901 nf 2 [11,111]; need1 901 nf 2
  [12,121]; need2 903 nf 3 [13,1,0]. Expected
  `3 101 102 103 2 101 104 1 1`, versions `[2,2,4]`.
* G9999 = DECLINE probe, 1 need: need tag 904 (never bound elsewhere),
  nf 5, [5,1,1,1,1]. Family 0 refuses (nf!=2), family 1 refuses
  (nf != 1+ns*3 with ns=5), family 2 refuses (nf!=3). Expected
  `compose_iter` return 0, declines +1, and NO plan slot consumed.

### W2 BETA, 9 facts. Different identifier range entirely.
```
(9001,9001,9101) (9002,9001,9101)
(9001,9002,9201) (9003,9002,9201)
(9001,9003,9301) (9004,9003,9301) (9005,9003,9301)
(9101,9004,9401)
(9101,9005,9501) (9102,9005,9502)
```
W2 episodes: ret (9001,9101); ret (9002,9201); ret (9003,9301);
vfy [(9001,9002,9201)]; cnt (9001,9001). Coverage: RET nrel 3
{9001,9002,9003}; VFY {9002}; CNT {9001}. Relations 9004 and 9005 have facts
and NO coverage.

W2 goals, ALL under goal tags already holding a plan from W1 (BOUND-5 reuse):

* G7001@W2 fields [9001,9101]. Expected `2 9001 9002`, versions `[2]`.
* G7001@W2u fields [9005,9501] (uncovered). Expected `1 9101`,
  versions `[0]`.
* G7002@W2 fields [9001,9101] / [2,0,9002,9201, 0,9004,9401] /
  [9001,1,0]. Expected `2 9001 9002 0 1 1`, versions `[2,1,5]`.
* G7003@W2: need0 [9002,9201]; need1 [9003,9301]; need2 [9004,1,0] with
  two kind3 links. Expected `2 9001 9003 3 9001 9004 9005 1 1`,
  versions `[2,2,0]->v4` i.e. `[2,2,4]` (9004 uncovered for CNT).
* G7004@W2: need0 901 [9001,9101]; need1 901 [9003,9301] self kind1;
  need2 902 nf 4 [1,0,9004,9401] kind2 from need1. The self-walk starts
  from a 3-subject output, takes slot 0 = 9001, then (9003,9001) is empty,
  so it halts empty. Expected how=0, answer `3 9001 9004 9005 0 0`,
  versions `[2,2,1]`.

### W3 GAMMA, 16 facts. An unfamiliar formal system (a term-rewriting /
congruence system with type and grade annotations) AND a causal cascade
world, together.
```
(1,5001,2) (3,5001,3) (2,5001,3)
(1,5002,0) (2,5002,0) (3,5002,0)
(1,5003,0) (2,5003,1) (3,5003,1)
(7001,6001,7101) (7101,6001,7201) (7201,6001,7301)
(7001,6002,7401) (7201,6002,7401)
(8001,6003,8101)
```
Note `(3,5001,3)` is inserted BEFORE `(2,5001,3)`, so `ret_gen(5001,3)`
returns `[3,2]` and the self-walk slot-0 fixes on 3. This ordering is
frozen and load-bearing.

W3 episodes: ret (5001,2); ret (5001,3); ret (6001,7101); ret (6002,7401);
vfy [(1,5002,0),(1,5003,0)]; cnt (5001,1). Coverage: RET nrel 4
{5001,6001,6002}; VFY {5002}; CNT {5001}. Relations 5003, 6003 have facts
and NO coverage.

W3 goals:

* G7001@W3 fields [5001,2]. Expected `1 1`, versions `[2]`.
* G7001@W3u fields [6003,8101] (uncovered). Expected `1 8001`,
  versions `[0]`.
* G7002@W3 = rewrite maximality + typing + reduct union: need0 901 nf 2
  [5001,3] self kind1; need1 902 nf 7 [2,0,5002,0, 0,5003,1] kind2 from
  need0; need2 903 nf 3 [5001,1,0] kind3 from need0. Expected
  `2 3 2 2 3 2 1 1`, versions `[2,3,5]`.
* G7003@W3 = causal blast-radius union: need0 901 [6001,7101];
  need1 901 [6001,7201]; need2 903 [6002,1,0] two kind3 links. Expected
  `1 7201 1 7301 1 1`, versions `[2,2,5]`.
* G7004@W3 = converging rewrite walk: need0 901 [5001,3] self kind1;
  need1 902 nf 4 [1,0,5002,0] kind2 from need1. Expected how=0, answer
  `2 3 2 2 3 2`, versions `[2,3]`.

## 4. BATTERIES

### CF1 (B1, W1) capabilities the core already supports
CF1-a 1-step projection, generic interface, no goal-specific driver logic.
CF1-b conjunct chain verification (fan-out + 2-step chain).
CF1-c union cardinality over a retrieved subject set.
CF1-d diamond with per-step version selection including a generic fallback
      (relation 13 has facts, no coverage) in the SAME goal as two
      specialized steps.
CF1-e multi-source kind-3 fan-in (TWO incoming kind-3 links into one COUNT);
      no goal with this shape exists anywhere in the frozen c8 lane.
CF1-f oscillation: the learner detects a 2-cycle from its OWN trajectory and
      invents a response (how=1).
CF1-g convergent control: same shape, no oscillation (how=0).
CF1-h honest decline on an unbindable need shape.

### CF2 (B1, W2) a domain never seen, still frozen, still driver-only
CF2-a a plan built in W1 from W1 relations executed in W2 with W2 relations
      and W2 identifiers, at ZERO binding trials and ZERO new plans.
CF2-b an uncovered relation that has facts, in a brand-new namespace,
      correctly answered by the generic seed.
CF2-c the multi-source fan-in reused in the new namespace.
CF2-d a self-walk that halts empty, in the new namespace.
Kills for CF2: any new binding trial after W1 (L[13232] must not change
between the W1 block and the W2 block), any new plan (L[13224] must stay at
4 for the whole lifetime), or any wrong answer.

### CF3 (B1, W3) unfamiliar formal system + causal world + long lifetime, all
in ONE frozen lifetime, no source change
CF3-a typed rewriting: the maximal rewrite set, filtered by type AND grade,
      plus the cardinality of the union of reducts.
CF3-b causal blast radius as the union cardinality over a multi-source
      subject list, in the same lifetime as CF1/CF2.
CF3-c generic fallback on an uncovered relation in a third namespace.
CF3-d the SAME oscillation entry point applied in W3, returning how=0.
Kills for CF3: any wrong answer, or any new binding trial, or any source
change.

### B2 STUPID BASELINES (charter 79) and the competence/cost decomposition
* BASE-FULL: B1 as preregistered.
* BASE-NOEP: identical world and goal tables, but the episode table is
  REPLACED BY AN EMPTY TABLE. No coverage, so no index, so every step runs a
  generic seed. Predicted: competence IDENTICAL to BASE-FULL; total fact
  checks STRICTLY HIGHER; ret_spec/vfy_spec/cnt_spec use counters all zero.
* BASE-FRESH: identical to BASE-FULL but L is zeroed at each world boundary
  (a fresh learner per world). Predicted: competence IDENTICAL; binding
  trials and plans REPEATED per world.
* BASE-NOEP-FRESH: both.
This battery is the load-bearing honesty control. If BASE-NOEP matches
BASE-FULL on competence then the frozen core's competence does NOT come from
learner state, and the report MUST say so.

### B3 CURRICULUM INDEPENDENCE (charter 62), four orders
Tasks, each its own world, each one goal:
* TA: facts (2001,31,3001),(2002,31,3001); tag 7001; 901 nf 2 [31,3001];
  episodes ret(31,3001). Expected `2 2001 2002`, version `[2]`.
* TB: facts (2003,32,3002),(2004,32,3003),(2004,33,3003),(2003,33,3003);
  tag 7002 diamond; episodes ret(32,3002), vfy[(2003,33,3003)],
  cnt(32,2003). Expected `1 2003 1 2003 1 1`, versions `[2,3,5]`.
* TC: facts (2005,34,3005),(2005,34,2005),(2005,35,2005); tag 7004
  self-walk + fan-out; episodes ret(34,3005), vfy[(2005,35,2005)].
  Expected `1 2005 1 2005`, versions `[2,3]`, how=0.
Orders: ABC, BCA, CAB, INTERLEAVED (A B A C B C). Fresh L per order.
Final competence per order = re-present all three tasks in order A, B, C
after the whole sequence and count exact answer matches (target 9/9).
Recorded per order: final competence, plans_built, plans_loaded, binding
trials, RET coverage nrel, total fact checks, osc handlings.
Reported, not barred: path dependence = spread of these across the four
orders. KILL BAR: any order with final competence < 9/9 is a CURRICULUM
FAIL and is reported as such. Also: any order where a task presented EARLY
later produces a WRONG answer is catastrophic interference and is reported.

### B4 ONE-SHOT / FEW-SHOT (charter 63)
World OS: (4001,41,5001),(4002,41,5002),(4003,42,5002).
Arms, each with a FRESH L:
* OS0: 0 episodes, query tag 7001 fields [41,5001]. Predicted version `[0]`,
  answer `1 4001`.
* OS1: exactly 1 ret episode on rel 41, `specialize_ret`, query. Predicted
  version `[2]`, answer `1 4001`. Measures one-shot storage, integration and
  immediate reuse.
* OS2: 2 ret episodes on rel 41. Predicted version `[2]`, answer `1 4001`,
  RET `rev` counter 2, RET coverage nrel 1. Measures whether a second
  example adds structure.
* OS1-LATER: OS1, then the query is repeated 3 more times. Predicted
  version `[2]` every time, identical answer, plans_loaded incrementing.
  Measures later reuse.
* OSR: OS1, then the ARENA IS REPLACED by a contradicting fact set
  (4009,41,5001) only, and the query is repeated WITHOUT re-specialization.
  Predicted: STALE WRONG ANSWER `2 4001 4002` (BOUND-4). This is the
  preregistered prediction that revision is NOT contradiction-triggered.
* OSR2: identical to OSR but `specialize_ret` is called again before the
  query. Predicted: `1 4009`, version `[2]`. Revision by re-derivation only.

B4 kills: OS1 must reach version 2 with a correct answer (one-shot storage).
OSR must return the stale answer (BOUND-4 confirmed) -- if OSR returns the
fresh answer, BOUND-4 is falsified and that is reported as a POSITIVE.
OSR2 must be correct. The report must explicitly separate "remembering one
fact" (OS1 stores the relation in coverage, i.e. one i32) from "generalising
from one example" (NOT claimed: the core's coverage table records a relation
id, not a concept; no new procedure family can be learned from one example
because `learn_bindings` retries all three families on EVERY unbound need
tag, so one example never reduces the family search space).

### B5 DEVELOPMENTAL LEARNING AND EARLY ABLATION (charter 61)
World DEV, 4 facts: (6001,51,7001),(6002,51,7002),(6003,51,7003),
(6001,52,7002).
* DEV stage 1: ret episodes (51,7001),(51,7002),(51,7003), then
  `specialize_ret`. Stage 2 goal: tag 7002 diamond, need0 901 [51,7001];
  need1 902 nf 7 [2,0,52,7002, 0,51,7002] kind2 from need0; need2 903
  [51,1,0] kind3 from need0. Predicted answer `1 6001 0 1 1`,
  versions `[2,1,4]`.
* DEV-ABL: identical, but immediately before stage 2 the RET coverage count
  `L[0]` is set to 0 (the ablation lesion: the learned RET index becomes
  find-invisible, exactly restoring a fresh run's RET state; every other
  region, including the BIND and PLAN tables, is untouched). Predicted
  answer `1 6001 0 1 1` IDENTICAL, versions `[0,1,4]`, fact checks
  STRICTLY HIGHER. Conclusion if confirmed: early learned structures are
  prerequisites for later EFFICIENCY, not for later COMPETENCE.
* DEV-NOEP: stage 1 skipped entirely. Predicted answer identical to DEV.
  This is the second, stronger developmental control: if the complex stage-2
  task is solved identically with no stage-1 experience at all, then stage-2
  competence is a SECRETLY INDEPENDENT mechanism with respect to stage-1
  state, and the report MUST say so.
* OSC-DEP: within B1's W1 block, present G7004 three times:
  1st expected how=1 (invented, outc_store ran);
  2nd expected how=2 (replayed from the stored outcome record);
  3rd, after zeroing ONLY `L[14500]` (the OUTC entry count, the c8 lane's own
  ablation lesion), expected how=1 again. This tests whether the learned
  artifact gates a capability.
B5 kills: DEV and DEV-ABL answers must be identical (else the ablation
leaked into competence and is reported as a POSITIVE dependency finding).
OSC-DEP must be how=1, how=2, how=1. If the 3rd is how=2 the lesion failed
and the wave is reported as instrument-invalid.

## 5. CORE-FREEZE ACCOUNTING, THREE TIERS (charter 216 headline)

For EVERY capability listed in section 4, the report MUST state one of:
* **TIER-A** zero source change AND zero new goal-record data: the same goal
  record, presented again, behaves differently because of learner state.
* **TIER-B** zero source change, but a new goal-record BYTE TABLE was needed.
  The plan topology is computed by the frozen core, but the goal record
  itself is researcher-authored data. This is re-encoding, not acquisition.
* **TIER-C** required driver code beyond the generic engine. Any TIER-C
  capability does NOT count as a core-freeze gain (charter 2/108).
The reported headline ratio is
  (count of TIER-A) / (lines of cognition source changed) = n / 0,
which is formally UNDEFINED, and the report must say so rather than call it
infinite. The load-bearing honest statement is: **the denominator is zero and
the Tier-A numerator is small, and the stupid baseline removes most of even
that.**

## 6. DETERMINISM, HYGIENE, AND PER-GENERATION KILL BARS

K0 INFRA (generation 0, must pass before anything else is believed):
 0a `tnn_pure_zag_report` prints `VERDICT: PURE-ZAG-CLEAN`.
 0b compile exit 0 with `--target macos-arm64`.
 0c 3/3 byte-identical stdout, sha256 recorded.
 0d stdout non-empty AND contains at least one `BAR` line.
 0e the three frozen files' sha256 equal section 0's values.
 0f `cf_engine.zag` grep audit: zero world relation ids, zero goal tags, zero
    need tags.
 0g zero em-dash and en-dash bytes anywhere in the lane.

K1 CF1: all W1 answers equal the frozen expectations; decline observed;
 oscillation how=1 observed; convergent how=0 observed.
K2 CF2: all W2 answers equal the frozen expectations; binding trials
 unchanged across the W1 -> W2 boundary; plans_built == 4 for the whole
 lifetime.
K3 CF3: all W3 answers equal the frozen expectations; binding trials
 unchanged across W1 -> W3.
K4 BASELINES: BASE-NOEP competence == BASE-FULL competence (if not, report).
K5 DEVELOPMENT: DEV == DEV-ABL == DEV-NOEP answers; OSC-DEP == 1,2,1.
K6 CURRICULUM: every order reaches 9/9 final competence.
K7 ONE-SHOT: OS0 version 0, OS1/OS2 version 2 correct, OS1-LATER stable,
 OSR stale-wrong, OSR2 correct.
Any generation failing: that level's claim is reported FAIL. NO BAR IS MOVED
AFTER SEEING RESULTS. If a frozen expectation turns out to be wrong the
expected value is reported as wrong and the observed value is reported; the
implementation is never edited to match the expectation, and the discrepancy
is analysed.

## 7. FALSIFIERS, STATED IN ADVANCE

* If `cf_engine.zag` needs a per-goal branch, H1 is FALSE for this core and
  the wave's CF claims are void.
* If any W2 or W3 answer requires a binding trial, the core's binding is not
  domain-general and CF2/CF3 are downgraded.
* If BASE-NOEP matches BASE-FULL on competence, "capability from learner
  state" is FALSE for this core and the report must lead with that.
* If DEV-NOEP equals DEV on competence, development creates NO prerequisite
  for competence and the report must lead with that.
* If any order of B3 scores below 9/9, the core is curriculum-fragile.
* If OSR returns the fresh answer, BOUND-4 is falsified (a genuine positive:
  the specialized path is self-validating).
