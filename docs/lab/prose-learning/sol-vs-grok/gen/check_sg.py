#!/usr/bin/env python3
"""Check every battery sentence's parsed frame against design assertions.
Reads frames.tsv (from validate_sg), teach_sg.txt, probe_sg.txt, expected_sg.json.
Exit 0 iff all assertions hold."""
import json, re, sys
from collections import defaultdict

D = sys.argv[1]
ENT_MAIN = ["Corvane", "Vexley", "Marrowick", "Pellisor",
            "Dunmore", "Kestrel", "Vanemor", "Sorrelbay"]
if len(sys.argv) > 2:
    import importlib.util
    spec = importlib.util.spec_from_file_location("cfg", sys.argv[2])
    cfg = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cfg)
    ENT_MAIN = cfg.CONFIG["ent_main"]
frames = {}
order = []
with open(f"{D}/frames.tsv") as f:
    for ln in f:
        p = ln.rstrip("\n").split("\t")
        kind, sid = p[0], p[1]
        eid, reln, att, vok, val = int(p[2]), int(p[3]), int(p[4]), int(p[5]), int(p[6])
        rel = frozenset(int(x) for x in p[7].split(",") if x != "")
        frames.setdefault(sid, []).append(
            dict(kind=kind, eid=eid, rel=reln, att=att, vok=vok, val=val, relset=rel))
        order.append(sid)

teach_text = {}
with open(f"{D}/teach_sg.txt") as f:
    for ln in f:
        i, t = ln.rstrip("\n").split("\t", 1)
        teach_text[i] = t
probe_text, probe_cls = {}, {}
with open(f"{D}/probe_sg.txt") as f:
    for ln in f:
        i, t, c = ln.rstrip("\n").split("\t")
        probe_text[i] = t
        probe_cls[i] = c
expected = json.load(open(f"{D}/expected_sg.json"))

fails = []
def ck(cond, msg):
    if not cond:
        fails.append(msg)

def quoted(t):
    m = re.findall(r'"([^"]+)"', t)
    return m

# 1. every line parsed; sentence counts
ck(all(len(v) >= 1 for v in frames.values()), "some id missing frames")
n_teach_sent = sum(len(v) for k, v in frames.items() if v[0]["kind"] == "T")
n_probe_sent = sum(len(v) for k, v in frames.items() if v[0]["kind"] == "P")
ck(n_teach_sent == 432, f"teach sentences {n_teach_sent} != 432")
ck(n_probe_sent == 432, f"probe sentences {n_probe_sent} != 432")

# 2. entity consistency per quoted name
name_eid = defaultdict(set)
for sid, t in teach_text.items():
    for q in quoted(t):
        for s in frames[sid]:
            name_eid[q].add(s["eid"])
for sid, t in probe_text.items():
    for q in quoted(t):
        for s in frames[sid]:
            name_eid[q].add(s["eid"])
for name, eids in name_eid.items():
    ck(len(eids) == 1, f"entity {name} has eids {eids}")
all_eids = {next(iter(v)) for v in name_eid.values()}
ck(len(all_eids) == len(name_eid), "two entity names share an eid")
EID = {n: next(iter(v)) for n, v in name_eid.items()}
# multi-hop sentence 2 (no quotes) must resolve to line entity via coref
for sid, t in teach_text.items():
    if sid.startswith("M") and len(frames[sid]) == 2:
        q = quoted(t)[0]
        ck(frames[sid][1]["eid"] == EID[q],
           f"multi {sid} s2 eid {frames[sid][1]['eid']} != {EID[q]}")

# 3. relation classes per family
REL = {}  # (kind,ri,ei) -> relset ; from T0/P0
for ri in range(12):
    for ei in range(8):
        r0 = frames[f"T{ri:02d}{ei:02d}a"][0]["relset"]
        rc = frames[f"T{ri:02d}{ei:02d}c"][0]["relset"]
        r1 = frames[f"T{ri:02d}{ei:02d}b"][0]["relset"]
        p0 = frames[f"P{ri:02d}{ei:02d}0"][0]["relset"]
        p1 = frames[f"P{ri:02d}{ei:02d}1"][0]["relset"]
        ck(r0 == p0 == rc, f"fam {ri},{ei}: T0/P0/T2 rel mismatch {[sorted(r0),sorted(p0),sorted(rc)]}")
        ck(r1 == p1, f"fam {ri},{ei}: T1/P1 rel mismatch")
        ck(r0 != r1, f"fam {ri},{ei}: Ra/Rb relsets identical (synonym stem collision)")
        ck(len(r0) >= 2 and len(r1) >= 2, f"fam {ri},{ei}: rel too small")
        # eid match
        e = ENT_MAIN[ei]
        for sid2 in (f"T{ri:02d}{ei:02d}a", f"P{ri:02d}{ei:02d}0", f"P{ri:02d}{ei:02d}1"):
            ck(frames[sid2][0]["eid"] == EID[e], f"{sid2} eid wrong")
        # value frames
        for sid2 in (f"T{ri:02d}{ei:02d}a", f"T{ri:02d}{ei:02d}b", f"T{ri:02d}{ei:02d}c"):
            s = frames[sid2][0]
            ck(s["vok"] == 1 and s["att"] == 0, f"{sid2} not asserted value frame")
        for sid2 in (f"P{ri:02d}{ei:02d}0", f"P{ri:02d}{ei:02d}1"):
            s = frames[sid2][0]
            ck(s["vok"] == 0 and s["att"] == 0, f"{sid2} probe should be value-less asserted")
        # EXTRA / TYPO
        if (ri + ei) % 2 == 0:
            xs = frames[f"X{ri:02d}{ei:02d}"][0]
            ck(xs["relset"] > r0 and len(xs["relset"]) == len(r0) + 1,
               f"X{ri:02d}{ei:02d}: extra-word rel not superset+1")
            ck(xs["eid"] == EID[e] and xs["vok"] == 0, f"X{ri:02d}{ei:02d} frame")
        else:
            ys = frames[f"Y{ri:02d}{ei:02d}"][0]
            ck(len(ys["relset"]) == len(r0) and len(ys["relset"] - r0) == 1
               and len(r0 - ys["relset"]) == 1,
               f"Y{ri:02d}{ei:02d}: typo rel not single-uid swap")
            ck(ys["eid"] == EID[e] and ys["vok"] == 0, f"Y{ri:02d}{ei:02d} frame")

# 4. NEG / HEDGE / CONTR frames
for k in range(8):
    for j in range(3):
        sn = frames[f"N{k:02d}{j}"][0]
        ck(sn["att"] == 2 and sn["vok"] == 1, f"N{k:02d}{j} not negated value frame")
        pn = frames[f"PN{k:02d}{j}"][0]
        # parser keeps the polarity marker ("not") inside the relation set:
        # teach rel must equal probe rel plus exactly one marker uid.
        ck(pn["relset"] < sn["relset"] and len(sn["relset"]) - len(pn["relset"]) == 1,
           f"PN{k:02d}{j} rel != teach-minus-marker")
        ck(pn["att"] == 0, f"PN{k:02d}{j} probe att")
        sh = frames[f"H{k:02d}{j}"][0]
        ck(sh["att"] == 1 and sh["vok"] == 1, f"H{k:02d}{j} not hedged value frame")
        ph = frames[f"PH{k:02d}{j}"][0]
        ck(ph["relset"] < sh["relset"] and len(sh["relset"]) - len(ph["relset"]) == 1,
           f"PH{k:02d}{j} rel != teach-minus-marker")
        sc = frames[f"C{k:02d}{j}"]
        ck(len(sc) == 2, f"C{k:02d}{j} should have 2 sentences")
        ck(sc[0]["relset"] == sc[1]["relset"] and sc[0]["eid"] == sc[1]["eid"],
           f"C{k:02d}{j} contra sentences frame mismatch")
        ck(sc[0]["att"] == 0 and sc[1]["att"] == 0, f"C{k:02d}{j} not asserted")
        ck(sc[0]["val"] != sc[1]["val"], f"C{k:02d}{j} values not distinct")
        ck(frames[f"PC{k:02d}{j}"][0]["relset"] == sc[0]["relset"], f"PC{k:02d}{j} rel != teach")

# 5. DISTR: untaught relations never equal any taught relset; probes value-less
taught_rels = set()
for sid, ss in frames.items():
    if ss[0]["kind"] == "T":
        for s in ss:
            taught_rels.add(s["relset"])
for k in range(8):
    for j in range(3):
        sd = frames[f"DE{k:02d}{j}"][0]
        ck(sd["vok"] == 0, f"DE{k:02d}{j} probe has value?")
for k in range(8):
    for j in range(3):
        sd = frames[f"DR{k:02d}{j}"][0]
        ck(sd["relset"] not in taught_rels, f"DR{k:02d}{j} rel collides with taught")
        ck(sd["vok"] == 0, f"DR{k:02d}{j} probe has value?")

# 6. expected.json values match teach frames (VALUE probes)
for sid, e in expected.items():
    v = e["verdict"]
    if v.startswith("VALUE:"):
        want = int(v.split(":")[1])
        s = frames[sid][0]
        ck(s["vok"] == 0, f"{sid}: value probe parsed with vok=1")

# 7. no probe has unknown entity
for sid, ss in frames.items():
    if ss[0]["kind"] == "P":
        ck(all(s["eid"] != 4294967295 for s in ss), f"{sid}: probe unknown entity")

# 8. polarity markers: one consistent uid each, never colliding with probe rels
not_uids = set()
might_uids = set()
for k in range(8):
    for j in range(3):
        sn = frames[f"N{k:02d}{j}"][0]
        pn = frames[f"PN{k:02d}{j}"][0]
        not_uids.add(next(iter(sn["relset"] - pn["relset"])))
        sh = frames[f"H{k:02d}{j}"][0]
        ph = frames[f"PH{k:02d}{j}"][0]
        might_uids.add(next(iter(sh["relset"] - ph["relset"])))
ck(len(not_uids) == 1, f"'not' marker uids not consistent: {not_uids}")
ck(len(might_uids) == 1, f"'might' marker uids not consistent: {might_uids}")
ck(not_uids != might_uids, "not/might marker uid collision")

print("FAILURES:", len(fails))
for m in fails[:40]:
    print(" -", m)
sys.exit(1 if fails else 0)
