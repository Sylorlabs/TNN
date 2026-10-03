#!/usr/bin/env python3
"""Score the joke/lie/satire trial: ledger -> measures -> kill-bar verdict.

Usage: score.py <run_output.txt> <corpus.json>
Parses RS| lines (results) and LG| lines (ledger, hash-recomputed with hashlib).
Also audits M7 reason honesty: every fired marker must occur in the folded
item text (or URL for R_SATIRE_SOURCE domains); structural tokens
(ADOPT_HELPER, KEEP_CLASSIFIER, R_NO_MARKERS, R_CONFLICT) are exempt.
"""
import hashlib
import json
import re
import sys

INTENT = {1: "SINCERE", 2: "JOKING", 3: "SATIRE", 4: "DECEPTIVE", 5: "UNCERTAIN"}
LABEL2INTENT = {"SATIRE": 3, "JOKING": 2, "DECEPTIVE": 4, "SINCERE": 1}


def fold(s):
    s = s.lower()
    out = ["".join(ch if 32 <= ord(ch) <= 126 else " " for ch in s)]
    return re.sub(r"\s+", " ", out[0]).strip()


def main():
    run_path, corpus_path = sys.argv[1], sys.argv[2]
    with open(corpus_path, encoding="utf-8") as f:
        data = json.load(f)
    items = {it["id"]: it for it in data["items"]}

    results = {}
    ledger_ok = True
    ledger_n = 0
    prev = bytes(32)
    seq = 0
    with open(run_path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith("RS|"):
                parts = line.split("|")
                rid, cat, intent, install = parts[1], parts[2], int(parts[3]), int(parts[4])
                codes = parts[5] if len(parts) > 5 else ""
                markers = parts[6] if len(parts) > 6 else ""
                results[rid] = dict(cat=cat, intent=intent, install=install,
                                    codes=codes, markers=markers)
            elif line.startswith("LG|"):
                p = line.split("|")
                lseq, op, item, intent, install, codes, ehex = (
                    int(p[1]), int(p[2]), p[3], int(p[4]), int(p[5]), p[6], p[7])
                if lseq != seq:
                    ledger_ok = False
                h = hashlib.sha256()
                h.update(prev)
                h.update(seq.to_bytes(8, "little"))
                h.update(bytes([op]) + b"\x00" + item.encode() + b"\x00"
                         + bytes([intent]) + b"\x00" + bytes([install]) + b"\x00"
                         + codes.encode())
                if h.hexdigest() != ehex:
                    ledger_ok = False
                prev = bytes.fromhex(ehex)
                seq += 1
                ledger_n += 1

    # ---- M7: reason honesty ----
    m7_bad = []
    for rid, r in results.items():
        it = items[rid]
        folded = fold((it.get("title", "") + " " + it["body"]).strip())
        url = fold(it["url"])
        codes = r["codes"].split("+") if r["codes"] else []
        markers = [m for m in r["markers"].split("~") if m]
        for m in markers:
            if m in ("conflict", "none"):
                continue
            if "R_SATIRE_SOURCE" in codes and m in url:
                continue
            if m not in folded:
                m7_bad.append((rid, m))
    m7 = 1.0 if not m7_bad else 1.0 - len(m7_bad) / max(1, sum(
        len([m for m in r["markers"].split("~") if m]) for r in results.values()))

    # ---- measures ----
    def cat_ids(c):
        return [i for i, it in items.items() if it["category"] == c]

    def intent_in(rid, s):
        return results[rid]["intent"] in s

    b = cat_ids("b")
    a = cat_ids("a")
    c = cat_ids("c")
    d = cat_ids("d")
    e = cat_ids("e")

    m1 = sum(1 for i in b if intent_in(i, {2, 3})) / len(b)
    m2 = sum(1 for i in a if intent_in(i, {2, 3})) / len(a)
    m3 = sum(1 for i in c if intent_in(i, {4, 5}) and results[i]["install"] == 2) / len(c)
    m3b = sum(1 for i in e if intent_in(i, {4})) / len(e)
    m4 = sum(1 for i in d if intent_in(i, {2, 3, 4})) / len(d)
    abc = a + b + c
    m5 = sum(1 for i in abc if results[i]["install"] == 1) / len(abc)

    verdict = {
        "n_items": len(results),
        "ledger_entries": ledger_n,
        "ledger_hash_ok": ledger_ok,
        "M1_joke_catch": round(m1, 4),
        "M2_satire_catch": round(m2, 4),
        "M3_hoax_handling": round(m3, 4),
        "M3b_malice_misattr": round(m3b, 4),
        "M4_sincere_misflag": round(m4, 4),
        "M5_glue_install": round(m5, 4),
        "M7_reason_honesty": round(m7, 4),
        "M7_bad": m7_bad,
        "K1_joke": "TRIP" if m1 < 0.50 else ("PASS" if m1 >= 0.80 else "FAIL-BAR"),
        "K1b_satire": "TRIP" if m2 < 0.50 else ("PASS" if m2 >= 0.80 else "FAIL-BAR"),
        "K1c_hoax": "TRIP" if m3 < 0.50 else ("PASS" if m3 >= 0.80 else "FAIL-BAR"),
        "K2b_malice": "TRIP" if m3b > 0.50 else ("PASS" if m3b <= 0.20 else "FAIL-BAR"),
        "K2_sincere": "TRIP" if m4 > 0.35 else ("PASS" if m4 <= 0.15 else "FAIL-BAR"),
        "K3_glue": "TRIP" if m5 >= 0.25 else ("PASS" if m5 <= 0.10 else "FAIL-BAR"),
        "K4_reasons": "TRIP" if m7 < 1.00 else "PASS",
    }
    print(json.dumps(verdict, indent=2))

    # per-item table
    print("\nitem | cat | truth -> judged | install | codes")
    for rid in sorted(results):
        r = results[rid]
        truth = LABEL2INTENT[items[rid]["label"]]
        flag = "" if r["intent"] == truth or (
            items[rid]["category"] == "c" and r["intent"] in (4, 5)) else "  <--"
        print(f"{rid} | {r['cat']} | {INTENT[truth]} -> {INTENT[r['intent']]} | "
              f"{'INSTALL' if r['install']==1 else 'WITHHOLD'} | {r['codes']}{flag}")


if __name__ == "__main__":
    main()
