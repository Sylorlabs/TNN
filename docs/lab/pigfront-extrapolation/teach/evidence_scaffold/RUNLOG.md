# RUNLOG: TNN-on-placement scaffold-and-release (2026-09-26)

## Setup
- Workdir: ~/workspace/pigfront/scaffold/
- Deliberation binary: dialogue_bin_trace (round-3 chat infra, ~/workspace/tnnchat3/),
  copied, not rebuilt. Reads kb.txt / gaz.txt / battery.txt from CWD.
  Pure Zag, zero RNG.
- KB: 10 facts (9 measured from pigfront/teach/knowledge/knowledge.txt,
  1 honest negative fact). No layout principles taught (would smuggle the answer).
- Gazetteer: 8 pig entities, longer names first (cmp_scan order).

## Runs
- P1 run1/run2 (9-fact KB): byte-identical stdout+stderr (sha256 match).
  Turn 3 showed the predicate hole live (y-question -> x-fact).
- Added negative fact (fid 9), reran: turn 3 ->
  "TNN did not measure the pig head center y in the teaching frame."
- P1 run3/run4 (10-fact KB): byte-identical. Final battery E-lines set to
  genuine answers; final run: 5/5 PASS, byte-identical x2.
- P2 (untaught KB: 2 facts, side views only): 2 turns, byte-identical x2.

## Key observations
- Turn 1 trace proves native comparison: `TR compare e1=ear midpoint offset
  v1=2 e2=snout offset v2=25 tall=1 dmin=1` -> branch=compose.
- The machinery needed NO layout-principle training to choose the estimator;
  measured offsets + native comparison sufficed.
- Negative knowledge ("never saw the front", "did not measure y") produces
  the best epistemic behavior; absence alone triggers the predicate hole.

## Committed
docs/lab/pigfront-extrapolation/teach/evidence_scaffold/: this log, VERDICT,
kb.txt, gaz.txt, battery_p1.txt, battery_p2_untaught.txt, trace_p1.txt,
trace_p2.txt, kb_p2.txt, gaz_p2.txt. No binaries.
