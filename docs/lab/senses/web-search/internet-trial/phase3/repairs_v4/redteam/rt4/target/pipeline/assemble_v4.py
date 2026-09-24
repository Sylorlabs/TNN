#!/usr/bin/env python3
"""hell-hole V4 pipeline: assemble the trial driver's input TSVs.

HARNESS ONLY (no verdict logic). Everything here is file assembly from
frozen evidence + native-classifier outputs:
  - r12 tags: read from r12_v4_72.tsv / r12_v4_helper.tsv (native r12_v4)
  - tiers:   frozen phase-2 tier_map.tsv + v3_tier_additions.tsv (V3 additions
             win on conflict); unknown domain -> tier 1 (compose.zag default,
             a human design choice, documented in the report)
  - weight:  tier->weight map {3:32,2:16,1:8,0:4,-1:1} (frozen r5.zag rule)
  - gated:   derived MECHANICALLY from the frozen course claim_type field
             (CONTESTED/AMBIGUOUS/EVOLVED/SKEPTICISM -> 1); no hand column
  - logic:   derived from the native logic_bin run (r6_v4_out.txt):
             DENY(2) -> logic=2; any other tag -> ABORT (bar fails loudly)
  - is_joke: claim_type == "JOKE-FAMILY" (frozen course metadata)
  - joke intents: from joke_v4 stdout (native g_intent6_v4); helper intents
             and markers: frozen helper_jokes.tsv (unchanged from v3)
Outputs: candidates_v4.tsv, votes_solo.tsv, votes_helper.tsv,
         jokes_solo.tsv, jokes_helper.tsv
"""
import json, sys

H = "/home/hatch/workspace/scratch-hellhole/hellhole/"
LAB = "/home/hatch/workspace/tnn-lab/senses/web-search/internet-trial/phase3/"
W = "/home/hatch/workspace/scratch-hellhole/crews/pipeline/work/"
# run outdir: all pipeline-generated files live here (default = W)
OUT = (sys.argv[1] if len(sys.argv) > 1 else W).rstrip("/") + "/"

course = json.load(open(H + "v3_course.json", encoding="utf-8"))
items = {it["id"]: it for it in course["items"]}

# --- tiers ---
tier = {}
for ln in open(LAB + "repairs/evidence/tier_map.tsv", encoding="utf-8"):
    p = ln.rstrip("\n").split("\t")
    if len(p) == 2:
        tier[p[0].lower()] = int(p[1])
n_conflict = 0
for ln in open(LAB + "trial_v3/evidence/v3_tier_additions.tsv", encoding="utf-8"):
    p = ln.rstrip("\n").split("\t")
    if p[0] == "domain":
        continue
    d, t = p[0].lower(), int(p[1])
    if d in tier and tier[d] != t:
        n_conflict += 1
        print("TIER-CONFLICT %s base=%d v3=%d -> using v3" % (d, tier[d], t))
    tier[d] = t
WT = {3: 32, 2: 16, 1: 8, 0: 4, -1: 1}
n_default = 0

# --- rowid -> domain (stance col 9 is NEVER read: inert human annotation) ---
rowdom = {}
for ln in open(LAB + "trial_v3/evidence/v3_search_results.tsv", encoding="utf-8"):
    p = ln.rstrip("\n").split("\t")
    if p[0] == "rowid":
        continue
    rowdom[p[0]] = p[4].lower()

# --- rowid -> tag ---
tag = {}
for fn in ("r12_v4_72.tsv", "r12_v4_helper.tsv"):
    for ln in open(W + fn, encoding="utf-8"):
        q = ln.rstrip("\n").split(" ")
        tag[q[0]] = int(q[1])

def weight_of(rowid):
    global n_default
    d = rowdom.get(rowid, "")
    if d in tier:
        t = tier[d]
    else:
        t = 1
        n_default += 1
        print("TIER-DEFAULT %s -> 1" % d)
    return WT[t]

# --- votes ---
solo, helper = [], []
for rowid in sorted(rowdom):
    cid = rowid.split("-q")[0]
    w = weight_of(rowid)
    solo.append("%s\t%d\t%d" % (cid, tag[rowid], w))
    helper.append("%s\t%d\t%d" % (cid, tag[rowid], w))
for ln in open(LAB + "trial_v3/evidence/helper_obs.tsv", encoding="utf-8"):
    p = ln.rstrip("\n").split("\t")
    cid = p[0]
    helper.append("%s\t%d\t4" % (cid, tag[cid + "-h96"]))  # tier 0 helper rule
assert len(solo) == 72 and len(helper) == 81, (len(solo), len(helper))
open(OUT + "votes_solo.tsv", "w").write("\n".join(solo) + "\n")
open(OUT + "votes_helper.tsv", "w").write("\n".join(helper) + "\n")

# --- R6 logic column from the native engine ---
r6 = {}
for ln in open(OUT + "r6_v4_out.txt", encoding="utf-8"):
    q = ln.split(" ")
    cid = q[0].replace("R6-", "")
    r6[cid] = int(q[1])
for cid, t in r6.items():
    assert t == 2, ("R6 BAR FAIL", cid, t)

# --- candidates ---
GATED = {"CONTESTED", "AMBIGUOUS", "EVOLVED", "SKEPTICISM"}
cands = []
for i in range(1, 25):
    cid = "V3-%02d" % i
    ct = items[cid]["claim_type"]
    gated = 1 if ct in GATED else 0
    logic = 2 if cid in r6 else 0
    isj = 1 if ct == "JOKE-FAMILY" else 0
    cands.append("%s\t%d\t%d\t%d" % (cid, gated, logic, isj))
open(OUT + "candidates_v4.tsv", "w").write("\n".join(cands) + "\n")

# --- jokes ---
cls = {}
for ln in open(OUT + "joke_v4_out.txt", encoding="utf-8"):
    q = ln.rstrip("\n").split("|")
    cls[q[0]] = int(q[1])
assert len(cls) == 4, cls
hj = {}
for ln in open(LAB + "trial_v3/evidence/helper_jokes.tsv", encoding="utf-8"):
    p = ln.rstrip("\n").split("\t")
    hj[p[0]] = (int(p[1]), p[2])  # frozen helper intents/markers, unchanged
js, jh = [], []
for i in range(14, 18):
    cid = "V3-%02d" % i
    text = items[cid]["claim"]
    hi, mk = hj[cid]
    js.append("%s\t%d\t0\t\t%s" % (cid, cls[cid], text))
    jh.append("%s\t%d\t%d\t%s\t%s" % (cid, cls[cid], hi, mk, text))
open(OUT + "jokes_solo.tsv", "w").write("\n".join(js) + "\n")
open(OUT + "jokes_helper.tsv", "w").write("\n".join(jh) + "\n")

print("tier conflicts:", n_conflict, "| tier defaults:", n_default)
print("candidates:", len(cands), "| votes:", len(solo), len(helper))
print("gated:", [c.split("\t")[0] for c in cands if c.split("\t")[1] == "1"])
print("logic2:", [c.split("\t")[0] for c in cands if c.split("\t")[2] == "2"])
print("jokes:", [c.split("\t")[0] for c in cands if c.split("\t")[3] == "1"])
print("cls intents:", cls)
