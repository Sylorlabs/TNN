#!/usr/bin/env python3
"""Round-3 randomized combinatorial fuzzer: multi-sentence, multi-trigger,
blocker-stacking templates over fresh token pools."""
import random, sys
sys.path.insert(0, "/tmp/r3")

verbs = ["said", "told", "claimed", "mentioned", "thinks", "reported", "asked"]
subjs = ["she", "he", "they", "my friend", "the teacher", "john", "i", "we",
         "the man", "mary", "my very good friend", "nobody"]
conds = ["if", "suppose", "whether", "unless", "assuming"]
hedges = ["maybe", "perhaps", "could", "possibly"]
negs = ["never", "not", "had not", "hadn't", "didn't"]
fillers = ["moby dick", "the whaling tale", "paris", "france capital",
           "pride and prejudice", "the louvre", "melville", "austen"]
parts = ["well", "oh", "uh", "so", "right", "hmm"]
seps = ["; ", ". ", "? ", "! ", ", ", " ", "\n"]

def sent(rng):
    kind = rng.random()
    f = rng.choice(fillers)
    if kind < 0.30:
        # reported-ish
        s = rng.choice(subjs); v = rng.choice(verbs)
        return f"{s} {v} no, i meant {f}?"
    elif kind < 0.45:
        c = rng.choice(conds)
        return f"{c} i meant {f}, would you agree?"
    elif kind < 0.55:
        h = rng.choice(hedges)
        return f"{h} i meant {f}?"
    elif kind < 0.65:
        n = rng.choice(negs)
        return f"i {n} meant {f}?"
    elif kind < 0.75:
        p = rng.choice(parts)
        return f"{p}, no, i meant {f}?"
    elif kind < 0.85:
        return f"correction: {f}?"
    else:
        return f"no, i meant {f}?"

def query(rng):
    n = rng.randint(1, 3)
    ss = [sent(rng) for _ in range(n)]
    out = ss[0]
    for s in ss[1:]:
        out += rng.choice(seps) + s
    # random quote wrapping
    r = rng.random()
    if r < 0.12:
        out = '"' + out
        if rng.random() < 0.7:
            out += '"'
    elif r < 0.2:
        i = rng.randint(0, max(0, len(out) - 8))
        out = out[:i] + "'" + out[i:]
    return out

rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 7)
N = int(sys.argv[2]) if len(sys.argv) > 2 else 400
with open("/tmp/r3/fuzz_rand.txt", "w") as f:
    for _ in range(N):
        q = query(rng).replace("\n", "\\n")
        f.write(q + "\n")
print(f"wrote {N} randomized queries")
