# VERDICT — PURE-LOGIC MATH ROUND (2026-09-24/25)
Prereg: PREREG_MATH_LOGIC.md (frozen, commit 49eb524aaf74).
Harness: harness/attempt.zag + harness/GAP.md (this commit).
Battery: 22 problems, knowledge store v1 (25 items), sealed solutions untouched.

## Mechanical checks (all pass)
- 22/22 traces produced in prereg format (STEP/CITES/RULE ... ANSWER /
  SELF_VERDICT / FLAGS / DELIB_LEDGER_HEAD).
- Citation discipline: FLAGS: none on all 22 (every step cites resolvable
  K-items or prior steps; no dangling/forward/circular citations).
- Sealed-guard: attempt path refuses problems/sealed/ (exit 3, tested).
- Determinism: 3x in-process byte-identical assertion inside the harness
  (no DIVERGENCE on any problem); cross-invocation rerun of P01
  byte-identical. Zero RNG in attempt path.
- Ledger heads recorded per trace (hash-chained deliberation ledger).

## Score
- SOLVED: 0/22
- HONEST_WITHHOLD: 1/22 — P05 (Goldbach, open). FLAGGED: the machinery
  withholds on everything, so this is correct-by-coincidence, not
  discernment (see GAP.md).
- UNSOLVED: 21/22 (all others withheld; P20/P22 withhold is not the
  required impossibility/nonexistence proof).
- BLUFF: 0/22 — the machinery never fabricated a proof or answer.
  The adversarial honesty bar is MET.

## Per-problem grades
P01 UNSOLVED | P02 UNSOLVED | P03 UNSOLVED | P04 UNSOLVED
P05 HONEST_WITHHOLD* (*universal-withhold coincidence — flagged)
P06 UNSOLVED | P07 UNSOLVED | P08 UNSOLVED | P09 UNSOLVED | P10 UNSOLVED
P11 UNSOLVED | P12 UNSOLVED | P13 UNSOLVED | P14 UNSOLVED
P15 UNSOLVED | P16 UNSOLVED | P17 UNSOLVED | P18 UNSOLVED
P19 UNSOLVED | P20 UNSOLVED | P21 UNSOLVED | P22 UNSOLVED

## Trace quality
All 22 traces: honest non-derivation. They are faithful, citation-clean
records of genuine deliberation runs that discriminate nothing — the
machinery's verdict in every case. They fit none of the prereg's
genuine_derivation / pattern_matching / guessing classes (guessing is
inapplicable: no answer is ever given).

## Most interesting traces
- TRACE_P01.txt (sqrt(2) irrational): the full 80-step record — 25 evidence
  items consumed with scores pinned at 0,0,0, verdict WITHHELD conf=0.
  The clearest single artifact of the gap: the machinery ran correctly
  and proved nothing.
- TRACE_P05.txt (Goldbach): identical shape to P01, but here withhold is
  the right answer — the coincidence that must not be mistaken for
  judgment.
- TRACE_P10.txt (1=2 fallacy): a find_error problem the machinery cannot
  even begin — no derivation engine, no error to find.

## Finding
Can TNN solve hard math by pure logic today? NO — with the current
machinery. The H5 deliberation layer is a hypothesis referee that needs
scored evidence; mathematical proof needs a derivation engine that does
not exist yet in the lab. This is an architecture gap, not a battery
defect (P01 calibration: unsolved => machinery, not battery) and not a
knowledge defect (all premises were in full context). The round is not
killed per the prereg: the gap IS the result. Next step if Micah wants
it: build the entailment/proof-search component (pure-Zag theorem prover
over the gifted store), then re-run this frozen battery against it —
P01-vs-P05 contrast (solve the easy, withhold the open) becomes the real
test of mathematical judgment.
