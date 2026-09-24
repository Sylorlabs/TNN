# PREREG DRAFT — H-PAM-36 (commit-then-sample)

**Status:** DRAFT (not frozen). **Parent:** Round-C `HYPOTHESES_ROUND_C.md` §8.
**Origin:** grok-4.7 direction 2. Escape (i) without a human in the loop.

## Claim

Fixture commits a percept hash. The harness then draws a sample **s** from a
channel whose inputs are disjoint from the fixture's writable set. Admit iff the
opened percept entails s. s is published after the commit and replayed from the
transcript.

## Why this is none of the banned things

- Not PoW: no grinding, no cost asymmetry claim.
- Not a secret: s is published; replay re-derives it from the transcript.
- Not a content geometry: no (conf, measure) gate.
- Not act-to-check: s is not recomputed from the percept; the percept had to
  commit before s existed.

## Cheap probe (preregistered, not yet run)

Toy commit/entail/sample harness. Fixture classes:

- **Frozen:** pre-materialized (commit, open) pairs; sample drawn post-commit.
- **RC (deciding arm):** fixture reads s from the transcript, then opens a
  percept inside s's preimage. The entailment check must leave the false
  preimage empty — this is exactly the discrimination the Separation Lemma
  prices.
- **WG on the sample channel:** author-writable inputs influencing the sample
  draw.

## Kill bars

- (a) Frozen fixtures: false admits > 0 = **KILL**.
- (b) RC fixtures: false admits > 0 = **KILL**.
- **(c) WG: any author-writable influence on the sample channel = KILL,
  recorded as loss of independence, not patched with a story.** If no sample
  channel the author truly does not influence can be built, this hypothesis is
  **H-PAM-33 under a new name** and must not be run.
- (d) Honest: honest admits ≥ 95%.

## Determinism

Pure Zag, zero randomness, 3× byte-identical stdout. The sample draw lands in
the transcript after the commitment (replay-safe).

## Amendment policy

Frozen by Micah's signature. The independence of the sample channel is the
entire claim; any amendment weakening (c) voids the hypothesis.
