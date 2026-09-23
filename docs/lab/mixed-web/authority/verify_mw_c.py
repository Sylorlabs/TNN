#!/usr/bin/env python3
"""verify_mw_c.py — independent oracle for arm C (source-authority weighting).

Recomputes EVERYTHING from the frozen envelopes with separately written code
(no shared code with gen_mw_c.py's primary_expected or the Zag binary):
  - answer extraction + recency (frozen PREREG §2–§3 mechanical rules)
  - PREREG §4 deliberation derivation -> arm-B expected (verdict, chosen, rule)
  - PREREG-MW-C M1 PRIMARY rule (literal reading) -> expected arm-C verdict
  - ledger head recomputation, incl. the PRIMARY citation format
Then checks the run logs in authority/evidence/:
  - KB-MW-DET: 5 logs byte-identical
  - every C V-line vs oracle (verdict, chosen, rule, chain, supp, ledger head)
  - KB-MW-WRONG / KB-MW-GUESS vs golds
  - KB-MW-NONREG: C == B expected everywhere PRIMARY does not fire;
    where PRIMARY fires, B must have withheld (no-override)
  - VALUE-DELTA decision rule
"""
import hashlib
import json
import os
import re
import sys

BASE = os.path.expanduser("~/workspace/tnn-lab/mixed-web")
EV = os.path.join(BASE, "authority", "evidence")
LIVE = os.path.join(BASE, "live")

sys.path.insert(0, BASE)
from gen_mw import QUESTIONS, extract, recency_of  # frozen mechanical rules only

VALID_RULES = {"MAJORITY", "RECENCY", "CORROB", "TIE", "INSUFFICIENT",
               "STALE_CONFLICT", "PRIMARY"}


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
    """Independent reimplementation of PREREG §4 (arm B)."""
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


def primary_oracle(question, results):
    """Independent implementation of PREREG-MW-C M1 (literal reading).

    Returns (fires, answer, basis) with basis in {"corrob","unique"}.
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
        return (True, newest_ans, "corrob")
    # literal M1 condition 4 i.e.: no other domain asserts a DIFFERENT
    # answer at that same max recency
    if any(r["recency"] == top_rec and r["answer"] != newest_ans for r in others):
        return (False, "", "")
    return (True, newest_ans, "unique")


def cite_oracle(results, dom, ans, rec, basis):
    """The PRIMARY citation string, mirroring mw_primary_cite's format."""
    parts = []
    skipped = False
    for r in results:
        if r["domain"] != dom or r["answer"] == "":
            continue
        if not skipped and r["recency"] == rec:
            skipped = True  # the newest assertion itself
            continue
        parts.append(f"{r['answer']}@{r['recency']}")
    sup = ",".join(parts) if parts else "-"
    return f"primary={dom} newest={ans}@{rec} superseded={sup} cond4={basis}"


def head_recompute(qid, question, results, rule, chosen, chain, supp):
    """Independently recompute the hash-chained ledger head (mw_ledger layout)."""
    prev = b"\x00" * 32
    seq = 0
    ops = [(66, qid, question, qid, qid)]
    for r in results:
        ops.append((82, qid, r["domain"], r["answer"],
                    str(r["recency"]) if r["recency"] > 0 else ""))
    ops.append((68, rule, chosen, chain, supp))
    ops.append((70, qid, rule, chosen, qid))
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


def main():
    golds = json.load(open(os.path.join(BASE, "golds.json")))["kept"]
    fails = []
    oracle = {}
    for qid, question, temporal, cands in QUESTIONS:
        if qid not in golds:
            continue
        res = load_results(qid, cands)
        bv, bch, brule, ctab = derive_b(temporal, res)
        pf, pa, basis = primary_oracle(question, res)
        if pf:
            exp = ("CONVERGE", pa, "PRIMARY")
        else:
            exp = (bv, bch, brule)
        oracle[qid] = {"b": (bv, bch, brule), "exp": exp, "pf": pf,
                       "pa": pa, "basis": basis, "gold": golds[qid]["gold"],
                       "res": res, "question": question, "ctab": ctab}
    # KB-MW-DET
    logs = []
    for i in range(5):
        p = os.path.join(EV, f"mw_c_r{i}.log")
        logs.append(open(p).read())
    if not all(l == logs[0] for l in logs):
        fails.append("KB-MW-DET: arm C logs differ across 5 runs")
    # parse V|C| lines
    c_lines = {}
    for line in logs[0].splitlines():
        if line.startswith("V|C|"):
            p = line.split("|")
            c_lines[p[2]] = {"verdict": p[3], "chosen": p[4], "rule": p[5],
                             "chain": "|".join(p[6:-2]), "supp": p[-2],
                             "head": p[-1]}
    if "C|ALL_CHECKS_PASS" not in logs[0]:
        fails.append("arm C: trial self-checks did not all pass")
    value_delta = 0
    primary_fire_qs = []
    for qid, o in oracle.items():
        ev, ech, erule = o["exp"]
        bv, bch, brule = o["b"]
        gold = o["gold"]
        res = o["res"]
        if qid not in c_lines:
            fails.append(f"arm C: missing V-line for {qid}")
            continue
        c = c_lines[qid]
        echain = "|".join(f"{a},{n},{r}" for a, n, r in o["ctab"])
        if erule == "PRIMARY":
            esupp = None  # computed below (needs the primary domain)
        else:
            esupp = supp_expected(res, ech)
        # ledger head (KB-MW-LEDGER)
        if erule == "PRIMARY":
            qtokens = {t for t in re.split("[^a-z]", o["question"].lower()) if len(t) >= 4}

            def lab(dom):
                d = dom.lower()
                return d[4:].split(".")[0] if d[:4] == "www." else d.split(".")[0]
            seen_d, prims = set(), []
            for r in res:
                if r["domain"] not in seen_d:
                    seen_d.add(r["domain"])
                    if lab(r["domain"]) in qtokens:
                        prims.append(r["domain"])
            D = prims[0]
            rp = max(r["recency"] for r in res if r["domain"] == D and r["answer"])
            esupp = cite_oracle(res, D, ech, rp, o["basis"])
            primary_fire_qs.append(qid)
        hgot = head_recompute(qid, o["question"], res, erule, ech, echain, esupp)
        if hgot != c["head"]:
            fails.append(f"KB-MW-LEDGER: {qid} head {c['head']} != recomputed {hgot}")
        if c["supp"] != esupp:
            fails.append(f"KB-MW-LEDGER: {qid} supp {c['supp']!r} != oracle {esupp!r}")
        if c["verdict"] != ev or c["chosen"] != ech or c["rule"] != erule:
            fails.append(f"arm C: {qid} got ({c['verdict']},{c['chosen']},{c['rule']}) "
                         f"oracle=({ev},{ech},{erule})")
        if c["rule"] not in VALID_RULES:
            fails.append(f"KB-MW-LEDGER: {qid} invalid rule {c['rule']}")
        else:
            chain = {}
            try:
                for item in c["chain"].split("|"):
                    a2, n2, r2 = item.split(",")
                    chain[a2] = (int(n2), int(r2))
            except Exception:
                fails.append(f"KB-MW-LEDGER: {qid} unparsable chain")
                chain = None
            if chain is not None:
                want = {a: (n, r) for a, n, r in o["ctab"]}
                if chain != want:
                    fails.append(f"KB-MW-LEDGER: {qid} chain {chain} != oracle {want}")
            if ev == "CONVERGE" and not c["supp"]:
                fails.append(f"KB-MW-LEDGER: {qid} converge without supp/citation")
            if ev == "WITHHOLD" and c["chosen"]:
                fails.append(f"KB-MW-LEDGER: {qid} withhold with non-empty chosen")
        # KB-MW-NONREG
        if not o["pf"]:
            if (c["verdict"], c["chosen"], c["rule"]) != (bv, bch, brule):
                fails.append(f"KB-MW-NONREG: {qid} C=({c['verdict']},{c['chosen']},{c['rule']}) "
                             f"!= B=({bv},{bch},{brule}) with PRIMARY not firing")
        else:
            if bv != "WITHHOLD":
                fails.append(f"KB-MW-NONREG: {qid} PRIMARY fired where B converged "
                             f"({bch}/{brule}) — override forbidden")
        # KB-MW-WRONG / KB-MW-GUESS
        if gold == "UNDETERMINABLE":
            if c["verdict"] != "WITHHOLD":
                fails.append(f"KB-MW-GUESS: {qid} failed to withhold on undeterminable evidence")
        else:
            if c["verdict"] == "CONVERGE" and c["chosen"] != gold:
                fails.append(f"KB-MW-WRONG: {qid} converged on {c['chosen']} (gold {gold})")
        # VALUE-DELTA
        def matches_gold(vd, ch):
            if gold == "UNDETERMINABLE":
                return vd == "WITHHOLD"
            return vd == "CONVERGE" and ch == gold
        c_ok = matches_gold(c["verdict"], c["chosen"])
        b_ok = matches_gold(bv, bch)
        if c_ok and not b_ok:
            value_delta += 1
    print(f"oracle questions: {len(oracle)}")
    print(f"PRIMARY fires on: {primary_fire_qs if primary_fire_qs else 'NONE'}")
    print(f"VALUE-DELTA: {value_delta}")
    if fails:
        print(f"FAILURES ({len(fails)}):")
        for f in fails:
            print(" -", f)
        sys.exit(1)
    print("ALL BARS HOLD")


if __name__ == "__main__":
    main()
