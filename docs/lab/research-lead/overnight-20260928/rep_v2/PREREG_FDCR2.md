# PREREG H-FDCR2: Held-Out Inference Probes for FDCR

**Status:** FROZEN. This prereg strictly precedes implementation.
**Date:** 2026-09-29
**Author:** FDCR Held-Out Researcher (subagent)

## Background

The FDCR red team (9d03a1afb) found downgrade 1: K5-v2/K2-v2/K4-v2 probes
query TAUGHT facts. Step-0 direct lookup answers them without touching
concepts. Only mini_world's 3 "sib"-marked probes genuinely test inference.
H-INFER (4abfdf7d0) repaired the inference procedure (most-specific
preference), but the test suite still leans on confounded bars.

This prereg replaces the confounded bars with genuine held-out inference
probes. Every probe queries a (subject, relation) pair that was NEVER taught,
so Step-0 provably misses. The answer must come from sibling inference
(ans_kind=3, "sib" marker in output).

## Hypothesis H-FDCR2

FDCR's sibling inference derives correct answers for genuinely held-out
(subject, relation) pairs across five structural families: basic
bidirectional, multi-sibling consensus, conflicting-evidence withhold,
conjunctive disambiguation, and isolation withhold.

## Fixture: heldout_infer.txt (fresh vocabulary, hx_/hy_/hz_/hw_/hu_)

No vocabulary overlaps any existing fixture (verified by grep).

### Family H1: basic bidirectional sibling inference

```
T h1a | hx_alpha | ax1
T h1a | hx_beta  | bx1
T h1a | hx_gamma | gx1
T h1b | hx_alpha | ax1
T h1b | hx_beta  | bx1
T h1b | hx_delta | dx1
PHASE
Q HELD1 h1a | hx_delta | dx1
Q HELD1 h1b | hx_gamma | gx1
```

Shared features {hx_alpha=ax1, hx_beta=bx1} recruit a parent concept with
members {h1a, h1b}. h1a was never taught hx_delta; h1b was (dx1). h1b was
never taught hx_gamma; h1a was (gx1).

Predicted: both answer via sibling inference (sib marker).

### Family H2: multi-sibling consensus

```
T h2a | hy_low  | lx1
T h2a | hy_mid  | mx1
T h2b | hy_low  | lx1
T h2b | hy_mid  | mx1
T h2b | hy_high | hx1
T h2c | hy_low  | lx1
T h2c | hy_mid  | mx1
T h2c | hy_high | hx1
PHASE
Q HELD2 h2a | hy_high | hx1
```

h2a never taught hy_high. Siblings h2b and h2c agree on hx1.

Predicted: answers hx1 via sibling inference (sib marker).

### Family H3: conflicting siblings withhold

```
T h3a | hz_red   | rx1
T h3a | hz_blue  | bx1
T h3b | hz_red   | rx1
T h3b | hz_blue  | bx1
T h3b | hz_green | gx1
T h3c | hz_red   | rx1
T h3c | hz_blue  | bx1
T h3c | hz_green | gx2
PHASE
Q HELD3 h3a | hz_green | WITHHOLD
```

h3a never taught hz_green. Siblings h3b (gx1) and h3c (gx2) conflict.

Predicted: WITHHOLD (most-specific candidate has conflicting evidence).

### Family H4: conjunctive disambiguation (fresh-vocab disambig)

```
T h4a | hw_col | redx
T h4a | hw_shp | rndx
T h4a | hw_knd | rollx
T h4b | hw_col | redx
T h4b | hw_shp | sqrx
T h4b | hw_knd | blkx
T h4c | hw_col | blux
T h4c | hw_shp | rndx
T h4c | hw_knd | blkx
T h4d | hw_col | blux
T h4d | hw_shp | sqrx
T h4d | hw_knd | blkx
T h4e | hw_col | redx
T h4e | hw_shp | rndx
PHASE
Q HELD4 h4e | hw_knd | rollx
```

h4e taught redx+rndx but kind HELD OUT. Only the conjunction
redx AND rndx identifies roller (h4a); each dimension alone is ambiguous.

Predicted: answers rollx via sibling inference (sib marker).

### Family H5: isolation withhold (no sibling evidence)

```
T h5a | hu_x | xx1
T h5a | hu_y | yy1
PHASE
Q HELD5 h5a | hu_z | WITHHOLD
```

h5a has unique features; no concept contains a sibling with hu_z evidence.

Predicted: WITHHOLD.

## Kill bars (frozen)

- K-H1 (genuine held-out, 6/6): Every probe in heldout_infer.txt is
  answered correctly AND carries the "sib" marker (ans_kind=3), except the
  two WITHHOLD probes which must WITHHOLD. The sib marker proves Step-0
  direct lookup and Step-1 concept-direct did not answer; only sibling
  inference did. For WITHHOLD probes, the absence of an answer plus
  fixture analysis (conflicting/isolated evidence) proves non-triviality.
- K-H2 (Step-0 miss verified): A mechanical check (grep on the fixture)
  confirms no T line teaches the queried (subject, relation) pair for any
  held-out probe. This is documented in the result, not assumed.
- K-H3 (ablation): A modified learner copy with the sibling-inference
  block disabled (compiled in /tmp, not committed) is run on
  heldout_infer.txt. All 4 answer-probes must FAIL to produce the correct
  answer (WITHHOLD or wrong), proving sibling inference is causally
  necessary. The 2 WITHHOLD probes must still WITHHOLD (no hallucination
  introduced).
- K-H4 (determinism): Three consecutive runs of heldout_infer.txt produce
  byte-identical stdout (cmp-verified).

## What kills H-FDCR2

- Any answer-probe lacks the sib marker (answered by Step-0/Step-1, i.e.,
  the probe is confounded like K5/K2/K4): K-H1 FAIL, H-FDCR2 KILLED.
- Any probe answers incorrectly: K-H1 FAIL, H-FDCR2 KILLED.
- Ablation still answers correctly (inference not necessary): K-H3 FAIL,
  H-FDCR2 KILLED (or the probe is confounded).
- Non-deterministic output: K-H4 FAIL, H-FDCR2 KILLED.

## Scope

Bounded to FDCR's sibling-inference procedure. Does not address MERGE
incompleteness (downgrade 2) or spurious SPLITs (downgrade 3). Does not
claim L3. Success upgrades the inference evidence from 3 probes to 9
(3 mini_world + 6 held-out); the confounded K5/K2/K4 bars remain
documented as confounded, not repaired by this work.

## Prereg commit ordering

This file is committed before any fixture or result. The fixture
(heldout_infer.txt) and result (RESULT_FDCR2.md) come in later commits.
