#!/usr/bin/env python3
"""Deterministic probe generator for cmp_scale.

No random module, no seeds, no RNG anywhere. Probe i of a family =
pool[i % len(pool)]: combinatorial cycling over entity combos x phrasings.

Writes:
  battery_1x.txt        88 probes  (8/family)
  battery_10x.txt       880 probes (80/family)
  battery_100x_p1..p4   4 x 2200 = 8800 probes (800/family, global IDs)
  oracle.jsonl          one line per (dialogue id, turn) with oracle data
  GENERATOR_NOTES.md    design decisions (incl. SUP3 winner-last ordering)

Battery format matches the dialogue batch runner:
  DIALOGUE <id> COMPOSE / U <turn> / E <expected> / END
"""
import json
import os

OUT = os.path.dirname(os.path.abspath(__file__))

THE_PREFIX = {"eiffel tower", "montparnasse tower", "statue of liberty",
              "louvre", "colosseum"}

def qn(name):
    return ("the " + name) if name in THE_PREFIX else name

def rn(name):
    # response rendering mirrors needs_the in dialogue.zag
    return ("the " + name) if name in THE_PREFIX else name

HEIGHTS = [("eiffel tower", 330), ("montparnasse tower", 210),
           ("statue of liberty", 93), ("big ben", 96),
           ("mount everest", 8849)]

TIME = [
    ("herman melville", "born", 1819), ("jane austen", "born", 1775),
    ("charles darwin", "born", 1809), ("marie curie", "born", 1867),
    ("andy weir", "born", 1972),
    ("eiffel tower", "built", 1889), ("montparnasse tower", "built", 1973),
    ("moby dick", "published", 1851), ("pride and prejudice", "published", 1813),
    ("on the origin of species", "published", 1859),
    ("the martian", "published", 2011),
    ("colosseum", "completed", 80), ("statue of liberty", "dedicated", 1886),
    ("louvre", "opened", 1793),
]

WORKS_AUTH = [("moby dick", "herman melville", 1819),
              ("pride and prejudice", "jane austen", 1775),
              ("on the origin of species", "charles darwin", 1809),
              ("the martian", "andy weir", 1972)]
PERSONS = [(n, y) for (n, y) in
           [("herman melville", 1819), ("jane austen", 1775),
            ("charles darwin", 1809), ("marie curie", 1867),
            ("andy weir", 1972)]]

HEIGHTLESS = ["louvre", "colosseum", "herman melville", "jane austen",
              "moby dick", "amazon river"]
TIMELESS = ["big ben", "amazon river", "mount everest"]


def ordered_pairs(items):
    return [(a, b) for a in items for b in items if a != b]


def ordered_triples(items):
    return [(a, b, c) for a in items for b in items for c in items
            if len({id(a), id(b), id(c)}) == 3]


# Each probe = list of turns; turn = dict(question, expected, dec, winner, dir, dim)
def P1(q, e, dec, winner=None, d=None, dim=None):
    return [{"q": q, "e": e, "dec": dec, "winner": winner, "dir": d, "dim": dim}]


def fam_height():
    pool = []
    for (a, ha), (b, hb) in ordered_pairs(HEIGHTS):
        wa, wb = rn(a), rn(b)
        pool.append(P1(f"is {qn(a)} taller than {qn(b)}?",
                      "yes." if ha > hb else "no.", "yn"))
        pool.append(P1(f"is {qn(a)} shorter than {qn(b)}?",
                      "yes." if ha < hb else "no.", "yn"))
        w = a if ha > hb else b
        pool.append(P1(f"which is taller, {qn(a)} or {qn(b)}?",
                      f"{rn(w)} is taller.", "winner", w, "max", "H"))
        w = a if ha < hb else b
        pool.append(P1(f"which is shorter, {qn(a)} or {qn(b)}?",
                      f"{rn(w)} is shorter.", "winner", w, "min", "H"))
        w = a if ha > hb else b
        pool.append(P1(f"which of {qn(a)} and {qn(b)} is taller?",
                      f"{rn(w)} is taller.", "winner", w, "max", "H"))
        pool.append(P1(f"is {qn(b)} taller than {qn(a)}?",
                      "yes." if hb > ha else "no.", "yn"))
    return pool


def fam_time():
    pool = []
    allp = ordered_pairs(TIME)
    for (a, mka, ya), (b, mkb, yb) in allp:
        pool.append(P1(f"was {qn(a)} {mka} before {qn(b)} {mkb}?",
                      "yes." if ya < yb else "no.", "yn"))
        pool.append(P1(f"was {qn(a)} {mka} after {qn(b)} {mkb}?",
                      "yes." if ya > yb else "no.", "yn"))
        w, wmk = (a, mka) if ya < yb else (b, mkb)
        pool.append(P1(f"which came first, {qn(a)} or {qn(b)}?",
                      f"{rn(w)} was {wmk} first.", "winner", w, "min", "T"))
        w, wmk = (a, mka) if ya > yb else (b, mkb)
        pool.append(P1(f"which came last, {qn(a)} or {qn(b)}?",
                      f"{rn(w)} was {wmk} last.", "winner", w, "max", "T"))
    # same-marker pairs: older/younger/earlier/later phrasings
    by_mk = {}
    for t in TIME:
        by_mk.setdefault(t[1], []).append(t)
    for mk, group in by_mk.items():
        for (a, _, ya), (b, _, yb) in ordered_pairs(group):
            pool.append(P1(f"was {qn(a)} older than {qn(b)}?",
                          "yes." if ya < yb else "no.", "yn"))
            pool.append(P1(f"was {qn(a)} younger than {qn(b)}?",
                          "yes." if ya > yb else "no.", "yn"))
            pool.append(P1(f"was {qn(a)} earlier than {qn(b)}?",
                          "yes." if ya < yb else "no.", "yn"))
            pool.append(P1(f"was {qn(a)} later than {qn(b)}?",
                          "yes." if ya > yb else "no.", "yn"))
    return pool


def fam_sup3():
    pool = []
    # height triples: winner placed LAST (defeats pairwise-leftmost)
    for (a, ha), (b, hb), (c, hc) in ordered_triples(HEIGHTS):
        vals = [(a, ha), (b, hb), (c, hc)]
        wmax = max(vals, key=lambda t: t[1])[0]
        wmin = min(vals, key=lambda t: t[1])[0]
        others_max = [n for n, _ in vals if n != wmax]
        others_min = [n for n, _ in vals if n != wmin]
        A, B = others_max[0], others_max[1]
        pool.append(P1(f"which is the tallest of {qn(A)}, {qn(B)}, and {qn(wmax)}?",
                      f"{rn(wmax)} is tallest.", "winner", wmax, "max", "H"))
        A, B = others_min[0], others_min[1]
        pool.append(P1(f"which is the shortest of {qn(A)}, {qn(B)}, and {qn(wmin)}?",
                      f"{rn(wmin)} is shortest.", "winner", wmin, "min", "H"))
    # person triples (born)
    for (a, ya), (b, yb), (c, yc) in ordered_triples(PERSONS):
        vals = [(a, ya), (b, yb), (c, yc)]
        wmin = min(vals, key=lambda t: t[1])[0]
        wmax = max(vals, key=lambda t: t[1])[0]
        om = [n for n, _ in vals if n != wmin]
        ox = [n for n, _ in vals if n != wmax]
        pool.append(P1(f"who was born first of {qn(om[0])}, {qn(om[1])}, and {qn(wmin)}?",
                      f"{rn(wmin)} was born first.", "winner", wmin, "min", "T"))
        pool.append(P1(f"who was born last of {qn(ox[0])}, {qn(ox[1])}, and {qn(wmax)}?",
                      f"{rn(wmax)} was born last.", "winner", wmax, "max", "T"))
    # cross-marker triples: every 3rd ordered triple of TIME
    trips = ordered_triples(TIME)[::3]
    for (a, mka, ya), (b, mkb, yb), (c, mkc, yc) in trips:
        vals = [(a, mka, ya), (b, mkb, yb), (c, mkc, yc)]
        wmin = min(vals, key=lambda t: t[2])
        wmax = max(vals, key=lambda t: t[2])
        om = [t for t in vals if t[0] != wmin[0]]
        ox = [t for t in vals if t[0] != wmax[0]]
        pool.append(P1(
            f"which came first, {qn(om[0][0])}, {qn(om[1][0])}, or {qn(wmin[0])}?",
            f"{rn(wmin[0])} was {wmin[1]} first.", "winner", wmin[0], "min", "T"))
        pool.append(P1(
            f"which came last, {qn(ox[0][0])}, {qn(ox[1][0])}, or {qn(wmax[0])}?",
            f"{rn(wmax[0])} was {wmax[1]} last.", "winner", wmax[0], "max", "T"))
    return pool


def fam_moreless():
    pool = []
    for (a, ha), (b, hb) in ordered_pairs(HEIGHTS):
        pool.append(P1(f"is {qn(a)} higher than {qn(b)}?",
                      "yes." if ha > hb else "no.", "yn"))
        pool.append(P1(f"is {qn(a)} lower than {qn(b)}?",
                      "yes." if ha < hb else "no.", "yn"))
        w = a if ha > hb else b
        pool.append(P1(f"which is higher, {qn(a)} or {qn(b)}?",
                      f"{rn(w)} is higher.", "winner", w, "max", "H"))
        w = a if ha < hb else b
        pool.append(P1(f"which is lower, {qn(a)} or {qn(b)}?",
                      f"{rn(w)} is lower.", "winner", w, "min", "H"))
    return pool


def fam_thresh():
    pool = []
    for name, h in HEIGHTS:
        for d in (1, 10, 100):
            pool.append(P1(f"is {qn(name)} more than {h + d} meters tall?", "no.", "yn"))
            pool.append(P1(f"is {qn(name)} more than {h - d} meters tall?", "yes.", "yn"))
            pool.append(P1(f"is {qn(name)} less than {h + d} meters tall?", "yes.", "yn"))
            pool.append(P1(f"is {qn(name)} less than {h - d} meters tall?", "no.", "yn"))
    for name, mk, year in TIME:
        for d in (1, 10, 100):
            if year - d > 0:
                pool.append(P1(f"was {qn(name)} {mk} before {year - d}?", "no.", "yn"))
                pool.append(P1(f"was {qn(name)} {mk} after {year - d}?", "yes.", "yn"))
            pool.append(P1(f"was {qn(name)} {mk} before {year + d}?", "yes.", "yn"))
            pool.append(P1(f"was {qn(name)} {mk} after {year + d}?", "no.", "yn"))
    return pool


def fam_same():
    pool = []
    years = {}
    for n, y in PERSONS:
        assert y not in years, "dup year"
        years[y] = n
    hs = {}
    for n, h in HEIGHTS:
        assert h not in hs, "dup height"
        hs[h] = n
    for a, b in ordered_pairs([n for n, _ in PERSONS]):
        pool.append(P1(f"were {qn(a)} and {qn(b)} born in the same year?", "no.", "yn"))
        pool.append(P1(f"were {qn(a)} and {qn(b)} born in different years?", "yes.", "yn"))
    for a, b in ordered_pairs([n for n, _ in HEIGHTS]):
        pool.append(P1(f"are {qn(a)} and {qn(b)} the same height?", "no.", "yn"))
        pool.append(P1(f"are {qn(a)} and {qn(b)} different heights?", "yes.", "yn"))
    return pool


def fam_neg():
    pool = []
    for (a, ha), (b, hb) in ordered_pairs(HEIGHTS):
        pool.append(P1(f"is {qn(a)} not taller than {qn(b)}?",
                      "no." if ha > hb else "yes.", "yn"))
        pool.append(P1(f"is {qn(a)} not shorter than {qn(b)}?",
                      "no." if ha < hb else "yes.", "yn"))
    for (a, mka, ya), (b, mkb, yb) in ordered_pairs(TIME):
        pool.append(P1(f"was {qn(a)} not {mka} before {qn(b)}?",
                      "no." if ya < yb else "yes.", "yn"))
        pool.append(P1(f"was {qn(a)} not {mka} after {qn(b)}?",
                      "no." if ya > yb else "yes.", "yn"))
    return pool


def fam_hop():
    pool = []
    for w, au, ay in WORKS_AUTH:
        for p, py in PERSONS:
            pool.append(P1(f"was the author of {w} born before {qn(p)}?",
                          "yes." if ay < py else "no.", "yn"))
            pool.append(P1(f"was the author of {w} born after {qn(p)}?",
                          "yes." if ay > py else "no.", "yn"))
    for w1, au1, ay1 in WORKS_AUTH:
        for w2, au2, ay2 in WORKS_AUTH:
            if w1 == w2:
                continue
            pool.append(P1(f"was the author of {w1} born before the author of {w2}?",
                          "yes." if ay1 < ay2 else "no.", "yn"))
            pool.append(P1(f"was the author of {w1} born after the author of {w2}?",
                          "yes." if ay1 > ay2 else "no.", "yn"))
    return pool


def fam_beforeafter():
    pool = []
    for (a, mka, ya), (b, mkb, yb) in ordered_pairs(TIME):
        assert ya != yb
        pool.append(P1(f"was {qn(a)} {mka} before or after {qn(b)}?",
                      "before." if ya < yb else "after.", "ba"))
    return pool


def fam_unknown():
    pool = []
    for x in HEIGHTLESS:
        for h, _ in HEIGHTS:
            pool.append(P1(f"is {qn(x)} taller than {qn(h)}?", "I don't know.", "idk"))
            pool.append(P1(f"is {qn(h)} taller than {qn(x)}?", "I don't know.", "idk"))
    for x in TIMELESS:
        for t, mk, _ in TIME:
            pool.append(P1(f"was {qn(x)} built before {qn(t)}?", "I don't know.", "idk"))
            pool.append(P1(f"was {qn(t)} built before {qn(x)}?", "I don't know.", "idk"))
    return pool


def fam_ana():
    pool = []
    both = [("eiffel tower", 330, 1889, "built"),
            ("montparnasse tower", 210, 1973, "built"),
            ("statue of liberty", 93, 1886, "dedicated")]
    t2s = ["which of those two came first?", "which of these two came first?",
           "which of the two came first?"]
    for (a, ha, ya, mka), (b, hb, yb, mkb) in ordered_pairs(both):
        w = a if ha > hb else b
        t1e = f"{rn(w)} is taller."
        yw, ymk = (a, mka) if ya < yb else (b, mkb)
        t2e = f"{rn(yw)} was {ymk} first."
        for t2 in t2s:
            pool.append([
                {"q": f"which is taller, {qn(a)} or {qn(b)}?", "e": t1e,
                 "dec": "winner", "winner": w, "dir": "max", "dim": "H"},
                {"q": t2, "e": t2e,
                 "dec": "winner", "winner": yw, "dir": "min", "dim": "T"},
            ])
    return pool


FAMS = [
    ("HEIGHT", fam_height), ("TIME", fam_time), ("SUP3", fam_sup3),
    ("MORELESS", fam_moreless), ("THRESH", fam_thresh), ("SAME", fam_same),
    ("NEG", fam_neg), ("HOP", fam_hop), ("BEFOREAFTER", fam_beforeafter),
    ("UNKNOWN", fam_unknown), ("ANA", fam_ana),
]

COUNTS = {"1x": 8, "10x": 80, "100x": 800}


def build_scale(tag):
    n = COUNTS[tag]
    probes = []  # (fam, turns)
    for fam, fn in FAMS:
        pool = fn()
        assert len(pool) > 0, fam
        for i in range(n):
            probes.append((fam, pool[i % len(pool)]))
    return probes


def write_battery(path, probes, start_idx=0):
    oracle = []
    with open(path, "w") as f:
        for k, (fam, turns) in enumerate(probes):
            did = f"CMP-{fam}-{start_idx + k + 1:04d}"
            f.write(f"DIALOGUE {did} COMPOSE\n")
            for t, turn in enumerate(turns, 1):
                f.write(f"U {turn['q']}\n")
                f.write(f"E {turn['e']}\n")
                oracle.append({"id": did, "turn": t, "family": fam,
                               "expected": turn["e"], "dec": turn["dec"],
                               "winner": turn["winner"], "dir": turn["dir"],
                               "dim": turn["dim"]})
            f.write("END\n")
    return oracle


def main():
    all_oracle = []
    p1x = build_scale("1x")
    all_oracle += write_battery(os.path.join(OUT, "battery_1x.txt"), p1x)
    p10x = build_scale("10x")
    all_oracle += write_battery(os.path.join(OUT, "battery_10x.txt"), p10x)
    p100x = build_scale("100x")
    assert len(p100x) == 8800
    # 100x runs as 4 chunks of 2200 (dacc harness limit); global IDs stay
    # unique across chunks via the start_idx offset.
    gidx = 0
    for c in range(4):
        chunk = p100x[c * 2200:(c + 1) * 2200]
        all_oracle += write_battery(
            os.path.join(OUT, f"battery_100x_p{c + 1}.txt"), chunk,
            start_idx=gidx)
        gidx += 2200
    with open(os.path.join(OUT, "oracle.jsonl"), "w") as f:
        for o in all_oracle:
            f.write(json.dumps(o) + "\n")
    nq = sum(len(t) for _, t in p1x) + sum(len(t) for _, t in p10x) + \
        sum(len(t) for _, t in p100x)
    print(f"1x={len(p1x)} 10x={len(p10x)} 100x={len(p100x)} "
          f"total_questions={nq} oracle_lines={len(all_oracle)}")


if __name__ == "__main__":
    main()
