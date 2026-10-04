# Depth-config format (H5 deliberation harness)

The depth config is the harness's parametric interface: **every numeric knob
of the deliberation procedure comes from this file**. No depth numbers are
hardcoded in the harness. Any conforming config works.

## Format

UTF-8 text, one `key=value` per line. `#` starts a comment (whole-line only
after trimming). Blank lines ignored. All eleven keys are **required exactly
once**; unknown keys and duplicates are fatal errors.

```
mode=adaptive
shallow_rounds=2
deep_rounds=16
adaptive_min_rounds=2
adaptive_max_rounds=16
conf_threshold=800
stability_window=2
epsilon=50
elim_margin=900
refute_threshold=600
evidence_cap=64
```

## Keys

| Key | Type | Constraint | Meaning |
|---|---|---|---|
| `mode` | enum | `shallow` \| `deep` \| `adaptive` | which stopping rule governs the run |
| `shallow_rounds` | int | ≥1 | fixed round count for `mode=shallow` |
| `deep_rounds` | int | ≥1 | fixed round count for `mode=deep` |
| `adaptive_min_rounds` | int | ≥1 | adaptive: never stop before this round |
| `adaptive_max_rounds` | int | ≥ `adaptive_min_rounds` | adaptive: hard stop at this round |
| `conf_threshold` | int | ≥0 | adaptive: stop only once `confidence >=` this (fixed-point thousandths, 1000 = full) |
| `stability_window` | int | ≥1 | adaptive: leader must be unchanged for this many consecutive rounds |
| `epsilon` | int | ≥0 | adaptive: margin gain over the stability window must be `<` this (thousandths) |
| `elim_margin` | int | ≥0 | a hypothesis trailing the leader by ≥ this (thousandths) is eliminated |
| `refute_threshold` | int | ≥0 | a consumed attack with weight ≥ this decisively refutes the tested hypothesis |
| `evidence_cap` | int | ≥0 | max evidence items consumed per item |

Integers are strict syntax: optional leading `-`, then digits only.
`conf_threshold`, `epsilon`, `elim_margin`, `refute_threshold` are fixed-point
thousandths (e.g. `800` = 0.800). Weights in item files use the same scale.

## Semantics of the three modes

- **shallow**: exactly `shallow_rounds` rounds, unless natural termination
  fires first (no evidence left and ≤1 hypothesis alive, or a round that
  changes nothing).
- **deep**: exactly `deep_rounds` rounds, same natural-termination caveat.
- **adaptive** (the standing-law mode — "deliberation adapts to state, no
  fixed think-count"): after each round ≥ `adaptive_min_rounds` (and ≥
  `stability_window`), stop iff all hold: `confidence >= conf_threshold`,
  the leader is unchanged over the last `stability_window` rounds, and
  `margin[round] - margin[round - stability_window] < epsilon`.
  Hard stop at `adaptive_max_rounds`; natural termination also applies.
  The rule is a pure function of observable deliberation state — zero RNG.

## Coordination with Crew 1 (DEPTH_DEF.md)

Crew 1's frozen depth-definition spec had not landed when this harness was
built (2026-09-23). This format implements the brief's three named levels
(SHALLOW fixed-small / DEEP fixed-large / ADAPTIVE state-driven) with the
brief's suggested parameter slots (rounds, evidence caps, epsilon/k, hard
cap) exposed as named keys. If the frozen `DEPTH_DEF.md` renames keys or
fixes different parameter values, only a rename/value shim is needed — the
deliberation procedure itself is already fully config-driven.
