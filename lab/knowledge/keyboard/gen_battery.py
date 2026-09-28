#!/usr/bin/env python3
"""Deterministic battery generator for the keyboard-typo inference trial.

Glue only: the inference itself is pure Zag (run_battery.zag). This script
authors the word list, mirrors the QWERTY geometry (must match qwerty.zag
exactly - verified by selftest), and enumerates the battery deterministically.
No RNG anywhere: every item comes from exhaustive enumeration in a fixed order.

Battery kinds:
  S1 : single near-key substitution (kb cost tier 10 or 20), all positions,
       all near neighbors, alphabetical order.
  S2 : two adjacent-key substitutions (tier 10 only) at positions i<j,
       second error fixed to the alphabetically-first tier-10 neighbor
       (keeps the battery bounded while staying deterministic).
  RW : hand-authored real-world-style typos (transpositions, doublings,
       neighbor slips). Truths must all be in WORDS (asserted).
"""
import hashlib, os, sys

# ----------------------------------------------------------------------------
# QWERTY geometry mirror (quarter-key units; must match qwerty.zag exactly)
# ----------------------------------------------------------------------------
# Row strings with x of first key center, y of row:
#   q-row: x0=8,  y=4,  keys "qwertyuiop"  (x step 4)
#   a-row: x0=9,  y=8,  keys "asdfghjkl"
#   z-row: x0=11, y=12, keys "zxcvbnm"
GEO = {}
for i, ch in enumerate("qwertyuiop"):
    GEO[ch] = (8 + 4 * i, 4)
for i, ch in enumerate("asdfghjkl"):
    GEO[ch] = (9 + 4 * i, 8)
for i, ch in enumerate("zxcvbnm"):
    GEO[ch] = (11 + 4 * i, 12)

def kb_sub_cost(a, b):
    if a == b:
        return 0
    if a not in GEO or b not in GEO:
        return 40
    dx = GEO[a][0] - GEO[b][0]
    dy = GEO[a][1] - GEO[b][1]
    d2 = dx * dx + dy * dy
    if d2 <= 17:
        return 10
    if d2 <= 45:
        return 20
    if d2 <= 100:
        return 30
    return 40

def near_letters(c, max_cost):
    return sorted(n for n in GEO if n != c and kb_sub_cost(c, n) <= max_cost)

# ----------------------------------------------------------------------------
# Authored known-word list (the "word plausibility" knowledge).
# Alphabetical. All lowercase a-z, length 3..12.
# ----------------------------------------------------------------------------
WORDS = """about after again air also always animal answer any around ask back
because become before begin behind being below between book both boy bring
build called can change child city close cold come could country day did
different does done door down draw drink drive earth eat eight end enough
every example face fact fall far farm fast father feel feet few field find
fire first fish floor follow food form found four friend front full game gave
girl give going good great green ground group grow half hand happy hard has
have head hear heart heavy hello help here high home horse hot hour house
how however hundred idea into island just keep kind knew know large last
later laugh learn leave left less letter life light like line list little
live long look made make man many matter mean might mind minute miss money
month more morning most mother mountain move much music must name near
never night north now number often oil old once one only open order other
ought our over own page paper part people picture place plane plant play
point pound power press pretty print pull push put quick quiet quite rain
ran reach read ready real red river road rock room rose round rule run said
same say scale school science sea second seem seven shall shape share sharp
ship short should shoulder sick side since six size sleep small smile snow
some song soon sound south space speak speed spell spend stand start state
still stone stood story street strong study such summer sun table taken talk
teach tell ten than thank that their them then there these thick thing think
third those though thought three through throw tired today together told
took top toward town tree true try turn two under unit until use usual
very voice wait walk want war warm was wash water wave way week weight well
went were what when where which while white who whole whose why wide wife
will wind window wish with within without woman women wonder wood word work
world would write year yes yet young the and receive believe piece
separate definitely occurrence necessary tomorrow calendar argument coming
writing running happiness knowledge library february wednesday government
environment from broken words keyboard screen monitor program function
return input output error message language understand spelling written""".split()

# ----------------------------------------------------------------------------
# Hand-authored real-world-style typos: (typed, truth)
# ----------------------------------------------------------------------------
RW = [
    ("teh", "the"), ("hte", "the"), ("thw", "the"), ("tje", "the"),
    ("nad", "and"), ("adn", "and"), ("snd", "and"),
    ("wiht", "with"), ("wtih", "with"), ("wirh", "with"),
    ("becuase", "because"), ("becasue", "because"), ("brcause", "because"),
    ("recieve", "receive"), ("receove", "receive"),
    ("beleive", "believe"), ("belive", "believe"),
    ("freind", "friend"), ("friebd", "friend"),
    ("peice", "piece"),
    ("seperate", "separate"), ("seprate", "separate"),
    ("definately", "definitely"),
    ("occurrance", "occurrence"),
    ("neccessary", "necessary"),
    ("tommorow", "tomorrow"),
    ("calender", "calendar"),
    ("arguement", "argument"),
    ("comming", "coming"), ("ciming", "coming"),
    ("writting", "writing"),
    ("runing", "running"),
    ("happyness", "happiness"),
    ("knowlege", "knowledge"),
    ("libary", "library"),
    ("febuary", "february"),
    ("wensday", "wednesday"),
    ("goverment", "government"),
    ("enviroment", "environment"),
    ("sould", "should"), ("shoudl", "should"),
    ("woudl", "would"),
    ("coudl", "could"),
    ("thier", "their"),
    ("form", "from"),
    ("qiuck", "quick"), ("quicj", "quick"),
    ("borken", "broken"),
    ("wrods", "words"), ("worda", "words"),
    ("keybaord", "keyboard"), ("keyboarf", "keyboard"),
    ("scrren", "screen"), ("scren", "screen"),
    ("mointor", "monitor"),
    ("progam", "program"), ("prgram", "program"),
    ("funtion", "function"),
    ("reutrn", "return"),
    ("inptu", "input"),
    ("ouput", "output"),
    ("eror", "error"),
    ("mesage", "message"),
    ("languag", "language"),
    ("undertsand", "understand"),
    ("speling", "spelling"),
    ("writen", "written"),
]

def main():
    words = sorted(set(WORDS))
    assert all(w.isalpha() and w.islower() and 3 <= len(w) <= 12 for w in words), "word list hygiene"
    assert len(words) == len(WORDS), "duplicate in WORDS"
    wordset = set(words)
    for typed, truth in RW:
        assert truth in wordset, f"RW truth not in word list: {truth}"
        assert typed != truth, f"RW typed==truth: {typed}"
        assert typed.isalpha() and typed.islower(), f"RW typed hygiene: {typed}"

    outdir = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(outdir, exist_ok=True)

    with open(os.path.join(outdir, "words.txt"), "w") as f:
        f.write("\n".join(words) + "\n")

    items = []  # (typed, truth, kind)
    collisions = 0
    # S1: single near-key substitution (tiers 10 and 20)
    for w in words:
        for i, c in enumerate(w):
            for n in near_letters(c, 20):
                typed = w[:i] + n + w[i + 1:]
                if typed in wordset:
                    collisions += 1
                items.append((typed, w, "S1"))
    # S2: two adjacent-key substitutions (tier 10), second error = alpha-first
    for w in words:
        L = len(w)
        for i in range(L):
            n1s = near_letters(w[i], 10)
            for n1 in n1s:
                for j in range(i + 1, L):
                    n2s = near_letters(w[j], 10)
                    if not n2s:
                        continue
                    n2 = n2s[0]
                    typed = w[:i] + n1 + w[i + 1:j] + n2 + w[j + 1:]
                    if typed in wordset:
                        collisions += 1
                    items.append((typed, w, "S2"))
    # RW
    for typed, truth in RW:
        if typed in wordset:
            collisions += 1
        items.append((typed, truth, "RW"))

    with open(os.path.join(outdir, "items.txt"), "w") as f:
        for typed, truth, kind in items:
            f.write(f"{typed}\t{truth}\t{kind}\n")

    h = hashlib.sha256()
    with open(os.path.join(outdir, "items.txt"), "rb") as f:
        h.update(f.read())
    n1 = sum(1 for _, _, k in items if k == "S1")
    n2 = sum(1 for _, _, k in items if k == "S2")
    n3 = sum(1 for _, _, k in items if k == "RW")
    print(f"WORDS {len(words)}")
    print(f"S1 {n1}")
    print(f"S2 {n2}")
    print(f"RW {n3}")
    print(f"TOTAL {len(items)}")
    print(f"COLLISIONS {collisions}")
    print(f"ITEMS_SHA256 {h.hexdigest()}")

if __name__ == "__main__":
    main()
