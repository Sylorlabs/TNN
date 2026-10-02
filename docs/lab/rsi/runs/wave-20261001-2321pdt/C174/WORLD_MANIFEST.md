# WORLD_MANIFEST.md: sealed worlds for the C174 battery

Sealed 2026-10-01, wave wave-20261001-2321pdt, AFTER the prereg
freeze (commit 134af1cb2) and AFTER the implementation commit
(commit b5e0274f7), BEFORE any evaluation output exists.
No evaluation binary was run before this commit.

## Seal

- Generator: c174_gen.zag (committed, seed 20261001 frozen in
  PREREG_C174.md section 2.7).
- world_sealed.zag SHA-256:
  e66dab44370eaad23da57cedfef59e202a1f14aec42447addeaec4edad787fc8
- Generator command: sh build.sh seal (znc c174_gen.zag,
  stdout redirected).

## Re-verification

Anyone can reproduce this exact file: check out the frozen
prereg seed (20261001) plus the committed c174_gen.zag, compile
with the pinned znc, run, and compare SHA-256 with the hash
above. The worlds were not hand-tuned: every number in
world_sealed.zag is LCG output under the structural constraints
stated in PREREG_C174.md sections 3.1 and 3.2.

## Contents (summary, not a substitute for the file)

- W-REORDER: 48 trials, 6 families, sealed success permille
  {f0:900, f1:450, f2:600, f3:150, f4:300, f5:750}, precomputed
  per-trial per-family draw rows, 48 self-noise slots.
- W-RETIRE: 5 pursuits with sealed event histories (P1 ends
  ABANDONED with 4 consecutive failures; P4 F,F,F,S ends
  RE-ENGAGED), 10 structures with sealed pursuit assignment and
  bids, 5 victims under pressure, 6 held-out queries needing
  the clean ACTIVE pursuits.
- K-H3 migration world is not in this file; its seal is the
  frozen prereg 4b05c8011 plus the CONSEQ committed hashes
  (PREREG_C174.md section 3.3).
