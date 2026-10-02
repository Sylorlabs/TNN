# JUDGE_BRIEF.md -- Battery lane wave-20261001-2321pdt

## Provenance header

- RENDER_SHA: (to be filled by the renderer; source documents are
  committed at the hashes below)
- FIRST_RENDERED_WAVE: wave-20261001-2321pdt
- COMPONENT_LINEAGE: Battery v2 9/9 VALIDATED (wave-20261001-2021pdt);
  6 queued triviality-review corrections applied as v3 base design
  invariants (sealed per-run M2-W1 mappings, recency-proof
  distractors, representation-neutral white-box bars with tightened
  K-S11v3(d), cross-world consistency, documented K-S8 exploration
  budget, vocabulary-neutral validity); Battery v3 9/9 mechanism
  bars FAIL with predicted degenerate signatures (VALIDATED);
  post-freeze sealed adversarial battery 1/6 PASS (PF-C1 via
  direct-fact shadowing).
- NEW_KNOWLEDGE_CLAIM: The three frozen TNN-2 mechanisms fail on
  materially different post-freeze structures with exact failure
  modes (construction loses to retrieval; guides are constant and
  persistent under concurrency and partial resolution; revisions do
  not transfer across relations), corroborating the v1/v2/v3 kills
  through calibrated bars.

## Verdicts

Battery v3 (Part 1): VALIDATED. All 6 process bars PASS; all 9
mechanism bars FAIL with the predicted degenerate signatures;
retention 11/12; no-leak clean; all calibration gates pass. The
v1/v2 kills stand, corroborated on fresh instances carrying the 6
triviality-review corrections.

Post-freeze sealed adversarial battery (Part 2): 1/6 world bars
PASS. Mechanism (a) FAILS, mechanism (b) FAILS, mechanism (c)
FAILS. Exact failure modes are in POSTFREEZE_RUN.md. One battery
design caveat is recorded (PF-A2 does not discriminate BFS
reachability from selective composition); it does not change any
verdict.

## What this does and does not establish

Establishes: the three mechanisms fail on fresh, materially
different, adversarial structures through calibrated bars, with
byte-identical determinism and frozen-binary integrity. The
failures are corroborations, not new kills.

Does not establish: broad generality, L3, or progress toward L3.
Criterion 0 not met. Report as mechanism-targeted evidence only
(standing ruling: FW1-FW9 is a regression battery for TNN-2 only).

## Commits (local only, never pushed; branch tnn-native-lab)

- f7f8f5e3b: PREREG Battery v3 frozen (design only).
- a42a113aa: Battery v3 implementation, sealed worlds, validation
  runs. v3 VALIDATED.
- 59e029102: PREREG post-freeze sealed adversarial battery frozen
  (design only).
- (post-freeze implementation commit id to be recorded on commit)

## Evidence paths

- docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY/PREREG_BATTERY_V3.md
- docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY/VALIDATION_RUN_V3.md
- docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY/PREREG_POSTFREEZE.md
- docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY/POSTFREEZE_RUN.md
- v3_worlds/, v3_runs/, v3_controls_out/, pf_worlds/, pf_runs/,
  pf_controls_out/ (transcripts, manifests, inspector reports)
