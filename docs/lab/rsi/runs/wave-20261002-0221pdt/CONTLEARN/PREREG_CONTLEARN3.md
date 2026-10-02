# PREREG_CONTLEARN3: mechanism-proposal-first continuing learner (frozen)

Status: PREREG-FROZEN (design only; no implementation in this commit).
Wave: wave-20261002-0221pdt. Lane: CONTLEARN. Date: 2026-10-02.
Worker phase: 1 (writing only). Implementation authorized only after the
coordinator commits this prereg alone.

Note: this document uses hyphens only; no em or en dashes appear.

## 0. Commit order (K0)

This prereg is committed with only lane documentation
(docs/lab/rsi/runs/wave-20261002-0221pdt/CONTLEARN/): NAMECHECK.md and this
file. No implementation file of this lane may exist at or before the
prereg commit. The implementation commit must be a strict descendant of
the prereg commit, verified by `git merge-base --is-ancestor <prereg-sha>
<impl-sha>` before any verdict is reported. UNVERIFIABLE ORDERING voids
the prereg. No bar may be altered after results are seen; amendment
requires a transparent re-freeze.

## 1. Question and lineage

Lineage: CONTLEARN INTEGRATION-DEMONSTRATED (REUSE_COUNT 30/30);
LEARNOWN-DEMONSTRATED red-team QUALIFY (machinery integration under
per-query supervision, not learner-owned); CONTLEARN-OWNED/OWNED2
MACHINERY-DEPENDENT (0/6 vs 6/6, doubly confirmed); LEARNER-MECH /
MECH-VERIFY root cause: the frozen core has no learner-state initiation
path; learner state is read as DATA, never as CONTROL.

This experiment is the queued mechanism-proposal-first design: the learner
itself must propose the mechanism/instruction for a novel continuing task
BEFORE any researcher machinery engages. It is NOT another
machinery-disabled replication of the old CONTLEARN-OWNED design (that
replication is explicitly excluded by the queued instruction).

Honest status, frozen here (binding on the verdict and the red team):

- The proposal CONTENT (mech=TRY_CHAIN, the instruction code) is a fixed
  researcher template in the measurement instrument. This experiment does
  NOT claim learner authorship of proposal content.
- What IS measured: (a) the control plane structurally cannot engage the
  trial/promotion machinery without a live learner-state proposal
  structure for (s,r): a proposal gate in the miss path checks learner
  state first, and engagement is refused (logged as MACHINERY_SKIPPED)
  when no proposal exists; (b) the proposal structure lives in learner
  state (POLICY_ROOT space, tag-1 node, type-10 link: the same existing
  format as learner guides, no new tags, no new edge types, no new state
  formats); (c) the promoted MAP cites the licensing proposal with a
  type-1 DEP edge, giving white-box provenance of proposal-before-
  machinery; (d) the transcript shows PROPOSAL before MACHINERY for every
  novel task.
- Initiation of the proposal write is still event-triggered (the
  instrument's miss path), not learner-scheduled. The gate reads learner
  state as CONTROL (a step on the LEARNER-MECH control-parameter axis),
  but the parameters are not learner-derived. The red-team self-review
  must attack exactly these points.

## 2. The instrument: proposal-gated variant core (TREAT)

Frozen core: docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag,
SHA-256 a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd.
Recorded nomain derivation: cl_core_nomain.zag in the 2021pdt CONTLEARN
lane, SHA-256
26b455e78a9b0ba0f6d6967c12ff8c05f9ebd9152dddca9efeb2a3b44064ec9d
(verified again before any build; the frozen file is never written).

TREAT core `pf_core_treat.zag` is derived mechanically from that nomain
derivation with exactly these changes (the full diff is recorded before
any run; the diff is larger than the OWNED lanes' because this is a
control-plane instrument, not a deletion):

- New fn `pf_find(W,s,r)`: returns the live proposal node for (s,r), or
  -1. Proposal signature: tag==1, alive, field20==30, field24==-998,
  field4==s, field28==r. (Guides use field24==-999; the proposal marker is
  -998. Existing tag, existing fields, existing formats only.)
- New fn `pf_propose(W,s,r)`: allocates a tag-1 node, ns(field4)=s,
  write_node(30,-998,r,1) (field20=30, field24=-998, field28=r,
  field32=mech=1 meaning TRY_CHAIN), creates POLICY_ROOT if absent (same
  pattern as miss_inquire), links the proposal to POLICY_ROOT with a
  type-10 edge, emits the trace line
  `PROPOSAL s=<s> r=<r> mech=1 node=<p>`, and logs kind-5
  log_ev(W,5,s,r,1,p,0,0). mech=1 is the fixed researcher template named
  in section 1.
- New fn `pf_mp_run(W,s,r,expected,flags)`: the only trial entry in TREAT.
  It calls pf_find first; if no live proposal exists it emits
  `MACHINERY_SKIPPED s=<s> r=<r>` and returns -2 (machinery refused).
  Otherwise it runs the original mp_run logic; on engagement (ans!=-2) it
  links a type-1 DEP edge from each promoted MAP(s,r) node to the proposal
  node (provenance), emits
  `MACHINERY s=<s> r=<r> mech=1 prop=<p> ans=<a>`, and logs kind-6
  log_ev(W,6,s,r,1,p,a,0).
- `ev_query` in TREAT: on the miss path (after the exact-hit and recent-
  link blocks, verbatim), the sequence is: pf_find; if absent,
  pf_propose; then pf_mp_run; then the verbatim bootstrap fallback; then
  the verbatim miss log and miss_inquire. Nothing else in the core is
  touched. The five machinery functions keep their exact logic; only their
  entry is gated.

CONTROL core `pf_core_control.zag` is a byte copy of the recorded nomain
derivation (machinery-first, no proposal gate), reproducing the
DEMONSTRATED behavior.

Structural-difference statement (for the re-freeze requirement): no prior
lane gated machinery engagement on a learner-state structure; OWNED/OWNED2
deleted the engagement path, the 2021pdt lane ran it ungated. This is a
new control-plane ordering instrument plus a new battery.

## 3. Experience sequence (exact, frozen, fresh, one process)

All subject ids (21001..23006, 24001..25006, 26001, 27001..27003,
28001..29024) and all relations (511, 521, 522, 531, 541, 551) are unused
by any prior battery in the wave-20261001 and wave-20261002 .zag sources
(verified by grep before writing this prereg). The script is disclosed,
not adversary-designed. Event kinds: 1=TEACH (ev_teach), 2=MQUERY
(ev_query, expected=-2, flags=1: disclosed supervisor disconnect, not a
task label), 3=OBSERVE (ev_observe: the frozen counterexample protocol,
carrying only integer (s,r,o) operands, not a task label). PHASE markers
are driver-side prints and never reach cognition.

Full script (76 events), both binaries, one process per run:

- NOVEL (24 events): new vocabulary introduction as fresh 2-hop chains.
  - for i in 0..5: TEACH(21001+i, 511, 22001+i) (concept links, relation
    511 is new vocabulary).
  - for i in 0..5: TEACH(23001+i, 521, 21001+i) (anchor links).
  - for i in 0..5: MQUERY(23001+i, 522) (relation 522 is novel: each first
    miss must fire the proposal path, then integrate; expected answer
    22001+i via MAP(23001+i,522) with alive DEP edges to the licensing
    chain facts).
  - for i in 0..5: TEACH(24001+i, 531, 25001+i) (standing sanity family).
- CONFLICT (2 events): one conflicting-evidence episode.
  - TEACH(26001, 541, 27001) (fact A).
  - OBSERVE(26001, 541, 27002) (contradictory evidence B; frozen revision
    protocol supersedes fact A with a type-3 self-edge and teaches fact
    B; returns rv=0).
- CORRECTION (2 events): one correction episode.
  - OBSERVE(26001, 541, 27003) (correction C; supersedes fact B, teaches
    fact C; rv=0).
  - MQUERY(26001, 541) (must return 27003, served by the corrected fact).
- RETENTION (12 events): pre-conflict knowledge probes.
  - for i in 0..5: MQUERY(21001+i, 511) expecting 22001+i.
  - for i in 0..5: MQUERY(24001+i, 531) expecting 25001+i.
- INTERFERE (24 events): for i in 0..23: TEACH(28001+i, 551, 29001+i).
- DELAYED (12 events): reuse without re-teaching.
  - for i in 0..5: MQUERY(23001+i, 522) expecting 22001+i.
  - for i in 0..5: MQUERY(24001+i, 531) expecting 25001+i.

Node/edge budget: TREAT worst case about 150 alive nodes and under 700
edges; far below the 1024/4096 caps, so no eviction can occur and any
missing structure is evidence, not capacity.

## 4. White-box measurement oracles

All predicates are structural (tag/field/edge/reachability) over the live
arena through the core's own accessors, content-identified, never by
assumed id ranges.

- fact(s,r,o): tag==1, alive, field20==s, field24==r, field28==o.
- map(sbj,rel): tag==20, alive, field8==sbj, field4==rel.
- proposal(s,r): tag==1, alive, field20==30, field24==-998, field4==s,
  field28==r.
- superseded(n): type-3 self-edge on n exists (is_superseded==1).

STORE_OK (end of NOVEL): for i in 0..5, map(23001+i,522) exists AND has an
alive DEP edge to fact(21001+i,511,22001+i) AND has an alive DEP edge to
proposal(23001+i,522) AND the integrate query returned 22001+i. Bar: 6/6.

ORDER_OK (TREAT): transcript line-order check per i in 0..5: the PROPOSAL
line for (23001+i,522) appears at an earlier transcript line than the
MACHINERY line for the same (s,r); the MACHINERY line names the same
proposal node id that is live in the census; exactly 6 PROPOSAL lines and
exactly 6 MACHINERY lines exist; zero MACHINERY_SKIPPED lines exist.
Bar: 6/6 ordered pairs, 0 skips.

REUSE_OK (DELAYED): 12/12 probes return stored values with the
content-expected live fact as serving node (6x 22001+i on (23001+i,522),
6x 25001+i on (24001+i,531)), with no re-teaching after INTERFERE.

CONFLICT_OK: after the OBSERVE of B: fact(26001,541,27001) is superseded
(type-3 self-edge present), fact(26001,541,27002) is live.

CORRECT_OK: after the OBSERVE of C: fact(26001,541,27002) is superseded,
fact(26001,541,27003) is live, and MQUERY(26001,541) returns 27003 with
the corrected fact as serving node. Bar: 1/1.

RETENTION_OK: the 12 RETENTION probes return the pre-conflict values
(6x 22001+i on (21001+i,511), 6x 25001+i on (24001+i,531)), after the
conflict and correction episodes. Bar: 12/12.

SANITY_S (TREAT, DELAYED): the 6 (24001+i,531) probes served via
activate. Covered by REUSE_OK/RETENTION_OK; proves the variant is
functional.

Mechanism census per phase: MAPC (alive tag-20), PROPC (proposal-signature
nodes), DEPC (alive type-1), UNC (tag-30), GUIDEC (guide-signature nodes),
N1 (alive tag-1), Eall (all live edges).

## 5. Frozen kill bars

CP-1 (proposal-before-machinery ordering, TREAT): ORDER_OK passes 6/6
with 0 skips and exactly 6/6 PROPOSAL lines preceding their MACHINERY
lines.

CP-2 (integration under proposal-first, TREAT): STORE_OK == 6/6.

CP-3 (delayed reuse without re-teaching): REUSE_OK == 12/12.

CP-4 (conflict/correction/retention): CONFLICT_OK and CORRECT_OK hold,
RETENTION_OK == 12/12.

CP-5 (determinism): 3/3 byte-identical stdout per binary (SHA-256 equal
across reps), printed FNV-1a arena checksums equal, exit code 0, zero
stderr bytes, no PID/timestamps/paths in transcripts.

CP-6 (control reproduces DEMONSTRATED, machinery-first): on the
unmodified frozen core, STORE_OK_C == 6/6 (MAPs with DEP edges to
licensing facts; no proposal citation expected), REUSE_OK_C == 12/12,
RETENTION_OK_C == 12/12, CORRECT_OK_C holds, and the transcript contains
zero PROPOSAL lines (machinery-first ordering confirmed).

Governance bars:

K0: prereg committed alone with only lane docs; implementation strictly
descendant; merge-base verified before verdict.

K1 (one learner, no reset, no recompile, no task labels): K1a: exactly 6
learner processes total (2 binaries x 3 reps), one process per full
76-event run; transcripts contain no PID; harness log records spawns.
K1b: znc wrapper logs every invocation; exactly 2 entries (the two
pre-run builds) before the runs; 0 new entries during the runs. K1c:
driver self-audit; every tuple flows through the choke points with kind
in {1,2,3} and plain integer operands; MQUERY carries the frozen
parameters expected=-2, flags=1 (disclosed supervisor disconnect, not a
task label); OBSERVE (kind 3) is the frozen counterexample protocol
(ev_observe), disclosed here, not a task label; PHASE markers never reach
cognition; all runs launch with empty argv and empty env; expected
audited count 76 per run; prints AUDIT_PASS.

K2 (frozen ISA boundary and architecture accounting): K2a: SHA-256 of the
frozen tnn2.zag equals
a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd before
the builds and after the runs; the recorded nomain derivation hash equals
26b455e78a9b0ba0f6d6967c12ff8c05f9ebd9152dddca9efeb2a3b44064ec9d before
the builds. The frozen path is never written. K2b: driver source audit:
0 cognition functions, 0 structural writes (ns(/link_edge(/alloc_node(
count 0 in the driver), 0 new node tags, 0 new edge types, 0 new opcodes,
0 modes, 0 bridges, 0 routers, 0 task-specific handlers, 0 semantic cases
(switch/match count 0 in the driver). K2c: architecture accounting: the
variant is a lane-dir measurement instrument, not a change to the frozen
architecture; cognition-source delta on the frozen path 0/0/0; added
lines in the variant counted exactly; zero new modes/bridges/handlers;
zero new node tags, edge types, or subsystem state formats; the
ONE-SYSTEM RULE is checked explicitly: one persistent arena (the same
110656-byte layout), the proposal is a tag-1 node in POLICY_ROOT space
(the same existing format as learner guides), and the instrument adds no
independent state format. K2d: pure Zag plus shell only; `which python3`
prints nothing under the safebin PATH (NAMECHECK.md Step 0).

K3 (no regression): the committed 2321pdt `lo_driver` binary re-run 3x
read-only; stdout SHA-256 must equal
1ff527fa97b36da25fd8163299773680e53ae47fba521fc2227b0bf7c39394d9 on all
3 reps. Kill: any mismatch.

## 6. Frozen decision rule

- PROPOSAL-FIRST-DEMONSTRATED iff CP-1, CP-2, CP-3, CP-4, CP-5, CP-6, K0,
  K1, K2, K3 all pass, with the explicit claim bound of section 1: the
  proposal-before-machinery ordering is structurally enforced and
  verified; the novel task integrates under that ordering in one
  continuing learner with no reset, no task label, no recompilation. NOT
  claimed: learner authorship of proposal content, learner agency in the
  causal sense, any L3 or generality claim. Citation form stays
  machinery-enabled per the debate Q7 binding form.
- MACHINERY-ORDER-VIOLATION iff CP-1 fails while CP-2 passes (machinery
  engaged without a preceding proposal): informative negative on the
  instrument; reported honestly with root-cause analysis.
- PROPOSAL-FIRST-FAIL iff CP-2, CP-3, or CP-4 fails (the gated learner
  does not integrate/reuse/retain): informative negative; followed by
  root-cause analysis, not by new handlers, modes, or opcodes.
- VOID iff K0, K1, K2, K3, CP-5, or CP-6 fails: instrument failure, no
  verdict. A CP-6 failure with CP-2 passing is reported as an anomaly
  with root-cause analysis (the control must reproduce the bar).

## 7. Exact claim bound (frozen)

If PROPOSAL-FIRST-DEMONSTRATED: on the fixed disclosed 76-event battery,
with the trial/promotion machinery gated on a learner-state proposal
channel, the continuing learner integrates 6/6 novel 2-hop chains into
MAP structures with DEP citations to the licensing facts and to the
licensing proposal, reuses 12/12 values after an interference gap and
12/12 pre-conflict values after a conflict plus correction episode with
the corrected fact live and superseded predecessors, all 3/3
byte-identical, in one process with no reset, no task label, and no
recompilation.

Explicitly not shown: learner authorship of proposal content (the
mech=TRY_CHAIN code is a fixed researcher template, disclosed); learner
scheduling of proposal initiation (still event-triggered); learner agency
in the causal sense (H2-v2/H3 stand); procedure execution at query time;
any L3 or generality claim; the variant is not a proposed architecture;
the battery is disclosed, not sealed adversarial.

## 8. What this prereg does NOT authorize

- No implementation in this commit.
- No new cognitive machinery of any kind beyond the proposal-gate
  instrument: no new Zag subsystems, modes, bridges, routers,
  task-specific handlers, semantic cases, node tags, edge types, ISA
  opcodes, or subsystem state formats. The variant core is a lane-dir
  measurement instrument; it is not a learner design and must not be
  presented as one.
- No tuning of any kind to this battery; K2a and the recorded diff forbid
  edits beyond the frozen proposal-gate derivation.
- No sealed adversarial worlds; the script is disclosed. The post-freeze
  adversarial battery remains the generality test and is separate.
- The 2321pdt binary is re-run read-only for K3; it is not rebuilt and not
  modified.
- No further machinery-disabled replications of the old CONTLEARN-OWNED
  design (explicitly excluded by the queued instruction).
