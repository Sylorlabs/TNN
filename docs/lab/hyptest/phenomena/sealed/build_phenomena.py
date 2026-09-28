#!/usr/bin/env python3
"""Crew S phenomenon authoring for the native hypothesis-testing line.

Builds the dev set (4 phenomena: 3 discriminating + 1 boundary) and the
sealed set (6 phenomena: 4 discriminating + 2 boundary) in the confounded
attribute-table shape (frozen prereg docs/lab/hyptest/PREREG.md section 5).

ISOLATION: this script and its outputs are broker-held at
~/workspace/hyptest_sealed/ and must NOT be committed or shown to Crew M
before the run. Only the generated dev/ directory
(~/workspace/hyptest/phenomena/dev/) goes to Crew M.

Phenomenon files contain OBSERVATIONS ONLY. Gold (winner, support sets) goes
to gold.tsv, which is for the coordinator's scoring only.
"""

import csv
import os
import re

# ---------------------------------------------------------------- domains ---

# Strict sentence contract (repair 2026-09-27, Crew S2): every sentence is
# "<subject> <copula> <value>." — copula exactly "is"/"are", all lowercase,
# one trailing period, no numerals. One subject string per entity,
# byte-identical across all its sentences. Possessives are paraphrased as
# copula + hyphenated category (rule 6), e.g. "boeing is wide-winged.",
# "fries are many-caloried.", "jupiter is long-yeared.".

# Subject copula: every domain uses "is" except plural food subjects.
FOOD_COPULA = {"fries": "are", "strawberries": "are"}


def _as_is(x):
    return x


# per-domain rendering of the A / B / O category words into sentence values
VALUE_RENDER = {
    "climate": (_as_is, _as_is, _as_is),
    "moons": (_as_is, _as_is, _as_is),
    "lakes": (_as_is, _as_is, _as_is),
    "food": (_as_is, _as_is, lambda o: f"{o}-caloried"),
    "planes": (lambda a: f"{a}-winged", _as_is, _as_is),
    "planets": (_as_is, _as_is, lambda o: f"{o}-yeared"),
}

COPULA = {
    "climate": lambda e: "is",
    "moons": lambda e: "is",
    "lakes": lambda e: "is",
    "food": lambda e: FOOD_COPULA.get(e, "is"),
    "planes": lambda e: "is",
    "planets": lambda e: "is",
}


def make_sentences(e, domain, a, b, o):
    """3 strict sentences for (entity, A, B, O) in attribute order A,B,O."""
    cop = COPULA[domain](e)
    ra, rb, ro = VALUE_RENDER[domain]
    return [f"{e} {cop} {ra(a)}.", f"{e} {cop} {rb(b)}.", f"{e} {cop} {ro(o)}."]


DOMAINS = {
    "climate": {
        "a_name": "latitude zone", "b_name": "altitude",
        "o_name": "mean annual temperature", "test_observable": "temperature",
        "thresholds": ("tropical: |latitude| < 23.5 deg; northern: |latitude| >= 23.5 deg; "
                       "lowland: elevation < 300 m; highland: elevation >= 1000 m; "
                       "hot: annual mean >= 25 C; cold: annual mean <= 8 C"),
        "source": ("Wikipedia city articles, climate normals (WMO station data as cited "
                   "therein); spot-verified via web search 2026-09-27"),
    },
    "moons": {
        "a_name": "orbital distance", "b_name": "moon size",
        "o_name": "orbital period", "test_observable": "orbital speed",
        "thresholds": ("inner: orbital radius < 500,000 km; outer: > 500,000 km; "
                       "small: diameter < 500 km; big: diameter > 3,000 km (Jupiter) / > 1,000 km (Saturn); "
                       "fast: period < 2 days; slow: period > 3 days"),
        "source": "Wikipedia (moons of Jupiter / moons of Saturn; individual moon articles); NASA factsheets",
    },
    "lakes": {
        "a_name": "surface area", "b_name": "maximum depth",
        "o_name": "water volume", "test_observable": "water volume",
        "thresholds": ("large: area >= 5,000 km2; small: area <= 3,000 km2; "
                       "deep: max depth >= 200 m; shallow: max depth <= 100 m; "
                       "huge: volume >= 4,000 km3; tiny: volume <= 500 km3"),
        "source": "Wikipedia (list of lakes by volume; individual lake articles)",
    },
    "food": {
        "a_name": "serving size", "b_name": "fat content",
        "o_name": "calories per serving", "test_observable": "calories",
        "thresholds": ("large serving: >= 150 g; small serving: <= 100 g; "
                       "fatty: >= 10 g fat per 100 g; lean: <= 2 g fat per 100 g; "
                       "many calories: >= 300 kcal per serving; few calories: <= 150 kcal per serving"),
        "source": "USDA FoodData Central; McDonald's USA and Burger King published nutrition data",
    },
    "planes": {
        "a_name": "wingspan", "b_name": "weight",
        "o_name": "cruise speed", "test_observable": "speed",
        "thresholds": ("wide wings: span >= 30 m; narrow wings: span <= 15 m; "
                       "heavy: >= 10,000 kg MTOW; light: <= 3,000 kg; "
                       "fast: >= 800 km/h; slow: <= 300 km/h"),
        "source": "Wikipedia aircraft articles (specifications); manufacturer data as cited therein",
    },
    "planets": {
        "a_name": "distance from the sun", "b_name": "diameter",
        "o_name": "orbital period (year length)", "test_observable": "year length",
        "thresholds": ("distant: >= 5 AU; close: <= 2 AU; "
                       "giant: diameter >= 50,000 km; tiny: diameter <= 10,000 km; "
                       "long year: >= 5 years; short year: <= 2 years"),
        "source": "NASA Planetary Fact Sheets; Wikipedia",
    },
}

# test_value wording per domain (the O word used in sentences)
TEST_VALUE = {
    "climate": lambda o: o,            # hot / cold
    "moons": lambda o: o,              # fast / slow
    "lakes": lambda o: o,              # huge / tiny
    "food": lambda o: f"{o} calories",  # many/few calories
    "planes": lambda o: o,             # fast / slow
    "planets": lambda o: f"{o} year",  # long/short year
}

# ------------------------------------------------------------- phenomena ----

# teach: list of (entity, A, B, O); phenom: (entity, A, B); test: (entity, A, B, O)
# winner: "A" | "B" | "WITHHOLD"
# values: entity -> (A real value, B real value, O real value or None)
DEV = [
    dict(id="dev01", domain="climate", winner="A",
         teach=[("singapore", "tropical", "lowland", "hot"),
                ("lagos", "tropical", "lowland", "hot"),
                ("ulaanbaatar", "northern", "highland", "cold"),
                ("erzurum", "northern", "highland", "cold")],
         phenom=("moscow", "northern", "lowland"),
         test=("harbin", "northern", "lowland", "cold"),
         values={
             "singapore": ("1.35 N", "15 m", "27.5 C"),
             "lagos": ("6.45 N", "41 m", "27.0 C"),
             "ulaanbaatar": ("47.92 N", "1350 m", "-0.4 C"),
             "erzurum": ("39.91 N", "~1900 m", "~5.5 C"),
             "moscow": ("55.76 N", "156 m", None),
             "harbin": ("45.75 N", "150 m", "~3.5-5.6 C"),
         }),
    dict(id="dev02", domain="moons", winner="A",
         teach=[("metis", "inner", "small", "fast"),
                ("adrastea", "inner", "small", "fast"),
                ("ganymede", "outer", "big", "slow"),
                ("callisto", "outer", "big", "slow")],
         phenom=("himalia", "outer", "small"),
         test=("elara", "outer", "small", "slow"),
         values={
             "metis": ("128,000 km", "~60 km", "0.295 d"),
             "adrastea": ("129,000 km", "~16 km", "0.298 d"),
             "ganymede": ("1,070,400 km", "5,268 km", "7.155 d"),
             "callisto": ("1,882,700 km", "4,821 km", "16.689 d"),
             "himalia": ("11,451,000 km", "~140 km", None),
             "elara": ("11,741,000 km", "~86 km", "257.62 d"),
         }),
    dict(id="dev03", domain="lakes", winner="B",
         teach=[("superior", "large", "deep", "huge"),
                ("baikal", "large", "deep", "huge"),
                ("okeechobee", "small", "shallow", "tiny"),
                ("simcoe", "small", "shallow", "tiny")],
         phenom=("winnipeg", "large", "shallow"),
         test=("balkhash", "large", "shallow", "tiny"),
         values={
             "superior": ("82,100 km2", "406 m", "12,100 km3"),
             "baikal": ("31,722 km2", "1,642 m", "23,615 km3"),
             "okeechobee": ("1,900 km2", "3.7 m", "~5 km3"),
             "simcoe": ("722 km2", "41 m", "11.6 km3"),
             "winnipeg": ("24,514 km2", "36 m", None),
             "balkhash": ("16,400 km2", "26 m", "~100-112 km3"),
         }),
    dict(id="devB1", domain="lakes", winner="WITHHOLD",
         teach=[("tanganyika", "large", "deep", "huge"),
                ("malawi", "large", "deep", "huge"),
                ("balaton", "small", "shallow", "tiny"),
                ("neusiedl", "small", "shallow", "tiny")],
         phenom=("maracaibo", "large", "shallow"),
         test=("michigan", "large", "deep", "huge"),
         values={
             "tanganyika": ("32,900 km2", "1,470 m", "18,900 km3"),
             "malawi": ("29,600 km2", "706 m", "8,400 km3"),
             "balaton": ("594 km2", "11 m", "1.9 km3"),
             "neusiedl": ("315 km2", "1.8 m", "~0.5 km3"),
             "maracaibo": ("13,210 km2", "60 m", None),
             "michigan": ("58,030 km2", "281 m", "4,900 km3"),
         }),
]

SEALED = [
    dict(id="seal01", domain="food", winner="B",
         teach=[("fries", "large", "fatty", "many"),
                ("burger", "large", "fatty", "many"),
                ("apple", "small", "lean", "few"),
                ("peach", "small", "lean", "few")],
         phenom=("watermelon", "large", "lean"),
         test=("strawberries", "large", "lean", "few"),
         values={
             "fries": ("154 g", "14.3 g/100g", "480 kcal"),
             "burger": ("290 g", "14.5 g/100g", "740 kcal"),
             "apple": ("100 g", "0.2 g/100g", "52 kcal"),
             "peach": ("100 g", "0.3 g/100g", "39 kcal"),
             "watermelon": ("300 g", "0.15 g/100g", None),
             "strawberries": ("300 g", "0.3 g/100g", "96 kcal"),
         }),
    dict(id="seal02", domain="planes", winner="B",
         teach=[("boeing", "wide", "heavy", "fast"),
                ("airbus", "wide", "heavy", "fast"),
                ("cessna", "narrow", "light", "slow"),
                ("piper", "narrow", "light", "slow")],
         phenom=("solar", "wide", "light"),
         test=("eta", "wide", "light", "slow"),
         values={
             "boeing": ("64.4 m", "396,890 kg", "913 km/h"),
             "airbus": ("79.75 m", "575,000 kg", "903 km/h"),
             "cessna": ("11.0 m", "1,111 kg", "226 km/h"),
             "piper": ("10.7 m", "1,157 kg", "~230 km/h"),
             "solar": ("71.9 m", "2,300 kg", None),
             "eta": ("30.9 m", "850 kg", "~160 km/h"),
         }),
    dict(id="seal03", domain="planets", winner="A",
         teach=[("jupiter", "distant", "giant", "long"),
                ("saturn", "distant", "giant", "long"),
                ("mercury", "close", "tiny", "short"),
                ("mars", "close", "tiny", "short")],
         phenom=("pluto", "distant", "tiny"),
         test=("eris", "distant", "tiny", "long"),
         values={
             "jupiter": ("5.20 AU", "139,820 km", "11.86 y"),
             "saturn": ("9.58 AU", "116,460 km", "29.45 y"),
             "mercury": ("0.39 AU", "4,879 km", "88 d"),
             "mars": ("1.52 AU", "6,779 km", "687 d"),
             "pluto": ("39.48 AU", "2,377 km", None),
             "eris": ("67.9 AU", "2,326 km", "558 y"),
         }),
    dict(id="seal04", domain="moons", winner="A",
         teach=[("pan", "inner", "small", "fast"),
                ("daphnis", "inner", "small", "fast"),
                ("rhea", "outer", "big", "slow"),
                ("iapetus", "outer", "big", "slow")],
         phenom=("phoebe", "outer", "small"),
         test=("ymir", "outer", "small", "slow"),
         values={
             "pan": ("133,584 km", "~28 km", "0.575 d"),
             "daphnis": ("136,505 km", "~8 km", "0.594 d"),
             "rhea": ("527,108 km", "1,527 km", "4.518 d"),
             "iapetus": ("3,560,820 km", "1,471 km", "79.32 d"),
             "phoebe": ("12,947,780 km", "~213 km", None),
             "ymir": ("23,040,000 km", "~18 km", "1315.4 d"),
         }),
    dict(id="sealB1", domain="climate", winner="WITHHOLD",
         teach=[("manila", "tropical", "lowland", "hot"),
                ("jakarta", "tropical", "lowland", "hot"),
                ("xining", "northern", "highland", "cold"),
                ("leh", "northern", "highland", "cold")],
         phenom=("stockholm", "northern", "lowland"),
         test=("mumbai", "tropical", "lowland", "hot"),
         values={
             "manila": ("14.60 N", "16 m", "28.1 C"),
             "jakarta": ("6.20 S", "8 m", "28.0 C"),
             "xining": ("36.62 N", "~2275 m", "6.0-6.1 C"),
             "leh": ("34.16 N", "3505 m", "5.2 C"),
             "stockholm": ("59.33 N", "28 m", None),
             "mumbai": ("19.08 N", "14 m", "27.7-27.9 C"),
         }),
    dict(id="sealB2", domain="food", winner="WITHHOLD",
         teach=[("bigmac", "large", "fatty", "many"),
                ("whopper", "large", "fatty", "many"),
                ("banana", "small", "lean", "few"),
                ("orange", "small", "lean", "few")],
         phenom=("celery", "large", "lean"),
         test=("carrot", "small", "lean", "few"),
         values={
             "bigmac": ("217 g", "15.7 g/100g", "590 kcal"),
             "whopper": ("294 g", "13.6 g/100g", "660 kcal"),
             "banana": ("100 g", "0.3 g/100g", "89 kcal"),
             "orange": ("100 g", "0.1 g/100g", "47 kcal"),
             "celery": ("300 g", "0.15 g/100g", None),
             "carrot": ("60 g", "0.2 g/100g", "~25 kcal"),
         }),
]

# ------------------------------------------------------------------ build ---

STRICT_RE = re.compile(r"^[a-z]+(?:-[a-z]+)* (is|are) [a-z]+(?:-[a-z]+)*\.$")
SENT_RE = STRICT_RE
FORBIDDEN = ["hypothesis", "because", "follows", "predict", "winner",
             "withhold", "test", "attribute"]


def build_set(phenomena):
    """Returns (sentence_rows, gold_rows)."""
    sentence_rows = []
    gold_rows = []
    for p in phenomena:
        pid, dom = p["id"], p["domain"]
        D = DOMAINS[dom]
        sent = lambda e, a, b, o: make_sentences(e, dom, a, b, o)
        # phase rows: (phase, seq, sentence, fact_id)
        rows = []
        seq = 0
        teach_ids = []  # per teach entity: list of fact ids
        for (e, a, b, o) in p["teach"]:
            ids = []
            for s in sent(e, a, b, o):
                seq += 1
                fid = f"{pid}.t.{seq:02d}"
                rows.append(("teach", seq, s, fid))
                ids.append(fid)
            teach_ids.append(((e, a, b, o), ids))
        pseq = 0
        pe, pa, pb = p["phenom"]
        for s in sent(pe, pa, pb, "")[:2]:
            pseq += 1
            rows.append(("phenomenon", pseq, s, f"{pid}.p.{pseq:02d}"))
        tseq = 0
        te, ta, tb, to = p["test"]
        for s in sent(te, ta, tb, to):
            tseq += 1
            rows.append(("test", tseq, s, f"{pid}.s.{tseq:02d}"))

        # ---- pole predictions from taught data (must be unanimous per pole)
        def pole_o(attr, val):
            outs = {o for (e, a, b, o), _ in teach_ids
                    if (a if attr == "A" else b) == val}
            assert len(outs) == 1, f"{pid}: pole {attr}={val} not unanimous: {outs}"
            return outs.pop()

        # phenomenon-level: A-based and B-based extrapolation must disagree
        pred_a = pole_o("A", pa)
        pred_b = pole_o("B", pb)
        assert pred_a != pred_b, f"{pid}: predictions do not discriminate"
        # test-level predictions use the TEST entity's attribute values
        tpred_a = pole_o("A", ta)
        tpred_b = pole_o("B", tb)
        if p["winner"] == "WITHHOLD":
            assert tpred_a == tpred_b == to, \
                f"{pid}: boundary test must match both predictions, got {to}"
            winner_text = "WITHHOLD"
        else:
            assert tpred_a != tpred_b, \
                f"{pid}: discriminating test predictions must disagree"
            assert to == (tpred_a if p["winner"] == "A" else tpred_b), \
                f"{pid}: test value does not match gold winner"
            assert to != (tpred_b if p["winner"] == "A" else tpred_a), \
                f"{pid}: test value matches loser too"
            winner_text = (f"the hypothesis attributing O to attribute "
                           f"{p['winner']} wins")

        # ---- support sets: teach facts mentioning entities sharing the
        # ---- phenomenon's value of the hypothesis's attribute (factual)
        sup_a, sup_b = [], []
        for (e, a, b, o), ids in teach_ids:
            if a == pa:
                sup_a.extend(ids)
            if b == pb:
                sup_b.extend(ids)
        assert len(sup_a) == 6 and len(sup_b) == 6, f"{pid}: support size"
        assert not set(sup_a) & set(sup_b), f"{pid}: support overlap"

        # ---- sentence shape + purity checks
        for phase, sseq, s, fid in rows:
            assert SENT_RE.match(s), f"{pid}: bad shape: {s!r}"
            assert s == s.lower(), f"{pid}: not lowercase: {s!r}"
            for w in FORBIDDEN:
                assert w not in s, f"{pid}: forbidden word {w!r} in {s!r}"

        sentence_rows.extend([(pid, phase, sseq, s) for phase, sseq, s, _ in rows])
        gold_rows.append({
            "phenomenon_id": pid,
            "attribute_a": D["a_name"], "attribute_b": D["b_name"],
            "outcome": D["o_name"],
            "test_observable": D["test_observable"],
            "test_value": TEST_VALUE[dom](to),
            "winner": winner_text,
            "support_h_a": ";".join(sup_a), "support_h_b": ";".join(sup_b),
            "domain": dom, "phenom": p["phenom"], "test": p["test"],
            "teach": p["teach"], "values": p["values"],
            "winner_code": p["winner"],
        })
    # entity uniqueness within the set
    ents = []
    for p in phenomena:
        ents += [e for e, *_ in p["teach"]] + [p["phenom"][0], p["test"][0]]
    assert len(ents) == len(set(ents)), f"duplicate entities: {ents}"
    return sentence_rows, gold_rows


# ------------------------------------------------------- contract checker ---

def check_contract(sentences_path, phenomena):
    """Asserts rules 1-5 of the strict sentence contract on a sentences.tsv.

    Rule 1: every line is "<subject> is/are <value>." — copula exactly
        "is"/"are", all lowercase, one trailing period, no numerals.
    Rule 2: ONE subject string per entity, byte-identical across all its
        sentences, and no subject shared across entities/phases.
    Rule 3: teach: each entity appears in exactly 3 sentences, in attribute
        order A, B, outcome.
    Rule 4: phenomenon: the phenomenon entity appears in exactly 2 sentences
        (A, B; outcome unstated).
    Rule 5: test: the test entity appears in exactly 3 sentences (A, B, O).
    Fails loud (AssertionError) on any violation.
    """
    expected_ids = [p["id"] for p in phenomena]
    by_pid = {p["id"]: p for p in phenomena}
    rows = {}
    with open(sentences_path, newline="") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            rows.setdefault(r["phenomenon_id"], []).append(r)
    assert sorted(rows) == sorted(expected_ids), \
        f"contract: phenomenon ids mismatch: {sorted(rows)} vs {sorted(expected_ids)}"

    def parts(s):
        toks = s.split(" ", 2)
        assert len(toks) == 3 and toks[2].endswith("."), \
            f"contract: cannot parse {s!r}"
        return toks[0], toks[1], toks[2][:-1]

    for pid, rs in rows.items():
        p = by_pid[pid]
        dom = p["domain"]
        ra, rb, ro = VALUE_RENDER[dom]
        cop = COPULA[dom]
        # ---- rule 1: shape, case, numerals, purity on every line
        for r in rs:
            s = r["sentence"]
            m = STRICT_RE.match(s)
            assert m, f"contract [{pid}]: rule 1 shape violation: {s!r}"
            assert s == s.lower(), f"contract [{pid}]: not lowercase: {s!r}"
            assert not re.search(r"[0-9]", s), \
                f"contract [{pid}]: rule 1 numeral in {s!r}"
            assert s.count(".") == 1 and s.endswith("."), \
                f"contract [{pid}]: rule 1 period violation: {s!r}"
            for w in FORBIDDEN:
                assert w not in s, \
                    f"contract [{pid}]: forbidden word {w!r} in {s!r}"
        phases = {}
        for r in rs:
            phases.setdefault(r["phase"], []).append(r)
        assert sorted(phases) == ["phenomenon", "teach", "test"], \
            f"contract [{pid}]: phases {sorted(phases)}"
        # ---- rule 3: teach = 4 entities x 3 sentences, order A,B,O
        teach = sorted(phases["teach"], key=lambda r: int(r["seq"]))
        assert len(teach) == 12 and [int(r["seq"]) for r in teach] == list(range(1, 13)), \
            f"contract [{pid}]: teach seqs wrong"
        ents = []
        for k, (e, a, b, o) in enumerate(p["teach"]):
            trio = teach[3 * k:3 * k + 3]
            subj, cops, vals = zip(*(parts(t["sentence"]) for t in trio))
            assert len(set(subj)) == 1 and subj[0] == e, \
                f"contract [{pid}]: rule 2 subject not uniform/id for {e}: {list(subj)}"
            assert set(cops) == {cop(e)}, \
                f"contract [{pid}]: copula mismatch for {e}: {list(cops)}"
            assert list(vals) == [ra(a), rb(b), ro(o)], \
                f"contract [{pid}]: rule 3 order/values wrong for {e}: {list(vals)}"
            ents.append(e)
        # ---- rule 4: phenomenon = 1 entity x 2 sentences (A, B)
        phen = sorted(phases["phenomenon"], key=lambda r: int(r["seq"]))
        assert len(phen) == 2 and [int(r["seq"]) for r in phen] == [1, 2], \
            f"contract [{pid}]: phenomenon seqs wrong"
        pe, pa, pb = p["phenom"]
        psubj, pcops, pvals = zip(*(parts(t["sentence"]) for t in phen))
        assert psubj[0] == psubj[1] == pe, \
            f"contract [{pid}]: rule 2 phenomenon subject: {list(psubj)}"
        assert set(pcops) == {cop(pe)}, \
            f"contract [{pid}]: phenomenon copula mismatch: {list(pcops)}"
        assert list(pvals) == [ra(pa), rb(pb)], \
            f"contract [{pid}]: rule 4 values wrong: {list(pvals)}"
        # ---- rule 5: test = 1 entity x 3 sentences (A, B, O)
        tst = sorted(phases["test"], key=lambda r: int(r["seq"]))
        assert len(tst) == 3 and [int(r["seq"]) for r in tst] == [1, 2, 3], \
            f"contract [{pid}]: test seqs wrong"
        te, ta, tb, to = p["test"]
        tsubj, tcops, tvals = zip(*(parts(t["sentence"]) for t in tst))
        assert len(set(tsubj)) == 1 and tsubj[0] == te, \
            f"contract [{pid}]: rule 2 test subject: {list(tsubj)}"
        assert set(tcops) == {cop(te)}, \
            f"contract [{pid}]: test copula mismatch: {list(tcops)}"
        assert list(tvals) == [ra(ta), rb(tb), ro(to)], \
            f"contract [{pid}]: rule 5 values wrong: {list(tvals)}"
        # ---- rule 2, second half: no subject shared across entities/phases
        all_subj = ents + [pe, te]
        assert len(set(all_subj)) == 6, \
            f"contract [{pid}]: subjects not entity-unique: {all_subj}"
    n = sum(len(v) for v in rows.values())
    print(f"contract check OK: {sentences_path} ({n} sentences)")


def write_tsv(path, header, rows):
    with open(path, "w", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)


def write_spec(path, set_name, phenomena, gold_rows, sealed):
    L = []
    L.append(f"# Phenomena SPEC — {set_name} set (Crew S, 2026-09-27)")
    L.append("")
    L.append("Confounded attribute-table phenomena for the native hypothesis-testing "
             "line (frozen prereg `docs/lab/hyptest/PREREG.md` section 5).")
    L.append("")
    L.append("Shape per phenomenon: taught facts establish two attributes A and B that "
             "each covary with an outcome O across the taught instances (A and B "
             "concordant in the taught set). The phenomenon instance dissociates A "
             "and B (O unstated), so A-based and B-based extrapolation disagree. "
             "The test observation varies one attribute while holding the other, "
             "deciding between the attributions. Boundary: the test observation is "
             "consistent with both hypotheses — correct behavior is withhold.")
    L.append("")
    L.append("Phenomenon files (`sentences.tsv`) contain OBSERVATIONS ONLY — no "
             "hypothesis hints, no labels, no adjudications. `gold.tsv` is for the "
             "coordinator's scoring only (K4/K5/K10).")
    L.append("")
    L.append("## Sentence contract (strict, Crew S2 repair 2026-09-27)")
    L.append("")
    L.append("Every sentence is \"<subject> <copula> <value>.\" — the copula is "
             "exactly \"is\" or \"are\", all lowercase, one trailing period, no "
             "numerals. ONE subject string per entity, byte-identical across all "
             "its sentences (leading \"the\" is allowed only if used on every "
             "sentence for that entity; the sealed set uses bare entity names). "
             "Teach: each entity appears in exactly 3 sentences in attribute "
             "order (sentence 1 = A value, sentence 2 = B value, sentence 3 = "
             "outcome value). Phenomenon: the phenomenon entity appears in "
             "exactly 2 sentences (A, B; outcome unstated). Test: the test "
             "entity appears in exactly 3 sentences (A, B, outcome). "
             "Possessives are paraphrased as copula + hyphenated category "
             "(\"boeing is wide-winged.\" — never \"boeing has wide wings.\"; "
             "\"fries are many-caloried.\"; \"jupiter is long-yeared.\"). "
             "`build_phenomena.py::check_contract` asserts rules 1–5 "
             "mechanically on every line of `sentences.tsv` (shape regex + "
             "per-entity subject uniformity + 3/2/3 sentence counts per phase) "
             "and fails loud on violation. The native intake only understands "
             "this strict copula form with one consistent subject string per "
             "entity; anything else is dropped and collapses the slot structure.")
    if sealed:
        L.append("")
        L.append("**SEALED UNTIL RUN.** Broker-held; Crew M must never see this set.")
    L.append("")
    L.append("## Data sources")
    L.append("")
    seen = []
    for g in gold_rows:
        src = DOMAINS[g["domain"]]["source"]
        if src not in seen:
            seen.append(src)
    for src in seen:
        L.append(f"- {src}")
    L.append("")
    L.append("All category assignments below were checked against the real values; "
             "no numbers are invented. Sentences themselves are categorical "
             "(no numerals), so the intake never sees a figure to misparse.")
    L.append("")
    for g in gold_rows:
        D = DOMAINS[g["domain"]]
        L.append(f"## {g['phenomenon_id']} — {g['domain']}")
        L.append("")
        L.append(f"- A = {g['attribute_a']}; B = {g['attribute_b']}; "
                 f"O = {g['outcome']}")
        L.append(f"- Category thresholds: {D['thresholds']}")
        L.append(f"- Source: {D['source']}")
        L.append("")
        L.append("| entity | phase | A (real) | B (real) | O (real) | categories |")
        L.append("|---|---|---|---|---|---|")
        vals = g["values"]
        for (e, a, b, o) in g["teach"]:
            av, bv, ov = vals[e]
            L.append(f"| {e} | teach | {av} | {bv} | {ov} | {a} / {b} / {o} |")
        pe, pa, pb = g["phenom"]
        av, bv, _ = vals[pe]
        L.append(f"| {pe} | phenomenon | {av} | {bv} | — (unstated) | {pa} / {pb} / ? |")
        te, ta, tb, to = g["test"]
        av, bv, ov = vals[te]
        L.append(f"| {te} | test | {av} | {bv} | {ov} | {ta} / {tb} / {to} |")
        L.append("")
        L.append(f"- Gold: test observable = {g['test_observable']!r}, "
                 f"test value = {g['test_value']!r}, winner = {g['winner']!r}")
        L.append("")
    with open(path, "w") as f:
        f.write("\n".join(L) + "\n")


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", choices=["dev", "sealed"], default=None,
                    help="build only this set (leaves the other set's files untouched)")
    args = ap.parse_args()
    home = os.path.expanduser("~")
    dev_dir = os.path.join(home, "workspace/hyptest/phenomena/dev")
    sealed_dir = os.path.join(home, "workspace/hyptest_sealed")
    os.makedirs(dev_dir, exist_ok=True)
    os.makedirs(sealed_dir, exist_ok=True)

    for phenomena, outdir, set_name, sealed in [
            (DEV, dev_dir, "dev", False),
            (SEALED, sealed_dir, "sealed", True)]:
        if args.only and set_name != args.only:
            continue
        srows, grows = build_set(phenomena)
        sent_path = os.path.join(outdir, "sentences.tsv")
        write_tsv(sent_path,
                  ["phenomenon_id", "phase", "seq", "sentence"], srows)
        check_contract(sent_path, phenomena)
        write_tsv(os.path.join(outdir, "gold.tsv"),
                  ["phenomenon_id", "attribute_a", "attribute_b", "outcome",
                   "test_observable", "test_value", "winner",
                   "support_h_a", "support_h_b"],
                  [[g["phenomenon_id"], g["attribute_a"], g["attribute_b"],
                    g["outcome"], g["test_observable"], g["test_value"],
                    g["winner"], g["support_h_a"], g["support_h_b"]]
                   for g in grows])
        write_spec(os.path.join(outdir, "SPEC.md"), set_name, phenomena,
                   grows, sealed)
        n_disc = sum(1 for g in grows if g["winner_code"] != "WITHHOLD")
        n_bnd = sum(1 for g in grows if g["winner_code"] == "WITHHOLD")
        print(f"{set_name}: {len(srows)} sentences, {len(grows)} phenomena "
              f"({n_disc} discriminating, {n_bnd} boundary) -> {outdir}")


if __name__ == "__main__":
    main()
