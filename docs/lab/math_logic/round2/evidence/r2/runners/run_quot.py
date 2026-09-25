#!/usr/bin/env python3
"""MATH R2 QUOT battery runner.
Same protocol as run_battery.py (3x byte-identical reruns, sealed guard is
in-binary, per-problem verdicts vs sealed solutions), but QUOT only.
Writes to out_quot/ and results_formal_quot.json (never touches the frozen
results_formal.json from the main eval).
CWD for engines: ~/workspace/tnn-lab/math_logic (STORE: paths resolve).
"""
import os, sys, subprocess, hashlib, time, json, re, signal

BASE = "/home/hatch/workspace/tnn-lab/math_logic"
R1 = "/home/hatch/workspace/math_r2/r1/problems"
QUOT = "/home/hatch/workspace/math_r2/eval/bin/quot_bin"
OUT = "/home/hatch/workspace/math_r2/eval/out_quot"
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
SEAL_B2["B2_07"] = "WITHHELD"  # CORRECTED (F-SEAL-01, same as eval)
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

def parse_out(path):
    with open(path, "rb") as f: data = f.read()
    txt = data.decode("utf-8", errors="replace")
    v = re.search(r"^verdict:\s*(\S+)", txt, re.M)
    d = re.search(r"^committed:\s*(\S+)", txt, re.M)
    return (v.group(1) if v else "NO_VERDICT",
            d.group(1) if d else "?",
            hashlib.sha256(data).hexdigest())

def verdict_class(v):
    if v in ("DERIVED", "DERIVED-WEIGHED"): return "derived"
    if v in ("REFUTED", "REFUTED-WEIGHED"): return "refuted"
    return "withheld"  # WITHHELD, UNSUPPORTED, CONTESTED, FORMALIZE-ABSTAIN, NO_VERDICT

def run_once(cmd, timeout):
    # New process session so a timeout kills the whole tree (shell + quot_bin),
    # never leaving orphaned engine processes to distort later wall times.
    t0 = time.time()
    p = subprocess.Popen(cmd, shell=True, cwd=BASE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, start_new_session=True)
    try:
        p.wait(timeout=timeout)
        return time.time() - t0, p.returncode
    except subprocess.TimeoutExpired:
        os.killpg(p.pid, signal.SIGKILL)
        p.wait()
        raise subprocess.TimeoutExpired(cmd, timeout)

def main():
    only = sys.argv[1:]  # optional battery filter
    results = {"engine": "QUOT", "binary": QUOT,
               "binary_sha256": hashlib.sha256(open(QUOT, "rb").read()).hexdigest()}
    for bname, (probs, sealed_, bound) in BATTERIES.items():
        if only and bname not in only: continue
        print(f"=== {bname} ({len(probs)} problems, bound {bound}) ===", flush=True)
        erec = {"problems": {}, "divergent": []}
        for prob in probs:
            pid = os.path.basename(prob).replace(".form", "")
            outbase = f"{OUT}/{bname}_QUOT_{pid}"
            shas, wall = [], 0.0
            ok = True
            for r in range(3):
                outp = f"{outbase}.r{r}"
                cmd = f"{QUOT} {prob} {outp}"
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
            v, d, sha = parse_out(f"{outbase}.r0")
            vc = verdict_class(v)
            sv = sealed_.get(pid, "?")
            svc = verdict_class(sv)
            solved = (vc == svc)
            erec["problems"][pid] = {
                "status": "ok", "verdict": v, "vclass": vc, "sealed": sv,
                "solved": solved, "incorrect": not solved,
                "committed": d, "sha": sha, "wall_s": round(wall, 3),
            }
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
        print(f"  QUOT: solved {a['solved']}/{a['n']}, incorrect {a['incorrect']} "
              f"(false_derived {a['false_derived']}, false_withheld {a['false_withheld']}), "
              f"divergent {a['divergent']}, timeouts {a['timeouts']}, wall {a['wall_total_s']}s", flush=True)
        results[bname] = erec
    with open("/home/hatch/workspace/math_r2/eval/results_formal_quot.json", "w") as f:
        json.dump(results, f, indent=1)
    print("wrote results_formal_quot.json")

if __name__ == "__main__":
    main()
