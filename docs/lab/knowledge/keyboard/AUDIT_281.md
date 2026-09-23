# Keyboard-281 Audit: Is the QWERTY geometry genuine knowledge, and what exactly worsened 281 items?

**Date:** 2026-09-23
**Auditor:** keyboard-audit-281 crew (dispatched by Micah's order 2026-09-22)
**Scope:** `knowledge/keyboard/qwerty.zag`, the 281/20,031 battery items where geometry worsened the rank
**Method:** pure Zag (`audit281.zag`); Python used only as glue for tabulation. Zero RNG anywhere.

**Frozen inputs (all verified byte-identical to committed branch `tnn-native-lab` before analysis):**

| File | SHA-256 |
|---|---|
| `knowledge/keyboard/qwerty.zag` | `b9c57a83b709b4665524ad53d14a110b2fa8f7bd97de8d365deb29026deb309e` |
| `knowledge/keyboard/items.txt` | `c62b4150cd86a9702e3aae6dd4c216ae9af90986272eb0f5a4ec26b38b981ad7` |
| `knowledge/keyboard/words.txt` | `921db28f73143d7c0bfd1f30796a6007e0907f27b7813b123de6a0442d348153` |
| `knowledge/keyboard/gen_battery.py` | `42e3a2339c0f7f1e65e72901fc6319177f82d9cafbb79824c6ad87bbdae8a533` |

`qwerty.zag` was frozen **before** battery generation and execution (prereg record 2026-09-22). Nothing in this audit amends it.

## Verdict

1. **The coordinates are genuine knowledge.** Every one of 26 key centers matches a clean physical formula with zero per-key deviation; the row staggers (Q→A 0.25u, A→Z 0.50u) match real US-ANSI hardware derived from standard modifier widths (Tab 1.5u, Caps 1.75u, Shift 2.25u → alpha-key centers at exactly 8, 9, 11 quarter-units). Cost thresholds sit inside genuine gaps of the realized squared-distance spectrum — moving any threshold by ±1 changes nothing (verified: equivalents are 17–19, 42–51, 98–112; frozen choices 17, 45, 100 all lie strictly inside). Nothing was fitted per-key or per-pair.
2. **The 281 are fully classified, and none is a geometry error.** 281/281 have the ground-truth typo at the tier-20 ("near") substitution level; the battery itself generates these as truth via its own rule ("every neighbor with kb cost ≤ 20"). 214 are strict-cheaper keyboard-path competitors (56 tier-10 substitutions, 158 insertion/deletion/multi-edit paths cheaper than 20); 67 are alphabetical tie-breaks among keyboard-equal candidates. The blind baseline's "wins" on these items are alphabetical tie-break artifacts among blind-equal candidates, not discrimination.
3. **One systematic ranking flaw (not a knowledge flaw) is confirmed:** the tie-break by alphabetical word-list order has no epistemic basis. A principled secondary key (blind edit cost, then alphabetical) is **proposed and its test preregistered below — not implemented.**

---

## Part A — Coordinate / tier audit (all in Zag)

**A1 — formula audit: 0/26 mismatches.** For each letter the audit recomputed the center from the preregistered formulas (`q-row x=8+4i y=4`, `a-row x=9+4i y=8`, `z-row x=11+4i y=12`) and compared against the table in `qwerty.zag`. Zero deviations — no key was individually nudged, which is what battery-fitted hardcoding would look like.

**Physical grounding (independent of the repo):** standard US-ANSI hardware gives alpha-key centers at 2.00u / 2.25u / 2.75u from the left edge (from Tab 1.5u, Caps Lock 1.75u, left Shift 2.25u widths). In quarter-key units that is exactly 8, 9, 11 — the frozen formula — with 1u = 4 quarter-units per letter step. The knowledge's prose comment ("each row starts ~half a key right") is imprecise (the real encoded offsets are 0.25u and 0.50u); the numbers themselves are exact.

**A2 — threshold gap audit.** Realized squared distances by tier: tier-10 max 17, tier-20 min 20 / max 41, tier-30 min 52 / max 97, tier-40 min 113. The unreachable bands are d² ∈ {18,19}, {42…51}, {98…112}. The frozen thresholds (17, 45, 100) sit strictly inside these bands: **no pair's tier assignment changes if any threshold moves by ±1.** The tiers are not knife-edged; they cannot have been fitted pair-by-pair.

**A3 — physical-neighbor audit.** 32 undirected pairs sit at tier 10, and all 32 have d² ∈ {16,17} (horizontal neighbor or stagger-diagonal neighbor — every physical king-move at minimum distance). All 110 directed physically-touching key pairs are tier ≤ 20 (64 at tier 10, 46 at tier 20); **zero touching pairs are called "far" (tier 30+).** The 23 undirected touching-but-tier-20 pairs are the broader diagonal neighborhood (d² ∈ {20,25,32}) — coarser than physics but distance-ordered, never inverted.

**A4 — documented probes: 10/10 pass.** The prereg's 10 worked examples (e↔r 10, t↔y 10, q↔a 20, e↔d 10, a↔s 10, z↔x 10, e↔w 25, t↔g 32, q↔z 65, a↔p 100) all reproduce.

**On the tier values (10/20/30/40) and indel/transposition costs:** these are round, pre-frozen prior choices, not fitted — the only pre-freeze evidence was a 4-item smoke test, too small to fit 7 parameters. They encode the ordinal claim "adjacent slip (10) < dropped/duplicated key (15) < near slip (20)", with far slips (30/40) progressively penalized. The values matter beyond pure ordering (e.g. tier-20 sub 20 vs del+ins 30 determines alignments), and no real typing data calibrated the ratios — that is a named residual, not hardcoding. Hardcoding would have shown up as per-key/per-pair deviations (ruled out by A1) or knife-edge thresholds (ruled out by A2).

## Part B — The 281, classified (all in Zag, replay-verified)

Pass 1 of `audit281.zag` independently replayed the ranking on all 20,031 items with a from-scratch DP (392 candidates, blind and keyboard costs, same tie-break) and matched `results.txt` exactly: **improved 3,553 / worsened 281 / unchanged 16,197 / collisions 50** — all four numbers reproduce the verdict doc. **Replay mismatches: 0.**

Pass 2 classified every worsened item by finding each KB-only competitor above the truth and labeling strict-cheaper vs equal-cost-alphabetical, with collision and replay-ok flags. Full row-level data: `knowledge/keyboard/audit281_detail.txt` (281 rows + header). **Replay_ok = 1 on all 281 rows. Anomalies (no KB-only cause): 0. Truth not in word list: 0.**

| Class | Count | Meaning |
|---|---|---|
| STRICT | 214 | A competitor has strictly cheaper KB cost than the truth |
| └─ via tier-10 substitution | 56 | Competitor is a genuine physical neighbor (all d²∈{16,17}) |
| └─ via insertion/deletion/multi-edit | 158 | Competitor path (e.g. insertion 15) beats the truth's 20 |
| TIE | 67 | Competitor ties the truth's KB cost; alphabetical order picks it |
| Collision-context | 5 | Typed string is itself a dictionary word (overlaps the above; same mechanism) |
| Kind breakdown | 281 S1 / 0 S2 / 0 RW | All worsened items are single-substitution typos |

**The single dominant fact: 281/281 worsened items have the truth's true substitution at tier 20 ("near": d² ∈ {20,25,32,41}). Zero have truth tier 10.**

Representative rows (typed → truth | KB's pick | mechanism):

- STRICT/sub: `wnd → and` → KB picks `end` (w>e d²=16, tier 10) vs truth (w>a d²=25, tier 20). `bfing → being` → `bring` (f>r d²=17). `gook → book` → `took` (g>t d²=17).
- STRICT/indel: `atter → after` → `matter` (dropped-m insertion, 15 < 20). `arain → again` → `rain` (dropped-a, 15 < 20). `aid → air` → `said` (15 < 20).
- TIE: `coke → come` ties `cold` at KB 20 (alphabetical picks `cold`). `eah → eat` ties `day`. `vood → food` ties `cold`.
- Collision: `way → day` — "way" itself is a word (KB cost 0); the worsening comes from `say` (w>s tier 10) outranking the truth (w>d tier 20).

**Why the blind baseline "wins" these:** under blind scoring the truth and the tier-10 competitor both cost 10 (single substitution), and truth wins only by being alphabetically earlier; in TIE items the competitor costs strictly more under blind, so blind ranks truth better. In both cases the blind advantage is the alphabetical tie-break, not better discrimination. Geometry's answer — "the tier-10 competitor is the likelier reading" — is the honest Bayesian answer under the frozen prior; whether it is empirically right depends on real near-vs-adjacent slip base rates, which neither method knows (no frequency priors in the knowledge — a named residual boundary).

**Battery-design caveat (material to the "hardcoded" question):** the S1 battery's corruption model uses the knowledge's own table — it generates ground-truth typos as "every neighbor with kb cost ≤ 20", i.e. the battery deliberately includes tier-20 slips as truth while the frozen prior prices them at 20. This is disclosed in the prereg, but it means S1 is partially a home game: it cannot test whether KB over-penalizes far slips, and it overgenerates tier-20 truths relative to the prior. The knowledge-independent, hand-authored RW battery is the neutral corroboration: +2.99pp with **0** worsened. The 281 are the measurable price of the frozen prior on single-substitution items — fully characterized, not a defect.

## Systematic flaw found: the alphabetical tie-break

On the 67 TIE items, keyboard geometry is genuinely indifferent (equal cost) and the alphabetical word-list order decides. Alphabetical order has no epistemic basis as a typo-likelihood prior. Verified in the classifier: every TIE competitor has blind edit cost strictly greater than the truth's (truth = 10, competitor > 10 — otherwise it would also outrank truth under blind). So a secondary tie-break of **blind edit cost, then alphabetical** would recover all 67 without touching any strict-cost decision.

### Preregistered test (PROPOSED — not implemented, no code changed)

- **Hypothesis:** adding blind-edit-cost as the secondary tie-break (after KB cost, before alphabetical) recovers the 67 TIE worsened items without reducing the improved count, net ≥ 0 on a fresh battery.
- **Test:** implement in a copy of the runner; run on a **fresh battery** (new seed-free generation from `gen_battery.py` logic, or the hand-authored RW set extended) — not the frozen 20,031, to avoid fitting to these 281. Report improved/worsened/unchanged deltas vs blind on the fresh battery; pass bar: worsened decreases by ≥ 50% of the TIE count with no net improved-count regression.
- **Kill bar:** if any improved item flips to worsened on the fresh battery, the change is rejected (tie-breaks must not trade improvements for ties).
- **Note:** the STRICT 214 are untouched by any tie-break change; recovering them would require recalibrating the tier-20 vs insertion cost ratio against **real typing data** — future work needing new data, not a code tweak.

## Reproducibility

`audit281.zag` (Part A + Part B) compiles with `toolchain/bin/znc_linux_x86_64_abed8aa1` and runs deterministically: two runs produce byte-identical `audit281_detail.txt` (verify: `sha256sum` across runs). Part A prints its audit lines to stdout; Part B writes the TSV. Zero randomness anywhere (no RNG primitives in the program; verified by inspection).

## Residuals (not flaws)

- Tier ratios (10/15/20/30/40) are round pre-frozen choices, uncalibrated by real typing data. Empirical calibration is the correct next step for the STRICT-214 class and needs new data.
- No word-frequency or sentence-context priors: "atter → matter" is a legitimate geometric reading; only frequency/context disambiguates. Named in the verdict doc; out of scope for this audit.
- The doc prose ("each row starts ~half a key right") is imprecise vs the encoded 0.25u/0.50u staggers; numbers are exact, prose should be corrected in a doc-only edit.
