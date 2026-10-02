# PREREG_CONTLEARN: continuing-learner integration experiment (frozen)

Status: PREREG-FROZEN (design only; no implementation in this commit).
Wave: wave-20261001-2021pdt. Lane: CONTLEARN. Date: 2026-10-01.
Worker phase: 1 (writing only). Implementation authorized only after the
coordinator commits this prereg alone.

## 0. Commit order (K0)

This prereg is committed alone in
docs/lab/rsi/runs/wave-20261001-2021pdt/CONTLEARN/. The implementation commit
must be a strict descendant of the prereg commit. Verified via
`git merge-base --is-ancestor <prereg-sha> <impl-sha>` before any verdict is
reported. UNVERIFIABLE ORDERING voids the prereg. No bar may be altered after
results are seen; amendment requires a transparent re-freeze.

## 1. Question

Does one persistent learner process running the frozen TNN-2 core exhibit
learner-owned cross-phase integration: white-box evidence that a structure
created in phase N is referenced, revised, or reused in phase M > N, with no
process reset, no task label supplied to cognition, and no recompilation per
phase? The opposite of a resettable per-task store.

Architectural context. H10 (one learner-owned structural workspace) is the
standing precondition for the continuing learner: all subsystem state in one
learner-addressable workspace. This experiment does NOT implement H10 or H11.
It measures the frozen core's cross-phase integration baseline, which any H10
implementation must later beat. The frozen core's separate per-mechanism
formats are expected to avoid interference trivially (no shared store, no
cross-type collisions); K4 verifies that white-box rather than assuming it.
A failure of K3 (reuse) on the frozen core is an informative negative that
locates the missing capability at the researcher/learner line drawn in the
TNN-2 architecture accounting, not a request for another subsystem.

What this battery is not: the event script below is disclosed and fixed. It
is a measurement instrument, not a sealed adversarial world. No L3 claim and
no generality claim follows from it. FW1-FW9 are not used and not referenced
as targets.

## 2. Substrate (re-derived from the frozen source)

Frozen core: `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`,
commit f4de7ff46, 1591 lines, SHA-256
`a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`
(verified by this worker before writing). Protected ISA: 4 ops
{MOVE=101, BRANCHEQ=102, INC=103, DEC=104}. Arena: 110656 bytes, 1024 nodes
(ids 2..1023; 0/1 reserved), 4096 edges. Node tags used: FACT=1, MAP=20,
UNCERT=30, literal=902. Cell tags: SETREG=101, guard=102. Edge types used:
DEP=1, SUP=2, CON=3, REF=4, INS=5, USE=6, CFM=7, SUR=8, PRO=9, SEQ=12, COR=13.

Mechanism facts the design relies on (read from the source, not remembered):

- `ev_query(W,s,r,expected,flags)`: exact hit via `activate` (max bid among
  live non-superseded FACT nodes); else the trial loop `mp_run`/`t2_trial`
  gathers fact paths by BFS from s (depth 1..4), assembles k-hop chain graphs
  (k=2..4 first), executes each against `expected`, and on match calls
  `promote_graph`, which allocates a MAP node (tag 20; field4=r, field8=s,
  field20=root, field28=answer), writes DEP edges from the MAP to every
  licensing fact, writes DEP edges from each SETREG cell to its licensing
  fact, and teaches the answer fact. Else P-INV bootstrap, else miss path
  (UNCERTAINTY node + guide).
- `ev_observe(W,s,r,o)`: on a contradicting observation of a live fact,
  writes a CON self-edge on the old fact (supersede mark), calls
  `revise_on_contradict`, writes a history node, teaches the new fact with a
  REF edge to the old one. `revise_on_contradict` scans all MAPs for a DEP
  edge to the contradicted fact; `t2_revise_graph` finds the stale SETREG
  cell via its DEP edge, tombstones it (tag 0, alive 0), inserts a corrected
  SETREG cell with a DEP edge to the contradicted fact, rewires the guard's
  true-target and SEQ edges, re-executes, and on success marks the old
  answer fact superseded, teaches the corrected answer fact, and updates the
  MAP answer field.
- `alloc_node` scans ids upward from 2 and only evicts (lowest bid,
  unprotected) when all 1024 slots are live. `decay` only ages PROTection
  edge clocks. `z_alloc` zero-fills. No RNG anywhere in the source. The core
  is therefore deterministic given a fixed event order.
- Node budget for this battery: about 140 nodes and 300 edges worst case,
  far below the 1024/4096 caps, so no eviction and no allocation failure can
  occur; any missing structure at end of run is evidence, not capacity.

## 3. Experience sequence (exact, frozen)

One treatment process runs all six phases in one event stream. Phase
boundaries are driver-side markers consumed by the driver only; cognition
receives only (kind, subject, relation, object) integer tuples. Event kinds:
TEACH (ev_teach), QUERY (ev_query with the listed expected and flags=0),
OBSERVE (ev_observe).

- P1 taught facts (24 events): for i in 0..11: TEACH(5001+i, 101, 5101+i);
  then for i in 0..11: QUERY(5001+i, 101, expected 5101+i). S1 = accuracy/12.
- P2 concept block (12 events): for i in 0..5: TEACH(6001+i, 201, 5001+i);
  then for i in 0..5: QUERY(6001+i, 202, expected 5101+i). Each query should
  miss exact hit, trial-build a 2-hop chain 6001+i -> 5001+i -> 5101+i, and
  promote a MAP with DEP edges to the P1 licensing fact. S2 = accuracy/6;
  R1c defined in section 4.
- P3 conflicting evidence (9 events): let T be the first 3 engaged chains
  by ascending subject (frozen selection rule; logged in the transcript; with
  symmetric chains T is expected to be {0,1,2}). For t in T:
  OBSERVE(5001+t, 101, 9101+t). This contradicts the P1 licensing fact, so
  the M3 path should revise that chain's MAP in place. Then for t in T:
  QUERY(5001+t, 101, expected 9101+t) and QUERY(6001+t, 202, expected
  9101+t). S3 = R2c/3 revisions and probe accuracy/6.
- P4 correction (7 events): for j in 0..2: OBSERVE(5010+j, 101, 9201+j).
  These facts license no MAP (chains use 5001..5006), so only the
  fact-level supersede+reteach path fires. Then for j in 0..2:
  QUERY(5010+j, 101, expected 9201+j). S4 = accuracy/3; R3c in section 4.
- P5 unrelated interference (80 events): for k in 0..39:
  TEACH(7001+k, 301, 7101+k); then for k in 0..39: QUERY(7001+k, 301,
  expected 7101+k). S5 = accuracy/40. No other measurement; this phase is
  pure unrelated load (40 teaches, more than double the P1-P4 structure
  count) against which K4 tests survival.
- P6 delayed-reuse probe (18 events): for i in 0..11: QUERY(5001+i, 101,
  expected E1(i)); for i in 0..5: QUERY(6001+i, 202, expected E2(i)), where
  E1(i) = 9101+i if i in T, else 9201+(i-9) if i >= 9, else 5101+i; and
  E2(i) = 9101+i if i in T else 5101+i. R4c/R5c in section 4.

Total: 150 events. All id ranges, relations, and expected values are frozen
above. The only run-time-determined value is T, fixed by the frozen
selection rule.

## 4. White-box measurement oracles

All predicates are structural (tag/field/edge/reachability) over the live
arena, read through the core's own accessors. Structures are identified by
content, never by assumed id ranges (P3 revision frees and reuses cell ids,
so id-range attribution is unsound and is not used).

- fact(s,r,o): tag==1, alive, field20==s, field24==r, field28==o.
- map(sbj,rel): tag==20, alive, field8==sbj, field4==rel.
- superseded(n): an alive CON (type 3) self-edge on n exists.
- serving node of QUERY(s,r): the node returned by activate(s,r) after the
  query (the driver calls it read-only); it must be the content-expected
  node, not merely a value match.

R1c (P2 cites P1), measured at end of P2: count of i in 0..5 where
map(6001+i,202) exists AND has an alive DEP edge to fact(5001+i,101,5101+i)
AND the P2 query answer was 5101+i. Floor: >= 4.

R2c (P3 revises P2), measured at end of P3: count of t in T where
map(6001+t,202).field28 == 9101+t AND there exists a live tag-101 cell c
with (a) an alive DEP edge to fact(5001+t,101,5101+t), (b) its literal node
(field8) holding 9101+t in field20, (c) some live tag-102 guard g with
field12 == c, AND fact(6001+t,202,5101+t) is superseded AND
fact(6001+t,202,9101+t) exists alive AND the P3 chain probe returned
9101+t. Floor: >= 2 (requires |T| == 3, which follows from R1c >= 4).

R3c (P4 correction), measured at end of P4: count of j in 0..2 where
fact(5010+j,101,5110+j) is superseded AND fact(5010+j,101,9201+j) exists
alive AND the P4 probe returned 9201+j. Floor: 3/3.

R4c (early facts survive to the end), measured at P6: count of i in 0..11
where probe (5001+i,101) returned E1(i) AND the serving node is the
content-expected live fact (original P1 node, or its P3/P4 successor).
Floor: >= 10 (P1 loss <= 2).

R5c (P2 procedures reused at the end), measured at P6: count of i in 0..5
where probe (6001+i,202) returned E2(i) AND the serving node is the
content-expected answer fact (P2-created for i not in T, P3-revised for i
in T). Floor: >= 4.

REUSE_COUNT = R1c + R2c + R3c + R4c + R5c (maximum 30).

Supporting (reported, not kill): UNCERT node count in the treatment run
(expected 0; every probe is designed to hit); per-phase node/edge census;
FNV-1a arena checksum printed in the transcript.

## 5. Frozen kill bars

K1 (one learner, no reset, no recompile, no task labels), verified by the
experiment harness itself:
- K1a: the shell harness spawns exactly one treatment learner process for
  the whole 150-event run. The byte-compared transcript contains no PID.
  The harness log records the PID and asserts the spawn count is 1.
- K1b: a znc wrapper script logs every znc invocation. Exactly 1 entry
  (the pre-run build) exists before the runs; 0 new entries appear during
  the 7 runs (1 treatment + 6 control). Any second compile is a K1 failure.
- K1c: driver self-audit. The driver logs every tuple passed to cognition
  and asserts each is (kind, subject, relation, object) with kind in
  {TEACH, QUERY, OBSERVE} and plain integer operands; PHASE markers are
  consumed by the driver and never reach cognition. The audit prints
  AUDIT_PASS; anything else voids the run. All runs launch with empty argv
  and phase-free env (shell asserts via env -i plus PATH).

K2 (frozen ISA boundary and architecture accounting):
- K2a: SHA-256 of tnn2.zag equals
  a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd
  immediately before the build, and `git diff f4de7ff46` on the frozen path
  is empty. One znc invocation compiles the byte-identical frozen file plus
  the new driver source; the frozen file is referenced read-only (the exact
  link mechanism is implementation detail and must satisfy K2a/K2b).
- K2b: driver source audit. The driver is fixture: it emits the frozen
  event script, calls the frozen event API, runs read-only censuses, and
  prints results. It defines 0 cognition functions (no new learning,
  retrieval, inference, retention, eviction, planning, derivation, revision,
  or execution logic), 0 new node tags, 0 new edge types, 0 new opcodes,
  0 modes, 0 bridges, 0 routers, 0 task-specific handlers, 0 semantic cases
  (switch/match count in driver source is 0).
- K2c: cognition-source delta accounting (projected here, measured at
  implementation): lines added 0, lines deleted 0, net 0; new hardcoded
  semantic cases 0; new modes 0; new bridges 0; new routers 0; new
  task-specific handlers 0; learner-state structures created are counted by
  the per-phase census (fact nodes, MAP nodes, cells, literals, DEP/SEQ
  edges, supersede marks, history nodes), all in frozen formats.
- K2d: pure Zag plus shell orchestration only. Zero Python, C, JavaScript,
  or Rust invocations at every stage (source, znc build, execution,
  analysis). Toolchain guard recorded in NAMECHECK.md Step 0; `which
  python3` prints nothing at run start.

K3 (cross-phase reuse, the integration bar): R1c >= 4 AND R2c >= 2 AND
R3c == 3 AND R4c >= 10 AND R5c >= 4 AND REUSE_COUNT >= 20. Kill: any
component floor missed.

K4 (interference bound):
- K4a: edge census. At end of P4 the driver records E4, the set of alive
  edges (from-id, type, to-id) with type in {DEP=1, SEQ=12}. At end of run,
  every member of E4 is still alive. Zero missing edges; P5-attributed
  corruption is impossible by allocator design (no live slot is ever
  reused) and is verified, not assumed.
- K4b: all 6 map(6001+i,202) nodes exist alive at end of run. 6/6.
- K4c: R4c >= 10 (at most 2 of the 12 P1 facts lost).
- K4d (diagnosability): for each lost fact or unanswerable chain the
  transcript reports the white-box cause (supersede mark, missing edge, or
  eviction record). Missing diagnosis withholds the verdict.
Kill: any of K4a/K4b/K4c violated.

K5 (negative control: per-phase reset):
- Six control processes, one per phase, each on a fresh arena. Each
  control phase re-teaches its prerequisites inside the phase: C-P1 = P1
  events; C-P2 = P1 teaches + P2 events; C-P3 = P1 teaches + P2 events +
  P3 events (same frozen T rule applied to its own engagement); C-P4 = P1
  teaches + P4 events; C-P5 = P5 events; C-P6 = P6 probes only.
- K5a: control per-phase score >= treatment per-phase score on each of
  P1..P5 (S1, S2 accuracy and R1c, S3 R2c and probes, S4, S5). Expectation
  is equality (identical event subsequences on equivalent stores); a
  treatment advantage on any phase is investigated, not celebrated.
- K5b: control cross-phase reuse is 0 by construction (separate arenas)
  and verified: C-P6 scores 0/18, its final state holds 0 tag-20 nodes,
  and every tag-1 node has field24 == -999 (guide markers only).
Kill: any K5a violation, or any K5b violation (a K5b violation means the
harness leaks state: VOID the comparison, fix under amendment, re-run).

K6 (determinism): 3/3 byte-identical runs of the treatment and 3/3 of each
control phase: SHA-256 of stdout transcripts equal across the three runs,
printed FNV-1a arena checksums equal, exit code 0, zero stderr bytes. The
transcript contains no PID, timestamps, or paths. Zero randomness in
decision paths (the core has no RNG; z_alloc zero-fills; all scans are
deterministic). Kill: any mismatch.

## 6. Verdicts

- INTEGRATION-DEMONSTRATED iff K0, K1, K2, K3, K4, K5, K6 all pass.
- INTEGRATION-ABSENT iff K0, K1, K2, K4, K5, K6 pass and K3 fails. This is
  an informative negative: the frozen core retains (K4) but does not
  integrate across phases; the missing capability sits on the researcher
  side of the control-plane line. Per the no-patch-treadmill rule, this
  verdict is followed by root-cause clustering, not by a request for new
  handlers, modes, or opcodes.
- INTERFERENCE-FAIL iff K4 fails: the H10 pressure (cross-phase structural
  corruption) is realized even with separate formats; H10's design must
  answer it before any unification work proceeds.
- VOID iff K0, K1, K2, or K6 fails: instrument failure, no verdict.

## 7. What this prereg does NOT authorize

- No implementation in this commit. The implementation worker builds only
  after the coordinator commits this prereg alone and authorizes phase 2.
- No H10/H11 substrate implementation and no new cognitive machinery of
  any kind. No new Zag subsystems, modes, bridges, routers, task-specific
  handlers, semantic cases, node tags, edge types, or ISA opcodes.
- No tuning the frozen core to this script (K2a forbids any edit).
- No L3, generality, or architecture claim from this battery. The script is
  disclosed; the claim, if INTEGRATION-DEMONSTRATED, is exactly: on this
  fixed 150-event sequence the frozen core shows >= 20 white-box
  cross-phase citations with the stated floors, under the stated controls.
- No second memory engine and no per-phase state formats. One arena, one
  event loop, six phases, one process.
- The mini_lifetime_integration 3/3 determinism claim is not cited as
  established (governance caveat: not artifact-backed beyond run1
  transcripts). This prereg re-derives its own determinism bar in K6.

## 8. Provenance of this design

Re-derived for this prereg from: the frozen source tnn2.zag (event loop,
trial, promotion, revision, allocator; line references in section 2); the
TNN-2 architecture accounting
(docs/lab/rsi/runs/wave-20261001-1721pdt/TNN3/ARCH_ACCOUNTING.md); H10 in
(docs/lab/rsi/runs/wave-20261001-1721pdt/TNN3/HYPOTHESES.md); the CLA-2
prereg and contlearn2 prereg
(docs/lab/research-lead/overnight-20260928/continuing_learner/). Nothing
above is cited from memory; the mechanism behaviors were re-read from the
source during this turn.
