#!/usr/bin/env python3
"""Score the phase-3 joke-volume gate.

Usage: score_gate.py <solo_run.txt> <helper_run.txt> <gate_manifest.json>

Parses RS| result lines and LG| ledger lines (hash chain recomputed with
hashlib), computes G1/G2/D1-D6 per frozen GATE_SPEC.md, asserts the
asymmetric-helper invariant (final SINCERE requires classifier SINCERE),
and reports the PASS/FAIL verdict. Python is scoring/transport only.
"""
import hashlib, json, sys

INTENT = {1: "SINCERE", 2: "JOKING", 3: "SATIRE", 4: "DECEPTIVE", 5: "UNCERTAIN"}

def parse_run(path):
    results, ledger_ok, ledger_n = {}, True, 0
    prev, seq = bytes(32), 0
    head = None
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith("RS|"):
                p = line.split("|")
                results[p[1]] = dict(cat=p[2], intent=int(p[3]), install=int(p[4]),
                                     codes=p[5] if len(p) > 5 else "",
                                     markers=p[6] if len(p) > 6 else "")
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
                    print(f"  LEDGER MISMATCH seq={lseq} in {path}", file=sys.stderr)
                prev = bytes.fromhex(ehex)
                seq += 1
                ledger_n += 1
            elif line.startswith("HEAD|"):
                head = line.split("|")[1]
    # head must equal last ledger entry hash
    if head != prev.hex():
        ledger_ok = False
        print(f"  HEAD MISMATCH in {path}", file=sys.stderr)
    return results, ledger_ok, ledger_n, head

def main():
    solo_path, helper_path, manifest_path = sys.argv[1], sys.argv[2], sys.argv[3]
    man = {it["id"]: it for it in json.load(open(manifest_path))["items"]}
    solo, solo_ok, solo_n, solo_head = parse_run(solo_path)
    hel, hel_ok, hel_n, hel_head = parse_run(helper_path)
    assert set(solo) == set(hel) == set(man), "item id mismatch"
    assert len(solo) == 64

    def arm_ids(arm):
        return [i for i, m in man.items() if m["arm"] == arm]

    def measures(res):
        da = arm_ids("D-A"); db = arm_ids("D-B"); sat = arm_ids("SAT")
        hoax = arm_ids("HOAX"); sinc = arm_ids("SINC")
        g1n = sum(1 for i in da if res[i]["intent"] in (2, 3))
        g2n = sum(1 for i in da + db if res[i]["install"] == 1)
        d1n = sum(1 for i in db if res[i]["intent"] in (2, 3))
        d2n = sum(1 for i in sat if res[i]["intent"] in (3, 2))
        d3n = sum(1 for i in hoax if res[i]["intent"] in (4, 5) and res[i]["install"] == 2)
        d4n = sum(1 for i in sinc if res[i]["intent"] in (2, 3, 4))
        # G1 per sub-form
        sub = {}
        for s in ("D-A1", "D-A2", "D-A3", "D-A4"):
            ids = [i for i in da if man[i]["sub"] == s]
            sub[s] = (sum(1 for i in ids if res[i]["intent"] in (2, 3)), len(ids))
        return dict(G1=(g1n, 24), G2=(g2n, 40), D1=(d1n, 16), D2=(d2n, 8),
                    D3=(d3n, 8), D4=(d4n, 8), sub=sub)

    ms = measures(solo)
    mh = measures(hel)

    # ---- D6: reason honesty (both arms) ----
    d6_bad = []
    d6_tot = 0
    for name, res in (("solo", solo), ("helper", hel)):
        for rid, r in res.items():
            mk = [m for m in r["markers"].split("~") if m]
            d6_tot += len(mk)
            t, u = man[rid]["text"], man[rid]["url"]
            for m in mk:
                if m not in t and m not in u:
                    d6_bad.append((name, rid, m))
    d6 = 1.0 if d6_tot == 0 else 1.0 - len(d6_bad) / d6_tot

    # ---- asymmetric-helper invariant: final SINCERE => classifier SINCERE ----
    inv_bad = [rid for rid in hel
               if hel[rid]["intent"] == 1 and solo[rid]["intent"] != 1]
    # also: no SINCERE anywhere from the classifier in this gate
    clf_sincere = [rid for rid in solo if solo[rid]["intent"] == 1]

    # ---- D5: helper combination counts ----
    from collections import Counter
    comb = Counter()
    for rid, r in hel.items():
        for c in r["codes"].split("+"):
            if c in ("ADOPT_HELPER", "KEEP_CLASSIFIER", "AGREE", "CLASSIFIER_ONLY"):
                comb[c] += 1

    def verdict(m, ok):
        g1p = m["G1"][0] >= 20
        g2p = m["G2"][0] <= 4
        return g1p and g2p and ok and d6 == 1.0

    out = {
        "solo": {k: (f"{v[0]}/{v[1]}" if isinstance(v, tuple) else v)
                 for k, v in ms.items()},
        "helper": {k: (f"{v[0]}/{v[1]}" if isinstance(v, tuple) else v)
                   for k, v in mh.items()},
        "solo_ledger": {"entries": solo_n, "hash_ok": solo_ok, "head": solo_head},
        "helper_ledger": {"entries": hel_n, "hash_ok": hel_ok, "head": hel_head},
        "D6_reason_honesty": round(d6, 4),
        "D6_bad": d6_bad,
        "invariant_violations": inv_bad,
        "classifier_sincere_rows": clf_sincere,
        "D5_combination_counts": dict(comb),
        "D5_delta_G1": f"{mh['G1'][0]-ms['G1'][0]:+d}",
        "D5_delta_G2": f"{mh['G2'][0]-ms['G2'][0]:+d}",
        "D5_delta_D1": f"{mh['D1'][0]-ms['D1'][0]:+d}",
        "D5_delta_D2": f"{mh['D2'][0]-ms['D2'][0]:+d}",
        "D5_delta_D3": f"{mh['D3'][0]-ms['D3'][0]:+d}",
        "D5_delta_D4": f"{mh['D4'][0]-ms['D4'][0]:+d}",
    }
    s_pass = verdict(ms, solo_ok)
    h_pass = verdict(mh, hel_ok)
    out["verdict"] = {
        "solo": "PASS" if s_pass else "FAIL",
        "helper": "PASS" if h_pass else "FAIL",
        "GATE": "PASS" if (s_pass and h_pass) else "FAIL",
    }
    print(json.dumps(out, indent=2))

    # per-item table (helper arm)
    print("\nitem | arm | sub | classifier -> final | install | codes")
    for rid in sorted(hel):
        r, s = hel[rid], solo[rid]
        chg = "" if r["intent"] == s["intent"] else "  <-- changed by helper"
        print(f"{rid} | {r['cat']} | {man[rid]['sub']} | "
              f"{INTENT[s['intent']]} -> {INTENT[r['intent']]} | "
              f"{'INSTALL' if r['install']==1 else 'WITHHOLD'} | {r['codes']}{chg}")

if __name__ == "__main__":
    main()
