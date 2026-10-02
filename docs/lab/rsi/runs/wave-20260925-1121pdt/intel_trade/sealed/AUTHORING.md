# COMP-2 probe authoring record (wave-20260925-1121pdt)

Authored and sealed 2026-09-25, after prereg freeze (commit 5bf152b35),
before any implementation file existed.

## Method

Probes were drafted by hand from the 38-fact KB fixture, targeting pairs
of facts that share a gazetteer entity and jointly cover a compositional
question no single fact covers. Drafts were then verified by an
independent pure-Zag brute-force enumerator
(intel_trade/tools/pair_enum.zag), which implements the frozen F9-COMP
rule (shared gazetteer entity, union of stemmed content words covers the
probe, lexicographically lowest pair, no single-fact cover) using
byte-copied stemmer and stopword logic from the adopted source.

## Authoring checks (all pass)

A1. All 20 COMP probes: enumerator reports SINGLE=- (no single fact
    covers) and exactly one valid pair, which matches the intended pair
    recorded in KEY.md. (P3 reports a second valid pair (10,11); the
    frozen rule selects the lexicographically lowest, (8,10).)
A2. All 10 UNANS probes: enumerator reports SINGLE=- and PAIRS empty
    (no valid pair exists under the frozen rule).
A3. All probes are single-turn, single-line, within the frozen budget
    (<= 4 KB per turn), and avoid the frozen template phrases
    ("was the author of", "which is taller", " was written by ",
    " meters tall", " is in ", " in 18", " in 19", " did you ",
    " write ", " in paris", " in london", " write about ", " born in ").
A4. UNANS probes avoid the F9.2 template-adjacent decline patterns
    (no " did ... write ", no "how tall"/"how high", no "born ... in",
    no "did it win"/"win an"/"win the", no "become ... of").
A5. All probes use only entities present in the gazetteer fixture.

## SHA pins (authoring inputs)

Enumerator source:
  pair_enum.zag
  sha256: 56257e0746139b1c2fb9c736af5e0e24526fba19c83a580d0a1fadde4346062d
KB fixture (byte-identical to wave-20260925-0521pdt intel_trade impl runs):
  kb.txt
  sha256: 3ef27296c147a101eea0f093940cdbe1bb8be9fe58c21118119646aec6889be1
Gazetteer fixture (byte-identical to wave-20260925-0521pdt intel_trade impl runs):
  gaz.txt
  sha256: b75fd113dc7e2b3812d7a2b8819641ed2844926c64f33c74adc4ef8e5c85255a

Enumerator raw output (2026-09-25):
  P1 SINGLE=- PAIRS= 0,2
  P2 SINGLE=- PAIRS= 4,6
  P3 SINGLE=- PAIRS= 8,10 10,11
  P4 SINGLE=- PAIRS= 12,14
  P5 SINGLE=- PAIRS= 15,17
  P6 SINGLE=- PAIRS= 18,19
  P7 SINGLE=- PAIRS= 21,22
  P8 SINGLE=- PAIRS= 24,25
  P9 SINGLE=- PAIRS= 26,27
  P10 SINGLE=- PAIRS= 29,30
  P11 SINGLE=- PAIRS= 31,32
  P12 SINGLE=- PAIRS= 1,3
  P13 SINGLE=- PAIRS= 5,7
  P14 SINGLE=- PAIRS= 9,11
  P15 SINGLE=- PAIRS= 13,14
  P16 SINGLE=- PAIRS= 18,20
  P17 SINGLE=- PAIRS= 19,20
  P18 SINGLE=- PAIRS= 22,23
  P19 SINGLE=- PAIRS= 27,28
  P20 SINGLE=- PAIRS= 2,3
  P21-P30 SINGLE=- PAIRS= (empty)
