#!/usr/bin/env python3
"""verify_mw.py — independent oracle for the mixed-web experiment.

Recomputes EVERYTHING from the frozen envelopes with separately written code
(no shared code with gen_mw.py's derive or the Zag binaries):
  - answer extraction + recency (frozen PREREG §2–§3 rules)
  - PREREG §4 deliberation derivation -> expected (verdict, chosen, rule, class)
  - arm-A ws2 decide recomputation (incl. the 6-slot cap, amendment A1)
Then checks the run logs:
  - every B V-line vs oracle (verdict, chosen, rule, chain, ledger completeness)
  - golds: KB-MW-WRONG / KB-MW-GUESS
  - every A line vs oracle recomputation (sanity; tamper must be 0)
  - determinism: 5 logs per arm byte-identical
  - head-to-head: VALUE-CONFIRMED decision rule
"""
import hashlib
import json
import os
import re
import sys

BASE = os.path.expanduser("~/workspace/tnn-lab/mixed-web")
LIVE = os.path.join(BASE, "live")
RUNS = os.path.join(BASE, "runs")

sys.path.insert(0, BASE)
from gen_mw import QUESTIONS, extract, recency_of  # frozen mechanical rules only

YEAR_RE = re.compile(r"\b(19\d{2}|20\d{2})\b")
VALID_RULES = {"MAJORITY", "RECENCY", "CORROB", "TIE", "INSUFFICIENT", "STALE_CONFLICT"}


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


def derive(temporal, results):
    """Independent reimplementation of PREREG §4."""
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
        return ("WITHHOLD", "", "INSUFFICIENT", "W", cands)
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
                return ("CONVERGE", na, "RECENCY", "R", cands)
            if bc >= 2 * nn:
                return ("WITHHOLD", "", "STALE_CONFLICT", "W", cands)
            return ("CONVERGE", na, "RECENCY", "R", cands)
    if bc >= 3 and bc >= 2 * rc:
        return ("CONVERGE", cands[bi][0], "MAJORITY", "C", cands)
    if bc >= 2 and tot <= 4 and rc <= 1:
        return ("CONVERGE", cands[bi][0], "CORROB", "C", cands)
    return ("WITHHOLD", "", "TIE" if rc >= 1 else "INSUFFICIENT", "W", cands)


def arm_a_expected(results):
    """Replicate ws2_sense ws_add_result (dedup (domain,answer), cap 6) + ws_decide."""
    stored = []
    for r in results:
        if any(d == r["domain"] and a == r["answer"] for d, a in stored):
            continue
        if len(stored) < 6:
            stored.append((r["domain"], r["answer"]))
    n = len(stored)
    if n == 0:
        return (2, "")
    counts, order = {}, []
    for d, a in stored:
        if a not in counts:
            counts[a] = 0
            order.append(a)
        counts[a] += 1
    top, topc = order[0], counts[order[0]]
    for a in order[1:]:
        if counts[a] > topc:
            top, topc = a, counts[a]
    distinct = len(order)
    if topc >= 2:
        return (1 if distinct == 1 else 6, top)
    return (2, "")


def head_recompute(qid, question, results, rule, chosen, chain, supp):
    """Independently recompute the mw_sense hash-chained ledger head.

    Mirrors mw_ledger's byte layout from its Zag source (read, not shared):
      entry = prev(32) || seq u64-LE || op || 0x00 || f1 || 0x00 || f2 ||
              0x00 || f3 || 0x00 || f4 ;  prev = sha256(entry)
    Ops: B(66): qid,question,qid,qid
         R(82) x nres (ledger records every fed result, pre-dedup):
             qid,domain,answer,recency-decimal-or-""
         D(68): rule,chosen,chain,supp
         F(70): qid,rule,chosen,qid
    """
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


def parse_logs(arm, n=5):
    logs = []
    for i in range(n):
        p = os.path.join(RUNS, f"mw_{arm}_r{i}.log")
        logs.append(open(p).read())
    return logs


def main():
    golds = json.load(open(os.path.join(BASE, "golds.json")))["kept"]
    fails = []
    oracle = {}
    for qid, question, temporal, cands in QUESTIONS:
        if qid not in golds:
            continue
        res = load_results(qid, cands)
        v, ch, rule, cls, ctab = derive(temporal, res)
        ad, ach = arm_a_expected(res)
        oracle[qid] = {"exp": (v, ch, rule, cls, ctab), "a": (ad, ach),
                       "gold": golds[qid]["gold"], "n": len(res),
                       "res": res, "question": question}
    # determinism
    for arm in ("a", "b"):
        logs = parse_logs(arm)
        if not all(l == logs[0] for l in logs):
            fails.append(f"KB-MW-DET: arm {arm} logs differ across 5 runs")
    # arm A sanity
    a_lines = {}
    for line in parse_logs("a")[0].splitlines():
        if line.startswith("A|") and not line.startswith("A|DONE"):
            p = line.split("|")
            a_lines[p[1]] = (int(p[2]), p[3], p[4])
    for qid, o in oracle.items():
        if qid not in a_lines:
            fails.append(f"arm A: missing line for {qid}")
            continue
        got = (a_lines[qid][0], a_lines[qid][1])
        if got != o["a"]:
            fails.append(f"arm A: {qid} got disp={got} oracle={o['a']}")
        if a_lines[qid][2] != "T0":
            fails.append(f"arm A: {qid} TAMPER flag set (data bug)")
    # arm B checks
    b_lines = {}
    for line in parse_logs("b")[0].splitlines():
        if line.startswith("V|B|"):
            p = line.split("|")
            # V|B|qid|verdict|chosen|rule|<chain with '|' separators>|supp|head
            b_lines[p[2]] = {"verdict": p[3], "chosen": p[4], "rule": p[5],
                             "chain": "|".join(p[6:-2]), "supp": p[-2], "head": p[-1]}
    value_hits = 0
    for qid, o in oracle.items():
        ev, ech, erule, ecls, ectab = o["exp"]
        gold = o["gold"]
        if qid not in b_lines:
            fails.append(f"arm B: missing V-line for {qid}")
            continue
        b = b_lines[qid]
        res = o["res"]
        echain = "|".join(f"{a},{n},{r}" for a, n, r in ectab)
        esupp = supp_expected(res, ech)
        # 0. ledger head: independent hash-chain recomputation (KB-MW-LEDGER)
        hgot = head_recompute(qid, o["question"], res, erule, ech, echain, esupp)
        if hgot != b["head"]:
            fails.append(f"KB-MW-LEDGER: {qid} head {b['head']} != recomputed {hgot}")
        # 0b. supp field exact match
        if b["supp"] != esupp:
            fails.append(f"KB-MW-LEDGER: {qid} supp {b['supp']!r} != oracle {esupp!r}")
        # 1. verdict/chosen/rule vs oracle derivation
        if b["verdict"] != ev or b["chosen"] != ech or b["rule"] != erule:
            fails.append(f"arm B: {qid} got ({b['verdict']},{b['chosen']},{b['rule']}) "
                         f"oracle=({ev},{ech},{erule})")
        # 2. KB-MW-LEDGER: chain completeness
        if b["rule"] not in VALID_RULES:
            fails.append(f"KB-MW-LEDGER: {qid} invalid rule {b['rule']}")
        else:
            chain = {}
            try:
                for item in b["chain"].split("|"):
                    a2, n2, r2 = item.split(",")
                    chain[a2] = (int(n2), int(r2))
            except Exception:
                fails.append(f"KB-MW-LEDGER: {qid} unparsable chain")
                chain = None
            if chain is not None:
                want = {a: (n, r) for a, n, r in ectab}
                if chain != want:
                    fails.append(f"KB-MW-LEDGER: {qid} chain {chain} != oracle {want}")
            if ev == "CONVERGE" and not b["supp"]:
                fails.append(f"KB-MW-LEDGER: {qid} converge without supporting domains")
            if ev == "WITHHOLD" and b["chosen"]:
                fails.append(f"KB-MW-LEDGER: {qid} withhold with non-empty chosen")
        # 3. KB-MW-WRONG / KB-MW-GUESS vs gold
        if gold == "UNDETERMINABLE":
            if b["verdict"] != "WITHHOLD":
                fails.append(f"KB-MW-GUESS: {qid} failed to withhold on undeterminable evidence")
        else:
            if b["verdict"] == "CONVERGE" and b["chosen"] != gold:
                fails.append(f"KB-MW-WRONG: {qid} converged on {b['chosen']} (gold {gold})")
        # 4. head-to-head value
        av, ach = o["a"][0], o["a"][1]
        a_ok = (ev == "CONVERGE" and av in (1, 6) and ach == (gold if gold != "UNDETERMINABLE" else ech)) \
            or (ev == "WITHHOLD" and av == 2)
        b_ok = (b["verdict"] == ev and b["chosen"] == ech and b["rule"] == erule)
        if b_ok and not a_ok:
            value_hits += 1
    print(f"oracle questions: {len(oracle)}")
    print(f"value hits (B right where A wrong): {value_hits}")
    print(f"VALUE-CONFIRMED: {'YES' if value_hits >= 4 else 'NO'} (bar=4)")
    if fails:
        print(f"FAILURES ({len(fails)}):")
        for f in fails:
            print(" -", f)
        sys.exit(1)
    print("ALL BARS HOLD")


if __name__ == "__main__":
    main()
