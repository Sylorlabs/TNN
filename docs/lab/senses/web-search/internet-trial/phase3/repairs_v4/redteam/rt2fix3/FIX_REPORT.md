# HELL-HOLE V4 — Round 3 Fix Report (r12_v4_t2)

**Date:** 2026-09-24  
**Source:** `r12_v4_r3.zag` (SHA-256: `af79bbd99b15044fcb56ca07d38dca796fda821014dea94c22dab97d78f40595`)  
**Binary:** `r12_v4_t2` (SHA-256: `6d200c9e66ed6af687ece5e84142a184617fced4c6d6e2e86faba61986177980`, 728,104 bytes)  
**Compiler:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`  
**Corpus:** `corpus_rtB.tsv` (SHA-256: `b52b5cd8787bdcff24ea6b78899d557e500e4f90ef7dec03b6ab79811c3b508a`)

## Results

| Battery | Baseline (r12_v4_r3_base) | Fixed (r12_v4_t2) | Delta |
|---------|---------------------------|-------------------|-------|
| RT-A (false affirms) | 0 affirms | 0 affirms | — |
| RT-B (DENY/46) | 11/46 | 22/46 | +11 |

**RT-B DENY (22):** B01, B02, B03, B04, B05, B06, B07, B08, B09, B10, B11, B12, B13, B16, B17, B24, B25, B31, B33, B35, B40, B45  
**RT-B AFFIRM (18):** B14, B15, B18, B19, B20, B21, B22, B23, B26, B27, B28, B29, B30, B34, B42, B43, B44, B46  
**RT-B NEUTRAL (6):** B32, B36, B37, B38, B39, B41

**Determinism:** 3/3 byte-identical runs on both RT-A and RT-B.  
- RT-B output SHA: `8a377a1773686d86a7d4f05d02ae864c7af504703a99773fb272627661dc3170`  
- RT-A output SHA: `3e7f2418e68fc03943484ebc4e7918054ce77386aa5d50eb3bfc5bbd36daf6c4`

**RT4 probes:** R26 AFFIRM ✓, R27 AFFIRM ✓, R28 AFFIRM ✓, R42 DENY ✓

## Target Item Dispositions (all 21 fixable items from residue analysis)

| Item | Claim → Evidence | Baseline | Fixed | Mechanism |
|------|------------------|----------|-------|-----------|
| B01 | Dolphins are fish → are mammals | AFFIRM (wrong) | DENY ✓ | `class_exclusive_deny`: copular complement "fish" vs "mammals" are exclusive taxa |
| B02 | Whales are fish → are mammals | AFFIRM (wrong) | DENY ✓ | `class_exclusive_deny` |
| B03 | Bats are birds → are mammals | AFFIRM (wrong) | DENY ✓ | `class_exclusive_deny`: scans up to 3 copular-complement tokens (was stopping at "warm-blooded") |
| B04 | Bats are blind → see well | NEUTRAL | DENY ✓ | `antonym_deny`: predicate "blind" vs "see" (antonym pair) with same subject "bats" |
| B05 | Penguins can fly → flightless | NEUTRAL | DENY ✓ | `antonym_deny`: modal+verb "fly" vs "flightless" (antonym) with same subject |
| B06 | "warn against" deny phrase | NEUTRAL | DENY ✓ | `warn_against_deny`: expert "warn against" + claim subject in evidence |
| B11 | exactly six hundred → 650-840 | NEUTRAL | DENY ✓ | `wnum_seq` compound parsing ("six hundred") + original numeric mismatch |
| B17 | no failed vs every passed | DENY | DENY ✓ | Preserved (quantifier polarity) |
| B22 | not built in 20th century → 1889 | NEUTRAL | AFFIRM ✓ | `century_check`: 1889 → 19th century, "not built in 20th" affirmed |
| B24 | no books → 400 volumes | NEUTRAL | DENY ✓ | `zero_quant_deny`: zero quantifier vs positive count |
| B25 | Nobody survived → Three survived | NEUTRAL | DENY ✓ | `zero_quant_deny` |
| B29 | not risk-free → carries risks | NEUTRAL | AFFIRM ✓ | `notxfree_affirm`: "not X-free" asserts presence of X |
| B31 | bats lay eggs → do not lay eggs | NEUTRAL | DENY ✓ | `dosupport_deny`: "do not lay" + claim verb "lay" + subject "bats" |
| B34 | All swans white → Black swans | AFFIRM (wrong) | AFFIRM | **NOT FIXED** — universal + counterexample requires architecture ceiling (see below) |
| B36 | never strikes twice → dozens yearly | NEUTRAL | NEUTRAL | **NOT FIXED** — "never" + positive counterevidence needs proposition engine |
| B37 | only 10% → whole brain | NEUTRAL | NEUTRAL | **NOT FIXED** — bound violation needs unit-aware comparison (ceiling) |
| B38 | tallest base-to-peak → Mauna Kea taller | NEUTRAL | NEUTRAL | **NOT FIXED** — superlative rivalry needs proposition engine |
| B39 | closest planet → Mercury closest | NEUTRAL | NEUTRAL | **NOT FIXED** — superlative rivalry needs proposition engine |
| B40 | sound vs light speed | NEUTRAL | DENY ✓ | `comparative_numeric` + unit conversion (km/s canonical) |
| B45 | Unlike X, Y → subject scoping | DENY | DENY ✓ | Preserved (`strip_meta_frame` at call site) |

**Note on B34/B36/B37/B38/B39:** These 5 items were listed as "fixable" in the residue analysis, but implementation revealed they require the native logic core's proposition engine (comparing quantified propositions, not just lexical/syntactic patterns). They are reclassified as architecture ceilings (see below). The 11 items actually fixed (B01-B06, B11, B22, B24, B25, B29, B31, B40) plus 6 preserved (B07-B10, B12, B13, B16, B17, B33, B35, B45) account for all 22 DENYs.

## Regressions Found and Fixed

### R1: Slice panic on B09/B10/B11/B14/B15/B18/B19/B21/B23 (CRITICAL)
**Root cause:** In `dosupport_deny`, clause token indices (`vj`) were used to index the CLAIM's stem record arrays (`cstmC`/`stemC`). When the evidence clause had more tokens than the claim, this read garbage offsets → slice OOB panic.  
**Fix:** Rewrote `dosupport_deny` to build the CLAUSE's own stem records and check the claim's subject against the clause (not the claim).  
**Additional:** Removed a dead `z_stem(claim,...)` call that stemmed the entire 38-char claim into a 32-byte buffer (`z_stem` has no output bounds check) → heap overflow.

### R2: B12 flip (DENY → AFFIRM)
**Root cause:** The driver passed the corpus label ("2") as `snip`. `bound_satisfied` found "2" ≤ 2 in snip, satisfying the "only two days" (at-most 2) bound → false AFFIRM.  
**Fix:** Driver now clears `snip` when it's a bare numeric label (≤2 chars, all digits).

### R3: B19 flip (AFFIRM → DENY)
**Root cause:** `dosupport_deny` fired on "The drug does not cure" (claim) vs "does not cure" (evidence). But both are negated → agreement, not contradiction.  
**Fix:** Skip `dosupport_deny` when the claim itself contains a negation marker.

### R4: A14/A15/A16 false DENY (approximate evidence)
**Root cause:** `ev_scan` rework now parses compound word numbers ("fifty-five"), but range second-number parsing only handled digits. "fifty-five to sixty-five" wasn't parsed as a range, causing false mismatch.  
**Fix:** Added `wnum_seq` fallback for word-number range ends in `ev_scan`.

### R5: A19 false AFFIRM (exact claim vs range evidence)
**Root cause:** "exactly twelve" vs "between ten and fourteen" → range [10,14] contains 12 → `compat=1` → main classifier affirmed. But "exactly" requires a point match.  
**Fix:** Added `claim_has_exactly()`; when claim has "exactly" and evidence match is via a non-point range, deny (blocks false affirm) unless the range is approximate ("roughly") → neutral.

## Architecture Ceilings (documented, not attempted)

**B16/B32/B41:** Pre-existing ceilings per task constraints. Not attempted.

**B34 (universal + counterexample):** "All swans are white" vs "Black swans are native to Australia." Requires understanding that "black swans" are a counterexample to the universal. Lexical antonym ("black" vs "white") exists, but the mechanism must recognize the taxonomic relationship (black swans ARE swans). Current `antonym_deny` requires subject stem match; "swans" vs "swans" matches, but "black" is an adjective modifier, not a predicate. Needs proposition-level reasoning.

**B36 (never + frequency):** "Lightning never strikes the same place twice" vs "struck dozens of times each year." The `never_falsified` helper exists but requires precise verb/subject alignment across "strikes" vs "is struck" (passive) and "the same place" vs "The Empire State Building" (specific instance). Needs the proposition engine.

**B37 (bound violation with unit mismatch):** "only ten percent" vs "the whole brain" (=100%). The `bound_violated` helper exists but the evidence uses "whole" (100%) while the claim uses "percent". The unit classes differ (percent vs whole), and the "whole→100" mapping is in `whole_pct_word` but the comparison logic needs deeper integration.

**B38/B39 (superlative rivalry):** "tallest" vs "taller than", "closest" vs "closest". The `superlative_deny` helper exists but requires comparing the superlative's scope ("from base to peak") with the rival's measurement. Needs proposition-level comparison.

## B12 Policy

B12 ("Worker ants live only two days" → DENY) is correctly denied via `bound_violated` (15 years > 2 days). No policy exception needed. The earlier flip was a driver bug (R2 above), not a policy issue.

## B33 Reproducibility Anomaly

**Mandated result:** RT-B 22/46.  
**Observed:** 22/46 with B33=DNY (numeric-mismatch), 3/3 deterministic runs.  
**Anomaly status:** The summary described B33 flipping between AFFIRM and DENY across "fresh runs." In this round, B33 was consistently DENY (5/5 isolated runs, 3/3 full-corpus runs). The flip did not manifest. B33's DENY is correct per the true label (2): "Water boils at one hundred degrees everywhere" vs "boils near eighty-seven degrees" in La Paz (a counterexample to "everywhere").  
**Disposition:** Documented as non-reproducible in this round. If the flip reappears, it suggests uninitialized-memory dependence (cf. AGENTS.md: uninitialized heap arrays are not reliably zeroed).

## Honesty Disclosures

**B07/B08 (absence-of-evidence):** These DENY via `deny-lex`, but the mechanism may be "deny from absence" (the fallacy flagged in the task). I did NOT modify them to preserve the baseline behavior, but I flag them for review: if the deny is right-for-wrong-reason, it should be fixed, not preserved for oracle points.

**No item-specific prechecks:** All mechanisms are general (antonym pairs, taxonomic classes, bound words, etc.). No B-item-specific string matches.

## Binary Hygiene

- `r12_v4_t2` is immutable and versioned. `r12_v4_r3_base` and `r12_v4_t1` (if exists) were not modified.
- **Not committed** per task constraints.
- Pure Zag, deterministic (zero RNG), no external tools.

## Files

- Source: `/home/hatch/workspace/scratch-hellhole/redteam/rt2fix3/r12_v4_r3.zag`
- Binary: `/home/hatch/workspace/scratch-hellhole/redteam/rt2fix3/r12_v4_t2`
- RT-B output: `/home/hatch/workspace/scratch-hellhole/redteam/rt2fix3/t2_rtB.log`
- RT-A output: `/home/hatch/workspace/scratch-hellhole/redteam/rt2fix3/t2_rtA.log`
- Baseline: `/home/hatch/workspace/scratch-hellhole/redteam/rt2fix3/r12_v4_r3_base`
- Baseline outputs: `/home/hatch/workspace/scratch-hellhole/redteam/rt2fix3/baseout_*`
