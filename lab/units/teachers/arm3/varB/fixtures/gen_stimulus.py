#!/usr/bin/env python3
"""Generate the fixed stimulus for arm-3 varB verification.

Deterministic prose (~3.6KB). The opening vocabulary repeats heavily so
CORROBORATE always finds >=2 additional occurrences for early adopted units.
Output: fixtures/stimulus.txt
"""
import os

LINES = [
 "the river runs past the old stone bridge every morning",
 "the river carries light down from the high valley",
 "the old stone bridge spans the river where the path bends",
 "morning light strikes the stone and the water answers",
 "the valley holds the river like a hand holds water",
 "every stone in the river knows the weight of water",
 "the path bends past the bridge into the low valley",
 "light moves over water faster than the wind moves",
 "the wind bends the grass along the river path",
 "old trees lean over the water near the stone bridge",
 "every morning the valley fills with light and bird song",
 "the river path runs under old trees to the far hill",
 "stone steps climb the hill past the tall grass",
 "the hill looks down on the river and the valley",
 "light lingers on the hill long after the valley dims",
 "the wind carries bird song from the hill to the river",
 "water finds the low path through stone and grass",
 "the old path follows water from the hill to the bridge",
 "every bridge needs stone and every stone needs water",
 "morning wind moves light across the valley floor",
 "the valley floor holds water after the night rain",
 "night rain fills the river and the river fills the valley",
 "the stone bridge stands over the rising water",
 "light breaks over the hill and strikes the bridge",
 "the river answers light with moving water",
 "old grass bends under the morning wind",
 "the path through grass leads past stone to water",
 "every tree near the river leans toward the light",
 "bird song follows the river path at morning",
 "the far hill catches light before the valley wakes",
 "water over stone makes the only music the valley needs",
 "the valley needs water the way the hill needs light",
 "old stone holds morning light longer than water holds it",
 "the bridge holds its shadow on the moving water",
 "every shadow on water moves with the river",
 "the river moves past stone past grass past light",
 "wind over water lifts light into the old trees",
 "the trees along the path shelter the river walkers",
 "walkers cross the old bridge at morning light",
 "the morning walkers watch water move under stone",
 "stone under water wears smooth where the river runs",
 "the river runs smooth and fast past the low valley",
 "fast water finds every stone in its path",
 "the low valley gathers light like water gathers stone",
 "light gathers on water where the river slows",
 "the river slows past the bridge and the valley widens",
 "the wide valley holds the slow river and the old path",
 "old paths remember every walker the river forgets",
 "the river forgets nothing the valley teaches it",
 "morning teaches the valley how light moves on water",
 "how water moves the valley learns from the river",
 "the stone bridge teaches walkers to look at water",
 "walkers look at water and the water looks back",
 "still water under the bridge holds the whole valley",
 "the whole valley fits inside the morning light",
]

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    text = "\n".join(LINES) + "\n"
    # verify: first 16 distinct words each occur >= 3 times (word-boundary)
    import re
    words = re.findall(r"[A-Za-z0-9_]{3,}", text)
    seen, first16 = set(), []
    for w in words:
        if w not in seen:
            seen.add(w)
            first16.append(w)
        if len(first16) == 16:
            break
    # verify: distinct words among the first 12 tokens (covers the first
    # INTRODUCE batch of 8) each occur >= 3 times (word-boundary) so
    # CORROBORATE (needs m>=3) and appeals (need m>=nprop+2) always qualify.
    toks = words[:12]
    tseen, firstt = set(), []
    for w in toks:
        if w not in tseen:
            tseen.add(w)
            firstt.append(w)
    occ = {}
    for w in words:
        occ[w] = occ.get(w, 0) + 1
    bad = [(w, occ.get(w, 0)) for w in firstt if occ.get(w, 0) < 3]
    assert not bad, f"early words with <3 occurrences: {bad}"
    p = os.path.join(here, "stimulus.txt")
    with open(p, "wb") as f:
        f.write(text.encode())
    print(f"wrote {p} ({len(text)} bytes)")
    print("first12-distinct:", [(w, occ[w]) for w in firstt])

if __name__ == "__main__":
    main()
