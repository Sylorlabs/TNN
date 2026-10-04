#!/usr/bin/env python3
"""Score RT2d runs against oracle labels."""
TAG = {"AFFIRM": 1, "DENY": 2, "NEUTRAL": 0}
INV = {1: "AFFIRM", 2: "DENY", 0: "NEUTRAL"}

def load_corpus(path, ceiling_col):
    items = {}
    with open(path) as f:
        for line in f:
            p = line.rstrip("\n").split("\t")
            items[p[0]] = {"claim": p[1], "title": p[2], "snippet": p[3],
                           "oracle": p[4],
                           "ceiling": (p[5] == "CEILING") if ceiling_col else False}
    return items

def load_out(path):
    out = {}
    with open(path) as f:
        for line in f:
            p = line.rstrip("\n").split(" ", 2)
            out[p[0]] = (int(p[1]), p[2] if len(p) > 2 else "")
    return out

def score(cpath, opath, ceiling_col, family):
    items = load_corpus(cpath, ceiling_col)
    out = load_out(opath)
    assert set(items) == set(out), "id mismatch"
    hits, ceil_hits = [], []
    for i, it in items.items():
        tag, reason = out[i]
        exp = TAG[it["oracle"]]
        if tag != exp:
            rec = (i, it["claim"], it["snippet"], it["oracle"], INV[tag], reason, it["ceiling"])
            (ceil_hits if it["ceiling"] else hits).append(rec)
    print(f"== {family}: {len(items)} items ==")
    print(f"  oracle-matches: {len(items)-len(hits)-len(ceil_hits)}/{len(items)}")
    print(f"  mechanism hits: {len(hits)}  ceiling hits: {len(ceil_hits)}")
    for h in hits + ceil_hits:
        mark = "[CEILING]" if h[6] else "[MECH]"
        print(f"  {mark} {h[0]} oracle={h[3]} got={h[4]} ({h[5]})")
        print(f"       claim: {h[1]}")
        print(f"       ev:    {h[2]}")
    return hits, ceil_hits

ha, ca = score("corpus_rta.tsv", "run_rta_out1.txt", False, "RT-A")
hb, cb = score("corpus_rtb.tsv", "run_rtb_out1.txt", True, "RT-B")
print()
print("K-RTA (need >=3 MECH false-affirms to FAIL):", len([h for h in ha if h[4]=="AFFIRM"]))
print("K-RTB (non-ceiling oracle mismatches):", len(hb))
