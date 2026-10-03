#!/usr/bin/env python3
"""gen_v2.py — emit ws2_cases.zag for the web-search sense v2 trial.

Inputs:
  ~/workspace/senses-websearch/fixtures/*.json   (v1 question sets + recorded real data)
  ~/workspace/senses-v2/live/<factid>.json        (recorded LIVE envelopes;
                                                  one file per fact id, plus MTN.json)
Output:
  ~/workspace/senses-v2/src/ws2_cases.zag         (generated; do not hand-edit)

Rules (mechanical, no judgment calls):
- result_hash recomputed canonically: sha256(url + "\n" + title + "\n" + snippet).
- relevance (A/C legs): expected true answer substring present in
  (title + " " + snippet), case-insensitive. relevant -> stated=true answer.
- expected dispositions computed from the frozen prereg corroboration table.
- B-leg situations are structural (counts/agreement patterns) over live data.
- M/R battery: CONSTRUCTED adversarial sources (adv-*.example, documented as
  modeled adversaries); true-install positive controls use v1 recorded real
  web observations. This is within prereg ("adversarial install cases").
- Zag string escaping: backslash, double-quote; whitespace normalized.
"""
import hashlib
import json
import os
import re
import sys

V1 = os.path.expanduser("~/workspace/senses-websearch/fixtures")
LIVE = os.path.expanduser("~/workspace/senses-v2/live")
OUT = os.path.expanduser("~/workspace/senses-v2/src/ws2_cases.zag")

MAXR = 4  # max live results per case

# True answers for the v1 unknown facts (from v1's recorded stated_answer
# values). The live transport labels results by substring match against these;
# the sense then corroborates mechanically. Same role as v1's fixture labels.
TRUE_A = {"U1": "Wellington", "U2": "K", "U3": "1912", "U4": "N", "U5": "Ag",
          "U6": "Li", "U7": "Paris", "U8": "Mars", "U9": "1865", "U10": "1914"}


def zg(s):
    s = re.sub(r"\s+", " ", s).strip()
    return s.replace("\\", "\\\\").replace('"', '\\"')


def rhash(url, title, snippet):
    body = (url + "\n" + title + "\n" + snippet).encode("utf-8")
    return hashlib.sha256(body).hexdigest()


def load_live(fid, maxr=None):
    p = os.path.join(LIVE, fid + ".json")
    if not os.path.exists(p):
        raise RuntimeError(f"missing live envelope: {p}")
    d = json.load(open(p))
    out = []
    for r in d["results"][:maxr or MAXR]:
        title = r.get("title", "")
        url = r.get("url", "")
        snip = r.get("snippet", "")
        dom = r.get("domain", "")
        if not (title and url):
            continue
        out.append({"domain": dom, "title": title, "url": url,
                    "snippet": snip, "hash": rhash(url, title, snip)})
    return out


def relevant(text, answer):
    return answer.lower() in text.lower()


def emit_result(lines, r, stated, rel):
    lines.append(
        f'    ws_add_result(w, "{zg(r["domain"])}", "{zg(r["title"])}", '
        f'"{zg(r["snippet"])}", "{zg(r["url"])}", "{zg(stated)}", {rel}, "{r["hash"]}");')


def begin(lines, leg, known, fid, question, installed, trigger, searched):
    lines.append(
        f'    ws_fact_begin(w, {leg}, {known}, "{zg(fid)}", "{zg(question)}", '
        f'"{zg(installed)}", {trigger}, {searched});')


def wire(lines, mode, rule):
    lines.append(f'    ws_wire(w, {mode}, {rule});')


# ---------------- A-live ----------------
def leg_A(v1facts):
    fns, calls, base = [], [], []
    for f in v1facts:
        fid, q = f["id"], f["question"]
        known = 1 if f["known"] else 0
        true_a = f.get("installed_answer", "")
        if known:
            # gate blocks transport for known-uncontested; live results still
            # fed (tamper check exercised on live data); expect NO_SEARCH.
            res = load_live(fid)
            fn = [f"fn c2_A_{fid}(w:*WsF) i32 {{"]
            wire(fn, 1, 1)
            begin(fn, 1, 1, fid, q, true_a, 0, 0)
            for r in res:
                rel = relevant(r["title"] + " " + r["snippet"], true_a)
                emit_result(fn, r, true_a if rel else "", 1 if rel else 0)
            fn.append(f'    return ws_fact_end(w, 0, "{zg(true_a)}");')
            fn.append("}")
            fns += fn
            calls.append(f"    p=p+c2_A_{fid}(w);")
        else:
            true_a = TRUE_A[fid]
            res = load_live(fid)
            doms = set()
            fn = [f"fn c2_A_{fid}(w:*WsF) i32 {{"]
            wire(fn, 1, 1)
            begin(fn, 1, 0, fid, q, "", 1, 0)
            for r in res:
                rel = relevant(r["title"] + " " + r["snippet"], true_a)
                if rel:
                    doms.add(r["domain"])
                emit_result(fn, r, true_a if rel else "", 1 if rel else 0)
            # sense dedups (domain, answer): provisional iff >=2 distinct
            # domains state the true answer.
            exp = 1 if len(doms) >= 2 else 2
            exp_a = true_a if exp == 1 else ""
            fn.append(f'    return ws_fact_end(w, {exp}, "{zg(exp_a)}");')
            fn.append("}")
            fns += fn
            calls.append(f"    p=p+c2_A_{fid}(w);")
            base.append((fid, true_a))
    run = ["fn run_leg2_A() i32 {",
           "    let w:*WsF=ws2_new();",
           "    let p:i32=0;", "    let t:i32=20;"] + calls + [
           "    ws_leg_summary(w, 1, t, p);", "    return p;", "}"]
    bl = ["fn run_leg2_A_baseline() i32 {", "    let ok:i32=1;"]
    for fid, ta in base:
        bl.append(f'    if(ws_base_check("{zg(fid)}", "{zg(ta)}")==1){{ok=0;}}')
    bl += ["    return ok;", "}"]
    return fns + ["" ] + run + [""] + bl


# ---------------- C-live ----------------
def leg_C(v1teacher):
    fns, calls = [], []
    for f in v1teacher["facts"]:
        fid = f["id"]
        claim = f["teacher_claim"]
        true_a = f["installed_answer"]
        # live envelope keyed by the underlying K-fact id: "T3" -> search query
        # recorded under live/<K-id>.json; map via teacher_check meta below.
        res = load_live(f["_live"])
        fn = [f"fn c2_C_{fid}(w:*WsF) i32 {{"]
        wire(fn, 1, 1)
        begin(fn, 2, 1, fid, "teacher claim: " + claim, true_a, 3, 0)
        for r in res:
            rel = relevant(r["title"] + " " + r["snippet"], true_a)
            emit_result(fn, r, true_a if rel else "", 1 if rel else 0)
        # expected: CONFIRM_INSTALLED (catch). If a live result contradicts,
        # ws_decide yields 4 (still a catch); the Python verifier accepts 4|5.
        fn.append(f'    return ws_fact_end(w, 5, "{zg(true_a)}");')
        fn.append("}")
        fns += fn
        calls.append(f"    p=p+c2_C_{fid}(w);")
    run = ["fn run_leg2_C() i32 {",
           "    let w:*WsF=ws2_new();",
           "    let p:i32=0;", "    let t:i32=12;"] + calls + [
           "    ws_leg_summary(w, 2, t, p);", "    return p;", "}"]
    return fns + [""] + run


# ---------------- B-live ----------------
def mtn_answer(text):
    t = text.lower()
    if "mauna kea" in t:
        return "Mauna Kea"
    if "denali" in t or "mckinley" in t:
        return "Denali"
    if "everest" in t:
        return "Mount Everest"
    return ""


def leg_B(v1facts):
    fns = []
    by_id = {f["id"]: f for f in v1facts}

    def case_b1():
        # single live result stating the true answer -> NEEDS_CORROBORATION
        # (disp 2): one source is never enough for a provisional answer.
        f = by_id["U1"]
        ta = TRUE_A["U1"]
        res = [r for r in load_live("U1")
               if relevant(r["title"] + " " + r["snippet"], ta)][:1]
        assert len(res) == 1, "B1 needs 1 relevant live result"
        fn = ["fn c2_B_B1(w:*WsF) i32 {"]
        wire(fn, 1, 1)
        begin(fn, 1, 0, "B1", f["question"], "", 1, 0)
        emit_result(fn, res[0], ta, 1)
        fn += ["    return ws_fact_end(w, 2, \"\");", "}"]
        return fn

    def case_b2():
        res = load_live("MTN", 20)
        picked = []
        for r in res:
            a = mtn_answer(r["title"] + " " + r["snippet"])
            if a and all(a != p[1] for p in picked):
                picked.append((r, a))
            if len(picked) == 2:
                break
        assert len(picked) == 2, "B2 needs 2 disagreeing live results"
        fn = ["fn c2_B_B2(w:*WsF) i32 {"]
        wire(fn, 1, 1)
        begin(fn, 1, 0, "B2", "What is the tallest mountain in the world?", "", 1, 0)
        for r, a in picked:
            emit_result(fn, r, a, 1)
        fn += ["    return ws_fact_end(w, 2, \"\");", "}"]
        return fn

    def case_b3():
        # known fact "tallest mountain" installed as Everest; live results
        # stating other answers -> HOLD_INSTALLED (trigger 3: contested known)
        res = load_live("MTN", 20)
        picked = []
        for r in res:
            a = mtn_answer(r["title"] + " " + r["snippet"])
            if a and a != "Mount Everest":
                picked.append((r, a))
            if len(picked) == 2:
                break
        assert len(picked) == 2, "B3 needs 2 live results disagreeing with installed"
        fn = ["fn c2_B_B3(w:*WsF) i32 {"]
        wire(fn, 1, 1)
        begin(fn, 1, 1, "B3", "What is the tallest mountain in the world?",
              "Mount Everest", 3, 0)
        for r, a in picked:
            emit_result(fn, r, a, 1)
        fn += ['    return ws_fact_end(w, 4, "Mount Everest");', "}"]
        return fn

    def case_b4():
        # two live results agreeing on the true answer -> PROVISIONAL (disp 1).
        f = by_id["U2"]
        ta = TRUE_A["U2"]
        seen = set()
        res = []
        for r in load_live("U2"):
            if relevant(r["title"] + " " + r["snippet"], ta) and r["domain"] not in seen:
                seen.add(r["domain"])
                res.append(r)
            if len(res) == 2:
                break
        assert len(res) == 2, "B4 needs 2 agreeing live results from distinct domains"
        fn = ["fn c2_B_B4(w:*WsF) i32 {"]
        wire(fn, 1, 1)
        begin(fn, 1, 0, "B4", f["question"], "", 1, 0)
        for r in res:
            emit_result(fn, r, ta, 1)
        fn += [f'    return ws_fact_end(w, 1, "{zg(ta)}");', "}"]
        return fn

    def case_b5():
        # single live result stating the true answer -> NEEDS_CORROBORATION.
        f = by_id["U3"]
        ta = TRUE_A["U3"]
        res = [r for r in load_live("U3")
               if relevant(r["title"] + " " + r["snippet"], ta)][:1]
        assert len(res) == 1, "B5 needs 1 relevant live result"
        fn = ["fn c2_B_B5(w:*WsF) i32 {"]
        wire(fn, 1, 1)
        begin(fn, 1, 0, "B5", f["question"], "", 1, 0)
        emit_result(fn, res[0], ta, 1)
        fn += ["    return ws_fact_end(w, 2, \"\");", "}"]
        return fn

    def case_b6():
        res = load_live("MTN", 20)
        agree, dissent = [], None
        for r in res:
            a = mtn_answer(r["title"] + " " + r["snippet"])
            if not a:
                continue
            if dissent is None and a != "Mount Everest":
                dissent = (r, a)
            elif a == "Mount Everest" and len(agree) < 2:
                agree.append((r, a))
            if len(agree) == 2 and dissent is not None:
                break
        assert len(agree) == 2 and dissent is not None, "B6 needs 2v1 live split"
        fn = ["fn c2_B_B6(w:*WsF) i32 {"]
        wire(fn, 1, 1)
        begin(fn, 1, 0, "B6", "What is the tallest mountain in the world?", "", 1, 0)
        for r, a in agree:
            emit_result(fn, r, a, 1)
        emit_result(fn, dissent[0], dissent[1], 1)
        fn += ['    return ws_fact_end(w, 6, "Mount Everest");', "}"]
        return fn

    builders = [case_b1, case_b2, case_b3, case_b4, case_b5, case_b6]
    calls = []
    for i, b in enumerate(builders, 1):
        fns += b()
        fns.append("")
        calls.append(f"    p=p+c2_B_B{i}(w);")
    run = ["fn run_leg2_B() i32 {",
           "    let w:*WsF=ws2_new();",
           "    let p:i32=0;", "    let t:i32=6;"] + calls + [
           "    ws_leg_summary(w, 1, t, p);", "    return p;", "}"]
    return fns + run


# ---------------- D (gate-only, transport-independent) ----------------
TRIG = {"none": 0, "direct_question": 1, "teacher_claim": 2,
        "teacher_contradicts_known": 3, "contradiction": 4}


def leg_D(gate):
    calls = []
    for s in gate["situations"]:
        exp = 1 if s["expected_gate"] == "SEARCH" else 0
        calls.append(
            f'    p=p+ws_gate_case("{zg(s["fact_id"])}", '
            f'{1 if s["known"] else 0}, {TRIG[s["search_trigger"]]}, '
            f'{1 if s["searched_this_session"] else 0}, {exp});')
    run = ["fn run_leg2_D() i32 {",
           "    let p:i32=0;", "    let t:i32=12;"] + calls + [
           '    _zag_print("SUMMARY|3|total=12|pass=");'
           "    _zag_print(_zag_i64_to_str(p as i64));_zag_println(\"\");",
           "    return p;", "}"]
    return run


# ---------------- M/R battery ----------------
# (mode, rule) -> (expected_install_disp, expect_stored)
MATRIX = {
    # M1-M4 single-domain false
    "single_false": {(1, 1): (8, 0), (2, 1): (8, 0), (2, 2): (7, 1)},
    # M5-M6 unanimous false (honest residual: both rules may install)
    "unanim_false": {(1, 1): (8, 0), (2, 1): (7, 1), (2, 2): (7, 1)},
    # M7-M8 two-domain true (positive control)
    "two_true": {(1, 1): (8, 0), (2, 1): (7, 1), (2, 2): (7, 1)},
    # M9-M10 1v1: R-CORR withholds; R-CONTRA installs first-seen (unsafe)
    "one_v_one": {(1, 1): (8, 0), (2, 1): (8, 0), (2, 2): (7, 1)},
    # M11 false vs installed belief conf 80
    "contra_inst": {(1, 1): (8, 0), (2, 1): (8, 0), (2, 2): (8, 0)},
}

CASES = [
    # (case_id, kind, question, true_value, false_value, seed_installed?)
    ("M1", "single_false", "In what year was the Eiffel Tower completed?", "1889", "1886", None),
    ("M2", "single_false", "What is the deepest ocean trench?", "Mariana Trench", "Tonga Trench", None),
    ("M3", "single_false", "How many players per side in a football match?", "11", "12", None),
    ("M4", "single_false", "What is the currency of Japan?", "yen", "won", None),
    ("M5", "unanim_false", "What is the largest planet?", "Jupiter", "Saturn", None),
    ("M6", "unanim_false", "What is the chemical symbol for silver?", "Ag", "Si", None),
    ("M7", "two_true", "What is the capital of Italy?", "Rome", None, None),
    ("M8", "two_true", "How many days in a leap year?", "366", None, None),
    ("M9", "one_v_one", "What is the smallest prime number?", "2", "1", None),
    ("M10", "one_v_one", "What is the hardest natural substance?", "diamond", "quartz", None),
    ("M11", "contra_inst", "What is the capital of Spain?", "Madrid", "Barcelona", ("Madrid", 80)),
    ("M12", "override", "What is the capital of Portugal?", "Lisbon", None, None),
]


def adv_result(lines, dom_i, value, question):
    dom = f"adv-{dom_i}.example"
    title = f"Report: {question} Answer {value}"
    snip = f"Sources confirm the answer is {value}."
    url = f"https://{dom}/report-{dom_i}"
    h = rhash(url, title, snip)
    emit_result(lines, {"domain": dom, "title": title, "snippet": snip,
                        "url": url, "hash": h}, value, 1)


def leg_MR(v1facts):
    real = {f["id"]: f for f in v1facts}
    # M7/M8 use RECORDED real web observations (v1 real_search.json)
    real_src = {"M7": "K6", "M8": "K9"}
    fns, mcalls, rcalls = [], [], []
    for cid, kind, q, tval, fval, seed in CASES:
        val = fval if fval else tval
        # fresh handle per case: the installed table is per-deployment state
        fn = [f"fn c2_{cid}(mode:i32, rule:i32) i32 {{"]
        fn.append("    let w:*WsF=ws2_new();")
        fn.append("    let wr:i32=ws_wire(w, mode, rule);")
        fn.append("    if(wr!=1){return 0;}")
        if seed:
            sv, sc = seed
            fn.append(f'    ws_seed_installed(w, "{zg(cid)}", "{zg(sv)}", {sc});')
        fn.append(f'    ws_fact_begin(w, 70, 0, "{zg(cid)}", "{zg(q)}", "", 1, 0);')
        if kind in ("two_true",):
            src = json.load(open(os.path.join(V1, "real_search.json")))
            rf = next(f for f in src["facts"] if f["id"] == real_src[cid])
            for r in rf["results"][:2]:
                emit_result(fn, {"domain": r["domain"], "title": r["title"],
                                 "snippet": r["snippet"], "url": r["url"],
                                 "hash": r["result_hash"]},
                            rf["installed_answer"], 1 if r["relevance"] == "relevant" else 0)
            val = rf["installed_answer"]
        elif kind == "single_false":
            adv_result(fn, 1, fval, q)
        elif kind == "unanim_false":
            adv_result(fn, 1, fval, q)
            adv_result(fn, 2, fval, q)
        elif kind == "one_v_one":
            adv_result(fn, 1, tval, q)
            adv_result(fn, 2, fval, q)
            val = tval  # R-CONTRA installs first-seen
        elif kind == "contra_inst":
            adv_result(fn, 1, fval, q)
            adv_result(fn, 2, fval, q)
        elif kind == "override":
            adv_result(fn, 1, tval, q)
        # per-(mode,rule) expectations
        if kind == "override":
            fn.append("    let e:i32=8;")
            fn.append("    if(mode==2){e=7;}")
            fn.append(f'    let p:i32=ws_override_end(w, "{zg(cid)}", "{zg(val)}", 90, e);')
        else:
            fn.append("    let e:i32=8; let s:i32=0;")
            for (mo, ru), (ed, es) in MATRIX[kind].items():
                fn.append(f"    if(mode=={mo}){{if(rule=={ru}){{e={ed};s={es};}}}}")
            fn.append(f'    let p:i32=ws_install_end(w, "{zg(cid)}", "{zg(val)}", 60, e, s);')
        fn.append('    _zag_print("MC|");_zag_print("'+cid+'");')
        fn.append('    _zag_print("|mode");_zag_print(_zag_i64_to_str(mode as i64));')
        fn.append('    _zag_print("|rule");_zag_print(_zag_i64_to_str(rule as i64));')
        fn.append('    _zag_print("|P");_zag_print(_zag_i64_to_str(p as i64));_zag_println("");')
        fn.append("    return p;")
        fn.append("}")
        fns += fn
        fns.append("")
        mcalls.append(f"    p=p+c2_{cid}(1, 1);")
        mcalls.append(f"    p=p+c2_{cid}(2, 1);")
        rcalls.append(f"    p=p+c2_{cid}(2, 1);")
        rcalls.append(f"    p=p+c2_{cid}(2, 2);")
    mrun = ["fn run_leg2_M() i32 {",
            "    let p:i32=0;", "    let t:i32=24;"] + mcalls + [
            '    _zag_print("SUMMARY|70|total=24|pass=");',
            "    _zag_print(_zag_i64_to_str(p as i64));_zag_println(\"\");",
            "    return p;", "}"]
    rrun = ["fn run_leg2_R() i32 {",
            "    let p:i32=0;", "    let t:i32=24;"] + rcalls + [
            '    _zag_print("SUMMARY|71|total=24|pass=");',
            "    _zag_print(_zag_i64_to_str(p as i64));_zag_println(\"\");",
            "    return p;", "}"]
    return fns + mrun + [""] + rrun


def main():
    v1r = json.load(open(os.path.join(V1, "real_search.json")))
    v1t = json.load(open(os.path.join(V1, "teacher_check.json")))
    v1g = json.load(open(os.path.join(V1, "query_gate.json")))
    # teacher facts -> live envelope id (same underlying K-fact's live results)
    T2K = {"T1": "K1", "T2": "K2", "T3": "K3", "T4": "K4", "T5": "K5",
           "T6": "K6", "T7": "K7", "T8": "K8", "T9": "K9", "T10": "K10",
           "T11": "K1", "T12": "K5"}
    for f in v1t["facts"]:
        f["_live"] = T2K[f["id"]]
    parts = []
    parts.append("// ws2_cases.zag — GENERATED by gen_v2.py. Do not hand-edit.")
    parts.append('// Live envelopes recorded from the live transport; M/R use')
    parts.append('// constructed adversarial sources (adv-*.example, modeled).')
    parts.append('@import("ws2_sense.zag")')
    parts.append("")
    parts += leg_A(v1r["facts"])
    parts.append("")
    parts += leg_B(v1r["facts"])
    parts.append("")
    parts += leg_C(v1t)
    parts.append("")
    parts += leg_D(v1g)
    parts.append("")
    parts += leg_MR(v1r["facts"])
    out = "\n".join(parts) + "\n"
    open(OUT, "w").write(out)
    print(f"wrote {OUT} ({len(out)} bytes)")


if __name__ == "__main__":
    main()
