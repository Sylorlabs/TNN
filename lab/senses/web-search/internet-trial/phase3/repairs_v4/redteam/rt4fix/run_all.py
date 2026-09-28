#!/usr/bin/env python3
"""rt4fix harness: build decide.zag inputs, run old/new rules, score.

HARNESS ONLY — no verdict logic. The decider is the pure-Zag decide binary.
Reads:
  - RT4 corpora + RT4's component outputs (runs/rta1, runs/rtb1) for the
    committed-component passes; the repaired joke classifier outputs
    (runs/joke_{rta,rtb}_fixed.txt) for the repaired-component pass.
  - Committed course artifacts (target/pipeline/work/run1) + frozen
    v3_course.json for the M1/K1 bar check.
Writes per-run decider inputs/outputs under runs/<name>/ and course ledgers
under runs/course_<arm>_<tag>/ledger_{solo,helper}.tsv for score_v4.py.
"""
import subprocess, sys, os, json

HERE = os.path.dirname(os.path.abspath(__file__))
RT4 = "/home/hatch/workspace/scratch-hellhole/redteam/rt4"
TGT = RT4 + "/target/pipeline/work/run1"
DECIDE = HERE + "/src/decide"
WT = {3: 32, 2: 16, 1: 8, 0: 4, -1: 1}
GATED = {"CONTESTED", "AMBIGUOUS", "EVOLVED", "SKEPTICISM"}

def run_decide(inp, mode):
    r = subprocess.run([DECIDE, inp, mode], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[:300]
    d = {}
    for ln in r.stdout.splitlines():
        p = ln.split("\t")
        d[p[0]] = (p[1], p[2])
    return d

def parse_corpus(path):
    items = []
    for ln in open(path, encoding="utf-8"):
        p = ln.rstrip("\n").split("\t")
        assert len(p) == 7, p[0]
        rows = []
        for chunk in p[6].split(";;"):
            d, t, txt = chunk.split("|", 2)
            rows.append(int(t))
        items.append(dict(id=p[0], ctype=p[2], oracle=p[3], rows=rows))
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

def corpus_inputs(name, corpus, rundir, jokefile):
    items = parse_corpus(corpus)
    r12 = load_tags(rundir + "/r12_out.txt")
    logic = load_tags(rundir + "/logic_out.txt")
    joke = load_joke(jokefile)
    lines = []
    for it in items:
        iid = it["id"]
        w = [0, 0, 0]; ne = nd = 0
        for n, t in enumerate(it["rows"]):
            rid = "%s-r%d" % (iid, n)
            tag = r12[rid][0]
            w[tag] += WT[t]
            if tag == 1: ne += 1
            if tag == 2: nd += 1
        lt, proof = logic[iid]
        ji = joke[iid]
        gated = 1 if it["ctype"] in GATED else 0
        lines.append("%s\t%d\t%d\t%s\t0\t%d\t%d\t%d\t%d\t%d\t%d" % (
            iid, gated, lt, proof, ji, w[0], w[1], w[2], ne, nd))
    return items, lines

def run_corpus(name, corpus, rundir, jokefile, mode, expect):
    items, lines = corpus_inputs(name, corpus, rundir, jokefile)
    outdir = os.path.join(HERE, "runs", name)
    os.makedirs(outdir, exist_ok=True)
    inp = os.path.join(outdir, "decide_in.tsv")
    open(inp, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    disp = run_decide(inp, mode)
    open(os.path.join(outdir, "decide_out_%s.tsv" % mode),
         "w", encoding="utf-8").write(
        "".join("%s\t%s\t%s\n" % (k, v[0], v[1]) for k, v in disp.items()))
    if expect == "A":
        hits = [it["id"] for it in items if disp[it["id"]][0] == "INSTALL"]
    else:
        hits = [it["id"] for it in items if disp[it["id"]][0] != "INSTALL"]
    print("%s mode=%s hits=%d/%d %s" % (name, mode, len(hits), len(items), hits))
    return disp

# ---------------- course ----------------
def load_course():
    c = json.load(open("/home/hatch/workspace/scratch-hellhole/hellhole/v3_course.json",
                        encoding="utf-8"))
    return {it["id"]: it for it in c["items"]}

def course_inputs(arm, jokefile):
    course = load_course()
    cand = {}
    for ln in open(TGT + "/candidates_v4.tsv", encoding="utf-8"):
        p = ln.rstrip("\n").split("\t")
        cand[p[0]] = (int(p[1]), int(p[2]), int(p[3]))  # gated, logic, is_joke
    r6proof = {}
    for ln in open(TGT + "/r6_v4_out.txt", encoding="utf-8"):
        ln = ln.rstrip("\n")
        if not ln:
            continue
        q = ln.split(" ", 2)
        r6proof[q[0].replace("R6-", "")] = q[2] if len(q) > 2 else ""
    votes = {}
    for ln in open(TGT + "/votes_%s.tsv" % arm, encoding="utf-8"):
        p = ln.rstrip("\n").split("\t")
        votes.setdefault(p[0], []).append((int(p[1]), int(p[2])))
    joke = load_joke(jokefile)
    lines = []
    for i in range(1, 25):
        cid = "V3-%02d" % i
        gated, logic, isj = cand[cid]
        proof = r6proof.get(cid, "")
        ji = joke[cid]
        w = [0, 0, 0]; ne = nd = 0
        for tag, wt in votes.get(cid, []):
            w[tag] += wt
            if tag == 1: ne += 1
            if tag == 2: nd += 1
        lines.append("%s\t%d\t%d\t%s\t%d\t%d\t%d\t%d\t%d\t%d\t%d" % (
            cid, gated, logic, proof, isj, ji, w[0], w[1], w[2], ne, nd))
    return lines

def run_course(arm, jokefile, mode, tag):
    lines = course_inputs(arm, jokefile)
    outdir = os.path.join(HERE, "runs", "course_%s_%s" % (arm, tag))
    os.makedirs(outdir, exist_ok=True)
    inp = os.path.join(outdir, "decide_in.tsv")
    open(inp, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    disp = run_decide(inp, mode)
    DC = {"INSTALL": 2, "REJECT": 3, "WITHHOLD": 4}
    led = []
    for i in range(1, 25):
        cid = "V3-%02d" % i
        d, a = disp[cid]
        led.append("%s\t%d\t%s\t%d\t%s\tmode=%s" % (arm, i - 1, cid, DC[d], a, mode))
    open(os.path.join(outdir, "ledger_%s.tsv" % arm), "w",
         encoding="utf-8").write("\n".join(led) + "\n")
    return disp

def main():
    os.makedirs(HERE + "/runs", exist_ok=True)
    # 1. reproduction: committed components + old rule
    run_corpus("rta_old", RT4 + "/rta_pipeline.tsv", RT4 + "/runs/rta1",
               RT4 + "/runs/rta1/joke_out.txt", "old", "A")
    run_corpus("rtb_old", RT4 + "/rtb_pipeline.tsv", RT4 + "/runs/rtb1",
               RT4 + "/runs/rtb1/joke_out.txt", "old", "B")
    # 2. new rule, committed components
    run_corpus("rta_new", RT4 + "/rta_pipeline.tsv", RT4 + "/runs/rta1",
               RT4 + "/runs/rta1/joke_out.txt", "new", "A")
    run_corpus("rtb_new", RT4 + "/rtb_pipeline.tsv", RT4 + "/runs/rtb1",
               RT4 + "/runs/rtb1/joke_out.txt", "new", "B")
    # 3. new rule, repaired joke classifier
    run_corpus("rta_new_fj", RT4 + "/rta_pipeline.tsv", RT4 + "/runs/rta1",
               HERE + "/runs/joke_rta_fixed.txt", "new", "A")
    run_corpus("rtb_new_fj", RT4 + "/rtb_pipeline.tsv", RT4 + "/runs/rtb1",
               HERE + "/runs/joke_rtb_fixed.txt", "new", "B")
    # 4. course bars: old rule sanity (must match committed ledger)
    for arm in ("solo", "helper"):
        run_course(arm, HERE + "/runs/joke_course_orig.txt", "old", "old_origjoke")
    # 5. course bars: new rule + original joke
    for arm in ("solo", "helper"):
        run_course(arm, HERE + "/runs/joke_course_orig.txt", "new", "new_origjoke")
    # 6. course bars: new rule + repaired joke
    for arm in ("solo", "helper"):
        run_course(arm, HERE + "/runs/joke_course_fixed.txt", "new", "new_fixedjoke")

if __name__ == "__main__":
    main()
