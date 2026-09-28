#!/usr/bin/env python3
"""Held-out battery for cmp_scale: NOVEL phrasing templates generated AFTER
the prototype freeze (commit b0441c69). Same entity/attribute tables and
oracle semantics as gen_probes.py; every template below is a surface frame
that does not occur in the frozen battery.

Covers the engine's implemented operator vocabulary in new arrangements:
between/of-frames, "which stands taller", "did X come before N",
"taller than N meters", "is it true that ... not ...", hop via
"come earlier", "choose: did ... before or after", etc.

Deterministic: combinatorial cycling only, no RNG.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_probes import (HEIGHTS, TIME, WORKS_AUTH, PERSONS, HEIGHTLESS,
                        TIMELESS, qn, rn, ordered_pairs, ordered_triples, P1)

OUT = os.path.dirname(os.path.abspath(__file__))
N_PER_FAMILY = 48  # dialogues per family (ANA: 48 two-turn dialogues)


def cycle(pool, n):
    return [pool[i % len(pool)] for i in range(n)]


def h_height():
    pool = []
    for (a, ha), (b, hb) in ordered_pairs(HEIGHTS):
        w = a if ha > hb else b
        pool.append(P1(f"between {qn(a)} and {qn(b)}, which is taller?",
                      f"{rn(w)} is taller.", "winner", w, "max", "H"))
        w = a if ha < hb else b
        pool.append(P1(f"between {qn(a)} and {qn(b)}, which is shorter?",
                      f"{rn(w)} is shorter.", "winner", w, "min", "H"))
        w = a if ha > hb else b
        pool.append(P1(f"which stands taller, {qn(a)} or {qn(b)}?",
                      f"{rn(w)} is taller.", "winner", w, "max", "H"))
        w = a if ha < hb else b
        pool.append(P1(f"tell me which is shorter, {qn(a)} or {qn(b)}.",
                      f"{rn(w)} is shorter.", "winner", w, "min", "H"))
    return pool


def h_time():
    pool = []
    for (a, mka, ya), (b, mkb, yb) in ordered_pairs(TIME):
        w, wmk = (a, mka) if ya < yb else (b, mkb)
        pool.append(P1(f"between {qn(a)} and {qn(b)}, which came first?",
                      f"{rn(w)} was {wmk} first.", "winner", w, "min", "T"))
        w, wmk = (a, mka) if ya > yb else (b, mkb)
        pool.append(P1(f"between {qn(a)} and {qn(b)}, which came last?",
                      f"{rn(w)} was {wmk} last.", "winner", w, "max", "T"))
        w, wmk = (a, mka) if ya < yb else (b, mkb)
        pool.append(P1(f"which was earlier, {qn(a)} or {qn(b)}?",
                      f"{rn(w)} was {wmk} first.", "winner", w, "min", "T"))
        w, wmk = (a, mka) if ya > yb else (b, mkb)
        pool.append(P1(f"which was later, {qn(a)} or {qn(b)}?",
                      f"{rn(w)} was {wmk} last.", "winner", w, "max", "T"))
    return pool


def h_sup3():
    pool = []
    for (a, ha), (b, hb), (c, hc) in ordered_triples(HEIGHTS):
        vals = [(a, ha), (b, hb), (c, hc)]
        wmax = max(vals, key=lambda t: t[1])[0]
        wmin = min(vals, key=lambda t: t[1])[0]
        pool.append(P1(f"of {qn(a)}, {qn(b)} and {qn(c)}, which is tallest?",
                      f"{rn(wmax)} is tallest.", "winner", wmax, "max", "H"))
        pool.append(P1(f"of {qn(a)}, {qn(b)} and {qn(c)}, which is shortest?",
                      f"{rn(wmin)} is shortest.", "winner", wmin, "min", "H"))
    for (a, ya), (b, yb), (c, yc) in ordered_triples(PERSONS):
        vals = [(a, ya), (b, yb), (c, yc)]
        wmin = min(vals, key=lambda t: t[1])[0]
        wmax = max(vals, key=lambda t: t[1])[0]
        pool.append(P1(f"who came first of {qn(a)}, {qn(b)} and {qn(c)}?",
                      f"{rn(wmin)} was born first.", "winner", wmin, "min", "T"))
        pool.append(P1(f"who came last of {qn(a)}, {qn(b)} and {qn(c)}?",
                      f"{rn(wmax)} was born last.", "winner", wmax, "max", "T"))
    return pool


def h_moreless():
    pool = []
    for (a, ha), (b, hb) in ordered_pairs(HEIGHTS):
        w = a if ha > hb else b
        pool.append(P1(f"between {qn(a)} and {qn(b)}, which is higher?",
                      f"{rn(w)} is higher.", "winner", w, "max", "H"))
        w = a if ha < hb else b
        pool.append(P1(f"between {qn(a)} and {qn(b)}, which is lower?",
                      f"{rn(w)} is lower.", "winner", w, "min", "H"))
        w = a if ha > hb else b
        pool.append(P1(f"which stands higher, {qn(a)} or {qn(b)}?",
                      f"{rn(w)} is higher.", "winner", w, "max", "H"))
    return pool


def h_thresh():
    pool = []
    for name, h in HEIGHTS:
        for d in (2, 25, 250):
            pool.append(P1(f"is {qn(name)} taller than {h + d} meters?",
                          "no.", "yn"))
            pool.append(P1(f"is {qn(name)} taller than {h - d} meters?",
                          "yes.", "yn"))
            pool.append(P1(f"is {qn(name)} shorter than {h + d} meters?",
                          "yes.", "yn"))
            pool.append(P1(f"is {qn(name)} shorter than {h - d} meters?",
                          "no.", "yn"))
    for name, mk, year in TIME:
        for d in (7, 70):
            if year - d > 0:
                pool.append(P1(f"did {qn(name)} come before {year - d}?",
                              "no.", "yn"))
                pool.append(P1(f"did {qn(name)} come after {year - d}?",
                              "yes.", "yn"))
            pool.append(P1(f"did {qn(name)} come before {year + d}?",
                          "yes.", "yn"))
            pool.append(P1(f"did {qn(name)} come after {year + d}?",
                          "no.", "yn"))
    return pool


def h_same():
    pool = []
    for (a, ha), (b, hb) in ordered_pairs(HEIGHTS):
        pool.append(P1(f"is the height of {qn(a)} the same as the height of {qn(b)}?",
                      "no.", "yn"))
        pool.append(P1(f"does {qn(a)} have the same height as {qn(b)}?",
                      "no.", "yn"))
        pool.append(P1(f"is {qn(a)} a different height than {qn(b)}?",
                      "yes.", "yn"))
    for (a, ya), (b, yb) in ordered_pairs(PERSONS):
        pool.append(P1(f"was {qn(a)} born in the same year as {qn(b)}?",
                      "no.", "yn"))
    return pool


def h_neg():
    pool = []
    for (a, ha), (b, hb) in ordered_pairs(HEIGHTS):
        pool.append(P1(f"is it true that {qn(a)} is not taller than {qn(b)}?",
                      "no." if ha > hb else "yes.", "yn"))
        pool.append(P1(f"is {qn(a)} not higher than {qn(b)}?",
                      "no." if ha > hb else "yes.", "yn"))
    for (a, mka, ya), (b, mkb, yb) in ordered_pairs(TIME):
        pool.append(P1(f"was {qn(a)} really not {mka} before {qn(b)}?",
                      "no." if ya < yb else "yes.", "yn"))
    return pool


def h_hop():
    pool = []
    for w1, au1, ay1 in WORKS_AUTH:
        for w2, au2, ay2 in WORKS_AUTH:
            if w1 == w2:
                continue
            pool.append(P1(f"did the author of {w1} come earlier than the author of {w2}?",
                          "yes." if ay1 < ay2 else "no.", "yn"))
            pool.append(P1(f"was the author of {w1} born later than the author of {w2}?",
                          "yes." if ay1 > ay2 else "no.", "yn"))
            w = au1 if ay1 < ay2 else au2
            pool.append(P1(f"which author came first, the author of {w1} or the author of {w2}?",
                          f"{rn(w)} was born first.", "winner", w, "min", "T"))
            pool.append(P1(f"which author was born first, the author of {w1} or the author of {w2}?",
                          f"{rn(w)} was born first.", "winner", w, "min", "T"))
    return pool


def h_beforeafter():
    pool = []
    for (a, mka, ya), (b, mkb, yb) in ordered_pairs(TIME):
        assert ya != yb
        pool.append(P1(f"choose: did {qn(a)} come before or after {qn(b)}?",
                      "before." if ya < yb else "after.", "ba"))
        pool.append(P1(f"before or after -- when did {qn(a)} come relative to {qn(b)}?",
                      "before." if ya < yb else "after.", "ba"))
    return pool


def h_unknown():
    pool = []
    for x in HEIGHTLESS:
        for h, _ in HEIGHTS:
            pool.append(P1(f"could {qn(x)} be taller than {qn(h)}?",
                          "I don't know.", "idk"))
            pool.append(P1(f"is {qn(h)} not taller than {qn(x)}?",
                          "I don't know.", "idk"))
    for x in TIMELESS:
        for t, mk, _ in TIME:
            pool.append(P1(f"did {qn(x)} come before {qn(t)}?",
                          "I don't know.", "idk"))
            pool.append(P1(f"was {qn(t)} {mk} after {qn(x)}?",
                          "I don't know.", "idk"))
    return pool


def h_ana():
    pool = []
    both = [("eiffel tower", 330, 1889, "built"),
            ("montparnasse tower", 210, 1973, "built"),
            ("statue of liberty", 93, 1886, "dedicated")]
    t2s = [("which came first of those two?", "min"),
           ("which of these two came last?", "max"),
           ("of these two, which came last?", "max"),
           ("which of those two came last?", "max")]
    t1s = [("between {a} and {b}, which is higher?", "max", "higher"),
           ("of {a} and {b}, which is lower?", "min", "lower")]
    for (a, ha, ya, mka), (b, hb, yb, mkb) in ordered_pairs(both):
        for t1q, t1dir, t1w in t1s:
            for t2q, t2dir in t2s:
                if t2dir == "min":
                    yw, ymk = (a, mka) if ya < yb else (b, mkb)
                    t2e = f"{rn(yw)} was {ymk} first."
                else:
                    yw, ymk = (a, mka) if ya > yb else (b, mkb)
                    t2e = f"{rn(yw)} was {ymk} last."
                w = (a if ha > hb else b) if t1dir == "max" else (a if ha < hb else b)
                pool.append([
                    {"q": t1q.format(a=qn(a), b=qn(b)),
                     "e": f"{rn(w)} is {t1w}.",
                     "dec": "winner", "winner": w, "dir": t1dir, "dim": "H"},
                    {"q": t2q, "e": t2e,
                     "dec": "winner", "winner": yw, "dir": t2dir, "dim": "T"},
                ])
    return pool


FAMILIES = [
    ("HEIGHT", h_height), ("TIME", h_time), ("SUP3", h_sup3),
    ("MORELESS", h_moreless), ("THRESH", h_thresh), ("SAME", h_same),
    ("NEG", h_neg), ("HOP", h_hop), ("BEFOREAFTER", h_beforeafter),
    ("UNKNOWN", h_unknown), ("ANA", h_ana),
]


def main():
    dialogues = []
    for fam, fn in FAMILIES:
        pool = fn()
        assert len(pool) >= N_PER_FAMILY, (fam, len(pool))
        for i, turns in enumerate(cycle(pool, N_PER_FAMILY)):
            dialogues.append((f"HELD-{fam}-{i:04d}", fam, turns))
    with open(os.path.join(OUT, "battery_heldout.txt"), "w") as f:
        for did, fam, turns in dialogues:
            f.write(f"DIALOGUE {did} COMPOSE\n")
            for ti, t in enumerate(turns, 1):
                f.write(f"U {t['q']}\nE {t['e']}\n")
            f.write("END\n")
    with open(os.path.join(OUT, "oracle_heldout.jsonl"), "w") as f:
        for did, fam, turns in dialogues:
            for ti, t in enumerate(turns, 1):
                f.write(json.dumps({
                    "id": did, "turn": ti, "family": fam,
                    "expected": t["e"], "dec": t["dec"],
                    "winner": t.get("winner"), "dir": t.get("dir"),
                    "dim": t.get("dim"),
                }) + "\n")
    nq = sum(len(t) for _, _, t in dialogues)
    print(f"dialogues={len(dialogues)} questions={nq}")


if __name__ == "__main__":
    main()
