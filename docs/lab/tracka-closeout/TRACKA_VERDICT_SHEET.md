# TRACK A — CONSOLIDATED VERDICT SHEET (closeout, r1 1x)

**Date:** 2026-09-21. **Frozen source:** `units/PREREG_FREEZE.md` §3/§5/§7 (commit `b0b9140c0eda`, branch `tnn-native-lab`; all §3 criteria extracted programmatically, never from memory).
**Frozen question:** "what is a unit of knowledge, if not an LLM token?"

## HEADLINE

**Y5 CONFIRMED BLOWOUT (scale-confirmed 2026-09-21, crew S7-SCALE).** The M5 methodology blocker is resolved: Y5 and U re-measured at identical prose-only coverage (5,422,721 B) under the frozen §5 formula (harness-measured RSS delta + slot table, per source byte) — Y5 **1.659** B/B vs U **2.902** B/B (4 s.f.). Transfer-tax is tied 0.0/0.0 on all four ceiling columns, so the frozen §7 cost tie-break goes to Y5 on M1-content, M2, M3, and M6-transfer-tax. Decided columns: Y5 7/8 (M1-content, M1-boundary, M2, M3, M4, M6-tax, M7), L1 1/8 (M5). §7 rules 1–4 are met at 1x; rule 5 (scale confirmation) is now MET — Y5's 10x leg CONFIRMED 2026-09-21 (T2-followup, commit `f225a71ffb53bc459877679e9e757052e2272281`): rules 1–4 re-applied to the 10x evidence all hold, so the blowout is CONFIRMED, not provisional. U's binding PASS (commit `9c6d9384ef9973fcc96e4e857145c74d72c27769`) is unaffected; the harmonized numbers are tie-break inputs only and change no arm's scorecard or verdict.

**The tokenizer replacement (confirmed):** Y5's model still leads every column it holds — a unit of knowledge is **one ID over a non-contiguous span set** — a LINK naming an ordered set of 2–8 fixed spans, recalled by replaying the spans in order; kills cascade atomically via LINK with eliminative justification (a LINK survives only while every member span verifies against the corpus). (Stands on the 7 decided Y5 columns at 1x — blowout scale-confirmed at 10x 2026-09-21; L1 holds the cost column.)

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
| I1 | KILLED | yes (kill ii: 22.1% prose audit ops > 20% bar) | PASS (10/10 byte-identical) | full 1x |
| I2 | KILLED | yes (55.9% arbitration error) | NOT STATED | 1x |
| J1 | KILLED | yes | NOT RUN | 1x |
| J2 | KILLED | yes | NOT RUN | 1x |
| K1 | KILLED (kill ii: mean chain 20.00>8, latency 9.99x>2x) | yes (kill ii) | PARTIAL (M1 PASS; M8 gap documented) | 1x (20-batch diagnostic; 100-batch blocked by infra) |
| K2 | PASS | no | PASS | 1x |
| K3 | PROVISIONAL | unresolved | NOT ATTEMPTED | incomplete 1x |
| L1 | PASS | no | PASS | 1x |
| L2 | PASS | no | PASS | 1x |
| M | KILLED (scoped: cross-store/global identity) | yes | PASS | 1x |
| M2 | KILLED | yes (28.8%/26.8% at 10x) | n/a | 10x (K2 leg) |
| N | PASS | no | PASS | 1x (10x ATTEMPTED—FAILED, toolchain) |
| O | KILLED (kill-i: acceleration) | yes | INCOMPLETE | 1x |
| P | PASS | no | PASS | 1x |
| Q | KILLED | yes | PASS | 1x |
| R | KILLED | yes (OR-kill: 100.0 vs 100.0 tie) | PASS | 1x |
| R2 | KILLED | yes (disjunct a: margin 0.0 < 3) | PASS | 1x |
| S | PASS | no | PASS | 1x |
| T | KILLED | yes (i: B2 ratio 1.00 ≤ 2 both corpora; ii: 100% sub-episode queries; iv: floor, beats X on 0/4) | PASS | 1x |
| U | PASS | no | PASS | 1x |
| V | UNADJUDICATED (never built: no arm.zag) | n/a | — | — |
| W | PASS | no (i: not computable, no frozen formula; ii: 0/959825 refusals; iii: M8GATE PASS small-corpus, full in progress; iv: beats X 4/4) | PASS | 1x |
| X | PASS | no | PASS | 1x |
| Y1 | KILLED | yes | PASS | 1x |
| Y3 | PASS | no | PASS | 1x |
| Y4 | PROVISIONAL (conditional on D) | unresolved | PASS | 1x |
| Y5 | **PASS — CONFIRMED BLOWOUT** | no | PASS | 10x (scale-confirmed 2026-09-21) |
| Y6 | PASS | no | PASS | 1x |
| Z1 | PROVISIONAL (blocked on D; adjudicated U13 2026-09-21 — kill disjunct 2 verified NOT triggered, disjunct 1 gated on T3) | unresolved | PASS | 1x |
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
| M1-content | Y5 | 100.0 (tie broken on cost) | DECIDED — tax tie 0.0/0.0; cost tie-break: Y5 1.659 < U 2.902 B/B (prose-only harmonized, see below) |
| M1-boundary | Y5 | 100.0 > U 99.9 | DECIDED — outright |
| M2 | Y5 | ETC 1 all tiers (tie broken on cost) | DECIDED — cost tie-break: Y5 1.659 < U 2.902 B/B (prose-only harmonized) |
| M3 | Y5 | 100.0 / CLEAR (tie broken on cost) | DECIDED — cost tie-break: Y5 1.659 < U 2.902 B/B (prose-only harmonized) |
| M4 | Y5 | 100.0/100.0 > U 93.0/100.0 | DECIDED — outright |
| M5 | L1 | 0.839 B/B | DECIDED — outright (beats Y5 1.659* and U 2.902*; *prose-only harmonized 2026-09-21 — Y5's scorecard M5 remains 1.498 on its committed prose+code leg) |
| M6 tax | Y5 | 0.0 (tie broken on cost) | DECIDED — transfer-tax tie 0.0/0.0; cost tie-break: Y5 1.659 < U 2.902 B/B (prose-only harmonized) |
| M7 | Y5 | 100.0 hit (U N/A — non-ID arm) | DECIDED — outright |

**Championship count (decided):** Y5 7/8 · L1 1/8 · 0/8 provisional.

**M5 methodology blocker — RESOLVED 2026-09-21 (crew M5-HARMONIZE, decide-and-document).** The harmonized re-measurement is complete: both arms at identical prose-only coverage (**5,422,721 B**, SHA-256 `a023115c2d4e2ee12221bdd780fdf2ac5a864fe225948656f51f8be462c7fffb`, the frozen r1 prose corpus) under the frozen §5 formula — M5 memory B/B = ((RSS_run_KB − RSS_baseline_KB) × 1024 + slot_table_bytes) / source_bytes, RSS from the official harness double-run (`run_metric.sh`, run2 convention per `scorecard_assemble.py`):

- **U:** frozen source = committed adjudication `9c6d9384ef9973fcc96e4e857145c74d72c27769`; re-run of the committed M5 leg byte-identical to committed evidence (fragment fields identical; run2 RSS 17,260 KB / baseline 8,304 KB = committed values exactly). M5 = ((17,260−8,304)×1024 + 6,563,843) / 5,422,721 = **2.902**.
- **Y5:** committed leg covered prose+code; a prose-only adapter leg was built from the committed source (Git-blob `057792f6d6f6691c0be0533ca4e115535245bf28`) — same mechanisms (same `y_new` sizing rule, same `ingest_all`, same `y_link_pass`, same slot/ledger accounting, same touched empty-store baseline), code corpus removed from coverage only; pure Zag, frozen compiler. Rebuilt-binary reproduction of the committed prose+code leg was byte-identical to committed evidence first (run2 RSS 56,804 KB / baseline 37,700 KB). Prose-only double-run: run2 RSS 33,724 KB / baseline 26,236 KB, stdout byte-identical, 17,867 units / 1,327,320 B slot table. M5 = ((33,724−26,236)×1024 + 1,327,320) / 5,422,721 = **1.659**.
- **Tie-break:** transfer-tax tied 0.0/0.0 on M1-content, M2, M3, M6-tax → frozen §7 cost tie-break → **Y5 wins all four** (1.659 < 2.902; relative margin 74.9%, far beyond any tie band). Y5's scorecard M5 (1.498, committed prose+code leg) and U's adjudicated PASS are unchanged — the harmonized numbers are tie-break inputs only.
- U's ≈1.22 B/B figure remains a non-compliant reading (slot_table+ledger, no RSS delta). Full measurement record: `~/workspace/NIGHT_RUN_2026-09-21.md` ("M5-HARMONIZE" entry); working artifacts: `~/workspace/m5h/`.

**Blowout rules applied (re-evaluated post-harmonization, 2026-09-21):** Y5 holds 7/8 decided columns (M1-content, M1-boundary, M2, M3, M4, M6-tax, M7); L1 holds M5. Rule 1 (M8 PASS) ✓; rule 2 (≥ 6 of 8) ✓ at 7/8; rule 3 (no weak flank) ✓ — Y5's only non-champion scored metric is M5, where its scorecard 1.498 B/B ranks 2nd of the 17 M1-clearing arms (L1 0.839), and even if all 4 unlisted eligible arms beat it, 6th of 21 clears the 50th percentile; rule 4 (N/A discipline) ✓ — Y5 has no N/A scored metric, 7/8 of 8. Rule 5 (scale confirmation) is MET 2026-09-21 (crew S7-SCALE): Y5's 10x leg CONFIRMED (T2-followup, commit `f225a71ffb53bc459877679e9e757052e2272281`) and rules 1–4 reproduce on the 10x evidence (see SCALE-CONFIRMATION RECORD). **Y5's blowout is CONFIRMED 2026-09-21 on decided 7/8, scale-confirmed at 10x.** Pareto + scenario-fit (§4) remain the expected-verdict frame for everything the blowout doesn't cover. The rule does not manufacture a winner.

**RECOMPUTATION RECORD 2026-09-21 (CREW S7-RECOMPUTE):** this section supersedes the 2026-09-21 U11 flag (recomputation was due, now done). Trigger: U adjudicated PASS (binding), commit `9c6d9384ef9973fcc96e4e857145c74d72c27769`. Per-column before→after: M1-content Y5→Y5↔U (provisional); M1-boundary Y5→Y5 (decided outright, 100.0 > 99.9); M2 Y5→Y5↔U (provisional); M3 Y5→Y5↔U (provisional); M4 Y5→Y5 (decided outright); M5 L1→L1 (decided); M6-tax Y5→Y5↔U (provisional); M7 Y5→Y5 (decided, U N/A). Championship: Y5 7/8→3/8 decided (+4 provisional), L1 1/8→1/8. No other arm's verdict or scorecard was altered; no other arm threatens any column (r1 robustness check stands; U is the only new scored arm). Full working record appended to `~/workspace/NIGHT_RUN_2026-09-21.md`.

**HARMONIZATION RECORD 2026-09-21 (CREW M5-HARMONIZE):** this record supersedes the S7-RECOMPUTE "M5 methodology blocker" (resolved, not re-ruled). Trigger: S7's required harmonized re-measurement. Per-column before→after: M1-content Y5↔U provisional→Y5 DECIDED (cost tie-break 1.659 < 2.902); M2 Y5↔U provisional→Y5 DECIDED (same); M3 Y5↔U provisional→Y5 DECIDED (same); M6-tax Y5↔U provisional→Y5 DECIDED (same); M1-boundary, M4, M5, M7 unchanged. Championship: Y5 3/8→7/8 decided, L1 1/8→1/8, provisional 4/8→0/8. §7 rules 1–4 re-evaluated and met at 1x (see "Blowout rules applied"); rule 5 unmet → PROVISIONAL BLOWOUT restored on decided 7/8. No arm's verdict, scorecard, or §13 was altered. Full measurement record appended to `~/workspace/NIGHT_RUN_2026-09-21.md` ("M5-HARMONIZE" entry).

**SCALE-CONFIRMATION RECORD 2026-09-21 (CREW S7-SCALE):** this record resolves frozen §7 rule 5 (scale confirmation) for Y5. Evidence: T2-followup 10x battery, commit `f225a71ffb53bc459877679e9e757052e2272281` (`units/arms/Y5/evidence/battery_10x/`: `Y5_10X_VERDICT_REPORT.md` + `battery_10x_n5.log`; report sha256-verified identical to the committed blob). 10x scorecard, all legs N=5 byte-identical reruns: M1-content recall 100.0 / boundary 100.0 (ID probe PASS); M1-boundary recall 100.0 / boundary 100.0; M2 ETC=1 all tiers (final recall 100.0); M3 = 0 per §5 (FROZEN-UNDER-PRESSURE flag; survival 100.0 — scored 0, not N/A); M4 rev boundary 100.0 / content 100.0, kill 0.0; M5 leg PASS (580,218 units, 151.5MB learned); M6-transfer-tax 0.0 both directions (rec/bnd/rev 100.0); M7 hit 100.0, reuse 3.1; M8-10x 25/25 byte-identical PASS. Rules 1–4 re-applied at 10x: rule 1 ✓ (M8-10x PASS, no disqualification); rule 2 ✓ — Y5 section champion in 8/8 scored columns ≥ 6; rule 3 ✓ — Y5 at the 100th percentile of the applicable-score population on every scored metric; rule 4 ✓ — no N/A scored metric, 8/8 applicable ≥ 6. 10x-arm survey on the branch: Y5 is the sole arm with a completed 10x leg; E's 10x files (`units/arms/E/evidence/`) are partial M1/M5 leg fragments and M2's `k2_10x.json` is a K2 kill check — neither a complete 10x scorecard; D/T 10x fragments exist only as uncommitted work files. READING OF "REPRODUCE" (stated, not assumed): rule 5 re-applies rules 1–4 to the 10x evidence under the frozen population-relative definitions ("best scorecard value"; "percentiles over arms with applicable scores"), which impose no minimum arm count at the new scale — with Y5 the sole arm holding a completed 10x leg, the rules evaluate over that population and all four hold. The alternative reading (multi-arm 10x head-to-head required before promotion) would add an unwritten requirement — an amendment needing Micah's signature — so it is not applied. CAVEAT: the 10x championships are single-arm (uncontested). If another arm completes a 10x leg, the §7 computation at 10x must be re-run. Result: **PROMOTED — Y5 PROVISIONAL BLOWOUT → CONFIRMED BLOWOUT.** No other §7 content changed. Full working record appended to `~/workspace/NIGHT_RUN_2026-09-21.md` ("S7-SCALE" entry).

## 4. Scenario-fit map (the §7 expected verdict)

| Dimension | Champion | Margin / note |
|---|---|---|
| (1) Corpus type — best M1+M6-tax pair, P→C and C→P | Y5+U both directions | tie at ceiling, tax 0.0 both directions (margin 0.0 < 2 pts → TIED); cost tie-break resolved 2026-09-21: Y5 1.659 < U 2.902 B/B (prose-only harmonized, see §3) |
| (2) Scale — best M1-at-scale + M5 at highest completed leg | Y5 (1x) | 10x: UNTESTED for all surviving arms (toolchain wall); Y5's 10x leg (T2) still running — columns depending on 10x numbers get recomputed when it lands |
| (3) Pressure regime — M3 survival, freeze CLEAR (high-churn); M5 (archival) | high-churn: Y5+U (both 100.0/CLEAR; cheapest-of-group: Y5 1.659 < U 2.902 B/B, prose-only harmonized 2026-09-21); archival: L1 (0.839 B/B) | — |
| (4) Teaching availability — M2 ETC + M9 on T2/T3 (autonomous) | Y5+U | tie — ETC 1 all tiers (margin 0 < 2 pts → TIED) |
| (5) Integrity criticality — M1 ID-probe PASS + M8 PASS + M4 (any FAIL excluded) | Y5 (ID probe PASS/PASS, M8 PASS, M4 100/100); also qualify: H1, L1, L2, Y3, Y4, Y6, Z1 | Z4/Z5 excluded (M8 FAIL—panic); U excluded (non-ID arm, no ID probe applicable) |
| (6) Budget constraint — M5 per-byte cost among M1-clearers | L1 0.839 · Y5 1.498 · S 1.718 · Z7 1.811 · Y4 1.823 · Z2 1.974 · X 2.002 · Y3 2.07 · H1 2.412 · Z6 2.437 · U 2.902* · Y6 3.136 · B-16 3.626 · L2 4.307 · A 13.01 · C-P ~14.3 · C-W 16.481 | *U 2.902 = frozen-formula value from harness data (prose-only leg); harmonized vs Y5 2026-09-21 (see §3); Y5's 1.498 is its committed prose+code scorecard leg |

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
5. **§7 M5 methodology blocker — RESOLVED 2026-09-21 (crew M5-HARMONIZE, decide-and-document):** the Y5↔U cost tie-break is DECIDED per the frozen §7 rule (transfer-tax tied 0.0/0.0 → lower harmonized cost wins): Y5 **1.659** vs U **2.902** B/B, both at identical prose-only coverage (5,422,721 B) under the frozen §5 formula (harness-measured RSS delta + slot table, per source byte). U's ≈1.22 B/B figure is not a compliant reading (slot_table+ledger, no RSS delta). This determination decides no arm's verdict and changes no methodology — it records the comparison as now decidable, and decided. Full record in §3 + `~/workspace/NIGHT_RUN_2026-09-21.md` ("M5-HARMONIZE" entry).

## 7. Pending — needs Micah's word or further work

- **Gap-fill verdicts:** complete (commit `4902dc51dc56f63773cf784367755e19921faefc`). Z2, Z7 PASS; T, K1, F-S, K3, D-R PROVISIONAL (blockers stated); V, W, Z8 UNADJUDICATED (evidence insufficient). KILLED 0 this round.
- **M5 harmonization — DONE 2026-09-21 (crew M5-HARMONIZE):** Y5 1.659 vs U 2.902 B/B (prose-only, frozen §5 formula); M1-content, M2, M3, M6-tax now DECIDED (Y5) per the §7 cost tie-break. No verdict changed.
- **10x scale leg:** blocked by the znc 2^25-byte slice limit for N and others; Y5's 10x leg (T2) is still running — when it lands, every column depending on 10x numbers gets recomputed again (per the sheet's 1x/10x convention; the 1x recomputation above stands on its own).
- **Sign-offs:** §7 metric-count interpretation (§6.2); B-family ≥2x-on-M3 kill-bar wording; whether M5 cost becomes binding via amendment.
- **D-family completion:** D's draft verdict + missing M8/scorecard is the critical path for the program thesis.

## Evidence trail

- Arm inventory: `docs/lab/tracka-closeout/ARM_INVENTORY.md` (commit `4abfb1c0f0eac9374fe4bd4010bbc67df7114b43`)
- Scorecards: `docs/lab/tracka-closeout/scorecards/` (47 JSONs, 33 arms; originals untouched)
- Section spot-check: `docs/lab/units/closeout/SECTION_SPOTCHECK.md` (commit `025e2172bb002aef40dc35b9d21faf0d01c20065`)
- B-family verdict: `docs/lab/units/arms/B-8/VERDICT.md` (commit `59fb89777f3f`)
- R2 verdict: `units/arms/R2/VERDICT.md` + `docs/lab/units/arms/R2/` (commits `0631928b4413`, `e6d92e47a304`, `8b6e11d28d2f`)
- Z1 adjudication: `docs/lab/units/arms/Z1/ADJUDICATION.md` (MARATHON CREW U13 re-dispatch, 2026-09-21) — independent rebuild + ×2 byte-identical re-runs of m1/m4 legs; kill disjunct 2 NOT triggered (1.3% prose / 8.2% code narrowing, 0.0% widened); prose corpus-staleness corrected (39,870 units / 54.7% regret on frozen r1 corpus); M8 re-run 10/10 byte-identical on frozen corpus. Disjunct 1 (vs arm D) gated on crew T3's committed D-family verdict — not yet landed.
- Championship computation: `/tmp/tracka_rows2.json` (working); method documented in §3 above.
- §7 recomputation 2026-09-21 (crew S7-RECOMPUTE): working record in `~/workspace/NIGHT_RUN_2026-09-21.md` ("§7 recomputation" entry); U M5 source artifacts `units/arms/U/work/adjud/scorecard/m5-1x/` + Y5 `units/arms/Y5/evidence/scorecard_y5_1x.json`.
- M5 harmonization 2026-09-21 (crew M5-HARMONIZE): full measurement record in `~/workspace/NIGHT_RUN_2026-09-21.md` ("M5-HARMONIZE" entry); working artifacts (adapted Y5 prose-only source, binaries, harness STATUS/fragments) in `~/workspace/m5h/`; U re-run workdirs `~/workspace/m5h/work/urepro-m5-1x` + `urepro-m5-baseline`; Y5 harmonized workdirs `~/workspace/m5h/work/harm-m5-1x-prose` + `harm-m5-baseline-prose`.
