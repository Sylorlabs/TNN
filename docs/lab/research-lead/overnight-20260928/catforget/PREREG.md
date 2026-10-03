# PREREG.md -- H-CATFORGET-1: Catastrophic Forgetting under Interference

Worker: Catastrophic Forgetting Worker (H-CATFORGET-1), 2026-10-02.
Status: FROZEN before implementation. Committed alone before any source
file is written.

## 0. Hypothesis

H-CATFORGET-1: when one persistent learner masters capability A via
learned composition links and then trains on an interfering capability
B, A's survival is predicted by whether the composition links between
A's structures and the shared substrate stay in the decision loop.
Severing the links causes catastrophic forgetting of A; unrelated
interference (disjoint substrate) causes little forgetting in either
case. This is the phased, dedicated-interference test of the C220
finding (composition links shield applicability; no-comp ablation
catastrophically forgets).

## 1. Design

### 1.1 Learner (one persistent learner per arm across all three phases; no reset between phases)

Generic protected-class machinery (fixed, domain-neutral): graph store
with edges as (from, kind, to) triples, a 4-instruction interpreter
(MATCH/ADD/ANSWER/SETCUR), an epsilon-greedy bandit selector over op
indices, two LCG RNG streams (env, learn), generic consequence credit
assignment.

Learner-owned structures (all in learner-state arrays; written only by
consequence updates, never by task logic):
- body[o]: 5 executable byte-array op bodies (innate initial forms;
  every control parameter is learned).
- appl[o][ctx]: mean recorded reward per observable context (5 x 32).
  ctx = hasV + 2*hasD + 4*hasS + 8*hasT + 16*hasU, an edge-existence
  probe from CUR. The probe is cheap and ambiguous by design.
- comp[p][o]: mean recorded reward of o immediately following p
  (5 x 5). Written only when p was effective (non-failed).
- consequence ring (24 x 2, audit only).

Ops: 0 gather (MATCH V; ANSWER), 1 follow (MATCH D; CUR=E),
2 complete (MATCH V; MATCH R; ADD; ANSWER), 3 followT (MATCH T; CUR=E),
4 readU (MATCH U; ANSWER).

The interpreter never branches on op id. The selector never branches on
op id (ids occur only as table indices; ties broken by least-tried then
lowest id). Zero modes, bridges, handlers, semantic cases.

Selection: score(o) = appl_mean(o,ctx) + comp_term, where comp_term =
comp_mean(prev,o) in FULL arms and 0 in SEV arms (links are recorded in
both arms but severed from scoring in SEV, exactly the C220 contrast).
Unseen (op,ctx) and unseen (p,o) score 500 (uniform optimism).
Epsilon-greedy with eps=0.15 for episode<150 of a phase, else 0.
Within an episode: failed ops are excluded for the rest of the episode;
max 12 steps; a wrong or right answer ends the episode; timeout ends the
episode as failure.

Credit (generic, at episode end): a failed op records 0 to appl at its
selection ctx; an op answering wrong records -1; an op answering right
records +1; a moved (non-terminal) op records +1 iff the episode is
eventually solved, else 0 (never punished for a later op's wrong
answer). comp(prev,o) records o's value iff prev>=0 and prev was
effective. Phase 3 runs with learning frozen (the harness skips all
writes; selection code is identical, so this is not a learner mode).

### 1.2 Worlds (deterministic via the env LCG; values in 1..50)

- N1 (task A): (Q)-[D]->(E2), (E2)-[V]->V2, (E2)-[R]->K; true answer
  V2+K. Solved by follow->complete. At E2 the probe reads ctx=1
  (hasV), identical to the F probe: the ambiguous shared context.
- F (task B, similar): (Q)-[V]->ans; true answer ans; ctx=1. Solved
  by gather. F writes the SAME appl cell (gather,1) that Phase 1
  teaches as -1000: maximally similar interference, one cell with
  directly contradicting rewards.
- U (task B, unrelated): (Q)-[T]->(E4), (E4)-[U]->W; true answer W;
  ctx=8 at Q, ctx=16 at E4. Solved by followT->readU. Touches only
  appl rows 3,4 and comp pairs among {3,4}: disjoint from A's
  substrate (rows 0,1,2; pairs among {0,1,2}; ctx 1,2).

### 1.3 Phases (per arm; the learner persists; no reset)

- Phase 1: 200 N1 episodes. Task A (the follow->complete composition)
  mastered to criterion.
- Phase 2: 300 B episodes (SIM arms: F; DIFF arms: U). Learning
  continues on the same tables.
- Phase 3: 100 N1 episodes, learning FROZEN, eps=0. Retention = N1
  success rate, no retraining.

### 1.4 Arms (2x2) x 3 seeds (111, 222, 333)

- FULL-SIM: comp consulted in scoring; Phase 2 = F.
- SEV-SIM: comp recorded but not consulted; Phase 2 = F.
- FULL-DIFF: comp consulted in scoring; Phase 2 = U.
- SEV-DIFF: comp recorded but not consulted; Phase 2 = U.

All four arms and all three seeds run inside one binary invocation, in
a fixed order, from fixed seeds.

### 1.5 Predicted mechanism (why the bars are set where they are)

Phase 1 teaches appl(gather,1)=-1000 (gather answers wrong at E2),
appl(complete,1)=+1000, appl(follow,2)=+1000, comp(1,2)=+1000.
Phase-2 F episodes teach appl(gather,1)=+1000, a direct contradiction
in the shared cell, while comp(1,2) and appl(follow,2) stay untouched
(F episodes are single-op so no pairs are written; F never sees
ctx=2). Phase 3 at E2: FULL routes via comp(1,2) to complete
(shielded); SEV scores appl only, picks the corrupted gather cell,
answers wrong, and forgets A. U episodes touch disjoint cells, so
neither DIFF arm should forget.

## 2. Preregistered bars (x1000 fixed point; every bar must hold on all 3 seeds)

- R1 mastery: late-Phase-1 (last 50 episodes) N1 success >= 90% in all
  4 arms, AND comp(1,2) >= 900 in FULL arms at end of Phase 1 (the
  link whose shielding is under test must demonstrably exist). If R1
  misses in any arm, retention claims for that arm are VOID.
- R2 shielding: FULL-SIM Phase-3 retention >= 90%.
- R3 catastrophic forgetting: SEV-SIM Phase-3 retention <= 30%.
- R4 link effect: FULL-SIM retention minus SEV-SIM retention >= 50pp.
- R5 gradient: FULL-DIFF retention >= 90% AND SEV-DIFF retention
  >= 90% (unrelated B does not corrupt A in either arm); SEV-DIFF
  retention minus SEV-SIM retention >= 50pp (similarity drives
  forgetting).

Verdict: CATFORGET-COMPLETE iff R1..R5 all hold on all 3 seeds. Any
bar miss yields CATFORGET-INCOMPLETE with the missed bar named. A 3/3
byte-identity mismatch is PROCESS-FAIL.

## 3. Determinism and purity

Pure Zag via the pinned znc; shell only for builds, binary runs,
byte checks, and git. Two LCG streams, fixed seeds, fixed tie-breaks.
3/3 byte-identical runs required on the same seed set. Per AGENTS.md
toolchain lessons: u8-backed cells with get32/set32 helpers (no
`as *i32` slice construction inside functions); a single preallocated
output buffer with cursor-returning e1str/e1i64 helpers and one
_zag_raw_syscall(1,1,ptr,len) write at end (no _zag_print for dynamic
content); no `as []f64` casts.

## 4. Architecture accounting (One-System Rule)

One new standalone file: catforget.zag. 0 modes, 0 bridges,
0 handlers, 0 semantic cases, 0 hardcoded op sequences in learner
code. Learner-state structures: 5 op bodies, appl 5x32, comp 5x5,
consequence ring. The phase loop and the Phase-3 freeze are
harness-level (not learner modes): the learner's selection and credit
code paths are identical in all phases.
