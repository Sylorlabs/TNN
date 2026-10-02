# PREREG_LEARNOWN: learner-owned structural workspace probe (frozen)

Status: PREREG-FROZEN (design only; no implementation in this commit).
Wave: wave-20261001-2321pdt. Lane: CONTLEARN. Date: 2026-10-01.
Worker phase: 1 (writing only). Implementation authorized only after the
coordinator commits this prereg alone.

## 0. Commit order (K0)

This prereg is committed alone in
docs/lab/rsi/runs/wave-20261001-2321pdt/CONTLEARN/. The implementation commit
must be a strict descendant of the prereg commit. Verified via
`git merge-base --is-ancestor <prereg-sha> <impl-sha>` before any verdict is
reported. UNVERIFIABLE ORDERING voids the prereg. No bar may be altered after
results are seen; amendment requires a transparent re-freeze.

## 1. Question

The wave-20261001-2021pdt CONTLEARN battery was INTEGRATION-DEMONSTRATED
(REUSE_COUNT 30/30) and red-team QUALIFIED: the integration was machinery
integration under per-query supervision, not learner-owned memory growth.
Every QUERY passed the correct answer as `expected` with flags=0, and the
promotion accept was `v==expected` by frozen machinery (t2_try_verify,
tnn2.zag line 497). The learner's causal contribution to every counted
citation was zero.

This probe asks the next question the red team suggested but did not
authorize: do the frozen core's store, retrieve, and reuse mechanics survive
disconnection of the per-query supervisor? Concretely: with every query
masked (expected=-2, flags=1, so the machinery can no longer match an answer
key), does the frozen core still (a) store chain structures as MAPs with DEP
citations in the single persistent arena, (b) retrieve stored values by
masked query across at least 3 distinct task families and N=20 sequential
queries, and (c) show reuse that causally depends on the stored structures,
verified by in-arena deletion (delete the serving structures, reuse must
drop)?

Honest framing, frozen here and carried into the verdict. This probe does
NOT test learner agency. H2-v2 (K-H2-3(a)) and H3 stand on the byte-identical
source: no learner-created state influences any store, accept, or retrieve
decision; the trial search order, the first-clean-candidate accept rule, and
the promotion rule are frozen researcher code. What changes versus 2021pdt is
only the removal of per-query answer keys. The workspace under test is the
single frozen arena itself: one persistent learner-addressable store, no
independent subsystem state formats, no per-query researcher supervision of
what gets stored. Under the project's H10 terminology this is the weak
reading of "learner-owned" (resident in the learner's arena, manipulated
only through the frozen event interface). The strong reading (the learner
decides or authors) is explicitly not claimed. The Attack 6 qualification is
carried forward: measured "reuse" is exact-hit retrieval of machinery-taught
answer facts via `activate`, not execution of promoted MAPs at query time;
the MAP is executed only inside trial verification.

What this battery is not: the event script below is disclosed and fixed. It
is a measurement instrument, not a sealed adversarial world. No L3 claim and
no generality claim follows from it. FW1-FW9 are not used.

## 2. Substrate (re-derived from the frozen source for this prereg)

Frozen core: `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`,
commit f4de7ff46, 1591 lines, SHA-256
`a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`
(re-verified by this worker before writing; `git diff f4de7ff46` on the
frozen path is empty). Protected ISA: 4 ops
{MOVE=101, BRANCHEQ=102, INC=103, DEC=104}. Arena: 110656 bytes, 1024 nodes,
4096 edges.

Mechanism facts this design relies on (re-read from the source, not
remembered):

- `ev_query(W,s,r,expected,flags)`: exact hit via `activate` (max bid among
  live non-superseded tag-1 nodes with field20==s, field24==r); else the
  trial loop `mp_run`/`t2_trial`; else P-INV `bootstrap_miss`; else the miss
  path `miss_inquire` (UNCERTAINTY node tag 30 plus a guide tag-1 fact with
  field24==-999), returning -2.
- `mp_run` sets `masked = flags & 1`. `t2_try_verify` with masked==1 accepts
  the first candidate whose executed value satisfies
  `v!=-2 && v!=-999999` (tnn2.zag line 497-508). No answer key is consulted.
- `t2_trial` tries k-hop chains for k=2..4 first (composition-preserving
  order), then sums, then counts, then 1-hop. On accept it calls
  `promote_graph`, which allocates a MAP node (tag 20; field4=r, field8=s,
  field20=root, field28=answer), writes DEP (type 1) edges from the MAP to
  every licensing fact on the chain path, and teaches the answer fact via
  `ev_teach_in(W,s,r,ans)`.
- `ev_observe` on a contradicting observation of a live fact: writes a CON
  (type 3) self-edge on the old fact (the core's supersede mark), calls
  `revise_on_contradict` (scans all MAPs for a DEP edge to the contradicted
  fact; `t2_revise_graph` tombstones the stale SETREG cell found via its DEP
  edge, inserts a corrected cell, rewires the guard, re-executes; on success
  supersedes the old answer fact, teaches the corrected answer fact,
  updates the MAP answer field), writes a history node (tag 3), and teaches
  the new fact with a REF (type 4) edge to the old one. Supersede marks and
  cell tombstones are the frozen core's only deletion-equivalent operations;
  no node is ever removed by the event interface.
- `activate` returns the max-`bid` live non-superseded fact; `bid` counts
  DEP/SUP/USE/CFM edges minus CON edges (plus guide-linked counts). A
  promoted MAP's DEP edges to its licensing facts therefore raise those
  facts' bids; the answer fact taught by `ev_teach_in` starts at bid 0 and
  gains one USE self-edge per exact-hit query.
- `ev_teach` always allocates a fresh fact node (no dedupe). The core has no
  RNG; `z_alloc` zero-fills; all scans are id-ascending. The core is
  deterministic given a fixed event order.
- Node budget for this battery: about 260 nodes and 700 edges worst case,
  far below the 1024/4096 caps, so no eviction and no allocation failure can
  occur; any missing structure at end of run is evidence, not capacity.

Design consequence verified against the source: a concept-link fact and a
promoted answer fact must NOT share (s,r), because `activate` would serve
the higher-bid node and the concept fact carries MAP/cell DEP bids. Family C
therefore teaches concept links on relation 401 and queries relation 402
(family B already separates 201 concept links from 202 queries; family A is
1-hop with no promoted structure).

## 3. Experience sequence (exact, frozen)

Two modes, each one process on one fresh arena. Event kinds: TEACH
(ev_teach), MQUERY (ev_query with expected=-2, flags=1; the frozen
supervisor-disconnect mechanism, disclosed here; it carries no task identity
and is not a task label), OBSERVE (ev_observe). Phase boundaries are
driver-side markers consumed by the driver only; cognition receives only
(kind, subject, relation, object) integer tuples.

TREAT (92 events):

- STORE (39 events, supervisor disconnected throughout):
  - Family A (1-hop facts): for i in 0..6: TEACH(5001+i, 101, 5101+i).
  - Family B (2-hop concept chains): for i in 0..6:
    TEACH(6001+i, 201, 5001+i); then for i in 0..6: MQUERY(6001+i, 202).
    Each masked query must miss exact hit, trial-build the 2-hop chain
    6001+i -> 5001+i -> 5101+i, accept the first clean candidate, and
    promote MAP(6001+i,202) with DEP edges to the licensing facts.
  - Family C (2-hop chains, distinct relations): for i in 0..5:
    TEACH(7001+i, 301, 7101+i); then for i in 0..5:
    TEACH(8001+i, 401, 7001+i); then for i in 0..5: MQUERY(8001+i, 402).
    Each masked query must promote MAP(8001+i,402) for the chain
    8001+i -> 7001+i -> 7101+i.
- REUSE (20 events): 20 sequential masked probes spanning the 3 families:
  for i in 0..6: MQUERY(5001+i, 101) [stored 5101+i]; for i in 0..6:
  MQUERY(6001+i, 202) [stored 5101+i]; for i in 0..5: MQUERY(8001+i, 402)
  [stored 7101+i].
- ABLATE (13 events, in-arena deletion of the serving structures):
  for i in 0..6: OBSERVE(5001+i, 101, 9901+i). This supersedes each family-A
  serving fact and, via revise_on_contradict, tombstones the family-B MAP
  cells and reteaches corrected answer facts (6001+i, 202, 9901+i). Then for
  i in 0..5: OBSERVE(8001+i, 402, 9801+i). This supersedes each family-C
  answer fact and reteaches (8001+i, 402, 9801+i). No MAP revision fires on
  the family-C contradicts (MAP DEP edges target the licensing facts, not
  the answer facts).
- REUSE2 (20 events): the same 20 masked probes as REUSE, in the same order.

NOSTORE (20 events): the same 20 masked probes as REUSE, on a fresh arena
with no STORE phase. Every probe must take the true miss path.

## 4. White-box measurement oracles

All predicates are structural (tag/field/edge/reachability) over the live
arena, read through the core's own accessors. Structures are identified by
content, never by assumed id ranges.

- fact(s,r,o): tag==1, alive, field20==s, field24==r, field28==o.
- map(sbj,rel): tag==20, alive, field8==sbj, field4==rel.
- superseded(n): an alive CON (type 3) self-edge on n exists.
- serving node of MQUERY(s,r): the node returned by activate(s,r) after the
  query, called read-only by the driver; it must be the content-expected
  live fact, not merely a value match.

STORE_OK, measured at end of STORE: count of promoted structures created
with the supervisor disconnected:
- for i in 0..6: map(6001+i,202) exists AND has an alive DEP edge to
  fact(5001+i,101,5101+i) AND the STORE masked query returned 5101+i.
- for i in 0..5: map(8001+i,402) exists AND has an alive DEP edge to
  fact(7001+i,301,7101+i) AND the STORE masked query returned 7101+i.
Floor: 13/13.

REUSE_OK, measured at REUSE: count of the 20 masked probes where the
returned value equals the stored value AND the serving node is the
content-expected live fact. Floor: 20/20.

REUSE2_ORIG, measured at REUSE2: count of the 20 masked probes returning the
ORIGINAL stored values (5101+i / 7101+i). Expectation: 0 (every original
serving fact is superseded). REUSE2_NEW: count returning the post-ablation
values (9901+i on families A/B, 9801+i on family C). Expectation: 20.

NOSTORE_OK, measured on the NOSTORE run: count of the 20 masked probes
returning -2 (true miss). Floor: 20/20, with exactly 20 UNCERT (tag 30)
nodes in the final arena.

## 5. Frozen kill bars

K1 (one learner, no reset, no recompile, no task labels):
- K1a: the harness spawns exactly one treatment process for the whole
  92-event TREAT run and one per NOSTORE rep. Transcripts contain no PID;
  the harness log records PIDs and asserts spawn counts.
- K1b: a znc wrapper script logs every znc invocation. Exactly 1 entry
  (the pre-run build) exists before the runs; 0 new entries appear during
  the runs. Any second compile is a K1 failure.
- K1c: driver self-audit. Every tuple passed to cognition flows through the
  single choke point, logged, with kind in {TEACH=1, QUERY=2, OBSERVE=3} and
  plain integer operands; MQUERY is kind 2 with the frozen parameters
  expected=-2, flags=1 (supervisor disconnect, disclosed in section 3, not
  a task label). PHASE markers are consumed by the driver and never reach
  cognition. The audit prints AUDIT_PASS. All runs launch with empty argv
  and empty env. Expected audited counts: TREAT 92, NOSTORE 20.

K2 (frozen ISA boundary and architecture accounting):
- K2a: SHA-256 of tnn2.zag equals
  a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd
  immediately before the build, and `git diff f4de7ff46` on the frozen path
  is empty. One znc invocation compiles the byte-identical frozen file
  (mechanical nomain derivation: exactly the single `fn main` line removed,
  diff-verified) plus the new driver source; the frozen file is referenced
  read-only.
- K2b: driver source audit. The driver is fixture: it emits the frozen
  event script, calls the frozen event API, runs read-only censuses, and
  prints results. It defines 0 cognition functions, 0 new node tags, 0 new
  edge types, 0 new opcodes, 0 modes, 0 bridges, 0 routers, 0 task-specific
  handlers, 0 semantic cases (switch/match count in driver source is 0).
- K2c: cognition-source delta: lines added 0, deleted 0, net 0; new
  hardcoded semantic cases 0; new modes/bridges/routers/handlers 0;
  learner-state structures created are counted by the per-phase census, all
  in frozen formats, in the single arena (no independent subsystem state).
- K2d: pure Zag plus shell orchestration only. Zero Python, C, JavaScript,
  or Rust invocations at every stage. Toolchain guard recorded in
  NAMECHECK.md Step 0; `which python3` prints nothing at run start.

K3 (no regression on the 2021pdt battery): the committed 2021pdt
`cl_driver` binary is re-run read-only, 3 reps of TREAT mode. Stdout
SHA-256 must equal
`53ff2c990e4f7f8d29c8b1bb809cf6616226b9f6bd3dd28d06210dc54446bc44` on all
3 reps, and the transcript must contain the REUSE_COUNT 30 line with all
component lines at ceiling (R1C 6, R2C 3, R3C 3, R4C 12, R5C 6). Kill: any
hash mismatch or REUSE_COUNT != 30.

K4 (learner-ownership probe):
- K4a: STORE_OK == 13.
- K4b: REUSE_OK == 20.
- K4c: REUSE2_ORIG <= 2 (expect 0) AND REUSE2_NEW >= 18 (expect 20).
  The ablation must strictly reduce original-value reuse.
- K4d: NOSTORE_OK == 20 AND final UNCERT node count == 20.
Kill: any component missed.

K5 (machinery sanity): UNCERT (tag 30) node count in the TREAT run == 0
(no true miss: every STORE masked query promoted, every REUSE/REUSE2 probe
exact-hit). Final alive node count < 1024 (no eviction possible). Kill:
UNCERT_TREAT != 0.

K6 (determinism): 3/3 byte-identical runs of TREAT and 3/3 of NOSTORE:
SHA-256 of stdout transcripts equal across the three runs, printed FNV-1a
arena checksums equal, exit code 0, zero stderr bytes. Transcripts contain
no PID, timestamps, or paths. Kill: any mismatch.

## 6. Verdicts

- LEARNOWN-DEMONSTRATED iff K0, K1, K2, K3, K4, K5, K6 all pass.
- REGRESSION-FAIL iff K3 fails: the no-regression claim is void; probe
  results are reported separately and not combined into a pass.
- LEARNOWN-ABSENT iff K0, K1, K2, K5, K6 pass and K4 fails. Informative
  negative: store/retrieve/reuse do not survive supervisor disconnect; the
  missing capability sits on the researcher side of the control-plane line.
  Per the no-patch-treadmill rule this is followed by root-cause analysis,
  not by new handlers, modes, or opcodes.
- VOID iff K0, K1, K2, or K6 fails: instrument failure, no verdict.

## 7. Exact claim bound (frozen)

If LEARNOWN-DEMONSTRATED, the claim is exactly: on the fixed disclosed
92-event treatment script, with the per-query supervisor disconnected
(every query masked: expected=-2, flags=1), the frozen TNN-2 core's
event-triggered machinery stores 13/13 chain structures as MAPs with DEP
citations in the single persistent arena, retrieves 20/20 stored values by
masked query across 3 task families, and after in-arena deletion of the
serving structures (contradiction: supersede marks plus MAP-cell
tombstones) the masked reuse of original values drops to <=2/20 while the
machinery still retrieves the 20 successor values; the nostore control shows
0/20 reuse with 20 UNCERT misses; 3/3 byte-identical.

Explicitly not shown: learner agency in the causal sense (H2-v2/H3 stand);
procedure execution at query time (Attack 6: reuse is exact-hit retrieval
of machinery-taught facts); unsupervised integration beyond the disclosed
script; any L3 or generality claim.

## 8. What this prereg does NOT authorize

- No implementation in this commit.
- No H10/H11 substrate implementation and no new cognitive machinery of any
  kind. No new Zag subsystems, modes, bridges, routers, task-specific
  handlers, semantic cases, node tags, edge types, or ISA opcodes. The
  single persistent workspace is the frozen arena; the probe exercises it
  through the frozen event interface only.
- No tuning the frozen core to this script (K2a forbids any edit).
- No sealed adversarial worlds; the script is disclosed. The post-freeze
  adversarial battery remains the generality test and is separate.
- The 2021pdt binary is re-run read-only for K3; it is not rebuilt and not
  modified.
