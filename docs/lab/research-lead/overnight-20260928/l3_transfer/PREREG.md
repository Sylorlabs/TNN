# PREREG: L3 Transfer, Reuse of an Invented Intermediate Across Domains

Status: PREREG-FROZEN 2026-10-02. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/l3_transfer/` only.
Worker: L3 Transfer Worker (subagent, 2026-10-02).
Parent mandate: test L3 TRANSFER, reuse an invented intermediate across
domains. Prior waves: FORAGE invented M = [ADD R0,R2], COMPILE invented
M = [ADD R0,R3], INTERVENE invented M = [ADD R0,R1], each invented fresh
for its domain. Open: can an intermediate invented in one domain be
REUSED (not reinvented) in another domain where it applies.

## 1. What is being tested

Whether a learner that invents a novel intermediate M in domain A, and
stores it in a persistent learner owned intermediate library with
provenance, later REUSES that same intermediate in domain B (same
underlying structure, different surface: different episodes, labels,
threshold, decision vocabulary) instead of reinventing it from scratch.
Reuse must be evidence driven (the library is evaluated on B experience;
a non fitting stored intermediate is rejected), cheaper than fresh
invention, and causally attributable to the library (ablation: library
wiped, the cost returns).

The intermediate's structural identity is its reduction program bytes
(the composition_l3 ERRATUM-1 rationale carries over: the threshold is
Y's adaptive decision parameter, refit per domain; the program is the
invented structure).

## 2. Frozen learner machinery (disclosed)

Generic machinery plus learned state. No episode data, no hidden world
rules, no reduction solution in `learner.zag`. Frozen for this build:

- X: episode recall, 48 slots of [id,e0,e1,e2,e3]. Y: threshold decide
  on scalars, 24 scalar observations, threshold i32. M slot: 32 bytes
  [n, gen, sup, pad, threshold i32, program 24 bytes, 8 instr x 3].
- Reduction program: up to 8 instructions, registers R0..R3 preloaded
  with the 4 readings, output R0. Instruction = (op, d, s), d,s in 0..3.
  Frozen op basis: 0=CPY (Rd=Rs), 1=ADD (Rd+=Rs), 2=SUB (Rd-=Rs),
  3=MAX (Rd=max(Rd,Rs)), 4=MIN (Rd=min(Rd,Rs)). Not expandable.
- construct(): greedy search, identical logic to the composition_l3
  learner. From a starting program, each round evaluates every (op,d,s)
  append (5*16=80 candidates) by best threshold classification score on
  the labeled train episodes; applies the single append with the largest
  strictly positive gain; ties broken by candidate order (op 0..4,
  d 0..3, s 0..3, first max). Threshold sweep t=0..40 ascending,
  first max. Stops at no positive gain or 8 instructions. Counts
  construct_calls and construct_evals (candidate evaluations) in state.
- Intermediate library (new learner owned state, generic, no modes):
  8 entries of 28 bytes [program 24, n, gen, origin domain tag,
  n_reuse]. lib_store() files the current M slot with an origin tag.
  lib_probe() evaluates every stored entry on new labeled experience
  with a refit threshold (t=0..40 ascending, first max) and reports
  per entry score and threshold. lib_reuse() adopts an entry: M slot
  takes the entry program (same generation), Y threshold takes the
  refit value, n_reuse increments.
- lib_adapt(): the generic transfer policy. Probe the library on the
  new train set. If EXACTLY ONE stored entry reaches perfect
  classification with its refit threshold, reuse it (code 0). Otherwise
  construct fresh from the empty program, write the M slot, set Y from
  the constructed threshold, and store the invention with the caller
  supplied origin tag (code 1). The policy is domain blind: it never
  reads a domain tag except to record provenance.
- decide(): X recall, exec M, Y decide; -1 = NO_DECISION.

## 3. Frozen world (environment, hidden from learner)

Three domains. The learner sees only sequences (X teaching) and labels
(observed outcomes). Labels below are generated from the hidden rules;
the learner source never calls the rules.

Domain A = FORAGE (tables frozen from composition_l3 phase 1):
- Y prior scalars: (12,rich),(15,rich),(11,rich),(8,poor),(5,poor),
  (9,poor). Fit: 6/6, t=10.
- Hidden rule: rich iff e0+e2 >= 10.
- Train ids 1..8:
  1:[7,1,5,2] rich  2:[2,9,9,0] rich  3:[8,0,4,8] rich  4:[1,2,9,9] rich
  5:[9,0,0,1] poor  6:[8,8,1,0] poor  7:[0,1,2,3] poor  8:[5,5,4,1] poor
- Test ids 9..12:
  9:[6,0,6,0] rich  10:[9,9,0,0] poor  11:[3,3,8,8] rich  12:[4,4,4,4] poor

Domain C = RELAY decoy (tables frozen from composition_l3_adv phase 1):
- Y prior scalars: (12,open),(15,open),(11,open),(8,closed),(5,closed),
  (9,closed). Fit: 6/6, t=10.
- Hidden rule: open iff e0-e1 >= 4.
- Train ids 201..208:
  201:[5,0,9,9] open  202:[6,1,2,2] open  203:[4,0,7,3] open
  204:[8,3,1,1] open  205:[9,7,0,5] closed  206:[7,6,4,4] closed
  207:[3,5,8,8] closed  208:[2,1,6,6] closed
- Test ids 209..212:
  209:[7,2,5,0] open  210:[9,8,1,9] closed  211:[5,0,3,7] open
  212:[6,4,2,2] closed

Domain B = SENTRY (new tables, builder designed, hand verified below):
- Y prior scalars: (17,alert),(18,alert),(15,calm),(14,calm),(16,alert),
  (13,calm). Fit: 6/6, t=16.
- Hidden rule: alert iff e0+e2 >= 16. Same underlying structure as
  FORAGE (sum of channels 0 and 2), different episodes, labels,
  threshold, and vocabulary.
- Train ids 101..108 (e1=5, e3=5 constant on all episodes):
  101:[9,5,7,5] alert  102:[7,5,9,5] alert  103:[9,5,9,5] alert
  104:[8,5,8,5] alert  105:[9,5,6,5] calm  106:[6,5,9,5] calm
  107:[7,5,7,5] calm  108:[5,5,8,5] calm
- Test ids 109..112:
  109:[9,5,8,5] alert  110:[7,5,9,5] alert  111:[8,5,6,5] calm
  112:[5,5,5,5] calm

## 4. Frozen hand derived expectations

SENTRY train audit (each single instruction candidate appended to the
empty program; score = best threshold classification on train 101..108;
baseline = empty program, R0 = e0):
- e0+e2 values: alert {16,16,18,16}, calm {15,15,14,13}. ADD R0,R2 is
  8/8, first max threshold t=16. Gain over baseline below.
- Baseline e0 values: alert {9,7,9,8}, calm {9,6,7,5}. Best 6/8
  (t=7 or t=8; the value 9 occurs as both alert and calm). So baseline
  6/8, ADD R0,R2 gain = 2, strictly positive.
- All other candidates score below 8/8: CPY R0,R2 (e2) 5/8;
  MIN R0,R2 7/8 at t=7 (7 occurs as alert and calm); MAX R0,R2 5/8;
  SUB R0,R2 (e0-e2) 4/8; 2*e0 6/8; e0+e1, e0+e3, e0-e1, e0-e3 6/8
  (e1=e3=5 constant, same order as e0); MAX R0,R1, MAX R0,R3 6/8;
  MIN R0,R1, MIN R0,R3 4/8 (constant 5); CPY R0,R1, CPY R0,R3 4/8;
  SUB R0,R0 4/8; every d in 1..3 variant leaves R0 = e0, 6/8, gain 0.
- Therefore ADD R0,R2 (op=1,d=0,s=2) is the UNIQUE 8/8 round 1 winner,
  gain 2, t=16. Round 2: no candidate can beat 8/8, stop. Fresh
  construction on SENTRY costs 2 rounds x 80 = 160 candidate evals.
- Decoy check: SUB R0,R1 (the RELAY intermediate) on SENTRY train is
  e0-5, same order as e0, best 6/8 < 8/8. It must be rejected.
- M_A probe on SENTRY train: e0+e2, 8/8 at t=16. Exactly one library
  entry perfect when the library holds M_A (FORAGE) and M_C (RELAY).
- SENTRY test with M=[ADD R0,R2], t=16: 109: 17 alert ok; 110: 16 ok;
  111: 14 calm ok; 112: 10 calm ok. 4/4.

FORAGE expectations (frozen, composition_l3): construction round 1:
80 evals, baseline 5/8, ADD R0,R2 unique 8/8, gain 3, t=10. Round 2:
stop. M_A program bytes [1,0,2], test 9..12: 4/4.

RELAY expectations (frozen, composition_l3_adv): M_A probe on RELAY
train: 5/8 at t=12, not perfect, correctly rejected. Construction
round 1: 80 evals, baseline 6/8, SUB R0,R1 (op=2,d=0,s=1) unique 8/8,
gain 2, t=3. Round 2: stop. M_C program bytes [2,0,1], test 209..212:
4/4.

## 5. Frozen arms

- ARM-TRANSFER: one learner state. Phase A FORAGE: teach, lib_adapt
  origin=FORAGE (library empty, constructs). Phase C RELAY: teach,
  lib_adapt origin=RELAY (M_A probed 5/8, rejected; constructs M_C).
  Phase B SENTRY: teach, lib_adapt origin=SENTRY (M_A 8/8 t=16, M_C
  6/8; exactly one perfect; REUSE M_A; zero construct evals in B).
- ARM-FRESH: fresh learner state, SENTRY only: teach, lib_adapt
  origin=SENTRY (library empty; constructs M_B from scratch, 160
  evals, origin=SENTRY).
- ARM-NO-LIB: same as ARM-TRANSFER through phase C, then the library
  is wiped (LIBN=0, entries cleared), then SENTRY via lib_adapt
  origin=SENTRY (library empty; constructs from scratch, 160 evals).
  Causal ablation: the library is what removes the B invention cost.

## 6. Kill bars

- T1 (determinism): 3 runs of the binary are byte identical
  (sha256 equal).
- T2 (invention in A): phase A construct stats exactly: rounds=2,
  evals=160, base0=5, win=(1,0,2), gain=3, score=8, t=10. Library
  entry 0 program bytes [1,0,2], origin=FORAGE. A test 4/4.
- T3 (decoy invention in C): phase C probe of entry 0 (M_A) on RELAY
  train = 5/8 (< 8/8, rejected, not reused). Phase C construct stats
  exactly: rounds=2, evals=160, base0=6, win=(2,0,1), gain=2, score=8,
  t=3. Library entry 1 program bytes [2,0,1], origin=RELAY. C test
  4/4.
- T4 (reuse in B, not reinvention): phase B probe: entry 0 score 8/8
  t=16, entry 1 score 6/8, exactly one perfect. lib_adapt code=0
  (reused). construct_evals delta across phase B == 0. M slot program
  bytes [1,0,2], threshold 16. Reused entry origin == FORAGE,
  n_reuse == 1. B test 4/4.
- T5 (fresh baseline): ARM-FRESH lib_adapt code=1, construct evals =
  160, stats base0=6, win=(1,0,2), gain=2, score=8, t=16. Invented
  entry program [1,0,2] with origin=SENTRY (reinvented, not
  transferred). B test 4/4.
- T6 (faster): transfer phase B construct_evals (0) < fresh phase B
  construct_evals (160).
- T7 (library causal): ARM-NO-LIB phase B lib_adapt code=1,
  construct evals = 160, invented origin=SENTRY, B test 4/4. Wiping
  the library restores the full invention cost.
- T8 (hygiene): 0 modes, 0 bridges, 0 handlers, 0 new semantic cases.
  Pure Zag for all research logic. Safebin PATH, no forbidden
  executables. Unfrozen scope only; frozen source untouched; paper
  untouched; nothing pushed; explicit pathspecs on every git
  add/commit; no em/en dashes in docs (byte verified).

Verdict L3-TRANSFER-COMPLETE requires T1..T8 all PASS with no
falsifier firing.

## 7. Falsifiers

- F-NO-INVENT-A: phase A construct stats deviate from section 4.
- F-DECOY-ACCEPT: M_A probe on RELAY train reaches 8/8 (selection
  would be vacuous).
- F-WRONG-PICK: phase B reuses entry 1 (M_C) or any non FORAGE entry.
- F-REINVENT-B: transfer phase B construct_evals delta > 0.
- F-ORIGIN: reused entry origin tag != FORAGE.
- F-NO-SPEEDUP: transfer B evals >= fresh B evals.
- F-OP-EXPAND: op basis extended beyond {CPY,ADD,SUB,MAX,MIN}. Voids
  the build.
- F-AUDIT: any section 8 pattern matches in learner.zag. Voids the
  build.
- F-NONDET: the three runs differ by one byte. Voids the build.
- F-PYTHON: any python/python3 invocation in the worker process tree.
  Voids the build.

## 8. Frozen grep audit spec (run on learner.zag)

Each pattern must return zero matches (grep -c == 0):
1. `e0+e2` (the solution expression)
2. `ADD R0,R2` (the solution instruction)
3. `7,1,5,2` (episode data must not live in the learner)
4. `5,0,9,9` (RELAY episode data must not live in the learner)
5. `9,5,7,5` (SENTRY episode data must not live in the learner)
6. `_MODE` (zero modes allowed)
7. `bridge` (case insensitive; never used in code at all)

## 9. Determinism spec

No RNG. Fixed candidate order, first max tie breaking everywhere,
ascending threshold sweeps, library probed in invention order. Output
via one preallocated buffer and a single raw syscall write. 3/3 byte
identical required. Stdout byte verified (od -c spot check) before
trusting it.

## 10. Disclosed residual footprint and non claims

- The op basis {CPY,ADD,SUB,MAX,MIN}, the register machine, and the
  greedy construct() are researcher supplied generic machinery,
  disclosed here. The claim is about the intermediate's cross domain
  reuse being learner driven (invention in A, evidence driven
  selection in B), not about the basis.
- The SENTRY tables were designed by the builder, not an independent
  adversary. Sealed adversary generality (Micah C0-C) is open future
  work. One transfer pair does not establish broad generality.
- The library, probe, reuse, and lib_adapt policy are new generic
  learner machinery for this experiment, not a domain specific
  shortcut: the policy never conditions on a domain tag except to
  record provenance, and the decoy rejection in phase C shows it does
  not blindly apply old solutions.
- This build does not claim Micah's full 12 criterion L3 bar.

## 11. Amendments (transparent, before the frozen evaluation runs)

AMEND-1 (SENTRY Y prior fit scope): section 3 lists the SENTRY Y prior
fit as 6/6 t=16. In ARM-TRANSFER the learner is continuing: Y scalar
observations accumulate across phases (6 FORAGE + 6 RELAY + 6 SENTRY =
18), so the fit over the accumulated 18 mixed observations is 15/18 at
t=10 and is not asserted. The 6/6 t=16 expectation applies to the
isolated 6 SENTRY observations, evaluated in ARM-FRESH (asserted
there). In ARM-TRANSFER phase B the driver still teaches the 6 SENTRY
scalars (honest accumulation); the operative B threshold is the library
refit t=16, asserted via the probe and the M slot. No load bearing bar
changes: T4 still requires probe entry 0 at 8/8 t=16 and M slot
threshold 16.

AMEND-2 (T7 arithmetic): the driver first asserted ARM-NO-LIB total
construct evals == 320, a builder slip: state N accumulates phase A
(160) + phase C (160) + phase B (160) = 480. T7 is corrected to assert
the phase B delta == 160 (reinvention cost fully restored by wiping the
library). The T6 comparison (transfer B delta 0 vs fresh B delta 160)
is unchanged.
