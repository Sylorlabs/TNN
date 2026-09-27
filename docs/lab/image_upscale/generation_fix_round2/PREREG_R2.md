# PREREG — Upscale Repair Round 2: Match-Time Energy-Consistent Search + Diverse Vocabulary

Written 2026-09-27 BEFORE any round-2 implementation or run. This is a FRESH
prereg; it does not amend round 1's PREREG.md (which stays frozen with its
killed arms). Tests decide; nothing here may be tuned after seeing scores.

## Problem (from round 1, HONEST_VERDICT.md)

Baseline generation-from-learned-atoms loses to bicubic everywhere (bridge
18.47 vs 25.89 dB; 9 diverse photos all lose). Round 1's three arms attacked
the key-ambiguity failure with post-hoc vetoes; all were killed by their own
bars (best: Arm 3 +0.44 dB bridge, killed by its 2 dB bar; loses 7/9 diverse).

Round 1's mechanism finding: rejection-after-the-fact cannot fix key
ambiguity (~10% SSE net vs ~37% needed for 2 dB). The fix must resolve
ambiguity AT MATCH TIME, over the FULL vocabulary (not Arm 3's top-3
prefilter), and the vocabulary must contain same-distribution atoms (4
training images gave sparse coverage for the 9 sealed photos).

## Mechanism (a): match-time energy-consistent search

### The ambiguity, precisely

At scale si, an input block B (s×s deviations, s=S/2) is matched against
atom keys K_A = D(A) (s×s), where D is the 2×2 box downscale of the atom's
full-res deviation field A (S×S). The winner (argmin keySSD) is CONSTRUCTED
by stamping the FULL-res field: output = block_mean + A (S×S).

Two atoms with near-identical keys can carry very different full-res
textures. keySSD is blind to exactly the high-frequency content that
determines construction quality. Round 1 confirmed 25/63 atoms within 2×
of the winner's SSD on the bad block.

### Expected SSE math (the score derivation)

Let GT be the true high-res block (S×S deviations), B ≈ D(GT) the observed
low-res block. For candidate atom A with full-res field A_dev:

  True construction SSE:  E(A) = ||GT_dev − A_dev||²   (S×S, unobservable)

Split X = GT_dev − A_dev into low-frequency L(X) = U(D(X)) (U = 2× nearest
upsample) and high-frequency remainder:

  E(A) ≈ ||L(X)||² + ||X − L(X)||²          (cross term ≈ 0)

  ||L(X)||² = 4·||D(X)||² = 4·||B_dev − K_A||² = 4·keySSD(A)
    (D averages 2×2 blocks; ||U(D(X))||² = 4·||D(X)||²; D(GT)≈B, D(A)=K_A)

  ||X − L(X)||² = ||HF(GT) − HF(A)||² ≈ (√UHF(A) − √H_GT)²
    (magnitude-matched model; HF = high-pass X − U(D(X)))

where:
  UHF(A) = ||A_dev − U(D(A_dev))||²   (atom's UNVOUCHED high-freq energy;
                                        precomputable per atom, S×S)
  H_GT   = ||HF(GT_dev)||²             (true missing-octave energy;
                                        estimated by Hhat below)

Hhat estimator (fixed, no tuning): the block's own top octave predicts the
missing octave via 1/f² octave constancy (energy per octave ≈ constant):

  Hhat(B) = ||B_dev − U(D(B_dev))||²   (s×s; D down to (s/2)×(s/2),
                                         U nearest back to s×s)

NULL atom (mean-fill): E(0) ≈ 4·e + Hhat, where e = ||B_dev||².

**Match-time score (computed per atom, per block, over the FULL vocabulary
at scale si — no top-K prefilter):**

  score(A) = 4·keySSD(A) + (isqrt(UHF(A)) − isqrt(Hhat(B)))²

  gain(A)  = E(0) − E(A)
           = 4·(e − keySSD(A)) + Hhat − (isqrt(UHF(A)) − isqrt(Hhat))²

TAKE iff gain(winner) ≥ 9 per constructed value AND gain(winner) ≥
gain_split (children's gains in the same construction-SSE units; the
recursion, split logic, commit, render, and LINES paths are otherwise
byte-identical to baseline).

Limits check (no free parameters):
- Smooth block (Hhat≈0): score ≈ 4·keySSD + UHF(A). Textured atoms pay
  their full unvouched energy — hallucination is penalized at match time.
- Energy-matched atom (UHF≈Hhat): score ≈ 4·keySSD. No penalty; the atom
  also earns +Hhat in gain (credit for explaining the HF energy).
- Under-textured atom on textured block: pays (√UHF−√Hhat)² — symmetric.

### Why this is match-time, not a veto

The score is evaluated for EVERY atom during the argmin search. It does
not reject a selected match afterward (round 1's failed pattern); it
changes which atom wins by estimating each candidate's construction SSE
from observable quantities + the atom's own full-res field.

## Mechanism (b): diverse vocabulary

Reteach from a 12-image DIVERSE corpus (CC-licensed Wikimedia Commons
photos; provenance in CORPUS2.md; seal-verified 0 overlap with the 9
held-out test photos):

  brick_wall, stone_wall, foliage, lake_water (continuity with round 1),
  fabric, woodgrain, treebark, portrait, car, building, cat, market (new;
  in-distribution atoms for 7 of the 9 sealed test categories).

Teaching discipline unchanged (farthest-point exemplars, tau=9/value,
NULL atom 0, keys = 2×2 box downscale round-half-away). Atom caps scaled
with corpus size to hold per-distribution density: dense scales
96/96/64/48 (S=64/32/16/8; was 48/48/48/32), thin 64 (unchanged).
Cap choices are a design decision recorded here, not tuned (teaching runs
once, before any scoring).

## Calibration: what the mechanism's ceiling is

Pre-registration measurement on the OLD vocabulary + bridge baseline
takes (Python replication, byte-exact: takes=35, G=18343607):

- Oracle atom selection (best TRUE construction SSE per take, using GT):
  222.4M → 221.2M SSE = **+0.025 dB**. Atom SELECTION is already
  near-optimal; the vocabulary — not the matching — is the binding
  constraint on the old corpus.
- The new score's predicted effect on old vocab: 7/35 winners change,
  **+0.015 dB** (60% of the oracle ceiling). The score is sound but
  small while candidates are sparse.

Consequence for the bar: (a) alone cannot clear a dB-scale bar on the
old vocab (ceiling +0.025 dB). Any substantial gain must come from (b)
providing in-distribution atoms, with (a) disambiguating among the
denser candidate field (ambiguity WORSENS with more atoms, so the
energy term's value grows with vocabulary size). The bar below is set
to detect broad-coverage (b)-driven improvement with (a) soundness
verified separately — not to predict an exact dB.

## Bars

- BAR 1 (mechanism soundness): (a) implemented on the OLD vocabulary
  must score ≥ baseline − 0.05 dB on bridge (predicted +0.015 dB;
  tolerance covers integer-rounding noise). If the score is unsound,
  kill (a).
- BAR 2 (no regression on originals): (a)+(b) on bridge AND sky each
  ≥ baseline − 0.10 dB.
- BAR 3 (broad coverage — the mandate): (a)+(b) beats baseline on ≥7
  of the 9 sealed diverse photos; mean ΔdB over the 9 diverse ≥ +0.30
  dB; every category group (texture: fabric/woodgrain/treebark; smooth:
  calmwaters; people: portrait; object: car/building; animal: cat;
  mixed: market) has non-negative mean ΔdB.
- KILL (program): fail BAR 1 → (a) killed as unsound. Fail BAR 3 →
  killed for narrow coverage ("if it only fixes bridges, kill it").
  Post-result tuning of any kind → void.

## Method notes

- Pure Zag, zero RNG. Pinned toolchain
  ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1.
- Byte-identical reruns: every binary runs every image twice; output
  SHAs compared.
- New sources: azgen2.zag (energy-consistent SHAPES matching; LINES
  path byte-identical to baseline), azteach2.zag (12-image corpus).
  Baseline azgen.zag/azteach.zag untouched.
- Eval: frozen diverse_set/eval_all.py + bridge/sky harness; frozen
  metrics.py; bicubic as scoring baseline only (never in generation).
- Test images (bridge, sky, 9 sealed) NEVER enter teaching.
- No commits by the implementer (coordinator commits). No binaries or
  rendered images in repo dirs.

---
## Dated calibration appendix (pre-implementation, 2026-09-27)

- Baseline replication (Python): takes=35, G=18343607 — exact.
- Worst take (x=192,y=32, atom 42 brick): e=10,983,605, keySSD=9,988,165,
  UHF=3,244,755, Hhat=993,491, trueSSE=45,839,713. Atom 42 is the TRUE
  best among 63 atoms (oracle confirms) — the failure is vocabulary
  coverage (no good atom exists), not winner selection. This is the
  quantitative case for (b).
- New-score winner changes: 7/35 takes; predicted +0.015 dB (old vocab).
- Oracle ceiling (old vocab): +0.025 dB.
