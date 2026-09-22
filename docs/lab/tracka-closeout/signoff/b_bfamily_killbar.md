# Sign-off resolution (b) — B-family ≥2x-on-M3 kill-bar wording: arithmetic test

**Date:** 2026-09-22. **Status:** analysis complete; bar applied literally (did NOT fire — B family survives); any rewording AWAITS Micah's signature (nothing applied).
**Frozen source:** `units/PREREG_FREEZE.md` §3 (signed 2026-09-21), B-row kill criterion.
**Question:** is the B-family kill bar arithmetically reachable, and if not, what are the candidate rewordings and their computed outcomes?

## 1. Frozen rule (verbatim, §3 B-row)

> "A size retires when another B size strictly dominates it on M1/M2/M3 both corpora. **B as a family is killed as contender the moment any smart arm beats the best B size by ≥2x on M3 at equal-or-better M1.**"

## 2. Committed numbers

**Best B size** (B-family verdict, `docs/lab/units/arms/B-8/VERDICT.md`, commit `59fb89777f3f`, §5 — evidence table, field-by-field JSON comparison):

| Size | M1 prose (rec/bnd) | M1 code (rec/bnd) | M2 ETC | M3 surv / fresh / freeze | M5 B/B, audit/KB | M8 | Scorecard |
|---|---|---|---|---|---|---|---|
| B-8 | 100.0/100.0 | 100.0/100.0 | 1 | 100.0 / 67.6 / FROZEN-UNDER-PRESSURE → **cell 0** | 6.065 FAIL / 128.189 FAIL | PASS | `tracka-closeout/scorecards/B-8/run__battery_r1__scorecard_r1_1x.json` |
| B-16 | 100.0/100.0 | 100.0/100.0 | 1 | **100.0** / 100.0 / CLEAR | 3.626 FAIL / 64.189 FAIL | PASS | `tracka-closeout/scorecards/B-16/scorecard_r1_1x.json` |
| B-64 | 100.0/100.0 | 100.0/100.0 | 1 | **100.0** / 100.0 / CLEAR | 1.719 FAIL / 16.189 FAIL | PASS | `units/arms/harness/.work/battery_final/scorecard_r1_1x.json` (via B-family verdict §2–§3) |

B-8 is retired as a size (M3 cell 0 — frozen under pressure). **Best surviving B size: B-16 and B-64 tied at M3 = 100.0 (CLEAR), M1 = 100.0/100.0 both corpora** — the scale ceiling on both.

**Smart-arm sweep** (all committed scorecards in `tracka-closeout/scorecards/`, primary JSON per arm per `_manifest.json`): the highest M3 among all arms is **100.0** (A, E, H1, L2, R2, S, X, Y1, Y3, Y4, Y5, Y6, Z1, Z2, Z7 — all 100.0/CLEAR; B-family verdict independently found the same ceiling set). No arm anywhere exceeds 100.0. Y5's 1x M3 = 100.0/CLEAR (its 10x M3 = 0 scored, FROZEN-UNDER-PRESSURE — a separate leg, not the 1x comparison the bar governs).

## 3. The arithmetic

The bar requires a smart arm with:

    M3_smart ≥ 2 × M3_bestB = 2 × 100.0 = 200.0,  at M1_smart ≥ M1_bestB (= 100.0/100.0)

- M3 is a **survival rate**, codomain [0, 100.0] by the frozen §5 definition ("survival rate", bars "≥ 90%", "champion ≥ 95%"). 200.0 is outside the codomain.
- **Maximum arithmetically achievable ratio: 100.0 / 100.0 = 1.00× < 2.00× required.**
- The M1 clause is satisfiable (Y5 and others sit at M1 100.0/100.0 = "equal"); the ratio clause is the sole blocker. (Side note: U at M1-boundary 99.9 would fail the M1 clause — moot.)
- A "2× the loss rate" construction does not rescue it: with B's loss at 0.0 the ratio 0/0 is undefined, and the frozen wording says "beats … by ≥2x **on M3**" — the M3 value, i.e. the survival rate.

**Verdict, applying the frozen bar literally: the family-kill bar does NOT fire. The B family SURVIVES as a contender (B-16, B-64).** This matches the committed B-family verdict (commit `59fb89777f3f`, §5), which applied the prereg literally and raised the same flag. No amendment was needed for that verdict to stand.

**Structural observation (from the B-family verdict, confirmed here):** as written, the bar can only fire *after* a B size first drops below 50.0 on M3 — i.e. it tests B's collapse, not any smart arm's margin over a healthy B. Whether the "2x" was meant against a non-ceiling baseline (churn cost, M5) is the sign-off question.

## 4. Candidate rewordings (NOT applied — for Micah's choice)

### Option B1 — absolute-point margin on M3

> "B as a family is killed as contender the moment any smart arm beats the best B size by **≥ 10 absolute points on M3** (survival rate) at equal-or-better M1-content and equal-or-better M1-boundary, both corpora."

**Computed outcome on committed evidence:** best B M3 = 100.0; max smart M3 = 100.0; margin = 0.0 < 10 → **bar does NOT fire; B family still survives.** Honest consequence: with the whole field at the ceiling, no margin-based bar fires either — B1, like the frozen bar, only fires when B itself drops (a B-collapse detector with a 10-point trip instead of a 2× trip). Reachable in principle: fires iff some B size's M3 falls ≥ 10 points below a smart arm's.

### Option B2 — cost-axis 2× (the B-family verdict's suggested direction)

> "B as a family is killed as contender the moment any smart arm **matches-or-beats the best B size on M3** (≥ best-B M3, freeze CLEAR) at equal-or-better M1 (content and boundary, both corpora) **AND beats the best B size by ≥ 2× on M5 per-byte memory cost** (lower is better, frozen §5 formula)."

**Computed outcome on committed evidence:** best B = B-64 (M3 100.0/CLEAR, M5 1.719 B/B).
- Y5: M3 100.0/CLEAR ✓ match, M1 100/100 ✓ equal, M5 1.498 → cost ratio 1.719/1.498 = **1.147× < 2×** → does NOT fire.
- L1: M5 0.839 → 1.719/0.839 = 2.05× ≥ 2× on cost ✓, but M3 = 0 (FROZEN-UNDER-PRESSURE) fails the M3-match condition → does NOT fire.
- No other arm is within 2× on cost at matched M3/M1 → **bar does NOT fire today; B family still survives.** Reachable in principle: fires iff an arm holds M3 ≥ 100.0/CLEAR at M1 ≥ B's with M5 ≤ 0.86 B/B (half of B-64's 1.719).

## 5. What Micah must sign (exact sentence — pick one)

> Dated amendment 2026-09-22 to `PREREG_FREEZE.md` §3 (B-family kill criterion): the frozen "≥2x on M3" family-kill wording is SUPERSEDED by [Option B1 / Option B2 — quote chosen text verbatim]. The superseded wording is retained in history, not edited. Prior verdicts (B-8 retired as size; B-16/B-64 survive; family not killed — commit `59fb89777f3f`) stand unchanged; the new wording governs future evaluations only. — Signed: Micah, 2026-09-22.

Alternatively he may sign: "The frozen ≥2x-on-M3 wording stands as written (a B-collapse detector); no amendment." — also a valid sign-off.

Per §13, any rewording needs the dated amendment + his re-approval. **I have applied no rewording** — the frozen wording and the literal verdict (family survives) stand until he signs.

## Evidence refs

- B-family verdict: `docs/lab/units/arms/B-8/VERDICT.md` (commit `59fb89777f3f`), §§2–5, 8.
- Scorecards: `docs/lab/tracka-closeout/scorecards/{B-8,B-16}/…` (+ manifest `_manifest.json`); B-64 via the B-family verdict evidence table.
- Frozen rule: `docs/lab/units/PREREG_FREEZE.md` §3 (B-row), §5 (M3 definition).
