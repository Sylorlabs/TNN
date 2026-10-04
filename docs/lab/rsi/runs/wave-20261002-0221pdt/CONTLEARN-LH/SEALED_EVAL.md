# SEALED_EVAL: CONTLEARN-LH longer-horizon delayed reuse (frozen execution)

Wave: wave-20261002-0221pdt. Lane: CONTLEARN-LH. Frozen prereg:
PREREG_CONTLEARN_LH.md (commit 8d43c6e55) plus transparent
pre-implementation Amendment 1 (commit 32bfea311; event-count arithmetic
358 to 356, no design change). Implementation strictly descendant;
merge-base check recorded in VERDICT.

## Run record

Harness: run_lh.sh. 2 binaries x 3 reps = 6 learner processes, one
process per full 356-event run, empty argv, empty environment. All 6
exited rc=0. harness_lh.log: total_spawns=6 (TREAT 3, CONTROL 3),
pid_leak_check=0, znc_invocations_during_runs=2 (the two pre-run builds;
0 during runs). All 6 stderr files 0 bytes.

Transcripts (SHA-256):
- TREAT r1/r2/r3: 644ba03f719c185f3de04445880df0a6fcacec7c3391b2198d545b6d4d2a803d (3/3 byte-identical)
- CONTROL r1/r2/r3: 3ac5697ab195b5253610b416e4bc6fd04c76cf938678e6b23062781491dd94ef (3/3 byte-identical)
- FNV arena checksums: TREAT -1320742499 x3; CONTROL 1020256801 x3.
- AUDIT_PASS on all 6 runs (356 events each).

## Per-bar results (TREAT, proposal-gated)

| Bar | Result | Evidence |
|-----|--------|----------|
| CP-LH1 ordering maintained 8/8, 0 skips | PASS | 8 PROPOSAL occurrences, 8 MACHINERY lines, 0 MACHINERY_SKIPPED on all 3 reps; per-(s,r) line check: every PROPOSAL precedes its MACHINERY line with matching prop node ids (6 NOVEL pairs nodes 14/27/39/51/63/75; 2 LATE-NOVEL pairs nodes 394/406); PROPC_FINAL==8 |
| CP-LH2 integration under proposal-first | PASS | STORE_OK 6/6, STORE_PROP_CITE 6/6 (NOVEL); LATE_STORE_OK 2/2, LATE_PROP_CITE 2/2 (LATE-NOVEL at longest horizon) |
| CP-LH3 retention curve | FAIL | REUSE_A 12/12 at V=52; REUSE_B 10/12 at V=152; REUSE_C 8/12 at V=276. Serving-node checks; no re-teaching. The misses are exactly the chains whose licensing chain facts were deliberately conflicted (chains 0,1 at B; chains 0-3 at C). See root-cause analysis below and REDTEAM_SELF.md |
| CP-LH4 conflict/correction/retention | PASS | CONFLICT1_OK 1/1, CORRECT1_OK 1/1, CONFLICT2_OK 1/1, CORRECT2_OK 1/1, CONFLICT3_OK 1/1, CORRECT3_OK 1/1; RETENTION_OK 12/12 pre-conflict values |
| CP-LH5 determinism | PASS | 3/3 byte-identical stdout per binary, equal FNV, rc=0, 0 stderr bytes, no PID/timestamps/paths |

Census note (TREAT, FINAL): MAPC=8 PROPC=8 DEPC=44 UNC=0 GUIDEC=0 N1=317
Eall=463; far below the 1024/4096 caps; no eviction. UNC=0 throughout
(every novel miss engaged the trial path).

## CONTROL (unmodified frozen core, machinery-first)

STORE_OK_C 6/6, STORE_PROP_CITE_C 0/6 (expected: no proposal channel),
LATE_STORE_C 2/2, LATE_PROP_CITE_C 0/2, RETENTION_OK_C 12/12, all
CONFLICT/CORRECT checks 1/1, PROPC_FINAL 0, zero PROPOSAL occurrences in
all 3 transcripts, 3/3 byte-identical. REUSE curve on CONTROL: 12/12 at
V=52, 10/12 at V=152, 8/12 at V=276, identical to TREAT rep for rep.

CP-LH6 anomaly (prereg section 6 anomaly clause applies): the control
does not meet the literal 12/12/12 sub-expectation, but it reproduces the
TREAT curve EXACTLY with machinery-first ordering (zero PROPOSAL). The
degradation is instrument-independent: a property of the frozen core's
revision semantics under subset-conflict interference, not a control
failure. Root-cause analysis below; the control functioned as a
baseline.

## Root-cause analysis of the CP-LH3 misses (post-hoc diagnostic, /tmp)

A read-only diagnostic driver (identical 356-event script, extra end-of-
run dump only; run once in /tmp, not part of the sealed 6) shows the
mechanism precisely. For each conflicted chain (i=0..3):

- Chain facts: original (22001+i, superseded), contradictory (22101+i,
  superseded), resolved (22111+i, live). The revision protocol behaved
  as designed at the fact level.
- Integrated facts (23001+i,522): TWO nodes. The original (22001+i) is
  superseded; a NEW live node holds the CONTRADICTORY value (22101+i).
  No integrated fact holds the resolved value (22111+i).
- MAP DEP citations are intact: each MAP cites the anchor fact (live),
  the original chain-fact node (superseded, the licensing fact at
  promotion time), and the proposal node (live). Citations were not
  broken or removed by any interference.

Mechanism: when CONFLICT-2 contradicted a licensing chain fact, the
frozen revision operator propagated downstream: it superseded the
original integrated fact and created a new integrated fact with the
contradictory value (node ids 148/153 in the CONFLICT-2 era), i.e. the
MAP's executable composition was restructured and re-executed live. When
CORRECTION-2 later superseded the contradictory fact and taught the
resolved fact, NO downstream update fired: the correction superseded a
node (the contradictory fact) that the MAP does not cite, so the
composed structures stayed frozen at the contradiction's value.
Single-propagation revision: contradiction propagates downstream once;
correction does not re-propagate.

What this means for the curve: unrelated-domain interference (264 facts
across three episodes) caused ZERO degradation (REUSE_A 12/12; chains
4,5 and the sanity family intact through V=276). The 12 to 10 to 8
curve counts exactly the chains whose licensing facts were deliberately
conflicted (2, then 4). The DEP-cited MAP structure survived sustained
interference structurally; what changed was the composed ANSWER, via
live downstream revision that tracked the contradiction but not the
correction.

Oracle note (honest): the frozen CP-LH3 oracle demanded the ORIGINAL
values after the battery deliberately injected conflicting evidence on
the underlying chain facts. The learner's behavior (track the
contradiction live, stick after correction) is a precise, deterministic,
instrument-independent property of the frozen revision operator, not
noise. The numbers stand as the measured curve.

## Governance bars

K0: prereg 8d43c6e55 + amendment 32bfea311 both strict ancestors of the
implementation commit (merge-base verified in VERDICT).
K1a: 6 processes, one per 356-event run; harness log records all spawns;
pid_leak_check=0. K1b: znc_invocations_lh.log has exactly 2 entries
(pre-run builds), 0 new during runs. K1c: AUDIT_PASS on all 6 runs
(356 events each); kinds in {1,2,3}; MQUERY expected=-2, flags=1;
OBSERVE is the frozen counterexample protocol (disclosed); empty argv/env.
K2a: frozen tnn2.zag SHA-256 a29972ca... verified before builds and after
runs; nomain derivation 26b455e7... verified before builds (lane cores
are byte copies: 627af6eb... TREAT, 26b455e7... CONTROL); the frozen
path was never written. K2b: driver audit 0/0/0/0/0 (ns(, link_edge(,
alloc_node(, switch, match counts 0 in lh_driver.zag). K2c: frozen-path
delta 0/0/0; lane cores 0-line delta (byte copies); driver is a lane-dir
fixture (lh_driver.zag, 14171 bytes); 0 new modes/bridges/handlers/tags/
edges/opcodes/state formats; ONE-SYSTEM RULE checked explicitly (single
110656-byte arena, proposals as tag-1 nodes in POLICY_ROOT space,
existing formats only). K2d: pure Zag plus shell; `which python3` empty
under safebin PATH (NAMECHECK.md Step 0); one self-disclosed non-
incident (a stray `python3 -c` probe typed in a shell command that did
not resolve under the safebin PATH; no Python process ran; recorded in
RUN_LOG.md).
K3: committed 2321pdt lo_driver re-run 3x read-only (stdin "TREAT" per
the CONTLEARN/RUN_LOG.md lesson); stdout SHA-256 1ff527fa... on all 3
reps; rc=0; 0 stderr bytes. PASS.
