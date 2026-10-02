#!/usr/bin/env python3
"""RT4b phase-2: fresh blind attack on corpus_fresh.tsv (frozen BEFORE any
target runs; SHA 563a4bce...).

Pipeline (all pure-Zag, zero RNG):
  rows -> r12_v4_t3 -> tags
  claim -> joke_fix -> intent
  R6 tags/proofs -> frozen oracle-authored (T1 logic core is a separate
                    track, not among this task's components; disclosed)
  -> decide_rt4b new mode -> dispositions

Scoring: RT-A (oracle NONINSTALL) hit iff INSTALL.
         RT-B (oracle INSTALL) hit iff disposition != INSTALL.
         Probes (oracle PROBE:X): predicted-vs-actual map, informational.
HARNESS ONLY - no verdict logic.
"""
import subprocess, os, hashlib, json

HERE = os.path.dirname(os.path.abspath(__file__))
R12 = "/home/hatch/workspace/scratch-hellhole/redteam/rt2fix4/r12_v4_t3"
JOKE = "/home/hatch/workspace/scratch-hellhole/redteam/rt4fix/build/joke_fix"
DECIDE = os.path.join(HERE, "decide_rt4b")
WT = {3: 32, 2: 16, 1: 8, 0: 4, -1: 1}
GATED = {"CONTESTED", "AMBIGUOUS", "EVOLVED", "SKEPTICISM"}
OUTDIR = os.path.join(HERE, "attack")

def parse_corpus(path):
    items = []
    for ln in open(path, encoding="utf-8"):
        p = ln.rstrip("\n").split("\t")
        assert len(p) == 7, p[0]
        rows = []
        for chunk in p[6].split(";;"):
            d, t, txt = chunk.split("|", 2)
            rows.append((d, int(t), txt))
        items.append(dict(id=p[0], claim=p[1], ctype=p[2], oracle=p[3],
                          r6tag=int(p[4]), r6proof=p[5], rows=rows))
    return items

def main():
    os.makedirs(OUTDIR, exist_ok=True)
    items = parse_corpus(os.path.join(HERE, "corpus_fresh.tsv"))
    assert len(items) == 72

    r12_lines = []
    for it in items:
        for n, (d, t, txt) in enumerate(it["rows"]):
            r12_lines.append("%s-r%d\t%s\t%s\t%d\t%s" % (
                it["id"], n, it["claim"], it["id"], t, txt))
    r12_in = os.path.join(OUTDIR, "r12_in.tsv")
    open(r12_in, "w", encoding="utf-8").write("\n".join(r12_lines) + "\n")
    r = subprocess.run([R12, r12_in], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[:300]
    open(os.path.join(OUTDIR, "r12_out.txt"), "w", encoding="utf-8").write(r.stdout)
    r12tags, r12why = {}, {}
    for ln in r.stdout.splitlines():
        q = ln.split(" ", 2)
        r12tags[q[0]] = int(q[1]); r12why[q[0]] = q[2] if len(q) > 2 else ""

    joke_in = os.path.join(OUTDIR, "joke_in.tsv")
    open(joke_in, "w", encoding="utf-8").write(
        "\n".join("%s\t%s" % (it["id"], it["claim"]) for it in items) + "\n")
    r = subprocess.run([JOKE, joke_in], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[:300]
    open(os.path.join(OUTDIR, "joke_out.txt"), "w", encoding="utf-8").write(r.stdout)
    intents, jcodes = {}, {}
    for ln in r.stdout.splitlines():
        q = ln.split("\t")
        intents[q[0]] = int(q[1]); jcodes[q[0]] = q[2] if len(q) > 2 else ""

    dec_lines, detail = [], {}
    for it in items:
        iid = it["id"]
        w = [0, 0, 0]; ne = nd = 0; tags = []
        for n, (d, t, txt) in enumerate(it["rows"]):
            rid = "%s-r%d" % (iid, n)
            tag = r12tags[rid]
            tags.append((tag, r12why[rid]))
            w[tag] += WT[t]
            if tag == 1: ne += 1
            if tag == 2: nd += 1
        ji = intents[iid]
        gated = 1 if it["ctype"] in GATED else 0
        isj = 1 if it["ctype"] == "JOKE" else 0
        dec_lines.append("%s\t%d\t%d\t%s\t%d\t%d\t%d\t%d\t%d\t%d\t%d" % (
            iid, gated, it["r6tag"], it["r6proof"], isj, ji,
            w[0], w[1], w[2], ne, nd))
        detail[iid] = dict(oracle=it["oracle"], r6tag=it["r6tag"],
                           intent=ji, jcodes=jcodes[iid], w=w, ne=ne, nd=nd,
                           tags=tags, gated=gated)
    dec_in = os.path.join(OUTDIR, "decide_in.tsv")
    open(dec_in, "w", encoding="utf-8").write("\n".join(dec_lines) + "\n")
    r = subprocess.run([DECIDE, dec_in, "new"], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[:300]
    open(os.path.join(OUTDIR, "decide_out.tsv"), "w", encoding="utf-8").write(r.stdout)
    disp = {}
    for ln in r.stdout.splitlines():
        p = ln.split("\t")
        disp[p[0]] = (p[1], p[2])

    rta_hits, rtb_hits, probes = [], [], []
    for it in items:
        iid = it["id"]
        d, a = disp[iid]
        info = detail[iid]; info["disp"] = d; info["attrib"] = a
        detail[iid] = info
        oc = it["oracle"]
        if oc == "NONINSTALL":
            if d == "INSTALL": rta_hits.append(iid)
        elif oc == "INSTALL":
            if d != "INSTALL": rtb_hits.append(iid)
        else:
            probes.append((iid, oc.split(":", 1)[1], d, a))
    rep = {"rta_hits": rta_hits, "rtb_hits": rtb_hits,
           "probes": [{"id": i, "predicted": p, "actual": d, "attrib": a}
                      for i, p, d, a in probes],
           "detail": detail}
    open(os.path.join(OUTDIR, "attack_report.json"), "w", encoding="utf-8").write(
        json.dumps(rep, indent=1, sort_keys=True))
    print("RT-A installs (hits): %d/32 %s" % (len(rta_hits), rta_hits))
    print("RT-B non-installs (hits): %d/32 %s" % (len(rtb_hits), rtb_hits))
    for iid in rta_hits + rtb_hits:
        i = detail[iid]
        print("  HIT %s oracle=%s disp=%s attrib=%s r6=%d intent=%d(%s) w=%s ne=%d nd=%d tags=%s" % (
            iid, i["oracle"], i["disp"], i["attrib"], i["r6tag"], i["intent"],
            i["jcodes"], i["w"], i["ne"], i["nd"], i["tags"]))
    print("probes:")
    for i, p, d, a in probes:
        mark = "OK " if p == d else "DIFF"
        print("  %s %s predicted=%s actual=%s attrib=%s" % (mark, i, p, d, a))
    print("decide_out SHA256:", hashlib.sha256(r.stdout.encode("utf-8")).hexdigest())

if __name__ == "__main__":
    main()
