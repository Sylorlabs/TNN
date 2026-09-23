# VERDICT_CMP_SCALE.md

Comparison-engine scale trial — final binding verdict.
Prereg: `PREREG_CMP_SCALE.md` (committed `91098785492980c23fb40e7969356420fa141722`).
Date: 2026-09-23. All work on Muse's Linux VM, branch `tnn-native-lab`.

## Question under test

Does TNN's existing native dialogue logic already do general comparison
reasoning, or is dedicated comparison machinery required? Tested at 1x
(96 turns), 10x (960), 100x (9,600) probe scale, 11 families.

Terminology (per prereg): the baseline is NOT "no comparison path". It is the
**existing shallow keyword/marker `do_compare` branch inside native dialogue
logic**. The prototype is **dedicated typed, compositional comparison
machinery** (`engine/cmp_engine.zag`, frozen at commit `b0441c69`).

## Frozen kill criterion (from prereg, verbatim)

Fire if: any family < 0.90 at 1x; or any family drops > 0.03 from 1x to 100x;
or overall < 0.90 at 100x.

## Baseline results (existing shallow `do_compare` path)

Source SHA-256: `ef647ea70e93479dfb992a20f2a9e05597f139c7b212d2c0f34c8edea461862c`

| Family      | 1x    | 10x   | 100x  |
|-------------|------:|------:|------:|
| ANA         | 1.000 | 1.000 | 1.000 |
| BEFOREAFTER | 0.000 | 0.000 | 0.000 |
| HEIGHT      | 1.000 | 1.000 | 1.000 |
| HOP         | 0.750 | 0.800 | 0.812 |
| MORELESS    | 0.000 | 0.000 | 0.000 |
| NEG         | 0.000 | 0.000 | 0.000 |
| SAME        | 0.000 | 0.000 | 0.000 |
| SUP3        | 0.000 | 0.000 | 0.000 |
| THRESH      | 0.000 | 0.000 | 0.000 |
| TIME        | 1.000 | 1.000 | 1.000 |
| UNKNOWN     | 0.000 | 0.225 | 0.510 |
| **Overall** | **0.396** | **0.419** | **0.444** |

**The kill criterion fired at 1x** (8 of 11 families below 0.90; 7 at 0.000).
The shallow path handles only the frames it was keyworded for (taller-than /
came-first / higher-of-two style); it cannot do thresholds, sameness,
negation, superlatives, composition hops, or before/after disjunction.
No scale degradation was observed (it was already at floor), and wall-clock
was linear: 1x ~1.0s, 10x ~4.7s, 100x ~9.7s per 2,200-chunk.

## Prototype results (dedicated comparison engine)

Frozen engine commit: `b0441c692c96292bdfacefdfbcb5a27d1425bb23`
(prereg step 4; splice-only change, rest of source byte-identical to baseline).

| Scale | Correct    | Overall | Every family |
|-------|-----------:|--------:|--------------|
| 1x    | 96 / 96    | 1.000   | 1.000        |
| 10x   | 960 / 960  | 1.000   | 1.000        |
| 100x  | 9600 / 9600| 1.000   | 1.000        |

Determinism: every run1/run2 pair byte-identical (DIGEST match), at all three
scales including each 100x chunk. Final digests:
1x `8fd13d42...`, 10x `b5667953...`, 100x chunks `38b7962e...`,
`0cc295ad...`, `c2bb79a9...`, `60d07329...` (full values in run logs).

Wall-clock (prototype): 1x ~0.7s, 10x ~4.0s, 100x ~9.0s per chunk.
Linear scaling; no measured scale penalty versus baseline (timing is noisy;
both are linear in turns).

## Held-out verification (post-freeze, novel phrasing)

Generated AFTER the engine freeze with `gen_heldout.py`: 528 dialogues /
576 turns, 490 distinct questions, **zero overlap** with the frozen battery
(verified programmatically). Novel frames: "between X and Y, which is
taller?", "which stands taller, X or Y?", "did X come before N?",
"is X taller than N meters?", "is it true that X is not taller than Y?",
"did the author of W1 come earlier than the author of W2?",
"choose: did X come before or after Y?", "could X be taller than H?", etc.

Result: **576/576, every family 1.000**, byte-identical reruns
(DIGEST `02dba949...` both runs). Wall-clock ~2.2s for 528 dialogues.

### Honest incident report (held-out run 1)

The first held-out scoring showed HEIGHT at 0.750 (12/48). Investigation:
every failure was the template "tell me which is shorter, A or B?" — and in
every case **the engine's answer was correct and the oracle was wrong**: the
generator reused the taller-winner variable for a shorter question
(eiffel tower 330m vs montparnasse 210m: oracle expected "the eiffel tower is
shorter"). This was a harness bug, not an engine bug; the frozen engine was
not touched. The generator was fixed, the battery regenerated, and both
held-out runs were re-executed from scratch: 576/576. The initial failing
logs are superseded and were not committed.

## Binding verdict

1. **The existing native logic's shallow comparison path does not constitute
   general comparison reasoning.** Kill criterion fired decisively at 1x
   (overall 0.396; 7 families at 0.000).
2. **Dedicated comparison machinery is required.** The typed, compositional
   engine scores 1.000 on every family at 1x/10x/100x and 1.000 on a novel
   held-out battery, with byte-identical reruns at every scale.
3. **No scale degradation** in either system; both are linear in turns. The
   question was never about scale — it was about coverage, and the shallow
   path's coverage is narrow.
4. Zero randomness in all decision paths; all reruns byte-identical.

## Exact limitations

- The engine covers its implemented operator vocabulary: entity->dimension->
  value lookup (height/year), max/min/eq/neq, literal and comparative
  thresholds, negation scope over comparatives, author-of hop substitution,
  n-way superlatives, before-or-after disjunction, honest missing-attribute
  withhold, two-turn "those two" anaphora. Phrasing outside this vocabulary
  (e.g. "differ in height" without the word "different", multi-hop chains,
  other dimensions like population/area) is untested and likely unhandled.
- Entity universe is the frozen 5-heights / 14-time / 6-heightless /
  3-timeless / 3-works table; generalization to new entities was not tested.
- The held-out battery tests novel *frames*, not novel *semantics*: it stays
  within the preregistered operator set by design.
- Decisive-accuracy scoring grants paraphrase-equivalent winners; exact
  string match equals decisive match in every run above (all 1.000 exact).
- Timing is wall-clock on a shared VM and noisy; the claim is linearity,
  not a per-turn constant.
