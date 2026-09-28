#!/usr/bin/env python3
"""gen_mw_round2.py — generate round-2 case files for arms D and E.

Frozen evidence: live/*.json + golds.json (same as round 1) via gen_mw's
frozen mechanical pieces (QUESTIONS, extract, recency_of, load_results,
derive, zc, zg). Synthetic scenarios from PREREG-MW-D section S (fictional
entities, stipulated golds).

Arm D: mw_deliberate_d (PRIMARY_LOOSE, rule PRIMARY_L).
Arm E: mw_deliberate_e (hybrid tiebreak, rule PRIMARY_TB).
Expectations: loose-oracle below; D fires -> (CONVERGE, pa, PRIMARY_L) unless
arm B would converge (no-override guard); E fires the tiebreak only when arm
B withholds. The independent oracle (verify_mw_round2.py) reimplements both
separately.
"""
import json
import os
import re
import sys

BASE = os.path.expanduser("~/workspace/tnn-lab/mixed-web")
sys.path.insert(0, BASE)
from gen_mw import QUESTIONS, derive, load_results, zc, zg  # noqa

R2 = os.path.join(BASE, "authority", "round2")
OUT_D = os.path.join(R2, "src", "mw_cases_d.zag")
OUT_E = os.path.join(R2, "src", "mw_cases_e.zag")


def domain_label(dom):
    d = dom.lower()
    if d.startswith("www."):
        d = d[4:]
    return d.split(".")[0]


def loose_expected(question, results):
    """PREREG-MW-D D1 PRIMARY_LOOSE. Returns (fires, answer, basis) with
    basis in {"loose-corrob","loose-unique"}. The equally-new-contradiction
    veto of PREREG-MW-C M1 is GONE (AMENDMENT-A1)."""
    toks = set(t for t in re.split(r"[^a-z]", question.lower()) if len(t) >= 4)
    doms = []
    for r in results:
        if r["domain"] not in doms:
            doms.append(r["domain"])
    prim = [d for d in doms if domain_label(d) in toks]
    if len(prim) != 1:
        return (False, "", "")
    D = prim[0]
    answered = [r for r in results if r["domain"] == D and r["answer"]]
    if not answered:
        return (False, "", "")
    rp = max(r["recency"] for r in answered)
    A = next(r["answer"] for r in answered if r["recency"] == rp)
    if rp < 2000:
        return (False, "", "")
    gmax = max(r["recency"] for r in results) if results else 0
    if rp != gmax:
        return (False, "", "")
    if any(r["domain"] != D and r["answer"] == A for r in results):
        return (True, A, "loose-corrob")
    return (True, A, "loose-unique")


def synth_results(rows):
    return [{"domain": d, "answer": a, "recency": r} for d, a, r in rows]


# PREREG-MW-D section S: (qid, question, temporal, rows, stipulated gold,
# predicted class)
SYNTH = [
    ("S1A", "Who won the 2026 zorbian grand prix?", 1,
     [("zorbian.com", "Marco Venn", 2026),
      ("zorbian.com", "Marco Venn", 2024),
      ("racefeed.net", "Luis Okafor", 2026),
      ("speedway.org", "Luis Okafor", 2026),
      ("pitwall.io", "Marco Venn", 2025)],
     "Marco Venn", "HELP"),
    ("S1B", "Who won the 2026 zorbian grand prix?", 1,
     [("zorbian.com", "Marco Venn", 2026),
      ("zorbian.com", "Marco Venn", 2024),
      ("racefeed.net", "Luis Okafor", 2026),
      ("speedway.org", "Luis Okafor", 2026),
      ("pitwall.io", "Marco Venn", 2025)],
     "Luis Okafor", "HURT"),
    ("S2", "Who won the 2026 zorbian grand prix?", 1,
     [("zorbian.com", "Marco Venn", 2026),
      ("racefeed.net", "Marco Venn", 2026),
      ("pitwall.io", "Luis Okafor", 2024)],
     "Marco Venn", "NEUTRAL"),
    ("S3", "Who won the 2026 zorbian grand prix?", 1,
     [("zorbian.com", "Marco Venn", 2023),
      ("racefeed.net", "Luis Okafor", 2026),
      ("speedway.org", "Luis Okafor", 2026)],
     "Luis Okafor", "NEUTRAL"),
    ("S4", "Who won the 2026 zorbian grand prix?", 1,
     [("racefeed.net", "Marco Venn", 2026),
      ("pitwall.io", "Luis Okafor", 2026),
      ("speedway.org", "Marco Venn", 2025)],
     "Marco Venn", "NEUTRAL"),
    ("S5", "Who won the 2026 zorbian grand prix?", 1,
     [("zorbian.com", "Marco Venn", 2026),
      ("racefeed.net", "Luis Okafor", 2024),
      ("pitwall.io", "Marco Venn", 2022)],
     "Marco Venn", "NEUTRAL"),
    ("S6", "Who won the 2026 zorbian grand prix?", 1,
     [("zorbian.com", "Luis Okafor", 2026),
      ("zorbian.com", "Marco Venn", 2024),
      ("racefeed.net", "Luis Okafor", 2026)],
     "Luis Okafor", "NEUTRAL"),
    ("S7", "Who won the 2026 zorbian grand prix?", 1,
     [("zorbian.com", "Marco Venn", 2026),
      ("zorbian.net", "Luis Okafor", 2026),
      ("racefeed.net", "Marco Venn", 2025)],
     "Marco Venn", "NEUTRAL"),
    ("S8", "Who won the 2026 zorbian grand prix?", 1,
     [("zorbian.com", "Marco Venn", 2026),
      ("racefeed.net", "Luis Okafor", 2026),
      ("speedway.org", "Marco Venn", 2026),
      ("pitwall.io", "Luis Okafor", 2026)],
     "UNDETERMINABLE", "HURT"),
]


def emit_feed(lines, tag, qid, question, temporal, results):
    lines.append(f"fn feed{tag}_{qid}(w:*MwF) void {{")
    lines.append(f'    mw_fact_begin(w, "{qid}", "{zg(question)}", {temporal});')
    for r in results:
        lines.append(
            f'    mw_add_result(w, "{zg(r["domain"])}", "{zg(r["answer"])}", {r["recency"]});')
    lines.append("    return;")
    lines.append("}")


def emit_q(lines, tag, arm, qid, exp_verdict, exp_chosen, exp_rule,
           deliberate, cite_rule):
    lines.append(f"fn q{tag}_{qid}() i32 {{")
    lines.append("    let w:*MwF=mw_new();")
    lines.append(f"    feed{tag}_{qid}(w);")
    lines.append(f"    let v:i32={deliberate}(w);")
    lines.append("    mw_fact_end(w);")
    lines.append(f'    _zag_print("V|{arm}|");')
    lines.append(f'    _zag_print("{qid}|");')
    lines.append('    if(v==1){_zag_print("CONVERGE|");}else{_zag_print("WITHHOLD|");}')
    lines.append('    _zag_print(w.*.chosen);_zag_print("|");')
    lines.append('    _zag_print(w.*.rule);_zag_print("|");')
    lines.append('    _zag_print(mw_chain(w));_zag_print("|");')
    lines.append(f'    if(mw_equal(w.*.rule,"{cite_rule}")==1){{_zag_print(mw_primary_cite_of(w));}}'
                 'else{_zag_print(mw_supp(w,w.*.chosen));}')
    lines.append('    _zag_print("|");')
    lines.append('    _zag_print(mw_head(w));_zag_println("");')
    lines.append("    let ok:i32=1;")
    if exp_verdict == "CONVERGE":
        lines.append("    if(v!=1){ok=0;}")
        lines.append(f'    if(mw_equal(w.*.chosen, "{zg(exp_chosen)}")!=1){{ok=0;}}')
    else:
        lines.append("    if(v!=2){ok=0;}")
    lines.append(f'    if(mw_equal(w.*.rule, "{exp_rule}")!=1){{ok=0;}}')
    lines.append("    return ok;")
    lines.append("}")


def expected_d(question, results, temporal):
    bv, bch, brule, _cls, _ct = derive(temporal, results)
    pf, pa, _basis = loose_expected(question, results)
    if pf and bv != "CONVERGE":
        return ("CONVERGE", pa, "PRIMARY_L")
    return (bv, bch, brule)


def expected_e(question, results, temporal):
    bv, bch, brule, _cls, _ct = derive(temporal, results)
    pf, pa, _basis = loose_expected(question, results)
    if bv == "WITHHOLD" and pf:
        return ("CONVERGE", pa, "PRIMARY_TB")
    return (bv, bch, brule)


def build(tag, arm, out, deliberate, cite_rule, exp_fn):
    golds = json.load(open(os.path.join(BASE, "golds.json")))
    kept = golds["kept"]
    lines = [f"// mw_cases_{tag.lower()}.zag — GENERATED by gen_mw_round2.py. Do not hand-edit.",
             "// Frozen-set feeds reuse the frozen live envelopes (same rows as",
             "// round 1's feedC_*); synthetic feeds are PREREG-MW-D section S.",
             f'@import("mw_sense_{tag.lower()}.zag")', ""]
    manifest = []
    qids = []
    fires = []
    # frozen set
    for qid, question, temporal, cands in QUESTIONS:
        if qid not in kept:
            continue
        results, _disc = load_results(qid, cands)
        verdict, chosen, rule = exp_fn(question, results, temporal)
        pf, _pa, _basis = loose_expected(question, results)
        if pf:
            fires.append(qid)
        emit_feed(lines, tag, qid, question, temporal, results)
        emit_q(lines, tag, arm, qid, verdict, chosen, rule, deliberate, cite_rule)
        qids.append(qid)
        manifest.append(f"{qid}: expected={verdict} chosen={chosen or '-'} "
                        f"rule={rule} loose_fires={pf}")
    # synthetic scenarios
    for qid, question, temporal, rows, gold, pclass in SYNTH:
        results = synth_results(rows)
        verdict, chosen, rule = exp_fn(question, results, temporal)
        emit_feed(lines, tag, qid, question, temporal, results)
        emit_q(lines, tag, arm, qid, verdict, chosen, rule, deliberate, cite_rule)
        qids.append(qid)
        manifest.append(f"{qid}: expected={verdict} chosen={chosen or '-'} "
                        f"rule={rule} stip_gold={gold} predicted={pclass}")
    lines.append(f"fn run_{arm.lower()}_all() i32 {{")
    lines.append("    let p:i32=1;")
    for qid in qids:
        lines.append(f"    if(q{tag}_{qid}()!=1){{p=0;}}")
    lines.append("    return p;")
    lines.append("}")
    open(out, "w").write("\n".join(lines) + "\n")
    return manifest, fires, len(qids)


def main():
    m_d, fires_d, n_d = build("D", "D", OUT_D, "mw_deliberate_d", "PRIMARY_L",
                              expected_d)
    m_e, fires_e, n_e = build("E", "E", OUT_E, "mw_deliberate_e", "PRIMARY_TB",
                              expected_e)
    print(f"wrote {OUT_D}: {n_d} questions")
    print(f"wrote {OUT_E}: {n_e} questions")
    print(f"D: PRIMARY_LOOSE fires on frozen: {fires_d if fires_d else 'NONE'}")
    print(f"E: tiebreak fires on frozen: {fires_e if fires_e else 'NONE'}")
    print("--- D manifest ---")
    print("\n".join(m_d))
    print("--- E manifest ---")
    print("\n".join(m_e))


if __name__ == "__main__":
    main()
