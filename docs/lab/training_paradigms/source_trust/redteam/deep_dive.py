#!/usr/bin/env python3
"""Episode-level deep dives on wave-2 red-team ledgers.

Reads evidence/runs_<fork>_<stream>_a/<stream>.ledger (run a; run b is
byte-identical). Prints per-attack verdict tables for the report.
"""
import os, re, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
EVID = os.path.join(HERE, "evidence")
SAY_RE = re.compile(r"^ep=(\d+) et=1 src=(\d+) key=(\d+) val=(\d+) aux=(\d+) gt=(\d+) v=(\d+) w=(.*)$")
VN = {0: "INSTALL", 1: "WITHHOLD", 2: "REJECT"}

def load(fork, stream):
    p = os.path.join(EVID, "runs_%s_%s_a" % (fork, stream), stream + ".ledger")
    eps = []
    with open(p) as f:
        for line in f:
            m = SAY_RE.match(line.rstrip("\n"))
            if m:
                ep, src, key, val, aux, gt, v = (int(x) for x in m.groups()[:7])
                eps.append({"ep": ep, "src": src, "key": key, "val": val,
                            "aux": aux, "gt": gt, "v": v, "w": m.group(8)})
    return eps

def show(eps, title, filt=None, wmax=90):
    print("=" * 100)
    print(title)
    print("=" * 100)
    for e in eps:
        if filt and not filt(e):
            continue
        w = e["w"][:wmax]
        print("ep=%-4d aux=%d src=%-3d key=%-5d gt=%d v=%d %-9s w=%s" % (
            e["ep"], e["aux"], e["src"], e["key"], e["gt"], e["v"], VN[e["v"]], w))

def t_of(w):
    m = re.search(r"t=(\d+)", w)
    return m.group(1) if m else "?"

# ---------- 1. sleeper attack phase ----------
def sleeper():
    for fork in ("k", "l", "s", "sp"):
        eps = load(fork, "RT2-V4-sleeper")
        atk = [e for e in eps if e["aux"] == 2]
        inst = [e for e in atk if e["v"] == 0]
        print("fork=%s sleeper attack SAYs: %d installs / %d" % (fork, len(inst), len(atk)))
        # show first claim's 5 SAYs as the shape exemplar
        show(atk, "fork=%s sleeper: first false claim (5 SAYs)" % fork,
             filt=lambda e: e["key"] == 3201, wmax=70)
        # trust readings on L for the first attack SAY
        if fork == "l":
            e = atk[0]
            print("L first attack SAY warrant t=%s rule=%s" % (t_of(e["w"]), e["w"].split("rule=")[-1][:20]))

# ---------- 2. L-DOT phases ----------
def dot():
    eps = load("l", "L-DOT")
    # phase C: aux 3 = pre-taint, aux 4 = honest after pre-taint
    show(eps, "L-DOT phase C: pre-tainted truths (aux 3/4)", filt=lambda e: e["aux"] in (3, 4), wmax=80)
    show(eps, "L-DOT phase D: control truths, no pre-taint (aux 5)", filt=lambda e: e["aux"] == 5, wmax=80)
    show(eps, "L-DOT phase E: rescue by H2/H3 (aux 6)", filt=lambda e: e["aux"] == 6, wmax=80)
    for fork in ("k", "s"):
        e2 = load(fork, "L-DOT")
        c = [e for e in e2 if e["aux"] == 4]
        print("fork=%s phase-C honest truths: %d/%d installed" %
              (fork, sum(1 for e in c if e["v"] == 0), len(c)))

# ---------- 3. L-DES lie-by-lie ----------
def des():
    eps = load("l", "L-DES")
    lies = [e for e in eps if e["aux"] == 2]
    print("L-DES lies (aux=2):")
    for e in lies:
        print("  ep=%d src=%d key=%d gt=%d v=%d %-9s t=%s rule=%s" % (
            e["ep"], e["src"], e["key"], e["gt"], e["v"], VN[e["v"]],
            t_of(e["w"]), e["w"].split("rule=")[-1][:24]))
    probes = [e for e in eps if e["aux"] == 3]
    print("L-DES probes (aux=3, novel truths reading trust):")
    for e in probes:
        print("  ep=%d key=%d v=%d %-9s t=%s" % (e["ep"], e["key"], e["v"], VN[e["v"]], t_of(e["w"])))
    corr = [e for e in eps if e["aux"] == 4]
    print("L-DES corrections (aux=4):")
    for e in corr:
        print("  ep=%d key=%d v=%d %-9s t=%s" % (e["ep"], e["key"], e["v"], VN[e["v"]], t_of(e["w"])))

# ---------- 4. L-FRM frame-by-frame ----------
def frm():
    for fork in ("k", "l", "s"):
        eps = load(fork, "L-FRM")
        print("=" * 100)
        print("L-FRM fork=%s: forged episodes + H's genuine truths around frames" % fork)
        show(eps, "", filt=lambda e: e["aux"] in (2, 3, 4, 5) and e["key"] >= 7101, wmax=75)
    # L trust readings
    eps = load("l", "L-FRM")
    for e in eps:
        if e["aux"] in (2, 3, 4) and e["key"] in (7101, 7102, 7130, 7131):
            print("L ep=%d aux=%d key=%d v=%d t=%s %s" % (
                e["ep"], e["aux"], e["key"], e["v"], t_of(e["w"]), e["w"].split("rule=")[-1][:24]))

# ---------- 5. CROSS per-phase ----------
def cross():
    # phase ep ranges (SAY episodes; derived from generator order)
    eps = load("k", "CROSS")
    phases = {
        "P0 honest baseline": lambda e: e["ep"] <= 50,
        "P1 sybil (51-54, keys 6101-6103)": lambda e: 6101 <= e["key"] <= 6103,
        "P2 betrayal (B=4)": lambda e: e["src"] == 4 and e["key"] >= 6301,
        "P3 laundering (X=55,T=5)": lambda e: e["src"] in (55, 5) and e["key"] in (6391, 6401),
        "P4 drip (D=6, keys 6511+)": lambda e: e["src"] == 6 and e["key"] >= 6511,
    }
    for pname, f in phases.items():
        print("-" * 100)
        print(pname)
        for fork in ("k", "l", "s"):
            e2 = load(fork, "CROSS")
            sel = [e for e in e2 if f(e) and e["aux"] in (2, 3, 4, 5)]
            inst = [e["ep"] for e in sel if e["v"] == 0 and e["gt"] == 0]
            flag = [e for e in sel if e["v"] != 0 and e["gt"] == 0]
            first_warn = flag[0]["ep"] if flag else None
            print("  fork=%s attack SAYs=%d installs=%s first_warning_ep=%s" %
                  (fork, len(sel), inst, first_warn))
            if flag:
                w = flag[0]["w"][:110]
                print("    first warning warrant: %s" % w)

# ---------- 6. S' probe detail ----------
def probe():
    e_sp = load("sp", "ST-1")
    ctrl = [e for e in e_sp if e["aux"] == 20]
    print("S' ST-1: false installs=%d/80, honest controls: %d/20 installed, %d withheld" % (
        sum(1 for e in e_sp if e["gt"] == 0 and e["v"] == 0),
        sum(1 for e in ctrl if e["v"] == 0),
        sum(1 for e in ctrl if e["v"] == 1)))
    show(e_sp, "S' ST-1 withheld honest controls", filt=lambda e: e["aux"] == 20 and e["v"] != 0, wmax=100)
    e6 = load("sp", "ST-6")
    print("S' ST-6: truth installs=%d/160, withholds=%d" % (
        sum(1 for e in e6 if e["gt"] == 1 and e["v"] == 0),
        sum(1 for e in e6 if e["gt"] == 1 and e["v"] == 1)))
    show(e6, "S' ST-6 withheld truths (first 8)", filt=lambda e: e["gt"] == 1 and e["v"] != 0, wmax=100)
    # S on ST-1 for the baseline comparison (from battery runs? not run; use wave-1 claim)
    e_t2 = load("sp", "RT-T2")
    print("S' RT-T2 installs: %d/25" % sum(1 for e in e_t2 if e["v"] == 0))

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all", "sleeper"):
        sleeper()
    if which in ("all", "dot"):
        dot()
    if which in ("all", "des"):
        des()
    if which in ("all", "frm"):
        frm()
    if which in ("all", "cross"):
        cross()
    if which in ("all", "probe"):
        probe()
