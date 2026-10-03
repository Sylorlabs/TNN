# PREREG: 5th-Pair Transfer -- Does the Unified Behavior-Contract Operation Handle Spatial-Layout x Task-Scheduling Unmodified?

Committed BEFORE any implementation. Frozen kill bars; no weakening after results.
Commit order: this prereg (plus NAMECHECK.md Step 0) strictly precedes all implementation.

## 1. Question

COMPOSE-COLLAPSE (verdict SUBSUMPTION, 2026-10-02) reduced H1 (learned typed
contracts) and H2 (value-level function composition) to ONE operation U:
behavior-contract composition (kind-set admission over observed input/output
kind bitmasks, ordered trial execution with end-to-end verification,
failure-triggered widening, success recording). The collapse battery used one
world family (navigation x aggregation style: walk chains + counting).

Question: does the SAME unmodified U handle a NOVEL domain pair not in the
original 4 (navigation x aggregation, arithmetic x planning,
causal x intervention, grammar x construction), or does the new pair require
domain-specific tweaks to the composition logic?

## 2. The 5th pair: spatial-layout x task-scheduling

- Domain X (spatial layout): "which team is worker w on" = WALK over
  relation 91 (member-of), worker -> team. NODE -> NODE.
- Domain Y (task scheduling): "how many pending tasks does team t have" =
  COUNT over relation 92 (has-task), team -> task count. NODE -> NUM.
- Composition Z: "pending task-load of worker w's team" = Y(X(w)).
  NODE -> NUM. Requires the ordered pair (X, Y); neither MAP alone suffices.

The logic U sees only integer facts, kind bitmasks (1=NODE iff the value
appears as a fact subject, else 2=NUM), and the MAP table. If U smuggled any
domain assumption (relation numbers, entity ranges, kind-flow direction), the
new pair exposes it.

## 3. Frozen worlds (all facts fixed here)

Relations: 91 member-of, 92 has-task, 93 zone-of.
Entities: workers 201..206, teams 211..213, zones 221..222,
tasks 901..906 (objects only, hence NUM).

Facts (shared by Q0/Q1/Q4; Q2/Q3 use the same facts with reduced MAP tables):
- member-of (91): (201,91,211),(202,91,211),(203,91,212),(204,91,212),
  (205,91,213),(206,91,213)
- has-task (92): (211,92,901),(211,92,902),(211,92,903),
  (212,92,904),(212,92,905),(213,92,906)
- zone-of (93): (211,93,221),(212,93,221),(213,93,222),
  (221,93,221),(222,93,222)
  The zone self-loops are a deliberate world-construction choice: kind probing
  is subject-based, so zones need subject-hood to probe as NODE (reflexive
  containment). Documented here, frozen; not a logic tweak.

MAP inventory (4 MAPs):
- m0 = X: class 0 WALK, rel 91 (spatial: worker -> team)
- m1 = Y: class 1 COUNT, rel 92 (scheduling: team -> pending-task count)
- m2: class 3 IDENT (distractor)
- m3: class 0 WALK, rel 93 (distractor: team -> zone)

Teaching (independent, disjoint fact sets, all BEFORE any Z query):
- m0 (spatial only): teach(201->211), teach(203->212).
  Contract: inmask=1, outmask=1, nobs=2.
- m1 (scheduling only): teach(211->3), teach(212->2).
  Contract: inmask=1, outmask=2, nobs=2.
- m2: teach(201->201). Contract: inmask=1, outmask=1, nobs=1.
- m3: teach(211->221), teach(212->221).
  Contract: inmask=1, outmask=1, nobs=2.

## 4. Frozen queries and predictions

One TRIAL = one single-MAP execution or one ordered-pair pipeline execution.
3/3 byte-identical runs. Arm label UNI5 (the unmodified U).

- Q0 CENSUS (pre-Z, proves K1): census printed after teaching, before any
  Z query. Predicted lines:
  CENSUS m=0 inmask=1 outmask=1 n=2
  CENSUS m=1 inmask=1 outmask=2 n=2
  CENSUS m=2 inmask=1 outmask=1 n=1
  CENSUS m=3 inmask=1 outmask=1 n=2

- Q1 Z1 (taught, intact table): s=205, kin=1, kout=2, exp=1.
  Admission: singles: m1 admitted (in{1} out{2} compatible), fails
  (count(205,92)=0 -> -2); m0/m2/m3 rejected (out{1} vs kout 2).
  Pairs: (m0,m1) admitted (1 x {1} x 2); v1=walkf(205,91)=213, v2=1.
  Predicted: ANS=1 TRIES=2, exactly one INTER=213 line.

- Q2 Z-ABLATE-X (MAP table without m0; ids: 0=Y,1=IDENT,2=WALK93):
  s=205, kin=1, kout=2, exp=1.
  Singles: m0(Y) admitted, fails. Pairs admitted: (1,0) fails
  (v2=-2), (2,0) fails (v1=-2). WIDEN=1 fires; 4 rejected pairs retried,
  all fail.
  Predicted: ANS=-2 TRIES=7, WIDEN=1 present.

- Q3 Z-ABLATE-Y (MAP table without m1; ids: 0=X,1=IDENT,2=WALK93):
  s=205, kin=1, kout=2, exp=1.
  Singles: none admitted. Pairs: none admitted. WIDEN=1 fires; 6 rejected
  pairs retried, all fail (INTER sequence 213,213,205,205,-2,-2).
  Predicted: ANS=-2 TRIES=6, WIDEN=1 present.

- Q4 Z-FRESH (full 4-MAP table, NO teaching: all masks 0, nobs 0):
  s=205, kin=1, kout=2, exp=1.
  All 4 singles admitted (empty mask = compatible), all fail; first pair
  (0,1) succeeds: v1=213, v2=1.
  Predicted: ANS=1 TRIES=5, exactly one INTER=213 line.

## 5. Frozen kill bars

- K1 INDEPENDENT X,Y BEFORE Z: PASS iff the Q0 census (printed before any Z
  query in program order) shows m0 inmask=1 outmask=1 n=2 AND m1 inmask=1
  outmask=2 n=2, with the teaching calls of Section 3 (disjoint subject sets:
  workers for X, teams for Y) executed before the first uni_solve call.
- K2 CAUSAL DEPENDENCE: PASS iff Q1 ANS=1 AND Q2 ANS=-2 AND Q3 ANS=-2.
  (Removing either MAP breaks Z.)
- K3 UNMODIFIED LOGIC: PASS iff (a) the assembled p5_full.zag consists of
  ref_uc_base.zag byte-identical + ref_uc_uni.zag byte-identical (main
  excluded) + one new section (pair-5 setup + main), verified by extracting
  the regions and diffing against the reference files with EMPTY diff;
  (b) the new section contains no changes to admission, execution, widening,
  recording, or contract logic; (c) relation constants 91/92/93 and domain
  vocabulary appear ONLY in the new section.
- K4 DETERMINISM: PASS iff 3/3 runs produce byte-identical stdout; sha256
  digests recorded.
- K5 FRESH-LEARNER COST: PASS iff Q4 (fresh) solves Z with
  TRIES >= 2 * Q1 TRIES (predicted 5 >= 4). The learned contracts must
  materially reduce search on the new pair.
- K6 NO DOMAIN-PAIR TEMPLATE: PASS iff source audit shows zero new behavior
  classes, zero new opcodes, zero relation-conditional branches; the domain
  enters only as integer constants inside fact_add/map_new/teach calls in
  the setup function.

## 6. Verdict mapping (frozen)

- K1-K6 all PASS: BUILD-PASS. The unmodified unified operation handles the
  5th pair; composition is domain-blind (integer facts + kind bitmasks +
  MAP tables only).
- K3 FAILS (a logic tweak was required to pass Q1): BUILD-FAIL. The exact
  tweak is documented as the informative failure: the unified operation is
  NOT domain-general without that change.
- K2 FAILS (Z solvable with X or Y removed): BUILD-FAIL (vacuous world
  design; composition not actually exercised).
- K1/K5/K6 FAIL: BUILD-FAIL on that bar, cause stated.
- K4 FAILS (nondeterminism): UNDECIDED; decisive rerun named.

## 7. Honest boundaries (pre-declared)

- Behaviors (WALK/COUNT/IDENT) installed as previously-learned MAPs; behavior
  induction not under test (same standing as canonical H1/H2 and the
  collapse battery).
- Expected-answer verification of final acceptance (canonical boundary).
- 4-MAP inventory; one canonical composition query plus two ablations plus
  one fresh-learner cost query. No widening-stress case on the new pair
  (widening already discriminated on the original battery, P2b).
- Chain geometry only; the planning-composition frontier (SUM to PLAN)
  remains out of scope.
- The zone self-loop facts are a documented world-construction choice for
  kind probing, not a logic change (K3 diff covers this).

## 8. Implementation plan (frozen order)

1. Copy compose_collapse/uc_base.zag and uc_uni.zag as ref_uc_base.zag and
   ref_uc_uni.zag (read-only references for the K3 diff).
2. Write pair5_new.zag: setup functions (shared facts, taught/abx/aby/fresh
   MAP variants) + main (Q0 census, Q1..Q4, report lines).
3. Assemble p5_full.zag = ref_uc_base.zag + (ref_uc_uni.zag minus main) +
   pair5_new.zag, via cat/sed. Verify region boundaries; diff each copied
   region against its reference (must be empty).
4. Compile with the pinned safebin znc; run 3x; sha256 the outputs;
   byte-compare.
5. K3/K6 audits (diff, grep). REPORT.md with BUILD-PASS/FAIL per Section 6.

Zag pitfalls (from the collapse battery, apply here): no `as *i32` + slice
construction in functions (use the z_alloc []u8 pattern already in the base);
no _zag_print for dynamic content (single preallocated buffer, cursor
helpers, one _zag_raw_syscall flush; verify stdout bytes); if-nesting at
most 3 (new code has none); no `!(A && B)` in while conditions (new code has
none).
