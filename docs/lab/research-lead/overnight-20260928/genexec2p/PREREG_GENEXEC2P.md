# PREREG: GENEXEC2-P Build (Polynomial VM Variant)

Status: PREREGISTRATION. Frozen before any implementation.
Date: 2026-09-30.
Parent design: Battery v2 redesign `611e8fa1f`, section 3.1 and section 3.8 item 6.
Task source: parent agent directive (GENEXEC2-P Builder).

## 1. Frozen ancestor

- Commit: `8d5f58b89` ("GENEXEC2 implementation + evidence (BUILD-FAIL)").
- File: `docs/lab/research-lead/overnight-20260928/genexec2/genexec2.zag` (807 lines).
- The variant is derived ONLY from this frozen source. No other source.

## 2. Frozen opcode sets

Op encoding is unchanged from the frozen VM:

- 0=PUSH, 1=IN0, 2=IN1, 3=ADD, 4=SUB, 5=MUL, 6=DIV, 7=MOD,
  8=NEG, 9=DUP, 10=DROP, 11=SWAP, 12=OVER,
  13=LT, 14=EQ, 15=GT, 16=JZ, 17=JNZ, 18=JMP, 19=CALL, 20=RET.

ABLATED (removed in GENEXEC2-P): {6:DIV, 7:MOD, 13:LT, 14:EQ, 15:GT}.

KEPT (frozen semantics, byte-identical dispatch code):
{0:PUSH, 1:IN0, 2:IN1, 3:ADD, 4:SUB, 5:MUL, 8:NEG, 9:DUP, 10:DROP,
 11:SWAP, 12:OVER, 16:JZ, 17:JNZ, 18:JMP, 19:CALL, 20:RET}.

Per-op rationale is frozen in the parent design sec 3.1 and is not
re-argued here.

## 3. Frozen implementation plan

The variant file `genexec2p.zag` is the frozen source with EXACTLY these
changes, nothing else:

1. Header comment documents the variant, the ablation set, and the
   frozen ancestor commit hash.
2. The five dispatch branches for opcodes 6, 7, 13, 14, 15 in `vm_run`
   are replaced with trap branches:
   emit `PVM_TRAP op=<n> <NAME>` then `break` out of the execution loop.
   The trap fires instead of executing the ablated operation.
3. New function `pvm_valid(p, pl)` returns 1 iff the program's `pl`
   opcodes contain none of {6, 7, 13, 14, 15}, else 0.
4. `main()` is replaced with the conformance suite (section 5).
   All other functions are carried over byte-identical (including
   `mod_nonneg`, `op_name`, and the P1/P2/P3 machinery, which is dead
   code in this build).

No semantic change to any kept opcode. No new opcodes. No change to
program representation, stack discipline, step bound, or CALL/RET.

## 4. Frozen conformance suite (C1-C5)

All checks run in `main()`, deterministic, no randomness, no input.

- C1 (ablation): for each op in {6,7,13,14,15}, build program
  [PUSH:1, op] and assert `pvm_valid == 0`. For each kept op,
  build a program containing it and assert `pvm_valid == 1`.
  PASS iff all 21 assertions hold.
- C2 (no regression): program [IN0, PUSH:2, MUL, PUSH:1, ADD]
  (T0 2x+1) evaluated on x in 0..8. PASS iff 9/9 exact and
  `pvm_valid == 1`.
- C3 (shortcut killed): D's program
  [IN0, PUSH:-2, IN0, MUL, MOD, NEG, NEG] on x in -8..8.
  PASS iff `pvm_valid == 0` AND exact-match count < 17
  (the MOD trap fires; the program cannot compute abs on P-VM).
- C4 (kept-op semantics): spot checks, each a tiny program with a
  known result:
  ADD [PUSH:3, PUSH:4, ADD] -> 7; SUB -> -1; MUL [PUSH:3, PUSH:4] -> 12;
  NEG [PUSH:5, NEG] -> -5; DUP [PUSH:3, DUP, ADD] -> 6;
  DROP [PUSH:3, PUSH:9, DROP] -> 3; SWAP [PUSH:3, PUSH:4, SUB] -> 1;
  OVER [PUSH:3, PUSH:4, OVER, ADD, ADD] -> 10;
  IN0/IN1 passthrough; JZ [IN0, JZ:3, PUSH:99] x=0 -> 99, x=1 -> 1;
  JNZ mirrored; JMP [JMP:2, PUSH:99, PUSH:7] -> 7;
  CALL/RET: fragment [IN0, PUSH:1, ADD, RET] called from main -> in0+1.
  PASS iff all spot checks match.
- C5 (Lemma 1 mechanical coverage): assert the executable opcode set
  is exactly the kept set: `pvm_valid` accepts every op in
  {0,1,2,3,4,5,8,9,10,11,12,16,17,18,19,20} and rejects every op in
  {6,7,13,14,15} (this subsumes C1's assertions as a set-equality
  check, reported separately). Document the audit: the five trap
  branches are the only dispatch sites for the ablated opcodes, and
  every kept arithmetic op (PUSH, IN0, IN1, ADD, SUB, MUL, NEG) is
  polynomial-preserving by construction while DUP/DROP/SWAP/OVER only
  route values and JZ/JNZ/JMP/CALL/RET are control flow. PASS iff the
  set-equality holds.

Each check emits one line `C<n> PASS=<0|1> ...`. The run ends with
`CONFORM_DONE`.

## 5. Frozen kill bars

- K1 (this prereg): this file committed alone; the commit strictly
  precedes any implementation commit (verified with
  `git merge-base --is-ancestor`).
- K2 (build): variant builds with znc, conformance suite runs, and
  C1-C5 all PASS on 3/3 byte-identical runs (md5 recorded).
- K3 (purity): pure Zag at every stage. Zero `python3` invocations
  anywhere in this task, including byte checks (use shell grep/od).
  No em/en dashes (shell byte-verified). Deterministic.

## 6. Frozen falsifiers

- F1: an ablated opcode executes with full-VM semantics on the variant
  (trap fails to fire, or C3 exact count == 17). Then the ablation is
  broken: BUILD-FAIL.
- F2: C2 fails (T0 2x+1 regresses on P-VM). Then kept-op semantics
  changed: BUILD-FAIL.
- F3: `pvm_valid` accepts a program containing an ablated opcode.
  Then the validator is broken: BUILD-FAIL.

## 7. Honest scope

This task builds the VM variant and its conformance test only. It does
not evaluate any hypothesis, does not freeze Battery v2, and makes no
discovery claim. Lemma 1 itself is a mathematical argument in the parent
design (sec 3.2); this task supplies only its mechanical coverage (C5).
The F-TRICK kill switch remains the load-bearing fence, not this build.
