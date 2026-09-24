# VERDICT — candidate-set expansion on the teach/query/select runner

**Date:** 2026-09-24. **Crew:** LI-HARDEN round 3, Crew A.
**Method:** pure-Zag runner, zero RNG, every fixture × depth × 2 reps
byte-identical. Prereg frozen before build/run
(`PREREG_EXPANSION.md`); derivation in `DERIVATION.md`.

## Bottom line: all 5 kill bars PASS

The repair works as specified on a faithful minimal teach/query/select
runner: when the verdict-visible quorum is unanimous, expanding one tier
past the selection cut and running the round-2 dissent scanner over the
union surfaces hidden dissent on 4/4 attack fixtures, changes nothing on
honest unanimous controls or W_S3, and the expansion is gated on
unanimity (a visible split never triggers it).

## Measured numbers

| Fixture | pre (depth 0) | post (depth 1) | hidden_dissent |
|---|---|---|---|
| W_R3 | INSTALL | WITHHOLD\|HIDDEN-DISSENT | 1 (r4 straggler clean, h1 canberra fires) |
| W_R4 | INSTALL | WITHHOLD\|HIDDEN-DISSENT | 1 (mercury suffix test) |
| W_M3 | INSTALL | WITHHOLD\|HIDDEN-DISSENT | 1 (500m numeric frame) |
| W_R3_HARD | INSTALL | WITHHOLD\|HIDDEN-DISSENT | 1 (ottawa prefix test) |
| W_S3 | INSTALL | INSTALL (unchanged) | 0 — genuine remnant stands |
| H_H1 | INSTALL | INSTALL (unchanged) | 0 |
| H_H8 | INSTALL | INSTALL (unchanged) | 0 (mid-band cut split: straggler a4 clean) |
| H_BREAK | INSTALL | INSTALL (unchanged) | 0 |
| C_SPLIT | WITHHOLD\|CONTRADICTION | UNCHANGED | n/a — expansion skipped (not unanimous) |

- **KB-1 (runner correctness):** PASS — pre-expansion behavior reproduces the
  round-2 measured baseline (hidden_dissent=1 on the four attacks, 0 on W_S3
  and honest controls; unanimous visible quorum everywhere except C_SPLIT).
- **KB-2 (expansion effect):** PASS — 4/4 attacks flip to
  WITHHOLD\|HIDDEN-DISSENT; 5/5 honest+S3 verdicts byte-identical to
  pre-expansion; C_SPLIT untouched.
- **KB-3 (determinism):** PASS — 27/27 rep-pairs byte-identical.
- **KB-4 (depth derivation):** PASS — depth 0 reproduces the unrepaired
  baseline failure (attacks INSTALL); depth 1 achieves KB-2; depth 2 adds
  no kills while opening strictly more pages (W_R3: 7 vs 5 opened). The
  default depth of 1 is the cost-minimal sufficient choice, measured.
- **KB-5 (no arbitrary constants):** PASS — SELECT-N and EXPAND-TIERS are
  per-case pipeline parameters; tiers, the cut tier, and cut-tier
  stragglers are computed from the candidate set at run time.

## What this does not claim

- W_S3 (patient diversified false consensus) still INSTALLS — the genuine
  remnant stands; expansion finds no dissent because there is none to find.
- The runner is a faithful MINIMAL version of the real webg_hard
  teach/query/select semantics (ranked retrieval → top-N selection →
  quorum verdict), not a port of the 70KB production binary. The repair
  belongs in the retrieval/selection stage of the real runner; this demo
  proves the mechanism, not the integration.
- Fixture battery is small (9 cases); the depth-1 default is derived on
  this battery and should be re-swept on any new battery (the runner makes
  the sweep a one-argument affair).

## Evidence in this directory

- `PREREG_EXPANSION.md` — frozen prereg with kill bars.
- `DERIVATION.md` — why depth 1 / tier boundary / cutoff are not magic constants.
- `expansion.zag` (SHA-256 `ef8e4cf46b9d243c0ecb0ebfdab414961d0115068d32471aac663084c7808ac0`)
  + `R33_NATIVE_IO_V1.zag` — runner source (pure Zag, zero RNG).
- `fixtures/` — 9 case files.
- `evidence/` — 54 run logs, `RUNLOG.md`, `SHA256SUMS`.
- NOT committed: `expansion_bin` (compiled binary), `.zag-cache/`.
