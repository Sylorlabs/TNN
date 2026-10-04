# PREREGISTRATION: DDES Adaptive Intervention Planner, Law-Revert Family

Status: FROZEN PREREG. Committed alone before any implementation file
exists in the owned path. Any change requires a dated amendment
committed alone before the changed code runs.

Date: 2026-09-30 UTC
Worker: Law-Revert Adaptive Intervention Builder
Owned path: docs/lab/research-lead/overnight-20260928/ddes_revert/
Builds on: DDES-MULTISTEP-PASS (prereg edcefc164, implementation
7871ca6d3). The derivation core is copied verbatim from
ddes_multistep.zag, which itself copies verbatim from the frozen DDES
sources (56db8d606, 843c45fee). New in this work: the time-indexed
feed protocol (episodes with early/late passive observations),
per-episode survivor re-filtering, per-phase sealed true blocks, and
MODE=STATIC (monotonic cross-episode retirement, the C1-pathology
baseline). No derivation math is re-derived.

## 1. Problem

The C1 clean wave exposed revision-after-revert as the live mechanism
boundary (exploratory H0: deterministic 66/67 miss on the revert query).
The multi-step adaptive planner (DDES-MULTISTEP-PASS) chains
discriminating interventions, but its feed protocol takes a single
passive observation: a change-then-revert ambiguity is not expressible.
This work extends the planner so a revert becomes competing rule graphs
across time-indexed episodes, with round 2 derived conditioned on
revert evidence.

## 2. Protocol (frozen)

Variables X=0, Y=1, Z=2 (n_vars=3, as in the multi-step work).
An entry holds n_cands static candidate rule graphs plus n_phases
sealed true graphs (one per episode). Each episode supplies ONE passive
observation (phase-relative time, small t, as in the existing feed
semantics: prediction = schema-1 arrival check).

Per episode, in order:
1. Filter the FULL candidate set by the episode's passive observation
   (ADAPT/ONESHOT/BASE). MODE=STATIC instead filters its carried
   cross-episode survivor mask (monotonic retirement; never restores).
2. Zero survivors -> DECLARE-OUTSIDE-SET (honest declaration; the
   operative honest path, see section 6).
3. Exactly one survivor -> ACTIVE winner, no intervention.
4. Two or more -> AMBIGUOUS. BASE withholds. ONESHOT derives one
   frontier plan; resolves iff exactly one survivor remains.
   ADAPT/STATIC run the chaining round loop (BUDGET=3 per episode,
   single-survivor / no-frontier / no-progress / budget guards);
   interventions execute against the episode's sealed true graph.
   STATIC writes eliminations back to the cross-episode mask
   (permanent retirement, the C1 monotonic-supersede analogue).

Entry stride 1088: +0 status, +4 winner, +8 n_vars, +12 n_cands,
+16 n_phases, +20 candidate blocks (4 x 128), +532 phase true blocks
(4 x 128), +1044 rounds_total, +1048 episodes_done, +1052 static_mask,
+1056 ep_winner[4], +1072 ep_round[4]. Block layout unchanged (128 B:
+0 nr, +4 src[8], +36 dst[8], +68 delay[8]).

## 3. Frozen cases

Graphs (schema-1 arrivals in brackets):
- G0: [X->Y d1]. {X:0, Y:1, Z:INF}
- G1: [X->Z d1, Z->Y d1]. {X:0, Z:1, Y:2}
- G0p: [X->Y d2]. {X:0, Y:2, Z:INF}
- G3: [X->Z d1]. {X:0, Z:1, Y:INF}

Regression (single episode, ported loaders, same expectations as
7871ca6d3): e0 P1 probe, e1 P2 probe, e2 M1 (true=h2, ADAPT winner=h2
rounds=2, ONESHOT FAIL survivors=2), e3 M2 (true=h1, ADAPT winner=h1
rounds=2, ONESHOT FAIL survivors=2), e4 A (ADAPT and ONESHOT winner=h1
rounds=1).

e5 R1 change-then-revert: candidates h0=G0, h1=G1, h2=G0p.
True phases: P0=G0, P1=G1, P2=G0. Passive per phase: (Y,2)=1
(valid: G0 gives 1, G1 gives 1 since Y arr 2 <= 2, G0 gives 1).

e6 R2 change-then-partial-revert: candidates h0=G0, h1=G1, h2=G0p.
True phases: P0=G0, P1=G1, P2=G0p. Passive per phase: (Y,2)=1
(valid: G0p gives 1 since Y arr 2 <= 2).

e7 R3 outside-set honest failure: candidates h0=[X->Y d1, X->Z d3],
h1=[X->Y d2, X->Z d4], h2=[X->Z d5]. True (1 phase): G3.
Passive: (Z,1)=1 (valid: G3 Z arr 1 <= 1 gives 1; every candidate
predicts 0: Z arrivals 3, 4, 5 all > 1).

## 4. Frozen predictions

Modes: BASE=0 (withhold), ONESHOT=1, ADAPT=2, STATIC=3.

e5 R1 ADAPT: P0 passive (Y,2)=1 keeps {h0,h1,h2}; round 1 frontier
(Y,1) schema=1, plan [S,W,O(1)], real=1 (G0), PRED h0=1 h1=0 h2=0,
ELIM h1, ELIM h2, RESOLVED winner=h0 rounds=1. P1: round 1 (Y,1),
real=0 (G1), ELIM h0; round 2 survivors=[h1,h2] TARGET (Z,1)
schema=1, plan [S,W,O(2)], real=1, PRED h1=1 h2=0, ELIM h2,
RESOLVED winner=h1 rounds=2. P2: round 1 (Y,1), real=1 (G0),
ELIM h1, ELIM h2, RESOLVED winner=h0 rounds=1. Winners [h0,h1,h0],
rounds_total=4. Post query Q(1,1) -> 1 (final winner h0).

e5 R1 ONESHOT: P0 RESOLVED h0 rounds=1; P1 ONESHOT-RESOLVE-FAIL
survivors=2; P2 RESOLVED h0 rounds=1.

e5 R1 STATIC: P0 winner=h0 rounds=1, RETIRE h1, RETIRE h2. P1:
carried {h0}, passive-consistent, single survivor, winner=h0
rounds=0 (WRONG: true=G1; the static-revision failure). P2:
winner=h0 rounds=0 (right, wrong reason).

e5 R1 BASE: AMBIGUOUS all three episodes, withholds throughout.

e6 R2 ADAPT: P0 winner=h0 rounds=1; P1 winner=h1 rounds=2 (same
trace shape as R1 P1); P2: round 1 (Y,1), real=0 (G0p, Y arr 2 > 1),
PRED h0=1 h1=0 h2=0, ELIM h0; round 2 survivors=[h1,h2]
TARGET (Z,1) schema=1, plan [S,W,O(2)], real=0 (G0p Z INF),
PRED h1=1 h2=0, ELIM h1, RESOLVED winner=h2 rounds=2.
Winners [h0,h1,h2], rounds_total=5. The planner identifies the
partial-revert law G0p, not a snap-back to h0. Post queries:
Q(1,2) -> 1, Q(2,2) -> 0 (final winner h2).

e6 R2 ONESHOT: P0 RESOLVED h0; P1 FAIL survivors=2; P2 FAIL
survivors=2.

e6 R2 STATIC: winners [h0,h0,h0], rounds [1,0,0]; P1 and P2 wrong.

e6 R2 BASE: withholds throughout.

e7 R3: all four modes emit DECLARE-OUTSIDE-SET on the passive
observation (zero candidates consistent). No intervention is
derived. This is the honest-failure demonstration.

Regression: e2 ADAPT RESOLVED winner=h2 rounds=2; e3 ADAPT RESOLVED
winner=h1 rounds=2; e4 ADAPT and ONESHOT RESOLVED winner=h1
rounds=1; e2/e3 ONESHOT ONESHOT-RESOLVE-FAIL survivors=2;
BASE withholds on e2/e3/e4; e0/e1 ACTIVE with correct queries in
all modes.

Frozen SUMMARY expectations (ok/total, resolved = episodes
terminating with a single winner via the mode's machinery;
correctness is asserted separately by the winner checks):
- BASE: ok=13/13 resolved=0
- ONESHOT: ok=15/15 resolved=4
- ADAPT: ok=24/24 resolved=9
- STATIC: ok=19/19 resolved=9

## 5. Kill bars

K1: this prereg commit strictly precedes the implementation commit
(verified with git merge-base --is-ancestor).
K2: at least one revert-family adaptive resolution demonstrated
with the static-revision failure shown (R1: ADAPT winners
[h0,h1,h0] vs STATIC P1 misresolve; R2: ADAPT P2 winner=h2 not
h0), plus the honest outside-set declaration (R3), plus
regression clean (M1/M2/A as frozen).
K3: pure Zag, zero Python at every step, 3/3 byte-identical runs,
no em/en dash bytes (shell-only check_no_dash.sh).

## 6. Honesty notes (frozen)

- With binary outcomes, a round can never eliminate ALL survivors
(one side always matches real), so the intervention-level
world-outside-set guard is unreachable; the passive-filter
declaration (R3) is the operative honest path. The guard stays
coded as a backstop.
- Researcher still owns: hypothesis format, frozen case set,
derivation algorithm, action vocabulary, budget constant,
episode boundaries. The learner authors: per-episode survivor
sets, each round's target conditioned on observed outcomes, plan
shapes, and resolutions.
- Bounded L2. NOT L3. Arena C9 re-entry stays parked until the
revert family has a verdict.

## 7. Deliverables

ddes_revert.zag, BUILD.sh, RUN.sh (3 identical runs), VERIFY.sh
(checking every frozen line in section 4), DDES_REVERT_RESULT.md.
Committed with owned pathspec only.
