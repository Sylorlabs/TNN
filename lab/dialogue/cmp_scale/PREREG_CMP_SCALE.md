# PREREG — Comparison Engine vs Native Logic, at Probe Scale

Date: 2026-09-23. Status: FROZEN (committed before any probe generation or runs).
Program: TNN native-lab, branch `tnn-native-lab`.
Method note: Micah's final name for the paradigm is **guided learning (gl)**;
this trial follows the gl shape (frozen prereg → build → held-out verify).

## Question

Micah: "does TNN need a comparison engine or was logic able to save it?"
Plus: "what happens when we scale up probes?"

Background: the round-2 dialogue repair (18/18, 44/44 held-out) added
comparison handling via a keyword-scan + marker-lookup path (`do_compare` in
the integrated `dialogue.zag`). That machinery was proven only on a small
probe set. Open: whether it generalizes to new comparison families and to
large probe counts, or whether a dedicated, principled comparison engine
(typed attribute values, operators, negation scope, multi-hop chains, n-way
reduction) is required.

## Baseline under test (frozen, unmodified)

`dialogue/round2_repair/integrated/dialogue.zag` — the current native logic
machinery, byte-identical to the committed integrated build. It is copied,
never edited, into `dialogue/cmp_scale/baseline/`. The binary is rebuilt
from that copy with the pinned toolchain
(`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`).

## Probe families (11) and oracle semantics

All probes are single-turn `DIALOGUE <id> COMPOSE` blocks (`U`/`E`), except
ANA (two turns). All questions lowercase. Expected answers are computed by
the generator from an independent entity/attribute table (never from the
Zag code). Every probe is answerable from the KB by a competent comparison
reasoner; every expected answer is unique.

Entity attributes (from the frozen kb.txt):
- HEIGHT (meters): eiffel tower 330, montparnasse tower 210,
  statue of liberty 93, big ben 96, mount everest 8849
- YEAR: persons→born {herman melville 1819, jane austen 1775,
  charles darwin 1809, marie curie 1867, andy weir 1972};
  towers→built {eiffel tower 1889, montparnasse tower 1973};
  works→published {moby dick 1851, pride and prejudice 1813,
  on the origin of species 1859, the martian 2011};
  colosseum→completed 80; statue of liberty→dedicated 1886;
  louvre→opened 1793
- AUTHOR: moby dick→herman melville, pride and prejudice→jane austen,
  on the origin of species→charles darwin, the martian→andy weir
- "the "-prefix rule (mirrors `needs_the`): eiffel tower, montparnasse
  tower, statue of liberty, louvre, colosseum. All others: no "the".

| # | Family | Shape | Decisive oracle |
|---|--------|-------|-----------------|
| 1 | HEIGHT | comparatives taller/shorter, yes/no + which-winner, height pairs | correct yes/no, or correct winner + max/min direction |
| 2 | TIME | before/after/earlier/later/older/younger/first/last, yes/no + which-winner, same- and cross-marker year pairs | correct yes/no, or correct winner + min/max direction |
| 3 | SUP3 | 3-way superlatives: tallest/shortest of 3 heights; first/last of 3 years | correct winner of all 3 + direction |
| 4 | MORELESS | comparatives outside the engine's keyword list: higher/lower on heights, yes/no + which-winner | correct yes/no, or correct winner + direction |
| 5 | THRESH | threshold vs literal: "is A more/less than N meters tall?", "was A born/built before/after N?" (N = value ± {1,10,100}, N>0) | correct yes/no |
| 6 | SAME | same/different: "were A and B born in the same year?" → no; "...different years?" → yes; "are A and B the same height?" → no (all KB pairs distinct — asserted in generator) | correct yes/no |
| 7 | NEG | negation + comparison: "is A not taller than B?", "was A not born before B?" (yes/no only) | correct yes/no = NOT(unnegated outcome) |
| 8 | HOP | HOP1 (control): "was the author of \<work\> born before/after \<person\>?"; HOP2: "was the author of \<workA\> born before/after the author of \<workB\>?" | correct yes/no from author birth years |
| 9 | BEFOREAFTER | "was A \<mkA\> before or after B \<mkB\>?" (both dates in KB) | "before." iff yearA < yearB else "after." |
| 10 | UNKNOWN | comparison on missing attribute: height-q with heightless entity; time-q with timeless entity | "I don't know." |
| 11 | ANA | two-turn: T1 "which is taller, A or B?" then T2 "which of those two came first?" (pairs with both height+time) | T1: correct winner + max; T2: correct winner + min |

## Scales

- 1x = 88 probes (8/family), 10x = 880 (80/family), 100x = 8800 (800/family).
- Generation is fully deterministic: combinatorial cycling over entity
  combos × phrasing templates by index. No `random` module, no seeds, no
  RNG anywhere. The generator is test harnessing (Python); the decision
  path under test is the pure-Zag binary.
- Harness limit (found in code review, preregistered here): the batch
  runner's `dacc` digest accumulator is 131072 bytes with no bounds check,
  so one run holds ≈4300 responses max. The 100x battery therefore runs as
  4 chunks of 2200 (100x-p1..p4). Chunking changes no behavior: per-DIALOGUE
  state (sal/top/uc/hist/pqb/histb, pv slots 0/28) resets each DIALOGUE, and
  no probe reads cross-DIALOGUE state except ANA T2, which always follows
  its own T1. (pv 40/44 — the compared-pair slots — intentionally persist
  across DIALOGUEs; no single-turn probe reads them.)

## Metrics

- PRIMARY — **decisive accuracy**: the response conveys the correct
  comparison outcome. yes/no, before./after., and I-don't-know families:
  exact string. Winner families: winner's canonical name present AND the
  direction class matches (max: taller/tallest/higher; min: shorter/
  shortest/lower; time-min: first; time-max: last). Reported per family
  per scale, and overall per scale.
- SECONDARY — exact-match accuracy vs the canonical expected string.
- SCALE — wall time per run, ms/probe, and run1-vs-run2 DIGEST equality
  (byte-identical reruns required) at every scale.
- The scorer is deterministic Python over the `T`/`A` log lines.

## Kill criterion (frozen)

**"Comparison engine NEEDED"** iff, on the unmodified baseline:
- decisive accuracy < 0.90 on ANY family at 1x, OR
- decisive accuracy drops > 0.03 absolute from 1x → 100x on ANY family, OR
- overall decisive accuracy < 0.90 at 100x.

Otherwise the verdict is **"native logic suffices"** (with per-family
scores reported, including any weak-but-passing families).

## If the kill fires

Prototype a dedicated comparison engine in pure Zag as a cleanroom fork of
the integrated `dialogue.zag` (comparison path only; pipeline and battery
format unchanged): typed attribute model (entity → dimension → i32 value),
operator mapping (comparatives, superlatives, same/different, thresholds vs
literals), negation scope ("not" flips the outcome), multi-hop resolution
(work → author → attribute, recursive), n-way entity collection for
superlatives, before-or-after disjunction answers. Then:
- dev-test on 1x, verify on 10x and 100x (same batteries),
- verify on a HELD-OUT battery (novel phrasing templates, generated AFTER
  the prototype is frozen),
- claim the delta only if prototype decisive ≥ 0.99 on every family at
  every scale AND on held-out, with byte-identical reruns.

## Preregistered predictions (not bars)

HEIGHT/TIME/UNKNOWN/ANA near 1.0 decisive; SUP3, MORELESS, THRESH, SAME,
NEG, BEFOREAFTER near 0; HOP1 high, HOP2 partial. Accuracy flat across
scales (per-DIALOGUE state resets); runtime linear in probe count.

## Commit order

1. This prereg (alone). 2. Generator + batteries. 3. Baseline build +
   run logs (run1/run2 per scale). 4. Verdict + (if kill fires) prototype
   engine + its logs. 5. Final VERDICT_CMP_SCALE.md.
