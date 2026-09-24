# FIX REPORT — HELL-HOLE V4 r12_v4 Round 7b (t7)

**Date:** 2026-09-24  
**Binary:** `r12_v4_t7` (SHA256: `f9edd23bf8f88ddb3a0253df74d6ea26fdcda33e9a8f1605005ad32617a2e90e`, 1,562,733 bytes)  
**Source:** `r12_v4_t7.zag` (modified from `rt2fix7/r12_v4_r7.zag`)  
**Compiler:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned)

## Summary

Round 7b restores all 8 named regressions from round-7 (t6) to their t5 verdicts, using only guards and scope-narrowing on round-7 additions. No new mechanisms were added. The two broad veto mechanisms prototyped during development (`r7b_fused_veto`, `r7b_ambigpro_veto`) were **removed** per the no-new-mechanisms constraint — they overfired (a double-if counting bug caused single segments to count twice, vetoing ordinary conjunctions like "Dolphins are mammals... and nurse their young").

## Changes (guards only, no new mechanisms)

1. **r7_nonfactive_veto + r7b_frame_guarded**: Narrows the nonfactive veto to not fire when the report frame is negated ("It is not true that the study claimed...") or the frame subject is an epistemic authority ("Astronomers have catalogued...", "The study proved..."). Prevents false neutrals on authoritative evidence.

2. **r7_contrast_deny + r7b_contrast_guarded (G1-G4)**: Guards the contrast-deny mechanism:
   - G1: Provability verb precedes "not" ("has not been proven not guilty" is failure-to-prove, not denial).
   - G2/G3: Claim scopes Y under negation or prevention verb ("the policy is not unhelpful", "the levees prevented flooding" agree with denied half).
   - G4: Evidence copula-predicates Y of claim's subject (contrast is about a different subject).

3. **r7_doubleneg2 + D1/D2**: Narrows double-negation affirmation to require proof-scope and subject matching.

## Validation Results

### 8 Named Regressions (t7 vs t5) — ALL RESTORED
| Item | t5 | t7 | Status |
|------|----|----|--------|
| rt2 B08 | 2 (deny-lex) | 2 (deny-lex) | OK |
| rt2 B45 | 1 (polarity/paraphrase) | 1 (polarity/paraphrase) | OK |
| rt2b B18 | 1 (endorse) | 1 (endorse) | OK |
| rt2b B31 | 1 (frame/sequence) | 1 (frame/sequence) | OK |
| rt2b B33 | 1 (polarity/paraphrase) | 1 (polarity/paraphrase) | OK |
| rt2c A26 | 0 (neutral) | 0 (neutral) | OK |
| rt2c A43 | 0 (neutral) | 0 (neutral) | OK |
| rt2c B27 | 1 (frame/sequence) | 1 (frame/sequence) | OK |

### t6→t7 Changes (prior corpora) — ONLY INTENDED
- rt2_A: (none)
- rt2_B: B08 (0→2), B45 (2→1) — restorations
- rt2b_A: (none)
- rt2b_B: B18 (2→1), B31 (0→1), B33 (2→1) — restorations; B28 reason change only (2→2)
- rt2c_A: A26 (1→0), A43 (2→0) — restorations
- rt2c_B: B27 (0→1) — restoration

### RT2d (rta/rtb) — GAINS PRESERVED
- t6→t7: zero changes on both rta and rtb. All round-7 gains held.

### Frozen Assets (t6→t7)
- curated-18: zero changes
- reg382 (382 rows): zero changes
- v3 seeds (run_v3seed.tsv): zero changes

### Determinism
- 3× runs on rt2_B: byte-identical (SHA dfcf19529121c95aeac4297b8ba2212353b4a059457689f6be66dac40a47d042)

## Open Items

- **RT2d A20/A21/A45**: A20 (AFFIRM) and A45 (AFFIRM) remain false affirms; A21 (NEUTRAL) is correct. These require new mechanisms (fused-subject detection, ambiguous-pronoun resolution) which are prohibited by the no-new-mechanisms constraint for this round. The broad prototypes were removed.
- **No commit**: Per task instruction, pure Zag work, no commit.

## Conclusion

**SHIP**: Zero regressions vs t5 on the 8 named items. RT2d gains held (zero t6→t7 changes). All frozen assets stable. 3× byte-identical. The binary is ready as `r12_v4_t7`.
