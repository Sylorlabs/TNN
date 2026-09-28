#!/usr/bin/env python3
"""Prototype of the frozen compositional classifier (training calibration).

Implements the exact rule that will be ported to pure Zag:
  JOKING  if (FRAME>=1 or ACTION>=1) and HARM>=1
  SATIRE  elif SAT>=2
  JOKING  elif TROPE>=2
  else    UNCERTAIN   (never SINCERE; default withholds)

Marker lists are curated from work/marker_analysis.json (training-only,
df>=4). Substring matching on folded text (Zag will do the same).
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))

FRAME = """tip pro hack life kitchen body tech stop forget everyone know knows
real ones""".split()
ACTION = """add mix stir put delete download stick get use save avoid fix come
spray squeeze rub gargle exfoliate pour""".split()
HARM = """glue bleach soap detergent paint antifreeze ammonia drain cleaner
laundry lemon garlic rattlesnake sandpaper deodorant wd-40 eyes cut cuts mouth
knees skin teeth face stomach insides bitten system32 fork toaster microwave
freezer keyboard dishwasher drill phone computer ram toast battery pipes grease
juice""".split()
SAT = """area sources confirm says experts inside resident details developing
press weigh study finds local time report full man woman peer pending review
story nobody""".split()
TROPE = """free ram upgrade ama findings joke pet downloaded traveler""".split()

def _is_alnum(c):
    return ('a' <= c <= 'z') or ('0' <= c <= '9')

def _has_word(hay, w):
    """Zag-faithful whole-word match: literal w with non-alnum boundaries."""
    if not w or len(w) > len(hay):
        return False
    i = 0
    while i <= len(hay) - len(w):
        if hay[i:i+len(w)] == w:
            ok = True
            if i > 0 and _is_alnum(hay[i-1]):
                ok = False
            if i + len(w) < len(hay) and _is_alnum(hay[i+len(w)]):
                ok = False
            if ok:
                return True
        i += 1
    return False

def count_hits(text, words):
    t = text.lower()
    hits = [w for w in words if _has_word(t, w)]
    return len(hits), hits

def classify(text):
    nf, hf = count_hits(text, FRAME)
    na, ha = count_hits(text, ACTION)
    nh, hh = count_hits(text, HARM)
    ns, hs = count_hits(text, SAT)
    nt, ht = count_hits(text, TROPE)
    if (nf + na >= 1) and nh >= 1:
        return "JOKING", hf + ha + hh
    if ns >= 2:
        return "SATIRE", hs
    if nt >= 2:
        return "JOKING", ht
    return "UNCERTAIN", []

def main():
    d = json.load(open(os.path.join(os.path.dirname(HERE), "corpus",
                                    "training_corpus.json")))
    items = d["items"]
    # calibration on training only: F1 recall, F2/F4 behavior, cross-family FP
    from collections import Counter
    res = Counter()
    for it in items:
        pred, _ = classify(it["title"] + " " + it["body"])
        res[(it["family"], pred)] += 1
    print("(family, pred) counts:")
    for k in sorted(res):
        print(f"  {k}: {res[k]}")
    f1 = [i for i in items if i["family"] == "F1"]
    rec = sum(1 for i in f1 if classify(i["title"] + " " + i["body"])[0] == "JOKING")
    print(f"F1 train recall (JOKING): {rec}/{len(f1)} = {rec/len(f1):.3f}")

if __name__ == "__main__":
    main()
