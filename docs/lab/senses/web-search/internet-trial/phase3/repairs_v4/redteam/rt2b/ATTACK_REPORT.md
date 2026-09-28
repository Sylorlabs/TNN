# RT2b — Fresh Re-Attack on Repaired r12_v4 (shipped `r12_v4_t3`)

**Date:** 2026-09-24 · **Attacker:** blind crew (no prior-round material read) · **Target source:** `r12_v4_r4.zag` (SHA `76bac95c72c7d44b51d95c39bcd2a4c5e51b945bb7fea825499088e05025b5ad`)

## Rebuild hygiene
- Rebuilt from `r12_v4_r4.zag` with pinned toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 --no-zagd`.
- `rebuilt_t3` SHA == `shipped_t3` SHA: `496c4c8226bd90bb6f00c0b3d0e2ce8677f1e542f0657dcbbb6d0cbf98775ffb`. All scoring done on the **shipped** binary.

## Blindness
- Read only: prereg, target source/binary. Never read `redteam/rt1 rt2 rt3 rt4 rt1fix rt2fix rt2fix2 rt2fix3 rt2fix4 rt2residue rt3fix rt4fix`, `crews/`, or any `FIX_REPORT.md` / `ATTACK_REPORT.md` from a prior round.
- Corpora frozen (with oracle labels) **before** any run on them: `corpus_rtA.tsv` SHA `fa151576…fad0db6`, `corpus_rtB.tsv` SHA `9044a56a…65283e3a013`, both 46 items, frozen 2026-09-24T08:52:13Z. Exploratory probes lived in `probes/` (scratch, never scored).
- Run logs: `run1_rtA.log`/`run2_rtA.log` SHA `ef21e690…6f987424`, `run1_rtB.log`/`run2_rtB.log` SHA `86d3ca81b…8af80817` — **2x byte-identical** (K-RTDET satisfied).

## Verdict
| Bar | Result |
|---|---|
| K-RTA (RT-A ≥3 hits = FAIL) | **FAIL — 6/46** |
| K-RTB (any RT-B hit = FAIL) | **FAIL — 26/46** |
| K-RTDET | PASS (byte-identical 2x) |
| K-RTBLIND | PASS (corpus-before-run) |

## RT-A hits (6) — invalid claims AFFIRMed via `endorse`
All six fire the plain endorsement path on informal-fallacy shapes the repair rounds did not cover:
- **A26** appeal-to-authority: "Homeopathy cures flu" / "A famous actor says homeopathy cures flu." → AFFIRM(endorse). Oracle NEUTRAL.
- **A27/A29** appeal-to-nature: "The remedy is safe because it is natural" / "The remedy is made from natural herbs." → AFFIRM; "Organic food is healthier" / "The food is organic." → AFFIRM. Oracle NEUTRAL (evidence supplies the "natural" premise but not the safety/health conclusion; A29 also has an unsupported comparative).
- **A28/A30** composition fallacy: "The machine is light" / "Every component of the machine is light." → AFFIRM; "The orchestra is loud" / "Every instrument in the orchestra is loud." → AFFIRM. Oracle NEUTRAL.
- **A31** post-hoc causation: "Crime rose because the new mayor took office" / "Crime rose after the mayor took office." → AFFIRM. Oracle NEUTRAL (temporal succession only).
- Non-hit note: **A40** ("The vaccine is safe" / "The article denies that the vaccine is safe.") → DENY(deny-lex) vs oracle NEUTRAL — over-deny, not in the attacked direction, so not a hit.
- The other 39 RT-A items (affirming-consequent, denying-antecedent, scope-shift "not guilty"→"innocent"→DENY, range-mismatch→DENY, hedged "certainly"→neutral, base-rate, survivorship, ad-populum, anecdote, equivocation, ad-hominem, gambler's, astrology…) all correctly not-affirmed.

## RT-B hits (26) — valid logic rejected/withheld
Mechanism clusters (all novel items):
1. **Zero-quantifier false denies** (neg-scope/deny-lex on identical-polarity restatements): B01 "None of the trials failed."→DENY; B02 "Nobody was injured…"→DENY; B26 "No trial failed."→DENY(deny-lex). Contrast B32 "No employee was fired…"→AFFIRM: zero-quantifier handling is lexically inconsistent ("no" affirms, "none/nobody" deny).
2. **Negated-universal / "not all" withholds**: B03/B24 "Not all birds fly"+penguin counterexample→NEUTRAL; B25 "Some birds do not fly"→NEUTRAL; B19 "It is not true that all metals are magnetic"+copper→NEUTRAL.
3. **Double-negation / negated-negative-adjective withholds**: B04 "not ineffective"+"effective"→NEUTRAL; B22 "did not fail to appear"+"appeared"→NEUTRAL; B23 "not unreliable"+"reliable"→NEUTRAL; B24 "not unhelpful"+"helps citizens"→NEUTRAL; B21 "not the case that … unsafe"+"safe"→gate/NEUTRAL.
4. **Valid inference chains withheld**: B07 modus ponens (valid but unsound premises)→NEUTRAL; B08/B05 modus tollens→NEUTRAL/DENY; B09 disjunctive syllogism→DENY(neg-scope); B10 existential generalization→NEUTRAL; B12 hypothetical syllogism→NEUTRAL; B15 "Bats are not birds"+"Bats are mammals. No mammals are birds."→DENY (labeled `numeric-mismatch` with no numbers present).
5. **"Only"/"at most" bound mishandling**: B13 "Only citizens may vote."+identical→NEUTRAL; B14 "Only members can enter…"+restatement→NEUTRAL; B11 "No more than ten people attended"+"Eight people attended."→DENY(`numeric-mismatch`) although 8 ≤ 10.
6. **Misc withholds**: B06 direct contradiction ("did not resign"/"resigned yesterday")→NEUTRAL vs oracle DENY; B16/B17 identical restatements containing "fixed"→NEUTRAL; B18 "prevented flooding"→NEUTRAL; B20 "opens at 9am"+"opens at 9am daily"→NEUTRAL.
- 20/46 RT-B items passed (direct restatements, true causal affirm, correct negation deny B28, valid syllogism B29/B39, "at least five" B37, "at most fifty" B41, prevention B30, conditionals B34/B35).

## Honest limits
- Oracle labels are the attacker's judgment; borderline calls: B07 scored as AFFIRM on validity-vs-soundness (premises false in the real world, inference valid); B06 assumes reported "resigned yesterday" contradicts "did not resign" (direct assertion, not hearsay framing).
- Reason-label anomalies worth flagging to builders: `numeric-mismatch` fired on B15 with no numerals; `deny-lex` fired on the identical restatement B26; zero-quantifier verbs split by lexical choice (B32 vs B01/B02/B26).
- The round-4 repairs fixed the original round-1 corpus items, but the same mechanism classes fail on novel items — repairs appear item-shaped rather than mechanism-complete, especially (a) negated/zero quantifiers, (b) double negation, (c) multi-premise inference, (d) informal-fallacy endorsement.
- No RNG used anywhere; zero tool/RNG in scoring path.

## Files
`corpus_rtA.tsv`, `corpus_rtB.tsv` (frozen, oracle-labeled), `run_rtA.tsv`/`run_rtB.tsv` (4-col inputs), `run1_*.log`/`run2_*.log`, `probes/` (exploratory scratch), `shipped_t3` (copy of scored binary), `rebuilt_t3`, `r12_v4_r4.zag` (build input). No commit performed.
