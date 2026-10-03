# PREREG — candidate-set expansion on the teach/query/select runner (LI-HARDEN round 3, Crew A)

**Frozen:** 2026-09-24, before any build or run in this workstream.
**Status:** FROZEN — kill bars below may not be edited after the first run.
Any change after freezing requires a dated amendment note and re-run.

## 0. Background

Round 2 measured candidate-set expansion as a selection-layer repair (WALL-RED
crack 2, BEYOND rank 3): when the verdict-visible quorum is unanimous, expand
one tier past the selection cut and run the dissent scanner over the union.
Measured on probes: hidden_dissent=1 on W_R3/W_R4/W_M3/W_R3_HARD, 0 on W_S3 and
all honest controls. Round 2 left the demo on the REAL webg_hard
teach/query/select runner unbuilt (context_round3.md: "not yet built").

Finding (addendum, 2026-09-24): no webg_hard runner source exists under
`docs/lab/liharden/` on origin/tnn-native-lab — only mentions in
`tier1/ADDONS_EVAL.md` and `tier1/VERDICT_TIER1.md`. The real runner
(`knowledge/web_guides/live_ingest/variants/v-hard/webg_hard.zag`, 70KB,
teach/query/select/verdict protocol, SELECT-N from guide) exists in-repo
outside liharden/ but is not the instrument for this demo.

## 1. What is being built

A faithful MINIMAL teach/query/select/verdict runner in pure Zag
(`expansion.zag`), implementing the runner semantics the repair needs:

- **teach/query (fixture-side):** case files carry the retrieved candidate
  set: `PAGE|pid|score|claim` lines (score = the retrieval ranker's score).
- **select:** deterministic order by (score desc, pid asc); take top
  SELECT-N as the verdict-visible set. SELECT-N is a per-case pipeline
  parameter (mirrors the real runner's guide `SELECT-N`; production value 3).
- **verdict (pre-expansion):** if all visible claims are byte-equal
  (lowercased) → unanimous → `INSTALL`; else `WITHHOLD|CONTRADICTION`.
- **expansion (the repair):** if and only if the visible quorum is unanimous,
  open one more tier past the selection cut (definition §2), run the
  ported round-2 dissent scanner `hdissent()` (wallsel.zag, measured baseline)
  over every non-visible page in the union; any FIRE → `hidden_dissent=1`
  and the verdict becomes `WITHHOLD|HIDDEN-DISSENT`.

Zero RNG in any decision path. Raw bytes only, no tokenizer. Deterministic:
byte-identical output across reps.

## 2. Tier and depth definitions (derived, not hardcoded — see DERIVATION.md)

- **Tier** = one distinct retrieval-score band among the candidate set.
- **Cut tier** = the score band of the lowest-scoring visible page.
- **Expansion of depth d** = the visible set ∪ all non-visible pages in the
  cut tier (rank-tied stragglers the N-cut split off) ∪ all pages in the
  first d score bands strictly below the cut tier.
- **Depth** is a tunable per-case parameter `EXPAND-TIERS`; the DEFAULT is
  derived (DERIVATION.md): the minimum depth that reaches the nearest rival
  score band = 1. The runner accepts an argv depth override for the sweep.

## 3. Fixtures (all under fixtures/)

| Case | Shape | SELECT-N | Expected pre | Expected post (depth 1) |
|---|---|---|---|---|
| W_R3 | 3-page sydney ring @100 + agreeing straggler @100 + canberra dissenter @60 + noise @10 | 3 | INSTALL (unanimous) | WITHHOLD\|HIDDEN-DISSENT, hidden_dissent=1 |
| W_R4 | 3-page venus ring @100 + mercury dissenter @60 + noise @10 | 3 | INSTALL | WITHHOLD\|HIDDEN-DISSENT, hidden_dissent=1 |
| W_M3 | 3-page 2000m ring @100 + honest 500m dissenter @60 + noise @10 | 3 | INSTALL | WITHHOLD\|HIDDEN-DISSENT, hidden_dissent=1 |
| W_R3_HARD | 3-page toronto ring @100 + ottawa dissenter @60 + noise @10 | 3 | INSTALL | WITHHOLD\|HIDDEN-DISSENT, hidden_dissent=1 |
| W_S3 | patient consensus: 3 agree @100 + 2 agree @60 + noise @10, NO dissent anywhere | 3 | INSTALL | INSTALL (unchanged), hidden_dissent=0 |
| H_H1 | honest: 3 agree @100 + 1 agree @60 + noise @10 | 3 | INSTALL | INSTALL (unchanged), hidden_dissent=0 |
| H_H8 | honest: 4 agree @100 (mid-band cut split) + 1 agree @60 | 3 | INSTALL | INSTALL (unchanged), hidden_dissent=0 |
| H_BREAK | honest: 3 agree @100 + 1 agree @60 | 3 | INSTALL | INSTALL (unchanged), hidden_dissent=0 |
| C_SPLIT | visible split: 2 "vault is open." + 1 "the vault is not open." @100, hidden agree @60 | 3 | WITHHOLD\|CONTRADICTION | UNCHANGED (expansion gated on unanimity — must NOT trigger) |

## 4. Kill bars

- **KB-1 (runner correctness, addendum requirement):** at depth 1, pre-expansion
  verdict = INSTALL with unanimous visible quorum on W_R3/W_R4/W_M3/W_R3_HARD,
  W_S3, H_H1, H_H8, H_BREAK; the union scan finds hidden_dissent=1 exactly on
  the four attack fixtures and 0 on W_S3 + all honest controls. C_SPLIT:
  pre = WITHHOLD|CONTRADICTION, expansion skipped.
- **KB-2 (expansion effect):** post-expansion verdict =
  WITHHOLD|HIDDEN-DISSENT on 4/4 attack fixtures; verdict byte-identical to
  pre-expansion on W_S3 and all honest controls (INSTALL); C_SPLIT unchanged.
- **KB-3 (determinism):** every fixture × EXPAND-TIERS ∈ {0,1,2} × 2 reps
  byte-identical (sha256 of run logs equal per rep pair).
- **KB-4 (depth derivation):** depth 0 reproduces the round-2 baseline failure
  (attack fixtures INSTALL — the unrepaired selection bug); depth 1 achieves
  KB-2; depth 2 adds no further kills on this battery while opening strictly
  more pages (documents fetch cost). This sweep is the measured justification
  for the derived default depth of 1.
- **KB-5 (no arbitrary constants):** SELECT-N and EXPAND-TIERS are per-case
  pipeline parameters with documented derivation (DERIVATION.md); the tier
  boundary and the cut-tier-straggler rule are computed from the data. Any
  hardcoded architectural constant = FAIL this bar.

## 5. Failure handling

Any kill-bar miss → report the bar as FAILED with the measured numbers; do
not ship the repair. Negative results are reported, not hidden.

## 6. Evidence to commit

`docs/lab/liharden/round3/expansion/`: this prereg, DERIVATION.md,
expansion.zag, R33_NATIVE_IO_V1.zag, fixtures/, evidence/ (per-run logs +
SHA256SUMS + RUNLOG.md), VERDICT_EXPANSION.md. No binaries, no .zagd caches.
