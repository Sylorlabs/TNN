#!/usr/bin/env python3
"""D2 scorer: parses d2bin RESULT/TRACE lines, applies spec §6 criteria.
Usage: score_d2.py <scenarios_dir> <policy>  -> per-scenario PASS/FAIL + summary.
Also: score_d2.py --check <scenarios_dir>   -> runs the §10 reference gate.
"""
import subprocess, sys, os, re, hashlib

D2BIN = os.path.expanduser("~/workspace/composition_d2_rerun/d2build/d2bin")

def parse_scen(path):
    """Extract template, k, ep, storms from a scenario file."""
    txt = open(path).read()
    m = re.search(r"# phase=(\w+) template=(\w+) k=(\d+)", txt)
    phase, template, k = m.group(1), m.group(2), int(m.group(3))
    ep = int(re.search(r"# EPISODE (\d+)", txt).group(1))
    storms = [int(x) for x in re.search(r"# storms=([\d,]+)", txt).group(1).split(",")]
    return {"phase": phase, "template": template, "k": k, "ep": ep,
            "storms": storms, "path": path}

def run_episode(scen_path, policy):
    out = subprocess.run([D2BIN, "run", scen_path, policy],
                         capture_output=True, text=True, timeout=120).stdout
    lines = out.strip().split("\n")
    res = lines[0].split()
    # RESULT <policy> <ticks> <cause> <finalE> <nEat> <nCombine> <wastedEat> <wardTick> <unmitig> <invalid>
    assert res[0] == "RESULT", out[:200]
    vals = {
        "policy": res[1], "ticks": int(res[2]), "cause": int(res[3]),
        "finalE": int(res[4]), "nEat": int(res[5]), "nCombine": int(res[6]),
        "wastedEat": int(res[7]), "wardTick": int(res[8]),
        "unmitig": int(res[9]), "invalid": int(res[10]),
    }
    trace = lines[1].split()[1]
    vals["trace"] = trace
    return vals

def check_criteria(scen, r):
    """Apply spec §6 criteria. Returns (pass: bool, reasons: list)."""
    t, ep, s = scen["template"], scen["ep"], scen["storms"]
    reasons = []
    ok = True
    def need(cond, msg):
        nonlocal ok
        if not cond:
            ok = False
            reasons.append(msg)
    # invalid replies: 3+ = FAIL (§5)
    need(r["invalid"] < 3, f"invalid_replies={r['invalid']}>=3")
    # alive at end
    need(r["cause"] == 0 and r["ticks"] == ep, f"not_alive(cause={r['cause']},ticks={r['ticks']}/{ep})")
    # no void entry: cause!=2 (void death). cause 0=alive implies no void entry.
    need(r["cause"] != 2, "void_entry")
    if t == "F":
        need(r["nEat"] >= 4, f"nEat={r['nEat']}<4")
        need(r["wastedEat"] == 0, f"wastedEat={r['wastedEat']}")
    elif t == "W":
        need(r["wardTick"] >= 0 and r["wardTick"] < 60, f"wardTick={r['wardTick']} not <60")
        need(r["unmitig"] == 0, f"unmitig={r['unmitig']}")
        need(r["nCombine"] >= 1, f"nCombine={r['nCombine']}<1")
    elif t == "T":
        # unmitigated during [150,180): our unmitig counts all ticks; storms only
        # exist at 150,350,550 and ep=200, so unmitig>0 implies failure in window.
        need(r["unmitig"] == 0, f"unmitig={r['unmitig']}")
        need(r["nEat"] >= 4, f"nEat={r['nEat']}<4")
    elif t == "FW":
        need(r["unmitig"] == 0, f"unmitig={r['unmitig']}")
        need(r["wardTick"] >= 0 and r["wardTick"] < s[0], f"wardTick={r['wardTick']} not <{s[0]}")
        need(r["nEat"] >= 4, f"nEat={r['nEat']}<4")
        need(r["finalE"] >= 40, f"finalE={r['finalE']}<40")
    elif t == "WF":
        need(r["unmitig"] == 0, f"unmitig={r['unmitig']}")
        need(r["wardTick"] >= 0 and r["wardTick"] < 30, f"wardTick={r['wardTick']} not <30")
        need(r["nEat"] >= 4, f"nEat={r['nEat']}<4")
        need(r["finalE"] >= 40, f"finalE={r['finalE']}<40")
    elif t == "FWF":
        need(r["unmitig"] == 0, f"unmitig={r['unmitig']}")
        need(r["wardTick"] >= 0 and r["wardTick"] < 60, f"wardTick={r['wardTick']} not <60")
        need(r["nEat"] >= 7, f"nEat={r['nEat']}<7")
        need(r["finalE"] >= 30, f"finalE={r['finalE']}<30")
    elif t == "N":
        need(r["trace"] == "6" * ep, f"trace_not_all_wait(len={len(r['trace'])})")
    else:
        raise ValueError(t)
    return ok, reasons

def scen_files(sdir):
    return sorted(f for f in os.listdir(sdir)
                  if re.match(r"^(F|W|T|FW|WF|FWF|N)-\d+\.txt$", f))

def main():
    if len(sys.argv) == 4 and sys.argv[1] == "--policy":
        # single: --policy <dir> <policyname>
        sdir, policy = sys.argv[2], sys.argv[3]
        files = scen_files(sdir)
        npass = 0
        for fn in files:
            scen = parse_scen(os.path.join(sdir, fn))
            r = run_episode(scen["path"], policy)
            ok, reasons = check_criteria(scen, r)
            npass += ok
            print(f"{fn}: {'PASS' if ok else 'FAIL'} " + (";".join(reasons) if reasons else ""))
        print(f"SUMMARY {policy}: {npass}/{len(files)}")
    elif len(sys.argv) == 3 and sys.argv[1] == "--check":
        sdir = sys.argv[2]
        gate(sdir)
    else:
        print(__doc__); sys.exit(2)

def gate(sdir):
    """Spec §10 reference-validation gate."""
    files = scen_files(sdir)
    scens = [parse_scen(os.path.join(sdir, f)) for f in files]
    by_phase = {}
    for s in scens:
        by_phase.setdefault(s["phase"], []).append(s)
    results = {}  # (policy, fn) -> (ok, reasons, r)
    def runpol(policy, wanted):
        for s in wanted:
            fn = os.path.basename(s["path"])
            r = run_episode(s["path"], policy)
            ok, reasons = check_criteria(s, r)
            results[(policy, fn)] = (ok, reasons, r)
    P0, P2, P3 = by_phase["P0"], by_phase["P2"], by_phase["P3"]
    print("== §10 reference gate ==")
    # 1. refok passes every P0 and every P2, and every P3
    runpol("refok", P0 + P2 + P3)
    fails = [fn for (p, fn), (ok, _, _) in results.items() if p == "refok" and not ok]
    # P3 for refok: refok will NOT pass P3 (it moves). The gate says "REF-OK must
    # pass every P0 and P2" — P3 is for the all-WAIT check. refok is not expected
    # to pass P3. Let me check the spec...
    print(f"refok P0: {sum(1 for s in P0 if results[('refok', os.path.basename(s['path']))][0])}/{len(P0)}")
    print(f"refok P2: {sum(1 for s in P2 if results[('refok', os.path.basename(s['path']))][0])}/{len(P2)}")
    # 2. chance arms fail every P2
    for pol in ("null", "singlerule", "wrongorder"):
        runpol(pol, P2)
        npass = sum(1 for s in P2 if results[(pol, os.path.basename(s["path"]))][0])
        print(f"{pol} P2 passes: {npass}/{len(P2)} (must be 0)")
    # 3. refnomaster P2 -> (a): check its P0-S1
    runpol("refnomaster", P0 + P2)
    for s in P0:
        if s["template"] == "F":
            fn = os.path.basename(s["path"])
            ok, reasons, r = results[("refnomaster", fn)]
            print(f"refnomaster {fn}: {'PASS' if ok else 'FAIL'} nEat={r['nEat']} " + ";".join(reasons))
    # 4. refnocombine/refnoretrieve P2: must fail WARD-placed
    runpol("refnocombine", P2)
    for s in P2:
        fn = os.path.basename(s["path"])
        ok, reasons, r = results[("refnocombine", fn)]
        if ok:
            print(f"UNEXPECTED PASS refnocombine {fn}")
    print(f"refnocombine P2 passes: {sum(1 for s in P2 if results[('refnocombine', os.path.basename(s['path']))][0])}/{len(P2)} (must be 0)")
    # 5. reflex P3: must deviate from all-WAIT
    runpol("reflex", P3)
    for s in P3:
        fn = os.path.basename(s["path"])
        ok, reasons, r = results[("reflex", fn)]
        print(f"reflex {fn}: {'PASS' if ok else 'FAIL'} (P3 expects FAIL=all-wait holds; reflex must deviate)")
    # 6. refinterfere P2: FW pass, WF fail
    runpol("refinterfere", P2)
    for s in P2:
        fn = os.path.basename(s["path"])
        ok, reasons, r = results[("refinterfere", fn)]
        print(f"refinterfere {fn}: {'PASS' if ok else 'FAIL'}")

if __name__ == "__main__":
    main()
