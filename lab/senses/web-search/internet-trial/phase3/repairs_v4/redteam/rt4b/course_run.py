#!/usr/bin/env python3
"""RT4b course bars: M1/K1 with final components (as far as artifacts allow).

- decide: decide_rt4b (rebuilt from rt4fix/src/decide.zag), new mode
- joke:  joke_fix (rt4fix build of repaired classifier) on course claims
- r12 votes: COMMITTED votes_solo/helper.tsv (course row texts are not in
  the committed repo, so re-tagging with r12_v4_t3 is impossible; the new
  r12 is endorse-conservative per phase-2 findings, so K1 cannot increase
  from re-tagging — documented as a caveat, not a measurement)
- logic/proofs: committed r6_v4_out.txt (T1 unchanged)
- scoring: committed score_v4.py (unmodified)

HARNESS ONLY - no verdict logic.
"""
import subprocess, os, json, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.join(HERE, "course")
JOKE = "/home/hatch/workspace/scratch-hellhole/redteam/rt4fix/build/joke_fix"
DECIDE = os.path.join(HERE, "decide_rt4b")
OUTDIR = os.path.join(HERE, "course_run")

def load_joke_old(path):
    d = {}
    for ln in open(path, encoding="utf-8"):
        q = ln.rstrip("\n").split("|")
        d[q[0]] = int(q[1])
    return d

def main():
    os.makedirs(OUTDIR, exist_ok=True)
    course = json.load(open("/home/hatch/workspace/scratch-hellhole/hellhole/v3_course.json",
                            encoding="utf-8"))
    claims = {it["id"]: it["claim"] for it in course["items"]}
    cand = {}
    for ln in open(os.path.join(COURSE, "candidates_v4.tsv"), encoding="utf-8"):
        p = ln.rstrip("\n").split("\t")
        cand[p[0]] = (int(p[1]), int(p[2]), int(p[3]))
    r6proof = {}
    for ln in open(os.path.join(COURSE, "r6_v4_out.txt"), encoding="utf-8"):
        q = ln.rstrip("\n").split(" ", 2)
        r6proof[q[0].replace("R6-", "")] = q[2] if len(q) > 2 else ""
    votes = {}
    for arm in ("solo", "helper"):
        v = {}
        for ln in open(os.path.join(COURSE, "votes_%s.tsv" % arm), encoding="utf-8"):
            p = ln.rstrip("\n").split("\t")
            v.setdefault(p[0], []).append((int(p[1]), int(p[2])))
        votes[arm] = v
    # repaired joke intents on course claims
    joke_in = os.path.join(OUTDIR, "joke_in.tsv")
    ids = ["V3-%02d" % i for i in range(1, 25)]
    open(joke_in, "w", encoding="utf-8").write(
        "\n".join("%s\t%s" % (cid, claims[cid]) for cid in ids) + "\n")
    r = subprocess.run([JOKE, joke_in], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[:300]
    open(os.path.join(OUTDIR, "joke_out.txt"), "w", encoding="utf-8").write(r.stdout)
    jint = {}
    for ln in r.stdout.splitlines():
        q = ln.split("\t")
        jint[q[0]] = int(q[1])

    DC = {"INSTALL": 2, "REJECT": 3, "WITHHOLD": 4}
    for arm in ("solo", "helper"):
        lines = []
        for cid in ids:
            gated, logic, isj = cand[cid]
            proof = r6proof.get(cid, "")
            w = [0, 0, 0]; ne = nd = 0
            for tag, wt in votes[arm].get(cid, []):
                w[tag] += wt
                if tag == 1: ne += 1
                if tag == 2: nd += 1
            lines.append("%s\t%d\t%d\t%s\t%d\t%d\t%d\t%d\t%d\t%d\t%d" % (
                cid, gated, logic, proof, isj, jint[cid],
                w[0], w[1], w[2], ne, nd))
        dec_in = os.path.join(OUTDIR, "decide_in_%s.tsv" % arm)
        open(dec_in, "w", encoding="utf-8").write("\n".join(lines) + "\n")
        r = subprocess.run([DECIDE, dec_in, "new"], capture_output=True, text=True)
        assert r.returncode == 0, r.stderr[:300]
        disp = {}
        for ln in r.stdout.splitlines():
            p = ln.split("\t")
            disp[p[0]] = (p[1], p[2])
        led = []
        for i, cid in enumerate(ids):
            d, a = disp[cid]
            led.append("%s\t%d\t%s\t%d\t%s\tmode=new" % (arm, i, cid, DC[d], a))
        open(os.path.join(OUTDIR, "ledger_%s.tsv" % arm), "w",
             encoding="utf-8").write("\n".join(led) + "\n")
    # score with committed score_v4.py
    r = subprocess.run(["python3", os.path.join(HERE, "score_v4.py"), OUTDIR],
                       capture_output=True, text=True, cwd=HERE)
    print(r.stdout)
    print(r.stderr[:500] if r.returncode else "", end="")
    # determinism: hash the ledgers
    for arm in ("solo", "helper"):
        b = open(os.path.join(OUTDIR, "ledger_%s.tsv" % arm), "rb").read()
        print("ledger_%s SHA256: %s" % (arm, hashlib.sha256(b).hexdigest()))

if __name__ == "__main__":
    main()
