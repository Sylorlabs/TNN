#!/usr/bin/env python3
"""Driver for the RAW-VS-HUMAN TEST wave (B2/B3 forks).

Orchestration only: runs the pure-Zag binaries (EMIT/GROW/JUDGE),
joins their outputs with frozen truth labels, writes inputs, and
scores. No Python in any mechanism, growth, or judgment path.
"""
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

WAVE = os.path.dirname(os.path.abspath(__file__))
B2 = os.path.join(WAVE, "b2")
B3 = os.path.join(WAVE, "b3")
DATA = "/home/hatch/workspace/senses-rematch/data"
HARNESS = "/home/hatch/workspace/senses-rebuild/harness"
TRAIN_SEED = "20260922"

TASKS = {
    "colordisc":  ("t1_colordisc",  ".img"),
    "colorconst": ("t2_colorconst", ".img"),
    "pitchdisc":  ("t4_pitchdisc",  ".pcm"),
}

def fixture_dir(task, budget):
    sub, _ = TASKS[task]
    return os.path.join(DATA, budget, sub, "primary")

def fixture_paths(task, budget):
    d = fixture_dir(task, budget)
    _, ext = TASKS[task]
    names = sorted(f for f in os.listdir(d) if f.endswith(ext))
    return [os.path.join(d, f) for f in names]

def truth_of(path):
    tp = path + ".truth"
    with open(tp) as f:
        txt = f.read().strip()
    # format: "truth=SAME"
    if "=" in txt:
        txt = txt.split("=", 1)[1].strip()
    return txt

def run_emit(bindir, binary, task, path):
    p = subprocess.run([os.path.join(bindir, binary), task, path],
                       capture_output=True, text=True, timeout=300)
    if p.returncode != 0:
        raise RuntimeError(f"emit failed rc={p.returncode} {path}\n{p.stdout}\n{p.stderr}")
    out = {}
    for line in p.stdout.splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            try:
                out[k.strip()] = int(v.strip())
            except ValueError:
                out[k.strip()] = v.strip()
    return out

def emit_all(bindir, task, budget, binary="emit", workers=8):
    """Run EMIT on every fixture; return list of dicts with fid + measurements."""
    paths = fixture_paths(task, budget)
    def one(path):
        fid = os.path.basename(path)
        r = run_emit(bindir, binary, task, path)
        r["fid"] = fid
        r["truth"] = truth_of(path)
        return r
    with ThreadPoolExecutor(max_workers=workers) as ex:
        rows = list(ex.map(one, paths))
    rows.sort(key=lambda r: r["fid"])
    return rows

def write_emit_file(rows, path):
    """Write the GROW emit input: n, then per row fid-idx h1 bin1 pos1 h2 bin2 pos2."""
    with open(path, "w") as f:
        f.write(f"{len(rows)}\n")
        for i, r in enumerate(rows):
            f.write(f"{i} {r['h1']} {r['bin1']} {r['pos1']} {r['h2']} {r['bin2']} {r['pos2']}\n")

TRUTH_INT = {
    "colordisc":  {"SAME": 0, "DIFFERENT": 1},
    "colorconst": {"SAME_SURFACE": 0, "DIFFERENT": 1},
    "pitchdisc":  {"SAME": 0, "HIGHER": 1, "LOWER": 2},
}

def write_labels_file(rows, task, path):
    m = TRUTH_INT[task]
    with open(path, "w") as f:
        f.write(f"{len(rows)}\n")
        for i, r in enumerate(rows):
            f.write(f"{i} {m[r['truth']]}\n")

if __name__ == "__main__":
    # smoke: emit one fixture per task
    for task in TASKS:
        paths = fixture_paths(task, "TRAIN_T2")
        r = run_emit(B2, "emit", task, paths[0])
        print(task, paths[0].split("/")[-1], r)
