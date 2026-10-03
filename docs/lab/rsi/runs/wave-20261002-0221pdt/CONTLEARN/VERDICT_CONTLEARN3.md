# VERDICT_CONTLEARN3: mechanism-proposal-first continuing learner

Wave: wave-20261002-0221pdt. Lane: CONTLEARN. Date: 2026-10-02.
Frozen prereg: PREREG_CONTLEARN3.md (commit 3bacc8903), transparently
amended by PREREG_CONTLEARN3_AMEND1.md (commit 29a11bd85; pre-
implementation; the STORE_OK / STORE_PROP_CITE split, no tuple, script,
or decision-rule change). Implementation commit e1ca9aa93; merge-base
ancestry of both prereg commits verified (K0).

## Per-bar results

| Bar | Result | Evidence |
|-----|--------|----------|
| CP-1 proposal-before-machinery 6/6, 0 skips | PASS | 6 PROPOSAL / 6 MACHINERY / 0 MACHINERY_SKIPPED lines on all 3 TREAT reps; shell line-order check: each PROPOSAL precedes its MACHINERY line for the same (s,r) with matching prop node ids; STORE_PROP_CITE 6/6 (every MAP cites its proposal with a type-1 DEP edge) |
| CP-2 integration under proposal-first | PASS | STORE_OK 6/6 (MAPs with alive DEP edges to licensing chain facts, answers 22001+i) |
| CP-3 delayed reuse, no re-teaching | PASS | REUSE_OK 12/12 after INTERFERE |
| CP-4 conflict/correction/retention | PASS | CONFLICT_OK 1/1 (fact A superseded, fact B live); CORRECT_OK 1/1 (fact B superseded, fact C live, probe returns 27003 with serving-node check); RETENTION_OK 12/12 pre-conflict values |
| CP-5 determinism | PASS | 3/3 byte-identical stdout per binary (TREAT 1067bd5e..., CONTROL eac3f424...); FNV equal across reps; rc=0; 0 stderr bytes; no PID/timestamps/paths |
| CP-6 control reproduces DEMONSTRATED, machinery-first | PASS | STORE_OK_C 6/6; REUSE_OK_C 12/12; RETENTION_OK_C 12/12; CONFLICT_OK_C 1/1; CORRECT_OK_C 1/1; zero PROPOSAL lines on CONTROL |
| K0 commit order | PASS | Prereg 3bacc8903 and amendment 29a11bd85 both strict ancestors of implementation e1ca9aa93 |
| K1a one learner, no reset | PASS | 6 processes (2 binaries x 3 reps), one per 76-event run; pid_leak_check=0 |
| K1b builds logged | PASS | znc_invocations_pf.log: exactly 2 entries (pre-run builds), 0 new during runs |
| K1c audit, no task labels | PASS | AUDIT_PASS 76/76 on all 6 runs; kinds in {1,2,3}; MQUERY expected=-2, flags=1; OBSERVE is the frozen counterexample protocol; empty argv/env |
| K2a frozen ISA boundary | PASS | tnn2.zag SHA-256 a29972ca... before builds and after runs; nomain derivation 26b455e7... verified before builds; control core diff-empty vs derivation |
| K2b driver audit | PASS | 0 cognition functions; 0 structural writes; 0 new tags/edges/opcodes/modes/bridges; 0 switch/match |
| K2c source delta | PASS | Frozen path 0/0/0; variant instrument 48 non-comment added lines, 2 removed; 0 new modes/bridges/handlers/tags/edges/opcodes/state formats; ONE-SYSTEM RULE checked explicitly (single arena, proposal as tag-1 node in POLICY_ROOT space, existing formats) |
| K2d pure Zag | PASS | Zero Python/C/JS/Rust; `which python3` empty under safebin PATH (NAMECHECK.md Step 0) |
| K3 no regression | PASS | Committed 2321pdt lo_driver 3x in TREAT mode (stdin "TREAT"); stdout SHA-256 1ff527fa... on all 3 reps; rc=0; 0 stderr bytes |

K3 note: lo_driver reads its run mode from /dev/stdin; with the harness's
inherited stdin it blocks on anon_pipe_read, with </dev/null it prints
MODE_FAIL. The correct invocation is `printf 'TREAT' | ...`. Recorded in
RUN_LOG.md as a lesson.

## Verdict

**PROPOSAL-FIRST-DEMONSTRATED.** All frozen bars pass. On the fixed
disclosed 76-event battery, with the trial/promotion machinery gated on
a learner-state proposal channel, the continuing learner integrates 6/6
novel 2-hop chains (MAPs with DEP citations to the licensing facts and
to the licensing proposals), reuses 12/12 values after an interference
gap, retains 12/12 pre-conflict values across a conflict plus correction
episode (corrected fact live, predecessors superseded), and the trace
shows proposal-before-machinery ordering 6/6, all 3/3 byte-identical, in
one process with no reset, no task label, and no recompilation.

## Claim bound (binding)

Per the frozen prereg section 1 and the red-team self-review, the
proposal CONTENT (mech=TRY_CHAIN) is a fixed researcher template; the
experiment does NOT claim learner authorship of proposal content, learner
scheduling of proposal initiation (still event-triggered), or learner
agency in the causal sense. The gate's refusal branch is structurally
enforced but empirically unexercised (0 MACHINERY_SKIPPED). No L3, no
generality. The variant is a measurement instrument, not a proposed
architecture. Citation form stays machinery-enabled per the debate Q7
binding form: "LEARNOWN-DEMONSTRATED (machinery-enabled scope; strong
sense measured absent, CONTLEARN-OWNED/OWNED2)".

What this lane does establish: a proposal-first control-plane ordering
can be structurally enforced (learner state read as CONTROL at the
machinery entry) while preserving integration, reuse, conflict handling,
correction, and delayed reuse in one continuing learner. It is a step on
the LEARNER-MECH control-parameter axis, not a closure of the mechanism
gap.

## Build status

**BUILD-PASS.**

## Follow-ups for the coordinator

- The queued instruction ("no further machinery-disabled replications")
  was honored: this lane built the new proposal-gate instrument instead.
- Candidate next: an adversarial exercise of the gate's refusal branch
  (delete a proposal mid-run, attempt engagement) to empirically verify
  the structural enforcement; and a learner-scheduled initiation design
  (LEARNER-MECH axis (a)), which this lane explicitly did not test.
- K3 lesson: future workers re-running lo_driver must feed "TREAT" on
  stdin (RUN_LOG.md).
