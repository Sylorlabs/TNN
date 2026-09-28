#!/usr/bin/env python3
"""HTD-1 R3 frozen-artifact validator. Exits 0 iff every check passes.
Deterministic; reads corpora in place (never copies)."""
import hashlib
import json
import os
import sys
from collections import Counter

ART = os.path.expanduser("~/workspace/htd-1/artifacts")
PG = os.path.expanduser("~/workspace/tnn-lab/corpora/pg100.txt")
SQ = os.path.expanduser("~/workspace/tnn-lab/corpora/sqlite3.c")
fails = []

def check(name, cond, detail=""):
    if cond:
        print("ok  %s" % name)
    else:
        print("FAIL %s %s" % (name, detail))
        fails.append(name)

def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

pg = open(PG, "rb").read()
sq = open(SQ, "rb").read()
check("corpus pg100 size+sha",
      len(pg) == 5638480 and sha(pg) == "3cf4b3d44ee14cff4e14e78e2ad3318eff76f3f7f2afc3cee6bb925879110a37")
check("corpus sqlite3.c size+sha",
      len(sq) == 9515341 and sha(sq) == "b1dd5d74ec7f29055a6684fa06fb3c2f6821c87dd38f9a458dfd2e8a1db28189")

# ---- D-P1 -----------------------------------------------------------------
dp1 = [l.split("\t") for l in open(os.path.join(ART, "d_p1_items.tsv"), encoding="utf-8").read().splitlines()]
hdr, dp1 = dp1[0], dp1[1:]
check("dp1 count", len(dp1) == 600, str(len(dp1)))
check("dp1 plays", Counter(r[1] for r in dp1) == {"HAMLET": 150, "LEAR": 150, "MACBETH": 150, "OTHELLO": 150})
ok = True
for r in dp1:
    s, e = int(r[2]), int(r[3])
    if not (0 <= s < e <= len(pg) and 200 <= e - s <= 400 and int(r[4]) == e - s):
        ok = False; break
    if sha(pg[s:e]) != r[5]:
        ok = False; break
check("dp1 bounds+lengths+sha", ok)

# ---- D-P2 -----------------------------------------------------------------
dp2 = [l.split("\t") for l in open(os.path.join(ART, "d_p2_items.tsv"), encoding="utf-8").read().splitlines()]
hdr, dp2 = dp2[0], dp2[1:]
check("dp2 count", len(dp2) == 600, str(len(dp2)))
check("dp2 subsystems", Counter(r[3] for r in dp2) ==
      {"btree": 75, "pager": 75, "os": 75, "vdbe": 75, "parser": 75, "util": 75, "mem": 75, "other": 75})
ok = True
for r in dp2:
    s, e = int(r[4]), int(r[5])
    b = sq[s:e]
    if sha(b) != r[7]:
        ok = False; break
    t = b.decode("utf-8", "replace")
    brace = t.find("{")
    if brace == -1 or ";" in t[:brace].split(")")[-1]:
        ok = False; break  # prototype, not a definition
check("dp2 sha + real definitions (no prototypes)", ok)

# ---- corpus_qa_60 ----------------------------------------------------------
qa = [json.loads(l) for l in open(os.path.join(ART, "corpus_qa_60.jsonl"), encoding="utf-8")]
check("qa count", len(qa) == 60, str(len(qa)))
ok = True
for q in qa:
    data = pg if q["corpus"] == "pg100" else sq
    for a, (s, e) in zip(q["anchors"], q["gt_anchor_byte_offsets"]):
        if not (0 <= s < e <= len(data)) or data[s:e].decode("utf-8", "replace") != a:
            ok = False; break
    for (s, e) in q["gt_chunk_byte_offsets"]:
        if not (0 <= s < e <= len(data)):
            ok = False; break
check("qa anchors+chunks byte-exact", ok)
check("qa balance", Counter((q["corpus"], q["kind"]) for q in qa) ==
      {("pg100", "lookup"): 15, ("pg100", "discovery"): 15,
       ("sqlite3.c", "lookup"): 15, ("sqlite3.c", "discovery"): 15})

# ---- G-CM1 batteries --------------------------------------------------------
prom = [json.loads(l) for l in open(os.path.join(ART, "gcm1_promotion_200.jsonl"), encoding="utf-8")]
check("prom count+split", len(prom) == 200 and Counter(p["class"] for p in prom) ==
      {"false_consistent": 80, "false_contradictory": 60, "true": 60})
check("prom fields", all(p["origin_partition"] == "CONSTRUCTED" and p["target_partition"] == "BELIEF"
      and sha(p["claim_text"].encode("utf-8")) == p["claim_sha256"] for p in prom))
elab = [json.loads(l) for l in open(os.path.join(ART, "gcm1_elaboration_500.jsonl"), encoding="utf-8")]
check("elab 500 unique sessions", len(elab) == 500 and len(set(e["session_id"] for e in elab)) == 500)
rec = [json.loads(l) for l in open(os.path.join(ART, "gcm1_recall_500.jsonl"), encoding="utf-8")]
check("recall 500", len(rec) == 500)
ok = True
for r in rec[:450]:
    data = pg if r["corpus"] == "pg100.txt" else sq
    s, e = r["gt_byte_offsets"][0]
    if data[s:e].decode("utf-8") != r["expected_bytes"] or sha(data[s:e]) != r["expected_sha256"]:
        ok = False; break
check("recall corpus probes byte-exact", ok)
check("recall planted 50", sum(1 for r in rec if r["corpus"] == "planted") == 50)
para = [json.loads(l) for l in open(os.path.join(ART, "gcm1_paraphrases.jsonl"), encoding="utf-8")]
check("paraphrases 120", len(para) == 120 and Counter(p["rule_id"] for p in para) ==
      {"P-SYN": 40, "P-PASS": 40, "P-PRE": 40})
fr = json.load(open(os.path.join(ART, "gcm1_freeze_probes.json"), encoding="utf-8"))
check("freeze probes 2500", fr["n_probes"] == 2500 and len(fr["sessions"]) == 500 and len(fr["offsets"]) == 5)
cc = [json.loads(l) for l in open(os.path.join(ART, "gcm1_cache_contradictions_50.jsonl"), encoding="utf-8")]
check("cache contradictions 50", len(cc) == 50 and all(c["must_be_cache_miss"] for c in cc))
ctx = [json.loads(l) for l in open(os.path.join(ART, "gcm1_context_reset_100.jsonl"), encoding="utf-8")]
check("context reset 100", len(ctx) == 100 and len(set(c["attack_class"] for c in ctx)) == 10)
neg = json.load(open(os.path.join(ART, "gcm1_negative_controls.json"), encoding="utf-8"))
check("negative controls", [c["control_id"] for c in neg["controls"]] == ["KB-CM-NEG1", "KB-CM-DENY1"])

# ---- D-P3 -------------------------------------------------------------------
dp3z = open(os.path.join(ART, "dp3/dp3_gen.zag"), encoding="utf-8").read()
check("dp3 source present", "d3_rand_next" in dp3z and "D3-ITEM" in dp3z)
items, evs = {}, {}
for l in open(os.path.join(ART, "dp3/dp3_items.txt"), encoding="utf-8"):
    l = l.strip()
    if l.startswith("D3-ITEM,"):
        _, i, nh, s = l.split(","); items[int(i)] = (int(nh), int(s))
    elif l.startswith("D3-EV,"):
        _, i, o, e, h, w, d = l.split(",")
        evs.setdefault((int(i), int(o)), []).append((int(e), int(h), int(w), int(d)))
check("dp3 300 items", len(items) == 300)
ok = len(evs) == 900
for (i, o), rows in evs.items():
    nh, s = items[i]
    rows.sort()
    elims = [r[1] for r in rows]
    dec = [r for r in rows if r[3] == 1]
    if sorted(elims) != [h for h in range(nh) if h != s] or len(dec) != 1 or dec[0][1] == s:
        ok = False; break
check("dp3 elim semantics", ok)

# ---- params / taxonomy / relevance ------------------------------------------
esp = json.load(open(os.path.join(ART, "esp_params.json"), encoding="utf-8"))
check("esp tau grid", esp["E-SP"]["tau_grid"] == [0, 1, 2, 3, 4, 5, 6])
check("esp region size", esp["E-SP"]["region_size"] == 8)
check("esp ledger grids", esp["E-LG2"]["K_grid"] == [16, 64, 256] and esp["E-LG3"]["H_grid"] == [64, 128, 256])
ede1 = json.load(open(os.path.join(ART, "ede1_taxonomy.json"), encoding="utf-8"))
check("ede1 classes", set(ede1["classes"].keys()) ==
      {"ATTRIBUTE_PASSAGE", "CLASSIFY_FUNCTION", "ELIMINATE_HYPOTHESES",
       "VERIFY_CLAIM", "REVISE_MEMORY", "PLAN_ELABORATION"})
ede4 = json.load(open(os.path.join(ART, "ede4_relevance.json"), encoding="utf-8"))
ok = True
for c, v in ede4["declarations"].items():
    for rp in v["relevant_partitions"]:
        if not ({"partition_id", "provenance", "address_range", "rationale"} <= set(rp.keys())):
            ok = False
check("ede4 R7 fields", ok)
gco = [json.loads(l) for l in open(os.path.join(ART, "gco2_abstention_200.jsonl"), encoding="utf-8")]
check("gco2 200", len(gco) == 200 and Counter(x["category"] for x in gco) ==
      {"technology": 50, "geography/history": 50, "science": 50, "arts/sport/everyday": 50})

# ---- real traces -------------------------------------------------------------
rt = [json.loads(l) for l in open(os.path.join(ART, "real_traces.jsonl"), encoding="utf-8")]
check("real traces 13033", len(rt) == 13033, str(len(rt)))
check("real traces kinds", Counter(r["kind"] for r in rt) == {"debate_session": 33, "dr_block": 13000})

print()
if fails:
    print("VALIDATOR FAILED:", fails)
    sys.exit(1)
print("ALL CHECKS PASSED")
