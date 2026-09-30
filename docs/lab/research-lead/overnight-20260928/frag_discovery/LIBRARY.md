# Fragment Library (persistence record)

Committed as the persistence record required by PREREG_FRAGDISC.md section 3d.
Library state after the main phase (tasks T0..T5 in order), from the
deterministic run (byte-identical across 3 runs; see run7.log).

## Fragment 0: ABS (from T1)

- Inducing task: T1 (|x|, x in -8..8, GENEXEC2-P)
- Extraction: assembler (mode=asm). Main was [IN0] + 33-op chain; candidate
  = REST after IN0.
- Input-agnostic: yes (no IN0/IN1 in body)
- Single-input: yes
- P-VM-valid: yes (pvm_valid = 1; F-SMUG audit passes)
- Signature on S = {-4..4}: 4,3,2,1,0,1,2,3,4
- Kink set: {0}
- Generality: TRAIN-SCOPED (finite JZ chain; fails outside -8..8, disclosed)
- Confirmation: CONFIRMED (reused by the composer on T4 and T5)
- Body (33 ops):
  DUP PUSH-1 ADD JZ33 DUP PUSH-2 ADD JZ33 DUP PUSH-3 ADD JZ33
  DUP PUSH-4 ADD JZ33 DUP PUSH-5 ADD JZ33 DUP PUSH-6 ADD JZ33
  DUP PUSH-7 ADD JZ33 DUP PUSH-8 ADD JZ33 NEG
- Semantics: if x in {1..8} keep x; else negate. Computes |x| for x in -8..8.

## Fragment 1: MOD3 (from T2)

- Inducing task: T2 (x mod 3, x in 0..16, full GENEXEC2)
- Extraction: base solution contains MOD (mode=mod)
- Input-agnostic: no (contains IN0)
- Single-input: yes
- P-VM-valid: no (uses MOD; full-VM fragment)
- Signature on S = {-4..4}: 2,0,1,2,0,1,2,0,1
- Kink set: {-3,-1,0,2,3}
- Generality: GENERAL (exact on -12..12)
- Confirmation: UNCONFIRMED (never retrieved; correctly rejected for T4/T5
  by the kink-subset gate, and for P-VM tasks by pvm_valid)
- Body (3 ops): IN0 PUSH3 MOD

## Fragment 2: PARITY (from T3)

- Inducing task: T3 ((a+b) mod 2 == 0 ? 1 : 0, a,b in 0..4, full GENEXEC2)
- Extraction: base solution contains MOD (mode=mod)
- Input-agnostic: no (contains IN0/IN1)
- Two-input: yes
- P-VM-valid: no (uses MOD; full-VM fragment)
- Signature on SxS grid: 1,0,1,0,... (81 values, alternating)
- Kink set: {} (two-input; kink analysis is single-input only)
- Generality: GENERAL (exact on -12..12 grid)
- Confirmation: UNCONFIRMED (never retrieved; correctly rejected for T4/T5
  by the single-input gate)
- Body (8 ops): PUSH-1 IN0 IN1 ADD PUSH2 MOD ADD NEG

## Retrieval audit (precision)

- T4 (kinks {-2,0,2}): fragment 0 retrieved ({0} subset of {-2,0,2});
  fragments 1,2 correctly rejected (kink-not-subset / not-single-input).
- T5 (kinks {0,2}): fragment 0 retrieved ({0} subset of {0,2});
  fragments 1,2 correctly rejected.
- T2 (kinks {2,3,5,6,8,9,11,12,14,15}): fragment 0 correctly NOT retrieved
  ({0} not a subset); routed to base fallback instead.
