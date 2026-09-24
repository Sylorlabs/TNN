#!/usr/bin/env python3
"""rt4final acceptance: RT4's original 32+32 corpus through the REAL pipeline.

GLUE ONLY — no verdict logic. Components: logic_bin (real R6 core),
r12_v4_t8 (shipped), joke_run (real repaired classifier), decide (mode new).
Reads: ../rt4/rta_pipeline.tsv, ../rt4/rtb_pipeline.tsv (7 fields:
  id, claim, ctype, oracle, claim_prop, evidence_props, rows).
Writes under redteam/rt4final/accept/: logic_in.tsv, r12_in.tsv, joke_in.tsv,
  component outputs, decide_in.tsv, decide_out.tsv, accept_report.json,
  per-item verdict log.
Runs every component 2x; asserts byte-identical SHAs.
"""
import subprocess, sys, os, json, hashlib

RT4FINAL = "/home/hatch/workspace/scratch-hellhole/redteam/rt4final"
RT4 = "/home/hatch/workspace/scratch-hellhole/redteam/rt4"
BLD = RT4FINAL + "/build"
OUT = RT4FINAL + "/accept"
R12 = "/home/hatch/workspace/scratch-hellhole/redteam/rt2fix7c/r12_v4_t8"
WT = {3: 32, 2: 16, 1: 8, 0: 4, -1: 1}
GATED = {"CONTESTED", "AMBIGUOUS", "EVOLVED", "SKEPTICISM"}
os.makedirs(OUT, exist_ok=True)

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

def run2(binary, inp, outbase, extra=()):
    """Run binary twice on inp; assert byte-identical; write outbase."""
    outs = []
    for i in (1, 2):
        r = subprocess.run([binary, inp] + list(extra), capture_output=True)
        assert r.returncode == 0, (binary, r.stderr[:200])
        p = "%s.run%d" % (outbase, i)
        open(p, "wb").write(r.stdout)
        outs.append(p)
    assert sha(outs[0]) == sha(outs[1]), "NONDETERMINISM: %s" % binary
    os.replace(outs[0], outbase)
    os.remove(outs[1])
    return sha(outbase)

def parse_corpus(path):
    items = []
    for ln in open(path, encoding="utf-8"):
        p = ln.rstrip("\n").split("\t")
        assert len(p) == 7, (path, p[0], len(p))
        rows = []
        for chunk in p[6].split(";;"):
            src, t, txt = chunk.split("|", 2)
            rows.append((src, int(t), txt))
        items.append(dict(id=p[0], claim=p[1], ctype=p[2], oracle=p[3],
                          cprop=p[4], eprops=p[5], rows=rows))
    return items

def load_tags(path):
    d = {}
    for ln in open(path, encoding="utf-8"):
        ln = ln.rstrip("\n")
        if not ln:
            continue
        q = ln.split(" ", 2)
        d[q[0]] = (int(q[1]), q[2] if len(q) > 2 else "")
    return d

def load_joke(path):
    d = {}
    for ln in open(path, encoding="utf-8"):
        q = ln.rstrip("\n").split("\t")
        d[q[0]] = int(q[1])
    return d

def load_decide(path):
    d = {}
    for ln in open(path, encoding="utf-8"):
        q = ln.rstrip("\n").split("\t")
        d[q[0]] = (q[1], q[2], q[3] if len(q) > 3 else "")
    return d

def main():
    rta = parse_corpus(RT4 + "/rta_pipeline.tsv")
    rtb = parse_corpus(RT4 + "/rtb_pipeline.tsv")
    items = rta + rtb
    assert len(rta) == 32 and len(rtb) == 32, (len(rta), len(rtb))

    # --- component inputs ---
    with open(OUT + "/logic_in.tsv", "w", encoding="utf-8") as f:
        for it in items:
            f.write("%s\t%s\t%s\t0\n" % (it["id"], it["cprop"], it["eprops"]))
    with open(OUT + "/r12_in.tsv", "w", encoding="utf-8") as f:
        for it in items:
            for n, (src, t, txt) in enumerate(it["rows"]):
                f.write("%s-r%d\t%s\t%s\t%d\t%s\n" %
                        (it["id"], n, it["claim"], it["id"], t, txt))
    with open(OUT + "/joke_in.tsv", "w", encoding="utf-8") as f:
        for it in items:
            f.write("%s\t%s\n" % (it["id"], it["claim"]))

    shas = {}
    shas["logic_out"] = run2(BLD + "/logic_bin", OUT + "/logic_in.tsv",
                             OUT + "/logic_out.txt")
    shas["r12_out"] = run2(R12, OUT + "/r12_in.tsv", OUT + "/r12_out.txt")
    shas["joke_out"] = run2(BLD + "/joke_run", OUT + "/joke_in.tsv",
                            OUT + "/joke_out.txt")

    logic = load_tags(OUT + "/logic_out.txt")
    r12 = load_tags(OUT + "/r12_out.txt")
    joke = load_joke(OUT + "/joke_out.txt")

    # --- decide inputs (assembly wiring, same shape as rt4fix) ---
    lines = []
    for it in items:
        iid = it["id"]
        w = [0, 0, 0]; ne = nd = 0
        for n, (src, t, txt) in enumerate(it["rows"]):
            tag = r12["%s-r%d" % (iid, n)][0]
            w[tag] += WT[t]
            if tag == 1: ne += 1
            if tag == 2: nd += 1
        lt, proof = logic[iid]
        ji = joke[iid]
        gated = 1 if it["ctype"] in GATED else 0
        lines.append("%s\t%d\t%d\t%s\t0\t%d\t%d\t%d\t%d\t%d\t%d" % (
            iid, gated, lt, proof, ji, w[0], w[1], w[2], ne, nd))
    open(OUT + "/decide_in.tsv", "w", encoding="utf-8").write(
        "\n".join(lines) + "\n")
    shas["decide_out"] = run2(BLD + "/decide", OUT + "/decide_in.tsv",
                              OUT + "/decide_out.tsv", extra=("new",))
    disp = load_decide(OUT + "/decide_out.tsv")

    # --- score ---
    per_item = []
    for it in items:
        iid = it["id"]
        d, a, why = disp[iid]
        lt, proof = logic[iid]
        per_item.append(dict(id=iid, claim=it["claim"][:80], oracle=it["oracle"],
                             r6tag=lt, r6proof=proof, joke=joke[iid],
                             disp=d, attrib=a, why=why))
    a_hits = [p for p in per_item if p["id"].startswith("A-") and p["disp"] == "INSTALL"]
    b_non = [p for p in per_item if p["id"].startswith("B-") and p["disp"] != "INSTALL"]
    rep = dict(shas=shas,
               rta_installs=len(a_hits), rta_hit_ids=[p["id"] for p in a_hits],
               rtb_noninstalls=len(b_non),
               rtb_noninstall=[dict(id=p["id"], disp=p["disp"], attrib=p["attrib"],
                                    r6tag=p["r6tag"], joke=p["joke"], why=p["why"])
                               for p in b_non],
               per_item=per_item)
    json.dump(rep, open(OUT + "/accept_report.json", "w"), indent=1)
    print("RT-A installs: %d/32 %s" % (len(a_hits), [p["id"] for p in a_hits]))
    print("RT-B non-installs: %d/32 %s" %
          (len(b_non), [(p["id"], p["disp"], p["attrib"]) for p in b_non]))
    for k, v in shas.items():
        print("SHA %s %s" % (k, v))

if __name__ == "__main__":
    main()
