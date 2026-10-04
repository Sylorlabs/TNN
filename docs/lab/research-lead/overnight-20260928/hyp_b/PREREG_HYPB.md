# PREREG: Hypothesis B (Semantic Fragment Induction) Implementation

Date: 2026-09-30.
Status: FROZEN PREREGISTRATION. No implementation is authorized by this document.
Authority: freezes hypothesis B of `arch_review/ARCHITECTURE_REVIEW.md` (18be93c3e)
  under the battery protocol `discovery_battery/PREREG_BATTERY.md` (425f7276d).
Scope: T0 through T5. T6 is sealed by the independent adversary after freeze;
  this worker implements and tests T0-T5 only.

## 0. Commit order

This prereg commit strictly precedes the first hyp_b implementation commit.
Verified by `git merge-base --is-ancestor` before any result is accepted.
The battery prereg 425f7276d is an ancestor of this commit (verified).

## 1. Mechanism design (frozen)

B has three parts. There is no population of candidate programs, no scalar
score, no ranking, no width, no retention by score anywhere in any part.

### 1a. Base constructor: expression enumeration with observational equivalence

Grammar (frozen):
- leaves: IN0, IN1, PUSH c for c in {-1,0,1,2,3}
- unary: NEG
- binary: ADD, SUB, MUL, DIV, MOD, EQ, LT, GT

Enumeration: sizes 1..8 ascending. Within a size, deterministic order:
leaves in the fixed order above, then unary (operand behaviors in first-seen
order), then binary ops in the fixed order ADD,SUB,MUL,DIV,MOD,EQ,LT,GT with
operand behavior pairs in first-seen order.

Observational equivalence: behavior = output vector on the task train
episodes, hashed with 64-bit FNV-1a. The first (shortest, then first-seen)
expression per behavior is kept; all others are discarded. A new distinct
behavior counts as one candidate evaluation for budget purposes.

Behavior is computed compositionally (pointwise vector ops), never by
executing partial programs. DIV/MOD replicate the frozen VM edge semantics
(divisor zero yields 0; MOD is mod_nonneg).

Accept: the first behavior exactly equal to the target on all train
episodes. The winning expression is compiled to a stack program in postfix
order and verified exact on the frozen VM before it is reported.

Seed: none. There is no random choice anywhere. Determinism follows from
the fixed enumeration order.

### 1b. Routing (frozen, generic)

Kink analysis: for single-input tasks, sort train episodes by x; kink at
interior x_j iff (t_j - t_{j-1}) != (t_{j+1} - t_j). Kink set K_T.

- R1: single-input, K_T non-empty, library holds an input-agnostic fragment
  with kink set subset of K_T -> composition first. On success, done.
  On failure, fall through to assembly, then bounded base (sizes 1..5).
- R2: single-input, K_T non-empty, no such fragment -> conditional assembly.
  On success, done. On failure, bounded base (sizes 1..5), then FAIL.
- R3: otherwise (K_T empty or two-input) -> expression base, sizes 1..8.

Rationale: kinked targets are the designated work of the assembler and the
composer; routing them there first tests B's actual claim (retrieval-driven
composition). Straight-line re-derivation of kinked targets is the control
question, answered by the fresh-state reruns.

### 1c. Conditional assembler

Probe family (frozen): [DUP, PUSH k, CMP] for k in [0,1,-1,2,-2,3,-3,4,-4],
CMP in [LT, GT, EQ], in that fixed order. A probe is a stack transform:
push x, run probe, top is 0 or 1.

For each probe: partition train episodes by probe output. Skip the probe if
any partition has fewer than 2 episodes. Per region, synthesize a body by
expression enumeration over leaves {TOP, PUSH c for c in -1..3}, unary
{NEG}, binary {ADD,SUB,MUL,DIV,MOD}, sizes 1..4, where TOP denotes the
value already on the stack (compiles to the empty program). Body behavior
is computed with TOP = x.

If every region yields a body, assemble the main program
  [IN0, DUP, PUSH k, CMP, JZ else_pc, Q1, JMP end_pc, else: Q0, end:]
with absolute addresses computed from the part lengths (then-branch is the
probe-output-1 region). Verify exact on the frozen VM.

### 1d. Inducer

Induction rule (frozen): induce a fragment iff the task solution came from
the conditional assembler OR the expression solution contains a MOD op.
Rationale: smooth affine maps are cheaply re-derived by the base; MOD folds
and conditionals are the expensive discoveries worth keeping.

Extraction (this is the substructure extraction step; F2 guard):
- Conditional solution M = [IN0, REST]: check REST contains no IN0/IN1
  (input-agnostic). Fragment body = REST. Generality check: for s in
  -12..12, push s, run body on the frozen VM, require exact target(s).
- Expression solution with MOD: fragment body = the compiled program.
  Generality check: run as a main program on s in -12..12 (in0=s, in1=0),
  require exact target(s).

Signature: output vector on the probe set S = {-4..4} (S x S grid for
two-input fragments), executed on the frozen VM.

Behavioral dedup (F3 guard): the signature must differ from every stored
fragment signature; otherwise log DEDUP-SKIP and do not promote.

Promotion: assign the next fragment id, append the body to the library,
log the INDUCE event with the signature, the extraction steps, and the
generality result.

### 1e. Composer

Retrieval (frozen): for each library fragment in id order, log a
RETRIEVE-DECISION. A fragment is retrieved iff it is input-agnostic
(body contains no IN0/IN1), single-input, and its kink set is a subset
of the task kink set K_T. Both matches and non-matches are logged with
reasons (retrieval precision is auditable; F1 guard).

Composition for each retrieved fragment f (id order), P1 fixed to [IN0]
(fragments are single-input folds of the task input):
- 1-CALL: P2 ranges over stack programs over SEG13 =
  {PUSH-1, PUSH0, PUSH1, PUSH2, PUSH3, IN0, IN1, ADD, SUB, MUL, NEG,
   DUP, DROP} (fixed order), lengths 0..3. Candidate [IN0, CALL f, P2].
- 2-CALL: P2 lengths 0..3, P3 lengths 0..2 over SEG13.
  Candidate [IN0, CALL f, P2, CALL f, P3].
Each candidate is executed on the full train episode set on the frozen VM
(one candidate evaluation). The first exact candidate wins.

On success the trace logs one RETRIEVE event per CALL site, each recording
the fragment id and the kink-subset behavioral match that justified it.

### 1f. Library persistence

The library (fragment id, body, signature, kink set, input-agnostic flag)
persists across tasks in the fixed order T0..T5. Per-task reports include
the library diff. Transfer pairs (metric 12): for T4 and T5, report
evaluations-to-SOLVE with carried state and with fresh (empty library)
state. Fresh reruns follow routing R2.

## 2. Frozen predictions (from the review)

T0 2x+1: SOLVE via base. T1 abs: SOLVE via assembly; ABS induced.
T2 mod3: SOLVE via base; periodic fold fragment induced.
T3 parity: SOLVE via base; parity fragment induced.
T4 nested abs: SOLVE via composition, >=2 CALLs to ABS, >=2 retrieval events.
T5 fragment composition: SOLVE via composition, >=2 CALLs to ABS.

## 3. Kill bars

- K1: B implemented as specified (base + inducer + composer); the committed
  source contains no population, no score, no ranking, no beam.
- K2: T0-T5 executed under the frozen battery protocol with all 12 metrics
  per task committed alongside raw logs.
- K3: predictions evaluated per the frozen confirmation rule; the trace
  shows the mandatory events (T1 induction with signature and substructure,
  T2 induction, T4/T5 >=2 retrieval events and >=2 CALLs to one fragment).
- K4: pure Zag (no Python anywhere), no em/en-dash bytes, 3/3 byte-identical
  runs, per-task budget (1M evaluations or 300s) respected.

## 4. Falsifier watch (frozen from the battery prereg)

B-F1: T4/T5 solved without retrieval events, or retrieval precision at
chance -> composition claim falsified.
B-F2: fragments are whole-task solutions with no extraction step -> B
collapses to GENEXEC2 P2. Guard: the extraction pipeline (factor, check,
generality, dedup) is logged per induction.
B-F3: near-duplicate fragments accumulate -> semantic indexing falsified.
Guard: behavioral dedup enforced and logged.

## 5. Governance

Pure Zag for implementation, harness, and analysis. No Python anywhere.
No threshold weakening after results. This document contains no em dashes
(byte-verified before commit). Builder reports BUILD-PASS or BUILD-FAIL
against K1-K4; battery confirmation is evaluated separately.
