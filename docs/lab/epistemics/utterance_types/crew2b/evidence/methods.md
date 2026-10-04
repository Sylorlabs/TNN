# Methods: candidate mechanism tests

All candidates were implemented as a `mode:i32` parameter threaded through
`predict()` / `learn_exemplar()` / `score_set()` in a scratch copy of the
learner (`h7_modes.zag`, built with the pinned toolchain). No type constants,
no keyword lists, no marker-byte conditions — the mode only changes how the
firing set is adjudicated:

- **Mode 0 (baseline):** any firing live marker of a committed concept →
  WITHHOLD. Output byte-identical to the committed primary learner
  (SHA256 `71731400c1758f883c8057ad3dca044f34491c9a7861e6f53c1c5815b8f75407`).
- **Mode 1 (frame-gate):** WITHHOLD requires ≥1 firing marker from a
  non-content field (frame/spk) for the winning concept. (Debate R2's
  "discourse state as deciding evidence", implemented uniformly.)
- **Mode 2 (count ≥2):** WITHHOLD requires ≥2 firing markers for the winner.
- **Mode 3 (lone-content veto):** a lone single content-field firing marker is
  insufficient for WITHHOLD; anything else fires normally.

Each mode ran the full frozen curriculum once (deterministic; mode 0
additionally verified byte-identical across 3 reruns). Scratch binaries and
`.zagd` artifacts were not committed.

A fourth candidate — repaired support/conflict learning (reinforce matching
markers on correct predictions, then adjudicate on support/precision) — was
rejected on symmetry grounds before implementation: reinforcement and conflict
both act identically on `if the` and `why did` (each fires only on its own
concept's correctly-predicted items; neither ever fires on endorse-pool or
rival-concept items), so no support/conflict statistic separates them.
