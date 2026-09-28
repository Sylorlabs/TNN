#!/usr/bin/env python3
"""RT4b phase-1: mechanical acceptance on RT4's original 32+32 corpus.

Pipeline (all pure-Zag, zero RNG):
  rows -> r12_v4_t3 (repaired classifier, shipped binary) -> tags
  claim -> joke_fix (rt4fix build of repaired joke classifier) -> intent
  logic tags -> RT4's committed logic_out.txt (T1 logic core unchanged by repairs)
  (gated, logic, proof, is_joke=0, intent, w0,w1,w2,ne,nd) -> decide_rt4b new mode

HARNESS ONLY - no verdict logic. Run twice; outputs must be byte-identical.
"""
import subprocess, sys, os, hashlib, json

HERE = os.path.dirname(os.path.abspath(__file__))
RT4 = "/home/hatch/workspace/scratch-hellhole/redteam/rt4"
R12 = "/home/hatch/workspace/scratch-hellhole/redteam/rt2fix4/r12_v4_t3"
JOKE = "/home/hatch/workspace/scratch-hellhole/redteam/rt4fix/build/joke_fix"
DECIDE = os.path.join(HERE, "decide_rt4b")
WT = {3: 32, 2: 16, 1: 8, 0: 4, -1: 1}
GATED = {"CONTESTED", "AMBIGUOUS", "EVOLVED", "SKEPTICISM"}
OUTDIR = os.path.join(HERE, "accept")

def parse_corpus(path):
    items = []
    for ln in open(path, encoding="utf-8"):
        p = ln.rstrip("\n").split("\t")
        assert len(p) == 7, p[0]
        rows = []
        for chunk in p[6].split(";;"):
            d, t, txt = chunk.split("|", 2)
            rows.append((d, int(t), txt))
        items.append(dict(id=p[0], claim=p[1], ctype=p[2], oracle=p[3], rows=rows))
    return items

def load_logic(path):
    d = {}
    for ln in open(path, encoding="utf-8"):
        q = ln.rstrip("\n").split(" ", 2)
        d[q[0]] = (int(q[1]), q[2] if len(q) > 2 else "")
    return d

def run_bin(args, inp_path):
    r = subprocess.run(args + [inp_path], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[:300]
    return r.stdout

def main():
    os.makedirs(OUTDIR, exist_ok=True)
    corpora = [("rta", RT4 + "/rta_pipeline.tsv", RT4 + "/runs/rta1/logic_out.txt"),
               ("rtb", RT4 + "/rtb_pipeline.tsv", RT4 + "/runs/rtb1/logic_out.txt")]
    all_items, logic = [], {}
    for name, cpath, lpath in corpora:
        all_items += parse_corpus(cpath)
        logic.update(load_logic(lpath))
    assert len(all_items) == 64

    # r12 inputs: rowid \t claim \t itemid \t tier \t rowtext
    r12_lines = []
    for it in all_items:
        for n, (d, t, txt) in enumerate(it["rows"]):
            r12_lines.append("%s-r%d\t%s\t%s\t%d\t%s" % (
                it["id"], n, it["claim"], it["id"], t, txt))
    r12_in = os.path.join(OUTDIR, "r12_in.tsv")
    open(r12_in, "w", encoding="utf-8").write("\n".join(r12_lines) + "\n")
    r12_out = run_bin([R12], r12_in)
    open(os.path.join(OUTDIR, "r12_out.txt"), "w", encoding="utf-8").write(r12_out)
    r12tags = {}
    for ln in r12_out.splitlines():
        q = ln.split(" ", 2)
        r12tags[q[0]] = int(q[1])

    # joke inputs: id \t claim
    joke_lines = ["%s\t%s" % (it["id"], it["claim"]) for it in all_items]
    joke_in = os.path.join(OUTDIR, "joke_in.tsv")
    open(joke_in, "w", encoding="utf-8").write("\n".join(joke_lines) + "\n")
    joke_out = run_bin([JOKE], joke_in)
    open(os.path.join(OUTDIR, "joke_out.txt"), "w", encoding="utf-8").write(joke_out)
    intents = {}
    for ln in joke_out.splitlines():
        q = ln.split("\t")
        intents[q[0]] = int(q[1])

    # decide inputs
    dec_lines, detail = [], {}
    for it in all_items:
        iid = it["id"]
        w = [0, 0, 0]; ne = nd = 0
        tags = []
        for n, (d, t, txt) in enumerate(it["rows"]):
            rid = "%s-r%d" % (iid, n)
            tag = r12tags[rid]
            tags.append(tag)
            w[tag] += WT[t]
            if tag == 1: ne += 1
            if tag == 2: nd += 1
        lt, proof = logic[iid]
        ji = intents[iid]
        gated = 1 if it["ctype"] in GATED else 0
        dec_lines.append("%s\t%d\t%d\t%s\t0\t%d\t%d\t%d\t%d\t%d\t%d" % (
            iid, gated, lt, proof, ji, w[0], w[1], w[2], ne, nd))
        detail[iid] = dict(oracle=it["oracle"], ltag=lt, proof=bool(proof),
                           intent=ji, w=w, ne=ne, nd=nd, tags=tags)
    dec_in = os.path.join(OUTDIR, "decide_in.tsv")
    open(dec_in, "w", encoding="utf-8").write("\n".join(dec_lines) + "\n")
    dec_out_r = subprocess.run([DECIDE, dec_in, "new"], capture_output=True, text=True)
    assert dec_out_r.returncode == 0, dec_out_r.stderr[:300]
    dec_out = dec_out_r.stdout
    open(os.path.join(OUTDIR, "decide_out.tsv"), "w", encoding="utf-8").write(dec_out)
    disp = {}
    for ln in dec_out.splitlines():
        p = ln.split("\t")
        disp[p[0]] = (p[1], p[2])

    # score
    rep = {"rta_hits": [], "rtb_hits": [], "detail": {}}
    for it in all_items:
        iid = it["id"]
        d, a = disp[iid]
        info = detail[iid]; info["disp"] = d; info["attrib"] = a
        rep["detail"][iid] = info
        if iid.startswith("A-"):
            if d == "INSTALL": rep["rta_hits"].append(iid)
        else:
            if d != "INSTALL": rep["rtb_hits"].append(iid)
    rep["rta"] = "%d/32" % len(rep["rta_hits"])
    rep["rtb_noninstall"] = "%d/32" % len(rep["rtb_hits"])
    open(os.path.join(OUTDIR, "accept_report.json"), "w", encoding="utf-8").write(
        json.dumps(rep, indent=1, sort_keys=True))
    print("RT-A installs: %d/32 %s" % (len(rep["rta_hits"]), rep["rta_hits"]))
    print("RT-B non-installs: %d/32 %s" % (len(rep["rtb_hits"]), rep["rtb_hits"]))
    for iid in rep["rtb_hits"]:
        i = rep["detail"][iid]
        print("  %s disp=%s attrib=%s ltag=%d proof=%s intent=%d w=%s ne=%d nd=%d tags=%s" % (
            iid, i["disp"], i["attrib"], i["ltag"], i["proof"], i["intent"],
            i["w"], i["ne"], i["nd"], i["tags"]))
    h = hashlib.sha256(dec_out.encode("utf-8")).hexdigest()
    print("decide_out SHA256:", h)

if __name__ == "__main__":
    main()
