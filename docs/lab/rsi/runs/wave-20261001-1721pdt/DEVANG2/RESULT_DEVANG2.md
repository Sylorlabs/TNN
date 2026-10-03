# RESULT_DEVANG2 (wave-20261001-1721pdt): DEVANG1 Crash-Fix Retry with Cold-Start Repair

**Prereg:** commit a2b567de5, "FREEZE DEVANG2 retry prereg" (wave-20261001-1421pdt lane `devang2/`).
**Implementation:** `devang2.zag` in this lane dir (`docs/lab/rsi/runs/wave-20261001-1721pdt/DEVANG2/`).
**Binary:** `devang2`, compiled with pinned znc (`src/tools/toolchain/znc_linux_x86_64_abed8aa1`), pure Zag.
**Date:** 2026-10-01. Safebin toolchain guard active (NAMECHECK.md Step 0); no forbidden executable invoked.

## What was built

Faithful port of the memory-safe DEVANG2-overnight implementation (commit 153e2af8e) plus exactly ONE mechanism change per prereg section 4.2: a cold-start segmentation tie-break. Before segmenting episode t, `bigram_total` sums all 676 bigram counts (episodes 0..t-1 only). If the total is 0, segmentation returns single-character segments and the DP is not called; otherwise the unchanged DEVANG1 `seg_dp` runs (length-averaged log bigram score minus BOUNDARY_COST, retained per prereg section 3). In practice the branch fires at t=0 only. No new semantic cases, modes, bridges, routers, or handlers. Crash-fix bundle inherited: 24-byte lexicon entries (16-byte string field, length at offset 16, count at offset 20), `lex_add` rejects segments longer than 16, every buffer access bounds-checked, K1 measured from the t=60 snapshot.

## Kill bars (threshold, result, verdict)

| Bar | Threshold | Result | Verdict |
|-----|-----------|--------|---------|
| KR0 (crash regression, hard gate) | 3/3 runs complete, no panic/trap, zero stderr | 3/3 exit 0, 0 stderr bytes each | PASS |
| K1 (lexicon discovery) | >= 8/10 phase-1 true words at t=60 snapshot | 3/10 | FAIL |
| K2 (DIRECT novel) | >= 5/6 | 5/6 | PASS |
| K3 (NEG novel) | >= 2/3 | 1/3 | FAIL |
| K4 (REL novel) | >= 2/3 | 3/3 | PASS |
| K5 (SYN novel) | >= 2/3 | 1/3 | FAIL |
| K6 (SIZE novel) | >= 2/3 | 3/3 | PASS |
| K7 (3-WAY novel) | >= 1/2 | 0/2 | FAIL |
| K8 (beats controls) | learner test accuracy exceeds best control by >= 15pp | learner 13/20 vs best control 17/20; diff -20pp | FAIL |
| K9 (new vocab acquisition) | >= 7/10 on last 10 phase-2 training episodes | 6/10 | FAIL |
| K10 (true online, governance) | code audit: strictly sequential, updates after segmentation/interpretation | PASS by inspection (see audit) | PASS |
| K11 (no future leakage, governance) | bigram counts for episode t exclude episode t | PASS by inspection (see audit) | PASS |
| K12 (determinism) | 3/3 byte-identical outputs | PASS, sha256 `94856b34dfa590e1b2fee9aed5c34f253068c5b0915dffeb312edc26896ac564` on all 3 runs | PASS |

Sub-bars K2..K7,K9: 3/7 (need >= 4). FAIL.

## Additional metrics (for comparability)

- Train accuracy (learner): 43/100
- Test accuracy (learner): 13/20
- C1 (no-seg memorize): 4/20
- C2 (fixed-width-3): 17/20
- C3 (substring memory): 0/20

## Determinism evidence (K12)

Three runs (`RUN1.out`, `RUN2.out`, `RUN3.out`), exit code 0 each, stderr 0 bytes each (`RUN1.err`..`RUN3.err` empty). `cmp` confirms byte-identical outputs 3/3. sha256 recorded above, identical across runs.

## Crash-regression evidence (KR0)

The exact DEVANG1 crash input (seeded episode generator, seed 123456789, 100 strictly-online training episodes followed by 20 frozen test episodes) executed to completion on 3/3 runs with no panic, no trap, and non-zero stderr absent. The memory-safety defect class does not survive the layout fix.

## Online audit (K10, K11) by code inspection

- **K10:** The training loop processes episodes in order t=0..99. Each iteration calls `seg_online` (segmentation, using only the W buffer built from episodes 0..t-1), then lexicon lookup, then `interpret`, then `learn_update` (bigram/lexicon/grounding/negator/comparative updates). Test loop (t=100..119) calls `seg_online` and `interpret` only; no `learn_update`. No structure is built from future data. PASS.
- **K11:** Bigram counts are updated in `learn_update` step 1, which runs strictly after segmentation of episode t. The cold-start branch reads `bigram_total` from the same pre-update W buffer, so it sees totals from episodes 0..t-1 only. PASS.

## Architecture accounting (actuals)

| Field | Frozen expectation | Actual |
|-------|-------------------|--------|
| Cognition source lines added | < 120 new/changed lines vs faithful DEVANG1 port; no new subsystem/module | ~35 lines (`bigram_total`, `seg_online`, 2 call-site swaps, header comment); no new subsystem or module |
| New hardcoded semantic cases | 0 | 0 (negator and comparative remain the generic statistical tests of DEVANG1 4.5/4.6) |
| New modes / bridges / routers / handlers | 0 | 0 |
| Learner-state structures created | 0 new persistent structures | 0 (cold-start check reads the existing bigram buffer; no new state) |

No semantic case, mode, bridge, router, or handler was added; governance holds.

## Verdict

**BUILD-FAIL.**

Killing evidence: K1 FAIL (3/10 vs 8/10), K8 FAIL (learner 13/20 vs best control C2 17/20), sub-bars 3/7 (need >= 4). The cold-start hypothesis is falsified. A debug instrumented build confirmed the cold-start branch fires exactly once (at t=0) and the mechanism scores are byte-identical to the no-cold-start overnight run (identical K1, identical 13/20, identical train 43/100). Initialization was not the bottleneck: with zero counts the DP's single-segment default at t>=1 (all bigrams from episode 0 carry count 1, so whole-utterance segments still win under length-averaged scoring) poisons the lexicon identically whether or not t=0 yields single characters. This corroborates that the bottleneck is the scoring function itself, consistent with the DEVANG3 two-pass redesign line, exactly as the prereg's honest-boundaries section predicted for a mechanism BUILD-FAIL.

## Classification

Developmental L2 (structural learning attempt), not L3. No representational invention claimed. The mechanism (bigram DP segmentation, grounded lexicon, learned negator/comparative flags) is researcher-designed; the learner fills parameters.

## Files

- `devang2.zag`: implementation (pure Zag).
- `devang2`: compiled binary (pinned znc).
- `RUN1.out`, `RUN2.out`, `RUN3.out`: raw outputs (3/3 byte-identical).
- `RUN1.err`, `RUN2.err`, `RUN3.err`: stderr captures (all empty).
- `RESULT_DEVANG2.md`: this file.
- `BUILD-LOG.md`: file creation order (prereg analysis before implementation).
- `NAMECHECK.md`: toolchain guard Step 0.
