# PREREG: SUBSUMPTION-P0 (contract module vs COGOPS procedure composition)

Status: PREREG-FROZEN. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/subsumption_p0/` only.
Worker: SUBSUMPTION-P0 worker (subagent, 2026-10-03).
Parent mandate: COMPOSITION-SYNTHESIS (C436) P0 experiment. This decides
whether TNN has ONE composition mechanism or two.

Commit order: this prereg (plus NAMECHECK.md Step 0) strictly precedes
all implementation. No implementation file exists in this lane at this
commit.

## 1. Question and predicted outcome

COMPOSITION-SYNTHESIS (C436) established one live general mechanism for
learned-structure composition: the unified 5-operation contract module
of CONTRACT-UNIFICATION (C424, SUBSUMES), which absorbed GEN, LCONT,
and FC. One lane was never tested against it: COGOPS procedure
composition (C417 2-way, C422 3-way, C433 diamond), which composes
learner-owned procedure bodies via trial-learned bindings and topo
assembly. "One mechanism" is therefore justified only for MAP/contract
composition, not for procedures.

Question: can the frozen C424 5-op module (induct/check/grow/invalidate/
revise) reproduce COGOPS-DIAMOND's results (goals 813/814/815/808, plus
the 810 decline control), or does procedure composition require distinct
machinery?

PREDICTED OUTCOME (frozen): INFORMATIVE-FAIL / PARTIAL SUBSUMPTION.
The module subsumes the judgment halves of COGOPS composition
(trial-learned bindings as per-tag admission contracts, version
routing as coverage admission, principled decline as contract
abstention, plus binding/coverage revision which C433 lacks), but it
cannot subsume plan assembly, procedure execution, or step
verification. Procedure composition requires distinct machinery: an
ordering/plumbing mechanism and an executor over procedure bodies.
Verdict: TWO mechanisms. The 5-op module stays the one mechanism for
learned-structure (contract) composition; COGOPS procedure composition
is a second, distinct mechanism. Section 9 states the exact boundary
with proofs.

## 2. The module under test (frozen, not reimplemented)

The module is C424's u_* section, byte-copied verbatim from the
committed `contract_unify/cu_full.zag` (lines 55-389: the unified
contract module section, through the end of u_revise). Byte-identity
is verified by cmp during the build (K7). The module is not modified,
extended, or reimplemented. Its op signatures and codomains:

- u_induct(S,cbase): judgment table -> clause set. Returns 1/0.
  Writes clauses, CONTRACT_SET, NFIELDS, NCLAUSES, C_FIT_ERR.
  Returns 0 (no contract) when the accept set is empty.
- u_check(S,cbase,nf,f0..f5): integer vector -> {0,1} judgment.
  1 iff nf matches and at least one active clause exists and every
  active clause holds; 0 otherwise (empty active set judges 0).
- u_grow(S,cbase,f0..f5): (clauses, vector) -> widened clauses. void.
- u_invalidate(S,cbase,judgment,consequence): (judgment, consequence)
  -> ok in {0,1}; bumps fail run and per-clause disconfirmation
  counters; retires clauses at dc >= 2; latches revision request at
  fail run >= 3. Counters are global (slots 900-925).
- u_revise(S,cbase,enabled): latched request -> re-induct on the
  current table; records C_OLDERR_ON_NEW and C_REV_COUNT.

Clause language (frozen): (field, xform, k, lo, hi, active, dc) with
xform in {identity, div-by-k, mod-by-k}, k in {2,4,8,16,32}. Each
clause is a range test on ONE feature of ONE field. A contract is a
conjunction of at most 2 clauses (induct searches cardinality 1,
then 2). Induct's bias (frozen): fewer clauses, then maximal total
accept-region width, then lowest (field, feature) on ties.

Structural facts used by the predictions (read off the frozen source,
not asserted):
(S1) No op produces a value: every op returns a clause set, a
     {0,1} judgment, void, or a counter. There is no executor.
(S2) No op produces or orders a sequence: induct needs evidence;
     check judges a given vector. There is no planner / topo.
(S3) Clauses are per-field ranges: correctness that correlates
     fields (relational constraints) is inexpressible (proof in
     section 9).

## 3. The COGOPS behaviors under test (from C433, frozen)

From `cogops_diamond/REPORT.md` (commit-verified results):
- Trial-learned bindings: 801 -> RETRIEVE (fam 0), 802 -> VERIFY
  (fam 1), 807 -> COUNT (fam 2), with per-family ok/fail counts;
  811 -> no family (fam = -1), principled decline.
- Version selection from learned coverage: per need, specialized
  vs generic version at execution time (e.g. 813/814 run
  vers = [2,3,3,5]; 815 runs [0,1,1,4] with cleared coverages and
  [0,1,1,5] after count re-specialization on B).
- Per-goal plans by topo order over goal links: diamond goals
  assemble [0:801:0] [2:802:1] [1:802:1] [3:807:2]; chain 808
  assembles [0:801:0] [1:802:1] [2:807:2]. Same bindings produce
  diamond and chain plans (shape dissociation).
- Diamond execution with intermediate values: E0 (813)
  ans = 7:1,611,0,1,611,1,2 vers = [2,3,3,5] cs = 96 cg = 336;
  E1 (814) ans = 8:1,611,1,611,1,611,1,2 vers = [2,3,3,5]
  cs = 112 cg = 392; R0 (808) ans = 6:1,613,1,613,1,2
  vers = [2,3,5] cs = 64 cg = 224; B0/B1/S8 (815)
  ans = 7:1,713,0,1,713,1,2. Totals: agree = 6/6, cs = 944,
  cg = 1672 (1.77x).
- Plan persist / reuse / re-derive: plans_built = 5,
  plans_loaded = 1, rederive_match = 1 after wiping plans and
  bindings.
- Principled decline: goal 810 (need tag 811) declined, no plan,
  trials = 21 total.

The battery tests the actual C433 goals: goal records are built by
byte-copied constructors from `cogops_diamond/c4_world.zag`
(mk_goal813_E0, mk_goal814_E1, mk_goal815_B0, mk_goal808_A0,
mk_goal810 with the w_* helpers), and the harness reads need tags,
goal tags, and link structure from those records. Trial evidence and
execution traces are C433's frozen committed data (REPORT.md),
reproduced below as frozen tables.

## 4. Arm B1: bindings as admission contracts (predicted PASS)

Design: each need tag gets one binding contract over [tag, fam]
(nf = 2). Trial evidence (frozen, from C433 REPORT K3c):
- 801: accepts [[801,0]]; rejects [[801,1],[801,2]]
- 802: accepts [[802,1]]; rejects [[802,0],[802,2]]
- 807: accepts [[807,2]]; rejects [[807,0],[807,1]]
- 811: accepts []; rejects [[811,0],[811,1],[811,2]]

Hand derivations (1-clause search; field 0 clauses invalid because
rejects share the tag value; field 1 = fam):
- 801: valid 1-clauses are (1,identity,[0,0]), (1,mod4,[0,0]),
  (1,mod8,[0,0]), (1,mod16,[0,0]), (1,mod32,[0,0]), all width 0;
  tiebreak (lowest field, feature) picks (1,identity,[0,0]).
- 802: valid 1-clauses include (1,identity,[1,1]) (width 0) and the
  mod variants; tiebreak picks (1,identity,[1,1]).
- 807: tiebreak picks (1,identity,[2,2]).
- 811: na == 0, u_induct returns 0, CONTRACT_SET stays 0.

Frozen predictions:
- CB801: induct = 1; clause (field=1, xform=identity, k=0, lo=0,
  hi=0); CONTRACT_SET = 1; NFIELDS = 2; NCLAUSES = 1;
  C_FIT_ERR = 0.
- CB802: induct = 1; clause (1,identity,[1,1]).
- CB807: induct = 1; clause (1,identity,[2,2]).
- CB811: induct = 0; CONTRACT_SET = 0.
- Routing: check(CB801,2,801,0) = 1; check(CB801,2,801,1) = 0;
  check(CB801,2,801,2) = 0; check(CB802,2,802,1) = 1;
  check(CB802,2,802,0) = 0; check(CB802,2,802,2) = 0;
  check(CB807,2,807,2) = 1; check(CB807,2,807,0) = 0;
  check(CB807,2,807,1) = 0.
- Decline: check(CB811,2,811,0) = 0; goal 810's need (tag 811)
  unbindable on every family: DECLINE = 1.
- Revision demo (scratch contract CB802R, inducted as CB802, global
  counters zeroed first, slot 908 preset to -1, slot 7 set to 3):
  u_invalidate(CB802R,1,0) twice: fail run 1, 2; clause dc 1, 2;
  at dc = 2 the clause retires (active = 0);
  check(CB802R,2,802,1) = 0. Third u_invalidate(CB802R,1,0):
  fail run = 3, C_REV_REQ = 1, C_FIRST_DETECT_Q = 3.
  Load new table (accepts [[802,2]], rejects [[802,0],[802,1]]);
  u_revise(CB802R,1): C_OLDERR_ON_NEW = 2 (old clause errs on the
  new accept and on reject [802,1]); re-induct writes
  (1,identity,[2,2]); C_REV_COUNT = 1; req = 0; run = 0.
  check(CB802R,2,802,2) = 1; check(CB802R,2,802,1) = 0.
  This is machinery C433 lacks: binding revision after
  counterevidence.

## 5. Arm B2: version routing as coverage admission (predicted PASS)

Design: per-procedure coverage contracts over [rel] (nf = 1).
Frozen training evidence (from C433 REPORT learner state: LSTATE-RET
after S1A covers relations 601, 602):
- RET-spec coverage: accepts [[601],[602]];
  rejects [[603],[607],[609],[701],[702],[707]].
Hand derivation: valid 1-clauses are (0,identity,[601,602]) width 1,
(0,mod16,[9,10]) width 1, (0,mod32,[25,26]) width 1 (div variants
invalid: 603/2 = 301 in [300,301], etc.); tiebreak picks
(0,identity,[601,602]).
Frozen predictions:
- CBCOV: induct = 1; clause (0,identity,[601,602]);
  check(CBCOV,1,601) = 1 (route spec); check(CBCOV,1,602) = 1;
  check(CBCOV,1,603) = 0 (route gen); check(CBCOV,1,701) = 0.
- Coverage revision demo (global counters zeroed, 908 preset -1,
  slot 7 = 5): three u_invalidate(CBCOV,1,0) (world-B shift:
  spec no longer covers 601): clause retires at dc = 2;
  fail run = 3 latches req. Load new table
  (accepts [[701],[702]], rejects [[601],[602],[603],[607],[609],
  [707]]); u_revise(CBCOV,1): C_OLDERR_ON_NEW = 4 (old clause
  errs on both new accepts and on rejects [601],[602]);
  re-induct writes (0,identity,[701,702]) (tiebreak over
  (0,mod16,[13,14]) and (0,mod32,[29,30]), all width 1);
  C_REV_COUNT = 1. check(CBCOV,1,701) = 1; check(CBCOV,1,601) = 0.
What this shows: the version *routing decision* (spec vs gen from
learned coverage, revised under drift) is contract machinery. The
execution benefit (cs < cg) is not: it lives in the procedure
bodies, which the module cannot run (Arm E).

## 6. Arm V: procedure step verification (predicted FAIL)

Design: induct per-procedure step contracts from episode-derived
step records, then u_check each frozen C433 trace step. If the
module can verify procedure executions, this is internal
verification without an oracle (overnight priority 4).

Frozen training tables (accepts = true steps from C433's S1
episodes and world facts; rejects = the mistake classes a
verifier must catch: same query / wrong value, same value /
wrong query; every reject is field-wise covered by accepts,
see proof in section 9):

RET (nf = 3, [rel, obj, subj]):
accepts: [601,623,613] [602,625,614] [601,621,611] [602,622,611]
rejects: [601,623,611] [602,625,611] [601,621,613] [602,622,614]
         [601,625,614] [602,623,613]

VFY (nf = 5, [subj, step, rel, obj, pass]):
accepts: [611,0,601,621,1] [611,1,602,622,1] [612,0,603,621,1]
         [612,1,601,622,1] [613,0,602,624,1] [613,1,603,622,1]
         [614,0,601,624,1] [614,1,603,629,0]
rejects: [611,0,601,621,0] [611,0,601,622,1] [612,0,603,621,0]
         [614,1,603,629,1] [613,0,602,624,0] [612,1,602,622,1]

CNT (nf = 3, [rel, subj, count]):
accepts: [601,611,2] [602,611,2] [603,612,2] [601,613,2]
         [607,631,1] [701,711,2] [702,713,2]
rejects: [601,611,1] [607,631,2] [602,611,1] [601,613,1]
         [701,711,1] [603,612,1]

Frozen trace steps to check (from C433 REPORT per-query detail):
RET: [601,621,611] [601,621,611] [601,623,613] [701,723,713]
     [701,723,713] [701,723,713]
VFY: [611,0,602,629,0] [611,0,602,622,1] [611,1,603,620,1]
     [611,0,603,620,1] [611,1,601,631,1] [611,0,601,621,1]
     [611,1,602,622,1] [613,0,602,624,1] [613,1,603,622,1]
     [713,0,702,729,0] [713,0,702,724,1] [713,1,701,723,1]
     [713,0,702,729,0] [713,0,702,724,1] [713,1,701,723,1]
     [713,0,702,729,0] [713,0,702,724,1] [713,1,701,723,1]
CNT: [603,611,2] [601,611,2] [601,613,2] [701,713,2]
     [701,713,2] [701,713,2]

Frozen predictions:
- u_induct on all three tables returns 0 (no valid clause set of
  any cardinality; proof in section 9). CONTRACT_SET = 0 for
  CBRET, CBVFY, CBCNT.
- Every trace-step u_check returns 0 (principled abstention: the
  module declines to verify rather than hallucinating).
- Corruption spot checks (e.g. RET [601,621,612], VFY
  [611,0,602,622,0], CNT [603,611,3]) also return 0: abstention
  is uniform, not selective.
Arm V verdict: FAIL. The module cannot verify procedure steps.
The gap is in the clause *language*, not just missing execution:
per-field range clauses cannot express the relational content of
procedure I/O (section 9).

## 7. Arm E: end-to-end generation attempt (predicted FAIL)

Design: for each actual C433 goal (813, 814, 808, 815, 810; records
built by the byte-copied constructors), the driver attempts to
produce a plan and an answer using ONLY the five module ops. The
harness may read goal records (need tags, goal tags, links) as data;
it may not contain ordering, execution, or plan-record machinery
(K7 audits this).

Protocol per goal:
(E-a) Bind each need via the Arm B1 contracts (u_check). Log
      need tag -> family (or UNBOUND).
(E-b) Plan generation attempt: call u_induct on an empty judgment
      table at a scratch base. Log the return (predicted 0:
      induct requires evidence; plan evidence does not exist
      before planning; the module has no generation op).
(E-c) Answer generation attempt: no module op has a value in its
      codomain (S1). Log ANS_VALUE_SOURCE = none.
(E-d) Per-need output query: attempt to obtain need0's output
      subject via the module. Log UNAVAILABLE.

Frozen predictions: for all five goals, PLAN = none, ANS = none;
every attempt logs its structural block. Arm E verdict: FAIL.
The module cannot generate plans or answers. Combined with Arm V,
the boundary is: the module judges given vectors; it neither
produces values nor orders steps. (Arm F, next, shows the only
module-only path to the answers and why it is not composition.)

## 8. Arm F: flat-memorization control (predicted: answers via
lookup, composition criteria FAIL)

Design: per-goal tag contracts over [tag] (nf = 1), inducted from
supervised goal labels. Frozen: accepts [[813]] rejects
[[814],[808],[815],[810]] inducts (0,identity,[813,813]); likewise
(0,identity,[814,814]), (0,identity,[808,808]),
(0,identity,[815,815]), (0,identity,[810,810]).
Frozen predictions:
- check(CB813,1,813) = 1; check(CB813,1,814) = 0; etc.
- With the harness mapping each recognized tag to C433's frozen
  answer (813 -> 7:1,611,0,1,611,1,2; 814 -> 8:1,611,1,611,1,611,1,2;
  808 -> 6:1,613,1,613,1,2; 815 -> 7:1,713,0,1,713,1,2), all five
  answers are "reproduced". This reproduction is logged
  explicitly as NON-COMPOSITIONAL (the answers were supplied, not
  computed; the harness lookup is the researcher smuggling the
  execution).
- Composition criteria all fail: no procedure contracts are shared
  across goals (each goal's contract mentions only its own tag);
  no plan exists; no version selection; novel tag 816 ->
  check = 0 on every contract (no generalization).
Arm F verdict: the module can memorize goal->answer mappings, not
compose. This is the control that makes Arm E's FAIL sharp: the
only module-only route to the answers is supervised memorization,
which satisfies none of C433's composition observables (shared
bindings, per-goal plans, version selection, re-derivation).

## 9. The boundary (frozen analysis)

Three independent gaps, each sufficient:

(G1) No value production (S1). Every module op returns clauses,
{0,1}, void, or counters. COGOPS execution computes intermediate
values (P1 = [611], P2 = [], counts). Nothing in the module can
emit 611 or 2. Arm E demonstrates this.

(G2) No ordering/generation (S2). Plans are per-goal topo orders
over link structure ([0,2,1,3] for diamonds, [0,1,2] for the
chain). induct learns from evidence; check judges given vectors.
Neither generates or orders sequences. Arm E demonstrates this.

(G3) Clause language cannot express relational I/O (S3). Proof:
a clause is a range test on f(v) for one field, where f is a fixed
deterministic function of the field value (identity/div/mod).
Let R be a reject whose every field value occurs in some accept
(not necessarily the same accept). For any clause covering all
accepts, f(R.field) = f(some accept's field) is inside the
accepts' range, so R satisfies the clause. Hence R satisfies every
conjunction of such clauses covering the accepts, so no valid
clause set of any cardinality exists. All three Arm V reject sets
are constructed field-wise covered (verified value by value in
section 6), so no step contract can be inducted. Procedure I/O
correctness ("this triple is a world fact", "this count matches
the distinct objects") is inherently relational; the module's
contract language is intra-record arithmetic. This is why C424's
scenarios (drift law s2 >= 2; grammar mod-32) subsumed and
procedure steps do not.

What subsumes (Arms B1/B2): bindings and version routing are
admission judgments over small integer vectors, which is exactly
the module's vocabulary; invalidate/revise add revision, which
C433 lacks. What does not: plan assembly (G2), execution (G1),
step verification (G3). The composition of *procedures* needs an
ordering mechanism and an executor over procedure bodies, plus a
contract language that can express relational I/O if verification
is wanted. The 5-op module is therefore ONE mechanism for
learned-structure (contract) composition and NOT a mechanism for
procedure composition. Two mechanisms.

## 10. Kill bars (frozen)

- K1 (B1): clauses exactly (1,identity,[0,0]), (1,identity,[1,1]),
  (1,identity,[2,2]); CB811 induct = 0, CONTRACT_SET = 0; all 9
  routing checks as in section 4; goal 810 DECLINE = 1; revision
  demo: C_OLDERR_ON_NEW = 2, C_REV_COUNT = 1, new clause
  (1,identity,[2,2]), routing flipped (802,2) = 1, (802,1) = 0.
- K2 (B2): clause (0,identity,[601,602]); routing checks as in
  section 5; revision: C_OLDERR_ON_NEW = 4, C_REV_COUNT = 1, new
  clause (0,identity,[701,702]); routing flipped.
- K3 (V): all three step inducts return 0 with CONTRACT_SET = 0;
  all 30 trace-step checks return 0; all corruption spot checks
  return 0.
- K4 (E): PLAN = none and ANS = none for goals 813, 814, 808,
  815, 810; E-a bindings logged; E-b/E-c/E-d blocks logged.
- K5 (F): five tag contracts (0,identity,[tag,tag]); answers
  reproduced only via the logged non-compositional harness
  lookup; tag 816 checks 0 on all five; no shared procedure
  contracts (each contract's clause mentions only its goal tag).
- K6: 3/3 runs byte-identical stdout (sha256 equal); stderr empty.
- K7: toolchain: safebin PATH for every command; `which python3`
  and `which python` return nothing; zero forbidden-executable
  invocations; all computation pure Zag via the pinned znc; shell
  only for znc/binary/run/verify/git.
- K8: hygiene: the u_* section byte-identical to C424's
  (cmp-verified); the harness contains no topo sort, no
  procedure executor, no plan records (source audit in REPORT);
  opaque integer identifiers only; zero em/en dash bytes in
  lane docs (byte-verified).

## 11. Falsification criteria (frozen)

- F1: if Arm E emits a plan or an answer value for any goal
  through the five module ops, the structural analysis (S1/S2)
  is wrong; the verdict flips toward SUBSUMES and the prereg's
  prediction is recorded as falsified, not amended.
- F2: if any Arm V step induct returns 1 AND its checks verify
  the frozen trace steps while returning 0 on the corruption
  spot checks, the language gap (G3) is smaller than proved;
  re-evaluate (the proof's field-wise-coverage premise would
  have to be rechecked first).
- F3: if the harness is found to contain ordering, execution, or
  plan-record machinery (anything that does COGOPS's job for
  it), the test is VOID: the battery would not be testing the
  module. The REPORT must include the audit.

A PARTIAL/FAIL here is the informative outcome, not a defect: it
maps exactly where contract machinery ends and procedure
machinery begins.

## 12. Honest bounds (not claimed)

- The battery tests the C424 module against C433's diamond
  results; C417 (2-way) and C422 (3-way) behaviors are covered
  only insofar as C433's battery already includes the chain
  regression (808) and the same binding/version machinery.
- u_grow is not exercised (as in C424).
- The direction of the partial absorption is documented, not
  decided: bindings/version-routing are contract jobs; plans
  and execution are not. Governance decides the landing.
- One frozen module, five frozen goals, frozen tables. No broad
  generality claim.

## 13. Build and run plan (post prereg)

Files (prefix `sp_`), all pure Zag:
- `sp_base.zag`: byte-copy of cu_full.zag lines 1-54 (header +
  generic machinery: z_alloc, get32/set32, sg/ss, e1str/e1i64).
- `sp_module.zag`: byte-copy of cu_full.zag lines 55-389 (the
  frozen u_* module). cmp-verified identical.
- `sp_world.zag`: byte-copy of the w_* helpers and the five goal
  constructors from cogops_diamond/c4_world.zag (lines 90-103,
  105-..., 248-314). cmp-verified identical.
- `sp_harness.zag`: table loaders, arm drivers B1/B2/V/E/F,
  main. New code; contains no topo, no executor, no plan
  records (audited for K8).
- `sp_full.zag`: concatenation of the four (exactly one
  `fn main`).
- `sp_build.sh`: assemble + compile with the pinned safebin znc.
Arena: contract bases at 2000+ (100-int spacing; 13 contracts);
judgment table and scratch at the module's fixed slots (300-302,
304+, 528+, 900-925, 1200-1209); slot 7 as the query counter.
Build: `znc sp_full.zag -o sp_bin`. Run 3x, sha256sum compare,
stderr must be empty. Write REPORT.md. Commits: implementation
first, then REPORT, each with explicit pathspecs; local only,
never pushed.
