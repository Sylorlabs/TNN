#!/usr/bin/env python3
"""rt4final course bars: M1/K1 (+M3/K2/M-LOGIC/M-JOKE/K3/K5) with REAL components.

GLUE ONLY. Real: joke_run on the 24 course claims, logic_bin on the 6
committed R6 inputs (tags override candidates_v4.tsv's logic column),
decide mode new. Committed (not regenerable — row texts not in repo):
votes_solo.tsv / votes_helper.tsv, candidates' gated/is_joke columns.
Scores with the committed score_v4.py (unmodified).
"""
import subprocess, os, json, hashlib, shutil

RT4FINAL = "/home/hatch/workspace/scratch-hellhole/redteam/rt4final"
BLD = RT4FINAL + "/build"
OUT = RT4FINAL + "/course"
TGT = "/home/hatch/workspace/scratch-hellhole/redteam/rt4/target/pipeline/work/run1"
os.makedirs(OUT, exist_ok=True)

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

def run2(binary, inp, outbase, extra=()):
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

def main():
    course = {it["id"]: it for it in json.load(
        open("/home/hatch/workspace/scratch-hellhole/hellhole/v3_course.json",
             encoding="utf-8"))["items"]}
    assert len(course) == 24

    # --- real joke intents on the 24 course claims ---
    with open(OUT + "/joke_in.tsv", "w", encoding="utf-8") as f:
        for i in range(1, 25):
            cid = "V3-%02d" % i
            f.write("%s\t%s\n" % (cid, course[cid]["claim"]))
    jsha = run2(BLD + "/joke_run", OUT + "/joke_in.tsv", OUT + "/joke_out.txt")
    joke = {}
    for ln in open(OUT + "/joke_out.txt", encoding="utf-8"):
        q = ln.rstrip("\n").split("\t")
        joke[q[0]] = int(q[1])
    assert len(joke) == 24, len(joke)

    # --- real R6 tags on the 6 committed R6 inputs ---
    shutil.copy(TGT + "/r6_v4_input.tsv", OUT + "/r6_in.tsv")
    rsha = run2(BLD + "/logic_bin", OUT + "/r6_in.tsv", OUT + "/r6_out.txt")
    r6 = {}
    for ln in open(OUT + "/r6_out.txt", encoding="utf-8"):
        ln = ln.rstrip("\n")
        if not ln:
            continue
        q = ln.split(" ", 2)
        cid = q[0].replace("R6-", "")
        r6[cid] = (int(q[1]), q[2] if len(q) > 2 else "")
    assert len(r6) == 6, r6.keys()

    # --- candidates: gated/is_joke committed; logic overridden by real R6 ---
    cand = {}
    for ln in open(TGT + "/candidates_v4.tsv", encoding="utf-8"):
        p = ln.rstrip("\n").split("\t")
        cid = p[0]
        gated, _oldlogic, isj = int(p[1]), int(p[2]), int(p[3])
        lt, proof = r6.get(cid, (0, ""))
        cand[cid] = (gated, lt, proof, isj)

    votes = {}
    for arm in ("solo", "helper"):
        votes[arm] = {}
        for ln in open(TGT + "/votes_%s.tsv" % arm, encoding="utf-8"):
            p = ln.rstrip("\n").split("\t")
            votes[arm].setdefault(p[0], []).append((int(p[1]), int(p[2])))

    DC = {"INSTALL": 2, "REJECT": 3, "WITHHOLD": 4}
    shas = {"joke_out": jsha, "r6_out": rsha}
    for arm in ("solo", "helper"):
        lines = []
        for i in range(1, 25):
            cid = "V3-%02d" % i
            gated, lt, proof, isj = cand[cid]
            w = [0, 0, 0]; ne = nd = 0
            for tag, wt in votes[arm].get(cid, []):
                w[tag] += wt
                if tag == 1: ne += 1
                if tag == 2: nd += 1
            lines.append("%s\t%d\t%d\t%s\t%d\t%d\t%d\t%d\t%d\t%d\t%d" % (
                cid, gated, lt, proof, isj, joke[cid],
                w[0], w[1], w[2], ne, nd))
        inp = OUT + "/decide_in_%s.tsv" % arm
        open(inp, "w", encoding="utf-8").write("\n".join(lines) + "\n")
        shas["decide_" + arm] = run2(BLD + "/decide", inp,
                                     OUT + "/decide_out_%s.tsv" % arm,
                                     extra=("new",))
        disp = {}
        for ln in open(OUT + "/decide_out_%s.tsv" % arm, encoding="utf-8"):
            q = ln.rstrip("\n").split("\t")
            disp[q[0]] = (q[1], q[2])
        led = []
        for i in range(1, 25):
            cid = "V3-%02d" % i
            d, a = disp[cid]
            led.append("%s\t%d\t%s\t%d\t%s\tmode=new" %
                       (arm, i - 1, cid, DC[d], a))
        open(OUT + "/ledger_%s.tsv" % arm, "w", encoding="utf-8").write(
            "\n".join(led) + "\n")

    for k, v in shas.items():
        print("SHA %s %s" % (k, v))
    print("real R6 tags:", {k: v[0] for k, v in sorted(r6.items())})
    print("real joke intents:",
          {k: joke[k] for k in sorted(joke) if joke[k] in (2, 3)})

if __name__ == "__main__":
    main()
