# Sign-off resolution (c) — M5-as-binding amendment: impact analysis

**Date:** 2026-09-22. **Status:** analysis complete; the amendment is DRAFT ONLY — **not in force, nothing killed by this document**.
**Frozen source:** `units/PREREG_FREEZE.md` §5, M-22–M-26, M-57, §13 (signed 2026-09-21).
**Question:** if M5 cost became a binding kill bar via amendment, which arms would die?

## 1. Frozen status (verbatim)

- §5 M5 bars: "**per-byte memory ≤ 1.5× source bytes; ≤ 10 audit entries per KB learned.** Lower is better (↓)."
- M5 is a **scorecard metric with bars, NOT a kill bar** — no arm dies on M5 today (e.g. the B-family verdict records all three B sizes' M5 FAILs as "recorded, not adjudicated").
- **M-57 is an unresolved disjunction:** "M5 entry-count bars AND R4 byte bars — approve 'both-must-hold' or a unified bar". It was signed "as proposed" without selecting which. Any binding amendment must resolve this too.

## 2. Method and evidence grades

Primary source: committed scorecards in `tracka-closeout/scorecards/` (47 JSONs, 33 arms; `_manifest.json`; first-listed JSON per arm = the committed scorecard), cross-checked against the B-family verdict (commit `59fb89777f3f`) for B-64.

- **Grade A** — committed `metrics-v1` bar cells (`memory_bar_1_5x`, `audit_bar_10_per_kb`): quoted verbatim.
- **Grade B** — committed components allow mechanical evaluation: audit/KB = `ledger_entries / (source_bytes/1024)` (no RSS term in the formula); per-byte lower bound = `slot_table_bytes / source_bytes` (assumes RSSΔ ≥ 0 — every committed RSSΔ is ≥ 0; stated where used). B-64's cells come from the committed B-family verdict evidence table.
- **Grade C** — committed figure under the arm's own/provisional accounting, not the frozen §5 formula: flagged, not treated as a bar evaluation.
- **Grade D** — insufficient committed evidence to evaluate: named with what's missing.

Current verdicts per `TRACKA_VERDICT_SHEET.md` §2.

## 3. Impact table

### 3a. Bar (i): per-byte memory ≤ 1.5× source bytes, as a binding kill

| Arm | Verdict | B/B | Bar cell / basis | Grade | Would die? |
|---|---|---|---|---|---|
| A | PASS | 13.01 | FAIL | A | **YES** |
| B-8 | KILLED | 6.065 | FAIL | A | already dead |
| B-16 | PASS | 3.626 | FAIL | A | **YES** |
| B-64 | PASS | 1.719 | FAIL (B-family verdict §3) | B | **YES** |
| C-W | PASS | 16.481 | FAIL | A | **YES** |
| C-P | PASS | ≥14.25 | FAIL (slot-only lower bound) | B | **YES** |
| H1 | PASS | 2.412 | FAIL | A | **YES** |
| K2 | PASS | 2.417 | FAIL (committed pass=False) | B | **YES** |
| L1 | PASS | 0.839 | PASS | A | no |
| L2 | PASS | 4.307 | FAIL | A | **YES** |
| N | PASS | ≥2.62 | FAIL (slot-only lower bound) | B | **YES** |
| S | PASS | 1.718 | FAIL | A | **YES** |
| X | PASS | 2.002 | FAIL | A | **YES** |
| Y3 | PASS | 2.07 | FAIL | A | **YES** |
| Y4 | PROVISIONAL | 1.823 | FAIL | A | **YES** |
| Y5 | PASS (blowout) | 1.498 | PASS | A | no |
| Y6 | PASS | 3.136 | FAIL | A | **YES** |
| Z2 | PASS | 1.974 | FAIL | A | **YES** |
| Z6 | PASS | 2.437 | FAIL (provisional own accounting) | C | **YES*** |
| Z7 | PASS | 1.811 | FAIL | A | **YES** |
| E, Y1, Z4 | KILLED | 2.4–2.9 | FAIL | A | already dead |
| G2, H2, I1, I2, Z5 | KILLED | 3.05–3.9 / — | FAIL (own acct.) / uneval. | C/D | already dead |
| R2 | KILLED | 0.844 | PASS | A | already dead (passes) |
| Z1 | PROVISIONAL | — | RSSΔ null — unevaluable | D | cannot kill (no evidence) |
| F-S, F-B, K3, M | PROV/KILLED | — | partial / not-implemented / baseline-only | D | cannot kill (no evidence) |
| D, D-T, D-R, P, U, W, Z3, Z8, G1, J1, J2, K1, M2, O, Q, R, T, V | various | — | no committed M5 | D | cannot kill (no evidence) |

\* Z6's figure is provisional own-accounting; killing on it would need a compliant leg first (see draft §4).

**Bar (i) death toll: 15 PASS arms + Y4 (provisional) + Z6 (Grade C) — 17 arms. Survivors among measured PASS arms: L1 and Y5 only.** 16 of 18 Grade-A measured arms fail the 1.5× bar. Note: U has no scorecard cell here, but the M5-HARMONIZE record measured U at **2.902 B/B** under the frozen §5 formula (prose-only) — it would fail (i) if a scorecard cell existed.

### 3b. Bar (ii): ≤ 10 audit entries per KB learned, as a binding kill

| Arm | Verdict | aud/KB | Bar cell / basis | Grade | Would die? |
|---|---|---|---|---|---|
| A | PASS | 16.189 | FAIL | A | **YES** |
| B-8 | KILLED | 128.189 | FAIL | A | already dead |
| B-16 | PASS | 64.189 | FAIL | A | **YES** |
| B-64 | PASS | 16.189 | FAIL (B-family verdict §3) | B | **YES** |
| C-W | PASS | 364.066 | FAIL | A | **YES** |
| C-P | PASS | 0.189 | PASS (1001 entries / 5295.6 KB) | B | no |
| H1 | PASS | 8.326 | PASS | A | no |
| K2 | PASS | 16.19 | FAIL (committed pass=False) | B | **YES** |
| L1 | PASS | 16.001 | FAIL | A | **YES** |
| L2 | PASS | 16.19 | FAIL | A | **YES** |
| S | PASS | 16.189 | FAIL | A | **YES** |
| X | PASS | 0.188 | PASS | A | no |
| Y1 | KILLED | 16.189 | FAIL | A | already dead |
| Y3 | PASS | 16.189 | FAIL | A | **YES** |
| Y4 | PROVISIONAL | 30.258 | FAIL | A | **YES** |
| Y5 | PASS (blowout) | 5.015 | PASS | A | no |
| Y6 | PASS | 16.189 | FAIL | A | **YES** |
| Z1 | PROVISIONAL | 16.19 | FAIL (85731 / 5295.6) | B | **YES** |
| Z2 | PASS | 16.189 | FAIL | A | **YES** |
| Z4, E | KILLED | 16.189 | FAIL | A | already dead |
| G2, I2 | KILLED | 16.19 | FAIL (derived) | B | already dead |
| H2 | KILLED | 4.7 | PASS (committed) | B | already dead (passes) |
| R2 | KILLED | 2.431 | PASS | A | already dead (passes) |
| N, M, Z6, Z5 | various | — | no committed entry count | D | cannot kill (no evidence) |
| (rest as in 3a) | | | | D | cannot kill (no evidence) |

**Bar (ii) death toll: 12 PASS arms + Y4/Z1 (provisional) — 14 arms. Survivors among measured PASS arms: C-P, H1, X, Y5.**

### 3c. Headline findings for Micah

1. **The 1.5× byte bar is far tighter than the battery's reality:** 16 of 18 measured arms fail it. Making it binding kills 15 surviving arms — including B-16/B-64 (the B family the frozen §3 bar deliberately keeps alive as contender), H1, S, X, Z2, Z7. Only **L1 and Y5** survive it.
2. **The two halves of M5 disagree on L1:** L1 is the per-byte cost champion (0.839 B/B, PASS) but fails the entry bar (16.001/KB, FAIL). Under (ii), the M5 column champion dies on its own metric's other half.
3. **Y5 is the only surviving arm that passes both halves** (1.498 / 5.015). H1 and X pass (ii) but fail (i); R2 passes both but is already dead.
4. **Under "both-must-hold"** (one resolution of M-57), the joint survivors among measured PASS arms are: **Y5 alone**.
5. The bars' numeric values are not in question — only whether they bind. No arm's scorecard changes either way.

## 4. Draft amendment text (DRAFT — not in force)

> **Dated amendment 2026-09-22 to `PREREG_FREEZE.md` §5 / M-23–M-26 / M-57 (M5-as-binding).** M5 cost becomes a binding kill bar with scope **[Micah selects: (a) per-byte memory ≤ 1.5× source bytes only / (b) ≤ 10 audit entries per KB learned only / (c) both-must-hold]**. This also resolves M-57's disjunction as **[both-must-hold iff scope (c), else the selected single bar]**. The numeric bars are unchanged. **Evidence rule:** a kill fires only on Grade-A or Grade-B M5 evidence (committed `metrics-v1` bar cells, or committed components evaluating the frozen formula mechanically); Grade-C/D arms cannot be killed until a compliant M5 leg is committed. **Effect on signature:** the arms marked "Would die? YES" in `tracka-closeout/signoff/c_m5_binding.md` §§3a/3b (per the selected scope; Grade A/B rows only) are KILLED under §0 RULE-7 with no appeal; all other verdicts stand. History is not edited: the frozen text stands, this amendment appends. — Signed: Micah, 2026-09-22.

## 5. What Micah must sign (exact sentence)

> Dated amendment 2026-09-22 to `PREREG_FREEZE.md` §5/M-23–M-26/M-57: M5 cost becomes binding with scope **[select (a) byte-bar only / (b) entry-bar only / (c) both-must-hold]**; the arms listed "Would die? YES" (Grade A/B) in `tracka-closeout/signoff/c_m5_binding.md` §§3a/3b under the selected scope are KILLED per §0 RULE-7 on signature; Grade-C/D arms are unaffected pending a compliant M5 leg; the numeric bars (≤ 1.5×, ≤ 10/KB) are unchanged. — Signed: Micah, 2026-09-22.

Per §13 this needs the dated amendment + his re-approval. **Until he signs, M5 remains what the frozen prereg says it is: a scored metric with bars, not a kill bar. No arm dies on M5 today.** If he declines, the sign-off is equally complete: "M5 stays non-binding; no amendment."

## Evidence refs

- Scorecards: `docs/lab/tracka-closeout/scorecards/` (`_manifest.json`; primary JSON per arm), 47 JSONs / 33 arms.
- B-64 M5: `docs/lab/units/arms/B-8/VERDICT.md` (commit `59fb89777f3f`), §3 evidence table.
- U 2.902: M5-HARMONIZE record, `TRACKA_VERDICT_SHEET.md` §3.
- Frozen bars: `docs/lab/units/PREREG_FREEZE.md` §5, M-22–M-26, M-57, §13.
