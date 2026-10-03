# H5 — Legible per-item deliberation traces

**Date:** 2026-09-23. **Purpose:** show 2–3 real, row-by-row deliberation traces so the mechanism can be seen directly.

**Sources (nothing here is fabricated).** Every row below comes from the frozen sweep records in `~/workspace/scratch-h5/sweep/` (cells `d1_trap_A`, `d4_trap_A`, `d8_trap_A`, `adaptive_trap_A`, `adaptive_admit_A`, `deep16_admit_A` — run A of the A/B pair; A/B byte-identical per RESULTS_H5 §2). Item definitions (evidence weights/texts) from `~/workspace/tnn-lab/deliberation_depth/items_v2/`. Leader/margin/confidence and the refutation-test target come verbatim from each ledger's `ROUND`/`TEST` rows. Absolute scores are re-derived from the frozen evidence weights (all scores start at 0 — the harness zeroes them, `dlb_delib.zag` line 129) and cross-checked against every ledger `ROUND` margin: all agree.

**How to read these.** Each round: the harness reads one evidence item, adds its support weights / subtracts its attack weights to the live hypotheses' scores, drops any hypothesis trailing the leader by ≥ 900 (elimination bar), then tries to refute the runner-up by looking for a consumed attack on it of weight ≥ 600 (recorded as `TEST … holds` / `refuted`). **Confidence = leader score − runner-up score, clamped to 0…1000** (in thousandths; 1000 = maximum). **Per-round gain gᵢ = |confidenceᵢ − confidenceᵢ₋₁|**, with g₁ = 0. The adaptive rule (§6, DEPTH_DEF verbatim): stop when rounds ≥ 3 **and** the last 3 gains are **all < 20** thousandths (ε = 0.02). A confidence *drop* never counts as settling — gains are absolute.

---

## Trace 1 — one trap item, shallow (wrong) vs deep (right): `TRAP-C6-001`

The item is a Wason card-selection task in plain words: *"If a card shows a sensor detects motion on one side, then it shows the alarm sounds on the other."* Four cards on the table. Six candidate answers (hypotheses); the correct one is **P_and_not-Q** ("turn the P card and the not-Q card" — the only two that could break the rule). The wrong answer the bait sets up is **P_and_Q** (match what's mentioned in the rule).

Evidence, in the fixed order the harness reads it:

| id | what it says | effect on scores |
|----|---|---|
| e1 | "If a card shows a sensor detects motion on one side, then it shows the alarm sounds on the other." | +100 to P_and_Q |
| e2 | "Four cards lie on the table, one side visible each:" | +100 to P_and_Q |
| e3 | "P: a sensor detects motion" | +100 to P_and_Q |
| e4 | "not-P: it is not the case that a sensor detects motion" | +100 to P_and_Q |
| e5 | "Q: the alarm sounds" | +100 to P_and_Q |
| e6 | "not-Q: it is not the case that the alarm sounds" | +100 to P_and_Q |
| **e7** | "falsification analysis: only a P card (hidden side could be not-Q) and a not-Q card (hidden side could be P) can violate P->Q" | **+500 to P_and_not-Q, −500 to P_and_Q** |

The first six premises each push the matching answer P_and_Q +100. Only the seventh — the falsification analysis — pushes the correct answer and *penalizes* the bait.

Round-by-round (d1 | d4 | d8 are the same evidence order; each column stops where its depth cap says stop):

| round | evidence | d1: leader (score) vs runner-up (score) — conf, gain | d4: leader (score) vs runner-up (score) — conf, gain | d8: leader (score) vs runner-up (score) — conf, gain |
|---|---|---|---|---|
| 1 | e1 | **P_and_Q** (100) vs P_and_not-Q (0) — conf 100, g=0 | **P_and_Q** (100) vs P_and_not-Q (0) — conf 100, g=0 | **P_and_Q** (100) vs P_and_not-Q (0) — conf 100, g=0 |
| 2 | e2 | stopped — verdict **P_and_Q** ❌ | **P_and_Q** (200) vs P_and_not-Q (0) — conf 200, g=100 | **P_and_Q** (200) vs P_and_not-Q (0) — conf 200, g=100 |
| 3 | e3 | | **P_and_Q** (300) vs P_and_not-Q (0) — conf 300, g=100 | **P_and_Q** (300) vs P_and_not-Q (0) — conf 300, g=100 |
| 4 | e4 | | **P_and_Q** (400) vs P_and_not-Q (0) — conf 400, g=100. stopped — verdict **P_and_Q** ❌ | **P_and_Q** (400) vs P_and_not-Q (0) — conf 400, g=100 |
| 5 | e5 | | | **P_and_Q** (500) vs P_and_not-Q (0) — conf 500, g=100 |
| 6 | e6 | | | **P_and_Q** (600) vs P_and_not-Q (0) — conf 600, g=100 |
| 7 | e7 | | | **P_and_not-Q** (500) vs P_and_Q (100) — conf 400, g=200 |
| 8 | — (no evidence left) | | | **P_and_not-Q** (500) vs P_and_Q (100) — conf 400, g=0. stopped — verdict **P_and_not-Q** ✔ |

(Cell summary rows: d1 → verdict P_and_Q, conf 100, 1 round, 1 evidence, correct=0; d4 → P_and_Q, conf 400, 4 rounds, 4 evidence, correct=0; d8 → P_and_not-Q, conf 400, 8 rounds, 7 evidence, correct=0→1. Deep-16 matches d8 exactly.)

**What happened, in plain words.** Rounds 1–6 each arrive as another piece of the card-task setup, and each one adds 100 points to the obvious-but-wrong answer "turn P and Q." The correct answer sits at zero the whole time, and each round the harness probes it as the runner-up and finds nothing to refute it with — there is nothing wrong with it, it is just unsupported yet. Stop at depth 1 and you get the bait with confidence 100; stop at depth 4 and the bait has compounded four times (confidence 400, still wrong). Round 7 is where the disconfirming premise finally arrives: the falsification analysis gives P_and_not-Q +500 and takes 500 *off* P_and_Q, flipping the lead to 500 vs 100. Note the refutation test still "holds" for P_and_Q afterward — the 500-point attack is below the 600 refutation bar, so the wrong answer survives as runner-up rather than being eliminated; the win came from the score flip, not from a kill. Round 8 has nothing new (all 7 evidence consumed, no hypothesis ever trailed by ≥ 900 so nothing was eliminated), the lead holds, and deliberation ends with the right answer. The trap is exactly this: six misleading premises, one decisive one, and the decisive one is last.

---

## Trace 2 — the same item under the adaptive rule: why §6 never fired

Same item (`TRAP-C6-001`), adaptive config (ε = 20 thousandths, k = 3, cap 16). Result: **8 rounds, 7 evidence, verdict P_and_not-Q, conf 400, correct=1** — identical to d8. (Adaptive used exactly the same rounds as deep-16 here: 8 and 8. This is one of the 127/127 trap items with **zero** §6 early stops.)

The §6 math, round by round (c₀ := c₁ per the rule, so g₁ = 0):

| round | confidence | gain gᵢ = |cᵢ − cᵢ₋₁| | last 3 gains | §6 stop? |
|---|---|---|---|
| 1 | 100 | 0 | — | no (rounds < 3) |
| 2 | 200 | 100 | — | no (rounds < 3) |
| 3 | 300 | 100 | 0, 100, 100 | no (100 ≥ 20) |
| 4 | 400 | 100 | 100, 100, 100 | no |
| 5 | 500 | 100 | 100, 100, 100 | no |
| 6 | 600 | 100 | 100, 100, 100 | no |
| 7 | 400 | 200 (a drop — absolute value, counts against settling) | 100, 100, 200 | no |
| 8 | 400 | 0 | 100, 200, 0 | no — stopped because the round changed nothing (no evidence left, no elimination) |

**What happened, in plain words.** There was never a quiet stretch for the rule to latch onto. Confidence moved by 100 points *every* round for six rounds, then dropped by 200 when the lead flipped, then held once. The rule needs three consecutive near-zero gains (all under 20 thousandths); the closest it ever got was the final 100, 200, 0 — and by then deliberation was already over, because round 8 consumed no evidence and eliminated nothing, so the harness stopped on "nothing changed," not on §6. This is the honest behavior the 0/127 figure summarizes: on trap items the margin keeps moving until the evidence runs out, so the adaptive rule correctly refuses to stop early and behaves like deep-16.

---

## Trace 3 — an admit item where §6 fired for real: `admit-V2-A-clean-0059` (adaptive)

9 hypotheses, 12 evidence items, ground truth **NEGATIVE_EVIDENCE**. Adaptive stopped at **round 7** (7 of 12 evidence read); deep-16 read all 12 over 12 rounds. Same verdict, same max confidence. Five evidence items were never read — genuine savings, zero accuracy cost.

Evidence pattern (all twelve push the same way): e1 +425, e2 +44, e3 +409, e4 +657, e5 +411, e6 +411, e7 +19, e8 +25, e9 +660, e10 +418, e11 +25, e12 +656 — all supporting NEGATIVE_EVIDENCE, no attacks on anything. (Texts are fixture references, e.g. *"prior seq=48 … judgment=RICH disposition=WITHHELD confidence=425"*; the weights are what the harness sees.)

| round | evidence | leader (score) vs runner-up (score) | conf | gain | notes |
|---|---|---|---|---|---|
| 1 | e1 | **NEGATIVE_EVIDENCE** (425) vs ACCEPT_INSTALL (0) | 425 | 0 | refute test on ACCEPT_INSTALL: holds |
| 2 | e2 | **NEGATIVE_EVIDENCE** (469) vs ACCEPT_INSTALL (0) | 469 | 44 | test: holds |
| 3 | e3 | **NEGATIVE_EVIDENCE** (878) vs ACCEPT_INSTALL (0) | 878 | 409 | test: holds |
| 4 | e4 | **NEGATIVE_EVIDENCE** (1535) vs — (no runner-up) | 1000 | 122 | e4's +657 pushed the margin to 1535 ≥ 900: **all 8 rivals eliminated at once** |
| 5 | e5 | **NEGATIVE_EVIDENCE** (1946) vs — | 1000 | 0 | margin still growing, confidence pinned at max |
| 6 | e6 | **NEGATIVE_EVIDENCE** (2357) vs — | 1000 | 0 | |
| 7 | e7 | **NEGATIVE_EVIDENCE** (2376) vs — | 1000 | 0 | **§6 fires**: last 3 gains 0, 0, 0 — all < 20. Verdict NEGATIVE_EVIDENCE ✔ |

**What happened, in plain words.** Rounds 1–3 steadily build the case for NEGATIVE_EVIDENCE (confidence 425 → 469 → 878), and each round the harness tries to refute the runner-up ACCEPT_INSTALL and finds nothing — it just sits at zero with no attack evidence against it. Round 4 is the knockout: the fourth premise adds 657 points, the margin hits 1535, past the 900 elimination bar, and all eight rival hypotheses are dropped in a single round. From round 4 on the verdict is certain — confidence is pinned at its 1000 maximum because there is nobody left to be unsure against. Rounds 5–7 keep adding points to an already-won race (margin 1535 → 1946 → 2357 → 2376), confidence cannot move, and after three straight zero-gain rounds the §6 rule fires at round 7. The remaining five evidence items (e8–e12) are never read — they could not have changed anything. This is a genuine settle, not a give-up: the rule stopped *after* certainty was reached and held, and it saved 5 rounds (7 vs deep-16's 12) with the identical verdict and confidence.

---

## Reading notes

- **Runner-up scores of 0 are real**, not missing data: every score starts at 0 and only moves when evidence touches that hypothesis. In Trace 1 the bait's rivals sat at 0 for six rounds; in Trace 3 ACCEPT_INSTALL sat at 0 for three rounds while the refutation test probed it each time and found no attack evidence to kill it with.
- **Confidence 1000 in Trace 3 is a clamp, not a score.** The underlying margin was 1535 at round 4 and kept growing; the clamp is what makes the gains read 0 and lets §6 fire. The harness is stopping on a saturated meter while the true margin keeps rising — worth knowing when interpreting "settled."
- **Why d4 took the bait and d8 didn't** is visible in one number: evidence consumed (4/7 vs 7/7). The six misleading premises outnumber the one decisive premise 6-to-1 and are front-loaded; any fixed depth that ends before e7 loses. That is the whole knee: the curve flips only when depth reaches the decisive evidence.
- All three traces are byte-identical between run A and run B of their cells (determinism verified, RESULTS_H5 §2).
