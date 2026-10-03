# REPORT: SUBSUMPTION-P0 (contract module vs COGOPS procedure composition)

Date: 2026-10-03. Worker: SUBSUMPTION-P0.
Lane: `docs/lab/research-lead/overnight-20260928/subsumption_p0/`
Prereg: commit 180496211 (PREREG.md + NAMECHECK.md, committed alone
before any implementation file existed). Implementation commit
follows this report.

## Verdict: INFORMATIVE-FAIL / PARTIAL SUBSUMPTION: TWO mechanisms

The frozen C424 5-op contract module (induct/check/grow/invalidate/
revise, byte-copied verbatim) does NOT subsume COGOPS procedure
composition. It subsumes the judgment halves: trial-learned bindings
as per-tag admission contracts (Arm B1 PASS), version routing as
coverage admission (Arm B2 PASS), principled decline as contract
abstention (B1 PASS), plus binding/coverage revision which C433
lacks. It cannot subsume plan assembly (Arm E FAIL, as predicted),
procedure execution (Arm E FAIL, as predicted), or procedure-step
verification (Arm V FAIL, as predicted). The flat-memorization
control (Arm F) shows the only module-only route to C433's answers
is supervised lookup, which satisfies none of the composition
criteria.

Every frozen numeric prediction matched exactly. No falsification
criterion fired. The predicted outcome in PREREG section 1 is
confirmed without amendment.

**Answer to the parent's question: TNN has TWO composition
mechanisms.** The unified 5-op contract module is one mechanism for
learned-structure (contract) composition. COGOPS procedure
composition requires a second, distinct mechanism: an ordering /
plumbing mechanism over goal structure plus an executor over
procedure bodies. "One mechanism" is true for contracts, false for
procedures. Section "The boundary" states exactly what the contract
module lacks.

## What was built

- `sp_base.zag`: byte-copy of cu_full.zag lines 1-54 (generic
  machinery). cmp-verified identical.
- `sp_module.zag`: byte-copy of cu_full.zag lines 55-389 (the frozen
  u_* module under test). cmp-verified identical before and after
  the runs. Zero modifications.
- `sp_world.zag`: byte-copy of the w_* helpers and the five C433
  goal constructors (mk_goal813_E0, mk_goal814_E1, mk_goal815_B0,
  mk_goal808_A0, mk_goal810) from cogops_diamond/c4_world.zag.
- `sp_harness.zag`: new code (544 lines): frozen table loaders,
  five arm drivers, goal-record readers, main. Audited: no topo
  sort, no procedure executor, no plan records, no fact-table
  access (the only audit match is the comment declaring the
  absence).
- `sp_full.zag`: concatenation (exactly one `fn main`).
- `sp_build.sh`, `sp_bin`, `sp_compile.txt`,
  `sp_run1/2/3.txt` (sha256
  5ab9b76d187bc3ab551ab4f7f7c6b501ef1eeab01548d100426af87841d048cd)
  + `.err` (empty).

## Evidence (from sp_run1.txt; runs 2/3 byte-identical)

Arm B1 (bindings; predicted PASS): 801 induct=1 clause
(field=1,identity,[0,0]) routing 1/0/0; 802 clause
(1,identity,[1,1]) routing 0/1/0; 807 clause (1,identity,[2,2])
routing 0/0/1; 811 induct=0 CONTRACT_SET=0 DECLINE=1. Revision demo
on the 802 binding: two invalidations retire the clause (dc=2,
active=0, check goes 0); third latches req=1 first_detect=3;
re-induct on the new table gives (1,identity,[2,2]) with
olderr=2 revcount=1 and flipped routing. All exactly as frozen.

Arm B2 (version routing; predicted PASS): coverage contract
(0,identity,[601,602]); routing 601=1 602=1 603=0 701=0. Coverage
revision under the world-B shift: clause retired at dc=2, req
latched at run=3, re-induct gives (0,identity,[701,702]) with
olderr=4 revcount=1; routing flipped 701=1 601=0. All exactly as
frozen. The version *routing decision* (spec vs gen from learned
coverage, revised under drift) is contract machinery; the
execution benefit (cs < cg) lives in the procedure bodies.

Arm V (step verification; predicted FAIL): all three step-contract
inducts return 0 with CONTRACT_SET=0 (no valid clause set of any
cardinality, as proved in PREREG section 9). All 30 frozen C433
trace-step checks return 0 (principled abstention); all corruption
spot checks return 0 (abstention is uniform, not selective). The
module declines to verify procedure steps rather than
hallucinating. The gap is in the clause *language*: per-field
range clauses over intra-record arithmetic features cannot express
the relational content of procedure I/O ("this triple is a world
fact", "this count matches the distinct objects").

Arm E (generation attempt; predicted FAIL): for each actual C433
goal (813, 814, 808, 815 read from the byte-copied constructors;
810 the decline control): E-a binds every need through the B1
contracts (801->0, 802->1, 807->2; 811->UNBOUND); E-b plan
induct on empty evidence returns 0; E-c/E-d log
ANS_VALUE_SOURCE=none and NEED0_OUTPUT=UNAVAILABLE (no module op
has a value in its codomain); PLAN=none ANS=none for all five
goals. The module judges given vectors; it neither produces
values nor orders steps.

Arm F (flat-memorization control; predicted as stated): five tag
contracts (0,identity,[tag,tag]) recognize their goal (RECOG=1,
XREJ=0) and reject the novel tag 816 (=0). Answers are reproduced
only through the explicitly logged NONCOMPOSITIONAL harness
lookup of C433's frozen answers. No procedure contracts are
shared across goals, no plan exists, no version selection. This
is what non-compositional "solving" looks like, and it sharpens
Arm E: the only module-only path to the answers is supervised
memorization.

## Kill bar assessment (observed vs frozen)

| Bar | Frozen | Observed | Result |
|-----|--------|----------|--------|
| K1 (B1) | clauses (1,identity,[0,0]/[1,1]/[2,2]); 811 induct=0 decline; revision olderr=2 revcount=1 new clause (1,identity,[2,2]) | exact match on every value | PASS |
| K2 (B2) | clause (0,identity,[601,602]); routing 1/1/0/0; revision olderr=4 revcount=1 new clause (0,identity,[701,702]) | exact match | PASS |
| K3 (V) | 3 inducts return 0, CONTRACT_SET=0; 30 trace checks 0; corrupt checks 0 | exact match | PASS (predicted FAIL of the subsumption arm) |
| K4 (E) | PLAN=none ANS=none x5 goals; blocks logged | exact match | PASS (predicted FAIL of the subsumption arm) |
| K5 (F) | tag contracts (0,identity,[tag,tag]); lookup answers; 816 -> 0; no shared contracts | exact match | PASS |
| K6 | 3/3 byte-identical, stderr empty | sha256 5ab9b76d x3; .err 0 bytes | PASS |
| K7 | safebin, no python, pure Zag, pinned znc | verified; zero forbidden invocations | PASS |
| K8 | module byte-identical; harness has no topo/executor/plans; opaque ids; zero em/en dash bytes | cmp OK; audit clean; dash check clean | PASS |

## Falsification criteria (frozen; none fired)

- F1 (E emits a plan or answer value): NOT FIRED. PLAN=none and
  ANS=none on all five goals.
- F2 (a step induct returns 1 with teeth): NOT FIRED. All three
  inducts returned 0; the field-wise-coverage proof in PREREG
  section 9 held exactly.
- F3 (harness contains composition machinery): NOT FIRED. Audit:
  no topo sort, no procedure executor, no plan records, no
  fact-table access in sp_harness.zag.

## The boundary: what the contract module lacks

Three independent gaps, each sufficient, each demonstrated (not
asserted):

(G1) No value production. Every module op returns clauses, a
{0,1} judgment, void, or a counter. COGOPS execution computes
intermediate values (branch outputs [611] and [], counts 2).
Nothing in the module can emit 611 or 2. Demonstrated by Arm E.

(G2) No ordering or generation. Diamond plans are per-goal topo
orders ([0,2,1,3]); the chain is [0,1,2]. induct learns from
evidence; check judges given vectors. Neither generates nor
orders sequences. Demonstrated by Arm E (plan induct on empty
evidence returns 0; there is no generation op to call).

(G3) The clause language cannot express relational I/O. A clause
is a range test on f(v) for one field, f a fixed deterministic
function of the field value. Any reject whose every field value
occurs in some accept satisfies every clause covering the
accepts, so no valid clause set of any cardinality exists. All
three Arm V reject sets are field-wise covered (verified value
by value), so no step contract can be inducted. Procedure I/O
correctness is inherently relational; the module's contract
language is intra-record arithmetic. This is also why C424's
scenarios subsumed (drift law s2 >= 2 and grammar mod-32 are
per-field) and procedure steps do not.

What subsumes: bindings and version routing are admission
judgments over small integer vectors, which is exactly the
module's vocabulary; invalidate/revise add revision of bindings
and coverage under counterevidence, which C433 lacks. These are
genuine partial wins, not consolation prizes: the module gives
COGOPS something it does not have (contract-governed, revisable
bindings).

Consequence for the synthesis: the reduction chain A/B/C -> U ->
GEN -> contract module covers learned-structure (contract)
composition. Procedure composition (C417/C422/C433) is a second
mechanism requiring ordering/plumbing machinery and an executor
over procedure bodies. Any future unification must bridge G1-G3:
a contract language that can express relational I/O, plus
value-producing and sequence-ordering operations, which is to
say a different, larger module, not the frozen 5-op one.

## Architecture accounting

- Cognition lines added: 0 to the module (byte-identical copy).
  Harness: 544 lines new code, of which ~200 are frozen-data
  table loaders (experimental apparatus, disclosed) and ~340 are
  arm drivers, goal readers, and emit.
- New hardcoded semantic cases: 0. Modes/bridges/handlers: 0.
- New opcodes/behavior classes/edge types: 0.
- Researcher-owned: frozen tables, goal constructors
  (byte-copies), harness, prereg.
- Learner-owned (in the battery's learner state): binding
  contracts, coverage contracts, retired-clause markings,
  revision counts, fail runs. Plans, answers, and procedure
  bodies are absent by construction (that absence is the
  finding).
- Pinned znc 2026.07.0-dev via safebin.

## Toolchain guard

Step 0 executed on the first command of the session and recorded
in NAMECHECK.md: PATH=$HOME/safebin before anything else;
`which python3` and `which python` return nothing. Zero
forbidden-executable invocations in this task. All computation
pure Zag; shell only for safebin setup, znc, binary runs,
sha256sum, greps, byte-verification, and git. AGENTS.md
miscompile workarounds followed (get32/set32 on u8 state,
single-buffer e1str/e1i64 emit with one raw syscall flush, no
`as *i32` slice construction, no `!(A && B)` in while
conditions, if-nesting at most 3, `_zag_malloc as *u8`
allocation). Git writes via /usr/bin/git absolute path;
explicit pathspecs on every commit; nothing pushed.

## Disclosed bounds (not claimed)

- C417/C422 behaviors are covered only via C433's chain
  regression (808) and shared binding/version machinery; the
  battery does not re-run the 2-way/3-way batteries.
- u_grow is not exercised (as in C424).
- The direction of the partial absorption is documented, not
  decided: bindings/version-routing are contract jobs; plans and
  execution are not. Governance decides the landing.
- One frozen module, five frozen goals, frozen tables. No broad
  generality claim.

## Deliverables

All in `docs/lab/research-lead/overnight-20260928/subsumption_p0/`:
PREREG.md (frozen, commit 180496211), NAMECHECK.md (Step 0),
sp_base.zag, sp_module.zag, sp_world.zag, sp_harness.zag,
sp_full.zag (assembled; exactly one `fn main`), sp_build.sh,
sp_bin, sp_compile.txt, sp_run1/2/3.txt (+ .err, empty),
REPORT.md (this file).

## Recommended follow-ups (for the parent, not decided here)

1. The G3 gap suggests a concrete next experiment: a contract
   language with relational clauses (e.g. membership/existence
   over a fact table) tested against Arm V's tables. If it
   verifies the frozen traces with teeth, verification subsumes
   even though execution does not.
2. Port the B1/B2 binding and coverage contracts back into the
   COGOPS lane as a replacement for its BIND table: the module
   adds revision-under-counterevidence that C433's trial table
   lacks. That would be a real integration of the partial win.
3. The E-arm protocol (E-a through E-d) is reusable as a
   subsumption probe for any future "one mechanism" candidate:
   it tests value production, ordering, and generation
   separately.
