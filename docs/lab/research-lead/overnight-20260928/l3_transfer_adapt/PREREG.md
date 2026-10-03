# PREREG: L3 Transfer-Adapt, Adapting an Invented Intermediate for a Partial-Match Domain

Status: PREREG-FROZEN 2026-10-02. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/l3_transfer_adapt/` only.
Worker: L3 Transfer-Adapt Worker (subagent, 2026-10-02).
Parent mandate: test L3 TRANSFER where the stored intermediate needs
ADAPTATION (not exact reuse) for a partially matching domain.

## 1. What is being tested

L3-TRANSFER-COMPLETE showed exact reuse of an invented intermediate
across structurally matching domains. Its boundary is explicit: exact
reuse across structurally matching domains, not partial-match
adaptation, which is the L2 frontier. This experiment tests the open
question: can a stored intermediate M, invented in domain A, be ADAPTED
by the learner (via the generic L2 operators EXTEND, TRUNCATE,
SPECIALIZE) for a domain B that only partially matches, instead of
being reinvented from scratch?

The claim under test is narrow and falsifiable: on a domain B where no
stored intermediate classifies perfectly, the learner's generic
lib_adapt policy finds a one-edit adaptation of a stored intermediate
that does, adopts it with recorded provenance (parent entry, operator),
at lower evaluation cost than fresh construction, and the adapted
intermediate decides B correctly. The frozen test exercises EXTEND;
TRUNCATE and SPECIALIZE are implemented as generic machinery.
SPECIALIZE fires in the RELAY phase as a real second data point; a
TRUNCATE learning validation is an explicit non-claim (see 10).

## 2. Frozen learner machinery (disclosed)

Generic machinery plus learned state. No episode data, no hidden world
rules, no reduction solution in `learner.zag`. Frozen for this build.
The X/Y/M core, register machine, op basis {0=CPY,1=ADD,2=SUB,3=MAX,
4=MIN}, greedy construct(), and threshold sweep (t=0..40 ascending,
first max) are identical to the l3_transfer build.

New generic state and machinery for this experiment:

- Library entry: 32 bytes [program 24, n, gen, origin tag, parent idx
  (255 = invented, no parent), parent op (0=EXTEND, 1=TRUNCATE,
  2=SPECIALIZE, 255=none), n_reuse, pad]. Parent fields are new
  learner-owned provenance state, generic, no modes.
- Counters: adapt_calls, adapt_evals (one candidate program evaluation
  = one eval, same unit as construct_evals).
- L2 operators, defined on a stored program P of length n:
  - EXTEND(P): 80 candidates, append (op,d,s) for op 0..4, d 0..3,
    s 0..3 to P.
  - TRUNCATE(P): 1 candidate, P with its last instruction removed
    (length n-1; for n=1 this is the empty program).
  - SPECIALIZE(P): n*80 candidates, replace instruction at position
    p (p=0..n-1) with (op,d,s) for op 0..4, d 0..3, s 0..3.
- lib_adapt(origin): the generic transfer policy.
  1. Probe every stored entry exactly on the new labeled train set
     with a refit threshold. If exactly one entry is perfect, reuse
     it (code 0).
  2. Else scan entries in library order; for each entry scan
     operators in the frozen order EXTEND, TRUNCATE, SPECIALIZE.
     For each (entry, op) evaluate all candidates, take the best
     (first max on ties). Adopt the first (entry, op) whose best is
     perfect: M slot takes the adapted program, Y threshold takes
     the refit value, and a NEW library entry is stored with
     parent=entry, parent_op=op, origin=caller tag (code 2).
  3. Else construct fresh from the empty program and store the
     invention with parent=255 (code 1).
  The policy never conditions on a domain tag except to record
  provenance. The operator order is a frozen tie-break; the frozen
  test asserts global uniqueness of the perfect (entry, op,
  candidate), so the order is load-free here.
- Driver-side verification (not learner cost): an exhaustive audit
  enumerates every (entry, op, candidate) with the same candidate
  generator the learner uses, and asserts exactly one perfect
  adaptation with the frozen identity.

## 3. Frozen world (environment, hidden from learner)

The learner sees only sequences (X teaching) and labels (observed
outcomes). FORAGE and RELAY tables are reused verbatim from the frozen
l3_transfer build (disclosed prior). AEGIS tables are new, designed by
the builder and hand verified in section 4.

Domain A = FORAGE (frozen from l3_transfer):
- Y prior scalars: (12,rich),(15,rich),(11,rich),(8,poor),(5,poor),
  (9,poor). Fit: 6/6, t=10.
- Hidden rule: rich iff e0+e2 >= 10.
- Train ids 1..8:
  1:[7,1,5,2] rich  2:[2,9,9,0] rich  3:[8,0,4,8] rich  4:[1,2,9,9] rich
  5:[9,0,0,1] poor  6:[8,8,1,0] poor  7:[0,1,2,3] poor  8:[5,5,4,1] poor
- Test ids 9..12:
  9:[6,0,6,0] rich  10:[9,9,0,0] poor  11:[3,3,8,8] rich  12:[4,4,4,4] poor

Domain C = RELAY decoy (frozen from l3_transfer):
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

Domain B = AEGIS (new; partial match to FORAGE):
- Y prior scalars: (17,alert),(18,alert),(15,calm),(14,calm),(16,alert),
  (13,calm). Fit: 6/6, t=16 (asserted in ARM-FRESH only; in
  ARM-TRANSFER Y experience accumulates across phases, per the
  l3_transfer AMEND-1 rationale).
- Hidden rule: alert iff e0+e2+e3 >= 16. FORAGE's intermediate
  [ADD R0,R2] computes e0+e2, which is necessary but not sufficient
  here: the partial match needs one more term.
- Train ids 101..108 (e1=5 constant on all episodes):
  101:[9,5,7,1] alert  102:[7,5,9,1] alert  103:[5,5,8,4] alert
  104:[9,5,9,0] alert  105:[9,5,6,0] calm  106:[8,5,7,0] calm
  107:[7,5,7,0] calm  108:[5,5,8,1] calm
- Test ids 109..112:
  109:[9,5,8,0] alert  110:[6,5,9,2] alert
  111:[8,5,7,0] calm  112:[4,5,9,1] calm

## 4. Frozen hand derived expectations

Notation: score = best threshold classification on the 8 train
episodes, threshold sweep t=0..40 ascending, first max. Value vectors
are listed alert then calm.

### 4a. AEGIS train audit (ids 101..108)

Single channel and collapsed classes:
- e0 {9,7,5,9 | 9,8,7,5}: 5/8 (t=9). e1 const: 4/8.
- e2 {7,9,8,9 | 6,7,7,8}: 6/8. e3 {1,1,4,0 | 0,0,0,1}: 6/8.
- 2e0, e0+5, max(e0,e3)=e0, max(e0,5)=e0: same order as e0, 5/8.
- max(e0,e2) {9,9,8,9 | 9,8,7,8}: 6/8 (t=9).
- min(e0,e2) {7,7,5,9 | 6,6,7,5}: 6/8 (t=7).
- min(e0,e3)=e3: 6/8. min(e0,5)=5 const: 4/8.
- e0-e2 {2,-2,-3,0 | 3,1,0,-3}: 4/8. e0-e3 {8,6,1,9 | 9,8,7,4}: 4/8.
- e0+e3 {10,8,9,9 | 9,8,7,6}: 6/8 (t=9: 3/4+3/4; t=8: 4/4+2/4).
- e0+e2 {16,16,13,18 | 15,15,14,13}: 7/8 at t=16 (3/4+4/4). This is
  the M_A exact probe: imperfect, so exact reuse is rejected.
- e0+e2+e3 {17,17,17,18 | 15,15,14,14}: 8/8 at t=16. Designated
  adaptation target.

Fresh construction on AEGIS (from the empty program):
- Round 1 (80 evals): baseline e0 = 5/8. Winner (ADD,0,2) = e0+e2,
  score 7, t=16, gain 2. Unique: every other round-1 candidate is
  6/8 or worse (e0+e3 6/8, e2 6/8, e3 6/8, max(e0,e2) 6/8,
  min(e0,e2) 6/8, e0 5/8, rest below).
- Round 2 (from [ADD R0,R2], 80 evals): baseline 7/8. Winner
  (ADD,0,3) = e0+e2+e3, score 8, t=16, gain 1. Unique: next best
  7/8 (2(e0+e2), (e0+e2)+5, max(e0+e2,e3), all same order as e0+e2;
  e0+2e2 {23,25,21,27 | 21,22,21,21} 7/8 at t=23; e0+e2-e3 5/8;
  min(e0+e2,e3)=e3 6/8; min(e0+e2,e2)=e2 6/8; d in 1..3 leave R0 =
  e0+e2, 7/8).
- Round 3 (80 evals): 8/8 is the ceiling, no strictly positive gain,
  stop.
- Totals: rounds=3, evals=240. Invented program [1,0,2,1,0,3], n=2.

Adaptation scan on AEGIS (library holds M_A=[1,0,2], M_C=[2,0,1]):
- Exact probes: entry 0 (e0+e2) 7/8 t=16; entry 1 (e0-5, same order
  as e0) 5/8. n_perfect=0. Neither is reused.
- EXTEND(M_A), 80 candidates: unique 8/8 is (ADD,0,3). All others
  below (audited in the round-2 list above). First max in candidate
  order is (1,0,3).
- TRUNCATE(M_A) = empty program = e0: 5/8, not perfect.
- SPECIALIZE(M_A): d=0 replacements are exactly the round-1
  candidates (max 7/8); d in 1..3 leave R0=e0 (5/8). Not perfect.
- EXTEND(M_C), R0 = e0-5: (ADD,0,2) = e0+e2-5 {11,11,8,13 |
  10,10,9,8} 7/8 at t=11 is the best; (ADD,0,3) = e0+e3-5 6/8;
  (SUB,0,2), (SUB,0,3) 4/8; (MAX,0,2) 6/8; (MAX,0,3) 6/8;
  (MIN,0,3)=min(e0-5,e3) {1,1,0,0 | 0,0,0,0} 6/8; (ADD,0,0) same
  order as e0 5/8; (ADD,0,1)=e0 5/8; CPYs 4/8..6/8; d in 1..3 leave
  R0=e0-5, 5/8. None perfect.
- TRUNCATE(M_C) = e0: 5/8. SPECIALIZE(M_C): d=0 replacements are
  the round-1 candidates (max 7/8 = e0+e2); d in 1..3 leave R0=e0.
  None perfect.
- Global uniqueness: exactly one perfect (entry 0, EXTEND,
  (1,0,3)) across all entries, operators, and candidates.
- Learner cost: 80 adapt_evals (EXTEND of entry 0, first perfect
  (entry,op) in scan order). construct_evals delta = 0.

### 4b. RELAY phase audit (library holds M_A only)

- Exact probe entry 0: e0+e2 on RELAY train {14,8,11,9 | 9,11,11,8}:
  5/8 at t=12 (matches l3_transfer). Rejected.
- EXTEND(M_A), 80 candidates: best is (SUB,0,3) = (e0+e2)-e3
  {5,6,8,8 | 4,7,3,2} 7/8 at t=5; (SUB,0,1) = (e0+e2)-e1 6/8;
  (SUB,0,2) = e0 6/8; (ADD,0,2) = e0+2e2 5/8; (ADD,0,1) 4/8;
  (ADD,0,3) 4/8; (MAX,0,1) 5/8; (MIN,0,1) 4/8; CPYs 4/8..5/8;
  d in 1..3 leave R0=e0+e2, 5/8. None perfect.
- TRUNCATE(M_A) = e0: 6/8. Not perfect.
- SPECIALIZE(M_A): d=0 replacements are exactly the fresh round-1
  candidates on RELAY, whose unique 8/8 is (SUB,0,1) = e0-e1 with
  t=3 (l3_transfer frozen audit: baseline 6/8, gain 2). Adopted.
  d in 1..3 leave R0=e0, 6/8.
- Global uniqueness: exactly one perfect (entry 0, SPECIALIZE,
  position 0, (2,0,1)).
- Learner cost: 80 + 1 + 80 = 161 adapt_evals.

### 4c. FORAGE phase (frozen, l3_transfer)

Construction round 1: 80 evals, baseline 5/8, ADD R0,R2 unique 8/8,
gain 3, t=10. Round 2: 80 evals, no gain, stop. Totals: rounds=2,
evals=160. M_A program bytes [1,0,2], n=1, origin=FORAGE,
parent=255. A test 4/4.

### 4d. AEGIS test (ids 109..112)

With M=[ADD R0,R2, ADD R0,R3], t=16: 109: 9+8+0=17 alert ok;
110: 6+9+2=17 alert ok; 111: 8+7+0=15 calm ok; 112: 4+9+1=14 calm
ok. 4/4.
RELAY test with M=[SUB R0,R1], t=3: 4/4 (frozen, l3_transfer).

## 5. Frozen arms

- ARM-TRANSFER: one continuing learner state. Phase A FORAGE:
  lib_adapt origin=FORAGE (library empty; constructs; 160 evals;
  stores entry 0). Phase C RELAY: lib_adapt origin=RELAY (exact
  probe 5/8 rejected; EXTEND best 7/8; TRUNCATE 6/8; SPECIALIZE
  (2,0,1) 8/8 adopted; 161 adapt_evals; stores entry 1 with
  parent=0, pop=SPECIALIZE). Phase B AEGIS: lib_adapt origin=AEGIS
  (exact probes 7/8 and 5/8, none perfect; EXTEND of entry 0 finds
  (1,0,3) 8/8; 80 adapt_evals; zero construct_evals; stores entry 2
  with parent=0, pop=EXTEND).
- ARM-FRESH: fresh learner state, AEGIS only: lib_adapt
  origin=AEGIS (library empty; constructs from scratch: rounds=3,
  240 evals; invented entry program [1,0,2,1,0,3], origin=AEGIS,
  parent=255). Y prior fit asserted here: 6/6, t=16.
- ARM-NO-LIB: same as ARM-TRANSFER through phase C, then the
  library is wiped (LIBN=0, entries cleared), then AEGIS via
  lib_adapt origin=AEGIS (library empty; constructs from scratch;
  phase B construct_evals delta = 240). Causal ablation: the stored
  intermediate is what removes the B invention cost.

## 6. Kill bars

- T1 (determinism): 3 runs of the binary are byte identical
  (sha256 equal).
- T2 (invention in A): phase A lib_adapt code=1. Construct stats
  exactly: rounds=2, evals=160, base0=5, win=(1,0,2), gain=3,
  score=8, t=10. Round trace rwin[0]=(1,0,2,gain 3,score 8,t 10).
  Library entry 0 program bytes [1,0,2], n=1, origin=FORAGE,
  parent=255. A test 4/4.
- T3 (RELAY adaptation via SPECIALIZE): phase C exact probe of
  entry 0 on RELAY train = 5/8 (rejected, not reused). lib_adapt
  code=2, n_perfect=0, entry=0, op=SPECIALIZE(2), pos=0,
  instr=(2,0,1), t=3, score=8, adapt_evals=161. Library entry 1
  program bytes [2,0,1], n=1, origin=RELAY, parent=0,
  pop=SPECIALIZE. C test 4/4. Driver uniqueness audit: exactly one
  perfect (entry 0, SPECIALIZE, pos 0, (2,0,1)) on RELAY train.
- T4 (AEGIS adaptation via EXTEND, not reinvention): phase B exact
  probes: entry 0 score 7/8 t=16, entry 1 score 5/8, n_perfect=0.
  lib_adapt code=2, entry=0, op=EXTEND(0), instr=(1,0,3), t=16,
  score=8, adapt_evals=80. construct_evals delta across phase B ==
  0. M slot program bytes [1,0,2,1,0,3], n=2, threshold 16.
  Library entry 2 program bytes [1,0,2,1,0,3], n=2, origin=AEGIS,
  parent=0, pop=EXTEND. Provenance chain entry 2 -> entry 0
  (FORAGE, invented). B test 4/4. Driver uniqueness audit: exactly
  one perfect (entry 0, EXTEND, (1,0,3)) on AEGIS train.
- T5 (fresh baseline): ARM-FRESH lib_adapt code=1, construct
  rounds=3, evals=240. rwin[0]=(1,0,2,gain 2,score 7,t 16),
  rwin[1]=(1,0,3,gain 1,score 8,t 16). Invented entry program
  [1,0,2,1,0,3], n=2, origin=AEGIS, parent=255 (reinvented, not
  transferred). Y prior fit 6/6 t=16. B test 4/4.
- T6 (cheaper): transfer phase B adapt_evals (80) < fresh phase B
  construct_evals (240).
- T7 (library causal): ARM-NO-LIB phase B lib_adapt code=1,
  construct_evals delta = 240, invented origin=AEGIS, B test 4/4.
  Wiping the library restores the full invention cost.
- T8 (hygiene): 0 modes, 0 bridges, 0 handlers, 0 new semantic
  cases. Pure Zag for all research logic. Safebin PATH, no
  forbidden executables. Unfrozen scope only; frozen source
  untouched; paper untouched; nothing pushed; explicit pathspecs on
  every git add/commit; no em/en dashes in docs (byte verified).

Verdict L3-TRANSFER-ADAPT-COMPLETE requires T1..T8 all PASS with no
falsifier firing.

## 7. Falsifiers

- F-NO-INVENT-A: phase A construct stats deviate from section 4c.
- F-C-NOT-SPECIALIZE: phase C does not adapt via (entry 0,
  SPECIALIZE, pos 0, (2,0,1)) with 161 adapt_evals.
- F-C-EXACT-REUSE: phase C reuses an entry exactly (code 0).
- F-WRONG-ADAPT: phase B adapts any (entry, op, instr) other than
  (0, EXTEND, (1,0,3)).
- F-REINVENT-B: transfer phase B construct_evals delta > 0.
- F-ORIGIN: entry 2 parent != 0 or pop != EXTEND, or entry 0
  parent != 255.
- F-NO-SPEEDUP: transfer B adapt_evals >= fresh B construct_evals.
- F-NONUNIQUE: driver uniqueness audit finds != 1 perfect
  adaptation in phase B or phase C.
- F-OP-EXPAND: op basis extended beyond {CPY,ADD,SUB,MAX,MIN}.
  Voids the build.
- F-AUDIT: any section 8 pattern matches in learner.zag. Voids the
  build.
- F-NONDET: the three runs differ by one byte. Voids the build.
- F-PYTHON: any python/python3 invocation in the worker process
  tree. Voids the build.

## 8. Frozen grep audit spec (run on learner.zag)

Each pattern must return zero matches (grep -c == 0):
1. `e0+e2+e3` (the AEGIS solution expression)
2. `ADD R0,R3` (the adaptation instruction)
3. `9,5,7,1` (AEGIS episode data must not live in the learner)
4. `7,1,5,2` (FORAGE episode data must not live in the learner)
5. `5,0,9,9` (RELAY episode data must not live in the learner)
6. `_MODE` (zero modes allowed)
7. `bridge` (case insensitive; never used in code at all)

## 9. Determinism spec

No RNG. Fixed candidate order everywhere (op 0..4, d 0..3, s 0..3;
entries in library order; operators EXTEND, TRUNCATE, SPECIALIZE),
first max tie breaking, ascending threshold sweeps. Output via one
preallocated buffer and a single raw syscall write. 3/3 byte
identical required. Stdout byte verified (od -c spot check) before
trusting it.

## 10. Disclosed residual footprint and non claims

- The op basis, register machine, greedy construct(), and the three
  L2 operators are researcher supplied generic machinery, disclosed
  here. The claim is about the learner adapting a stored invented
  intermediate for a partially matching domain (evidence driven
  selection among entries and operators, cheaper than fresh
  invention, provenance recorded), not about the basis or operators.
- The adapted program [1,0,2,1,0,3] is byte identical to what fresh
  construction finds on AEGIS. This is expected (same optimum); the
  adaptation claim rests on path (adaptation scan, not
  construction), cost (80 vs 240 evals), and provenance
  (parent=entry 0, op=EXTEND), not on finding a different solution.
- The AEGIS and RELAY tables were designed by the builder, not an
  independent adversary. Sealed adversary generality (Micah C0-C) is
  open future work. Two adaptation instances do not establish broad
  generality.
- TRUNCATE is implemented and unit asserted in-binary on fixed
  programs, but no frozen learning domain exercises it; TRUNCATE as
  a learning operator is an explicit non-claim.
- This build does not claim Micah's full 12 criterion L3 bar.

## 11. Amendments (transparent, before the frozen evaluation runs)

(none)
