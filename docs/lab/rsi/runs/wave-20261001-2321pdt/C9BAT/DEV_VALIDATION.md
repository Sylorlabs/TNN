# DEV VALIDATION REPORT: C9GEN corrected causal battery generator
Lane: wave-20261001-2321pdt/C9BAT. Protocol: PREREG_C9GEN.md section 8
(frozen; amendment A1 recorded before the validation run; no kill
bar moved). Driver: run_dev.sh. All code pure Zag, pinned znc.

## Binaries (built 8.1 from committed sources, sha256)

- bin/c9gen:     073c014c41169da210a333ee1b61a09f55e7270d824380a877ee7a07f0e271de
- bin/c9gamer:   392177dfc005862ce21c3dd904c8e9d224984a752cd72d844ead6ab156f6f648
- bin/c9exp:     cebb6621bf45c441245c55900d06346e90d5d4cbf980a30b7da54e9332b5d496
- bin/c9score:   392a8392b8dc89e878453bb20e09306dff648dd2ca5bf821941875702c5095cc

(Hashes also stored in dev/BIN_HASHES.txt.)

## Dev battery (8.2; SEED_DEV = 777001337, 24 worlds)

turns.jsonl: 15384 lines (24 x (400 obs + 120 do + 120 do_out + 1 q))
key.txt: 24 lines. worlds.txt: 24 lines. manifest.txt: params.

sha256 (identical across dev/, dev2/, dev3/):
- turns.jsonl: 5a5dce4e5f2a9e09f06ccc45d0174c5d6f01a56e99788e1b6347ceb307ef70d0
- key.txt:     5b2a063868617499cb026c1ae871710db231fd4fa7486c3ef7d8d86b02e20b13
- worlds.txt:  25dcc21670cda7656f354d119d9cb9322ea6a09f9aa7e0075f054f40a42b7127
- manifest.txt: 1030bbdb5adfe152f7dfbcbd13e9ba1a288cfca01b69e19fe4bcb3d577c9bce7

World properties (dev/worlds.txt):
- True-chain distribution over 24 worlds: X->Y->Z x5, X->Z->Y x1,
  Y->X->Z x9, Y->Z->X x3, Z->X->Y x3, Z->Y->X x3. All 6
  permutations appear; none hand-picked.
- Candidate order: true chain listed first in 11 items, second in
  13 items (seeded coin flip; no positional bias).
- Observations: 909 of 9600 obs turns disagree on at least one
  variable (9.5%). Nothing enforces x==y==z; the broken
  battery's CHECK 1 exactness is gone. The observation
  distribution carries chain-identifying correlational
  structure (adjacent pairs agree w.p. 0.95, endpoint pairs
  w.p. 0.9025).

## Scores (8.3, 8.4, 8.5; c9score on dev/key.txt)

- gamer old (broken-battery exploit: first candidate, first
  variable): 0/24. The exploit that scored 3/3 on the frozen
  battery scores exactly zero here: answers are full chain
  strings, never single variable names.
- gamer first (first candidate full string): 11/24 (chance;
  equals the 11 first-listed true chains).
- gamer second (second candidate full string): 13/24 (chance).
- reference experimenter (two-stage interventional protocol,
  reads only turns.jsonl): 24/24.
- all-UNKNOWN replies: 0/24.

Experimenter run is deterministic (two consecutive runs
byte-identical).

## Audits (8.6)

- G4: grep for full chain-string literals in c9gen.zag returns
  0 hits. Chains, alt candidates, candidate order, obs bits,
  and do() outcomes all come from the seeded RNG stream.
- G5: `which python3` prints nothing at lane end (as at lane
  start). Zero non-safebin executable invocations this lane.

## Kill-bar verdicts

- G1 (gamer old = 0/24): PASS (0/24).
- G2 (experimenter = 24/24): PASS (24/24, strictly greater
  than 0 as required).
- G3 (3/3 byte-identical generation): PASS (sha256 equal
  across dev, dev2, dev3 for all four files).
- G4 (genericity, zero chain literals): PASS (0 hits).
- G5 (pure Zag): PASS (`which python3` empty at start and
  end; no forbidden invocations).
- G6 (no fixed positional rule reaches 24/24): PASS
  (first 11/24, second 13/24).
- G7 (honest UNKNOWN = 0/24): PASS (0/24).
- G8 (scope honesty): PASS. Stated here and in
  JUDGE_BRIEF.md: C9GEN is a candidate instrument, not a
  replacement for the frozen arena battery; no L3,
  substrate, or canonical-score claim is made; adoption is
  a future governance decision. The 24/24 is evidence
  about the instrument (it admits a genuine
  experiment-driven solution), not evidence that any
  learner is L3.

Verdict: GEN-PASS. All eight kill bars pass.

## Trial-found bug fixes (design unchanged; documented here)

1. LCG bit-0 parity: the arena LCG alternates bit 0 every
   step, so rng_range(rng,2) draws were degenerate. In a
   /tmp trial (seed 12345, not the frozen seed) the
   candidate-order coin came out 24/24 true-first, which
   would have failed G6. Fix: binary draws (obs root bits,
   do() root bits, order coin) use bit 33 via rng_bit;
   edge flips use rng_range(rng,2000) < 100 (p = 0.05
   kept). The single LCG stream and SEED_DEV are
   unchanged.
2. Chain coverage: the first Fisher-Yates implementation
   (driven by %3/%2 draws) reached only 3 of 6
   permutations in 24 worlds on the dev seed. Fix
   (prereg amendment A1, committed before validation):
   uniform permutation index via rng_range(rng,6000)/1000.
   All 6 permutations now appear.

Both fixes were found by inspecting trial/dev outputs,
not by moving any kill bar. The frozen dev seed
777001337 was used for exactly one validation campaign
(three runs); no reseeding was performed.

## What this does not show

- That any TNN subsystem can pass this battery (only the
  calibration experimenter was run).
- That passing it would constitute causal understanding in
  general, or L3 representational invention (the
  experimenter is a fixed two-stage statistical protocol,
  deliberately simple).
- That the frozen arena battery is repaired (it is
  untouched; this is a separate candidate instrument).
