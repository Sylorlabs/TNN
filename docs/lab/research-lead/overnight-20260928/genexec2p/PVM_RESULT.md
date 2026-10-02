# GENEXEC2-P Build Result

Status: BUILD-PASS.
Prereg: `PREREG_GENEXEC2P.md` (commit `495878df4`), strictly before implementation.
Parent design: Battery v2 redesign `611e8fa1f`, sec 3.1 and sec 3.8 item 6.

## What was built

`genexec2p.zag` (910 lines): the frozen GENEXEC2 interpreter
(`genexec2.zag` at commit `8d5f58b89`, 807 lines, md5-verified extract)
with exactly three change classes, nothing else:

1. Header comment documents the variant, ablation set, and ancestor.
2. Dispatch branches for opcodes 6=DIV, 7=MOD, 13=LT, 14=EQ, 15=GT
   replaced with trap branches: emit `PVM_TRAP op=<n> <NAME>`, break.
3. New `pvm_valid(p, pl)`: 1 iff no ablated opcode present, else 0.
4. `main()` replaced with the frozen conformance suite (C1-C5).

Diff audit (non-main region): the only differences from the frozen
source are the header, the five trap branches, and the added
`pvm_valid`. Every kept opcode (0,1,2,3,4,5,8,9,10,11,12,16,17,18,19,20)
has byte-identical dispatch code and frozen semantics.

## Conformance results (3/3 byte-identical, md5 a7577086acbf8440ccda91124044d0a5)

- C1 PASS=1: all 5 ablated opcodes rejected by `pvm_valid`; all 16 kept
  opcodes accepted (21/21 assertions).
- C2 PASS=1: T0 2x+1 `[IN0 PUSH:2 MUL PUSH:1 ADD]` runs on P-VM,
  valid=1, exact=9/9. No kept-op regression.
- C3 PASS=1: D's MOD program `[IN0 PUSH:-2 IN0 MUL MOD NEG NEG]` has
  valid=0 and exact=1/17 on x in -8..8. The MOD trap fired once per
  episode (17 PVM_TRAP lines). The shortcut is killed on P-VM.
- C4 PASS=1: 17 kept-op spot checks match (ADD, SUB, MUL, NEG, DUP,
  DROP, SWAP, OVER, IN0, IN1, PUSH, JZ taken/not-taken, JNZ
  taken/not-taken, JMP, CALL/RET with a promoted fragment).
- C5 PASS=1: executable opcode set equals the kept set exactly
  (opcodes 0..20 classified; 16 kept accepted, 5 ablated rejected).
  Lemma 1 mechanical coverage: the dispatch audit shows the five trap
  branches are the only sites for ablated opcodes; kept arithmetic ops
  (PUSH, IN0, IN1, ADD, SUB, MUL, NEG) are polynomial-preserving by
  construction; DUP/DROP/SWAP/OVER only route values; JZ/JNZ/JMP/CALL/RET
  are control flow. The induction argument itself is in the parent
  design sec 3.2.

CONFORM_PASS=1. Exit code 0. Zero stderr bytes on all three runs.

## Kill bars

- K1 PASS: prereg commit `495878df4` strictly precedes this
  implementation (verify: `git merge-base --is-ancestor`).
- K2 PASS: builds with znc, C1-C5 all PASS, 3/3 byte-identical.
- K3 PASS: pure Zag at every stage. Zero `python3` invocations anywhere
  in this task (byte checks via shell grep). No em/en dashes, no
  non-ASCII bytes (shell-verified). Deterministic.

## Falsifiers

- F1: silent. No ablated opcode executed with full-VM semantics.
- F2: silent. T0 2x+1 exact on P-VM.
- F3: silent. `pvm_valid` rejected every ablated-opcode program.

## Honest scope

This is a VM build variant plus its conformance test. It evaluates no
hypothesis, freezes no battery, and claims no discovery. It unblocks
the Battery v2 checklist item "Build GENEXEC2-P with its conformance
test; commit and hash-record." Downstream v2 evaluation harnesses must
run P-VM tasks through this interpreter and pre-validate programs with
`pvm_valid` (F-SMUG audit).

Builder label: BUILD-PASS.
