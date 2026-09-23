# Doc-sweep amendment red-team verification — 2026-09-22

**Commissioned by:** Micah ("Red team check and verify first" — signs only VERIFIED amendments)
**Scope:** prose-v3 (K18, K19, N9) · dialogue (N14, K17) · Track A three sign-offs
**Method:** read-only against frozen sources; independent recomputation where a number is cited; cited commits re-verified through the GitHub API on 2026-09-22.
**Rule applied:** exactly one verdict per amendment/sign-off — VERIFIED / REJECTED (exact failure) / NEEDS-REWORDING (exact replacement).

## Frozen sources and commit provenance (re-verified 2026-09-22)

| Source | Commit / blob |
|---|---|
| `units/PREREG_FREEZE.md` (signed 2026-09-21) | `b0b9140c0eda` — "units: PREREG_FREEZE signed and FROZEN by Micah 2026-09-21" |
| B-family verdict | `59fb89777f3f` — "Track A closeout: B-family verdict (B-8/B-16/B-64), r1 1x" |
| Proposed bars + these amendments | `abaa5c7b57b6` — red-team bar-sensitivity audit and proposed bars |
| Branch head at check time | `cf9f46b859fe09b1e38115f39a424e0f3136b092` (recheck before use) |

Proposal files checked byte-identical against the branch versions:

| File | Git blob SHA |
|---|---|
| `docs/lab/redteam/bar-audit/PROPOSED_BARS.md` | `eb7f81bf5551976018e88dcb3957b163facdb77a` |
| `docs/lab/tracka-closeout/signoff/a_metric_count.md` | `48e477671451cc4f168456f0953f692e4bdfaa14` |
| `docs/lab/tracka-closeout/signoff/b_bfamily_killbar.md` | `fa84868e46809d2061f16e40e557d5e32abde42f` |
| `docs/lab/tracka-closeout/signoff/c_m5_binding.md` | `5047d5e27d1bc3ddbc024befdc37a173d5c6a78c` |

## Verdict table

| # | Amendment | Verdict |
|---|---|---|
| K18 | Keep KB3-VIABLE conjunctive; forbid VIABLE(FAIL)+RETAIN(PASS) split | **VERIFIED** |
| K19 | v3 legs byte-match; frozen-binary baseline legs get documented tolerance; A0 exemption explicit | **VERIFIED** (with confinement caveat — §K19) |
| N9 | Tier-3-introduced wrong-value rate ≤2% on the clean set | **NEEDS-REWORDING** (§N9 fix) |
| N14 | COMPOSE-NOVEL verified by the oracle independently, not asserted by the binary | **VERIFIED** (recommend explicit trip condition — §N14) |
| K17 | Promote KB-DLG-COMPOSE to kill bar ≥24/28 with independent oracle novelty verification | **NEEDS-REWORDING** (§K17 fix) |
| A | Track A metric-count interpretation (R1: M1-content, M1-boundary, M2, M3, M4, M5, M6-transfer-tax, M7) | **VERIFIED** |
| B | B-family ≥2×-on-M3 kill-bar wording resolution (B1 / B2 / stands) | **NEEDS-REWORDING** (§B fix; B2 option only) |
| C | M5-as-binding kill bar, scope (a)/(b)/(c) | **NEEDS-REWORDING** (§C fix; bar-(ii) death-toll count) |

Nothing in the set is REJECTED. No amendment was found to be a disguised weakening; where a draft would kill arms, it discloses the kill list.

---

## K18 — VERIFIED

**Claim:** PREREG3 §6 defines KB3-VIABLE as a conjunction (beats v1 on ≥3/4 sources AND retains v2 capability wins); no KB3-RETAIN bar exists in the prereg; VERDICT.md lists a separate KB3-RETAIN PASS row that softens the VIABLE FAIL (2/4). K18 forbids the split.

**Trace:**
- PREREG3.md §6 (lines 117–121): "**KB3-VIABLE**: A3 beats v1's clean mastery on ≥3/4 sources AND retains all v2 capability wins (CONTR 24/24, HEDGE zero leaks, NEG zero leaks on the rebuilt battery, MULTI 24/24, dense PARA 48/48 on v2's battery)." `KB3-RETAIN` appears only in VERDICT.md, never in PREREG3.md (grep-confirmed).
- VERDICT.md §1: KB3-VIABLE = **FAIL — 2/4** (beats v1 on step, muse-native; loses on grok, sol); KB3-RETAIN = **PASS** (CONTR 24/24, HEDGE zero leaks, NEG zero negated-value returns, MULTI 24/24, PARA 48/48, asserted 12/12 both). The VIABLE row's criterion column quotes only the first conjunct, dropping the retention conjunct — consistent with the "softens the FAIL" charge.
- 2/4 cross-checked: A3 vs v1 = grok 183 vs 189 (−6), sol 204 vs 220 (−16), step 208 vs 204 (+4), muse-native 227 vs 200 (+27) → 2/4 ✓. §9 decision record: "KB3-VIABLE FAILS (2/4). v3 does not ship as the prose path; v1 stays pinned."

**Red team:** no hidden weakening (K18 tightens presentation discipline; it cannot rescue a FAIL), no kill criterion relaxed, no contradicting datum.

## K19 — VERIFIED (with confinement caveat)

**Claim:** PREREG3's oracle bar ("independent oracle must reproduce every leg's log byte-identically", PREREG3.md §5 lines 112–113) literally tripped at 26/28 sub-battery; the VERDICT PASS rests on the documented A0 exemption for the 2 id-17 v2-binary-vs-oracle misses (§11).

**Trace:**
- VERDICT.md §1 line 14: "**PASS with documented A0 exemption** — 16/16 championship, 26/28 sub-battery (2 misses = documented v2-binary id-17 deviation, §11)"; §§8, 10 repeat 16/16 + 26/28.
- VERDICT.md §11 root cause: unpreregistered coref-trigger expansion — v3 fires on `it/its/this/that/these/those` + bigrams vs v2's `it/this/that`; "v3 m0 ≠ v2 binary on exactly one scored sentence (sub_core id 17 sent=1; 14/15 input classes identical). **No scored result is affected** — A0/A1 ran the frozen v2 binary, never v3 m0."
- `run_legs.sh` (lines 10–11): A0 and A1 both run `BIN=../v2/src/prose_learn2` — the frozen v2 binary. So "frozen-binary baseline legs" (plural, K19's wording) is exactly right; all v3-implementation legs (A2/A3) byte-match.

**Red team:** scope narrowing, not hidden weakening — the oracle is an oracle for **v3**, not for the frozen v2 binary; holding v2 byte-identical against a v3 oracle is a category error, and v2 has its own verification history. The tested artifact keeps the strict bar.

**Caveat (confinement):** K19 introduces a general "documented tolerance" mechanism. Its wording confines it to frozen-binary baseline legs and demands it be explicit, not folded into PASS. Micah should keep that confinement: this mechanism must not become a general license to document-away tripped bars on implementation legs. With that understanding, VERIFIED.

## N9 — NEEDS-REWORDING

**Numbers recomputed from frozen run logs (rep1), all check:** A1/A2 clean=912, wrong-value=8; A3 clean=912, wrong-value=30; unknown/other 523 → 60 (≈463 converted ✓). 8/912 = 0.8772% → 0.9% ✓; 30/912 = 3.2895% → 3.29% ✓; tier-3-attributable Δ = 22/912 = **2.4123%**. Attribution is solid: C2 (A1→A2) changed exactly zero wrong-values (8→8), so the full +22 is C4/tier-3. "Clean set" = 912 = 4 sources × 228 (12 planted-falsehood probes excluded per §2) ✓. BAR_AUDIT.md H8 confirms the HONEST-FAIL characterization. No weakening — it is a new bar on an unbarred result; it tightens.

**Two defects:**

1. **Metric ambiguity.** "Tier-3-introduced wrong-value rate" most naturally reads as the *delta* attributable to tier-3 (22/912 = **2.41%**), but the doc-sweep caveat evaluates N9 using the *total* rate (30/912 = **3.29%**). Both honest-fail at ≤2% and pass at ≤5%, so the practical claim survives — but a signed bar must pin which one, because future legs can have a different baseline.
2. **The ≤2% threshold is a judgment call, not evidence-derived.** PROPOSED_BARS.md's own header promises "measured margins minus a stated safety factor — not round numbers," yet 2% is a round number with no margin derivation. Measured: introduced 2.41%, total 3.29%.

**§N9 fix (exact replacement):** "Tier-3-attributable Δwrong-value rate = (wrong-value_A_tier3 − wrong-value_A_baseline) / clean probes ≤ 2% on the clean set (912). Measured 22/912 = 2.41% → honest-fail at ≤2%, passes at ≤5%. Threshold is a judgment-call target (requires the precision price cut from 2.41% to ≤2.00%), not a measured margin."

*Minor doc-sweep flag (not N9-blocking):* §2.2's parenthetical "(≈3.6% error on tier-3-resolved probes)" does not recompute — 22/463 = 4.75%.

## N14 — VERIFIED (recommend explicit trip condition)

**Claim:** COMPOSE-NOVEL is self-attested; the independent oracle consumes the binary's flag and does not independently verify novelty.

**Trace:**
- PREREG.md novelty control (lines 116–119, verbatim): "**Novelty control**: the binary asserts the compose response is not a substring of any KB fact text or any prior turn text, and prints `COMPOSE-NOVEL=1` per compose turn." → the prereg itself **encodes self-attestation**; the binary does exactly what was asked.
- dialogue.zag:1498–1522 (`fn novelty_ok`): scans all KB fact texts and all prior-turn history rows for the response as a substring; emission at :1861–1870 prints the flag.
- verify_dialogue.py: `parse_log` captures the flag verbatim (`novel = line.startswith('NOVEL=1')`); §5 "Composition novelty check" is **gated on `r['novel']`** and checks only verbatim full-text membership against KB facts — it never recomputes substring non-membership, and never checks prior turns. A lying binary printing `NOVEL=1` on a response that is merely a *substring* of a KB fact (e.g. `1889`) would pass the oracle today. Live run of the frozen oracle on `run_det_1.log` confirms: `CP-01 turn 3: NOVEL=1, output not in KB ✓ ('yes.')` … 10/10.
- Measured: 10/10 composition-response turns carry `NOVEL=1` in all 5 det logs; oracle reports 0 errors.

**Red team:** not a hidden weakening — it adds a requirement. Implementable and non-vacuous: the oracle already has all inputs (KB facts from `kb.txt`, user turns from `battery.txt`, TNN outputs from the log's `A` lines) to lowercase-substring-check each composition response against all KB facts + all prior turns. The check can genuinely fail (substring-but-not-verbatim case), so it is a real gate, not theatre. No trial datum contradicts the wording.

**§N14 recommendation (not a rejection):** state the trip condition explicitly. Suggested: "the oracle recomputes novelty for every composition-response turn (response not a substring of any KB fact text or any prior turn text, lowercased) without consuming the binary's flag; any composition-response turn the oracle cannot confirm novel trips KB-DLG-COMPOSE." Minor precision nit: the wire token is `NOVEL=1 `, not `COMPOSE-NOVEL=1`; the flag appears on the 10 composition-response turns, not all 28 compose turns.

## K17 — NEEDS-REWORDING

PREREG.md confirmed: "**KB-DLG-COMPOSE** (measurement): report compose success rate and the novelty-control result. If compose is 0% and analysis shows repeat-only behavior, the verdict states that plainly — a finding, not a hidden failure." → measurement-only, no threshold; the "measurement" characterization is exact. Measured: 28/28 = 100% (8 dialogues × 3 turns + CP-09/CP-10 × 2 turns, from battery.txt and run_det_1.log). 24 = 28 − 4-turn slack (scratch/worker_C.md:131).

**Two defects:**

1. **Denominator ambiguity (substantive).** "≥24/28 with independent oracle novelty verification" can be read as requiring ≥24 of 28 turns to be *oracle-verified novel* — impossible by construction: 18 of the 28 turns are setup/retrieval turns whose battery expectations are verbatim KB facts (e.g. CP-01 turn 1: `Herman Melville wrote the novel Moby Dick.`). Only the 10 composition-response turns (8× turn 3, CP-09/CP-10 turn 2) are novelty candidates. A signed kill bar that can be read this way is unadjudicable.
2. **Unstated safety factor.** The 4-turn slack is the proposal's loosest count-bar (14.3pp vs the measured−1/−2 pattern at comparable n: K2 ≥23/24, K11 ≥23/24, C6 ≥10/12) and its rationale is not stated in the row — worker_C.md just writes "measured−4 turns".

**§K17 fix (exact replacement):** "**KB-DLG-COMPOSE (kill bar):** compose turn-correctness **≥24/28** (measured 28/28; 4-turn slack — tighten to ≥26/28 to match the C6/K2 slack pattern, or state the rationale for 4), **AND** every composition-response turn (the 10 final turns of the COMPOSE dialogues) independently oracle-confirmed novel per N14; any turn the oracle cannot confirm novel counts as a compose failure against the bar."

*Dependency note:* K17's "with independent oracle novelty verification" textually invokes N14; both apply "for the next prereg round" on signature, so the oracle upgrade is a next-round sequencing requirement, not a contradiction.

## Track A sign-off (A) — VERIFIED

**Claim:** §7 rules 2 and 4 are arithmetically incoherent unless "8 scored metrics" = {M1-content, M1-boundary, M2, M3, M4, M5, M6-transfer-tax, M7} (R1); the amendment adopts R1 explicitly, changes no verdict.

**Trace (all quotes verified against frozen `units/PREREG_FREEZE.md`):**
- §7 rule 2 (line 842): "≥ 6 of the **8 scored metrics** (M1–M7 scored; M8 is eligibility only; M9 informational, never counts)" — the parenthetical names 7 metric numbers while the head count says 8.
- §7 rule 4 (lines 846–847): "N/A metrics excluded from numerator and denominator — threshold is ≥ 6 of *applicable* scored metrics, or ≥ 75% of applicable rounded up, whichever is larger (an arm with M7 N/A needs ≥ 6 of 7)."
- §5 M1 (line 735): M1's two sub-scores "recorded separately, never folded" — kills R2/R3. §5 M6 (line 780): "P→C and C→P are separate scorecard columns — never averaged … champion = smallest transfer tax" (one champion — kills R3). M-28, M-33, M-40 corroborate.
- Coherence check: R1 satisfies all three (8 columns; M7 N/A → 8−1=7 applicable, max(6, ⌈5.25⌉=6) = 6/7 ✓); R2 fails rule 2's head count (7 ≠ 8); R3 violates §5 text (folded M1, split M6). The signoff's "only reading" claim is correct.
- TRACKA_VERDICT_SHEET.md already uses R1: §3 line 80 ("Scored columns (8): M1-content, M1-boundary, M2, M3, M4, M5, M6-transfer-tax, M7"), line 97 (Y5 7/8 · L1 1/8), line 136 ("Adopted as interpretation; needs Micah's sign-off as a counting-rule change").
- Outcome-neutral confirmed: under R1, Y5 = 7/8 (M1-content, M1-boundary, M2, M3, M4, M6-tax, M7) ≥ 6 ✓; under R2, Y5 = 6/7 (M1 folded, M5 to L1) ≥ 6 ✓ — same verdict.

**Red team:** pure clarification, no numeric change, no verdict change, no weakening in disguise. §13's amendment procedure (line 1014: any change to verdict rules needs a dated amendment with Micah's re-approval; history stands, amendment appends) correctly governs it.

*Minor citation nit:* the signoff's Evidence refs cite `docs/lab/units/PREREG_FREEZE.md`; no such file exists — the canonical frozen file is `units/PREREG_FREEZE.md`. Amendment sentence itself is fine.

## Track A sign-off (B) — NEEDS-REWORDING (B2 option only)

**Frozen wording verified** (units/arms B-family verdict + PREREG_FREEZE.md §3, via `docs/lab/units/arms/B-8/VERDICT.md`): "B as a family is killed as contender the moment any smart arm beats the best B size by ≥2x on M3 at equal-or-better M1." M3 is a survival rate bounded at [0,100] (§5 line 750–753: "M1 recall on V: survival rate. Bars: ≥ 90%; champion ≥ 95%"). The B-family verdict (commit `59fb89777f3f`, §5) correctly concluded: "A ≥2x beat on M3 requires M3 ≥ 200.0 … arithmetically unreachable while any B size holds the ceiling → The family-kill bar does NOT fire. The B family SURVIVES as a contender (B-16, B-64)" (B-8 retired). Its flag — "the bar can only fire after a B size first drops below 50% on M3" — is arithmetically correct (2×B ≤ 100 ⇒ B ≤ 50).

**B1 option verified:** best B M3 = 100.0 (B-16 scorecard), max smart M3 = 100.0 (Y5: 100.0/CLEAR from `evidence__scorecard_y5_1x.json`) → margin 0 < 10 absolute points → does NOT fire. Correct, and fireable on real regression (a B size dropping to ≤ 90.0 with a smart arm ≥ 10 points ahead at matched M1).

**The B2 option has a factual error in its computed outcome.** The doc claims: "Y5: M3 100.0/CLEAR, M1 100/100, M5 1.498 → 1.719/1.498 = 1.147× < 2× → does not fire. L1: … M3 = 0 … does NOT fire. **No other arm is within 2× on cost at matched M3/M1 → bar does NOT fire today.**"

That last sentence is false. **R2 satisfies B2 literally:** M3 = 100.0/CLEAR, M1 = 100.0/100.0 on both corpora (prose and code), M5 = 0.844 B/B → 1.719/0.844 = **2.037× ≥ 2×** (from `docs/lab/tracka-closeout/scorecards/R2/scorecard_r2_r1.json`). R2 is KILLED (disjunct a: margin 0.0 < 3 vs R — "dead on the ceiling technicality", TRACKA_VERDICT_SHEET.md lines 54, 127), but its measurements are committed Grade-A evidence. Under B2 as literally written, the bar would fire **today on a dead arm's numbers** — killing the B family on the strength of a corpse. That contradicts the doc's own "does NOT fire today" and is plainly not the bar's intent (kill bars adjudicate contenders).

**§B fix (exact replacement for the B2 option):** scope B2 to live contenders and disclose R2:

> **Option B2 — cost-axis rewrite (reworded):** "B as a family is killed as contender the moment any **non-disqualified** smart arm matches-or-beats the best B size on M3 (≥ best-B M3, freeze CLEAR), at equal-or-better M1 (content and boundary, both corpora), **and** beats the best B size by ≥ 2× on M5 per-byte memory cost." Computed outcome: Y5 1.147× → no; L1 M3 = 0 → no; **R2 (KILLED) would satisfy it (2.037× at matched M3/M1) but is excluded as disqualified** → bar does NOT fire today; B family still survives. NOTE: B2 changes the axis from survival to cost — it is a new bar, not a clarification of the old one.

The "stands as written" and B1 options need no change. **Structural note for Micah:** this signoff is an analysis with options, not a single signable amendment — it becomes signable only when he selects one of {B1, B2, stands}. Signing "stands" keeps the unreachable bar and the B family's contender status exactly as the frozen verdict recorded.

## Track A sign-off (C) — NEEDS-REWORDING (bar-(ii) death-toll count)

**Frozen-status claims verified:** M5 appears in **zero** program-level kill bars (§8) and **zero** arm kill criteria (§3) — it is today a scorecard metric with bars, not a kill bar. M-22–M-26 frozen text verified (M-23 per-source-byte comparison column; M-24 ≤ 1.5×; M-25 ≤ 10 audit entries per KB learned). M-57 verified as an unresolved disjunction: "M5 entry-count bars AND R4 byte bars — approve 'both-must-hold' or a unified bar (resolves the R4/M5 contradiction)." The draft's "both-must-hold iff scope (c), else the selected single bar" correctly resolves it. Grade-A/B-only killing (§3a/§3b, Z6 footnote) is internally consistent with the draft's evidence rule.

**All spot checks against committed scorecards match:**

| Arm | M5 B/B (bar i) | aud/KB (bar ii) | Doc claim | Check |
|---|---|---|---|---|
| Y5 | 1.498 PASS | 5.015 PASS | passes both, only joint survivor | ✓ |
| L1 | 0.839 PASS | 16.001 FAIL | (i) lives, (ii) dies | ✓ |
| B-16 | 3.626 FAIL | 64.189 FAIL | dies under (i) | ✓ |
| H1 | 2.412 FAIL | 8.326 PASS | (i) dies, (ii) lives | ✓ |
| X | 2.002 FAIL | 0.188 PASS | (i) dies, (ii) lives | ✓ |
| C-W | 16.481 FAIL | 364.066 FAIL | dies | ✓ |
| B-64 | 1.719 FAIL | 16.189 FAIL | dies (B-family verdict §3 evidence table) | ✓ |
| U | 2.902 (prose-only, M5-HARMONIZE) | — | would fail (i) | ✓ (TRACKA_VERDICT_SHEET.md line 8) |

§3a death toll verified: 17 `**YES**` rows = 15 PASS + Y4 (provisional) + Z6 (Grade C) ✓. Joint survivors under both-must-hold: Y5 alone ✓ (L1 fails (ii); C-P/H1/X fail (i)).

**The defect — §3b death toll is miscounted.** The doc says: "Bar (ii) death toll: **12 PASS arms + Y4/Z1 (provisional) — 14 arms**." The table's `**YES**` rows are exactly **13**: 11 PASS arms (A, B-16, B-64, C-W, K2, L1, L2, S, Y3, Y6, Z2) + 2 provisional (Y4, Z1). The headline overcounts by one PASS arm. The per-arm table is the operative part of the amendment ("the arms marked 'Would die? YES' … are KILLED"), and the table itself is correct — only the headline number is wrong.

**§C fix (exact replacement):** in `c_m5_binding.md`, change the bar-(ii) headline to "Bar (ii) death toll: **11 PASS arms + Y4/Z1 (provisional) — 13 arms**."

**Red team (substantive, for Micah's decision — not a verification failure):** (c) is a massive *strengthening*, not a weakening: scope (a) kills 17 arms including B-16/B-64, which the frozen §3 bar deliberately keeps alive as contenders, and it kills 15 PASS arms on a metric that was explicitly non-binding when they ran. The doc discloses this prominently ("far tighter than the battery's reality"; "killing the B family the frozen bar keeps alive"). The kill-on-signature clause ("KILLED under §0 RULE-7 with no appeal") is consistent with RULE-7's binding bars but is stronger than the normal process in one respect: it fires on *past* measurements rather than a new leg. All three scopes plus "M5 stays non-binding; no amendment" are presented as complete sign-offs, so the choice is genuinely his.

---

## Cross-cutting red-team notes

1. **No amendment in the set is a disguised weakening.** The failure mode present is the opposite: (C) is a disclosed mass-kill, and (B2)/(K17) had underspecified live-scopes/denominators that would have made kill bars fire perversely or be unadjudicable.
2. **Signoff (B) and (C) are not single signable amendments as written** — they present options for Micah to select. They become signable only after he picks one branch each; the "stands"/"stays non-binding" options are equally complete.
3. **Suggested signable set, post-fix:** K18, K19 (with confinement understood), N14 (with trip condition), N9 (fixed), K17 (fixed), A, B (one selected option; B2 fixed), C (one selected scope; count fixed).

*Report: red-team verification crew, 2026-09-22. Two independent verifier subagents (prose-v3, dialogue) contributed evidence; all of their cited numbers were re-verified or re-derived here before adoption.*
