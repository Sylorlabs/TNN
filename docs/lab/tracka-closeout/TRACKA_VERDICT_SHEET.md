# TRACK A — CONSOLIDATED VERDICT SHEET (closeout, r1 1x)

**Date:** 2026-09-21. **Frozen source:** `units/PREREG_FREEZE.md` §3/§5/§7 (commit `b0b9140c0eda`, branch `tnn-native-lab`; all §3 criteria extracted programmatically, never from memory).
**Frozen question:** "what is a unit of knowledge, if not an LLM token?"

## HEADLINE

**NO BLOWOUT — championship undecided (recomputed 2026-09-21, crew S7-RECOMPUTE).** Y5's 7/8 PROVISIONAL BLOWOUT ends: U's binding PASS (commit `9c6d9384ef9973fcc96e4e857145c74d72c27769`) ties Y5 at the ceiling on M1-content, M2, M3, and M6-transfer-tax, and the cost tie-break between them is methodologically blocked (see §3). Decided columns: Y5 3/8 (M1-boundary, M4, M7), L1 1/8 (M5). Per §7, the expected verdict is now Pareto + scenario-fit — the rule does not manufacture a winner.

**The tokenizer replacement (provisional):** Y5's model still leads every column it holds — a unit of knowledge is **one ID over a non-contiguous span set** — a LINK naming an ordered set of 2–8 fixed spans, recalled by replaying the spans in order; kills cascade atomically via LINK with eliminative justification (a LINK survives only while every member span verifies against the corpus). (Stands on the 3 decided Y5 columns + 4 provisional Y5↔U ties; L1 holds the cost column.)

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

## 3. §7 blowout computation (recomputed 2026-09-21 — crew S7-RECOMPUTE)

**Scored columns (8):** M1-content, M1-boundary, M2, M3, M4, M5, M6-transfer-tax, M7. (M1's two sub-scores count separately per §5 "recorded separately, never folded"; this is also the only reading under which §7 rule 4's "M7 N/A needs ≥ 6 of 7" is coherent. Interpretation adopted; counting-rule changes need Micah's re-approval.)

**Eligibility:** non-killed arms with M8 PASS and complete 1x scorecards (21 arms — U added 2026-09-21 per binding PASS, `units/arms/U/ADJUDICATION.md`, commit `9c6d9384ef9973fcc96e4e857145c74d72c27769`).

**Per-column champions** (best scorecard value; ties broken by transfer-tax, then lower cost; then co-champions):

| Column | Champion | Value | Status |
|---|---|---|---|
| M1-content | Y5 ↔ U tie | both 100.0 | PROVISIONAL — tax tie (0.0/0.0); cost tie-break blocked (M5 methodology mismatch, see below) |
| M1-boundary | Y5 | 100.0 > U 99.9 | DECIDED — outright |
| M2 | Y5 ↔ U tie | both ETC 1 all tiers | PROVISIONAL — same cost-tie-break blocker |
| M3 | Y5 ↔ U tie | both 100.0 / CLEAR | PROVISIONAL — same cost-tie-break blocker |
| M4 | Y5 | 100.0/100.0 > U 93.0/100.0 | DECIDED — outright |
| M5 | L1 | 0.839 B/B | DECIDED — outright (beats Y5 1.498 and U under either M5 reading) |
| M6 tax | Y5 ↔ U tie | both 0.0 | PROVISIONAL — same cost-tie-break blocker |
| M7 | Y5 | 100.0 hit (U N/A — non-ID arm) | DECIDED — outright |

**Championship count (decided):** Y5 3/8 · L1 1/8 · 4/8 provisional (Y5↔U).

**M5 methodology blocker (recorded, not a ruling — decides the provisional columns):** U's crew reported "0 corpus-buffer bytes" as the M5 figure, and the ≈1.22 B/B number in the U11 report uses (slot_table 6,563,843 + ledger 64,064) / source 5,422,721 — a formula the frozen §5 does not define (it folds ledger bytes into the memory term and omits the harness-measured RSS delta the frozen definition requires). Applied mechanically, the frozen §5 formula — memory bytes = harness-measured RSS delta + slot table, per source byte — gives U = ((17,256−8,304)×1024 + 6,563,843) / 5,422,721 = **2.90**; Y5's recorded 1.498 is verified against the same formula: (19,562,496 + 2,814,120) / 14,938,062 = 1.4980 exactly. Under the pure mechanical reading Y5 would win every ceiling cost tie-break. **But the two ratios are not apples-to-apples:** U's M5 leg ingested prose only (5,422,721 B — the §5 metric text says "Full prose ingest") while Y5's ingested prose+code (14,938,062 B), a 2.75× source-size gap over which fixed overheads do not normalize away, and granularity differs (U: 84,731 units / 5.4MB vs Y5: 50,797 / 14.9MB). The cost tie-break between Y5 and U cannot be decided by the frozen rule + consistent methodology on the evidence as it stands. **Required:** a harmonized re-measurement (both arms on the same corpus coverage, frozen §5 formula) before M1-content, M2, M3, and M6-tax leave PROVISIONAL. The M5 champion itself (L1 0.839) is unaffected — L1 beats Y5 (1.498) and U under both readings (0.839 < 1.22 < 2.90), so that column is decided outright.

**Blowout rules applied:** no arm reaches 6 of 8 scored columns on decided values — Y5 3/8, L1 1/8 (best provisional case: Y5 7/8, but 4 of those are methodologically provisional). **Y5's r1 PROVISIONAL BLOWOUT ENDS 2026-09-21.** Rule 5 (scale confirmation) is additionally unmet: no arm has a completed passing 10x leg (Y5's 10x leg T2 still running — all columns depending on 10x numbers get recomputed again when it lands). §7's expected verdict now governs: **no overall winner — Pareto frontier + scenario-fit map (§4).** The rule does not manufacture a winner.

**RECOMPUTATION RECORD 2026-09-21 (CREW S7-RECOMPUTE):** this section supersedes the 2026-09-21 U11 flag (recomputation was due, now done). Trigger: U adjudicated PASS (binding), commit `9c6d9384ef9973fcc96e4e857145c74d72c27769`. Per-column before→after: M1-content Y5→Y5↔U (provisional); M1-boundary Y5→Y5 (decided outright, 100.0 > 99.9); M2 Y5→Y5↔U (provisional); M3 Y5→Y5↔U (provisional); M4 Y5→Y5 (decided outright); M5 L1→L1 (decided); M6-tax Y5→Y5↔U (provisional); M7 Y5→Y5 (decided, U N/A). Championship: Y5 7/8→3/8 decided (+4 provisional), L1 1/8→1/8. No other arm's verdict or scorecard was altered; no other arm threatens any column (r1 robustness check stands; U is the only new scored arm). Full working record appended to `~/workspace/NIGHT_RUN_2026-09-21.md`.

## 4. Scenario-fit map (the §7 expected verdict)

| Dimension | Champion | Margin / note |
|---|---|---|
| (1) Corpus type — best M1+M6-tax pair, P→C and C→P | Y5+U both directions | tie at ceiling, tax 0.0 both directions (margin 0.0 < 2 pts → TIED); cost tie-break blocked pending M5 harmonization (see §3) |
| (2) Scale — best M1-at-scale + M5 at highest completed leg | Y5 (1x) | 10x: UNTESTED for all surviving arms (toolchain wall); Y5's 10x leg (T2) still running — columns depending on 10x numbers get recomputed when it lands |
| (3) Pressure regime — M3 survival, freeze CLEAR (high-churn); M5 (archival) | high-churn: Y5+U (both 100.0/CLEAR; cheapest-of-group blocked pending M5 harmonization); archival: L1 (0.839 B/B) | — |
| (4) Teaching availability — M2 ETC + M9 on T2/T3 (autonomous) | Y5+U | tie — ETC 1 all tiers (margin 0 < 2 pts → TIED) |
| (5) Integrity criticality — M1 ID-probe PASS + M8 PASS + M4 (any FAIL excluded) | Y5 (ID probe PASS/PASS, M8 PASS, M4 100/100); also qualify: H1, L1, L2, Y3, Y4, Y6, Z1 | Z4/Z5 excluded (M8 FAIL—panic); U excluded (non-ID arm, no ID probe applicable) |
| (6) Budget constraint — M5 per-byte cost among M1-clearers | L1 0.839 · Y5 1.498 · S 1.718 · Z7 1.811 · Y4 1.823 · Z2 1.974 · X 2.002 · Y3 2.07 · H1 2.412 · Z6 2.437 · U 2.90* · Y6 3.136 · B-16 3.626 · L2 4.307 · A 13.01 · C-P ~14.3 · C-W 16.481 | *U 2.90 = frozen-formula value from harness data (prose-only leg); methodology-flagged, see §3 |

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
4. **D family (D/D-T/D-R)** remains PROVISIONAL — the flagship has a draft verdict, no scorecard, M8 not run. If D dies, the program thesis dies with it (frozen §3). This is the battery's largest open item and is NOT resolved by any §7 championship computation.
5. **§7 M5 methodology blocker (S7-RECOMPUTE 2026-09-21, decide-and-document):** the Y5↔U cost tie-break is PROVISIONAL pending a harmonized M5 re-measurement (both arms, same corpus coverage, frozen §5 formula: harness-measured RSS delta + slot table, per source byte). U's ≈1.22 B/B figure is not a compliant reading (slot_table+ledger, no RSS delta); the mechanical frozen-formula value is 2.90 on a prose-only leg vs Y5's 1.498 on prose+code. This determination decides no arm's verdict and changes no methodology — it records that the comparison is currently non-decidable.

## 7. Pending — needs Micah's word or further work

- **Gap-fill verdicts:** complete (commit `4902dc51dc56f63773cf784367755e19921faefc`). Z2, Z7 PASS; T, K1, F-S, K3, D-R PROVISIONAL (blockers stated); V, W, Z8 UNADJUDICATED (evidence insufficient). KILLED 0 this round.
- **M5 harmonization (unblocks 4 provisional §7 columns):** re-measure U and Y5 M5 on the same corpus coverage under the frozen §5 formula (harness-measured RSS delta + slot table, per source byte); then M1-content, M2, M3, M6-tax leave PROVISIONAL per the cost tie-break. No verdict changes.
- **10x scale leg:** blocked by the znc 2^25-byte slice limit for N and others; Y5's 10x leg (T2) is still running — when it lands, every column depending on 10x numbers gets recomputed again (per the sheet's 1x/10x convention; the 1x recomputation above stands on its own).
- **Sign-offs:** §7 metric-count interpretation (§6.2); B-family ≥2x-on-M3 kill-bar wording; whether M5 cost becomes binding via amendment.
- **D-family completion:** D's draft verdict + missing M8/scorecard is the critical path for the program thesis.

## Evidence trail

- Arm inventory: `docs/lab/tracka-closeout/ARM_INVENTORY.md` (commit `4abfb1c0f0eac9374fe4bd4010bbc67df7114b43`)
- Scorecards: `docs/lab/tracka-closeout/scorecards/` (47 JSONs, 33 arms; originals untouched)
- Section spot-check: `docs/lab/units/closeout/SECTION_SPOTCHECK.md` (commit `025e2172bb002aef40dc35b9d21faf0d01c20065`)
- B-family verdict: `docs/lab/units/arms/B-8/VERDICT.md` (commit `59fb89777f3f`)
- R2 verdict: `units/arms/R2/VERDICT.md` + `docs/lab/units/arms/R2/` (commits `0631928b4413`, `e6d92e47a304`, `8b6e11d28d2f`)
- Championship computation: `/tmp/tracka_rows2.json` (working); method documented in §3 above.
- §7 recomputation 2026-09-21 (crew S7-RECOMPUTE): working record in `~/workspace/NIGHT_RUN_2026-09-21.md` ("§7 recomputation" entry); U M5 source artifacts `units/arms/U/work/adjud/scorecard/m5-1x/` + Y5 `units/arms/Y5/evidence/scorecard_y5_1x.json`.
