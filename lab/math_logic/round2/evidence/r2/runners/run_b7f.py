#!/usr/bin/env python3
"""B7F formalization battery: LEARN-FORM NL->formalize, score vs sealed analogs.
Also builds the CURATED baseline (mechanical round-1 human choices, no learning).
"""
import os, subprocess, re, sys

BASE = "/home/hatch/workspace/tnn-lab/math_logic"
BIN = "/home/hatch/workspace/math_r2/eval/bin"
EV = "/home/hatch/workspace/math_r2/eval"
NLDIR = f"{EV}/b7f_nl"
OUT = f"{EV}/out"
os.makedirs(OUT, exist_ok=True)
os.makedirs(f"{EV}/b7f_forms", exist_ok=True)

STORE = f"{BASE}/round2/engines/learnform/FORMALIZER_STORE"
KB = f"{BASE}/round2/batteries/knowledge/KB_B7F.md"
CHECKER = f"{BASE}/round2/batteries/b7f_checker.py"
SEALED_FORM = f"{BASE}/round2/batteries/sealed/SEALED_B7F_FORM.sol"

def run_lf(pid):
    nl = f"{NLDIR}/{pid}.txt"
    out = f"{OUT}/B7F_LEARN-FORM_{pid}.out"
    form_out = None
    for r in range(3):
        o = f"{out}.r{r}"
        p = subprocess.run([f"{BIN}/learnform_bin", "solve", nl, STORE, KB, o],
                           cwd=BASE, capture_output=True, timeout=300)
        if p.returncode != 0:
            return {"pid": pid, "status": f"EXIT_{p.returncode}", "score": 0}
    # byte-compare (normalize the FORMAL_FORM output-path line, which embeds
    # the per-run output filename; the semantic content is what must be identical)
    import hashlib, re
    def norm(p):
        with open(p, "rb") as f: t = f.read().decode("utf-8", errors="replace")
        t = re.sub(r"^FORMAL_FORM:\s*\S+", "FORMAL_FORM: <out>", t, flags=re.M)
        return hashlib.sha256(t.encode()).hexdigest()
    hs = [norm(f"{out}.r{r}") for r in range(3)]
    if not (hs[0] == hs[1] == hs[2]):
        return {"pid": pid, "status": "DIVERGENT", "score": 0}
    with open(f"{out}.r0") as f: txt = f.read()
    m = re.search(r"^VERDICT:\s*(\S+)", txt, re.M)
    verdict = m.group(1) if m else "?"
    fm = re.search(r"^FORMAL_FORM:\s*(\S+)", txt, re.M)
    score = 0
    sub = ""
    if fm and os.path.exists(fm.group(1)):
        # copy to a stable .form (checker needs ID matching sealed IDs)
        with open(fm.group(1)) as f: ftext = f.read()
        # rewrite ID to the B7F pid so the checker aligns blocks
        ftext2 = re.sub(r"^ID:\s*\S+", f"ID: {pid}", ftext, count=1, flags=re.M)
        pf = f"{EV}/b7f_forms/{pid}.form"
        with open(pf, "w") as f: f.write(ftext2)
        cp = subprocess.run(["python3", CHECKER, SEALED_FORM, pf],
                            capture_output=True, text=True, cwd=os.path.dirname(CHECKER))
        # checker prints numeric subscores only
        sub = cp.stdout.strip().replace("\n", " | ")
        nums = re.findall(r"(\d+(?:\.\d+)?)", cp.stdout)
        if nums: score = float(nums[-1])
    return {"pid": pid, "status": "ok", "verdict": verdict, "score": score,
            "subscores": sub, "sha": hs[0]}

def main():
    import json
    pids = [f"B7F_{i:02d}" for i in range(1, 21)]
    res = {}
    for pid in pids:
        r = run_lf(pid)
        res[pid] = r
        print(f"{pid}: {r['status']} verdict={r.get('verdict','?')} score={r['score']} {r.get('subscores','')}", flush=True)
    with open(f"{EV}/results_b7f_learnform.json", "w") as f:
        json.dump(res, f, indent=1)
    scores = [r["score"] for r in res.values() if r["status"] == "ok"]
    print(f"LEARN-FORM B7F: mean score {sum(scores)/len(scores):.1f} over {len(scores)} items")

if __name__ == "__main__":
    main()
