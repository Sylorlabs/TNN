# PREREG: Q3 Runtime Operator Recruitment (OP_RECRUIT)

Date: 2026-09-30.
Status: FROZEN. Committed before any implementation, build, or run.
Lane: frontier backlog Q3 (score 30/35), launched by N1 (Frontier Launcher).

## 1. Background

GENEXEC2 (F1, BUILD-FAIL) built a generic stack VM (ops 0-20) with a
persistent fragment library callable via CALL (op 19). T1 (|x|) was
solved via P3 conditional assembly, producing FRAG0 =
[IN0 PUSH:-1 GT JZ:6 IN0 JMP:8 IN0 NEG] (len 8, 17/17).

T4 (||x|-2|) and T5 (|x|+|x-2|) remain unsolved (0/13 each) despite the
library containing ABS. Amendment A2 designed T4/T5 to require nested
CALLs to ABS, with intended solution
[IN0, CALL ABS, PUSH 2, SUB, CALL ABS]. That intended solution is
incorrect under the actual VM semantics: CALL executes the fragment on
the shared data stack with global in0/in1, so CALL ABS always pushes
|in0| rather than transforming the stack top. The fragment is not a
stack function and cannot compose as ||x|-2|. The P1 beam (width 500,
max_len 12) scored 0/13 on both tasks.

## 2. Hypothesis (Q3)

The learner needs an ALLOCATE_OP primitive that recruits a solved
program's bytes as a new first-class opcode with stack discipline. The
recruited op's semantics is the learner-created bytes stored in learner
state, executed by one generic interpreter case. The wrapper (pop
input, bind as in0, execute on fresh stack, push result) makes the
fragment a composable unary stack function. This satisfies C0-A (no
dedicated source case per recruited op; semantics in learner data).
Test C0-D: recruited ops must reduce search cost on later tasks versus
the frozen no-recruitment baseline.

## 3. Design: ALLOCATE_OP

### 3.1 VM substrate changes (researcher-provided; generic machinery only)

1. Opcode range 32..63 reserved for recruited ops (32 slots; the cap is
   generic, not task-specific).
2. Learner state additions: `rec_buf` (flat bytes, same fragment format
   as lib: len:i32 then len*8 bytes), `rec_idx` (byte offsets, 32
   entries), `nrec` (count, initially 0).
3. ONE generic VM case: `op in [32,64)`:
   - Let ri = op - 32. If ri >= nrec, treat as NOP.
   - Pop a from data stack (a = 0 if empty).
   - Execute `rec_buf[rec_idx[ri]]` as a program with in0 = a, in1 = 0,
     on a fresh data stack and fresh return stack.
   - Push the result onto the caller's data stack.
   - No per-op semantic case exists. The source never mentions ABS or
     absolute value in connection with opcode 32.
4. `recruit_op(frag:[]u8) -> i32` (learner-invoked between tasks; not a
   VM opcode):
   - Copies frag's bytes (len + instructions) into rec_buf at the next
     free offset.
   - Records the offset in rec_idx[nrec].
   - Returns 32 + nrec, then increments nrec.
   - Deterministic; no task-specific logic.

### 3.2 Why C0-A is satisfied

Question: "Where are the semantics of OP32 implemented?" Answer: "In
learner state (rec_buf entry created at runtime by recruit_op); the
source contains one generic dispatch case for opcodes 32..63 and no
case for absolute value." If the learner recruits a different fragment,
OP32 means something else. The meaning is data, not source.

### 3.3 Recruitment protocol (frozen)

1. Precondition: learner has solved T1, obtaining program P_ABS. Its
   bytes must match the GENEXEC2 T1 solution (verified against
   EVIDENCE.md before implementation; the check is a byte comparison,
   not a re-solve).
2. Learner invokes `r = recruit_op(P_ABS)`. Expect r == 32 (first
   recruitment).
3. For subsequent tasks, the learner's beam search universe is the P1
   op set plus { (32,0) } as one atomic choice (denoted OP_ABS).
4. OP_ABS behaves as a unary stack function: [.., x] -> [.., |x|].

### 3.4 Difference from CALL (frozen claim)

CALL f (op 19) executes library fragment f on the shared stack with
global in0/in1; it is not a stack function and cannot compute
|stack_top|. Recruited op R pops the stack top, binds it as in0,
executes on a fresh stack, and pushes the result; it is a composable
unary stack function. Both use generic dispatch, but the stack
discipline and the recruiting authority (learner via ALLOCATE_OP vs
researcher promotion) differ. Falsifiable mechanistic claim: the T4/T5
solutions require the pop/bind/push wrapper; CALL cannot substitute.

## 4. C0-D Test (frozen)

### 4.1 Tasks and episodes (from PREREG_GENEXEC2.md; frozen)

- T1: y = |x|, x in -8..8 (17 episodes). Precondition only.
- T4: y = ||x|-2|, x in -6..6 (13 episodes).
- T5: y = |x| + |x-2|, x in -4..8 (13 episodes).

Episode construction: x values in ascending order; ein0 = x, ein1 = 0,
etgt = y. Identical to GENEXEC2.

### 4.2 Baseline (frozen; from GENEXEC2 F1 report)

P1 beam (width 500, max_len 12, no CALL, no recruited ops) on T4: 0/13.
On T5: 0/13.

### 4.3 Treatment (frozen procedure)

1. Verify P_ABS bytes against GENEXEC2 EVIDENCE.md (byte comparison).
2. `r = recruit_op(P_ABS)`; assert r == 32.
3. Run P1R on T4: beam search, universe = P1 ops + {(32,0)}, width 500,
   max_len 12, ordering (exact desc, mae asc, len asc, prog asc).
   Record best exact-match score, best program bytes, and whether
   (32,0) appears in the best program.
4. Run P1R on T5 identically.
5. Sanity: run OP_ABS in isolation on x in -8..8; must equal |x|
   (validates the wrapper, not counted toward K3).
6. Each full run executed 3 times; require byte-identical stdout.

### 4.4 Prediction

P1R scores above 0/13 on T4 and on T5, and the best programs contain
OP32. Example T4 solution: [IN0, (32,0), PUSH 2, SUB, (32,0)] (5 ops).
This demonstrates the recruited operator reduces search cost (from
unsolvable to solvable) on later tasks: C0-D SUPPORTED.

### 4.5 Falsification (frozen)

If P1R scores 0/13 on T4 and T5 (no improvement over baseline), the Q3
recruitment hypothesis is FALSIFIED for this task family. The report
must then diagnose: (a) whether OP32 appeared in any retained beam
candidate (if never retained, the beam prunes it: search bottleneck);
(b) the best MAE reached with vs without OP32 in the universe. If the
diagnosis is (a), the conclusion is that recruitment is insufficient
without search reform (consistent with the P1 Redesign direction), not
that the C0-A mechanism is invalid.

K3 passes iff the frozen procedure was executed as specified and the
verdict (SUPPORTED or FALSIFIED with diagnosis) follows the evidence.
K3 does NOT require the prediction to hold.

## 5. Kill bars

- K1 (design): ALLOCATE_OP designed, recruitment protocol specified,
  C0-A argument and CALL-difference claim documented. Satisfied by this
  prereg.
- K2 (implementation): Pure Zag implementation of the VM extension,
  recruit_op, and P1R. Exactly one generic VM case for opcodes 32..63
  (audited: no ABS or absolute-value case in source; grep for ABS,
  STEP, DOUBLE, COUPLED, COND as semantic cases must find none).
  Zero Python at any stage including /tmp scratch. Zero em dash bytes
  in committed files (byte check). 3/3 byte-identical runs, exit 0.
- K3 (C0-D test): Frozen procedure executed; verdict follows evidence
  per 4.4/4.5.

## 6. Commit order and paths

This prereg is committed alone under
`docs/lab/research-lead/overnight-20260928/op_recruit/PREREG_OPRECRUIT.md`.
The implementation commit must be a strict descendant (verified via
`git merge-base --is-ancestor` before the result is reported). All work
under `docs/lab/research-lead/overnight-20260928/op_recruit/`. No other
paths touched.

## 7. Honest limitations (frozen)

- Recruited ops are unary (pop 1, push 1). Binary recruitment is future
  work; the restriction is generic, not task-specific.
- recruit_op is invoked by the driver between tasks (learner-level
  loop), not by VM programs at runtime. Program-invoked recruitment
  (self-extending opcode set mid-execution) is future work.
- The wrapper allocates fresh stacks per recruited-op execution; no
  performance claim is made.
- If P1R succeeds, the credit is shared: the C0-A mechanism (learner
  bytes as semantics) plus the stack-discipline wrapper. The ablation
  that isolates them (wrapper with researcher-chosen bytes) is not run
  this wave; the CALL comparison in 3.4 is the analytic substitute.
