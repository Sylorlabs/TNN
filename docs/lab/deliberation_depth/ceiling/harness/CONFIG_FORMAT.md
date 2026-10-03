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
| `mode` | enum | `shallow` \| `deep` \| `adaptive` \| `bound` (H5B) | which stopping rule governs the run |
| `shallow_rounds` | int | ≥1 | fixed round count for `mode=shallow` |
| `deep_rounds` | int | ≥1 | fixed round count for `mode=deep` |
| `adaptive_min_rounds` | int | ≥1 | adaptive: the §6 window `k` and earliest stop round — stop only once `rounds >=` this |
| `adaptive_max_rounds` | int | ≥ `adaptive_min_rounds` | adaptive/bound: hard stop at this round (recorded `cap=1`) |
| `conf_threshold` | int | ≥0 | **ignored by the §6 rule in v2** (required key, format stability; the old rule's confidence gate) |
| `stability_window` | int | ≥1 | **ignored by the §6 rule in v2** (required key, format stability; the old rule's leader-stability window) |
| `epsilon` | int | ≥0 | adaptive: every one of the last `k` per-round absolute confidence gains must be `<` this (thousandths) |
| `elim_margin` | int | ≥0 | a hypothesis trailing the leader by ≥ this (thousandths) is eliminated |
| `refute_threshold` | int | ≥0 | a consumed attack with weight ≥ this decisively refutes the tested hypothesis |
| `evidence_cap` | int | ≥0 | max evidence items consumed per item |

Integers are strict syntax: optional leading `-`, then digits only.
`conf_threshold`, `epsilon`, `elim_margin`, `refute_threshold` are fixed-point
thousandths (e.g. `800` = 0.800). Weights in item files use the same scale.

## Semantics of the four modes

- **shallow**: exactly `shallow_rounds` rounds, unless natural termination
  fires first (no evidence left and ≤1 hypothesis alive, or a round that
  changes nothing).
- **deep**: exactly `deep_rounds` rounds, same natural-termination caveat.
- **bound** (H5B only): the residual-flip bound. After each round, stop iff
  the remaining unconsumed evidence provably cannot flip the current
  leader: for leader L and each alive runner-up R, with
  maxR = S_R + (remaining supports for R) and
  minL = S_L − (remaining attacks on L), R cannot overtake L iff
  maxR < minL, or (maxR == minL and R > L) since ties break to the lowest
  hypothesis index. Vacuously true with no alive runner-up. A bound-stop
  verdict always equals the run-to-exhaustion verdict. In `bound` mode only
  `adaptive_max_rounds` (hard cap, recorded `cap=1`), `elim_margin`,
  `refute_threshold`, and `evidence_cap` are active; `shallow_rounds`,
  `deep_rounds`, `adaptive_min_rounds`, `conf_threshold`,
  `stability_window`, and `epsilon` remain required keys but are ignored
  (format stability). Natural termination also applies.
- **adaptive** (DEPTH_DEF §6 verbatim, §12 amendment): after each round,
  stop iff `rounds >= k` (where `k = adaptive_min_rounds`, the §6 window)
  and all of the last `k` per-round absolute confidence gains
  `g_i = |c_i - c_{i-1}|` (with `c_0 := c_1`, thousandths) are `< epsilon`.
  A confidence drop never counts as settled (absolute value). Earliest
  stop: round `k`. Hard stop at `adaptive_max_rounds` (recorded as
  `cap=1` in the VERDICT ledger detail); natural termination also
  applies. `conf_threshold` and `stability_window` remain required keys
  but are ignored by the §6 rule. The rule is a pure function of
  observable deliberation state — zero RNG.

## Coordination with Crew 1 (DEPTH_DEF.md)

Crew 1's frozen depth-definition spec had not landed when this harness was
built (2026-09-23). This format implements the brief's three named levels
(SHALLOW fixed-small / DEEP fixed-large / ADAPTIVE state-driven) with the
brief's suggested parameter slots (rounds, evidence caps, epsilon/k, hard
cap) exposed as named keys. If the frozen `DEPTH_DEF.md` renames keys or
fixes different parameter values, only a rename/value shim is needed — the
deliberation procedure itself is already fully config-driven.
