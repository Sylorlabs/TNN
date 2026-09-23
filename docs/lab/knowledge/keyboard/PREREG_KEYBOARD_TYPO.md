# PREREG — Keyboard-geometry typo inference vs keyboard-blind baseline

Frozen 2026-09-22, before battery execution. This prereg may not be edited
after the battery runs; any deviation is reported as a defect, not silently
absorbed.

## Question

Does QWERTY keyboard-geometry knowledge improve typo→intent recovery over a
keyboard-blind edit-distance baseline? (Micah's order: bake keyboard-format
knowledge into TNN so it can infer the most likely intended letter/word from
typos — logic, not memorized corrections.)

## Knowledge under test

`qwerty.zag` (sha256 b9c57a83b709b4665524ad53d14a110b2fa8f7bd97de8d365deb29026deb309e):
key centers in quarter-key units, standard US-ANSI stagger (q-row y=4 x=8+4i;
a-row y=8 x=9+4i; z-row y=12 x=11+4i). Substitution cost from squared
Euclidean distance d2 of key centers, in tenths:

- d2 = 0        -> 0
- d2 in 1..17   -> 10  (adjacent incl. diagonals)
- d2 in 18..45  -> 20  (near / stagger-diagonal)
- d2 in 46..100 -> 30  (two keys over)
- d2 > 100      -> 40  (far)
- either char outside a-z -> 40

Uppercase = same keys (lowercase before querying). Digits/punctuation and
non-QWERTY layouts are NOT encoded (see KEYBOARD_KNOWLEDGE.md).

## Inference rule (frozen)

For typed string T, each candidate word W (from the frozen known-word list)
is scored by restricted-Damerau edit distance with:

- substitution(a,b): keyboard table above (method KB) vs uniform
  (0 if a=b else 10) (method BL)
- insertion = deletion = 15 (both methods)
- adjacent transposition = 10 (both methods; restricted/optimal-string-alignment form)

Both methods share the DP, the constants, and the candidate set, so the
head-to-head isolates EXACTLY the substitution-cost table — i.e., the
keyboard knowledge. (The baseline includes transposition deliberately: the
question is whether geometry adds anything beyond blind edit distance, not
whether transposition handling does.)

Ranking: score ascending, tie-break by word-list order ascending (the list
is alphabetical). rank(truth) = 1 + #{candidates strictly better, or equal
score but earlier in list order}. Top-1 = rank 1.

Character-level (diagnostic): for S1 items, let c = typed char at the single
differing position, t = truth char. Rank t among all 26 letters by
(kb_sub_cost(c,.), alphabetical). Note c itself always ranks first
(cost 0) — the ranking is a likelihood ordering, not a verdict.

Word plausibility = membership in the known-word list only. No frequency
priors.

## Battery (frozen construction; generated AFTER this prereg)

Generator: `gen_battery.py`
(sha256 42e3a2339c0f7f1e65e72901fc6319177f82d9cafbb79824c6ad87bbdae8a533).
Word list: `words.txt`, 392 authored common words, alphabetical, all
lowercase a-z length 3..12
(sha256 921db28f73143d7c0bfd1f30796a6007e0907f27b7813b123de6a0442d348153).

- S1 (single near-key substitution): every word × every position × every
  neighbor with kb cost ≤ 20 (alphabetical), typed = one substitution.
  N = 9,398.
- S2 (two adjacent-key errors): every word × position i × tier-10 neighbor
  at i × position j>i × alphabetically-first tier-10 neighbor at j.
  N = 10,566.
- RW (real-world-style): 67 hand-authored typos (transpositions, doublings,
  neighbor slips, e.g. teh->the, becuase->because, keybaord->keyboard).
  Every truth asserted in the word list.

Total N = 20,031. 50 items are "collisions" (the typed string is itself a
different list word); both methods necessarily miss those — they bound the
achievable top-1 from above and affect both methods equally.

Enumeration is exhaustive and deterministic; no RNG anywhere.

## Metrics

Per kind (S1/S2/RW) and overall, per method (KB/BL):
- top-1 rate = fraction with rank(truth) = 1
- top-3 rate = fraction with rank(truth) ≤ 3
Character-level on S1: top-1/top-3 rate of the truth char.

## Kill bar

PASS iff KB top-1 rate > BL top-1 rate on EACH of S1, S2, and RW
separately. If KB fails on any kind, verdict = FAIL with the boundary named.
(Character-level rates are diagnostic; no kill bar.)

## Determinism

The battery binary (`run_battery.zag`, pure Zag, zero RNG) runs twice on the
frozen `items.txt`; the two results files must be byte-identical, else the
run is invalid.

## Pre-freeze validation (allowed)

`qwerty.zag` geometry was verified against the Python mirror by self-test
(all 26 key coordinates + 9 cost probes match). `run_battery.zag` was
smoke-tested on a 4-item scratch battery with hand-verified results. One bug
was found and fixed before freezing: the truth-index search compared the
wrong buffers (would have silently mis-ranked); caught by a bounds panic on
the scratch battery. No battery items were executed before this freeze.
