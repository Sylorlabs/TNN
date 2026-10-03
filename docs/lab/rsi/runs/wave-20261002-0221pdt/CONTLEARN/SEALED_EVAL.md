# SEALED_EVAL: CONTLEARN3 mechanism-proposal-first (frozen execution)

Wave: wave-20261002-0221pdt. Lane: CONTLEARN. Frozen prereg:
PREREG_CONTLEARN3.md (commit 3bacc8903) plus transparent Amendment 1
(commit 29a11bd85, pre-implementation). Implementation strictly
descendant; merge-base check recorded in VERDICT.

## Run record

Harness: run_pf.sh. 2 binaries x 3 reps = 6 learner processes, one
process per full 76-event run, empty argv, empty environment. All 6
exited rc=0. harness_pf.log: total_spawns=6 (TREAT 3, CONTROL 3),
pid_leak_check=0, znc_invocations_during_runs=2 (the two pre-run builds;
0 during runs). All 6 stderr files 0 bytes.

Transcripts (SHA-256):
- TREAT r1/r2/r3: 1067bd5e51da07e6be9412539a8e430c26465c720de54a65919b3752158e621f (3/3 byte-identical)
- CONTROL r1/r2/r3: eac3f4246bcbf84300bd5fc435675957e5bdf79ba3f20a066877c1170abd6995 (3/3 byte-identical)
- FNV arena checksums: TREAT -1094991477 x3; CONTROL -621112903 x3.

## Per-bar results (TREAT, proposal-gated)

| Bar | Result | Evidence |
|-----|--------|----------|
| CP-1 proposal-before-machinery 6/6, 0 skips | PASS | 6 PROPOSAL lines, 6 MACHINERY lines, 0 MACHINERY_SKIPPED on all 3 reps; shell line-order check: every PROPOSAL line precedes its MACHINERY line for the same (s,r) and the prop node ids match; STORE_PROP_CITE 6/6 (each MAP cites its proposal with a type-1 DEP edge) |
| CP-2 integration under proposal-first | PASS | STORE_OK 6/6 (MAPs with alive DEP edges to licensing chain facts, answers 22001+i) |
| CP-3 delayed reuse, no re-teaching | PASS | REUSE_OK 12/12 after INTERFERE |
| CP-4 conflict/correction/retention | PASS | CONFLICT_OK 1/1 (fact A superseded, fact B live); CORRECT_OK 1/1 (fact B superseded, fact C live, probe returns 27003 via serving-node check); RETENTION_OK 12/12 pre-conflict values |
| CP-5 determinism | PASS | 3/3 byte-identical stdout, equal FNV, rc=0, 0 stderr bytes, no PID/timestamps/paths |

Census note (TREAT): UNC=0 at all phases (every novel miss engaged the
trial path; no true misses, hence no miss_inquire). PROPC=6 after NOVEL,
unchanged through DELAYED. N1/Eall far below caps; no eviction.

## CONTROL (unmodified frozen core, machinery-first)

STORE_OK_C 6/6, REUSE_OK_C 12/12, RETENTION_OK_C 12/12, CONFLICT_OK_C 1/1,
CORRECT_OK_C 1/1, STORE_PROP_CITE_C 0/6 (expected: no proposal channel),
PROPC_FINAL 0, zero PROPOSAL lines in all 3 transcripts, 3/3
byte-identical. CP-6 PASS: the control reproduces the DEMONSTRATED
numbers with machinery-first ordering (no proposal precedes engagement).

## Ordering discrimination (the structural difference this lane adds)

- TREAT: for each of the 6 novel first-misses, a learner-state proposal
  node is written (PROPOSAL line), the gated machinery consults it
  (MACHINERY line naming the proposal node), and the promoted MAP cites
  it (type-1 DEP). Proposal precedes machinery 6/6 in the trace and in
  learner state.
- CONTROL: the identical 6 chains integrate with zero proposals; the
  machinery engages immediately on the miss path.

## Governance bars

K0: prereg 3bacc8903 + amendment 29a11bd85 both strict ancestors of the
implementation commit (merge-base verified in VERDICT).
K1a: 6 processes, one per 76-event run; harness log records all spawns;
pid_leak_check=0. K1b: znc_invocations_pf.log has exactly 2 entries
(pre-run builds), 0 new during runs. K1c: AUDIT_PASS on all 6 runs
(76 events each); kinds in {1,2,3}; MQUERY expected=-2, flags=1;
OBSERVE is the frozen counterexample protocol (disclosed); empty argv/env.
K2a: frozen tnn2.zag SHA-256 a29972ca... verified before builds and after
runs; nomain derivation 26b455e7... verified before builds; control core
byte-identical to the derivation (diff empty). K2b: driver audit 0/0/0
(see DRIVER.md). K2c: frozen-path delta 0/0/0; variant 48 non-comment
added lines; 0 new modes/bridges/handlers/tags/edges/opcodes/state
formats; ONE-SYSTEM RULE checked explicitly (single arena, proposal in
POLICY_ROOT space, existing formats). K2d: pure Zag; `which python3`
empty under safebin PATH.
K3: committed 2321pdt lo_driver re-run 3x read-only (recorded in
VERDICT; pending at the time this file was drafted).
