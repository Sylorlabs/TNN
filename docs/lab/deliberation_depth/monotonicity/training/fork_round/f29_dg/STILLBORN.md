# F29 DG (Disagreement-Geometry Head) — STILLBORN

- **Prereg:** `PREREG_FORKROUND.md` FROZEN v2, §3 (F29) + `ideas/fable_forks.md`
  FORK 2 (Mechanism B). Adjudication class per §10: **STILLBORN**
  (reported, not killed). No failure-mode number (§7 taxonomy applies to
  fork deaths, not stillborns).
- **Date:** 2026-09-24. Authority verified byte-identical to frozen commit
  `3a2eef44` (`tnn-native-lab`): local `ideas/fable_forks.md` sha256
  `c519bbb03dde5cab7ba06a450986477e5b83ab020a3d8f15f72017ac7ac6553f`
  and local `PREREG_FORKROUND.md` sha256
  `86e043d7ae0441ac1ffab1aebb0ef02c6f353c5221cb609e1db449d60263521f`
  both match the GitHub blobs at `3a2eef44`.

## Missing observable (exact)

**Per-survivor binary hypothesis output values** `h_i ∈ {0,1}`.

The frozen definition (`ideas/fable_forks.md`, Mechanism B) requires them
verbatim:

```
// Pairwise disagreement among surviving hypotheses
// Let h_i, h_j be surviving hypothesis outputs (binary: 0 or 1)
D_t = Σ_{i<j, both alive} |h_i − h_j| * 1000 / (nalive * (nalive−1) / 2)
// If nalive ≤ 1: D_t = 0
```

`D_t`, `S_t = 1000 − D_t`, and the velocity `ΔD_t = D_t − D_{t−1}` cannot be
computed as specified without a binary per-survivor value. No frozen input
provides one (inventory below). Choosing any binarization of a non-binary
field would be inventing the observable, which the stillborn gate forbids.

## Observable inventory (all four frozen inputs checked)

1. **`training/features/features.tsv`** — SHA256 verified
   `4682190cfd504cb692df122a6b054d8fad65ef860707e6a92abfdf04e65a897d`
   (matches §2). 5240 rows × 15 cols:
   `id family heldout depth t rel4 correct4 f1..f8`. The only
   survivor-aggregate fields are `f6 = nalive*1000/nh` and the `f7`
   singleton flag. **No per-survivor columns at all.**
2. **items_v2 batteries** (`admit`, `revoke`, `logic`, `trap`, `cost` under
   `deliberation_depth/items_v2/`, plus
   `monotonicity/redteam/redteam_battery.jsonl`): every hypothesis object
   in every battery carries exactly `{"id", "label"}` — no binary
   output/value field. Evidence objects carry `supports`/`attacks` weight
   maps only.
3. **ceiling items** (`training/items/ceiling_{P,O,D}_{even,odd}.jsonl`):
   same schema — hypotheses are `{"id", "label"}` only.
4. **harness DSt** (`training/src/dlb_delib.zag`, struct `DSt`):
   per-hypothesis state is `scores[]` (i64 fixed-point thousandths,
   signed) and `alive[]` (binary 0/1). There is **no per-hypothesis binary
   output field**:
   - `alive[i]` is the survivor mask itself — restricted to survivors it
     is identically 1, so `|h_i − h_j| = 0` for every pair and `D_t ≡ 0`.
     Degenerate: the head would reduce to a 3-term sum with `w_s`
     multiplying the constant 1000.
   - `scores[i]` are i64, not binary; the ideas file specifies `h binary`
     with no binarization rule, so any mapping (e.g. score sign) would be
     an invented observable.
   - A leader-indicator reading is not a field in any input and degenerates
     to `D_t = 2000/nalive`, a deterministic function of the already-frozen
     `f6` aggregate.
   - Ledger output (`dlb_d_round`) is per-round (leader id, margin, conf),
     not per-survivor. No other harness module (`probe2/3`, `bisect*`,
     `dlb_ledger`) stores per-survivor binary outputs.

## Consequence

Nothing was built, trained, or evaluated: per prereg §5 the fork is
STILLBORN (reported, not killed). The `G`-rise-reversing weight ratchet,
the head form, and the kill bars (a) B2 V2 > 0 on converged-wrong
survivors, (b) eval B3 ≥ base, (c) weight collapse were never exercised
because the mechanism's required input does not exist in the frozen
pipeline. A future revival would need a prereg amendment defining the
binary `h_i` observable (e.g. a specified, frozen binarization rule) —
that amendment is a coordinator/Micah decision, not a builder decision.
