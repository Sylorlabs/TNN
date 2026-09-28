#!/usr/bin/env python3
"""RT4 pipeline runner (HARNESS ONLY — no verdict logic here).

Reconstructs the v4 pipeline decision order from the committed artifacts:
  R3 gate -> R6 logic (logic_bin) -> joke gate (joke_rt4) -> R5 vote (r12_v4).
Decision rule transcribed from committed crews/pipeline/work/run1/ledger_solo.tsv:
  - gated (claim_type in {CONTESTED,AMBIGUOUS,EVOLVED,SKEPTICISM}) -> WITHHOLD (R3, terminal)
  - logic_bin tag == 2 (DENY) -> REJECT (R6 precedence, terminal)
  - is_joke (claim_type == JOKE-FAMILY): intent in {2,3} -> REJECT; else WITHHOLD (JOKE)
  - R5 votes: w1 > w2 -> INSTALL; w2 > w1 -> REJECT; tie -> WITHHOLD
    (V3-01 84>8 INSTALL; V3-03 48=48 WITHHOLD; V3-05 68>24 REJECT)
Weights: tier->weight {3:32, 2:16, 1:8, 0:4, -1:1} (committed assemble_v4.py).
The deciders are the three Zag binaries; this script only assembles inputs,
parses outputs, and applies the transcribed rule.

Usage: run_rt4.py <corpus.tsv> <outdir>
"""
import subprocess, sys, os, hashlib

BUILD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build")
LOGIC = os.path.join(BUILD, "logic_bin")
R12 = os.path.join(BUILD, "r12_v4")
JOKE = os.path.join(BUILD, "joke_rt4")
WT = {3: 32, 2: 16, 1: 8, 0: 4, -1: 1}
GATED = {"CONTESTED", "AMBIGUOUS", "EVOLVED", "SKEPTICISM"}

def run_bin(path, arg):
    r = subprocess.run([path, arg], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError("%s failed rc=%d: %s" % (path, r.returncode, r.stderr[:500]))
    return r.stdout

def parse_items(corpus):
    items = []
    for ln in open(corpus, encoding="utf-8"):
        p = ln.rstrip("\n").split("\t")
        assert len(p) == 7, p[0]
        iid, claim, ctype, oracle, pclaim, pev, ev = p
        rows = []
        for chunk in ev.split(";;"):
            d, t, txt = chunk.split("|", 2)
            rows.append((d, int(t), txt))
        items.append(dict(id=iid, claim=claim, ctype=ctype, oracle=oracle,
                          pclaim=pclaim, pev=pev, rows=rows))
    return items

def main():
    corpus, outdir, mode = sys.argv[1], sys.argv[2], sys.argv[3]
    assert mode in ("A", "B"), mode  # A: hit iff INSTALL; B: hit iff not INSTALL
    os.makedirs(outdir, exist_ok=True)
    items = parse_items(corpus)

    # --- r12 input ---
    r12lines, r12map = [], {}
    for it in items:
        for n, (d, t, txt) in enumerate(it["rows"]):
            rid = "%s-r%d" % (it["id"], n)
            r12map[rid] = (it["id"], t)
            r12lines.append("%s\t%s\t\t%s" % (rid, it["claim"], txt))
    r12in = os.path.join(outdir, "r12_in.tsv")
    open(r12in, "w", encoding="utf-8").write("\n".join(r12lines) + "\n")
    r12out = run_bin(R12, r12in)
    open(os.path.join(outdir, "r12_out.txt"), "w").write(r12out)
    r12tag = {}
    for ln in r12out.splitlines():
        q = ln.split(" ", 2)
        r12tag[q[0]] = (int(q[1]), q[2] if len(q) > 2 else "")

    # --- logic input ---
    loglines = []
    for it in items:
        loglines.append("%s\t%s\t%s\t0" % (it["id"], it["pclaim"], it["pev"]))
    login = os.path.join(outdir, "logic_in.tsv")
    open(login, "w", encoding="utf-8").write("\n".join(loglines) + "\n")
    logout = run_bin(LOGIC, login)
    open(os.path.join(outdir, "logic_out.txt"), "w").write(logout)
    logres = {}
    for ln in logout.splitlines():
        q = ln.split(" ", 2)
        logres[q[0]] = (int(q[1]), q[2] if len(q) > 2 else "")

    # --- joke input (informational for all; gate consulted only if JOKE-FAMILY) ---
    jokelines = ["%s\t%s" % (it["id"], it["claim"]) for it in items]
    jokein = os.path.join(outdir, "joke_in.tsv")
    open(jokein, "w", encoding="utf-8").write("\n".join(jokelines) + "\n")
    jokeout = run_bin(JOKE, jokein)
    open(os.path.join(outdir, "joke_out.txt"), "w").write(jokeout)
    jokeres = {}
    for ln in jokeout.splitlines():
        q = ln.rstrip("\n").split("\t")
        jokeres[q[0]] = (int(q[1]), q[2] if len(q) > 2 else "", q[3] if len(q) > 3 else "")

    # --- decide ---
    ledger = []
    for it in items:
        iid = it["id"]
        w = [0, 0, 0]
        tagdetail = []
        for n, (d, t, txt) in enumerate(it["rows"]):
            rid = "%s-r%d" % (iid, n)
            tag, rsn = r12tag[rid]
            w[tag] += WT[t]
            tagdetail.append("%s=%d(%s)" % (rid, tag, rsn))
        ltag, proof = logres[iid]
        jint, jcodes, jmarks = jokeres[iid]
        if it["ctype"] in GATED:
            disp, attrib, why = "WITHHOLD", "R3", "gated claim_type"
        elif ltag == 2:
            disp, attrib, why = "REJECT", "R6", "logic DENY proof=%s" % proof
        elif it["ctype"] == "JOKE-FAMILY":
            if jint in (2, 3):
                disp, attrib, why = "REJECT", "JOKE", "intent=%d codes=%s" % (jint, jcodes)
            else:
                disp, attrib, why = "WITHHOLD", "JOKE", "intent=%d codes=%s" % (jint, jcodes)
        else:
            if w[1] > w[2]:
                disp, attrib = "INSTALL", "R5"
            elif w[2] > w[1]:
                disp, attrib = "REJECT", "R5"
            else:
                disp, attrib = "WITHHOLD", "R5"
            why = "w0=%d w1=%d w2=%d logic=%d(%s) tags=%s" % (w[0], w[1], w[2], ltag, proof, ";".join(tagdetail))
        if mode == "A":
            hit = "HIT" if disp == "INSTALL" else "ok"
        else:
            hit = "HIT" if disp != "INSTALL" else "ok"
        ledger.append("%s\t%s\t%s\t%s\t%s\t%s\tjintent=%d(%s)\t%s" % (
            iid, disp, attrib, it["oracle"], hit, why, jint, jcodes, it["claim"][:60]))
    open(os.path.join(outdir, "ledger.tsv"), "w").write("\n".join(ledger) + "\n")

    n_hit = sum(1 for l in ledger if "\tHIT\t" in l)
    print("items=%d hits=%d" % (len(ledger), n_hit))
    for l in ledger:
        if "\tHIT\t" in l:
            print(" ", l)

if __name__ == "__main__":
    main()
