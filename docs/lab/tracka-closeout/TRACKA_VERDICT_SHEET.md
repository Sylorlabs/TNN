# TRACK A — CONSOLIDATED VERDICT SHEET (closeout, r1 1x)

**Date:** 2026-09-21. **Frozen source:** `units/PREREG_FREEZE.md` §3/§5/§7 (commit `b0b9140c0eda`, branch `tnn-native-lab`; all §3 criteria extracted programmatically, never from memory).
**Frozen question:** "what is a unit of knowledge, if not an LLM token?"

## HEADLINE

**PROVISIONAL BLOWOUT: Y5 — Cross-stream span sets.** Y5 is champion in 7 of the 8 scored metric columns under §7's tie-break rules (transfer-tax, then lower cost), passes M8, has no weak flank, and clears the N/A discipline. It is PROVISIONAL — not confirmed — solely because no arm has a completed 10x leg with a passing verdict (§7 rule 5: "a 1x-only blowout is PROVISIONAL BLOWOUT").

**The tokenizer replacement (provisional):** a unit of knowledge is **one ID over a non-contiguous span set** — a LINK naming an ordered set of 2–8 fixed spans, recalled by replaying the spans in order; kills cascade atomically via LINK with eliminative justification (a LINK survives only while every member span verifies against the corpus).

## 1. The 53-vs-55 discrepancy — RESOLVED

- Frozen §3 defines **52 arms**, not 53. The file's own "53 arms ratified" footer is an arithmetic error (verified by programmatic row extraction: 52 distinct IDs). Y2 (`units/arms/Y2/`) is an explicitly PROPOSED-PENDING-FREEZE row, never signed — excluded.
- The 55 on-disk dirs = 52 arm dirs + 3 infrastructure dirs (`briefs/`, `harness/`, `hidden_files/`).
- `q/` = arm Q (case mismatch only). B-64's build lives in `units/arms/harness/b64/` (per §3: "B-64 doubles as harness validator (built first)") — build and testing CONFIRMED from primary evidence (B-family verdict, commit `59fb89777f3f`).

## 2. Per-arm verdicts (52 frozen arms)

| Arm | Verdict | Kill fired | M8 | Legs |
|---|---|---|---|---|
| A | PASS | no | PASS | 1x |
| B-8 | KILLED (retired as size) | yes | PASS | 1x |
| B-16 | PASS | no | PASS | 1x |
| B-64 | PASS (survives) | no | PASS | 1x |
| C-W | PASS | no | PASS | 1x |
| C-P | PASS | no | PASS | 1x |
| D | PROVISIONAL (draft) | unresolved | NOT RUN | partial 1x |
| D-T | PROVISIONAL | pending | NOT RUN | partial 1x |
| D-R | PROVISIONAL | not evaluated | NOT RUN | sub-1x |
| E | KILLED | yes (2.764× ≥ 2× at 10x) | PASS | 1x+10x |
| F-S | PROVISIONAL — kills (i),(ii) verified NOT FIRED (F1 max 0.000218; 17,155 cuts vs 12.2M threshold); kill (iii) blocked on D's M3 (rule: fires iff F-S M3 100.0 < D's both corpora) | pending | PASS | 1x (status) |
| F-B | PROVISIONAL | unresolved | NOT RUN | partial (M1) |
| G1 | KILLED | yes | NOT STATED | 1x |
| G2 | KILLED | yes | PASS | 1x |
| H1 | PASS | no | PASS | 1x |
| H2 | KILLED | yes (99.9% fallback vs 40% ceiling) | NOT STATED | 1x |
| I1 | PROVISIONAL | unresolved | INCOMPLETE | partial 1x |
| I2 | KILLED | yes (55.9% arbitration error) | NOT STATED | 1x |
| J1 | KILLED | yes | NOT RUN | 1x |
| J2 | KILLED | yes | NOT RUN | 1x |
| K1 | PROVISIONAL (kill ii unevaluable: k1-chain FATALs) | pending | — | M1 only |
| K2 | PASS | no | PASS | 1x |
| K3 | PROVISIONAL | unresolved | NOT ATTEMPTED | incomplete 1x |
| L1 | PASS | no | PASS | 1x |
| L2 | PASS | no | PASS | 1x |
| M | KILLED (scoped: cross-store/global identity) | yes | PASS | 1x |
| M2 | KILLED | yes (28.8%/26.8% at 10x) | n/a | 10x (K2 leg) |
| N | PASS | no | PASS | 1x (10x ATTEMPTED—FAILED, toolchain) |
| O | PROVISIONAL | unresolved | PENDING | partial 1x |
| P | PASS | no | PASS | 1x |
| Q | KILLED | yes | PASS | 1x |
| R | KILLED | yes (OR-kill: 100.0 vs 100.0 tie) | PASS | 1x |
| R2 | KILLED | yes (disjunct a: margin 0.0 < 3) | PASS | 1x |
| S | PASS | no | PASS | 1x |
| T | KILLED | yes (i: B2 ratio 1.00 ≤ 2 both corpora; ii: 100% sub-episode queries; iv: floor, beats X on 0/4) | PASS | 1x |
| U | PASS | no | PASS | 1x |
| V | UNADJUDICATED (never built: no arm.zag) | n/a | — | — |
| W | UNADJUDICATED (truncated M1 only; no composite def) | n/a | — | — |
| X | PASS | no | PASS | 1x |
| Y1 | KILLED | yes | PASS | 1x |
| Y3 | PASS | no | PASS | 1x |
| Y4 | PROVISIONAL (conditional on D) | unresolved | PASS | 1x |
| Y5 | **PASS — PROVISIONAL BLOWOUT** | no | PASS | 1x (10x blocked, toolchain) |
| Y6 | PASS | no | PASS | 1x |
| Z1 | PROVISIONAL (blocked on D) | unresolved | PASS | 1x |
| Z2 | PASS | no | PASS | 1x |
| Z3 | PASS (survives) | no | PASS | 1x |
| Z4 | KILLED | yes (panic) | FAIL | 1x |
| Z5 | KILLED | yes (panic) | FAIL | 1x |
| Z6 | PASS | no | PASS | 1x |
| Z7 | PASS | no | PASS | 1x |
| Z8 | PASS (commit `0587e778fcb2`; clause 1: 50.0% boundary-error reduction ≥ 40% bar; clause 2: mean fuzz → 0.0, tighten dominates) | n/a | — | — |

Counts: KILLED 17 · PASS 21 · PROVISIONAL 11 · UNADJUDICATED 3. (U adjudicated PROVISIONAL→PASS 2026-09-21, MARATHON CREW U11; see `units/arms/U/ADJUDICATION.md`.)
Verification: 7 section verdicts spot-checked (E, I2, K2, M-headline, M2, P, Z3) — 6 CONFIRMED, 1 secondary-claim correction (M-dedup, see §6). B-family verdict produced (B-8 retired, B-16/B-64 survive, family not killed as contender). R2 re-evaluated post-R-death: KILLED, disjunct (a).

## 3. §7 blowout computation

**Scored columns (8):** M1-content, M1-boundary, M2, M3, M4, M5, M6-transfer-tax, M7. (M1's two sub-scores count separately per §5 "recorded separately, never folded"; this is also the only reading under which §7 rule 4's "M7 N/A needs ≥ 6 of 7" is coherent. Interpretation adopted; counting-rule changes need Micah's re-approval.)

**Eligibility:** non-killed arms with M8 PASS and complete 1x scorecards (20 arms).

**Per-column champions** (best scorecard value; ties broken by transfer-tax, then lower cost; then co-champions):

| Column | Champion | Value | Margin to runner-up |
|---|---|---|---|
| M1-content | Y5 | 100.0 | tie at ceiling; wins tie-break (tax 0.0, cost 1.498 lowest among tax-0 group) |
| M1-boundary | Y5 | 100.0 | same tie-break |
| M2 | Y5 | ETC 1 | tie at 1; same tie-break |
| M3 | Y5 | 100.0 / CLEAR | tie at ceiling; same tie-break |
| M4 | Y5 | 100.0/100.0 | tie at ceiling; same tie-break |
| M5 | L1 | 0.839 B/B | outright; runner-up Y5 1.498 |
| M6 tax | Y5 | 0.0 | tie at 0.0; wins on cost tie-break |
| M7 | Y5 | 100.0 hit | tie at ceiling (8 ID arms with data); wins tie-break |

**Championship count:** Y5 7/8 · L1 1/8.

**Blowout rules applied to Y5:**
1. M8 PASS ✓ (`M8GATE PASS`, 6 perturbations byte-identical)
2. Champion in ≥ 6 of 8 scored columns ✓ (7/8)
3. No weak flank ✓ (worst column M5: 2nd of 13 with data — above 50th percentile)
4. N/A discipline ✓ (all 8 columns applicable; needs ≥ 6)
5. Scale confirmation 1x → 10x ✗ — Y5's 10x leg is blocked by the znc 2^25-byte slice limit (same toolchain wall that stopped N's 10x). No arm has a completed passing 10x leg.

**Verdict: PROVISIONAL BLOWOUT for Y5.** §7: "A 1x-only blowout is PROVISIONAL BLOWOUT." The rule does not manufacture a winner — and here it doesn't need to: Y5 earns 7/8 columns on the tie-breaks as written.

**Robustness of the computation:** every scored arm that could threaten Y5's tie-break was checked — S (m5 1.718), Z6 (2.437), C-P (~14.3), C-W (16.481), A (13.01) all cost more than Y5's 1.498 at equal ceiling metrics and zero transfer tax. N has no metrics scorecard (verdict-only PASS). Gap-fill is complete: Z2/Z7 PASS (both already in the computation — m5 1.974/1.811, no threat); T, K1, F-S, K3, D-R PROVISIONAL and V, W, Z8 UNADJUDICATED — none scored, so none can take a column from Y5. If any of them later produces ceiling metrics + transfer tax 0.0 + cost < 1.498, the championship must be recomputed.

**FLAG 2026-09-21 (MARATHON CREW U11):** U has been adjudicated PASS (binding) and now meets that trigger condition on its face — M1-content 100.0, M2 ETC 1, M3 100.0/CLEAR, M6 tax 0.0, M8 PASS, and M5 ≈ 1.22 B/B ((slot_table 6,563,843 + ledger 64,064) / source 5,422,721; methodology-dependent — U's crew reported "0 corpus-buffer bytes", not a B/B ratio, so the §7 M5 formula must be applied consistently before comparing to Y5's 1.498). **The §7 championship recomputation is therefore DUE but NOT YET DONE** — the per-column table above does not include U. A mechanical recomputation may move M1-content, M2, M3, and M6-tax from Y5 to U on the cost tie-break (U: tax 0.0, cost ~1.22 < 1.498), which would end Y5's 7/8 championship. This needs a dedicated §7 recomputation pass, not a unilateral edit.

## 4. Scenario-fit map (the §7 expected verdict)

| Dimension | Champion | Margin / note |
|---|---|---|
| (1) Corpus type — best M1+M6-tax pair, P→C and C→P | Y5 both directions | tie at ceiling; cost tie-break |
| (2) Scale — best M1-at-scale + M5 at highest completed leg | Y5 (1x) | 10x: UNTESTED for all surviving arms (toolchain wall) |
| (3) Pressure regime — M3 survival, freeze CLEAR (high-churn); M5 (archival) | high-churn: Y5 (100.0/CLEAR, cheapest of the M3-clear group); archival: L1 (0.839 B/B) | — |
| (4) Teaching availability — M2 ETC + M9 on T2/T3 (autonomous) | Y5 (ETC 1 all tiers) | — |
| (5) Integrity criticality — M1 ID-probe PASS + M8 PASS + M4 (any FAIL excluded) | Y5 (ID probe PASS/PASS, M8 PASS, M4 100/100); also qualify: H1, L1, L2, Y3, Y4, Y6, Z1 | Z4/Z5 excluded (M8 FAIL—panic) |
| (6) Budget constraint — M5 per-byte cost among M1-clearers | L1 0.839 · Y5 1.498 · S 1.718 · Z7 1.811 · Y4 1.823 · Z2 1.974 · X 2.002 · Y3 2.07 · H1 2.412 · Z6 2.437 · Y6 3.136 · B-16 3.626 · L2 4.307 · A 13.01 · C-P ~14.3 · C-W 16.481 | margins ≥ 2 pts except L1→Y5 (0.659 = 44% relative — not tied) |

## 5. What died and what it means

- **R, R2 — dead on the ceiling technicality.** Both hit 100.0 held-out recall; R's literal OR-kill fired on the tie, R2's disjunct (a) on the 0.0 margin vs R. Compression buys nothing measurable over the 64-byte baseline at these bars — but note the bars may be too easy, not the mechanism too weak.
- **E — dead informatively.** "References matter, transient segmentation does not": 2.764× B-64's stored bytes at equal recall.
- **B-8 — retired as a size.** 8-byte granularity priced in capacity (M3 FROZEN-UNDER-PRESSURE → cell 0); B-16/B-64 survive. The B family's ≥2x-on-M3 kill bar is arithmetically unreachable while any B size holds the ceiling — flagged for Micah.
- **M (scoped), M2, I2, G1/G2, H2, J1/J2, Q, Y1, Z4/Z5** — killed by their own bars; see inventory.
- **The ceiling pattern:** ~15 surviving arms sit at 100.0/ETC-1/tax-0.0 on the 1x battery. The battery discriminates on cost (M5) and pressure (M3) only. A harder battery (or the 10x leg) is needed before any champion is more than provisional.

## 6. Coordinator rulings (decide-and-document, per Micah's standing rule)

1. **M-dedup:** the verdict's M-dedup death (dedup_barred 0.00) is SUPERSEDED — the 0.00 was measured with the dedup path compiled out (invalid); the corrected run gives 50.01 ≥ 0.4 → survives. Headline scoped kill unaffected.
2. **§7 "8 scored metrics"** = {M1-content, M1-boundary, M2–M7}. Adopted as interpretation; needs Micah's sign-off as a counting-rule change.
3. **Y2 excluded** from the battery (unfrozen proposal; the "53 arms ratified" footer is an arithmetic error).
4. **D family (D/D-T/D-R)** remains PROVISIONAL — the flagship has a draft verdict, no scorecard, M8 not run. If D dies, the program thesis dies with it (frozen §3). This is the battery's largest open item and is NOT resolved by Y5's provisional blowout.

## 7. Pending — needs Micah's word or further work

- **Gap-fill verdicts:** complete (commit `4902dc51dc56f63773cf784367755e19921faefc`). Z2, Z7 PASS; T, K1, F-S, K3, D-R PROVISIONAL (blockers stated); V, W, Z8 UNADJUDICATED (evidence insufficient). KILLED 0 this round.
- **10x scale leg:** blocked by the znc 2^25-byte slice limit for Y5, N, and others. Y5's blowout cannot confirm until this wall is crossed or the leg is re-scoped by amendment.
- **Sign-offs:** §7 metric-count interpretation (§6.2); B-family ≥2x-on-M3 kill-bar wording; whether M5 cost becomes binding via amendment.
- **D-family completion:** D's draft verdict + missing M8/scorecard is the critical path for the program thesis.

## Evidence trail

- Arm inventory: `docs/lab/tracka-closeout/ARM_INVENTORY.md` (commit `4abfb1c0f0eac9374fe4bd4010bbc67df7114b43`)
- Scorecards: `docs/lab/tracka-closeout/scorecards/` (47 JSONs, 33 arms; originals untouched)
- Section spot-check: `docs/lab/units/closeout/SECTION_SPOTCHECK.md` (commit `025e2172bb002aef40dc35b9d21faf0d01c20065`)
- B-family verdict: `docs/lab/units/arms/B-8/VERDICT.md` (commit `59fb89777f3f`)
- R2 verdict: `units/arms/R2/VERDICT.md` + `docs/lab/units/arms/R2/` (commits `0631928b4413`, `e6d92e47a304`, `8b6e11d28d2f`)
- Championship computation: `/tmp/tracka_rows2.json` (working); method documented in §3 above.
