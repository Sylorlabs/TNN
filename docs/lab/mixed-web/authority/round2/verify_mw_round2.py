#!/usr/bin/env python3
"""verify_mw_round2.py — independent oracle for round 2 (arms D and E).

Recomputes EVERYTHING with separately written code (no shared mechanism
code with gen_mw_round2.py or the Zag binaries):
  - frozen envelopes -> results (frozen PREREG section 2-3 mechanical rules)
  - PREREG section 4 deliberation -> arm-B expected
  - PREREG-MW-D D1 PRIMARY_LOOSE (loose oracle) -> arm-D expected
  - PREREG-MW-D E1 hybrid tiebreak -> arm-E expected
  - ledger head recomputation for all three ledger shapes
    (B verbatim; D single PRIMARY_L entry; E B-withhold entry + PRIMARY_TB entry)
  - synthetic scenarios (PREREG-MW-D section S) from the prereg's stipulated rows
Then checks the run logs in authority/round2/evidence/:
  - KB-MW2-DET: 5 logs byte-identical per arm
  - every D/E V-line vs oracle (verdict, chosen, rule, chain, supp/cite, head)
  - KB-MW2-WRONG / KB-MW2-GUESS vs golds.json (frozen set)
  - KB-MW2-NONREG-D / KB-MW2-NONREG-E
  - KB-MW2-SYNTH: binary matches oracle on all 9 synthetic scenarios
  - VALUE-DELTA-D / VALUE-DELTA-E
  - free-lunch table: scenario | B | D | E | stipulated gold | predicted | observed
"""
import hashlib
import json
import os
import re
import sys

BASE = os.path.expanduser("~/workspace/tnn-lab/mixed-web")
R2 = os.path.join(BASE, "authority", "round2")
EV = os.path.join(R2, "evidence")
LIVE = os.path.join(BASE, "live")

sys.path.insert(0, BASE)
sys.path.insert(0, os.path.join(R2, "gen"))
from gen_mw import QUESTIONS, extract, recency_of  # frozen mechanical rules only
from gen_mw_round2 import SYNTH  # prereg section S data only (not mechanism code)

VALID_RULES = {"MAJORITY", "RECENCY", "CORROB", "TIE", "INSUFFICIENT",
               "STALE_CONFLICT", "PRIMARY_L", "PRIMARY_TB"}


def load_results(qid, cands, maxn=10):
    d = json.load(open(os.path.join(LIVE, qid + ".json")))
    out = []
    for r in d["results"][:maxn]:
        title, url, snip = r.get("title", ""), r.get("url", ""), r.get("snippet", "")
        dom = r.get("domain", "")
        if not (title and url):
            continue
        ans = extract(title + " " + snip, cands)
        if ans:
            out.append({"domain": dom, "answer": ans,
                        "recency": recency_of(title, snip)})
    return out


def derive_b(temporal, results):
    """Independent reimplementation of PREREG section 4 (arm B)."""
    order, data = [], {}
    seen_pairs = set()
    for r in results:
        k = (r["domain"], r["answer"])
        if k in seen_pairs:
            continue
        seen_pairs.add(k)
        a = r["answer"]
        if a not in data:
            data[a] = {"doms": set(), "rec": 0}
            order.append(a)
        data[a]["doms"].add(r["domain"])
        data[a]["rec"] = max(data[a]["rec"], r["recency"])
    cands = [(a, len(data[a]["doms"]), data[a]["rec"]) for a in order]
    if not cands:
        return ("WITHHOLD", "", "INSUFFICIENT", cands)
    bi, bc = 0, cands[0][1]
    rc = 0
    for i in range(1, len(cands)):
        n = cands[i][1]
        if n > bc:
            rc, bc, bi = bc, n, i
        elif i != bi and n > rc:
            rc = n
    tot = len({r["domain"] for r in results})
    if temporal == 1:
        ni, nr, sr = 0, cands[0][2], 0
        for i in range(1, len(cands)):
            r = cands[i][2]
            if r > nr:
                sr, nr, ni = nr, r, i
            elif i != ni and r > sr:
                sr = r
        nn = cands[ni][1]
        if nr >= 2000 and nn >= 2 and nr - sr >= 3:
            na, ba = cands[ni][0], cands[bi][0]
            if na == ba:
                return ("CONVERGE", na, "RECENCY", cands)
            if bc >= 2 * nn:
                return ("WITHHOLD", "", "STALE_CONFLICT", cands)
            return ("CONVERGE", na, "RECENCY", cands)
    if bc >= 3 and bc >= 2 * rc:
        return ("CONVERGE", cands[bi][0], "MAJORITY", cands)
    if bc >= 2 and tot <= 4 and rc <= 1:
        return ("CONVERGE", cands[bi][0], "CORROB", cands)
    return ("WITHHOLD", "", "TIE" if rc >= 1 else "INSUFFICIENT", cands)


def loose_oracle(question, results):
    """Independent implementation of PREREG-MW-D D1 PRIMARY_LOOSE.

    Same detection as the frozen M1 rule; condition 4 has NO veto.
    Returns (fires, answer, basis) with basis in {"loose-corrob","loose-unique"}.
    """
    qtokens = {t for t in re.split("[^a-z]", question.lower()) if len(t) >= 4}

    def lab(dom):
        d = dom.lower()
        if d[:4] == "www.":
            d = d[4:]
        return d.split(".")[0]

    seen_d, primaries = set(), []
    for r in results:
        d = r["domain"]
        if d in seen_d:
            continue
        seen_d.add(d)
        if lab(d) in qtokens:
            primaries.append(d)
    if len(primaries) != 1:
        return (False, "", "")
    D = primaries[0]
    own = [r for r in results if r["domain"] == D and r["answer"] != ""]
    if not own:
        return (False, "", "")
    newest_rec = max(r["recency"] for r in own)
    newest_ans = [r["answer"] for r in own if r["recency"] == newest_rec][0]
    if newest_rec < 2000:
        return (False, "", "")
    top_rec = max([r["recency"] for r in results] + [0])
    if newest_rec != top_rec:
        return (False, "", "")
    others = [r for r in results if r["domain"] != D]
    if any(r["answer"] == newest_ans for r in others):
        return (True, newest_ans, "loose-corrob")
    return (True, newest_ans, "loose-unique")


def cite_oracle(results, dom, ans, rec, basis):
    """The PRIMARY_L/PRIMARY_TB citation string, mirroring mw_primary_cite.

    Mirrors the binary's feed-time dedup: mw_add_result drops a result whose
    (domain, answer) pair was already fed (first wins), so the citation only
    ever sees the first occurrence.
    """
    deduped, seen_pairs = [], set()
    for r in results:
        k = (r["domain"], r["answer"])
        if k in seen_pairs:
            continue
        seen_pairs.add(k)
        deduped.append(r)
    parts = []
    skipped = False
    for r in deduped:
        if r["domain"] != dom or r["answer"] == "":
            continue
        if not skipped and r["recency"] == rec:
            skipped = True  # the newest assertion itself
            continue
        parts.append(f"{r['answer']}@{r['recency']}")
    sup = ",".join(parts) if parts else "-"
    return f"primary={dom} newest={ans}@{rec} superseded={sup} cond4={basis}"


def primary_dom_of(question, results):
    """Which single primary domain the loose rule sees ("" if not exactly one)."""
    qtokens = {t for t in re.split("[^a-z]", question.lower()) if len(t) >= 4}

    def lab(dom):
        d = dom.lower()
        if d[:4] == "www.":
            d = d[4:]
        return d.split(".")[0]

    seen, prims = set(), []
    for r in results:
        d = r["domain"]
        if d in seen:
            continue
        seen.add(d)
        if lab(d) in qtokens:
            prims.append(d)
    return prims[0] if len(prims) == 1 else ""


def head_recompute(qid, question, results, entries):
    """Recompute the hash-chained ledger head.

    entries: list of (op, f1, f2, f3, f4) AFTER the B/R entries, i.e. the
    D-entries and the final F-entry. B/R/F framing is derived here.
    """
    prev = b"\x00" * 32
    seq = 0
    ops = [(66, qid, question, qid, qid)]
    for r in results:
        ops.append((82, qid, r["domain"], r["answer"],
                    str(r["recency"]) if r["recency"] > 0 else ""))
    ops.extend(entries)
    for op, f1, f2, f3, f4 in ops:
        e = (prev + seq.to_bytes(8, "little") + bytes([op, 0]) +
             f1.encode() + b"\x00" + f2.encode() + b"\x00" +
             f3.encode() + b"\x00" + f4.encode())
        prev = hashlib.sha256(e).digest()
        seq += 1
    return prev.hex()


def supp_expected(results, chosen):
    if not chosen:
        return ""
    seen, out = set(), []
    for r in results:
        if r["answer"] == chosen and r["domain"] not in seen:
            seen.add(r["domain"])
            out.append(r["domain"])
            if len(out) == 3:
                break
    return ",".join(out)


def matches_gold(verdict, chosen, gold):
    if gold == "UNDETERMINABLE":
        return verdict == "WITHHOLD"
    return verdict == "CONVERGE" and chosen == gold


def main():
    golds = json.load(open(os.path.join(BASE, "golds.json")))["kept"]
    fails = []
    oracle = {}
    # frozen set
    for qid, question, temporal, cands in QUESTIONS:
        if qid not in golds:
            continue
        res = load_results(qid, cands)
        bv, bch, brule, ctab = derive_b(temporal, res)
        pf, pa, basis = loose_oracle(question, res)
        if pf and bv == "CONVERGE":
            dexp = (bv, bch, brule)          # no-override guard
        elif pf:
            dexp = ("CONVERGE", pa, "PRIMARY_L")
        else:
            dexp = (bv, bch, brule)
        if bv == "WITHHOLD" and pf:
            eexp = ("CONVERGE", pa, "PRIMARY_TB")
        else:
            eexp = (bv, bch, brule)
        oracle[qid] = {"frozen": True, "b": (bv, bch, brule),
                       "dexp": dexp, "eexp": eexp, "pf": pf, "pa": pa,
                       "basis": basis, "gold": golds[qid]["gold"],
                       "res": res, "question": question, "ctab": ctab,
                       "pred": None}
    # synthetic scenarios
    for qid, question, temporal, rows, gold, pclass in SYNTH:
        res = [{"domain": d, "answer": a, "recency": r} for d, a, r in rows]
        bv, bch, brule, ctab = derive_b(temporal, res)
        pf, pa, basis = loose_oracle(question, res)
        if pf and bv == "CONVERGE":
            dexp = (bv, bch, brule)
        elif pf:
            dexp = ("CONVERGE", pa, "PRIMARY_L")
        else:
            dexp = (bv, bch, brule)
        if bv == "WITHHOLD" and pf:
            eexp = ("CONVERGE", pa, "PRIMARY_TB")
        else:
            eexp = (bv, bch, brule)
        oracle[qid] = {"frozen": False, "b": (bv, bch, brule),
                       "dexp": dexp, "eexp": eexp, "pf": pf, "pa": pa,
                       "basis": basis, "gold": gold,
                       "res": res, "question": question, "ctab": ctab,
                       "pred": pclass}

    arm_logs = {}
    for arm in ("D", "E"):
        logs = []
        for i in range(5):
            logs.append(open(os.path.join(EV, f"mw_{arm.lower()}_r{i}.log")).read())
        if not all(l == logs[0] for l in logs):
            fails.append(f"KB-MW2-DET: arm {arm} logs differ across 5 runs")
        if f"{arm}|ALL_CHECKS_PASS" not in logs[0]:
            fails.append(f"arm {arm}: trial self-checks did not all pass")
        vlines = {}
        for line in logs[0].splitlines():
            if line.startswith(f"V|{arm}|"):
                p = line.split("|")
                vlines[p[2]] = {"verdict": p[3], "chosen": p[4], "rule": p[5],
                                "chain": "|".join(p[6:-2]), "supp": p[-2],
                                "head": p[-1]}
        arm_logs[arm] = vlines

    vd_d = vd_e = 0
    d_fire, e_fire = [], []
    e_eq_d = True
    lunch_rows = []
    for qid, o in oracle.items():
        bv, bch, brule = o["b"]
        res, ctab = o["res"], o["ctab"]
        echain = "|".join(f"{a},{n},{r}" for a, n, r in ctab)
        for arm, expkey, firekey, rulecode in (("D", "dexp", None, "PRIMARY_L"),
                                               ("E", "eexp", None, "PRIMARY_TB")):
            ev, ech, erule = o[expkey]
            vlines = arm_logs[arm]
            if qid not in vlines:
                fails.append(f"arm {arm}: missing V-line for {qid}")
                continue
            c = vlines[qid]
            # expected supp/citation and ledger entries
            if erule == "PRIMARY_L":
                D = primary_dom_of(o["question"], res)
                rp = max(r["recency"] for r in res
                         if r["domain"] == D and r["answer"])
                esupp = cite_oracle(res, D, ech, rp, o["basis"])
                entries = [(68, "PRIMARY_L", ech, echain, esupp),
                           (70, qid, "PRIMARY_L", ech, qid)]
                if o["frozen"]:
                    d_fire.append(qid)
            elif erule == "PRIMARY_TB":
                D = primary_dom_of(o["question"], res)
                rp = max(r["recency"] for r in res
                         if r["domain"] == D and r["answer"])
                esupp = cite_oracle(res, D, ech, rp, o["basis"])
                bsupp = supp_expected(res, bch)
                entries = [(68, brule, bch, echain, bsupp),
                           (68, "PRIMARY_TB", ech, echain, esupp),
                           (70, qid, "PRIMARY_TB", ech, qid)]
                if o["frozen"]:
                    e_fire.append(qid)
            else:
                esupp = supp_expected(res, ech)
                entries = [(68, erule, ech, echain, esupp),
                           (70, qid, erule, ech, qid)]
            hgot = head_recompute(qid, o["question"], res, entries)
            if hgot != c["head"]:
                fails.append(f"KB-MW2-LEDGER: {arm} {qid} head {c['head']} != recomputed {hgot}")
            if c["supp"] != esupp:
                fails.append(f"KB-MW2-LEDGER: {arm} {qid} supp {c['supp']!r} != oracle {esupp!r}")
            if c["verdict"] != ev or c["chosen"] != ech or c["rule"] != erule:
                fails.append(f"arm {arm}: {qid} got ({c['verdict']},{c['chosen']},{c['rule']}) "
                             f"oracle=({ev},{ech},{erule})")
            if c["rule"] not in VALID_RULES:
                fails.append(f"KB-MW2-LEDGER: {arm} {qid} invalid rule {c['rule']}")
            else:
                chain = {}
                try:
                    for item in c["chain"].split("|"):
                        a2, n2, r2 = item.split(",")
                        chain[a2] = (int(n2), int(r2))
                except Exception:
                    fails.append(f"KB-MW2-LEDGER: {arm} {qid} unparsable chain")
                    chain = None
                if chain is not None:
                    want = {a: (n, r) for a, n, r in ctab}
                    if chain != want:
                        fails.append(f"KB-MW2-LEDGER: {arm} {qid} chain != oracle")
                if ev == "CONVERGE" and not c["supp"]:
                    fails.append(f"KB-MW2-LEDGER: {arm} {qid} converge without supp/citation")
                if ev == "WITHHOLD" and c["chosen"]:
                    fails.append(f"KB-MW2-LEDGER: {arm} {qid} withhold with non-empty chosen")
            # NONREG — "fired" is operational: the authority rule actually
            # decided (rule code on the V-line). Where the loose conditions
            # hold but the no-override guard keeps arm B's verdict (S2/S5/S6),
            # the rule did not fire and D/E must equal B exactly.
            fired = (c["rule"] == rulecode)
            if not fired:
                if (c["verdict"], c["chosen"], c["rule"]) != (bv, bch, brule):
                    fails.append(f"KB-MW2-NONREG-{arm}: {qid} {arm}=({c['verdict']},{c['chosen']},{c['rule']}) "
                                 f"!= B=({bv},{bch},{brule}) authority did not fire")
            else:
                if bv != "WITHHOLD":
                    fails.append(f"KB-MW2-NONREG-{arm}: {qid} authority fired where B "
                                 f"converged ({bch}/{brule}) — override forbidden")
            # frozen-set kill bars + value delta
            if o["frozen"]:
                gold = o["gold"]
                if gold == "UNDETERMINABLE":
                    if c["verdict"] != "WITHHOLD":
                        fails.append(f"KB-MW2-GUESS: {arm} {qid} failed to withhold")
                else:
                    if c["verdict"] == "CONVERGE" and c["chosen"] != gold:
                        fails.append(f"KB-MW2-WRONG: {arm} {qid} converged on {c['chosen']} (gold {gold})")
                if matches_gold(c["verdict"], c["chosen"], gold) and not matches_gold(bv, bch, gold):
                    if arm == "D":
                        vd_d += 1
                    else:
                        vd_e += 1
        # E-vs-D verdict equivalence (headline question 3)
        dv, ev2 = o["dexp"], o["eexp"]
        if (dv[0], dv[1]) != (ev2[0], ev2[1]):
            e_eq_d = False
        # free-lunch row (synthetic only)
        if not o["frozen"]:
            gold = o["gold"]
            dc = arm_logs["D"].get(qid, {})
            dv, dch = dc.get("verdict", ""), dc.get("chosen", "")
            b_ok = matches_gold(bv, bch, gold)
            d_ok = matches_gold(dv, dch, gold)
            d_eq_b = (dv, dch) == (bv, bch)
            d_wrong_converge = (dv == "CONVERGE" and
                                ((gold != "UNDETERMINABLE" and dch != gold) or
                                 gold == "UNDETERMINABLE"))
            if d_ok and not b_ok:
                observed = "HELP"
            elif d_wrong_converge:
                observed = "HURT"
            elif d_eq_b:
                observed = "NEUTRAL"
            else:
                observed = "MIXED?"
            lunch_rows.append((qid, f"{bv}/{brule}", f"{dc.get('verdict')}/{dc.get('rule')}",
                               gold, o["pred"], observed))

    print(f"oracle questions: {len(oracle)} (frozen 17 + synthetic 9)")
    print(f"D PRIMARY_LOOSE fires on frozen: {d_fire if d_fire else 'NONE'}")
    print(f"E tiebreak fires on frozen: {e_fire if e_fire else 'NONE'}")
    print(f"VALUE-DELTA-D: {vd_d}")
    print(f"VALUE-DELTA-E: {vd_e}")
    print(f"E verdicts identical to D on all 26: {e_eq_d}")
    print("--- free-lunch table (synthetic) ---")
    print("scenario | arm B | arm D | stipulated gold | predicted | observed")
    pred_mismatch = []
    for qid, b, d, gold, pred, observed in lunch_rows:
        print(f"{qid} | {b} | {d} | {gold} | {pred} | {observed}")
        if pred != observed:
            pred_mismatch.append(qid)
    if pred_mismatch:
        print(f"PREDICTED-CLASS MISMATCHES: {pred_mismatch}")
    if fails:
        print(f"FAILURES ({len(fails)}):")
        for f in fails:
            print(" -", f)
        sys.exit(1)
    print("ALL BARS HOLD")


if __name__ == "__main__":
    main()
