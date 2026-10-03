#!/usr/bin/env python3
"""Round-3 final grids: O4 byte-after x position, R1 quote positions,
R5 no-exception grid, UTF-8/byte edges, O4/R1-heavy random."""
import random, sys

Q = []
def add(q): Q.append(q)

# O4: correction at positions x byte-after variants
frames = [
    "the correction{} moby dick?",
    "a correction{} moby dick?",
    "my correction{} moby dick?",
    "this correction{} moby dick?",
    "that correction{} moby dick?",
    "your correction{} moby dick?",
    "do you know the correction{}?",
    "do you know the correction{} moby dick?",
    "the correction{} moby dick, is wrong?",
    "is the correction{}?",
]
afters = [":", ",", ";", ".", "?", "!", " ", ""]
for f in frames:
    for a in afters:
        add(f.format(a))
# correction clause-initial with punctuation right after
for a in [":", ",", ";", ".", "?", "!", " "]:
    add(f"correction{a} moby dick?")

# R1: quote chars at every position around a trigger pair
base = "no, i meant moby dick?"
for i in range(len(base) + 1):
    add(base[:i] + '"' + base[i:])
    if i < len(base):
        add(base[:i] + "'" + base[i:])
# quote pairs
add('"no, i meant moby dick?"')
add("'no, i meant moby dick?'")
add("``no, i meant moby dick?''")

# R5 no-exception grid: no at clause positions x followers
for pre in ["", "oh ", "well ", "i said ", "there is "]:
    for foll in ["i", "we", "you", "no", "money", "way"]:
        add(f"{pre}no {foll} meant moby dick?")
        add(f"{pre}no, {foll} meant moby dick?")

# UTF-8 / byte edges
add("n\xc3\xa9, i meant moby dick?")       # né with accent
add("no, i meant mob\xc3\xbd dick?")       # moby with accent
add("\xe2\x80\x9cno, i meant moby dick?\xe2\x80\x9d")  # unicode quotes
add("no\xc2\xa0, i meant moby dick?")     # nbsp
add("no\xe2\x80\x99t i meant moby dick?")  # unicode apostrophe
add("caf\xc3\xa9 no, i meant moby dick?")

# long query (>96 tokens) - cap consistency
add(" ".join(["filler"] * 110) + " no, i meant moby dick?")
add("no, i meant moby dick? " + " ".join(["filler"] * 110))

# empty / degenerate
add("")
add("   ")
add("no")
add("meant")
add("correction")
add("actually")
add("?")
add(";;;")


# O4/R1-heavy random
rng = random.Random(31337)
arts = ["a", "the", "my", "this", "that", "your", "his", "our", ""]
puncts = [":", ",", ";", ".", "?", "!", " ", ""]
nouns = ["moby dick", "paris", "the louvre", "policy", "report"]
for _ in range(300):
    a = rng.choice(arts); p = rng.choice(puncts); n = rng.choice(nouns)
    lead = rng.choice(["", "do you know ", "is ", "about ", "the final ", "no, "])
    tail = rng.choice(["", f" {n}?", " is wrong?", f", {n}, is wrong?"])
    q = f"{lead}{a} correction{p}{tail}" if a else f"{lead}correction{p}{tail}"
    q = q.strip()
    if rng.random() < 0.25:
        i = rng.randint(0, len(q))
        q = q[:i] + rng.choice(['"', "'"]) + q[i:]
    add(q)

with open("/tmp/r3/fuzz_grid.txt", "w") as f:
    for q in Q:
        f.write(q + "\n")
print(f"wrote {len(Q)} grid queries")
