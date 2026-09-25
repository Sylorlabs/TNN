#!/usr/bin/env python3
"""B1N: P01-P22 raw NL. LEARN-FORM via solve; other engines verify clean abstain on NL input.
Ground truth: TYPE field (proof/open_or_impossible/find_error) + mathematical correctness.
An engine SOLVES a B1N problem iff it produces the TYPE-correct verdict via a
faithful formalization and sound derivation (judged by coordinator audit).
"""
import os, subprocess, re, hashlib, json

BASE = "/home/hatch/workspace/tnn-lab/math_logic"
BIN = "/home/hatch/workspace/math_r2/eval/bin"
EV = "/home/hatch/workspace/math_r2/eval"
OUT = f"{EV}/out"
STORE = f"{BASE}/round2/engines/learnform/FORMALIZER_STORE"
KB = f"{BASE}/knowledge/KB_SMOKE.md"

# TYPE -> expected verdict category
# proof: claim true, should DERIVE (but engines can't do real math; honest expectation: 0)
# open_or_impossible: should WITHHOLD (not derive falsehood)
# find_error: should identify error / not derive the false conclusion -> WITHHELD/REFUTED-of-fallacy
def get_type(pid):
    with open(f"{BASE}/problems/{pid}.txt") as f:
        t = f.read()
    m = re.search(r"TYPE:\s*(\S+)", t)
    return m.group(1) if m else "?"

def run_lf(pid):
    nl = f"{BASE}/problems/{pid}.txt"
    outbase = f"{OUT}/B1N_LEARN-FORM_{pid}"
    for r in range(3):
        o = f"{outbase}.r{r}"
        p = subprocess.run([f"{BIN}/learnform_bin", "solve", nl, STORE, KB, o],
                           cwd=BASE, capture_output=True, timeout=300)
        if p.returncode != 0:
            return {"pid": pid, "status": f"EXIT_{p.returncode}"}
    def norm(p):
        with open(p, "rb") as f: t = f.read().decode("utf-8", errors="replace")
        t = re.sub(r"^FORMAL_FORM:\s*\S+", "FORMAL_FORM: <out>", t, flags=re.M)
        return hashlib.sha256(t.encode()).hexdigest()
    hs = [norm(f"{outbase}.r{r}") for r in range(3)]
    if not (hs[0] == hs[1] == hs[2]):
        return {"pid": pid, "status": "DIVERGENT"}
    with open(f"{outbase}.r0") as f: txt = f.read()
    v = re.search(r"^VERDICT:\s*(\S+)", txt, re.M)
    verdict = v.group(1) if v else "?"
    # extract formalization for faithfulness audit
    fm = re.search(r"^FORMAL_FORM:\s*(\S+)", txt, re.M)
    form = ""
    if fm and os.path.exists(fm.group(1)):
        with open(fm.group(1)) as f: form = f.read()
    return {"pid": pid, "status": "ok", "verdict": verdict, "type": get_type(pid),
            "formalization": form, "sha": hs[0]}

def check_abstain(ename, binary, pid):
    """Feed raw NL .txt as problem file; engine should fail cleanly (parse error -> exit 4)
    or WITHHELD, never a DERIVED verdict on unparseable input."""
    nl = f"{BASE}/problems/{pid}.txt"
    out = f"{OUT}/B1N_{ename}_{pid}.probe"
    p = subprocess.run([binary, nl, out], cwd=BASE, capture_output=True, timeout=60)
    verdict = "?"
    if p.returncode == 0 and os.path.exists(out):
        with open(out) as f: txt = f.read()
        m = re.search(r"^VERDICT:\s*(\S+)", txt, re.M)
        verdict = m.group(1) if m else "?"
    return {"pid": pid, "exit": p.returncode, "verdict": verdict}

def main():
    pids = [f"P{i:02d}" for i in range(1, 23)]
    res = {"LEARN-FORM": {}, "abstain_check": {}}
    print("=== LEARN-FORM B1N ===", flush=True)
    for pid in pids:
        r = run_lf(pid)
        res["LEARN-FORM"][pid] = r
        print(f"{pid} [{r.get('type','?')}]: {r['status']} verdict={r.get('verdict','?')}", flush=True)
    print("=== Abstain check (other engines on raw NL) ===", flush=True)
    for ename, binary in [("ONE-R1", f"{BIN}/one_bin"), ("DUAL-R1", f"{BIN}/dual_bin"),
                          ("HYB", f"{BIN}/hyb_bin"), ("REF-FIRST", f"{BIN}/reffirst_bin"),
                          ("NFEE", f"{BIN}/nfee_bin")]:
        # sample 3 problems (not all 22; behavior is uniform)
        for pid in ["P01", "P10", "P22"]:
            r = check_abstain(ename, binary, pid)
            res["abstain_check"].setdefault(ename, {})[pid] = r
            print(f"{ename} {pid}: exit={r['exit']} verdict={r['verdict']}", flush=True)
    with open(f"{EV}/results_b1n.json", "w") as f:
        json.dump(res, f, indent=1)

if __name__ == "__main__":
    main()
