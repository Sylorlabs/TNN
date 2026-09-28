#!/usr/bin/env python3
"""gen_cu.py — CU frozen admission-tape generator (glue, never the instrument).

Deterministic (zero RNG). Reads the three frozen sources pinned in
PREREG_CU.md, writes cu_tape.txt and cu_questions.txt.

Tape line: K|id|conf|mrgF|strong|agree|prov|prov_ok|decl_ok|auth|atk
  prov: 0=GEN,1=SELF,2=EXT ; auth: 0=none,1=valid,2=forged ; atk: 0,1=LAU,2=FORK,3=AUTH

Frozen bar (M1, hands-off): conf>=705 and mrgF>=3588 (ST=0,AT=0: strong/agree
arms disabled). See PREREG_CU.md Correction C1.
"""
import json, os, hashlib, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SWEEP = "/home/hatch/workspace/pam_round2/o1_delivery/sweep.jsonl"
INSTALL = "/home/hatch/workspace/pam_round2/d1_stack/rec_install.records"
GUARD = "/home/hatch/workspace/pam_round2/cc1_guard/prereg/gen_guard.py"

PIN = {
    SWEEP: "4163fffa65f18f552d48f7efec0e9800a7406547a27c6259d39a48ec7f0833f2",
    INSTALL: "c26ac9743b8c079e782cdf8511caf2350f653556ac11ac70dfda03720c17c4ad",
    GUARD: "49eef7b169790207dd53b140a3586144fe34a8b99a134e18d2244702ae2c214b",
}

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def bar_pass(conf, mrgF, strong, agree):
    return conf >= 705 and mrgF >= 3588

def main():
    for p, want in PIN.items():
        got = sha(p)
        assert got == want, (p, got, want)

    crows = []   # (id, conf, mrgF, strong, agree)
    nbar = 0
    for line in open(SWEEP):
        r = json.loads(line)
        if r["judgment"] == r["truth"] and r["conf"] >= 700:
            crows.append(("C-%d" % r["seq"], r["conf"], r["mrgF"], r["strong"], r["agree"]))
            if bar_pass(r["conf"], r["mrgF"], r["strong"], r["agree"]):
                nbar += 1
    assert len(crows) == 1102, len(crows)
    # all C rows are honest: prov=GEN(0), prov_ok=1, decl_ok=1, auth=0(none)
    tape = [("C", i, c, m, s, a, 0, 1, 1, 0, 0) for (i, c, m, s, a) in crows]

    wrows = []
    for line in open(INSTALL):
        f = line.rstrip("\n").split("|")
        seq = int(f[0])
        if 24 <= seq <= 35:
            assert f[5] == "RICH" and f[10] in ("DARK", "BRIGHT"), f
            wrows.append(("W-%d" % seq, int(f[6]), int(f[8]), 1, 1))
    assert len(wrows) == 12, len(wrows)
    for (i, c, m, s, a) in wrows:
        tape.append(("W", i, c, m, s, a, 0, 1, 1, 0, 0))

    cells = {}
    cur = None
    for ln in open(GUARD):
        s = ln.strip()
        mh = re.match(r'\("((?:CC1(?:-V\d+)?))", \[', s)
        if mh:
            cur = mh.group(1)
            cells[cur] = []
            continue
        if cur is not None:
            mt = re.match(r'\((-?\d+(?:,-?\d+){12})\),?\s*$', s)
            if mt:
                cells[cur].append(tuple(int(x) for x in mt.group(1).split(",")))
            elif s.startswith("],"):
                cur = None
    order = ["CC1"] + ["CC1-V%d" % i for i in range(1, 9)]
    npp = 0
    for pi, name in enumerate(order):
        tr = cells[name]
        assert len(tr) == 4, (name, len(tr))
        for ti in (2, 3):
            t = tr[ti]
            assert t[2] == 2 and t[7] == 3, (name, ti, t)
            tape.append(("P", "P%d-%d" % (pi, ti), t[3], t[6], 1, 1, 0, 1, 1, 0, 0))
            npp += 1
    assert npp == 18, npp

    # Attack rows: copies of bar-passing C rows in tape order, one security
    # field corrupted each. Attack ids distinct from C ids (no double count).
    src = [r for r in crows if bar_pass(r[1], r[2], r[3], r[4])]
    assert len(src) >= 100, len(src)
    arows = []
    for n, (i, c, m, s, a) in enumerate(src[:40]):
        arows.append(("A", "A-LAU-%d" % n, c, m, s, a, 0, 0, 1, 0, 1))   # GEN relabel, sig fails
    for n, (i, c, m, s, a) in enumerate(src[40:70]):
        arows.append(("A", "A-FORK-%d" % n, c, m, s, a, 0, 1, 0, 0, 2))  # forged declaration
    for n, (i, c, m, s, a) in enumerate(src[70:100]):
        arows.append(("A", "A-AUTH-%d" % n, c, m, s, a, 0, 1, 1, 2, 3))  # forged authority
    assert len(arows) == 100
    for r in arows:
        tape.append(r)

    assert len(tape) == 1232, len(tape)

    tp = os.path.join(HERE, "cu_tape.txt")
    with open(tp, "w") as f:
        for r in tape:
            f.write("|".join(str(x) for x in r) + "\n")

    # Questions: first 20 bar-passing C rows (tape order) + first 5 W rows (diagnostic)
    qrows = ["ASK|" + i for (i, c, m, s, a) in crows if bar_pass(c, m, s, a)][:20]
    assert len(qrows) == 20
    qdiag = ["ASK|" + i for (i, c, m, s, a) in wrows][:5]
    qp = os.path.join(HERE, "cu_questions.txt")
    with open(qp, "w") as f:
        for q in qrows + qdiag:
            f.write(q + "\n")

    print("tape rows=%d (C=%d W=%d P=%d A=%d) barpassing-C=%d sha=%s"
          % (len(tape), 1102, 12, 18, 100, nbar, sha(tp)))
    print("questions primary=%d diagnostic=%d sha=%s" % (len(qrows), len(qdiag), sha(qp)))

if __name__ == "__main__":
    main()
