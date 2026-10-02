# Prereg reference note: L3A-TRACE clean rebuild

Date: 2026-09-30. This is a process-correctness rebuild, not a redesign.
No new prereg is written because the design is already frozen; this note
records which frozen material governs the rebuild.

## Frozen design (all committed before any implementation, original or rebuilt)

- Prereg 05898699e: L3A-TRACE trace-invention builder (FROZEN; committed
  alone before implementation). Defines: base VM ops 0-18 with
  18=TCALL as generic indirection; learner state (trace_heap, name
  table capacity 4, recorded traces 4 tasks x 8 episodes x 256 steps);
  invention protocol R1-R4 (record, detect longest contiguous (op,arg)
  segment in every episode of 2+ tasks with arity 0..2 and produced>=1,
  reify under runtime-assigned name id, reuse via TCALL); beam search
  config; task battery; frozen bars (a)-(e); C0-A audit A1-A7;
  determinism and purity; kill bars K1/K2/K3.
- Amendment A1 444617dd4 (pre-implementation): held-out T2 changed from
  3x^2 to x^4+3x^2+1 (later superseded by A2 for the T2 instance).
- Amendment A2 439dd54c5 (pre-implementation): beam 600; T0=y=x^2;
  T1=y=2x^2; T2=y=x^4+2x^2+x+1; SEGMENT-MATCH guard [1,1,5].

Effective frozen configuration for this rebuild:
T0: y=x^2, T1: y=2x^2, T2 (held-out): y=x^4+2x^2+x+1, x in 0..6,
7 episodes; beam_w=600, max_len=8; expansion order PUSH k (k in -4..4),
IN0, IN1, ADD..GT (ops 3..14), then TCALL n for n in 0..n_reified-1
in phase 2; ranking exact desc, total abs error asc, length asc,
lexicographic asc; dedup by exact (op,arg) equality; intended invention
[(IN0,0),(IN0,0),(MUL,0)] = [1,1,5].

## Why the original build failed

The original implementation (a6fbee865) achieved the technical bars
but the builder disclosed authoring a python3 heredoc on a /tmp scratch
copy during diagnostics. The standing rule is literal: authoring Python
scratch code anywhere in the wave is a K4 violation even if never
executed; disclosure does not cure use. Verdict: L3A-TRACE-BUILD-FAIL
(process). The committed technical artifacts were pure Zag and stand as
exploratory data only.

## This rebuild

- Reference implementation a6fbee865 (l3a_trace.zag, 890 lines) was read
  to understand the frozen design. The implementation in this directory
  (l3a_trace_clean.zag) is written independently from the prereg: own
  code organization, own helper names, own buffer/offset conventions.
  It is not a byte copy of the reference.
- K1 for this rebuild: prereg 05898699e and amendments 444617dd4 and
  439dd54c5 all strictly precede the implementation commit of this
  rebuild (verified with git merge-base --is-ancestor before the final
  report).
- Kill bars for this rebuild: K1 zero python3 invoked for any purpose
  in this wave (affirmatively stated in the final report); K2 all five
  bars reproduced 3/3 byte-identical with exit 0 and empty stderr;
  K3 C0-A A1-A7 PASS on the new implementation file; contaminated paper
  untouched.
- Verdict label: L3A-TRACE-CLEAN-[BUILD-PASS/BUILD-FAIL].
