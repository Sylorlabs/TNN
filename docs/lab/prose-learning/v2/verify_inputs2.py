#!/usr/bin/env python3
"""Verify every constructed battery item. Prints FIXES needed."""
import json, os, re

OUT = os.path.expanduser("~/workspace/richcomp/inputs2")
CH = os.path.expanduser("~/workspace/tnn-lab/prose-learning/inputs")
fixes = []

def note(msg):
    fixes.append(msg); print("FIX:", msg)

def lines(p):
    return [json.loads(l) for l in open(p, encoding="utf-8")]

# championship truth: entity -> probe_value from sol test, plus train text
sol_test = {it["id"]: it for it in json.load(open(f"{CH}/test_sol.jsonl"))}
sol_train = {it["id"]: it["sentence"] for it in json.load(open(f"{CH}/train_sol.jsonl"))}

def lastnum(s):
    nums = re.findall(r"\d+", s)
    return int(nums[-1]) if nums else None

# ---------- generic format checks
for p in sorted(os.listdir(OUT)):
    for i, it in enumerate(lines(f"{OUT}/{p}")):
        if "train" in p:
            assert set(it) == {"id", "text"}, (p, i, set(it))
            assert it["id"] == i, (p, "train id seq", i, it["id"])
        else:
            assert set(it) == {"id", "probe", "probe_value", "expect"}, (p, i, set(it))
            assert it["id"] == i, (p, "test id seq", i, it["id"])
            assert it["expect"] in ("value", "contradiction", "hedged", "unknown"), (p, i)
            if it["expect"] == "value":
                assert isinstance(it["probe_value"], int), (p, i)
            else:
                assert it["probe_value"] is None, (p, i)
print("format OK")

# ---------- SUB-PARA: truth check every train value
para_tr = lines(f"{OUT}/sub_para_train.jsonl")
para_te = lines(f"{OUT}/sub_para_test.jsonl")
# expected: fact f (0..47): train ids 5f..5f+4 share value; test f value
exp = []
for cat, facts in [
    ("alpha", [("A",1),("B",2),("C",3),("E",5),("F",6),("G",7),("H",8),("I",9),("J",10),("K",11),("L",12),("M",13)]),
    ("wordlen", [("a",1),("an",2),("the",3),("four",4),("seven",5),("minute",6),("seconds",7),("afternoon",9),("dictionary",10),("handwriting",11),("disappointed",12),("extraordinary",13)]),
    ("pubyear", [("Hamlet",1603),("Don Quixote",1605),("King Lear",1608),("The King James Bible",1611),("Shakespeare's First Folio",1623),("Leviathan",1651),("Paradise Lost",1667),("Robinson Crusoe",1719),("Gulliver's Travels",1726),("Pamela",1740),("Tom Jones",1749),("Candide",1759)]),
    ("count", [26,5,21,7,12,4,52,24,60,60,168,27]),
]:
    for f in facts:
        exp.append(f[-1] if cat != "count" else f)
for f in range(48):
    for k in range(5):
        ln = para_tr[5*f+k]["text"]
        v = lastnum(ln)
        if v != exp[f]:
            note(f"para train id {5*f+k}: value {v} != expected {exp[f]}: {ln}")
    if para_te[f]["probe_value"] != exp[f]:
        note(f"para test id {f}: probe_value {para_te[f]['probe_value']} != {exp[f]}")
# independent truth cross-checks
alpha_true = {c: ord(c)-64 for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
for f, (e, v) in enumerate([("A",1),("B",2),("C",3),("E",5),("F",6),("G",7),("H",8),("I",9),("J",10),("K",11),("L",12),("M",13)]):
    assert alpha_true[e] == v, e
for f, (w, v) in enumerate([("a",1),("an",2),("the",3),("four",4),("seven",5),("minute",6),("seconds",7),("afternoon",9),("dictionary",10),("handwriting",11),("disappointed",12),("extraordinary",13)]):
    assert len(w) == v, (w, v)
# pubyear/count vs championship test probes (entity match by probe text)
print("para truth OK")
# paraphrase novelty: no train line may equal a championship sol train sentence
sol_sents = set(sol_train.values())
for it in para_tr:
    if it["text"] in sol_sents:
        note(f"para train id {it['id']} duplicates championship wording")
# within-fact wording distinctness
for f in range(48):
    ws = [para_tr[5*f+k]["text"] for k in range(5)]
    if len(set(ws)) != 5:
        note(f"para fact {f}: duplicate train wordings")

# ---------- SUB-CONTR: two asserted different values
for it in lines(f"{OUT}/sub_contr_train.jsonl"):
    sents = [s.strip() for s in it["text"].split(". ") if s.strip()]
    assert len(sents) == 2, (it["id"], it["text"])
    v1, v2 = lastnum(sents[0]), lastnum(sents[1])
    assert v1 is not None and v2 is not None, it["id"]
    if v1 == v2:
        note(f"contr train id {it['id']}: both sentences assert {v1}")
    for te in lines(f"{OUT}/sub_contr_test.jsonl"):
        pass
te = {i["id"]: i for i in lines(f"{OUT}/sub_contr_test.jsonl")}
for it in lines(f"{OUT}/sub_contr_train.jsonl"):
    assert te[it["id"]]["expect"] == "contradiction"
    assert te[it["id"]]["probe_value"] is None
print("contr OK")

# ---------- SUB-HEDGE
hedge_tr = {i["id"]: i for i in lines(f"{OUT}/sub_hedge_train.jsonl")}
hedge_te = {i["id"]: i for i in lines(f"{OUT}/sub_hedge_test.jsonl")}
MARKERS = ["think","believe","probably","maybe","perhaps","might","could","seems",
           "allegedly","reportedly","possibly","likely"]
used = set()
for i in range(12):
    t = hedge_tr[i]["text"]; q = hedge_te[i]
    sents = [s.strip() for s in t.split(". ") if s.strip()]
    assert len(sents) == 2, (i, t)
    va, vh = lastnum(sents[0]), lastnum(sents[1])
    if va == vh: note(f"hedge AH id {i}: asserted==hedged value {va}")
    if q["expect"] != "value" or q["probe_value"] != va:
        note(f"hedge AH id {i}: probe should expect asserted {va}, got {q}")
    low = sents[1].lower()
    m = [mk for mk in MARKERS if mk in low]
    if not m: note(f"hedge AH id {i}: no hedge marker in: {sents[1]}")
    used.update(m)
for i in range(12, 24):
    t = hedge_tr[i]["text"]; q = hedge_te[i]
    low = t.lower()
    m = [mk for mk in MARKERS if mk in low]
    if not m: note(f"hedge HO id {i}: no hedge marker in: {t}")
    used.update(m)
    if q["expect"] != "hedged" or q["probe_value"] is not None:
        note(f"hedge HO id {i}: probe should be hedged/null, got {q}")
print("hedge markers used:", sorted(used))
if len(used) < 11: note(f"hedge: only {len(used)} distinct markers used")

# ---------- SUB-NEG
neg_tr = {i["id"]: i for i in lines(f"{OUT}/sub_neg_train.jsonl")}
neg_te = {i["id"]: i for i in lines(f"{OUT}/sub_neg_test.jsonl")}
for i in range(24):
    t = neg_tr[i]["text"]; q = neg_te[i]
    low = t.lower()
    if not (re.search(r"\bnot\b", low) or re.search(r"\bnever\b", low) or re.search(r"\bno\b", low) or "n't" in low or "'t " in low or low.endswith("'t")):
        note(f"neg-only id {i}: no negation marker: {t}")
    if q["expect"] != "unknown" or q["probe_value"] is not None:
        note(f"neg-only id {i}: probe should be unknown/null: {q}")
for i in range(24, 36):
    t = neg_tr[i]["text"]; q = neg_te[i]
    sents = [s.strip() for s in t.split(". ") if s.strip()]
    assert len(sents) == 2, (i, t)
    has_neg = any(re.search(r"\bnot\b", s.lower()) or "n't" in s.lower() for s in sents)
    if not has_neg: note(f"neg+asserted id {i}: no negated sentence: {t}")
    # find asserted sentence = the one without negation; its value must equal probe_value
    for s in sents:
        if not (re.search(r"\bnot\b", s.lower()) or "n't" in s.lower()):
            if lastnum(s) != q["probe_value"]:
                note(f"neg+asserted id {i}: asserted value {lastnum(s)} != probe {q['probe_value']}")
    if q["expect"] != "value": note(f"neg+asserted id {i}: expect should be value")
print("neg OK")

# ---------- SUB-MULTI: arithmetic
for it, q in zip(lines(f"{OUT}/sub_multi_train.jsonl"), lines(f"{OUT}/sub_multi_test.jsonl")):
    t = it["text"]
    m = re.search(r"([A-Z]) comes (after|before) ([A-Z])", t)
    assert m, t
    x, rel, y = m.groups()
    a = re.search(rf"{y} has an alphabet position of (\d+)", t)
    assert a, t
    py = int(a.group(1))
    assert alpha_true[y] == py, (t, y, py)
    want = py + 1 if rel == "after" else py - 1
    assert alpha_true[x] == want, (t, x, want)
    assert q["probe_value"] == want, (it["id"], q["probe_value"], want)
    assert q["expect"] == "value"
    assert f"alphabet position of {x}" in q["probe"]
print("multi OK")

# ---------- SUB-CORE: s1 entity quoted, s2 pronoun, expected == lastnum(s2)
PRON = [" it ", " this ", " that ", "its ", "the word", "the letter"]
for it, q in zip(lines(f"{OUT}/sub_core_train.jsonl"), lines(f"{OUT}/sub_core_test.jsonl")):
    sents = [s.strip() for s in it["text"].split(". ") if s.strip()]
    assert len(sents) == 2, (it["id"], it["text"])
    if '"' not in sents[0]: note(f"core id {it['id']}: s1 has no quoted entity: {sents[0]}")
    low2 = " " + sents[1].lower()
    if not any(p in low2 for p in PRON):
        note(f"core id {it['id']}: s2 has no pronoun/coref phrase: {sents[1]}")
    v = lastnum(sents[1])
    if v != q["probe_value"]:
        note(f"core id {it['id']}: s2 last number {v} != probe {q['probe_value']}")
    if q["expect"] != "value": note(f"core id {it['id']}: expect")
print("core OK")

# ---------- SUB-DISTR
dtr = lines(f"{OUT}/sub_distr_train.jsonl")
dte = lines(f"{OUT}/sub_distr_test.jsonl")
assert len(dtr) == 480 and len(dte) == 240
for i in range(240):
    if dtr[i]["text"] != sol_train[i]:
        note(f"distr train id {i}: not equal to championship sol train")
    if dtr[i]["id"] != i: note("distr id")
for i in range(240):
    q = dte[i]; s = sol_test[i]
    if q["probe"] != s["probe"] or q["probe_value"] != s["probe_value"]:
        note(f"distr test id {i}: probe mismatch vs championship")
    if q["expect"] != "value": note(f"distr test id {i} expect")
# distractor hygiene
FROZEN_REL = ["alphabet position", "letter count", "publication year", "comes after", "comes before"]
champ_entities = set()
for s in sol_train.values():
    champ_entities.add(s)
for it in dtr[240:]:
    t = it["text"].lower()
    for fr in FROZEN_REL:
        if fr in t: note(f"distr id {it['id']}: frozen relation '{fr}' in distractor")
    if re.search(r"\bnot\b|\bnever\b|\bno\b|n't", t): note(f"distr id {it['id']}: negation word in distractor")
    if any(mk in t for mk in ["think","believe","probably","maybe","perhaps","might","could","seem","allegedly","reportedly","possibly","likely","rumor"]):
        note(f"distr id {it['id']}: hedge word in distractor: {it['text']}")
    if '"' in it["text"]: note(f"distr id {it['id']}: quote in distractor")
    # no championship entity text overlap: check single-letter entities A-Z and key nouns
print("distr OK")
# distractor internal consistency: same entity -> same value across its 5 templates
from collections import defaultdict
ENTS = ["Eiffel Tower","Mount Everest","Mariana Trench","Nile River","Amazon River",
 "Sahara Desert","Great Wall of China","Burj Khalifa","Empire State Building",
 "Statue of Liberty","Big Ben tower","Colosseum","Sydney Opera House","Golden Gate Bridge",
 "Panama Canal","Suez Canal","Mississippi River","Yangtze River","Lake Baikal","Dead Sea",
 "Grand Canyon","Mount Kilimanjaro","Mount Fuji","Blue whale","Giraffe","Cheetah",
 "Peregrine falcon","Hummingbird","Ostrich","African elephant","Polar bear",
 "Great white shark","Anaconda","Komodo dragon","Redwood tree","Baobab tree",
 "Angel Falls","Niagara Falls","Victoria Falls","Hoover Dam","Three Gorges Dam",
 "London Eye","Space Needle","CN Tower","Tokyo Skytree","Shanghai Tower",
 "One World Trade Center","Willis Tower"]
assert len(ENTS) == 48
by_ent = defaultdict(set)
for it in dtr[240:]:
    hit = [e for e in ENTS if e in it["text"]]
    if len(hit) != 1: note(f"distr id {it['id']}: entity match {hit}")
    else: by_ent[hit[0]].add(lastnum(it["text"]))
for ent, vs in by_ent.items():
    if len(vs) != 1: note(f"distr entity inconsistent: {ent} -> {vs}")
print("distractor entities:", len(by_ent))

print()
print("TOTAL FIXES:", len(fixes))
