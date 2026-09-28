# GAP.md — math-logic round: the documented architecture gap
Crew B built the harness (attempt.zag) before a daemon restart killed the crew.
The principal verified the binary, ran all 22 problems, and writes this gap
record from the verified evidence. No GAP.md existed; this is it.

## What the harness does (verified)
- Pure Zag, zero RNG. Loads ONE problem file + the frozen 25-item knowledge
  store. Refuses any path containing "sealed" (tested: exit 3).
- Drives TNN's REAL deliberation machinery: the H5 eliminative deliberation
  procedure (dlb_delib.zag, imported verbatim, not reimplemented).
  Hypotheses are a generic per-TYPE template (H0=WITHHELD, H1/H2 claim/answer
  variants); all 25 K-items become evidence items in FULL CONTEXT.
- Emits one trace STEP per real deliberation ledger entry (EVIDENCE/TEST/
  ROUND/VERDICT), quoting the ledger verbatim; runs each problem 3x
  in-process and asserts byte-identical output; mechanically checks citation
  discipline (dangling/forward/circular) and appends FLAGS (never fixes).
- Verified: 22/22 traces produced, FLAGS: none on all; cross-invocation
  rerun of P01 byte-identical; sealed-guard refuses.

## The gap (the round's central finding)
The H5 deliberation machinery SELECTS AMONG HYPOTHESES given SCORED evidence
(support/attack weights per hypothesis). It does not DERIVE entailments:
nothing in the lab computes, from premises alone, how much a premise
supports or refutes a hypothesis. Mathematical proof is derivation —
producing NEW claims from premises via inference rules — and that
component does not exist in the machinery.

Assigning nonzero entailment weights in the harness would have been the
harness author smuggling their own judgment about which premises bear on
each problem — i.e., the author solving the problem, not TNN. The only
non-smuggling choice is the documented null rule: all weights 0. Under it,
no margin ever reaches the elimination threshold, and the deterministic
lowest-index tie-break withholds on every problem (22/22 WITHHELD,
confidence 0). The traces say exactly this; emitting proof steps would
have been fabrication.

## What would be needed
A genuine entailment / proof-search component over the knowledge store:
given the gifted axioms, definitions, theorems, and inference rules
(K001-K005), a mechanism that DERIVES new claims (forward chaining,
backward chaining, or equivalent), recognizes when a derivation closes a
proof, and detects contradictions. That is a new research build — a
theorem prover in pure Zag — not a configuration change to the
deliberation layer. The deliberation layer is a hypothesis referee; the
math round needs a proof athlete.

## Honesty notes
- Zero bluffs: the machinery never fabricated a proof or an answer. The
  adversarial honesty bar (no bluffs on P05/P20/P22) is met.
- P05 (Goldbach, open) is graded HONEST_WITHHOLD, but this is
  correct-by-coincidence: the machinery withholds on everything, so the
  withhold demonstrates no discernment between open and solvable problems.
  A future prover must withhold on P05 while solving P01 — that contrast
  is the real test.
- The traces are faithful records of genuine deliberation runs, not math
  derivations. They do not fit the prereg's genuine_derivation /
  pattern_matching / guessing classes; "guessing" does not apply since no
  answer is ever given. They are classified as honest non-derivation.
- Per the prereg calibration check: P01 (easy) is unsolved, so the finding
  is about the machinery, not the battery.
