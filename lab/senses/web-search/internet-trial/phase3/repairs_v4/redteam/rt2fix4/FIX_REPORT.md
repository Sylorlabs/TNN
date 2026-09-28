# HELL-HOLE V4 — Round 4 Fix Report (r12_v4_t3)

**Date:** 2026-09-24
**Source:** `r12_v4_r4.zag` (SHA-256: `76bac95c72c7d44b51d95c39bcd2a4c5e51b945bb7fea825499088e05025b5ad`)
**Binary:** `r12_v4_t3` (SHA-256: `496c4c8226bd90bb6f00c0b3d0e2ce8677f1e542f0657dcbbb6d0cbf98775ffb`, measured on the shipped binary)
**Compiler:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
**Corpus:** `corpus_rtB.tsv` (SHA-256: `b52b5cd8787bdcff24ea6b78899d557e500e4f90ef7dec03b6ab79811c3b508a`), `corpus_rtA.tsv` (SHA-256: `63a4f700d5684b14d1e5294874d61e3c24ce9a5bf090d6e889ddb146025471f3`)

Scored by **oracle-match** (verdict tag vs corpus label), not verdict counts.

## Results

| Battery | Baseline (unmodified source, `r12_v4_t3_unmod`) | Fixed (`r12_v4_t3`) |
|---------|-----------------------------------------------|---------------------|
| RT-A (false affirms) | 0 affirms | 0 affirms |
| RT-B (oracle-correct /46) | 36/46 | **38/46** |

Baseline binary SHA `6d200c9e66ed6af687ece5e84142a184617fced4c6d6e2e86faba61986177980` is byte-identical to round 3's shipped `r12_v4_t2` — same source reproduces the same binary across separate builds.

**RT-B misses after fix (8, all documented architecture ceilings — still missing, no checkmarks):**
B16 (oracle AFFIRM, DENY neg-scope), B32 (oracle DENY, neutral), B34 (oracle DENY, AFFIRM endorse), B36 (oracle DENY, neutral gate), B37 (oracle DENY, neutral gate), B38 (oracle DENY, neutral), B39 (oracle DENY, neutral gate), B41 (oracle AFFIRM, neutral). Not touched, per task constraints.

**Fixed this round:**
- B17 "No student failed the exam" vs "Every student passed the exam, a one hundred percent pass rate." — was DENY (quantifier), now **AFFIRM** (endorse). Oracle AFFIRM ✓
- B45 "Unlike the claim, iron is magnetic" vs "Iron is strongly magnetic; copper, by contrast, is not magnetic at all." — was DENY (neg-scope), now **AFFIRM** (endorse). Oracle AFFIRM ✓

**Determinism:** 3/3 byte-identical runs on RT-A and RT-B.
- RT-B output SHA: `3954992f5a1bac2abce04dd45a925a2cfdb990c790c7c670afc67248c604ea26`
- RT-A output SHA: `3e7f2418e68fc03943484ebc4e7918054ce77386aa5d50eb3bfc5bbd36daf6c4` (identical to round 3's RT-A SHA — zero change on RT-A)

**RT4 r12-level probes:** R26 AFFIRM ✓, R27 AFFIRM ✓, R28 AFFIRM ✓, R42 DENY (neg-scope) ✓ — output byte-identical to baseline.

**Frozen v4 batteries:** all 8 `batt/corpus_*.tsv` outputs byte-identical to baseline (unchanged-or-better holds: zero diffs).
**v3 seeds:** `run_v3seed.tsv` (8 rows) byte-identical to baseline.
**382:** `reg382_input.tsv` → 59 processable rows, byte-identical to baseline (pre-existing: only 59/382 lines carry ≥4 fields).
**rt4_check.tsv, probe_num.tsv:** byte-identical to baseline.
**Pure Zag, zero RNG.** No external tools at runtime.

## Mechanism repairs (2)

### Fix 1 — B17: negated-universal + universal antonym-verb evidence → AFFIRM
**Root cause:** In `scan_text`'s B4-QUANT pair rules, `Qc==7 && Qe==1` unconditionally returned 9 (DENY, "quantifier") — "negative-universal claim vs existential evidence". But "Every student passed" is not an existential contradicting "No student failed": "No X V" ≡ "Every X not-V", and the evidence's verb is the antonym of the claim's verb, so the evidence asserts the claim's own content.
**Repair (general, no item string match):** new `neg_univ_verb_affirm()` helper — finds the claim verb with a `negverb_antonym` mapping (fail→pass, deny→grant, refus→accept, lose/lost→win, lack→have); requires the evidence clause to contain the claim's subject (subjA/firstA) and the antonym verb stem. Wired into the pair-rules block as AFFIRM (q0): banks `affB[0]=1` and suppresses the pair-DENY (`qaff==0` gate) plus the downstream deny-(b) for that clause. Fires only for Qc==7 (claim opens with no/none/neither) + Qe==1 (clause opens with all/every/each). B17 is the sole Qc==7 item in either corpus, so the blast radius on current corpora is exactly B17; the rule itself is fully general.
**Limitation (pre-existing, out of scope):** the stemmer does not normalize irregular verbs ("had"→"had" not "have", "won"→"won" not "win"), so synthetic variants like "None of the applicants lacked experience / Every applicant had experience" do not fire. Fixing the stemmer is a wider change with its own blast radius; not attempted.

### Fix 2 — B45: contrast-frame guard on neg-scope DENY
**Correction to the task's diagnosis (verified, not assumed):** the task stated `strip_meta_frame` "misses" the "Unlike the claim," form. A debug build printing the stripped claim proves it does NOT miss it: `strip_meta_frame("Unlike the claim, iron is magnetic")` → `"iron is magnetic"`. The actual defect: the evidence's second clause "copper, by contrast, is not magnetic at all" — the negation scopes a predicate of COPPER (explicitly contrast-marked as not-the-claim-subject), and deny-(b) fired a neg-scope DENY without subject alignment. Proven by probe: the frameless claim "iron is magnetic" against the same evidence also gave DENY (neg-scope) on the baseline.
**Repair (frame-stripper generalization, no B45 string match):** new `clause_contrast_frame()` helper generalizes the frame concept from claim-leading frames ("Unlike X,", "Contrary to X,") to clause-internal contrast frames ("by contrast", "in contrast"). In deny-(b): if the clause carries a contrast frame AND neither the claim subject nor first-anchor appears among the clause's content stems, the neg-scope DENY is suppressed (`cfr`). B16 ("Not all metals are magnetic" / "...copper, aluminum and gold are not" — no contrast frame) still DENYs; B35 (same-subject negation) still DENYs; RT-A A30/A35 (no contrast frames) still DENY.

## Regression probes (synthetic, not corpus)
- "iron is magnetic" vs full B45 evidence → AFFIRM (was DENY) — fix is not frame-dependent.
- "No dog barked loudly" vs "Every dog sat quietly" → neutral, unchanged (no antonym → rule correctly abstains).
- B35/B16 re-probes → DENY preserved. B45-with-frame and without → both AFFIRM.

## Honesty disclosures
- **B07/B08** (round 3's right-for-wrong-reason flag: possible deny-from-absence) — untouched, flag carried forward.
- **B34** flipped AFFIRM(endorse) in baseline and stays so; it is one of the 8 documented ceilings (universal + counterexample needs the proposition engine).
- **"curated-18 exact"** (prereg integration bar) — no artifact by that name exists in any authorized location checked (`redteam/rt2fix3`, `redteam/rt2`, `redteam/` root, local repo path `tnn-lab/docs/lab/senses/web-search/internet-trial/phase3/repairs_v4/` which is absent locally). Not verifiable from here; everything else on the gate list verified above.
- No item-specific string matches were added. Both repairs are general mechanisms.

## Binary hygiene
- `r12_v4_t3` is the versioned shipped build; `r12_v4_t3_unmod` (unmodified-source baseline, SHA = round 3's `r12_v4_t2`) retained for diffing. No outputs overwritten.
- **Not committed** per task constraints.
