# PREREG: LIFETIME-AB-1 (LT1) -- one persistent learner across eight sequential worlds

Branch: `p1/lifetime-ab`
Frozen core: `cogops_learnosc2/c8_learn.zag` (1331 lines, sha256[:12] `750cb01d086f`)
Base arena: `cogops_rescueaware/c15_base.zag` (174 lines)
Contract module: `hook_phase1/hq_module.zag` (326 lines)
Binary 1: `lt1` (lifetime + baselines + ablations + TTC)
Binary 2: `lt2` (harder second lifetime, charter 221)

Committed ALONE, before any implementation file exists.

## 0. The question

Does TNN become MORE INTELLIGENT with age, or only larger / slower / more
cluttered? Specifically: given ONE learner instance, never reset, driven
through ONE generic interface, with no task labels and no answer feedback,
across eight sequential stages A..H:

- does accumulated structure make a LATER, UNSEEN goal solvable that a
  fresh learner at the same goal cannot solve (intelligence), as opposed
  to merely cheaper (size/cost), or worse (interference)?
- does structure from A get reused at F **unprompted**?
- does the structure assembled at F become reusable again at G (reuse of
  reuse)?
- what does a lifetime COST: memory, retrieval, interference?

The preregistered answer is allowed to be "no positive transfer". Bars are
frozen below; a failed bar is reported as a failed bar.

## 1. Hard constraints and how they are enforced

| Constraint | Enforcement |
|---|---|
| ONE learner instance, one process, no recompilation between stages | one `L` (frozen learner state, 16384 B) + one `LT` (additive lifetime block) allocated once in `main`, threaded unchanged through all 8 stages and all sub-phases that clone it |
| NO TASK LABELS | the learner is never passed a stage id, a stage name, a goal tag from another stage, a reuse hint, or a correctness flag. Audited by NAMECHECK grep + by the fact that `lt_episode` and `lt_query` are the ONLY two entry points and their signatures contain no stage selector |
| NO ANSWER FEEDBACK (stricter than asked) | the learner never receives judgment/consequence. All learner-side detection is from its own observation stream (episode facts + arena size). Consequence: the learner cannot know whether an answer is right; every correctness number below is evaluator-only |
| SAME generic interface for every stage | `lt_episode(L,LT,A,kind,p1,p2,p3)` and `lt_query(L,LT,A,G,K)`. `kind` is a MODALITY channel (retrieve / verify / count) inherited from the frozen core's own `ret_episode` / `vfy_episode` / `cnt_episode` split. Modality is not task identity: no stage, world, or goal is selectable through it |
| Pure Zag | all worlds, goals, oracles, statistics and verdicts are Zag. Shell only for concatenation + `tools/zbuild.sh` |
| New claim IDs | C500-C5xx only. C377-C466 never minted |

## 2. Substrate, and what is frozen vs additive

FROZEN (concatenated byte-identical, never edited):
- `z_alloc`, `get32`, `set32`, `o_app`, `o_i64`, `o_nl`, `o_flush`
- `ret_gen` (id 0), `vfy_gen` (id 1), `cnt_gen` (id 4) -- researcher-supplied
  generic procedures, verbatim
- all 1331 lines of `c8_learn.zag`: `specialize_ret/vfy/cnt`, `ret_spec`,
  `vfy_spec`, `cnt_spec`, `ret_episode/vfy_episode/cnt_episode`,
  `ret_version/vfy_version/cnt_version`, `g_tag/g_nneeds/need_tag/need_nf/
  need_f/g_linkbase/g_nlinks/link_w`, `mat_inputs`, `topo`, `topo_g`,
  `fanin_src`, `apply_kind1`, `apply_kind1_g`, `apply_kind3`, `bind_*`,
  `try_family`, `learn_bindings`, `plan_find/plan_new/plan_drop`,
  `clear_plans`, `clear_bindings`, `ans_append*`, `w_to_chain`,
  `execute_plan`, `execute_plan_iter`, `exec_step_iter`, `compose`,
  `compose_iter`, `snap_out`, `out_eq_snap`, `traj_*`, `outc_*`,
  `osc_*`, `osc_handle`

CONTRACT MODULE (`hq_module.zag`) is concatenated and linked, and a
`CONTRACT-SELFTEST` line proves it executes. It is deliberately NOT on the
learner's decision path: every entry point that changes belief
(`u_invalidate(judgment, consequence)`, `u_revise`) requires a ground-truth
consequence. Calling them inside the learner would inject answer
feedback and violate Section 1. Documented as an exclusion, not an
oversight.

ADDITIVE (this lane, new file, no frozen function modified):
- `lt_add` (arena append, capacity 512 facts instead of 128; same layout)
- `lt_sig_need`, `lt_sig_goal` -- purely DESCRIPTIVE signatures
- `lt_bind_store`, `lt_tmpl_store`, `lt_conn_store`, `lt_fun_store`
- `lt_ensure_fresh` -- self-maintenance on observed arena growth
- `lt_note_ep` -- modality dispatch + functional-arity observation
- `lt_query` -- the single query entry point
- oracles, baselines, ablation switches, TTC harness, statistics

### 2.1 The signature (the only new learner-owned "representation")

`lt_sig_need(G,ni) = nf * 7 + 13 * (#incoming kind-1 links) + 29 *
(#incoming kind-2 links) + 61 * (#incoming kind-3 links)`.

`lt_sig_goal(G)` = the ordered tuple of `lt_sig_need` over needs in INDEX
order, folded by `h = h*131 + (sig + 1)`.

The signature contains NO family information, NO relation identity, NO
need tag, NO world identity. It is a description of the need's arity and
of the link structure pointing at it. Which procedure family a need gets
is still decided by the frozen `try_family` trial, unchanged.

This is the weakest signature that could possibly support any transfer at
all. That is deliberate: it makes a POSITIVE result hard to explain by
representation engineering, and makes the predicted over-generalization
(Section 6, P6) likely rather than unlikely.

### 2.2 Why tag canonicalization is not leakage

The frozen BIND table is keyed by an arbitrary harness-chosen integer
(`need_tag`) that appears nowhere in the need's structure. Two needs with
identical structure but different tags get different bindings and the
learner re-runs the family trial. `lt_tmpl_store` records, per template
signature, the canonical tag set used the FIRST time that signature
occurred, and rewrites a later goal's need tags to those canonical values
in a shadow copy `GC`. The frozen `learn_bindings` then finds the binding
already present and skips the trial. The rewrite copies only tags; every
field, link and relation travels unchanged from the caller's goal record.
This is memoization of a pure function (shape -> family), which is why
Section 6 predicts over-generalization, not improved discrimination.

## 3. The world (harness side; ALL literals live in `lt_world.zag`)

Arena `A` is APPEND-ONLY, capacity 512 facts, layout `[nf, (s,r,o) x nf]`
(12 B per fact) so `ret_gen/vfy_gen/cnt_gen` read it unmodified.

Stage totals: A 52, B 27, C 28, D 39, E 200, F 15, G 27, H 28 = 416 facts.

- **A unfamiliar procedural world.** rels 101,102,103,105,106,107 (+decoy
  104). Subjects 10..17. Two shared-object procedure properties (105, 106)
  and a two-valued relation (107).
- **B causal world.** rels 201..208. Subjects 110..115. rel 201 is
  observed FUNCTIONAL at B (exactly one object per subject).
- **C formal constraint world.** rels 301..304. Subjects 30..37.
- **D misleading evidence.** rels 108..112. Subjects 200..207. A structural
  MIRROR of stage A under fresh relation ids, appended long after A, so a
  recency/memorizing baseline reads the mirror and a memorizing-by-(rel,obj)
  baseline cannot tell A from D.
- **E long unrelated distractor period.** rels 501..510, 20 facts each,
  200 facts, subjects 900+, never queried by any goal.
- **F A+C composition.** Appends rel 302 onto A's subjects and new rel 305
  onto A's subjects. The goal needs A's 2-step procedure shape AND C's
  1-step constraint shape over the SAME subject population, intersected.
- **G revision contradicting B.** Appends `(113,201,121)`, which violates
  the functional-arity of rel 201 that stage B exhibited. Plus rels
  601..604 on subjects 40..47.
- **H invention pressure.** rels 701..704 on subjects 50..56. The goal has
  the F-era template shape but its last need carries `aggop = 2`, which
  NO frozen family accepts. Correct behaviour is DECLINE.

Stage goals (tags are harness ids and never reach the learner except as the
opaque number inside the goal record):

| stage | tag | template | needs (nf, incoming links) |
|---|---|---|---|
| A | 9001 | T1 | (2,-), (7, k2), (3, k3) |
| B | 9002 | T2 | (2,-), (7, k2) |
| C | 9003 | T3 | (2,-), (4, k2), (3, k3) |
| D | 9004 | T1 | (2,-), (7, k2), (3, k3) |
| E | -- | -- | no goal (retention probe only) |
| F | 9005 | T4 | (2,-), (7, k2), (4, k2), (3, k3 x2) |
| G | 9006 | T4 | (2,-), (7, k2), (4, k2), (3, k3 x2) |
| H | 9007 | T4-shape, aggop=2 | (2,-), (7, k2), (4, k2), (3, k3 x2) |

T4 is the A+C composition: `nf=7` VERIFY and `nf=2` RETRIEVE and `nf=3`
COUNT were all instantiated at A; `nf=4` VERIFY was instantiated at C.
T1 is re-used at D on disjoint relation ids. T4 is re-used at G on
disjoint relation ids, then re-used at H.

### 3.1 Evaluator-declared correct answers

```
GA  [8,10,11,12,13,14,15,16,17, 5,10,11,12,13,14, 1,2]                     n=18
GB  [6,110,111,112,113,114,115, 3,110,111,112]                            n=11
GC  [8,30,31,32,33,34,35,36,37, 8,30,31,32,33,34,35,36,37, 1,2]           n=19
GD  [8,200,201,202,203,204,205,206,207, 5,200,201,202,203,204, 1,2]        n=18
GF  [8,10,11,12,13,14,15,16,17, 5,10,11,12,13,14, 7,10,11,12,13,14,15,16, 1,2]   n=25
GG  [8,40,41,42,43,44,45,46,47, 5,40,41,42,43,44, 7,40,41,42,43,44,45,46, 1,2]   n=25
HG  DECLINE (no family accepts nf=3 with aggop=2)
GA-retention-probe  identical to GA
```

An independent oracle (`lt_oracle`, fresh local state, `ret_gen/vfy_gen/
cnt_gen` over the live arena, hand-rolled fixed-point walk, no learner
state at all) recomputes every one of these from the arena at query time.
Correctness = `ans_eq(learner, oracle) AND oracle == declared`. A
`CONTRACT-ORACLE` line asserts oracle == declared for all seven goals; if
that assertion fails the whole run is VOID.

## 4. Phases (all inside ONE process, one binary)

1. **MAIN** -- the mission. One `L`, one `LT`. For stages A..H in order:
   append facts, feed episodes, then `lt_query` the stage goal. Log per
   query: outcome (correct / wrong / declined), family trials consumed,
   fact-checks consumed (`K`), passes, template hit or miss, template
   origin query index, connection fires, revisions, memory occupancy.
   At H, additionally re-query GA as a retention probe.
2. **FRESH0** -- fresh learner, zero episodes, given GF directly.
3. **FRESH1** -- fresh learner, given F's episodes only, then GF.
4. **RECENCY** -- 16-fact sliding window, GF. The stupid memorization
   baseline (charter 79).
5. **ABL-SNAP** -- clone the MAIN state at end of F, disable
   `lt_ensure_fresh`, re-query GF. Tests whether the accumulated snapshot
   is causally load-bearing for F's CORRECTNESS.
6. **ABL-STRUCT** -- clone the MAIN state at end of F, clear
   `lt_tmpl_store` and `lt_bind_store`, re-query GF. Tests whether the
   reused structure is causally load-bearing for F's COST.
7. **ABL-CAP** -- clone the MAIN state at end of F, refill BIND to capacity
   with throwaway tags so `bind_new` must fail, re-query GF. Tests the
   capacity-interference prediction.
8. **TTC** -- for each stage, from a clone of the state at the end of stage
   s-1, feed stage s's episodes ONE AT A TIME; after each, probe the stage
   goal on a further clone. TTC_s = index of the first correct probe
   (or -1). Probes use cloned state so the MAIN lifetime is not advanced.
9. **HARD (charter 221)** -- separate binary `lt2`: relabelled and
   HARDER second lifetime (see Section 8).

## 5. Metrics (all emitted as one buffered flush)

Memory growth: nonzero-i32-cell count in `L` and in `LT` per stage.
Retrieval cost: `K` delta per query and cumulative; spec-version uses vs
gen-version uses from the frozen counters.
Positive transfer: MAIN vs FRESH0/FRESH1 at F, on (a) correct/incorrect,
(b) trials, (c) fact-checks.
Negative transfer: MAIN vs FRESH at ANY stage; magnitude in trials,
fact-checks, and correctness flips. Reported per stage, not summarized.
Spontaneous reuse: per query, `tmpl_hit` and `origin_q`; a hit whose
origin is more than one stage old, with disjoint relation ids, is
classified `REUSE-XWORLD`.
Reuse of reuse (charter 25): a template first BUILT at F that later FIRES
at G and/or H. Counted separately from A-origin reuse.
Belief changes: `fun_viol` (observed functional-arity violations),
`n_revise` (self-triggered snapshot rebuilds), plan-drop events,
bind-eviction events.
TTC: Section 4 phase 8.
Learning cost: fact-checks consumed by episodes, per stage.
Forgetting: retention probe result at H; plus per-stage re-query of that
stage's own goal to detect self-decay.
Computational cost trajectory: cumulative fact-checks, monotonic by
construction and reported per stage.
Learner-created abstractions: distinct template signatures created.
Learner-created procedures: templates built (`plans_built` delta) and the
shape-memoization entries serving later queries (`bind_hit`).

## 6. FROZEN PREDICTIONS

- **P1** determinism 3/3 byte-identical.
- **P2** MAIN at stage A builds T1 and answers GA correctly.
- **P3** MAIN at F: template T4 is a MISS (new shape) but 3 of 4 need
  shapes are HITS, so the per-query trial increment at F is exactly 3.
  FRESH1 at F: trial increment exactly 12.
- **P4** MAIN at D: T1 HITS (3-stage gap, disjoint relation ids) ->
  `REUSE-XWORLD`, answer correct.
- **P5** MAIN at G: T4 HITS -> the template ASSEMBLED AT F fires again on
  disjoint relation ids. `REUSE-OF-REUSE` = 1. Answer correct.
- **P6** MAIN at H: does NOT decline (T4-shape template hit, mis-binds the
  aggop=2 need to COUNT) while FRESH0 at H DOES decline. `MISBIND` = 1.
  The correct answer at H is DECLINE.
- **P7** ABL-SNAP: GF's answer becomes WRONG (`ABL_SNAP_WRONG` = 1).
  Without refresh, the accumulated snapshot silently under-counts,
  because the arena is append-only and new facts never enter the buckets.
- **P8** ABL-STRUCT: GF's per-query trial increment rises from 3 to 12
  (`ABL_STRUCT_TRIALS` = 12) while the answer stays correct.
- **P9** RECENCY at F is WRONG. FRESH0 and FRESH1 at F are CORRECT.
- **P10** exactly 1 functional-arity violation is detected, at stage G,
  on rel 201, unprompted, before G's goal is queried.
- **P11** RET coverage saturates at 16 during stage E; consequently the
  goal at G uses the GEN version for its retrieve step
  (`ret_spec_uses` delta at G = 0, `ret_gen_uses` delta at G >= 1) while
  remaining CORRECT. Cost-side-only negative transfer.
- **P12** memory occupancy in L and LT is non-decreasing across stages.
- **P13** the GA retention probe at H is CORRECT despite 200 distractors
  and a contradiction. `FORGET` = 0.

## 7. FROZEN KILL BARS

- **K1 (integrity)** determinism 3/3 byte-identical, else VOID.
- **K2 (integrity)** `CONTRACT-ORACLE` assertion passes for all 7 goals,
  else VOID.
- **K3 (integrity)** NAMECHECK clean: no stage id, stage name, reuse
  hint, cross-stage goal tag, or correctness signal reaches the learner
  through `lt_episode` / `lt_query`; no frozen function is modified.
  Else VOID.
- **K4 (transfer)** MAIN beats FRESH0 and FRESH1 at F on at least one of
  {trials, fact-checks}. If it beats NEITHER, the positive-transfer claim
  is **KILLED** and only the "larger/slower/cluttered" reading survives.
  Not a void; a reportable negative.
- **K5 (causality of reuse)** ABL-STRUCT must move a measured quantity at
  F (trials or fact-checks). If nothing moves, the "reuse" is cosmetic and
  the reuse claim is **KILLED**.
- **K6 (causality of memory)** ABL-SNAP must make GF's answer WRONG. If
  GF's answer is unchanged, the accumulated snapshot is NOT causally
  load-bearing, the intelligence reading is **KILLED**, and only a
  cost reading may be claimed.
- **K7 (discriminative validity)** at least one of {P6 misbind, P7
  staleness, P11 saturation, P9 recency-failure, P10 violation} must
  fire. If none fires the apparatus is judged non-discriminative and the
  whole run is VOID.

VERDICT mapping, frozen:
`LIFETIME-INTELLIGENCE` requires K1,K2,K3,K6 AND K4 AND K5 AND at least
one of {P4,P5} true.
`LIFETIME-COST-ONLY` if K1,K2,K3 hold, K4 holds but K6 fails.
`LIFETIME-NO-ADVANTAGE` if K4 fails.
`VOID` if K1,K2,K3 or K7 fails.
In every case P6, P7, P9, P10, P11 are reported as found, and a positive
`MISBIND` or `ABL_SNAP_WRONG` is reported as a NEGATIVE-transfer result
even in the `LIFETIME-INTELLIGENCE` case.

## 8. Harder second lifetime (charter 221), binary `lt2`

Automatically produced after LT1. Harder on all five axes, not merely
relabelled:

1. 12 subjects per stage instead of 8.
2. 6 templates instead of 4 (exceeds the frozen 4-slot PLAN table).
3. 6 need signatures (exceeds the frozen 8-slot BIND table only when
   combined with reuse churn), and 9 frozen-tags BIND pressure.
4. 400 distractor facts instead of 200 (exceeds the frozen 16-relation
   coverage sets by a wider margin).
5. One extra need in the composition goal (4 -> still 4; instead a second
   fan-in diamond: 4 needs, 6 links).
6. Revision at G that contradicts B's rule in TWO places, so the
   functional-arity detector fires at least twice.

Preregistered LT2 predictions: LT2 (durable template store + LRU
eviction) reaches a HIGHER share of correct answers and LOWER total
fact-checks than LT1 at the same goal set, and LT1 degrades at the stage
where its 4-slot PLAN table saturates. Reported even if LT2 fails.

## 9. Boundaries this experiment cannot cross (stated before running)

- The procedure families RETRIEVE / VERIFY / COUNT are researcher-frozen
  templates (C397: "the learner did not invent the WRAP/SEQUENCE
  strategies"). Nothing here clears the L3 bar. The learner-created
  objects are: descriptive shape classes, a shape->tag memo, reusable plan
  templates, and a snapshot-freshness rule.
- `try_family` decides family from SHAPE ALONE; it never consults the
  arena. `learn_bindings` is therefore memoization of a TOTAL function of
  the need's field shape, and no experience enters it. Any "learning"
  credit for bindings is reported as memoization, and Section 6 P6 is the
  predicted price.
- CORRECTNESS IMPROVEMENT WITH AGE is only possible here through snapshot
  refresh. If K6 fails, the honest claim is "faster", not "smarter".
- The world is a finite append-only triple store. There is no perception,
  no noise, no concept drift, no social input.
- One lifetime, one arena, one population of subjects. Nothing licenses
  generalization past these 8 stages.