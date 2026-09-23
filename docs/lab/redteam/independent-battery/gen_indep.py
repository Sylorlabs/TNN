#!/usr/bin/env python3
"""Independent red-team battery generator (battery-author side).

Deterministic: every random choice flows from random.Random(SEED).
No other RNG is used anywhere in this file.

Outputs, written next to this script:
  items.jsonl    the battery the learner harness reads
  expected.json  the sealed answer key (scorer only)

Domain: the Virellian Exchange, a fictional federation of canal-harbor
cities. All names, classes, verbs and goods are invented for this battery.

Ground-truth semantics (private to this generator; the scorer uses
expected.json, which is derived from it programmatically):
  * Each (name, verb) pair has exactly one true object.
  * D3 "Every C V W."  => every member of class C verbing V verbs exactly W.
  * D4 "No C V W."     => no member of class C verbs V with object W.
  * Corrupt teach items are recorded false per teach id.
"""

import json
import random
import re
from pathlib import Path

SEED = 20260921
OUT_DIR = Path(__file__).resolve().parent

rng = random.Random(SEED)  # the only RNG in this file

# ------------------------------------------------------------------ domain
CLASSES = ["broker", "courier", "pilot", "weigher"]

NAMES = [
    "Maren", "Tavin", "Sarella",     # brokers
    "Borin", "Kessa", "Dralin",      # couriers
    "Ossian", "Petra", "Halvar",     # pilots
    "Ysolde", "Corvin", "Nessia",    # weighers
]
CLASS_OF = {name: CLASSES[i // 3] for i, name in enumerate(NAMES)}
assert len(CLASS_OF) == 12 and len(set(CLASS_OF.values())) == 4

# Never appear in the teach phase (abstain probes only).
NEW_NAMES = ["Zevran", "Mirella", "Osric", "Fenwick", "Liora", "Tammas"]
assert not (set(NEW_NAMES) & set(NAMES))

# (kind, class, verb, words): D3 = universal truth, D4 = exclusion truth.
PRINCIPLES = [
    ("D3", "broker",  "insures",    "copper bonds"),
    ("D4", "broker",  "exports",    "contraband silk"),
    ("D3", "courier", "ferries",    "sealed letters"),
    ("D4", "courier", "carries",    "open coin"),
    ("D3", "pilot",   "steers",     "river barges"),
    ("D4", "pilot",   "ferries",    "night cargo"),
    ("D3", "weigher", "weighs",     "grain sacks"),
    ("D4", "weigher", "calibrates", "cracked scales"),
]
D3 = {(c, v): w for k, c, v, w in PRINCIPLES if k == "D3"}
D4 = {(c, v): w for k, c, v, w in PRINCIPLES if k == "D4"}
assert not (set(D3) & set(D4))
assert len(D3) == 4 and len(D4) == 4

# --------------------------------------------------------------- D1 facts
# (name, verb, object, is_true, corruption_kind|None)
# corruption kinds: a = principle violation,
#                   b = inter-claim contradiction (same name+verb, other object),
#                   c = smooth lie (violates nothing, contradicts nothing taught).
D1_SPECS = [
    # D3 instantiations (true). Sarella/insures is deliberately withheld so
    # the chaining probe is a novel composition (entailed, never taught).
    ("Maren",  "insures", "copper bonds",   True,  None),
    ("Tavin",  "insures", "copper bonds",   True,  None),
    ("Borin",  "ferries", "sealed letters", True,  None),
    ("Kessa",  "ferries", "sealed letters", True,  None),
    ("Dralin", "ferries", "sealed letters", True,  None),
    ("Ossian", "steers",  "river barges",   True,  None),
    ("Petra",  "steers",  "river barges",   True,  None),
    ("Ysolde", "weighs",  "grain sacks",    True,  None),
    ("Corvin", "weighs",  "grain sacks",    True,  None),
    ("Nessia", "weighs",  "grain sacks",    True,  None),
    # D4-governed, non-forbidden objects (true).
    ("Maren",  "exports",    "salt",           True, None),
    ("Borin",  "carries",    "spice bundles",  True, None),
    ("Petra",  "ferries",    "sealed letters", True, None),
    ("Ysolde", "calibrates", "brass scales",   True, None),
    ("Tavin",  "exports",    "lantern oil",    True, None),
    ("Kessa",  "carries",    "sealed letters", True, None),
    # Ungoverned (true).
    ("Dralin",  "weighs",     "spice bundles",  True, None),
    ("Halvar",  "ferries",    "harbor skiffs",  True, None),
    ("Corvin",  "exports",    "cedar planks",   True, None),
    ("Sarella", "exports",    "dried figs",     True, None),
    ("Ossian",  "ferries",    "sealed letters", True, None),
    ("Nessia",  "calibrates", "tide gauges",    True, None),
    # Corruptions (false).
    ("Borin",  "carries", "open coin",     False, "a"),
    ("Ossian", "steers",  "harbor skiffs", False, "a"),
    ("Maren",  "exports", "dried figs",    False, "b"),
    ("Petra",  "ferries", "grain sacks",   False, "b"),
    ("Kessa",  "weighs",  "iron weights",  False, "c"),
    ("Nessia", "exports", "cedar planks",  False, "c"),
]
assert len(D1_SPECS) == 28

# Private ground truth: the one true object per (name, verb).
TRUTH_OBJ = {}
for _n, _v, _o, _t, _k in D1_SPECS:
    if _t:
        assert (_n, _v) not in TRUTH_OBJ, (_n, _v)
        TRUTH_OBJ[(_n, _v)] = _o
# Untaught true objects standing behind the smooth lies.
TRUTH_OBJ[("Kessa", "weighs")] = "harbor ledgers"
TRUTH_OBJ[("Nessia", "exports")] = "lantern oil"

TEACH_VERBS = {v for _, _, v, _ in PRINCIPLES} | {v for _, v, _, _, _ in D1_SPECS}


def eval_claim(name, verb, obj):
    """Ground-truth verdict for a D1-shaped claim.

    Returns (True|False|None, reason). None = not decidable from teaching.
    """
    cls = CLASS_OF.get(name)
    if cls is None:
        return None, "unknown-name"
    if (cls, verb) in D3:
        w = D3[(cls, verb)]
        return (obj == w), ("d3-holds" if obj == w else "d3-violation")
    if (cls, verb) in D4:
        if obj == D4[(cls, verb)]:
            return False, "d4-violation"
    key = (name, verb)
    if key in TRUTH_OBJ:
        return (obj == TRUTH_OBJ[key]), (
            "fact-holds" if obj == TRUTH_OBJ[key] else "fact-clash")
    return None, "untaught"


def conflict_reasons(c1, c2):
    """Why two D1-shaped claims cannot both be true (possibly empty)."""
    (n1, v1, o1), (n2, v2, o2) = c1, c2
    reasons = []
    if n1 == n2 and v1 == v2 and o1 != o2:
        reasons.append("surface")
    cl1, cl2 = CLASS_OF.get(n1), CLASS_OF.get(n2)
    if (cl1 is not None and cl1 == cl2 and v1 == v2 and o1 != o2
            and (cl1, v1) in D3):
        reasons.append("d3-mediated")
    t1, _ = eval_claim(*c1)
    t2, _ = eval_claim(*c2)
    if t1 is False or t2 is False:
        reasons.append("one-false")
    return reasons


def parse_d1(clause):
    name, verb, obj = clause.split(" ", 2)
    assert re.fullmatch(r"[A-Z][a-z]+", name), clause
    assert re.fullmatch(r"[a-z]+", verb), clause
    assert re.fullmatch(r"[a-z]+(?: [a-z]+)*", obj), clause
    return name, verb, obj


# ------------------------------------------------------------ wire format
NAME_RE = r"[A-Z][a-z]+"
SHAPE_RES = {
    "D1": re.compile(rf"^{NAME_RE} [a-z]+ [a-z]+(?: [a-z]+)*\.$"),
    "D2": re.compile(rf"^{NAME_RE} is a [a-z]+\.$"),
    "D3": re.compile(r"^Every [a-z]+ [a-z]+ [a-z]+(?: [a-z]+)*\.$"),
    "D4": re.compile(r"^No [a-z]+ [a-z]+ [a-z]+(?: [a-z]+)*\.$"),
    "Q1": re.compile(r"^Is it true that .+\?$"),
    "Q2": re.compile(r"^Which [a-z]+ [a-z]+ [a-z]+(?: [a-z]+)*\?$"),
    "Q3": re.compile(r"^First: .+\. Second: .+\. Do they agree\?$"),
    "Q4": re.compile(r"^Which teaching act stated: .+\?$"),
}


def check_text(text, shape):
    assert text.isascii(), text
    assert '"' not in text, text
    assert "  " not in text, text
    assert text == text.strip(), text
    assert len(text) <= 240, (len(text), text)
    assert SHAPE_RES[shape].match(text), (shape, text)


def split_q3(text):
    assert SHAPE_RES["Q3"].match(text), text
    body = text[len("First: "):-len(" Do they agree?")]
    a, b = body.split(". Second: ")
    return a, b


# ------------------------------------------------------------------ teach
def build_teach():
    teach = []
    for kind, cls, verb, words in PRINCIPLES:
        text = (f"Every {cls} {verb} {words}." if kind == "D3"
                else f"No {cls} {verb} {words}.")
        teach.append({"phase": "teach", "text": text,
                      "shape": kind, "truth": True, "corrupt": None})
    for n in NAMES:
        teach.append({"phase": "teach", "text": f"{n} is a {CLASS_OF[n]}.",
                      "shape": "D2", "truth": True, "corrupt": None})
    for name, verb, obj, truth, ckind in D1_SPECS:
        teach.append({"phase": "teach", "text": f"{name} {verb} {obj}.",
                      "shape": "D1", "truth": truth, "corrupt": ckind})
    assert len(teach) == 48
    assert len({it["text"] for it in teach}) == 48, "duplicate teach text"
    rng.shuffle(teach)
    for i, it in enumerate(teach):
        it["id"] = i
        check_text(it["text"], it["shape"])
    return teach


# ----------------------------------------------------------------- probes
probes = []
expected = {}


def add_probe(pid, cap, text, shape, verdict, detail=""):
    check_text(text, shape)
    assert all(p["id"] != pid for p in probes)
    assert all(p["text"] != text for p in probes)
    probes.append({"id": pid, "phase": "probe", "text": text})
    assert verdict in ("AFFIRM", "REJECT", "ABSTAIN", "CONTRA", "CITE")
    assert cap in ("contra", "false", "para", "truth", "abstain", "prov")
    expected[str(pid)] = {"cap": cap, "verdict": verdict, "detail": detail}


def build_contra(by_text):
    # ((name,verb,obj), (name,verb,obj), required_reason)
    pairs = [
        # principle-mediated: conflict only visible via the D3 + memberships
        (("Maren", "insures", "copper bonds"), ("Tavin", "insures", "silver ledgers"), "d3-mediated"),
        (("Borin", "ferries", "sealed letters"), ("Kessa", "ferries", "harbor skiffs"), "d3-mediated"),
        (("Petra", "steers", "river barges"), ("Halvar", "steers", "canal punts"), "d3-mediated"),
        (("Ysolde", "weighs", "grain sacks"), ("Corvin", "weighs", "iron weights"), "d3-mediated"),
        # surface-identical: same name+verb, different objects
        (("Maren", "exports", "salt"), ("Maren", "exports", "dried figs"), "surface"),
        (("Petra", "ferries", "sealed letters"), ("Petra", "ferries", "grain sacks"), "surface"),
        (("Ossian", "steers", "river barges"), ("Ossian", "steers", "harbor skiffs"), "surface"),
        (("Borin", "carries", "spice bundles"), ("Borin", "carries", "open coin"), "surface"),
        (("Maren", "insures", "copper bonds"), ("Maren", "insures", "silver ledgers"), "surface"),
        (("Dralin", "weighs", "spice bundles"), ("Dralin", "weighs", "iron weights"), "surface"),
        (("Halvar", "ferries", "harbor skiffs"), ("Halvar", "ferries", "night cargo"), "surface"),
        (("Ysolde", "calibrates", "brass scales"), ("Ysolde", "calibrates", "cracked scales"), "surface"),
    ]
    assert len(pairs) == 12
    for i, (c1, c2, required) in enumerate(pairs):
        reasons = conflict_reasons(c1, c2)
        assert required in reasons, (c1, c2, reasons)
        assert reasons, (c1, c2)
        if required == "d3-mediated":
            assert "surface" not in reasons, (c1, c2)  # genuinely principle-mediated
        a = f"{c1[0]} {c1[1]} {c1[2]}"
        b = f"{c2[0]} {c2[1]} {c2[2]}"
        add_probe(100 + i, "contra",
                  f"First: {a}. Second: {b}. Do they agree?",
                  "Q3", "CONTRA")


def build_false(by_text):
    # (name, verb, obj, principle_kind): inner violates a taught D3/D4 via a taught D2
    inners = [
        ("Maren", "insures", "silver ledgers", "D3"),
        ("Kessa", "ferries", "harbor skiffs", "D3"),
        ("Petra", "steers", "canal punts", "D3"),
        ("Nessia", "weighs", "iron weights", "D3"),
        ("Sarella", "insures", "tide policies", "D3"),
        ("Dralin", "ferries", "grain sacks", "D3"),
        ("Tavin", "exports", "contraband silk", "D4"),
        ("Dralin", "carries", "open coin", "D4"),
        ("Halvar", "ferries", "night cargo", "D4"),
        ("Corvin", "calibrates", "cracked scales", "D4"),
        ("Sarella", "exports", "contraband silk", "D4"),
        ("Kessa", "carries", "open coin", "D4"),
    ]
    assert len(inners) == 12
    for i, (name, verb, obj, pkind) in enumerate(inners):
        v, reason = eval_claim(name, verb, obj)
        assert v is False and "violation" in reason, (name, verb, obj, v, reason)
        table = D3 if pkind == "D3" else D4
        assert (CLASS_OF[name], verb) in table  # the principle is taught
        assert f"{name} is a {CLASS_OF[name]}." in by_text  # the D2 is taught
        add_probe(112 + i, "false",
                  f"Is it true that {name} {verb} {obj}?",
                  "Q1", "REJECT")


def build_para(by_text):
    # Q1: (source D1 text with period, reworded inner). Name token kept.
    q1s = [
        ("Maren exports salt.",           "Maren ships fine salt"),
        ("Borin ferries sealed letters.", "sealed letters are conveyed by Borin"),
        ("Petra steers river barges.",    "Petra guides the river barges"),
        ("Ysolde weighs grain sacks.",    "Ysolde measures sacks of grain"),
        ("Tavin insures copper bonds.",   "Tavin underwrites bonds of copper"),
        ("Kessa carries sealed letters.", "Kessa hauls letters that are sealed"),
    ]
    # Q2: (source D1 text with period, class, canonical verb, canonical obj, question)
    q2s = [
        ("Kessa carries sealed letters.",  "courier", "carries",    "sealed letters",
         "Which courier hauls letters that are sealed?"),
        ("Halvar ferries harbor skiffs.",  "pilot",   "ferries",    "harbor skiffs",
         "Which pilot conveys the harbor skiffs?"),
        ("Corvin exports cedar planks.",   "weigher", "exports",    "cedar planks",
         "Which weigher ships old cedar planks?"),
        ("Sarella exports dried figs.",    "broker",  "exports",    "dried figs",
         "Which broker ships dried figs?"),
        ("Nessia calibrates tide gauges.", "weigher", "calibrates", "tide gauges",
         "Which weigher tunes fine tide gauges?"),
        ("Dralin weighs spice bundles.",   "courier", "weighs",     "spice bundles",
         "Which courier measures fine spice bundles?"),
    ]
    assert len(q1s) == 6 and len(q2s) == 6
    for i, (src, inner) in enumerate(q1s):
        it = by_text[src]
        assert it["shape"] == "D1" and it["truth"] is True
        name = src.split(" ", 1)[0]
        assert name in inner.split(" "), (src, inner)  # Name token present
        v, _ = eval_claim(*parse_d1(src[:-1]))
        assert v is True
        add_probe(124 + i, "para",
                  f"Is it true that {inner}?", "Q1", "AFFIRM")
    for i, (src, cls, verb, obj, question) in enumerate(q2s):
        it = by_text[src]
        assert it["shape"] == "D1" and it["truth"] is True
        name = src.split(" ", 1)[0]
        assert CLASS_OF[name] == cls
        assert src == f"{name} {verb} {obj}."
        # the answer must be the unique name matching (class, verb, object)
        cands = [n for n in NAMES
                 if CLASS_OF[n] == cls and TRUTH_OBJ.get((n, verb)) == obj]
        assert cands == [name], (question, cands)
        add_probe(130 + i, "para", question, "Q2", "AFFIRM", detail=name)


def build_truth(by_text):
    reject_inners = [
        "Borin carries open coin",
        "Ossian steers harbor skiffs",
        "Maren exports dried figs",
        "Petra ferries grain sacks",
        "Kessa weighs iron weights",
        "Nessia exports cedar planks",
    ]
    affirm_inners = [
        "Maren exports salt",
        "Ysolde calibrates brass scales",
        "Dralin weighs spice bundles",
        "Halvar ferries harbor skiffs",
        "Corvin exports cedar planks",
    ]
    # every corrupted D1 is covered, and only corrupted D1s are REJECTed
    corrupt_texts = {it["text"] for it in by_text.values()
                     if it["shape"] == "D1" and it["truth"] is False}
    assert {r + "." for r in reject_inners} == corrupt_texts
    pid = 136
    for inner in reject_inners:
        it = by_text[inner + "."]
        assert it["truth"] is False
        v, reason = eval_claim(*parse_d1(inner))
        assert v is False, (inner, reason)
        add_probe(pid, "truth", f"Is it true that {inner}?", "Q1", "REJECT")
        pid += 1
    for inner in affirm_inners:
        it = by_text[inner + "."]
        assert it["shape"] == "D1" and it["truth"] is True
        v, reason = eval_claim(*parse_d1(inner))
        assert v is True, (inner, reason)
        add_probe(pid, "truth", f"Is it true that {inner}?", "Q1", "AFFIRM")
        pid += 1
    # novel composition: chaining a D2 membership through a D3 principle.
    # Entailed by teaching, but never stated outright as a D1.
    inner = "Sarella insures copper bonds"
    assert (inner + ".") not in by_text
    assert "Sarella is a broker." in by_text
    assert "Every broker insures copper bonds." in by_text
    v, reason = eval_claim(*parse_d1(inner))
    assert v is True, (inner, reason)
    add_probe(pid, "truth", f"Is it true that {inner}?", "Q1", "AFFIRM")
    assert pid == 147


def build_abstain(by_text):
    taught_true_keys = {(n, v) for n, v, o, t, k in D1_SPECS if t}
    q1s = [
        "Is it true that Zevran exports salt?",
        "Is it true that Mirella ferries sealed letters?",
        "Is it true that Osric weighs grain sacks?",
        "Is it true that Fenwick insures copper bonds?",
        "Is it true that Liora steers river barges?",
        "Is it true that Tammas calibrates brass scales?",
        "Is it true that Maren blends lantern oil?",
        "Is it true that Petra blends dried figs?",
        "Is it true that Ysolde blends sea charts?",
    ]
    q2s = [
        "Which pilot calibrates brass scales?",
        "Which weigher ferries sealed letters?",
        "Which broker steers river barges?",
    ]
    assert len(q1s) == 9 and len(q2s) == 3
    pid = 148
    for text in q1s:
        toks = text[:-1].split(" ")
        name, verb = toks[4], toks[5]
        assert text.startswith("Is it true that ") and text.endswith("?")
        if name in NEW_NAMES:
            assert name not in CLASS_OF  # never taught
        else:
            assert verb not in TEACH_VERBS, text  # novel verb: no taught match
            v, _ = eval_claim(name, verb, " ".join(toks[6:]))
            assert v is None, text
        add_probe(pid, "abstain", text, "Q1", "ABSTAIN")
        pid += 1
    for text in q2s:
        cls, verb = text[len("Which "):-1].split(" ", 2)[:2]
        assert (cls, verb) not in D3 and (cls, verb) not in D4  # no principle decides it
        assert not any(CLASS_OF[n] == cls and v == verb
                       for (n, v) in taught_true_keys)  # no taught match
        add_probe(pid, "abstain", text, "Q2", "ABSTAIN")
        pid += 1
    assert pid == 160


def build_prov(by_text, teach):
    true_d1_ids = [it["id"] for it in teach
                   if it["shape"] == "D1" and it["truth"] is True]
    assert len(true_d1_ids) == 22
    prov_ids = sorted(rng.sample(true_d1_ids, 12))
    id_to_text = {it["id"]: it["text"] for it in teach}
    for i, tid in enumerate(prov_ids):
        text = id_to_text[tid]
        assert text.endswith(".")
        inner = text[:-1]
        parse_d1(inner)  # canonical D1 shape
        assert (by_text[text]["shape"], by_text[text]["truth"]) == ("D1", True)
        add_probe(160 + i, "prov",
                  f"Which teaching act stated: {inner}?",
                  "Q4", "CITE", detail=str(tid))


# ------------------------------------------------------------------- main
def main():
    teach = build_teach()
    by_text = {it["text"]: it for it in teach}

    build_contra(by_text)
    build_false(by_text)
    build_para(by_text)
    build_truth(by_text)
    build_abstain(by_text)
    build_prov(by_text, teach)

    assert len(probes) == 72
    assert [p["id"] for p in probes] == list(range(100, 172))

    items = teach + probes
    items_path = OUT_DIR / "items.jsonl"
    with open(items_path, "w") as f:
        for it in items:
            f.write(json.dumps({"id": it["id"], "phase": it["phase"],
                                "text": it["text"]}) + "\n")

    expected_path = OUT_DIR / "expected.json"
    with open(expected_path, "w") as f:
        json.dump(expected, f, indent=2, sort_keys=True)
        f.write("\n")

    # ---- read-back verification (file integrity, independent of the build above)
    lines = items_path.read_text().splitlines()
    assert len(lines) == 120, len(lines)
    seen_ids = set()
    for ln in lines:
        o = json.loads(ln)
        assert set(o) == {"id", "phase", "text"}, o
        assert o["id"] not in seen_ids
        seen_ids.add(o["id"])
        assert o["phase"] in ("teach", "probe")
        check_text(o["text"], "Q4" if o["text"].startswith("Which teaching act stated: ")
                   else "Q1" if o["text"].startswith("Is it true that ")
                   else "Q2" if o["text"].startswith("Which ")
                   else "Q3" if o["text"].startswith("First: ")
                   else "D2" if " is a " in o["text"]
                   else "D3" if o["text"].startswith("Every ")
                   else "D4" if o["text"].startswith("No ")
                   else "D1")
    assert seen_ids == set(range(48)) | set(range(100, 172))

    exp = json.loads(expected_path.read_text())
    assert set(exp) == {str(i) for i in range(100, 172)}
    for k, v in exp.items():
        assert set(v) == {"cap", "verdict", "detail"}, (k, v)

    corrupt_ids = sorted(it["id"] for it in teach
                         if it["shape"] == "D1" and it["truth"] is False)
    kinds = {}
    for it in teach:
        if it["corrupt"]:
            kinds[it["corrupt"]] = kinds.get(it["corrupt"], 0) + 1
    print(f"seed={SEED} teach=48 probes=72")
    print(f"corrupt D1 ids: {corrupt_ids} kinds={kinds}")
    print("OK")


if __name__ == "__main__":
    main()
