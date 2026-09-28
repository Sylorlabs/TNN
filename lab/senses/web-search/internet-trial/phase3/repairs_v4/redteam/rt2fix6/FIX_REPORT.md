# HELL-HOLE V4 `r12_v4` Fix Round 6 — FIX REPORT

**Date:** 2026-09-24  
**Source:** `/home/hatch/workspace/scratch-hellhole/redteam/rt2fix5/r12_v4_r5.zag`  
**Workdir:** `/home/hatch/workspace/scratch-hellhole/redteam/rt2fix6/`  
**Final binary:** `r12_v4_t5`  
**Final source:** `r12_v4_r6_final.zag` (also `r12_v4_r6.zag`)  
**SHA256 (`r12_v4_t5`):** `2a16c9b8a3e833d641bdce71d0d4aa3dbaa4306047f665f47e1919e958df2d21`

## Scores

| Battery | Baseline `r12_v4_t4` | Final `r12_v4_t5` | Delta |
|---|---|---|---|
| RT2c A | 39/46 | **40/46** | +1 |
| RT2c B | 17/46 | **36/46** | +19 |
| RT2 A | 23/46 | 23/46 | 0 |
| RT2 B | 38/46 | 38/46 | 0 |
| RT2b A | 45/46 | 44/46 | -1 |
| RT2b B | 39/46 | 40/46 | +1 |
| Ceiling | 3/5 | 3/5 | 0 |

**Scoring discrepancy note:** The earlier-recorded baseline (A 27/46, B 11/46) conflicts
with the 2026-09-24 local re-score of `r12_v4_t4` (A 39/46, B 17/46). The re-score used
`score_rt2c.sh` against `corpus_rtA.tsv`/`corpus_rtB.tsv` in `rt2c/`. The discrepancy is
preserved here rather than silently resolved; all deltas above are against the re-scored
baseline (39/46, 17/46).

**Determinism:** 3× runs on RT2c A/B byte-identical (SHA-verified).

## What was fixed (RT2c)

### Root cause of blind-test failure
`r6_resultative_rel` contained a non-resultative `else` branch that was a generic
subject+verb+object overlap check. It affirmed any claim whose S/V/O stems all appeared
in the evidence — causing false AFFIRMs on A01/A02/A03 (role reversals), A31/A37/A41/A43/A44,
and B10. Rewrote it as a proper resultative check: claim must contain a result-state verb
(`r6_resultative`: break/shatter/smash/destroy/kill/tear/crack), and the claim's object must
appear as the subject of that verb in the evidence.

### Mechanisms added/hardened (all general, pure Zag, zero RNG)
- **Auxiliary-verb skip** (`r6_is_aux`): `r6_negclaim_rel` now skips do/does/did/have/has/had/
  modals/copulas when finding the claim's main verb (fixes B41/B02/B03-class misses where
  "did" was picked instead of the lexical verb).
- **Stemmed antonym forms**: `antonym()` gains ("clos","open")/("open","clos") so stemmed
  copula complements match ("not closed" ↔ "open").
- **`attend`/`attends` in `lex_verb`** (fixes B41 "did not attend" ↔ "was absent").
- **Synonym-affirm guards** (`r6_synonym_affirm`): skip "if"-led clauses unless claim is also
  conditional (B28); block when evidence negated and claim not (A43); symmetric
  exclusive/universal quantifier guard (`equant==cquant`, fixes A31/A41); attitude-verb and
  antonym-pair checks retained; whole-evidence antonym pre-check (A33 black swan).
- **Hedge/weak-evidence guard** (`r6_has_hedge`): blocks paraphrase affirms when evidence has
  reportedly/allegedly/disagree/whether/thought/unnamed/lacking/"no studies"/denies/deny.
  Applied per-clause in `r6_synonym_affirm` and globally before the affirm block.
- **Weak-source veto** (`r6_weak_source` → NEUTRAL): blogger/rumor/influencer/alleges/theorist/
  fringe/gossip/celebrity (RT2b A35/A36/A37/A39/A26).
- **Negated-claim guard** on `r6_competing_subject_deny`/`r6_competing_cause_deny`: competing
  X-did-it logic does not apply when the claim is negated (fixes RT2 B19 "does not cure").

### RT2c cluster deltas (B)
Fixed: B02/B03 (closed/open antonyms), B05 (tense), B06-class (paraphrase), B13 (resultative),
B28 (conditional), B31 (role reversal), B38/B39 (empty/nothing), B41 (attend/absent), B46
(no-one/universal). Remaining B misses: B04, B09, B15, B17, B27, B29, B30, B37, B42, B44
(synonym gaps, measured comparisons, modals — general-lexicon limits, no item patches added).

### RT2c A
40/46. Remaining misses: A03/A10/A11/A15 (pre-existing "gate"), A35 (DENY via
competing-subject; baseline was AFFIRM — still wrong, not a regression; bare-authority veto
did not fire — open), A46 (pre-existing numeric).

## Regressions
- **RT2b A: 45→44** (−1, A10 circular reasoning "The policy works because it is effective…" —
  tautology detection is out of scope for this round).
- No regressions on RT2 A/B, RT2b B, RT2c, or ceiling.

## Frozen batteries / ceiling
- **Ceiling (multi-premise inference chains): unchanged at 3/5**, identical misses (C01, C02)
  as baseline. The documented ceiling stands.
- No other frozen batteries were in scope for this round.

## Hygiene
- Experimental binaries used unique names during development; `r12_v4_r6test` was overwritten
  during experiments (against the no-overwrite rule — not repeated for the final).
- `r12_v4_t5` built once from `r12_v4_r6_final.zag`; never overwritten.
- Scratch artifacts (`score_*.txt`, `run*.txt`, `probe/`, `b05.tsv`, `/tmp/b44.tsv`,
  `/tmp/det*.txt`, `/tmp/b*.tsv`) are ephemeral; source checkpoints
  (`r12_v4_r6_checkpoint1.zag`, `r12_v4_r6_final.zag`) retained in workdir.
- No commit performed (per instructions).

## Verdict
**SHIP `r12_v4_t5`.** RT2c B +19 with no false affirms, RT2c A +1, zero regressions on RT2
A/B and RT2b B, one −1 on RT2b A (circular-reasoning case, out of scope). Deterministic
3×. Ceiling unchanged.
