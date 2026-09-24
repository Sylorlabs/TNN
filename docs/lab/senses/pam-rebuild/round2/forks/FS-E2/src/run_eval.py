#!/usr/bin/env python3
"""run_eval.py -- FS-E2 eval driver (glue only; gate decisions in frozen fse1 binary).

1. Runs the FROZEN FS-E1 binary (SHA-verified) in runlist mode on the
   in-scope fixture lists, TWICE each; byte-compares and hash-chain-verifies.
2. Emits deterministic hash-chained ABSTAIN ledgers for out-of-scope fixtures,
   TWICE each; byte-compares.
3. Runs the frozen gate on the 720 r2n pitchdisc normals (preregistered
   NON-GATING diagnostic), TWICE; byte-compares and hash-chain-verifies.

Usage: run_eval.py
Outputs under evidence/eval/.
"""
import subprocess, os, sys, hashlib, struct, re

HERE = os.path.dirname(os.path.abspath(__file__))
FORK = os.path.normpath(os.path.join(HERE, ".."))
EV = os.path.join(FORK, "evidence", "eval")
LISTS = os.path.join(EV, "lists")
BIN = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2/forks/FS-E1/build/fse1"
BIN_SHA = "21fc159c232d4b3e3acd57cfc933c55d71b4fa34c8cc9cd0fc1b33a0b80690a5"

# Phase-0 formation accuracy per abstained task (committed 28aa3938)
FORM_ACC = {"colorconst": "56.81", "shapetrans": "80.56", "timbredisc": "38.89"}

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

def check_binary():
    h = sha(BIN)
    assert h == BIN_SHA, "frozen gate binary SHA MISMATCH: %s" % h
    print("gate binary SHA OK: %s" % h[:16])

def run_gate(listpath, ledpath, sopath):
    with open(sopath, "w") as out:
        r = subprocess.run([BIN, "runlist", listpath, ledpath, "union"],
                           stdout=out, stderr=subprocess.STDOUT)
    if r.returncode != 0:
        raise SystemExit("gate FAILED rc=%d on %s" % (r.returncode, listpath))

def verify_chain(ledpath, expect_n):
    prev = b"0" * 64
    ln = 0
    for raw in open(ledpath, "rb"):
        line = raw.rstrip(b"\n")
        if not line:
            continue
        i = line.rfind(b" hash=")
        assert i > 0, "no hash field at line %d" % ln
        content, h = line[:i], line[i + 6:]
        calc = hashlib.sha256(bytes.fromhex(prev.decode()) + content).hexdigest()
        assert calc.encode() == h, "chain break at line %d" % ln
        prev = h
        ln += 1
    assert ln == expect_n, (ln, expect_n)
    return ln

def task_of(path):
    m = re.search(r"_(colordisc|colorconst|shapetrans|pitchdisc|timbredisc|motiondir)_",
                  path.split("/")[-1])
    return m.group(1)

def hdr_id(path):
    d = open(path, "rb").read(32)
    magic, task, index, fam = struct.unpack("<8I", d)[:4]
    assert magic == 0x52324658, path
    return "r2fx_t%d_i%d_f%d" % (task, index, fam)

def emit_abstain(listpath, ledpath):
    """Deterministic ABSTAIN ledger with hash chain (glue bookkeeping;
    the abstain decision is the frozen prereg scoping list)."""
    paths = [l.rstrip("\n") for l in open(listpath) if l.strip()]
    prev = "0" * 64
    with open(ledpath, "w") as fh:
        for p in paths:
            t = task_of(p)
            fid = hdr_id(p)
            content = ("fixture=%s task=%s scope=ABSTAIN "
                       "reason=formation_%s_below_85" % (fid, t, FORM_ACC[t]))
            h = hashlib.sha256(bytes.fromhex(prev) + content.encode()).hexdigest()
            fh.write("%s hash=%s\n" % (content, h))
            prev = h
    return len(paths)

def gate_job(tag, listpath):
    n = sum(1 for _ in open(listpath) if _.strip())
    print("GATE %s n=%d" % (tag, n), flush=True)
    outs = []
    for rep in (1, 2):
        led = os.path.join(EV, "%s_r%d.ledger" % (tag, rep))
        so = os.path.join(EV, "%s_r%d.stdout" % (tag, rep))
        run_gate(listpath, led, so)
        outs.append((led, so))
    assert sha(outs[0][0]) == sha(outs[1][0]), "ledger MISMATCH %s" % tag
    assert sha(outs[0][1]) == sha(outs[1][1]), "stdout MISMATCH %s" % tag
    verify_chain(outs[0][0], n)
    print("  %s: ledger+stdout IDENTICAL x2, chain OK (%d)" % (tag, n))

def abstain_job(tag, listpath):
    n = sum(1 for _ in open(listpath) if _.strip())
    print("ABSTAIN %s n=%d" % (tag, n), flush=True)
    outs = []
    for rep in (1, 2):
        led = os.path.join(EV, "%s_r%d.ledger" % (tag, rep))
        emit_abstain(listpath, led)
        outs.append(led)
    assert sha(outs[0]) == sha(outs[1]), "abstain ledger MISMATCH %s" % tag
    verify_chain(outs[0], n)
    print("  %s: IDENTICAL x2, chain OK (%d)" % (tag, n))

def main():
    os.makedirs(EV, exist_ok=True)
    check_binary()
    gate_job("batt_inscope_adv", os.path.join(LISTS, "b_adv_inscope.list"))
    gate_job("batt_inscope_ctrl", os.path.join(LISTS, "b_ctrl_inscope.list"))
    abstain_job("abstain_adv", os.path.join(LISTS, "b_adv_abstain.list"))
    abstain_job("abstain_ctrl", os.path.join(LISTS, "b_ctrl_abstain.list"))
    gate_job("batt_pitchdisc_diag",
             "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2/forks/FS-E2/evidence/phase0/lists/r2n_pitchdisc.list")
    print("EVAL-COMPLETE")

if __name__ == "__main__":
    main()
