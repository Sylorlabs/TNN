#!/usr/bin/env python3
"""run_eval_e2b.py -- FS-E2b eval driver (glue only).

Pipeline per battery list (b_adv_e2b, b_ctrl_e2b), each run TWICE:
  1. fse2b_form batch <list>            -> formation TSV (pure Zag)
  2. claim TSV: <path>\\t<claim_id>      (name->id map, validated by echo)
  3. fse2b_sup <claim.tsv>              -> gate decision lines (pure Zag;
     challenge + support rule + admission are byte-verbatim FS-E1b registry)
  4. hash-chained ledger assembly        (sha256(prev_raw32 + content))
Byte-compare r1 vs r2 at every stage; verify every hash chain.

Gate decisions come from frozen Zag; Python only transports and chains.
Zero RNG in any decision path.
"""
import subprocess, os, sys, hashlib

FORK = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2/forks/FS-E2b"
EV = os.path.join(FORK, "evidence", "eval")
FORM = os.path.join(FORK, "src", "fse2b_form")
SUP = os.path.join(FORK, "src", "fse2b_sup")

# judgment name -> claim id (== f_jname in fse2b_form.zag, == jname in fse1b.zag)
JMAP = {
    0: {"SAME": 0, "DIFFERENT": 1},
    1: {"SAME_SURFACE": 0, "DIFFERENT": 1},
    2: {"CIRCLE": 0, "TRIANGLE": 1, "SQUARE": 2},
    3: {"SAME": 0, "HIGHER": 1, "LOWER": 2},
    4: {"PURE": 0, "BRIGHT": 1, "DARK": 2, "RICH": 3},
    5: {"STILL": 0, "N": 1, "NE": 2, "E": 3, "SE": 4, "S": 5, "SW": 6, "W": 7, "NW": 8},
}
TN = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def run_form(listpath, tsvpath):
    with open(tsvpath, "w") as out:
        r = subprocess.run([FORM, "batch", listpath], stdout=out,
                           stderr=subprocess.STDOUT)
    if r.returncode != 0:
        raise SystemExit("formation FAILED rc=%d on %s" % (r.returncode, listpath))
    for line in open(tsvpath):
        if line.startswith("error="):
            raise SystemExit("formation error: " + line.strip())


def parse_form_tsv(tsvpath):
    rows = []
    for line in open(tsvpath):
        p, t, j = line.rstrip("\n").split("\t")
        rows.append((p, t.split("=", 1)[1], j.split("=", 1)[1]))
    return rows


def write_claims(form_rows, claimpath):
    with open(claimpath, "w") as f:
        for p, tname, jname in form_rows:
            t = TN.index(tname)
            f.write("%s\t%d\n" % (p, JMAP[t][jname]))


def run_supclaim(claimpath, rawpath):
    with open(rawpath, "w") as out:
        r = subprocess.run([SUP, claimpath], stdout=out, stderr=subprocess.STDOUT)
    if r.returncode != 0:
        raise SystemExit("support FAILED rc=%d on %s" % (r.returncode, claimpath))
    for line in open(rawpath):
        if line.startswith("error="):
            raise SystemExit("support error: " + line.strip())


def kv(line):
    return dict(x.split("=", 1) for x in line.strip().split(" ") if "=" in x)


def check_echo(form_rows, rawpath):
    """The extractor echoes judgment=; it must match the formation TSV."""
    raws = [kv(l) for l in open(rawpath) if l.strip()]
    assert len(raws) == len(form_rows), (len(raws), len(form_rows))
    for (p, tname, jname), r in zip(form_rows, raws):
        assert r["task"] == tname, (r["task"], tname)
        assert r["judgment"] == jname, (r["judgment"], jname)


def assemble_ledger(rawpath, ledpath):
    prev = "0" * 64
    n = 0
    with open(ledpath, "w") as fh:
        for line in open(rawpath):
            line = line.rstrip("\n")
            if not line.strip():
                continue
            content = line
            h = hashlib.sha256(bytes.fromhex(prev) + content.encode()).hexdigest()
            fh.write("%s hash=%s\n" % (content, h))
            prev = h
            n += 1
    return n


def verify_chain(ledpath, expect_n):
    prev = "0" * 64
    n = 0
    for raw in open(ledpath, "rb"):
        line = raw.rstrip(b"\n")
        if not line:
            continue
        i = line.rfind(b" hash=")
        assert i > 0, "no hash field at line %d" % n
        content, h = line[:i], line[i + 6:]
        calc = hashlib.sha256(bytes.fromhex(prev.decode()) + content).hexdigest()
        assert calc.encode() == h, "chain break at line %d" % n
        prev = h
        n += 1
    assert n == expect_n, (n, expect_n)
    return n


def job(tag, listpath):
    paths = [l.strip() for l in open(listpath) if l.strip()]
    n = len(paths)
    print("EVAL %s n=%d" % (tag, n), flush=True)
    stage = {}
    for rep in (1, 2):
        tsv = os.path.join(EV, "%s_formation_r%d.tsv" % (tag, rep))
        run_form(listpath, tsv)
        rows = parse_form_tsv(tsv)
        assert len(rows) == n and [r[0] for r in rows] == paths
        claim = os.path.join(EV, "%s_claim_r%d.tsv" % (tag, rep))
        write_claims(rows, claim)
        raw = os.path.join(EV, "%s_gate_raw_r%d.txt" % (tag, rep))
        run_supclaim(claim, raw)
        check_echo(rows, raw)
        led = os.path.join(EV, "%s_gate_r%d.ledger" % (tag, rep))
        m = assemble_ledger(raw, led)
        assert m == n
        verify_chain(led, n)
        stage[rep] = (tsv, claim, raw, led)
    for a, b, name in ((stage[1][0], stage[2][0], "formation TSV"),
                       (stage[1][2], stage[2][2], "gate raw"),
                       (stage[1][3], stage[2][3], "ledger")):
        assert sha(a) == sha(b), "%s MISMATCH %s" % (name, tag)
        print("  %s: %s IDENTICAL x2, chain OK" % (tag, name))
    return n


def main():
    os.makedirs(EV, exist_ok=True)
    for f in (FORM, SUP):
        assert os.path.isfile(f), "missing binary " + f
    job("adv", os.path.join(EV, "b_adv_e2b.list"))
    job("ctrl", os.path.join(EV, "b_ctrl_e2b.list"))
    print("EVAL-COMPLETE")


if __name__ == "__main__":
    main()
