#!/usr/bin/env python3
"""Wave-2 red-team runner.

For each (fork, stream): run the fork binary twice from fresh directories,
verify byte-identical ledgers (KB-4 discipline), then analyze verdicts.

Forks: k, l, s (frozen) + sp (S' probe, clearly separated).
Streams live in redteam/streams/ (+ battery streams for the S' probe).
Evidence: redteam/evidence/runs_<fork>_<stream>_{a,b}/ + analysis.json.
"""
import os, re, sys, json, shutil, subprocess, filecmp

HERE = os.path.dirname(os.path.abspath(__file__))
BAT = os.path.join(HERE, "..", "battery")
EVID = os.path.join(HERE, "evidence")

BINS = {
    "k": os.path.join(BAT, "build_k", "bin_k"),
    "l": os.path.join(BAT, "build_l", "bin_l"),
    "s": os.path.join(BAT, "build_s", "bin_s"),
    "sp": os.path.join(BAT, "build_sp", "bin_sp"),
}

RT_STREAMS = ["RT2-V1-ring12", "RT2-V2-ring4", "RT2-V3-stagger",
              "RT2-V4-sleeper", "RT2-V5-onekey",
              "L-DOT", "L-DES", "L-FRM", "CROSS"]
# (stream, stream_dir, [forks])
PLAN = ([(s, os.path.join(HERE, "streams"), ["k", "l", "s"]) for s in RT_STREAMS]
        + [("RT-T2", os.path.join(BAT, "streams"), ["sp"]),
           ("RT2-V4-sleeper", os.path.join(HERE, "streams"), ["sp"]),
           ("ST-1", os.path.join(BAT, "streams"), ["sp"]),
           ("ST-6", os.path.join(BAT, "streams"), ["sp"])])

SAY_RE = re.compile(r"^ep=(\d+) et=1 src=(\d+) key=(\d+) val=(\d+) aux=(\d+) gt=(\d+) v=(\d+) w=(.*)$")

def run_pair(fork, stream, sdir):
    bbin = BINS[fork]
    assert os.path.exists(bbin), "missing binary " + bbin
    sp = os.path.abspath(os.path.join(sdir, stream + ".txt"))
    assert os.path.exists(sp), "missing stream " + sp
    ledgers = []
    for run in ("a", "b"):
        rdir = os.path.join(EVID, "runs_%s_%s_%s" % (fork, stream, run))
        if os.path.exists(rdir):
            shutil.rmtree(rdir)
        os.makedirs(rdir)
        lp = os.path.join(rdir, stream + ".ledger")
        cp = os.path.join(rdir, stream + ".cost")
        r = subprocess.run([bbin, sp, lp, cp, fork],
                           capture_output=True, text=True)
        if r.returncode != 0:
            print("RUN FAILED fork=%s stream=%s run=%s" % (fork, stream, run))
            print(r.stdout[-2000:])
            print(r.stderr[-2000:], file=sys.stderr)
            sys.exit(1)
        ledgers.append(lp)
    same = filecmp.cmp(ledgers[0], ledgers[1], shallow=False)
    print("fork=%-2s stream=%-16s byte-identical=%s" % (fork, stream, same))
    if not same:
        print("BYTE-IDENTITY FAILURE", file=sys.stderr)
        sys.exit(1)
    return ledgers[0]

def parse_ledger(path):
    eps = []
    with open(path) as f:
        for line in f:
            m = SAY_RE.match(line.rstrip("\n"))
            if m:
                ep, src, key, val, aux, gt, v = (int(x) for x in m.groups()[:7])
                eps.append({"ep": ep, "src": src, "key": key, "val": val,
                            "aux": aux, "gt": gt, "v": v, "w": m.group(8)})
    return eps

def analyze(fork, stream, ledger):
    eps = parse_ledger(ledger)
    false_inst = [e["ep"] for e in eps if e["gt"] == 0 and e["v"] == 0]
    truth_inst = [e["ep"] for e in eps if e["gt"] == 1 and e["v"] == 0]
    truth_with = [e["ep"] for e in eps if e["gt"] == 1 and e["v"] == 1]
    truth_rej = [e["ep"] for e in eps if e["gt"] == 1 and e["v"] == 2]
    n_say = len(eps)
    return {
        "fork": fork, "stream": stream, "n_say": n_say,
        "v0": sum(1 for e in eps if e["v"] == 0),
        "v1": sum(1 for e in eps if e["v"] == 1),
        "v2": sum(1 for e in eps if e["v"] == 2),
        "false_installs": len(false_inst), "false_install_eps": false_inst,
        "truth_installs": len(truth_inst), "truth_withholds": len(truth_with),
        "truth_rejects": len(truth_rej), "truth_withhold_eps": truth_with,
        "n_gt0": sum(1 for e in eps if e["gt"] == 0),
        "n_gt1": sum(1 for e in eps if e["gt"] == 1),
    }

def main():
    os.makedirs(EVID, exist_ok=True)
    results = {}
    for stream, sdir, forks in PLAN:
        for fork in forks:
            ledger = run_pair(fork, stream, sdir)
            key = "%s/%s" % (fork, stream)
            results[key] = analyze(fork, stream, ledger)
            r = results[key]
            print("  -> say=%d v0=%d v1=%d v2=%d | false_inst=%d/%d truth_inst=%d/%d truth_with=%d" % (
                r["n_say"], r["v0"], r["v1"], r["v2"], r["false_installs"], r["n_gt0"],
                r["truth_installs"], r["n_gt1"], r["truth_withholds"]))
    ap = os.path.join(EVID, "analysis.json")
    json.dump(results, open(ap, "w"), indent=1)
    print("wrote", ap)

if __name__ == "__main__":
    main()
