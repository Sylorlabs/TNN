# PREREG_CONTLEARN_LH: longer-horizon delayed reuse under sustained interference (frozen)

Status: PREREG-FROZEN (design only; no implementation in this commit).
Wave: wave-20261002-0221pdt. Lane: CONTLEARN-LH. Date: 2026-10-02.
Worker phase: 1 (writing only). Implementation authorized only after the
coordinator commits this prereg alone.

Note: this document uses hyphens only; no em or en dashes appear.

## 0. Commit order (K0)

This prereg is committed with only lane documentation
(docs/lab/rsi/runs/wave-20261002-0221pdt/CONTLEARN-LH/): NAMECHECK.md and
this file. No implementation file of this lane may exist at or before the
prereg commit. The implementation commit must be a strict descendant of
the prereg commit, verified by `git merge-base --is-ancestor <prereg-sha>
<impl-sha>` before any verdict is reported. UNVERIFIABLE ORDERING voids
the prereg. No bar may be altered after results are seen; amendment
requires a transparent re-freeze.

## 1. Question and lineage

Lineage: CONTLEARN3 PROPOSAL-FIRST-DEMONSTRATED, BUILD-PASS
(CP-1..CP-6, K0..K3 all pass): on a disclosed 76-event battery the
continuing learner integrates 6/6 novel 2-hop chains proposal-first,
reuses 12/12 values after a single 24-event interference gap, and retains
12/12 pre-conflict values across one conflict plus one correction
episode, in one process with no reset, no task label, no recompilation.
Claim bound carried over: the proposal content (mech=TRY_CHAIN) is a
fixed researcher template; no learner authorship of proposal content is
claimed; no L3; citation stays machinery-enabled.

This lane's question is structurally different in the time dimension: it
is NOT a re-run of the 76-event battery. It measures retention as a
FUNCTION of interference volume (a curve at three volumes, not a single
point), applies MULTIPLE interference episodes of different kinds
(unrelated domain facts at growing volumes; conflicting evidence on a
subset of the original learned chains themselves; correction episodes),
and probes delayed reuse of the original chains without re-teaching at
the longest horizon. A second novel integration (LATE-NOVEL) is placed at
the longest horizon to test whether proposal-before-machinery ordering is
maintained after 300+ interfering events.

Key question, frozen: does the proposal-first ordering and the
DEP-cited MAP structure survive sustained interference, or does retention
degrade with horizon?

Structural-difference statement (for the re-freeze requirement): no prior
lane measured a retention curve over interference volume; the CONTLEARN3
battery had exactly one interference episode (24 unrelated TEACH events)
and one conflict/correction pair on a side fact; here the original chain
facts themselves are conflicted and corrected (subset), unrelated
interference arrives in three episodes of growing volume (48, 96, 120),
and a late novel integration tests ordering maintenance at the longest
horizon. The event script is 358 events (over 3x the 76-event battery).

## 2. Instruments: reused, unmodified

The TREAT and CONTROL cores are byte copies of the CONTLEARN lane files
(the proposal-gate instrument and the unmodified nomain derivation),
verified by SHA-256 before any build (hashes in NAMECHECK.md Step 2).
This lane modifies the instrument in zero ways; it extends only the
driver script. The cores' frozen derivation is never written.

- TREAT core `lh_core_treat.zag`: byte copy of pf_core_treat.zag
  (SHA-256 627af6eb0e88141fdeb00baba0aab178a29df128aa0250398355db42d8557f63).
  Proposal-gated trial/promotion machinery; PROPOSAL before MACHINERY;
  MAPs cite licensing proposal with a type-1 DEP edge.
- CONTROL core `lh_core_control.zag`: byte copy of pf_core_control.zag
  (SHA-256 26b455e78a9b0ba0f6d6967c12ff8c05f9ebd9152dddca9efeb2a3b44064ec9d,
  the recorded nomain derivation). Machinery-first, no proposal channel.

The only lane-authored research file is the driver `lh_driver.zag`
(fixture only: 0 cognition functions, 0 structural writes, 0 new tags,
edges, opcodes, modes, bridges, routers, handlers, semantic cases).

## 3. Experience sequence (exact, frozen, fresh, one process)

All new subject/object/relation ranges (relations 561, 562, 581, 582,
583; subjects 31001.., 41001.., 43001..; objects 22101.., 22111..,
32001.., 42001..) are unused by any prior battery in the wave-20261001
and wave-20261002 .zag sources (verified by grep before writing this
prereg; NAMECHECK.md Step 1). The script is disclosed, not
adversary-designed. Event kinds: 1=TEACH (ev_teach), 2=MQUERY
(ev_query, expected=-2, flags=1: disclosed supervisor disconnect, not a
task label), 3=OBSERVE (ev_observe: the frozen counterexample protocol,
integer (s,r,o) operands only, not a task label). PHASE markers are
driver-side prints and never reach cognition.

Full script (358 events), both binaries, one process per run:

- NOVEL (24): verbatim CONTLEARN3 novel block.
  - for i in 0..5: TEACH(21001+i, 511, 22001+i) (concept links).
  - for i in 0..5: TEACH(23001+i, 521, 21001+i) (anchor links).
  - for i in 0..5: MQUERY(23001+i, 522) (novel relation; proposal path,
    integrate; expected 22001+i).
  - for i in 0..5: TEACH(24001+i, 531, 25001+i) (standing sanity family).
- STORE_OK check + census (same oracles as CONTLEARN3).
- CONFLICT-1 (2): TEACH(26001, 541, 27001); OBSERVE(26001, 541, 27002).
- CORRECTION-1 (2): OBSERVE(26001, 541, 27003); MQUERY(26001, 541)
  (expects 27003).
- RETENTION (12): verbatim CONTLEARN3 probes (6 concept, 6 sanity).
- INTERFERE-A (48): for i in 0..47:
  TEACH(31001+i, rel, 32001+i) where rel=561 if i even else 562
  (unrelated domain facts, new relations).
- DELAYED-A (12): reuse probes without re-teaching:
  - for i in 0..5: MQUERY(23001+i, 522) expecting 22001+i.
  - for i in 0..5: MQUERY(24001+i, 531) expecting 25001+i.
  Interference volume at this point: V_A = 52 (CONFLICT-1 2 +
  CORRECTION-1 2 + INTERFERE-A 48).
- CONFLICT-2 (2): conflicting evidence on a SUBSET of the learned chains:
  for i in 0..1: OBSERVE(21001+i, 511, 22101+i) (contradicts the chain
  fact for chains 0 and 1; the frozen revision protocol supersedes the
  original fact and teaches the contradictory one; rv=0 expected).
- CORRECTION-2 (2): for i in 0..1: OBSERVE(21001+i, 511, 22111+i)
  (resolved values, distinct from both the original and the
  contradictory value; rv=0 expected).
- INTERFERE-B (96): for i in 0..95:
  TEACH(31101+i, rel, 32101+i), rel=561 if i even else 562.
- DELAYED-B (12): same 12 probes as DELAYED-A.
  Interference volume at this point: V_B = 152 (V_A + 2 + 2 + 96).
- CONFLICT-3 (2): for i in 2..3: OBSERVE(21001+i, 511, 22103+(i-2)).
- CORRECTION-3 (2): for i in 2..3: OBSERVE(21001+i, 511, 22113+(i-2)).
- INTERFERE-C (120): for i in 0..119:
  TEACH(31301+i, rel, 32301+i), rel=561 if i even else 562.
- LATE-NOVEL (6): novel chains at the longest horizon, before any
  re-teaching of them:
  - for i in 0..1: TEACH(41001+i, 581, 42001+i) (concept links, new rel).
  - for i in 0..1: TEACH(43001+i, 571, 41001+i) (anchor links).
  - for i in 0..1: MQUERY(43001+i, 583) (relation 583 novel; each first
    miss must fire the proposal path, then integrate; expected 42001+i).
- DELAYED-C (12): same 12 original probes as DELAYED-A/B (no re-teaching).
  Interference volume at this point: V_C = 276 (V_B + 2 + 2 + 120).
- LATE-REUSE (2): for i in 0..1: MQUERY(43001+i, 583) expecting 42001+i.

Node/edge budget: TREAT worst case about 340 alive nodes and under 1500
live edges; far below the 1024/4096 caps, so no eviction can occur and
any missing structure is evidence, not capacity.

Assumption under test (not assumed true): the frozen ev_observe revision
protocol is generic over (s,r); the subset-conflict behavior on chain
facts is measured by CONFLICT2_OK/CONFLICT3_OK, not presupposed.

## 4. White-box measurement oracles

Structural predicates from CONTLEARN3, reused unchanged (content-
identified over the live arena through the core's own accessors):

- fact(s,r,o): tag==1, alive, field20==s, field24==r, field28==o.
- map(sbj,rel): tag==20, alive, field8==sbj, field4==rel.
- proposal(s,r): tag==1, alive, field20==30, field24==-998, field4==s,
  field28==r.
- superseded(n): type-3 self-edge on n exists (is_superseded==1).

STORE_OK (end of NOVEL): 6/6 MAP(23001+i,522) with alive DEP edge to
fact(21001+i,511,22001+i) and integrate answer 22001+i.
STORE_PROP_CITE: 6/6 MAPs with alive type-1 DEP edge to
proposal(23001+i,522).
LATE_STORE_OK: 2/2 MAP(43001+i,583) with alive DEP edge to
fact(41001+i,581,42001+i) and answer 42001+i.
LATE_PROP_CITE: 2/2 MAPs with alive type-1 DEP edge to
proposal(43001+i,583).

ORDER_OK: transcript line-order per (s,r): the PROPOSAL line appears at an
earlier transcript line than the MACHINERY line for the same (s,r); the
MACHINERY line names the same live proposal node id; zero
MACHINERY_SKIPPED lines. Checked for the 6 NOVEL pairs and separately
for the 2 LATE-NOVEL pairs.

REUSE_A / REUSE_B / REUSE_C (DELAYED-A/B/C): 12/12 probes return stored
values with the content-expected live fact as serving node (6x 22001+i
on (23001+i,522), 6x 25001+i on (24001+i,531)), with no re-teaching of
those chains after NOVEL.

CONFLICT1_OK: fact(26001,541,27001) superseded, fact(26001,541,27002)
live, rv=0.
CORRECT1_OK: fact(26001,541,27002) superseded, fact(26001,541,27003)
live, MQUERY(26001,541) returns 27003 with serving-node check.
CONFLICT2_OK: for i in 0..1, fact(21001+i,511,22001+i) superseded,
fact(21001+i,511,22101+i) live, rv=0.
CORRECT2_OK: for i in 0..1, fact(21001+i,511,22101+i) superseded,
fact(21001+i,511,22111+i) live, rv=0.
CONFLICT3_OK / CORRECT3_OK: same for i in 2..3 with objects 22103+i-2 /
22113+i-2.
RETENTION_OK: the 12 RETENTION probes return pre-conflict values (6x
22001+i on (21001+i,511), 6x 25001+i on (24001+i,531)). Bar: 12/12.
Note: RETENTION runs before CONFLICT-2, so the original chain facts are
still the live values there; the chain-fact subsets are corrected in
episodes 2 and 3, and the MAP reuse probes are independent of fact
content.

Mechanism census per phase: MAPC, PROPC, DEPC, UNC, GUIDEC, N1, Eall.

## 5. Frozen kill bars

CP-LH1 (proposal-before-machinery ordering maintained, TREAT): NOVEL
ORDER_OK 6/6 ordered pairs with 0 skips AND LATE-NOVEL ORDER_OK 2/2
ordered pairs with 0 skips; 8 PROPOSAL lines, 8 MACHINERY lines total;
zero MACHINERY_SKIPPED lines on all 3 reps; PROPC_FINAL==8.

CP-LH2 (integration under proposal-first, TREAT): STORE_OK == 6/6 and
STORE_PROP_CITE == 6/6 (NOVEL); LATE_STORE_OK == 2/2 and
LATE_PROP_CITE == 2/2 (LATE-NOVEL).

CP-LH3 (retention curve, no re-teaching): REUSE_A == 12/12 at V=52,
REUSE_B == 12/12 at V=152, REUSE_C == 12/12 at V=276, each with
serving-node checks. This is the key bar: retention as a function of
interference volume. Any point below 12/12 is LH-DEGRADED, not a pass.

CP-LH4 (conflict/correction/retention): CONFLICT1_OK, CORRECT1_OK,
CONFLICT2_OK, CORRECT2_OK, CONFLICT3_OK, CORRECT3_OK all hold;
RETENTION_OK == 12/12.

CP-LH5 (determinism): 3/3 byte-identical stdout per binary (SHA-256 equal
across reps), printed FNV-1a arena checksums equal, exit code 0, zero
stderr bytes, no PID/timestamps/paths in transcripts.

CP-LH6 (control reproduces, machinery-first): on the unmodified frozen
core, STORE_OK_C == 6/6, LATE_STORE_C == 2/2, REUSE_A_C == REUSE_B_C ==
REUSE_C_C == 12/12, RETENTION_OK_C == 12/12, the CONFLICT/CORRECT checks
hold, and the transcript contains zero PROPOSAL lines.

Governance bars:

K0: prereg committed alone with only lane docs; implementation strictly
descendant; merge-base verified before verdict.

K1 (one learner, no reset, no recompile, no task labels): K1a: exactly 6
learner processes total (2 binaries x 3 reps), one process per full
358-event run; transcripts contain no PID; harness log records spawns.
K1b: znc wrapper logs every invocation; exactly 2 entries (the two
pre-run builds) before the runs; 0 new entries during the runs. K1c:
driver self-audit; every tuple flows through the choke points with kind
in {1,2,3} and plain integer operands; MQUERY carries the frozen
parameters expected=-2, flags=1 (disclosed supervisor disconnect, not a
task label); OBSERVE (kind 3) is the frozen counterexample protocol,
disclosed here, not a task label; PHASE markers never reach cognition;
all runs launch with empty argv and empty env; expected audited count
358 per run; prints AUDIT_PASS.

K2 (frozen ISA boundary and architecture accounting): K2a: SHA-256 of the
frozen tnn2.zag equals
a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd before
the builds and after the runs; the recorded nomain derivation hash equals
26b455e78a9b0ba0f6d6967c12ff8c05f9ebd9152dddca9efeb2a3b44064ec9d before
the builds; the lane cores are byte copies of the recorded CONTLEARN
files (hashes verified); the frozen path is never written. K2b: driver
source audit: 0 cognition functions, 0 structural writes (ns(/link_edge(/
alloc_node( count 0 in the driver), 0 new node tags, 0 new edge types, 0
new opcodes, 0 modes, 0 bridges, 0 routers, 0 task-specific handlers, 0
semantic cases (switch/match count 0 in the driver). K2c: architecture
accounting: the variant cores are unchanged byte copies (0-line delta);
the driver is a lane-dir fixture; cognition-source delta on the frozen
path 0/0/0; zero new modes/bridges/handlers; zero new node tags, edge
types, or subsystem state formats; the ONE-SYSTEM RULE is checked
explicitly: one persistent arena (the same 110656-byte layout), the
proposal is a tag-1 node in POLICY_ROOT space (the same existing format
as learner guides), and nothing adds an independent state format. K2d:
pure Zag plus shell only; `which python3` prints nothing under the
safebin PATH (NAMECHECK.md Step 0).

K3 (no regression): the committed 2321pdt `lo_driver` binary re-run 3x
read-only (feed "TREAT" on stdin per the CONTLEARN/RUN_LOG.md lesson);
stdout SHA-256 must equal
1ff527fa97b36da25fd8163299773680e53ae47fba521fc2227b0bf7c39394d9 on all
3 reps. Kill: any mismatch.

## 6. Frozen decision rule

- LH-SUSTAINED iff CP-LH1, CP-LH2, CP-LH3, CP-LH4, CP-LH5, CP-LH6, K0,
  K1, K2, K3 all pass, with the claim bound of section 7: the
  proposal-first ordering and the DEP-cited MAP structure survive
  sustained interference with a flat retention curve at 12/12 over
  V=52/152/276, in one process with no reset, no task label, no
  recompilation. BUILD-PASS.
- LH-DEGRADED iff CP-LH3 fails (any REUSE_X below 12/12) while CP-LH2
  passes (the chains integrated): informative negative; retention
  degrades with horizon. Followed by root-cause analysis, not by new
  handlers, modes, or opcodes. BUILD-FAIL for the sustained claim; the
  numbers stand as the measured curve.
- MACHINERY-ORDER-VIOLATION-LH iff CP-LH1 fails while CP-LH2 passes
  (machinery engaged without a preceding proposal, including at the
  late-novel horizon): informative negative on the instrument.
- VOID iff K0, K1, K2, K3, CP-LH5, or CP-LH6 fails: instrument failure,
  no verdict. A CP-LH6 failure with CP-LH2 passing is reported as an
  anomaly with root-cause analysis.

## 7. Exact claim bound (frozen)

If LH-SUSTAINED: on the fixed disclosed 358-event battery, with the
trial/promotion machinery gated on a learner-state proposal channel, the
continuing learner integrates 6/6 novel 2-hop chains (MAPs with DEP
citations to the licensing facts and to the licensing proposals), reuses
12/12 original values at each of three interference volumes (52, 152,
276 interfering events: three unrelated-fact episodes of 48/96/120 plus
conflict and correction episodes, including conflicting evidence on a
subset of the original chain facts themselves), integrates 2/2 novel
chains at the longest horizon with proposal-before-machinery ordering
maintained (8/8 ordered pairs, 0 skips), and retains 12/12 pre-conflict
values, all 3/3 byte-identical, in one process with no reset, no task
label, and no recompilation.

Explicitly not shown: learner authorship of proposal content (the
mech=TRY_CHAIN code is a fixed researcher template, disclosed); learner
scheduling of proposal initiation (still event-triggered); learner
agency in the causal sense (H2-v2/H3 stand); procedure execution at
query time; any L3 or generality claim; the instrument is not a proposed
architecture; the battery is disclosed, not sealed adversarial. The
red-team self-review must attack whether the longer horizon is a real
test (does interference actually threaten the DEP citations?) and whether
the retention curve discriminates anything the single point did not.

## 8. What this prereg does NOT authorize

- No implementation in this commit.
- No modification of the instrument cores beyond byte-copying the
  recorded CONTLEARN files; no new cognitive machinery of any kind: no
  new Zag subsystems, modes, bridges, routers, task-specific handlers,
  semantic cases, node tags, edge types, ISA opcodes, or subsystem state
  formats.
- No tuning of any kind to this battery.
- No sealed adversarial worlds; the script is disclosed. The post-freeze
  adversarial battery remains the generality test and is separate.
- The 2321pdt binary is re-run read-only for K3; it is not rebuilt and
  not modified.
