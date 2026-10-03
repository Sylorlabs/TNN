# VERDICT: COMP lane, wave-20261002-0521pdt

Prereg: PREREG_COMP.md frozen alone at cc9acf48e (Amendment A1
pre-implementation). Evidence: SEALED_EVAL.md, REDTEAM_SELF.md,
committed run logs and binaries in this lane dir. Commits local only.

## Verdict line: BUILD-PASS

The battery was built and run per the frozen prereg: five binaries
from frozen sources (3x byte-identical builds), sealed 12/13-test
suites, 3x byte-identical runs for B/C/C0/D. Findings include two
confounds (B-ABL control, trial-path attribution) and one
incompleteness (A), all reported as evidence, none patched over.

## Per-family verdicts

- D (satisfy, one general operation): BUILD-PASS. 12/12 tests, every
  pass mechanism-attributed (SAT-SEGS/SAT-FIX markers). KB2 holds on
  all three axes, KB3 holds (COMP5, NOSUP: genuine strict extension
  over C on isolating tests), KB4 holds (no compose flag/stage/mode;
  C0 control behaves), KB5 holds (299 cognition lines, zero new
  modes/bridges/handlers/semantic cases/opcodes, LINK14 pre-existing).
- C (constraint DFS): BUILD-PASS as a mechanism (10/12), but strictly
  dominated by D on every isolating test; its PART/ADVA/SINGLE
  passes are trial-path artifacts. Keep as bounded L2 baseline.
- B (co-use type-15): PARTIAL. Canonical COMP2 works via co-use
  staging, but the B-ABL causality control is BUILD-FAIL (confounded
  by the trial path), and its PART/D3H passes are trial artifacts.
  This battery cannot certify B's composition as history-caused.
- A (contract/plen chaining): INCOMPLETE, not scored. bin_a stalled
  70+ min in D4's goal query (O(MAPs^2 x paths^2) exhaustive search
  vs 40 distractors); KB1 unverifiable, results unadoptable this
  wave. Completed: COMP2/D2/D3H PASS, COMP3/COMP5 FAIL.
- C0 (compose_on=0): control PASS (ans=-2), KB4b holds.

## KB7 collapse decision: COLLAPSE-SUPPORTED (with caveats)

No completed test exists where any mechanism passes and D fails;
D covers every genuine win of A/B/C and strictly extends C where
C is structurally incapable (5-segment COMP5, unsupervised NOSUP).
Caveats: KB1 unverifiable for A; KB6 B-ABL comparison BUILD-FAIL;
the ADV-A exhaustive-grounding axis is untested (A incomplete);
D's subsumption was engineered toward the thesis (A1), so this is
a verified construction, not a discovered identity. Per the owner
ruling, this does NOT mean integrating engines: it means D's
`satisfy` (goal-part satisfaction; composition when one structure
is not enough; no COMPOSE_MODE) is the single operation that
covers the others' genuine wins.

## Criterion 0

No mechanism meets all four clauses (C0-C fails for all: no
independent-adversary family; C0-D unmeasured). No L3 claimed.
A is L2 structural-reuse; B/C/D are L2 structural composition.
D is the strongest L2 candidate.

## Keep / discard / queued

- Keep: D's satisfy as the working single composition operation
  for continuing-learner work (it needs no mode flag and handles
  1..n structures uniformly). Keep A/B/C sources and binaries as
  frozen experimental baselines; do not integrate them.
- Discard: nothing this wave (A's numbers are unadopted, not
  discarded; B's causality claim is unsupported, not refuted).
- Queued: (1) complete A's battery or build a targeted
  exhaustive-grounding breaker for the ADV-A axis; (2) a
  composition battery with the trial path removed or goals beyond
  its reach, plus mandatory stage-attribution markers, to end the
  attribution confound; (3) an independent-adversary sealed family
  (C0-C) before any L3-adjacent claim; (4) revision/reuse of
  composites under memory pressure in one continuing learner.
