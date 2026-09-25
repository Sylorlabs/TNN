#!/usr/bin/env python3
"""MATH R2 head-to-head evaluation runner.
Runs formal batteries for all engines with 3x byte-identical verification.
CWD for engines: ~/workspace/tnn-lab/math_logic (STORE: paths resolve).
"""
import os, sys, subprocess, hashlib, time, json, re

BASE = "/home/hatch/workspace/tnn-lab/math_logic"
R1 = "/home/hatch/workspace/math_r2/r1/problems"
BIN = "/home/hatch/workspace/math_r2/eval/bin"
OUT = "/home/hatch/workspace/math_r2/eval/out"
os.makedirs(OUT, exist_ok=True)

def sealed(path):
    d = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"): continue
            pid, v = line.split(":")
            d[pid.strip()] = v.strip()
    return d

SEAL_B2 = sealed(f"{BASE}/problems/sealed/SEALED_B2.sol")
SEAL_B2["B2_07"] = "WITHHELD"  # CORRECTED: hand-verified underivable; all 5 engines withhold; sealed DERIVED is wrong (finding F-SEAL-01)
SEAL_B3 = sealed(f"{BASE}/problems/sealed/SEALED_B3.sol")
SEAL_B4 = sealed(f"{BASE}/problems/sealed/SEALED_B4.sol")
SEAL_B4X = sealed(f"{BASE}/round2/batteries/sealed/SEALED_B4X.sol")
SEAL_B5X = sealed(f"{BASE}/round2/batteries/sealed/SEALED_B5X.sol")
SEAL_B6X = sealed(f"{BASE}/round2/batteries/sealed/SEALED_B6X.sol")

BATTERIES = {
    "B2R": ([f"{R1}/b2/B2_{i:02d}.form" for i in range(1, 13)], SEAL_B2, 8),
    "B3R": ([f"{R1}/b3/B3_{i:02d}.form" for i in range(1, 11)], SEAL_B3, 8),
    "B4R": ([f"{R1}/b4/B4_{i:02d}.form" for i in range(1, 16)], SEAL_B4, 8),
    "B4X": ([f"{BASE}/round2/batteries/b4x/B4X_{i:02d}.form" for i in range(1, 16)], SEAL_B4X, 8),
    "B5X": ([f"{BASE}/round2/batteries/b5x/B5X_L{lvl}_{i:02d}.form" for lvl in [2, 3, 4] for i in range(1, 21)], SEAL_B5X, 8),
    "B6X": ([f"{BASE}/round2/batteries/b6x/B6X_{i:02d}.form" for i in range(1, 4)], SEAL_B6X, 128),
}

# engine -> (binary, bound_arg_template); {prob} {out} {bound}
ENGINES = {
    "ONE-R1":   (f"{BIN}/one_bin",      "{bin} {prob} {out}"),
    "DUAL-R1":  (f"{BIN}/dual_bin",     "{bin} {prob} {out}"),
    "HYB":      (f"{BIN}/hyb_bin",      "{bin} {prob} {out}"),
    "REF-FIRST":(f"{BIN}/reffirst_bin", "{bin} {prob} {out} {bound}"),
    "NFEE":     (f"{BIN}/nfee_bin",     "{bin} {prob} {out} {bound}"),
    # LEARN-FORM formal path = byte-identical ONE core (build-verified); uses one_bin
    "LEARN-FORM": (f"{BIN}/one_bin",    "{bin} {prob} {out}"),
}
B6X_BIN = {"ONE-R1": f"{BIN}/one_b6x_bin", "DUAL-R1": f"{BIN}/dual_b6x_bin",
           "HYB": f"{BIN}/hyb_b6x_bin", "LEARN-FORM": f"{BIN}/one_b6x_bin"}

def parse_out(path):
    with open(path, "rb") as f: data = f.read()
    txt = data.decode("utf-8", errors="replace")
    v = re.search(r"^VERDICT:\s*(\S+)", txt, re.M)
    c = re.search(r"^CONFIDENCE:\s*(\S+)", txt, re.M)
    d = re.search(r"^DERIVATIONS:\s*(\S+)", txt, re.M)
    return (v.group(1) if v else "NO_VERDICT",
            c.group(1) if c else "?",
            d.group(1) if d else "?",
            hashlib.sha256(data).hexdigest())

def verdict_class(v):
    if v in ("DERIVED", "DERIVED-WEIGHED"): return "derived"
    if v in ("REFUTED", "REFUTED-WEIGHED"): return "refuted"
    return "withheld"  # WITHHELD, UNSUPPORTED, CONTESTED, FORMALIZE-ABSTAIN, NO_VERDICT

def run_once(cmd, timeout):
    t0 = time.time()
    p = subprocess.run(cmd, shell=True, cwd=BASE, capture_output=True, timeout=timeout)
    return time.time() - t0, p.returncode

def main():
    only = sys.argv[1:]  # optional battery filter
    results = {}
    for bname, (probs, sealed, bound) in BATTERIES.items():
        if only and bname not in only: continue
        print(f"=== {bname} ({len(probs)} problems, bound {bound}) ===", flush=True)
        results[bname] = {}
        for ename, (binary, tmpl) in ENGINES.items():
            ebin = B6X_BIN.get(ename, binary) if bname == "B6X" else binary
            erec = {"problems": {}, "divergent": []}
            for prob in probs:
                pid = os.path.basename(prob).replace(".form", "")
                outbase = f"{OUT}/{bname}_{ename}_{pid}"
                shas, wall = [], 0.0
                ok = True
                for r in range(3):
                    outp = f"{outbase}.r{r}"
                    cmd = tmpl.format(bin=ebin, prob=prob, out=outp, bound=bound)
                    try:
                        dt, rc = run_once(cmd, timeout=600)
                    except subprocess.TimeoutExpired:
                        ok = False; erec["problems"][pid] = {"status": "TIMEOUT"}; break
                    wall += dt
                    if rc != 0 or not os.path.exists(outp):
                        ok = False; erec["problems"][pid] = {"status": f"EXIT_{rc}"}; break
                    with open(outp, "rb") as f: shas.append(hashlib.sha256(f.read()).hexdigest())
                if not ok: continue
                if not (shas[0] == shas[1] == shas[2]):
                    erec["divergent"].append(pid)
                    erec["problems"][pid] = {"status": "DIVERGENT", "shas": shas}
                    continue
                v, c, d, sha = parse_out(f"{outbase}.r0")
                vc = verdict_class(v)
                sv = sealed.get(pid, "?")
                svc = verdict_class(sv)
                solved = (vc == "derived" and svc == "derived") or (vc == "withheld" and svc == "withheld")
                # refuted counts as incorrect unless sealed says refuted (never in these batteries)
                incorrect = not solved
                erec["problems"][pid] = {
                    "status": "ok", "verdict": v, "vclass": vc, "sealed": sv,
                    "solved": solved, "incorrect": incorrect,
                    "confidence": c, "derivations": d, "sha": sha, "wall_s": round(wall, 3),
                }
            # aggregate
            ps = [p for p in erec["problems"].values() if p.get("status") == "ok"]
            erec["agg"] = {
                "n": len(ps),
                "solved": sum(1 for p in ps if p["solved"]),
                "incorrect": sum(1 for p in ps if p["incorrect"]),
                "withheld_correct": sum(1 for p in ps if p["vclass"] == "withheld" and p["solved"]),
                "false_derived": sum(1 for p in ps if p["vclass"] == "derived" and not p["solved"]),
                "false_withheld": sum(1 for p in ps if p["vclass"] == "withheld" and not p["solved"]),
                "divergent": len(erec["divergent"]),
                "timeouts": sum(1 for p in erec["problems"].values() if p.get("status") == "TIMEOUT"),
                "wall_total_s": round(sum(p["wall_s"] for p in ps), 1),
            }
            a = erec["agg"]
            print(f"  {ename}: solved {a['solved']}/{a['n']}, incorrect {a['incorrect']} "
                  f"(false_derived {a['false_derived']}, false_withheld {a['false_withheld']}), "
                  f"divergent {a['divergent']}, wall {a['wall_total_s']}s", flush=True)
            results[bname][ename] = erec
    with open(f"{OUT}/../results_formal.json", "w") as f:
        json.dump(results, f, indent=1)
    print("wrote results_formal.json")

if __name__ == "__main__":
    main()
