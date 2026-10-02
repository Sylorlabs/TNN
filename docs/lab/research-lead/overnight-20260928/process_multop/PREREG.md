# PREREG.md -- Multi-Op Process Selection (Constitution Priority F)

Worker: Multi-Op Process Selection Worker (Priority F).
Frozen: 2026-10-02, BEFORE any implementation. This file was committed
alone; implementation came after.

## 1. Mission

Constitution Priority F: learner-owned process selection for
MULTI-OPERATION sequences. Prior work proved: (1) unlabeled operation
selection works (19/19, sequences emerge from consequence history);
(2) cognitive ops as learner-owned structures work (applicability
revision, composition links, retirement; composition links shield
applicability); (3) logic-vs-predict: 0 predictions on exact knowledge,
state-driven dispatch. UNTESTED: sequences of 3+ operations where the
MIDDLE steps were never demonstrated as a pair.

Research questions:
- Q1: Can the learner discover a 3-operation chain A->B->C purely from
  consequence records, when NEITHER inner 2-op link (A->B, B->C) was
  ever directly rewarded? This tests true compositional
  generalization, not pair memorization.
- Q2: Can the learner revise an op's INTERNAL body parameter (not just
  select/reject the op) based on consequences?

## 2. Design (frozen)

One binary, `multop.zag`, pure Zag, deterministic (two LCG streams,
fixed seeds 123456789 / 987654321, fixed tie-breaks). Two experimental
arms share ALL learner machinery; they differ only in world
distribution and op count (experimental setup, not learner modes).

### 2.1 Learner machinery (identical in both arms)

- Ops are learner-owned byte-array instruction bodies executed by a
  fixed generic 8-instruction interpreter
  (SET/COPY/ADD/EQ/JNZ/MATCH/READF/YIELD). The interpreter never
  branches on op id. No OP_ constants as modes. No semantic cases.
- Learned tables, all written only by consequence updates:
  appl[o][ctx] (mean reward per observable context, 16 contexts),
  comp[p][o] (mean reward of o following p; written only when p was
  effective, i.e. non-failed), tot[o], retired[o].
- Selector: epsilon-greedy bandit over op indices.
  score = appl[o][ctx] + comp[prev][o] (prev valid only).
  Unseen (appl or comp) scores 500 (uniform optimism, no domain
  knowledge). Ties broken by least-tried, then lowest id.
  Epsilon schedule: (300*300)/(300+ep) per 1000. Max 4 steps/episode.
- Credit rule (generic): failed op records 0; op yielding a wrong
  answer records -1; any other op records +1 iff the episode is
  eventually solved, else 0. A non-terminal op is never punished for a
  later op's wrong answer.
- Retirement (generic): tot uses >= 15 and mean reward < -0.6.
- Observable context probe: edge existence from CUR only:
  ctx = hasV + 2*hasD + 4*hasS + 8*hasT (edge types 1..5 = V,D,R,S,T).
- Body parameter revision (generic rule): an op body may contain a
  numeric immediate operand whose offset is recorded in learner state
  at build time (param_off[o] >= 0). On a WRONG answer (rec = -1) by an
  op selected through the GREEDY path (not epsilon exploration),
  p[o] <- p[o] + sign(true_ans - ans_given), and the new value is
  written into the body bytes. Rationale, domain-neutral: parametric
  revision attributes error to miscalibration, which is licensed only
  for a committed (greedy) choice; exploration outcomes update
  selection tables only. No reference to any task, op, or constant.

### 2.2 Arm A: 3-operation compositional discovery (Q1)

Ops (4): 0 GATHER (answer V at CUR), 1 FOLLOW (move along D),
2 COMPLETE (answer V+R at CUR), 3 SHIFT (move along S).

Worlds, fresh per episode:
- F (30%): (Q)-[V]->v, true = v. GATHER solves.
- F2 (25%): (Q)-[D]->(E2), (E2)-[V]->v2, (E2)-[R]->k2,
  true = v2+k2. FOLLOW->COMPLETE solves.
- T2 (15%): (Q)-[S]->(E3), (E3)-[V]->v3, true = v3.
  SHIFT->GATHER solves.
- CHAIN3 (30%): (Q)-[D]->(E2), (E2)-[S]->(E4), (E4)-[V]->v4,
  (E4)-[R]->k4, (E4)-[T]->marker, true = v4+k4.
  Only FOLLOW->SHIFT->COMPLETE (op ids [1,3,2]) solves.

Applicability transfer built into the design: FOLLOW at D-contexts is
learned in F2, SHIFT at S-contexts in T2, COMPLETE at V+R-contexts in
F2; the E4 context (V+R+T marker, ctx 9) is unique to CHAIN3 so the
GATHER/COMPLETE ambiguity studied in prior work does not confound the
composition question. The two inner links (1->3) and (3->2) can only
be rewarded by the triple itself: (3,2) structurally so (SHIFT is
effective only where S edges exist, and COMPLETE can only solve
immediately after it in CHAIN3); (1,3) likewise except via a
solved non-triple episode, which the logging reports.

Discovery logging: every CHAIN3 episode records the emitted op
sequence, per-step greedy flags, and the comp sums/counts of (1,3)
and (3,2) BEFORE the episode's credit update. The discovery event is
the first episode in which [1,3,2] occurs as a consecutive
subsequence, all three selections greedy, episode solved.

### 2.3 Arm B: body parameter revision (Q2)

Ops (5): 0 GATHER, 1 FOLLOW, 2 COMPLETE, 3 SHIFT, 4 ADJUST.
ADJUST body: answer V at CUR plus a learner-owned immediate parameter
p4 (initial 0); param_off[4] recorded at build.

Worlds:
- F (50%): as above. GATHER solves.
- EST (50%): (Q)-[V]->v, (Q)-[T]->marker, true = v+4.
  ADJUST solves once p4 = 4. The constant 4 lives only in the
  environment; the learner never observes it except through signed
  wrong-answer errors.

Revision events are logged (episode, greedy flag). Only ADJUST has a
parameter cell.

### 2.4 What is NOT in the learner (anti-memorization)

- No innate composition links favoring any pair (uniform 500).
- No scripted or hardcoded 3-sequences anywhere in learner code.
  (The [1,3,2] check exists only in measurement code, as the F2 pair
  check did in prior work.)
- The environment defines CHAIN3 worlds (task setup, as F2/T2 worlds
  were task setup in prior work); the learner discovers the chain.

## 3. Frozen kill bars

500 episodes per arm. Late window: episodes 400..499.

- T1 (compositional discovery): a discovery event occurs (Arm A):
  [1,3,2] as consecutive subsequence, all three selections greedy,
  episode solved, AND pre-episode comp_sum(1,3) <= 0 AND
  comp_sum(3,2) <= 0 (neither inner link ever directly rewarded
  before discovery). Pair trial counts (n) are reported as context;
  the bar is on reward, per the research question.
- T2 (adoption): over late CHAIN3 episodes: success >= 75% AND
  [1,3,2] consecutive subsequence in >= 55% of them.
- T3 (body revision): p4 == 4 at end of Arm B AND all revision
  events greedy AND late EST success >= 75%.
- OVERALL: T1 AND T2 AND T3 -> PROCESS-MULTIOP-COMPLETE,
  else INCOMPLETE (reported honestly with the failed bar named).
- Determinism: 3/3 runs byte-identical stdout (sha256 recorded).
  Non-determinism voids the verdict.

## 4. Architecture accounting (to record in REPORT.md)

Cognition lines added, new hardcoded semantic cases, modes, bridges,
handlers (all expected 0), learner-state structures created,
capability-source delta. Standalone unfrozen experiment; frozen
sources untouched; paper untouched; nothing pushed.

## 5. Amendment v2 (2026-10-02, after the v1 run, BEFORE v2 code)

v1 ran 3/3 byte-identical. Verdicts: T1=0, T2=1, T3=0.
v1 outputs preserved as run1_v1.txt/run2_v1.txt/run3_v1.txt and
multop_bin_v1. The kill-bar thresholds below are UNCHANGED; only the
apparatus is fixed. Root causes:

- T1 failed (DISCOVERY ep=26, clean=0, pre13=2/4): in single-phase
  training, early exploration (30%) emitted exploration-assisted
  triples (e.g. one exploration step plus two greedy steps) that
  rewarded the inner links (1,3) and (3,2) before the first
  all-greedy triple. The "no prior reward" condition is fragile when
  component learning and novel-task exposure are simultaneous.
  Apparatus failure, not a hypothesis kill: T2 showed the triple is
  reliably produced and adopted (late 26/27 solved, 22/27 triple).
- T3 failed (p4=0, rev_n=0, EST 0/241): design deadlock. The v1 rule
  revised p4 only on greedy wrong answers, but after ADJUST's first
  wrong answer at the EST context its applicability (-1000) fell
  below the fail-0 competitors (FOLLOW/COMPLETE/SHIFT score 0), so
  greedy never selected it again and exploration selections could not
  revise. Permanent lockout. Apparatus failure.

v2 design changes (bars unchanged):

- Arm A becomes two-phase. Phase 1 (ep 0..249): F/F2/T2 only, so
  component applicability (FOLLOW at D-contexts, SHIFT at S-contexts,
  COMPLETE at V+R-contexts) converges with no CHAIN3 exposure.
  Phase 2 (ep 250..499): F/F2/T2/CHAIN3 (30/25/15/30). CHAIN3 and its
  E4 context are entirely novel in Phase 2; the inner links still
  cannot be rewarded in Phase 1 (verified empirically at the phase
  boundary and by the pre-discovery snapshot). Discovery is then a
  zero-shot composition of mastered components plus optimism, and
  clean discovery is robust to exploration. This is a curriculum, not
  an answer leak: the triple and its inner links remain unexperienced
  and unrewarded until discovery.
- Arm B: ADJUST body gains a T-edge gate (MATCH T after MATCH V;
  FAIL if no T edge). ADJUST therefore FAILS (rec 0, no revision, no
  -1 pollution) in F worlds and only ever answers wrongly in EST
  worlds, structurally isolating parameter revision to the task that
  needs it. Revision rule becomes: on ANY wrong answer
  (greedy or exploration), p[o] <- p[o] + (true_ans - ans_given)
  (full signed error, a generic delta rule; the deterministic
  additive bias is identified by one sample). The v1 greedy-only
  restriction is dropped because the T-gate removes the interference
  it was guarding against. T3 clause updated to match: p4 == 4 at
  end AND rev_n >= 1 AND late EST success >= 75% (thresholds 4 and
  75% unchanged).
- Step limit stays 4; all other machinery identical.

This amendment is committed alone and re-frozen before any v2 code
is written. v1 remains reported honestly in REPORT.md.

## 6. Amendment v3 (2026-10-02, after the v2 run, BEFORE v3 code)

v2 ran 3/3 byte-identical. Verdicts: T1=0, T2=1, T3=1.
v2 outputs preserved as run1_v2.txt/run2_v2.txt/run3_v2.txt and
multop_bin_v2. Kill-bar thresholds UNCHANGED again.

- T3=1 (p4=4, rev_n=1, late EST 53/53): body revision works. The
  T-gate plus full-error delta rule fixed the v1 deadlock; a single
  wrong answer identified the bias exactly.
- T2=1 (late 25/25 solved, 19/25 exact triple): adoption works.
- T1=0 again (DISCOVERY ep=277, clean=0, pre13=1/7, pre32=3/4):
  with a 4-step limit, solved non-triple episodes of the form
  [1,3,X,2] (X a failed/wrong op at E4, COMPLETE recovering at
  step 4) rewarded the (1,3) link, and exploration-assisted triples
  rewarded (3,2), before the first all-greedy triple. Phase 1 itself
  was clean (PHASE2-START comp13sum=0/6 comp32sum=0/1). Root cause:
  the 4-step budget lets a perturbed triple still solve, so link
  rewards leak before the policy's own greedy composition.

v3 design changes (bars unchanged):

- Global step limit 4 -> 3. With 3 steps, a CHAIN3 episode can only
  solve via the exact [1,3,2] triple (2 steps to reach E4, 1 step to
  answer); any perturbed [1,3,X] ends unsolved and rewards nothing.
  Hence the inner links (1,3)/(3,2) can be rewarded ONLY by the
  triple itself, structurally, in all phases.
- Arm A Phase 2 (ep>=250) runs with epsilon = 0 (train/test split:
  Phase 1 explores, Phase 2 tests the greedy policy on the novel
  task). With eps=0 every Phase-2 triple is all-greedy by
  construction, so the first triple is the compositional discovery
  event and clean=1 holds structurally (verified empirically).
  Component applicability still transfers from Phase 1; the E4
  context is novel and COMPLETE is found there by the greedy
  least-tried rotation under uniform optimism. This does not hand
  the learner the triple: the triple remains unexperienced and its
  links unrewarded until the policy assembles it.

v1 and v2 remain reported honestly in REPORT.md as apparatus
iterations; the verdict is governed by v3.

## 7. Amendment v4 (2026-10-02, after the v3 run, BEFORE v4 code)

v3 ran 3/3 byte-identical. Verdicts: T1=0, T2=0, T3=1.
v3 outputs preserved as run1_v3.txt/run2_v3.txt/run3_v3.txt and
multop_bin_v3. Kill-bar thresholds UNCHANGED.

- T3=1 again (p4=4, late EST 53/53). Body revision is solid.
- T1=0, T2=0 (CHAIN3 65 episodes, 0 solved, 0 triples): v3 broke
  discovery. Root cause: at CHAIN3-E2, COMPLETE outscored SHIFT
  (664 vs 541) because F2's FOLLOW->COMPLETE pair history
  (comp(1,2)) outweighed SHIFT's applicability, which Phase 1 had
  left weak (T2 only 25%, plus F2-exploration dilution). With eps=0
  the greedy policy then picked COMPLETE (which fails at E2) every
  time and never reached E4. This is itself informative: it is the
  pair-history-vs-applicability contest the experiment is about, and
  v3's Phase 1 did not train applicability strongly enough to be a
  fair test.
- v4: Phase 1 distribution becomes F(35)/F2(25)/T2(40) (was
  40/30/25), so SHIFT applicability at S-contexts is mastered
  strongly enough to fairly contest F2's pair history at E2.
  Everything else (two phases, eps=0 in Phase 2, 3-step limit,
  T-gated ADJUST, full-error revision) is unchanged. Bars unchanged.

This amendment is committed alone and re-frozen before any v4 code.
