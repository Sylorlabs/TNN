# JUDGE_BRIEF.md -- BATTERY-E3 lane wave-20261001-2321pdt

## Provenance header

- RENDER_SHA: (to be filled by the renderer; source documents are
  committed at the hashes below)
- FIRST_RENDERED_WAVE: wave-20261001-2321pdt
- COMPONENT_LINEAGE: BATTERY Part 2 1/6 PASS on frozen TNN-2
  (post-freeze sealed adversarial battery); BATTERY-CLUSTER
  analysis clustering the failures into two shared architectural
  causes with eight discriminating hypotheses, E3 prioritized as
  the blind composition probe with the oracle withheld (the
  riskiest experiment: a FAIL reframes every construction claim).
- NEW_KNOWLEDGE_CLAIM: With the oracle withheld, the frozen TNN-2
  trial still assembles and executes composition graphs blind but
  selects among multiple executable chains by oracle verification
  only, emitting the first-executable chain otherwise: E3B blind
  0/2 with the exact predicted spurious outputs, so every PF
  construction observation is BFS enumeration plus oracle
  selection, not selective construction.

## Verdict

E3-ORACLE-DEPENDENT. H1d (oracle-verified traversal, not
construction) is SUPPORTED in refined form; it is not killed.
The frozen decision rule's SIGNATURE-ORACLE-DEPENDENT matched on
every pre-registered element: E3B blind = 0/2 with outputs
exactly [80971, 80972] as predicted from frozen-source analysis,
E3B oracle-present = 2/2 (validity gate), E3A blind bar probes =
2/2 (calibration: blind assembly intact), byte-identical
transcripts across 3 fresh-state runs per condition, and
white-box inspector evidence that the blind outputs were
constructed (runtime-assembled GUARD/SETREG graphs with ET_DEP
provenance to taught facts, promoted as MAP nodes, executed to
produce the answers).

## What this does and does not establish

Establishes: on fresh sealed worlds, the trial's correct
composition outputs depend on the QUERY-carried oracle value for
candidate selection. Assembly and execution of composition graphs
do not need the oracle; selecting the right chain among several
does. The PF-A2 2/2 is re-described as enumeration plus oracle
selection. All construction claims in the wave whose evidence
came from unmasked QUERY runs must be re-examined blind.

Does not establish: broad generality, L3, or progress toward L3.
Criterion 0 not met. No repair proposed (no-patch-treadmill
rule). Report as mechanism-targeted evidence only.

## Commits (local only, never pushed; branch tnn-native-lab)

- a17a276c8: PREREG E3 frozen (design only) + NAMECHECK.
- ce46b327a: E3 implementation: worldgen, sealed worlds and
  oracles, MANIFEST_E3, blind driver (cognition region
  byte-identical to frozen), scorer, inspector, audit. No runs.
- (runs commit): 12 sealed runs (3 fresh-state runs x blind E3A,
  blind E3B, oracle-present E3A, oracle-present E3B), E3_RUN.md,
  JUDGE_BRIEF.md.

## Evidence paths

- docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E3/PREREG_E3.md
- docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E3/E3_RUN.md
- docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E3/MANIFEST_E3
- docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E3/e3_runs/
  (12 transcripts + 12 state bins)
