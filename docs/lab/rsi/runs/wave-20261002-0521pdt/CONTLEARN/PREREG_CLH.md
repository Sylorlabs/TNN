# PREREG_CLH: longer-horizon delayed REBIND under sustained interference (frozen)

Status: PREREG-FROZEN (design only; no implementation in this commit).
Wave: wave-20261002-0521pdt. Lane: CONTLEARN (CLH2, backlog item 29).
Date: 2026-10-02. Worker phase: 1 (writing only). Implementation
authorized only after the coordinator commits this prereg alone.

Note: this document uses hyphens only; no em or en dashes appear.

## 0. Commit order (K0)

This prereg is committed with only lane documentation
(docs/lab/rsi/runs/wave-20261002-0521pdt/CONTLEARN/): NAMECHECK.md and
this file. No implementation file of this lane may exist at or before
the prereg commit. The implementation commit must be a strict descendant
of the prereg commit, verified by `git merge-base --is-ancestor
<prereg-sha> <impl-sha>` before any verdict is reported. UNVERIFIABLE
ORDERING voids the prereg. No bar may be altered after results are seen;
amendment requires a transparent re-freeze.

## 1. Question and lineage

Lineage: CONTLEARN3 PROPOSAL-FIRST-DEMONSTRATED (0221pdt; proposal-gated
integration, 12/12 delayed reuse after a 24-event gap, binding caveats
below); CONTLEARN-LH LH-DEGRADED (0221pdt; retention curve 12/12, 10/12,
8/12 at V=52/152/276; unrelated interference caused ZERO degradation;
losses were exactly the deliberately conflicted chains, localized to
single-propagation revision semantics, instrument-independent).

This lane (CLH2) is the queued backlog item 29 follow-up. CONTLEARN-LH
tested RETENTION (same probes repeated). This lane tests REBIND: after a
capability session and unrelated interference sessions (memory pressure,
unrelated conflicting evidence, a second task family), the learner faces
NEW problems (new subjects, new relations, new entry points into the old
chains) that can only be solved by recruiting the earlier structure. The
delay and the interference are the test: does the structure survive and
get rebound for a new problem, in one process, with no reset, no task
labels, no recompilation, no re-teaching of the earlier knowledge.

Honest status, frozen here (binding on the verdict and the red team,
carried over from CONTLEARN3):

- The proposal CONTENT (mech=TRY_CHAIN) is a fixed researcher template
  in the measurement instrument. This experiment does NOT claim learner
  authorship of proposal content, learner scheduling of proposal
  initiation (still event-triggered), or learner agency in the causal
  sense.
- The gate's refusal branch is structurally enforced but empirically
  unexercised (0 MACHINERY_SKIPPED expected again; this lane does not
  exercise it either, and says so).
- No L3, no generality. The battery is disclosed and prereg-frozen, not
  adversary-designed. "Sealed" in this lane means: the battery is frozen
  before implementation, all ids and relations are fresh and verified
  unused, all oracles are content-identified (no assumed node ids), and
  no tuning to results is permitted. It does not mean sealed adversarial
  worlds; those remain the separate generality test.
- Citation form stays machinery-enabled per the debate Q7 binding form.
- The variant cores are measurement instruments, not proposed
  architectures.

## 2. The instrument

Frozen core: docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag,
SHA-256 a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd.
Recorded nomain derivation: cl_core_nomain.zag in the 2021pdt CONTLEARN
lane, SHA-256
26b455e78a9b0ba0f6d6967c12ff8c05f9ebd9152dddca9efeb2a3b44064ec9d
(verified again before any build; the frozen file is never written).

This lane builds NO new instrument. The two cores are byte copies of the
recorded 0221pdt CONTLEARN lane files (hashes verified before the
builds):

- `clh2_core_treat.zag`: byte copy of pf_core_treat.zag (the
  proposal-gated instrument from CONTLEARN3), recorded SHA-256
  627af6eb0e88141fdeb00baba0aab178a29df128aa0250398355db42d8557f63.
- `clh2_core_control.zag`: byte copy of pf_core_control.zag (the
  unmodified frozen core), SHA-256 equal to the nomain derivation
  26b455e78a9b0ba0f6d6967c12ff8c05f9ebd9152dddca9efeb2a3b44064ec9d.

The only new source in this lane is the driver: `clh2_driver_full.zag`
(the frozen 166-event script with content-identified oracles) and
`clh2_driver_nophase.zag` (the frozen 142-event structure-dependence
control script, phase A elided, same oracles). Three binaries, built once
before any run, via the logged wrapper: clh2_treat (treat core + full
driver), clh2_control (control core + full driver), clh2_nophase (treat
core + nophase driver).

Structural-difference statement: no prior lane tested rebind (new
problems through old structures); CONTLEARN3 tested proposal-first
integration with identical probes, CONTLEARN-LH tested retention curves.
The new battery plus the no-phase-A discriminator is the new content;
the cores are unchanged instruments.

## 3. Experience sequences (exact, frozen, fresh)

All subject/object ids (96001..96202, 96301..96497, 96501, 96601..96603,
96701..96902, 97001..97106) and all relations (850, 851, 852, 853, 854,
855, 857, 858, 862, 863, 864, 866) are unused by any prior battery in the
wave-20261001 and wave-20261002 .zag sources (verified by grep before
writing this prereg; the 95300+ id block and these relations have zero
hits). Event kinds: 1=TEACH (ev_teach), 2=MQUERY (ev_query, expected=-2,
flags=1: disclosed supervisor disconnect, not a task label), 3=OBSERVE
(ev_observe: the frozen counterexample protocol, integer (s,r,o)
operands only, not a task label). PHASE markers are driver-side prints
and never reach cognition.

### 3a. FULL script (166 events), TREAT and CONTROL binaries, one process per run

- CAPABILITY (18 events): new vocabulary as fresh 2-hop chains.
  - for i in 0..5: TEACH(96001+i, 850, 96101+i) (chain heads).
  - for i in 0..5: TEACH(96101+i, 851, 96201+i) (chain tails).
  - for i in 0..5: MQUERY(96001+i, 852) (relation 852 novel: machinery
    integrates MAP(96001+i,852) with DEP edges to the licensing chain
    facts; expected answer 96201+i).
- INT1 memory pressure (96 events):
  - for i in 0..95: TEACH(96301+i, 853, 96401+i).
- INT2 unrelated conflict plus correction (4 events):
  - TEACH(96501, 854, 96601) (fact A, unrelated to the chains).
  - OBSERVE(96501, 854, 96602) (contradictory evidence B; rv=0; A
    superseded, B taught).
  - OBSERVE(96501, 854, 96603) (correction C; rv=0; B superseded, C
    taught).
  - MQUERY(96501, 854) (must return 96603).
- INT3 second task family (18 events): new vocabulary, new chains.
  - for i in 0..5: TEACH(96701+i, 855, 96801+i).
  - for i in 0..5: TEACH(96801+i, 857, 96901+i).
  - for i in 0..5: MQUERY(96701+i, 858) (novel; expected 96901+i).
- RETENTION (6 events): manipulation check before rebind.
  - for i in 0..5: MQUERY(96001+i, 852) expecting 96201+i.
- REBIND anchors (12 events): new problems anchored into the old chains.
  - for i in 0..5: TEACH(97001+i, 862, 96101+i) (tail anchors: new
    subjects bound to the phase-A mid-chain nodes).
  - for i in 0..5: TEACH(97101+i, 864, 96001+i) (head anchors: new
    subjects bound to the phase-A chain roots).
- REBIND queries (12 events): new problems, new relations, no re-teaching.
  - for i in 0..5: MQUERY(97001+i, 863) (novel; expected 96201+i via the
    2-hop chain 862->851 through the surviving phase-A tail facts).
  - for i in 0..5: MQUERY(97101+i, 866) (novel; expected 96101+i via the
    2-hop chain 864->850 through the surviving phase-A head facts).

Node/edge budget: worst case about 520 alive nodes and under 2000 live
edges (135 taught facts, 24 promoted answer facts, 24 MAPs, 24 proposals,
about 300 executable-graph cells); far below the 1024/4096 caps, so no
eviction can occur and any missing structure is evidence, not capacity.
Capacity guard (VOID if tripped): any per-phase census showing 900 or
more alive nodes or 3500 or more live edges.

### 3b. NOPHASE script (142 events), clh2_nophase binary (treat core)

Identical to FULL except the CAPABILITY block (18 events) and the
RETENTION block (6 events) are elided: INT1 (96), INT2 (4), INT3 (18),
REBIND anchors (12), REBIND queries (12). The rebind anchors reference
96101+i and 96001+i as plain integers, but no phase-A facts exist, so no
chain can be completed through them. Frozen prediction, derived from the
frozen source (t2_trial order: k=2..4 chain loop, then comb, then the
di==0 count branch, then the 2-node fallback): with only the anchor
facts present, no len>=3 path exists, comb is absent, and the count
branch verifies a 1-link count graph whose execution yields 1
(t2_asm_count MOVE r0<-r1 epilogue after one INC). Expected rebind
answers: 1 on all 12 queries, with MAPs that cite only the anchor facts.

### 3c. Why these rebind problems test structure reuse, not recall

The rebind queries use new subjects (97001+i, 97101+i) and new relations
(863, 866) that were never taught. No fact with (97001+i,863) or
(97101+i,866) exists before the query. The only route to the expected
answers is chain discovery through the phase-A facts taught 148 events
earlier and never re-taught. The new MAPs must DEP-cite the phase-A
facts (provenance), binding old structure into the new problem's
solution. The NOPHASE control proves the answers are structure-caused:
same machinery, same interference, same problems, no phase-A structure
gives different answers (1, not 96201+i / 96101+i).

A further derivation frozen here: for the head family, t2_gather from
97101+i finds two len-3 paths, [U,S,A] via fact(96001+i,850,96101+i) and
[U,S,B] via the promoted fact(96001+i,852,96201+i). The k=2 loop tries
paths in discovery order; discovery scans fact nodes in ascending node
id, and the 850 head fact was allocated before the 852 answer fact, so
[U,S,A] is tried first and verifies, giving 96101+i deterministically.
If the run instead yields 96201+i on the head family, CP-R1 fails and the
root cause is analyzed honestly; the bar is not moved.

## 4. White-box measurement oracles

All predicates are structural (tag/field/edge/reachability) over the live
arena through the core's own accessors, content-identified, never by
assumed id ranges.

- fact(s,r,o): tag==1, alive, field20==s, field24==r, field28==o.
- map(sbj,rel): tag==20, alive, field8==sbj, field4==rel.
- proposal(s,r): tag==1, alive, field20==30, field24==-998, field4==s,
  field28==r.
- superseded(n): type-3 self-edge on n exists (is_superseded==1).
- serve_ok(s,r,exp,got): got==exp and activate(s,r) returns the live
  content-expected fact node (tag-1, not superseded, fields match).

REBIND_OK (end of REBIND, TREAT/CONTROL): for i in 0..5, tail:
a=MQUERY(97001+i,863); serve_ok(97001+i,863,96201+i,a)==1 AND
map(97001+i,863) exists AND has an alive DEP edge to
fact(96101+i,851,96201+i) AND has an alive DEP edge to the anchor fact
(97001+i,862,96101+i). Head: a=MQUERY(97101+i,866);
serve_ok(97101+i,866,96101+i,a)==1 AND map(97101+i,866) exists AND has an
alive DEP edge to fact(96001+i,850,96101+i) AND has an alive DEP edge to
the anchor fact (97101+i,864,96001+i). Bar: 12/12.

REBIND_PROP_CITE (TREAT only): each of the 12 rebind MAPs has an alive
DEP edge to its licensing proposal node. Measured and reported;
expected 12/12 on TREAT, 0/12 on CONTROL (no proposals exist there).

SURVIVE_OK (after REBIND, TREAT/CONTROL): for i in 0..5,
map(96001+i,852) is live AND has alive DEP edges to
fact(96001+i,850,96101+i) and fact(96101+i,851,96201+i) (both live) AND
fact(96001+i,852,96201+i) is live. Bar: 6/6.

RETAIN_OK (RETENTION, TREAT/CONTROL): 6/6 probes (96001+i,852) return
96201+i with serve_ok.

INT_OK (TREAT/CONTROL): pressure: 96/96 facts (96301+i,853,96401+i)
live; INT2: fact(96501,854,96601) superseded, fact(96501,854,96603) live,
MQUERY(96501,854) returns 96603 with serve_ok (1/1 episode);
STORE3_OK: 6/6 map(96701+i,858) exist with alive DEP edges to the INT3
chain facts and integrate answers 96901+i.

NOPHASE_OK (clh2_nophase): 12/12 rebind answers == 1; phase-A facts
absent: pf_find_fact(96001,850,96101)==-1 and
pf_find_fact(96101,851,96201)==-1; NOPHASE integrity: INT3 STORE3_OK 6/6,
pressure 96/96, INT2 episode 1/1 (proves the nophase learner is
functional, so the 1-answers are machinery behavior, not breakage).

ORDER (TREAT, transcript shell check): exactly 24 PROPOSAL lines and
exactly 24 MACHINERY lines, zero MACHINERY_SKIPPED lines; for each of
the 12 rebind (s,r) pairs the PROPOSAL line appears at an earlier
transcript line than the MACHINERY line for the same (s,r), naming the
same live proposal node id.

Mechanism census per phase: MAPC, PROPC, DEPC, UNC, GUIDEC, N1, Eall (as
in CONTLEARN3).

## 5. Frozen kill bars

CP-R0 (proposal-before-machinery on the new problems, TREAT): ORDER
passes: 24/24 PROPOSAL before MACHINERY, 0 skips, 12/12 rebind pairs
ordered with matching prop node ids.

CP-R1 (rebind success, TREAT): REBIND_OK == 12/12.

CP-R2 (structure survival, TREAT): SURVIVE_OK == 6/6.

CP-R3 (retention, TREAT): RETAIN_OK == 6/6.

CP-R4 (interference integrity, TREAT): INT_OK holds (pressure 96/96,
INT2 1/1, STORE3_OK 6/6).

CP-R5 (structure dependence, clh2_nophase): NOPHASE_OK holds (12/12
answers == 1, phase-A facts absent, nophase integrity 6/6, 96/96, 1/1).

CP-R6 (determinism): 3/3 byte-identical stdout per binary (SHA-256 equal
across reps), printed FNV-1a arena checksums equal, exit code 0, zero
stderr bytes, no PID/timestamps/paths in transcripts.

CP-R7 (control reproduces, CONTROL): REBIND_OK_C == 12/12,
SURVIVE_OK_C == 6/6, RETAIN_OK_C == 6/6, and the transcript contains zero
PROPOSAL lines (machinery-first ordering confirmed). Anomaly clause: a
CP-R7 divergence with CP-R1 passing is reported as an anomaly with
root-cause analysis (CONTLEARN-LH precedent), not as VOID; the rebind
claim then carries the anomaly explicitly.

Governance bars:

K0: prereg committed alone with only lane docs; implementation strictly
descendant; merge-base verified before verdict.

K1 (one learner, no reset, no recompile, no task labels): K1a: exactly 9
learner processes total (3 binaries x 3 reps), one process per full run;
transcripts contain no PID; harness log records spawns. K1b: znc wrapper
logs every invocation; exactly 3 entries (the three pre-run builds)
before the runs; 0 new entries during the runs. K1c: driver self-audit;
every tuple flows through the choke points with kind in {1,2,3} and
plain integer operands; MQUERY carries the frozen parameters expected=-2,
flags=1 (disclosed supervisor disconnect, not a task label); OBSERVE
(kind 3) is the frozen counterexample protocol (ev_observe), disclosed
here, not a task label; PHASE markers never reach cognition; all runs
launch with empty argv and empty env; expected audited counts 166 per
FULL run and 142 per NOPHASE run; prints AUDIT_PASS.

K2 (frozen ISA boundary and architecture accounting): K2a: SHA-256 of the
frozen tnn2.zag equals
a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd before
the builds and after the runs; the recorded nomain derivation hash equals
26b455e78a9b0ba0f6d6967c12ff8c05f9ebd9152dddca9efeb2a3b44064ec9d before
the builds; both lane cores hash-equal their recorded 0221pdt CONTLEARN
sources before the builds; the frozen path is never written. K2b: driver
source audit on both driver files: 0 cognition functions, 0 structural
writes (ns(/link_edge(/alloc_node( count 0 in each driver), 0 new node
tags, 0 new edge types, 0 new opcodes, 0 modes, 0 bridges, 0 routers, 0
task-specific handlers, 0 semantic cases (switch/match count 0 in each
driver). K2c: architecture accounting: the variant cores are lane-dir
measurement instruments, not changes to the frozen architecture;
cognition-source delta on the frozen path 0/0/0; lane cores 0-line delta
(byte copies); the drivers are lane fixtures; zero new modes, bridges,
handlers, node tags, edge types, ISA opcodes, or subsystem state
formats; the ONE-SYSTEM RULE is checked explicitly: one persistent arena
(the same 110656-byte layout), proposals as tag-1 nodes in POLICY_ROOT
space (the existing learner-guide format), no independent state format
anywhere. K2d: pure Zag plus shell only; `which python3` prints nothing
under the safebin PATH (NAMECHECK.md Step 0).

K3 (no regression): the committed 2321pdt `lo_driver` binary re-run 3x
read-only (stdin "TREAT" per the CONTLEARN3 K3 lesson); stdout SHA-256
must equal
1ff527fa97b36da25fd8163299773680e53ae47fba521fc2227b0bf7c39394d9 on all
3 reps. Kill: any mismatch.

## 6. Frozen decision rule

- REBIND-DEMONSTRATED iff CP-R0, CP-R1, CP-R2, CP-R3, CP-R4, CP-R5,
  CP-R6, CP-R7, K0, K1, K2, K3 all pass, with the explicit claim bound of
  section 1 and section 7.
- REBIND-FAIL iff CP-R1 fails (the gated learner does not rebind the
  earlier structure for the new problems): informative negative with
  root-cause analysis, not followed by new handlers, modes, or opcodes.
- STRUCTURE-LOST iff CP-R2 fails: reported with root-cause analysis; if
  CP-R1 passed simultaneously, reported as an anomaly (rebind without
  surviving MAPs) with the provenance traces that explain it.
- DISCRIMINATOR-FAIL iff CP-R5 fails (the rebind answers are obtainable
  without the phase-A structure, or the nophase learner is broken): kills
  the structure-dependence interpretation; reported honestly.
- VOID iff K0, K1, K2, K3, CP-R6 fail, or the capacity guard trips. A
  CP-R7 divergence is an anomaly with root-cause analysis, not VOID.

## 7. Exact claim bound (frozen)

If REBIND-DEMONSTRATED: on the fixed disclosed 166-event battery, the
continuing proposal-first learner integrates 6/6 novel 2-hop chains,
then, after 118 unrelated interference events (96 memory-pressure facts,
one unrelated conflict-plus-correction episode, and a second 2-hop
chain family with its own 6/6 novel integrations), rebinds the phase-A
structure for 12/12 new problems (new subjects, new relations 863/866,
new entry points into the old chains) with correct answers served by new
MAPs DEP-citing the never-re-taught phase-A facts, while the 6/6
phase-A MAPs stay live with intact citations and 6/6 retention probes
hold; the 12/12 rebind answers are structure-caused (the no-phase-A
control gives 1, not the chain answers, on the identical machinery); all
3/3 byte-identical, in one process per run with no reset, no task label,
and no recompilation.

Explicitly not shown: learner authorship of proposal content (the
mech=TRY_CHAIN code is a fixed researcher template, disclosed); learner
scheduling of proposal initiation (still event-triggered); learner
agency in the causal sense; exercise of the refusal branch (0
MACHINERY_SKIPPED again); procedure execution at query time; any L3 or
generality claim; the cores are not proposed architectures; the battery
is disclosed and prereg-frozen, not sealed adversarial.

## 8. What this prereg does NOT authorize

- No implementation in this commit.
- No new cognitive machinery of any kind: no new Zag subsystems, modes,
  bridges, routers, task-specific handlers, semantic cases, node tags,
  edge types, ISA opcodes, or subsystem state formats. The drivers are
  fixtures; the cores are byte copies.
- No tuning of any kind to this battery; K2a and the recorded hashes
  forbid edits beyond the frozen byte copies and the two fixture
  drivers.
- No sealed adversarial worlds; the script is disclosed and frozen. The
  post-freeze adversarial battery remains the generality test and is
  separate.
- The 2321pdt lo_driver binary is re-run read-only for K3; it is not
  rebuilt and not modified.
- No weakening of any frozen bar after results; amendment requires a
  transparent re-freeze, never an edit.
