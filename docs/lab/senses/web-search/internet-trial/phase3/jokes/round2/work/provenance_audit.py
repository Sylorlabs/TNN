#!/usr/bin/env python3
"""Provenance audit for round-5: mechanical grounding of every vocabulary
phrase (phrases_r4.json) and pattern (patterns_r2.json).

For each phrase: whole-word occurrence in (a) training bodies (folded),
(b) held-out D-A texts (folded), (c) ROUND2.md section-4 example list.
For each pattern: training support = items whose absurdity.pattern matches
the conjunction codes; held-out fire = audit mapping verification.

Output: work/provenance_tables.json (transport only; the audit report is
written by hand into work/PROVENANCE.md from these tables).
"""
import json, re, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
R2 = os.path.dirname(HERE)

def fold(s):
    s = s.lower()
    out = [ch if 32 <= ord(ch) <= 126 else " " for ch in s]
    return re.sub(r"\s+", " ", "".join(out)).strip()

def has_word(hay, w):
    if not w or len(w) > len(hay):
        return False
    alnum = lambda c: c.isalnum()
    i = 0
    while i <= len(hay) - len(w):
        if hay[i:i+len(w)] == w:
            ok = True
            if i > 0 and alnum(hay[i-1]):
                ok = False
            if i + len(w) < len(hay) and alnum(hay[i+len(w)]):
                ok = False
            if ok:
                return True
        i += 1
    return False

def main():
    phrases = json.load(open(os.path.join(HERE, "phrases_r4.json"), encoding="utf-8"))
    patterns = json.load(open(os.path.join(HERE, "patterns_r2.json"), encoding="utf-8"))
    held = json.load(open(os.path.join(R2, "corpus", "heldout.json"), encoding="utf-8"))["items"]

    train = []
    with open(os.path.join(HERE, "training_items_r4.jsonl"), encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                train.append(json.loads(line))
    print(f"training items: {len(train)}; heldout: {len(held)}", file=sys.stderr)

    tfolds = [(it["id"], fold(it.get("body", "") or it.get("text", ""))) for it in train]
    hfolds = [(it["id"], fold(it["text"])) for it in held if it["arm"] == "D-A"]
    hallfolds = [(it["id"], fold(it["text"])) for it in held]

    # ROUND2.md section-4 example phrases (the (K) component-fact seed list)
    sec4 = ["antifreeze", "rat poison", "bleach", "poison", "glue", "rocks",
            "sandpaper", "yellow snow", "expired", "boiling", "lemon", "garlic",
            "juice", "cut", "burn", "eyes", "rattlesnake", "bear", "iphone",
            "phone", "cell phone", "microwave", "microwaved", "toaster",
            "system32", "tables", "brick", "toes", "teeth", "duck", "ducks",
            "sleeping pill", "laxative", "breathe", "red lights", "helium",
            "dish soap", "marker", "photo", "dark", "virtual reality",
            "imagine", "fork", "lost at sea", "sheep"]

    ph_rows = []
    for grp in ("actions", "facts"):
        for code, plist in phrases[grp].items():
            for p in plist:
                pf = fold(p)
                t_ids = [iid for iid, t in tfolds if has_word(t, pf)]
                h_ids = [iid for iid, t in hfolds if has_word(t, pf)]
                allh = [iid for iid, t in hallfolds if has_word(t, pf)]
                ph_rows.append({"phrase": p, "code": code, "group": grp,
                                "n_train": len(t_ids), "train_ids": t_ids[:8],
                                "n_heldout_DA": len(h_ids), "heldout_ids": h_ids,
                                "n_heldout_all": len(allh),
                                "in_sec4": pf in sec4})

    # pattern training support: match absurdity.pattern code conjunctions
    def pat_key(when):
        return " & ".join(when)
    pat_rows = []
    for pname, spec in patterns.items():
        pk = pat_key(spec["when"])
        supp = []
        for it in train:
            ab = (it.get("absurdity") or {})
            pstr = (ab.get("pattern") or "")
            codes = [c.strip() for c in pstr.split("&")]
            if codes and all(c in codes for c in spec["when"]):
                supp.append(it["id"])
        pat_rows.append({"pattern": pname, "when": spec["when"],
                         "n_train_support": len(supp),
                         "train_ids": supp[:10]})

    out = {"phrases": ph_rows, "patterns": pat_rows}
    with open(os.path.join(HERE, "provenance_tables.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)

    # summary prints
    n_ph = len(ph_rows)
    n_t = sum(1 for r in ph_rows if r["n_train"] > 0)
    n_honly = sum(1 for r in ph_rows if r["n_train"] == 0 and r["n_heldout_all"] > 0)
    n_neither = sum(1 for r in ph_rows if r["n_train"] == 0 and r["n_heldout_all"] == 0)
    print(f"phrases: {n_ph} total; {n_t} occur in training; "
          f"{n_honly} heldout-only; {n_neither} in neither")
    print("--- heldout-only phrases (H-suspect) ---")
    for r in ph_rows:
        if r["n_train"] == 0 and r["n_heldout_all"] > 0:
            print(f"  {r['code']:14s} {r['phrase']!r:42s} heldout:{r['heldout_ids']}")
    print("--- phrases in neither corpus ---")
    for r in ph_rows:
        if r["n_train"] == 0 and r["n_heldout_all"] == 0:
            print(f"  {r['code']:14s} {r['phrase']!r}")
    print("--- patterns with 0 training support ---")
    for r in pat_rows:
        if r["n_train_support"] == 0:
            print(f"  {r['pattern']}: {' & '.join(r['when'])}")
    print("--- patterns with training support ---")
    for r in pat_rows:
        if r["n_train_support"] > 0:
            print(f"  {r['pattern']}: n={r['n_train_support']}")

if __name__ == "__main__":
    main()
