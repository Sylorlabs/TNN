#!/usr/bin/env python3
"""Independent-battery scorer. FIRST program allowed to read expected.json.
Reads runs/runN.log verdict lines + expected.json, emits per-capability scores,
independence gaps, mirror baseline, and kill-bar adjudication to SCORES.md.
"""
import json, sys, os

BAT = os.path.expanduser("~/workspace/tnn-lab/redteam/independent-battery")
RUNS = [os.path.join(BAT, "runs", f"run{i}.log") for i in range(1, 6)]
EXP = os.path.join(BAT, "expected.json")

COUPLED = {"contra": 1.0000, "false": 1.0000, "para": 0.9649}

def load_run(path):
    v = {}
    with open(path) as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.startswith("V,"):
                continue
            parts = line.split(",", 3)
            if len(parts) < 3:
                continue
            pid = int(parts[1])
            verdict = parts[2]
            detail = parts[3] if len(parts) > 3 else ""
            v[pid] = (verdict, detail)
    return v

def detail_ok(got, exp):
    if exp == "":
        return True
    # CITE: numeric compare; AFFIRM name: case-insensitive
    try:
        return int(got) == int(exp)
    except ValueError:
        return got.strip().lower() == exp.strip().lower()

def main():
    with open(EXP) as f:
        expected = json.load(f)
    runs = [load_run(p) for p in RUNS]
    # determinism across runs
    det = all(r == runs[0] for r in runs[1:])
    caps = {}
    for pid_s, e in expected.items():
        pid = int(pid_s)
        cap = e["cap"]
        caps.setdefault(cap, []).append((pid, e))
    lines = []
    lines.append("# INDEPENDENT BATTERY — SCORES")
    lines.append("")
    lines.append(f"determinism_5x: {'PASS' if det else 'FAIL'}")
    lines.append("")
    lines.append("| cap | n | correct | score | coupled | gap (coupled-indep) |")
    lines.append("|---|---|---|---|---|---|")
    gaps = {}
    truth_score = None
    mirror = None
    for cap in ["contra", "false", "para", "truth", "abstain", "prov"]:
        items = caps.get(cap, [])
        n = len(items)
        ok = 0
        for pid, e in items:
            got = runs[0].get(pid)
            if got and got[0] == e["verdict"] and detail_ok(got[1], e["detail"]):
                ok += 1
        score = ok / n if n else 0.0
        cpl = COUPLED.get(cap)
        gap = (cpl - score) if cpl is not None else None
        gaps[cap] = gap
        cpl_s = f"{cpl:.4f}" if cpl is not None else "n/a"
        gap_s = f"{gap:+.4f}" if gap is not None else "n/a"
        lines.append(f"| {cap} | {n} | {ok} | {score:.4f} | {cpl_s} | {gap_s} |")
        if cap == "truth":
            truth_score = score
            # mirror baseline: fraction of truth probes whose taught claim was true
            mirror = sum(1 for _, e in items if e["verdict"] == "AFFIRM") / n if n else 0.0
    lines.append("")
    lines.append(f"mirror_baseline_truth: {mirror:.4f}" if mirror is not None else "mirror: n/a")
    lines.append(f"learner_truth: {truth_score:.4f}" if truth_score is not None else "learner: n/a")
    lines.append("")
    lines.append("## Kill bars")
    # KB-GAP
    for cap in ["contra", "false", "para"]:
        g = gaps[cap]
        if g is not None and g > 0.30:
            lines.append(f"- KB-GAP({cap}): TRIPPED — gap {g:.4f} > 0.30 → headline GENERATOR-COUPLED, revised to independent number")
        else:
            lines.append(f"- KB-GAP({cap}): HOLD — gap {g:+.4f}" if g is not None else f"- KB-GAP({cap}): n/a")
    # KB-TRUTH
    if truth_score is not None and mirror is not None:
        if truth_score > mirror:
            lines.append(f"- KB-TRUTH: HOLD — learner {truth_score:.4f} > mirror {mirror:.4f}")
        else:
            lines.append(f"- KB-TRUTH: TRIPPED — learner {truth_score:.4f} <= mirror {mirror:.4f} → 'truthful' qualifier SUSPENDED")
    # KB-DET
    lines.append(f"- KB-DET: {'HOLD' if det else 'TRIPPED'}")
    out = "\n".join(lines) + "\n"
    with open(os.path.join(BAT, "SCORES.md"), "w") as f:
        f.write(out)
    print(out)

if __name__ == "__main__":
    main()
