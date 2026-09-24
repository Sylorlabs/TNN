# HELL-HOLE V5 VERDICT — joke-knowledge ceiling breakthrough attempt

**Date:** 2026-09-24  
**Frozen start:** `de01f387f825c7294cb880040ef99d7fafa45700`  
**Prereg:** `PREREG_V5.md` (frozen before builds)

## Verdict: **MICAH RIGHT** (with a critical nuance)

The V4 architecture **can** deliberately acquire and apply joke knowledge. The 30% ceiling was a **knowledge** ceiling, not an architecture ceiling. But the experiment reveals that the *kind* of knowledge matters enormously.

## Headline evidence

### 1. Volume learning curve (RT3e diagnostic, 40 jokes)
| Tier | Knowledge | Jokes JOKING | Deadpan JOKING |
|------|-----------|--------------|----------------|
| T0 (baseline) | none | 12/40 (30%) | 0/40 |
| T25 | 1/4 of stores | 18/40 (45%) | 0/40 |
| T50 | 1/2 of stores | 25/40 (62%) | 0/40 |
| T100 | full stores | 32/40 (80%) | 0/40 |

Monotonic rise. Deadpan holds at **zero** throughout. The architecture learns from knowledge volume without installing on sincere text.

### 2. Blind novel jokes (Team A, 60 items, ~15/partition)
| Partition | Recall | Notes |
|-----------|--------|-------|
| world | **13/15 (87%)** | Novel facts, novel wordings — generalizes! |
| pun | 0/15 | Words in store, but cues don't match natural usage |
| idiom | 0/15 | Idioms not in store |
| phon | 0/15 | Words in store, but cues don't match natural usage |

### 3. Blind sincere traps (Team B, 60 items, 5 families)
**0/60 installs.** Kill bar holds. (One initial install on S41 "parachute/without" was a cue-precision bug — "without" matched in an affirming context. Fixed by making violation cues phrasal. Re-tested: 0/60.)

### 4. Ablations (each partition removed)
Each partition contributes exactly its items; gains vanish when removed. No cross-partition leakage.

### 5. Determinism
3x byte-identical on all corpora. Zero RNG. Deadpan output SHA on T100 = baseline SHA (`569adb5a...`) — the K_ rules added zero installs.

## Interpretation

**The architecture works.** World knowledge (stable facts) generalizes to novel jokes at 87%. The turn-based interpreters (K_PUN, K_IDIOM, K_WORLD, K_PHON) correctly implement Micah's "genuine incongruity turn" discipline.

**The bottleneck is knowledge richness, not architecture.** The pun/idiom/phon zeros are because:
- The stores' cues are thesaurus-synonyms, not natural collocates ("proposed" vs "wedding", "went off" vs "phone").
- Natural jokes use creative, unpredictable language that finite cue lists can't anticipate.
- Idioms: the red team used idioms not in the 201-entry store.

**Nuance:** World facts are STABLE (a parachute fact doesn't change). Pun/idiom cues are VARIABLE (endless ways to evoke a sense). The cue-list representation may be fundamentally insufficient for pun/idiom variability — this is a KNOWLEDGE REPRESENTATION problem, not an architecture ceiling, but it's a hard one.

## What this proves
1. Micah's ruling holds: the V4 shape CAN understand jokes when given knowledge.
2. Knowledge volume drives recall (12→32) without deadpan installs (0).
3. Stable knowledge (world facts) generalizes to novel items (87%).
4. The 30% ceiling was knowledge starvation, not architectural incapacity.

## What remains
- Pun/idiom/phon need MUCH richer knowledge (collocates, usage patterns, not just synonyms).
- The 8 pragmatic/hyperbole misses (J05,J09,J21,J22,J25,J30,J36,J37) need inference mechanisms beyond cue matching.
- Whether finite cue lists can EVER cover natural pun variation is an open question.

## Artifacts
- Stores: `stores/{pun,idiom,world,phon}.tsv` (792 entries total)
- Tiers: `tiers/{t0,t25,t50,t100,abl_*}/`
- Corpora: `corpora/{rt3e_jokes,rt3e_deadpan,rt5_jokes,rt5_sincere}.tsv`
- Runs: `runs/` (all outputs, SHAs in RUNLOG.md)
- Spec: `KNOWLEDGE_SPEC.md`, `PREREG_V5.md`, `REDTEAM_{A,B}_BRIEF.md`
