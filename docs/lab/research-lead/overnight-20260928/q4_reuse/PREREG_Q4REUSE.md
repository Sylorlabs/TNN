# Q4 Reuse Redesign Prereg: Deep Shared Structure for Phase 2

Date: 2026-09-30. Author: Q4 Reuse Redesign Worker (subagent).
Parent mandate: redesign Q4 Phase 2 with deeper shared structure so reuse
demonstrates clear savings vs scratch. This prereg is committed alone
before any Zag is written.

## Background

Q4 Implementation (f889d43f9): BUILD-FAIL. KB1/KB2 pass (discovery works,
bounded L2). KB3 FAIL: reuse ratio 1.0 > 0.5.

Diagnosis (from Q4_RESULT.md): "The beam search is too strong relative to
the Phase 2 task: scratch re-derives the 2-op solution as fast as reuse
composes the 1-op solution. The shared subexpression is too shallow to
demonstrate the required 0.5x savings."

## Redesign hypothesis

A deeper shared subexpression makes re-derivation costlier while reuse
stays cheap, separating the intervention curves.

Phase 1: F-THRESH. C = majority(X1, X2, X3)
  = (X1 AND X2) OR (X2 AND X3) OR (X1 AND X3). 5 operator nodes.
  Best single observable true accuracy: 0.75. Target D: 1.00.

Phase 2: F-THRESH-XOR. C' = D1 XOR X4, where D1 is the kept Phase 1
  variable (5-op majority). Materially different from Phase 1 (XOR with
  X4 flips half the outputs) while sharing the full 5-op subexpression.
  Reuse composes XOR(D1, X4): 1 operator over the atomic D1 terminal.
  Scratch must re-derive the 6-op expression from base terminals.

Shared structure depth: 5 ops (>= 4 required by K1).

## Mechanism

Same as Q4 implementation (q4.zag): beam width 32, lambda 0.02 per op,
8 passive samples with X6 bias, 24 adaptive interventions per phase,
uncertainty sampling, keep margin +0.15, max 7 ops, growth trace.
Only the sealed families change (fam 3 = F-THRESH, fam 4 =
F-THRESH-XOR). Phase 2 protocol unchanged: library terminal for D1 on
reuse side, disabled on scratch side; metric is interventions to first
reach true accuracy >= 61/64.

Prediction: reuse reaches 0.95 in few interventions (1-op composition
over atomic D1 appears after 1 beam extend); scratch needs >= 5
interventions just to generate the 6-op expression (one op level per
extend, one extend per round), plus evidence to rank it top. Expected
ratio well under 0.5.

## Kill bars

K1: Deeper Phase 2 specified. Shared subexpression is the 5-op majority
  function (D1). Satisfied by this prereg.

K2: Reuse ratio <= 0.5 (C0-D). reuse_iv * 2 <= scratch_iv, with 24
  recorded for any side never reaching 61/64 within budget.

K3: Pure Zag at every stage. Zero Python invocations. Zero em dash bytes
  in all committed docs. 3/3 byte-identical runs.

## Falsification

F1: Phase 1 fails to keep D1 (KB1/KB2 fail on F-THRESH). Redesign FAIL;
  the deep-discovery premise is false for this beam.

F2: Reuse ratio > 0.5 despite deep shared structure. Redesign FAIL on
  the C0-D claim; discovery remains bounded L2.

F3: Treadmill guard. If the run required adding an operator, terminal,
  or dedicated case beyond the frozen {AND, OR, NOT, XOR} over
  {X1..X6, 0, 1, D1}, the run is VOID.

## Honest scope

This is the implementer's own pairing, not an adversary-selected
family. It validates that deep shared structure enables KB3 for this
architecture. Adversary-selected pairings remain future work.

Discovery on F-THRESH also tests the design's open question of whether
beam-32 suffices for a 5-op target under 24 interventions. If Phase 1
fails, that question is answered negatively.

No em dashes were used in this document.
