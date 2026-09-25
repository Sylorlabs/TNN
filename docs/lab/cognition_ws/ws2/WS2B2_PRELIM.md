# WS2-B2 Track B: prelim and evidence

## Framing

Micah's standing correction governs this work: we thought we were not
using tokens, and we are not. TNN uses no LLM tokenization, no BPE, no
learned embeddings, no statistical models, and no subword vocabulary.
"Token overlap" is a battery measurement only. The mechanism below is
byte-exact word matching against a curated, versioned synonym table plus
deterministic byte-level stemming. Zero randomness anywhere.

## Result

| Battery | Before (WS2-B) | After (WS2-B2) |
|---|---|---|
| Official 51 | 46/51 | **51/51** |
| T-exact (45 non-PARA) | 45/45 | **45/45** (unchanged) |
| P-PARA (6) | 1/6 (QP04 via stemming) | **6/6** |
| P-NEG (6) | 6/6 abstain | **6/6 abstain** (unchanged) |
| Maintenance (7) | 7/7 | **7/7** |
| Fresh QR01-QR06 | n/a | **6/6** |
| Distractor QD01-QD06 | n/a | **6/6, zero decoy retrievals** |
| Abstention QV01-QV03 | n/a | **3/3 abstain** |

The five WS2-B paraphrase misses now resolve:

| Probe | WS2-B | WS2-B2 | Bridge? |
|---|---|---|---|
| QP01 moonwalkers/hop/gently/weak/selenian/attraction | miss | PP01 | yes |
| QP02 kraut/fizz/bacteria/dine/fortnights | miss | PP02 | yes |
| QP03 withered/limbs/trimmed/prior/sprouting | miss | PP03 | yes |
| QP04 | PP04 (stemming) | PP04 | **no** (phase-1 kept, per prereg) |
| QP05 witticism/beginning/before/readiness | PP03 (false positive) | PP05 | yes |
| QP06 sacred song/linger/basilica/masonry | miss | PP06 | yes |

## Design (frozen in PREREG_WS2B2.md)

- Synonym table: **56 curated pairs, 112 distinct stem keys, 56 canonical
  classes, zero stem-key collisions.** SHA-256 of the frozen table bytes:
  `bd23d16fe518024d15445299808017b91e4a47c1ef7d075d516363887c22fc7b`.
  Each pair is symmetric; both sides are stemmed with the frozen stemmer;
  the canonical form is the byte-lexicographically smaller stem; first
  pair wins on collision (generator asserts none).
- Morphology and stoplist unchanged from WS2-B.
- Phase 1 is the WS2-B lookup unchanged (routes 1/2/3, weighted score
  cell_score*1000 + own_score).
- Phase 2 (the bridge) fires ONLY in route 3 and ONLY when the phase-1 top
  candidate matches at most one distinct query stem (abstain or weak
  single-token match). It recomputes candidate scores with canonical-stem
  matching: tot2 = cell_score2*1000 + own_score2.
- The phase-2 ranking REPLACES the phase-1 ranking iff it has a UNIQUE top
  candidate matching at least two distinct canonical stems
  (dstem_hit >= 2, no tie). Otherwise the phase-1 result stands. This is
  what keeps QP04 passing: its phase-2 top matches one stem, so the
  phase-1 single-token win is kept.
- Gate and bar count DISTINCT query stems: one word matching in both the
  cell aggregate and the item's own token set is one stem's evidence.
  (QP05's "before" is the case that forced this reading: it matches PP03's
  cell and own sets, which is still a weak single-token match.)
- Report line gains a trailing bridge flag: route|nsj,nd,nt|ncand|take|
  bridge, bridge=1 iff phase 2 overrode phase 1.

## Implementation corrections during build

Two bugs in the first draft, both fixed before the evidence runs and both
required to meet the prereg's own definitions:

1. Gate/bar first implemented on the weighted tot (cell*1000+own), then on
   raw cell+own pair counts. Both wrong per the prereg's parentheticals
   ("weak single-token match", "at least two distinct stem matches").
   Final: distinct query stems via dstem_hit, top candidate selected by
   the weighted tot. Ranking itself is unchanged.
2. cmd_grade class-counter table overflow: `nio_alloc(32*16+8)` with 8
   counter bytes written PER class at `32*16+cfound*8` panicked with
   "slice index out of bounds" on any battery with 2+ query classes
   (pre-existing WS2-B bug; the old binary panics on its own outputs).
   Fixed to `32*16+32*8+8`. Grader harness only; retrieval path untouched.

## Determinism

Three full reruns (fresh init, official 51, B2 15, full maintenance leg
with install/revise/delete): all output files byte-identical across runs.

- out.txt:     b09796e7dbc2d2b1fd81246630cc27a80f0d2762eccbadefe83fcfdbdd1490b4
- rep.txt:     a17d10ec3cccae6d6fe780383b6d48351aa1e9b047bd4ce6ad0aa7a9c0d08954
- grade.txt:   c25fa213da8ef25dd95e0f207b4f374d019cf186c385e24d5cf0ee145f09124b
- out_b2.txt:  cc81ca27b53afb67d84c6835d7861d619f84325f811ad592ac9c9d6583598630
- rep_b2.txt:  7829a878fdc28dcecb43ffbff136116e2ba0878aca48acb1647b999e6b12ac05
- grade_b2.txt: fe58bfc88a64edd2e683135e3467228229e81fc000b5c9d2f937fa3ff944c953
- m_o123.txt:  b7dbaa57234a9aa2bf024cee2a8ade6e10ef251554e955e3fa1d3d6e1541c8ec
- m_o45.txt:   13277184fdcc881a19bd1beb04a8b0c3154827b643dda890e1b79e325ff7ec26
- m_o67.txt:   64e2d663a5c92323a846c9e9d8ce91eedaf77e8e971e3c4d20efe4263c55d415

## RNG gate

grep over the B2 runtime sources (toc_b2.zag, syn_table.zag, lib.zag) for
rand/srand/random/lcg/seed/shuffle/uuid/time(/clock: no hits. The bridge
is a linear scan over a frozen table with byte-exact comparison; tie-break
is by item index (deterministic sort). Zero RNG.

## Commits (branch tnn-native-lab)

- Prereg + frozen fixtures: 79468d21b05babfdf503cc7d9c2e1acc14159a5b
- Code (toc_b2.zag, syn_table.zag, gen_syn_table.py, build_b2.sh):
  7740f8fd1faf1d82cce471dbf18bd74b61e1065d
- Evidence (this doc + run script): see commit below.

## Kill-bar verdict

1. Official T-exact 45/45: PASS
2. P-PARA 6/6 including QP04: PASS
3. Maintenance 7/7: PASS
4. Fresh QR01-QR06 6/6: PASS
5. Distractor QD01-QD06 6/6, zero decoys: PASS
6. QV01-QV03 all abstain: PASS
7. Three full reruns byte-identical: PASS
8. Zero RNG grep gate: PASS
9. QN01-QN06 remain abstentions: PASS

9/9. Track B complete.
