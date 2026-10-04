# PREREG H-SEG2 Red Team (SEG2-ADV): Frozen Attacks

**Status:** FROZEN. This prereg strictly precedes any attack implementation
or execution.
**Date:** 2026-09-29
**Target:** H-SEG2 SURVIVES (5/5), SEG-LEX-P with FBPEN=20 fragmentation
penalty. See PREREG_SEG2.md, SEG2_RESULT.md, seg2_learn.zag.
**Stance:** Assume the repair claim is false. Attack it.

## Background

H-SEG2 repaired H-SEG's shared-substring kill by charging FBPEN=20 per
fallback character. The prereg's own design analysis states the value 20
"was validated in H-SEG exploratory analysis" against the specific "all"
phenomenon (spurious gain 36-32=4 per use). Chunk scores scale as
count*len^2 while the penalty is a constant 20 per character. The repair
therefore only works while count(C)*len(C)^2 - 20*r < word_score for the
residue r the spurious tiling needs. These attacks test whether that
inequality holds outside the frozen fixture's frequency regime.

## Attack X-SG2-1: Penalty sensitivity (penalty too small)

**Fixture ADV-1:** corpus of 6 raw strings:
"xabcd","xabcd","yabcd","yabcd","zabcd","zabcd".
Shared chunk "abcd": count 6, len 4, score 96. True words
"xabcd","yabcd","zabcd": count 2 each, len 5, score 50 each.

- Test T1 "xabcd" (a seen training word). Contract: "xabcd" (50).
  Frozen prediction: SEGMENTED "x|abcd", score 76 (-20+96).
- Test T2 "xabcdyabcd" (novel pairing of seen words, EXP-C shape).
  Contract: "xabcd|yabcd" (100).
  Frozen prediction: SEGMENTED "x|abcd|y|abcd", score 152.

**Fixture ADV-2:** corpus ADV-1 plus "wabcd","wabcd" (8 strings).
Shared chunk "abcd": count 8, score 128.

- Test T2 "xabcdyabcd". Contract: "xabcd|yabcd" (100).
  Frozen prediction: SEGMENTED "x|abcd|y|abcd", score 216.

**Success criterion:** If any predicted wrong segmentation is observed,
X-SG2-1 SUCCEEDS. Interpretation: the penalty does not scale with chunk
frequency; the "shared-substring limitation closed" claim holds only in
the frozen fixture's frequency band. Verdict contribution: DOWNGRADE
(the frozen 5/5 bars are untouched; the generality claim is narrowed).

## Attack X-SG2-2: Adversarial fixture

Same fixtures as X-SG2-1. They are adversarial by construction: natural
corpora (repeated words, the same regime as the frozen corpus), tests in
the exact shape of frozen EXP-C (novel pairing of seen words) and of a
seen word. No exotic inputs.

**Success criterion:** Wrong segmentation on T1 or T2 in either fixture
-> X-SG2-2 SUCCEEDS, confirming the failure is systematic, not a
one-off. Verdict contribution: DOWNGRADE (same verdict as X-SG2-1).

## Attack X-SG2-3: Long sequences

**Fixture ADV-3:** frozen EXP-A corpus table; test = 120-character digit
string ("0123456789" repeated 12 times). Digits never occur in corpus A,
so zero chunks match: pure fallback path, 120 DP moves, unique optimum
(nopt=1), which exercises build_best's 64-entry move stack and the
256-byte output buffer.

Run 3x with a 20s timeout each. Record completion, crash (signal),
hang, or output corruption.

**Frozen prediction:** heap buffer overwrite past the 64-entry stacks
-> likely crash or corrupted output.

**Success criterion:** Crash, hang, or corrupted/incorrect output on any
run -> X-SG2-3 SUCCEEDS: robustness failure class demonstrated.
Verdict contribution: DOWNGRADE-relevant boundary (long inputs are
outside the frozen scope, but a segmentation mechanism that corrupts
memory on a 120-char input has a documented robustness limit).
If it completes correctly 3x -> X-SG2-3 FAILS (attack fails).

## Attack X-SG2-4: Source audit

By inspection of seg2_learn.zag:

(a) The fallback relax site applies 0-FBPEN() per character.
(b) The reachability guard is dpi>DPSENT() with DPSENT()=-1000000.
(c) No expected-output literals; corpora are disclosed fixtures.
(d) Note latent bounds informationally: mv_add 8-move cap, 64-deep
    move stacks in build_best/enum_bwd, nopt cap 999, 256-byte buffer.

**Criterion:** PASS if (a)-(c) hold. (d) is informational, not a kill.

## Regression control

The attack binary re-runs frozen EXP-A, EXP-B, EXP-C, EXP-D first.
Expected: identical verdicts to SEG2_RESULT.md
(EXP-A SEGMENTED small|green|ball 132 NOPT 1;
 EXP-B AMBIGUOUS ab|cde, abc|de;
 EXP-C SEGMENTED small|red|cube 100 NOPT 1;
 EXP-D SEGMENTED big|b|l|u|e|cube -30 NOPT 1).
If any regression differs, halt: the harness is broken, not the target.

## Verdict rule

- X-SG2-1 or X-SG2-2 succeeds -> H-SEG2 DOWNGRADED. Frozen 5/5 bars
  stand; the "limitation closed" claim is narrowed to the validated
  frequency regime; the failure class (penalty does not scale with
  count*len^2) is documented with a repair direction (frequency-scaled
  penalty or MDL lexicon prior).
- X-SG2-3 succeeds -> robustness boundary documented (downgrade-relevant).
- X-SG2-4 PASS/FAIL as audited.
- All attacks fail -> H-SEG2 SURVIVES unmodified.

## Scope and governance

Pure Zag. No Python at any stage. No em dashes in documentation.
Determinism: 3x byte-identical runs per binary (cmp-verified), except
ADV-3 where crash/hang is itself the observation. Commit prereg before
any attack code. Stage and commit only adversary-owned files.

## Prereg commit ordering

This file is committed before any attack implementation, attack
execution, or result. Attack sources (seg2_adv.zag, seg2_advlong.zag),
raw evidence, and SEG2_ADV_RESULT.md come in later commits.
