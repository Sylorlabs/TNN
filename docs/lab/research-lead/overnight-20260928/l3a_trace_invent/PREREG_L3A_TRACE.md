# PREREG: L3A-TRACE (trace-invention builder)

Status: FROZEN. Committed alone before any implementation.
Date: 2026-09-30. Owner path: docs/lab/research-lead/overnight-20260928/l3a_trace_invent/

## 1. Mission

Build and test a mechanism where the learner invents a new executable operator from
its own execution traces, with the operator's semantics stored in learner state, not
in researcher source. Structural difference vs prior art: the invented operator's
semantics is a STORED EXECUTION TRACE (a sequence of base-VM instructions the learner
itself executed and recorded). A pre-existing generic trace interpreter executes the
stored trace. No new opcode semantics are written by the researcher for the invented
operator. The source-audit question "where are the semantics of the invented operator
implemented?" must be answerable as "in learner state (stored trace bytes), executed
by the pre-existing generic trace interpreter."

Prior art (all downgraded or bounded at C0-A): H-PROCLANG1 (COND was argmin of a
researcher-enumerated menu, L2+), REPEXPAND-1 (COUPLED production existed in
researcher code, L2+), OP-RECRUIT v2 (BUILD-PASS 67a2c7e42; recruited opcodes 32..63
with one generic dispatch branch; bounded L2). This attempt differs: (i) invention
operates on dynamic execution traces the learner recorded, not on static program
bytes; (ii) reification uses a runtime name table plus pure indirection, adding zero
new dispatch branches for the invented operator; (iii) the interpreter that executes
the invented operator is the pre-existing base-VM main loop, frozen before invention.

## 2. Base VM (frozen pre-existing machinery)

Stack VM over i32. Op encoding (op:i32, arg:i32), frozen:

0=PUSH k, 1=IN0, 2=IN1, 3=ADD, 4=SUB, 5=MUL, 6=DIV (0 when divisor is 0),
7=NEG, 8=DUP, 9=DROP, 10=SWAP, 11=OVER,
12=LT, 13=EQ, 14=GT, 15=JZ a, 16=JNZ a, 17=JMP a,
18=TCALL n (generic trace call by runtime name id).

`vm_run` is the generic trace interpreter: a single loop executing any (op,arg)
sequence with an operand stack, program inputs in0/in1, and a step cap of 10000.
Op 18 TCALL n does exactly four things: (1) bounds-check n against the learner
state's n_reified count; (2) look up (offset,length) in the learner state's name
table; (3) recursively invoke vm_run on those stored bytes with the same in0/in1
and the shared operand stack; (4) count the inner steps against the same step cap.
The TCALL branch contains no arithmetic, no stack manipulation, and no per-operator
semantics. It is pure indirection: generic execution machinery, frozen before any
invention, usable for any trace bytes the learner ever stores.

## 3. Learner state (persistent)

- trace_heap: flat []u8 holding reified (op,arg) pair bytes.
- Name table: per entry (offset into trace_heap, length in instructions, arity,
  produced count). Capacity 4 entries. n_reified count.
- Recorded traces: per training task (max 4), per episode (max 8), a trace record
  of executed steps, each step (op, arg, depth_before, depth_after). Cap 256 steps
  per episode trace.
- All invention outputs live here. Nothing about any invented operator is a source
  constant.

## 4. Invention protocol (frozen)

R1 RECORD. After a task is solved exactly by phase-1 search, the learner executes
the solution on every training episode with tracing enabled and appends each
executed step to that episode's trace record in learner state. The trace is a
record of what the learner actually executed, including per-step stack depths.

R2 DETECT. Over all recorded episode traces, find the longest contiguous (op,arg)
segment satisfying every condition: (i) length >= 2 instructions; (ii) occurs in
episode traces of at least 2 distinct solved tasks; (iii) occurs in EVERY episode
trace of each task it is credited to (execution-consistency: the learner executed
it on every episode, not just one); (iv) abstract stack arity in 0..2 and produced
>= 1, where arity is computed by generic abstract stack simulation (simulate from
symbolic depth, arity = deepest relative consumption). Deterministic selection:
longest length wins; tie-break by crediting-task count descending, then by
lexicographic ascending order of the (op,arg) sequence. At most one reification
per battery run (the first found under this total order).

R3 REIFY. Assign the next runtime name_id from the learner state's counter
(0-based; never a source constant). Copy the segment's (op,arg) pairs into
trace_heap; record table meta. Emit REIFIED with name_id, length, arity,
produced, and the (op,arg) sequence. The source contains no semantic case for
this name_id.

R4 REUSE. Phase-2 search is phase-1 beam search with TCALL 0..n_reified-1 added to
the expansion universe as opaque ops. The search learns what they do only by
executing candidate programs through the generic interpreter. No other change.

## 5. Search config (frozen)

Phase-1 and phase-2 share: beam width 120, max_len 8, deterministic beam search.
Expansion order (fixed): PUSH k for k in -4..4; IN0; IN1; ADD; SUB; MUL; DIV;
NEG; DUP; DROP; SWAP; OVER. Phase-2 additionally expands TCALL n for
n in 0..n_reified-1 after the base ops. Candidate ranking: exact-match count
descending, then total absolute error ascending, then program length ascending,
then lexicographic ascending on the (op,arg) sequence. Beam dedup by exact
(op,arg) sequence equality. No RNG anywhere.

## 6. Task battery (frozen)

- T0 (train): y = x^2 + x, x in 0..6 (7 episodes).
- T1 (train): y = x^2 + 3, x in 0..6 (7 episodes).
- T2 (held-out): y = 3*x^2, x in 0..6 (7 episodes). The learner never sees T2
  before the reuse/ablation tests.

Design intent (not a bar): phase-1 finds 5-instruction solutions containing the
executed segment [IN0, DUP, MUL] (op sequence 1,8,5); detection reifies it as a
0-arity 1-produced operator ("square the input"); phase-2 solves T2 in 5
instructions using TCALL.

## 7. Frozen test bars

Bar (a) T-INVENT. After training on T0 and T1: n_reified >= 1; the REIFIED report
shows a runtime-assigned name_id; the stored trace bytes equal the detected
segment; the segment satisfies R2 conditions as printed by the detector.

Bar (b) T-PERSIST. Export the learner state (byte copy of trace_heap and name
table into fresh arrays, simulating a fresh session that only receives the
bytes). Execute probe programs [TCALL name_id] from the copy on x in -3..6.
PASS iff 10/10 probes equal x^2.

Bar (c) T-REUSE. Phase-2 search with invention enabled and the frozen budget
(beam 120, max_len 8) on held-out T2. PASS iff the search returns an exact
(7/7) solution AND the solution contains TCALL of the reified name_id.

Bar (d) T-ABLATE. Phase-2 search with invention disabled (TCALL expansions
removed; identical beam 120, max_len 8) on held-out T2. PASS iff the search does
NOT reach exact (score < 7). The advantage must be destroyed by disabling
invention.

Bar (e) T-SWAP plus T-AUDIT. T-SWAP (behavioral C0-A): on the exported state
copy, overwrite name 0's stored bytes with [IN0, DUP, ADD] (op sequence 1,8,3);
probes [TCALL 0] on x in -3..6 must equal 2*x on 10/10 probes; then restore the
original bytes and confirm x^2 returns. PASS iff behavior followed the stored
bytes both ways. T-AUDIT (static C0-A): the worker executes the frozen audit
procedure in section 8 and all checks pass.

## 8. Frozen C0-A source-audit procedure

The adversary (worker or independent) runs these steps against the committed
source file l3a_trace.zag:

A1. Enumerate opcode dispatch branches: run `grep -n "op==" l3a_trace.zag`.
Every branch must be keyed on a constant in 0..18 matching the frozen op table
in section 2. No branch may be keyed on a runtime name_id or on any constant
outside 0..18.

A2. Read the op==18 (TCALL) branch in full. Confirm its body contains only:
bounds-check of n against n_reified, name-table offset/length lookup, a
recursive call to vm_run (the same generic interpreter), and step accounting.
Confirm it contains no stack push/pop, no arithmetic, no comparison, and no
conditional keyed on any invented operator identity.

A3. Confirm no other code path executes learner-state bytes: run
`grep -n "trace_heap" l3a_trace.zag` and `grep -n "nt_off\|nt_len" l3a_trace.zag`.
Only vm_run's TCALL branch may pass those bytes to vm_run. State export/import
helpers may copy them but must never execute them (confirm by reading).

A4. Confirm the reified name_id is a runtime counter: `grep -n "n_reified"
l3a_trace.zag` must show assignment from increment of a state counter, and no
source constant in a semantic position may equal the runtime-assigned id.

A5. Novelty vs source: read the beam_search expansion section and confirm every
expansion appends exactly one (op,arg); confirm no multi-op template or op-array
literal exists in source (`grep -n "prog_append" l3a_trace.zag` shows only
single-op appends inside the expansion loop and program-construction helpers;
no array literal of op sequences). The detected segment therefore cannot be a
researcher-authored unit.

A6. Zero Python: `grep -rni "python" l3a_trace.zag` returns empty; the owned
path contains only .zag, .md, .sh, .log files.

A7. Cross-check the battery stdout: it contains REIFIED with the runtime name_id
and a STATE-DUMP whose bytes match the detector's reported segment.

Audit PASS iff A1..A7 all hold as written.

## 9. Determinism and purity

Pure Zag, zero Python at every step. No RNG. Fixed iteration orders and total
tie-breaks throughout. The battery binary is run 3 times; stdout must be
byte-identical across runs (sha256sum). No em dashes or en dashes in source or
docs (shell-only check_no_dash.sh).

## 10. Kill bars

K1. The prereg commit strictly precedes the implementation commit, verified with
`git merge-base --is-ancestor <prereg-commit> <impl-commit>`.

K2. All five test bars (a) through (e) pass exactly as frozen in section 7.

K3. Pure Zag with zero Python, 3/3 byte-identical runs, and no em/en dash bytes
(shell-only snippet).

## 11. Verdict labels and non-claims

BUILD-PASS iff K1, K2, K3 all hold. BUILD-FAIL otherwise. This is a builder
report, not a SURVIVES claim: only the full 11-step pipeline may yield SURVIVES.
Independent red team (T-ADV) is PENDING and out of scope for this build. LLM
baseline PENDING; human baseline NOT MEASURED, per standing rules. No L3 or
Criterion-0 claim is made here: at most this evidences C0-A (runtime-defined
semantics) in a bounded setting; C0-B (open structural form), C0-C (multiple
unforeseen forms), and C0-D (cognitive reuse beyond the held-out task) are not
tested and partial C0 evidence is not L3.
