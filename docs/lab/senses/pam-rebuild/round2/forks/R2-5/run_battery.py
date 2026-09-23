#!/usr/bin/env python3
"""R2-5 parallel battery runner."""
import os, sys, glob, re, subprocess, hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed

FORK = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2/forks/R2-5"
SENSE = os.path.join(FORK, "src", "sense")
FIXDIR = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2/fixtures"
TASKS = ["colordisc","colorconst","shapetrans","pitchdisc","timbredisc","motiondir"]
EXT = {"colordisc":"img","colorconst":"img","shapetrans":"img",
       "pitchdisc":"pcm","timbredisc":"pcm","motiondir":"vid"}

def parse(out):
    d = {}
    m = re.search(r'judgment=([A-Z_0-9]+)', out); d['j'] = m.group(1) if m else None
    m = re.search(r'state=([A-Z]+)', out); d['s'] = m.group(1) if m else None
    m = re.search(r'confidence=([0-9]+)', out); d['c'] = int(m.group(1)) if m else 0
    m = re.search(r'ledger=([^\n]+)', out); d['ledger'] = m.group(1).strip() if m else None
    return d

def run_one(args):
    task, fixture, mode, idx = args
    cmd = [SENSE, task, fixture, mode, "0"*64, str(idx)]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=30).stdout
        d = parse(out)
        with open(fixture + ".truth") as f:
            truth = f.read().strip().split("=")[-1]
        d['truth'] = truth
        d['correct'] = (d['j'] == truth)
        d['fixture'] = fixture
        d['task'] = task
        d['mode'] = mode
        return d
    except Exception as e:
        return {'error': str(e), 'fixture': fixture, 'task': task, 'mode': mode}

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"
    prefix = sys.argv[2] if len(sys.argv) > 2 else "r2n"  # r2n or r2a
    max_workers = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    
    jobs = []
    idx = 0
    for task in TASKS:
        pattern = os.path.join(FIXDIR, f"{prefix}_{task}_*.{EXT[task]}")
        for f in sorted(glob.glob(pattern)):
            jobs.append((task, f, mode, idx))
            idx += 1
    
    print(f"Running {len(jobs)} jobs ({mode}, {prefix}) with {max_workers} workers...", flush=True)
    
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {ex.submit(run_one, j): j for j in jobs}
        for i, fut in enumerate(as_completed(futures)):
            r = fut.result()
            results.append(r)
            if (i+1) % 500 == 0:
                print(f"  {i+1}/{len(jobs)} done", flush=True)
    
    # Compute metrics
    tot = len(results)
    prom = sum(1 for r in results if r.get('s') == 'PROMOTED')
    prom_corr = sum(1 for r in results if r.get('s') == 'PROMOTED' and r.get('correct'))
    corr = sum(1 for r in results if r.get('correct'))
    esc = sum(1 for r in results if r.get('s') == 'ESCALATED')
    inst = sum(1 for r in results if r.get('s') == 'INSTALLED')
    
    prec = 100*prom_corr//prom if prom else 0
    rec = 100*prom_corr//corr if corr else 0
    esc_pct = 100*esc//tot if tot else 0
    
    print(f"\nResults ({mode}, {prefix}):", flush=True)
    print(f"  Total: {tot}", flush=True)
    print(f"  Correct: {corr} ({100*corr//tot if tot else 0}%)", flush=True)
    print(f"  Promoted: {prom}, Correct promoted: {prom_corr}", flush=True)
    print(f"  Precision: {prec}% (bar: >=95%)", flush=True)
    print(f"  Recall: {rec}% (bar: >=80%)", flush=True)
    print(f"  Escalated: {esc} ({esc_pct}%, bar: <=5%)", flush=True)
    print(f"  Installed (ablation): {inst}", flush=True)
    
    # Save results
    out_path = os.path.join(FORK, "evidence", f"battery_{mode}_{prefix}.txt")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        f.write(f"mode={mode} prefix={prefix} total={tot} corr={corr} prom={prom} prom_corr={prom_corr} prec={prec} rec={rec} esc={esc}\n")
        for r in results:
            f.write(f"{r.get('task')} {r.get('fixture')} {r.get('j')} {r.get('truth')} {r.get('s')} {r.get('c')}\n")
    print(f"Saved to {out_path}", flush=True)

if __name__ == "__main__":
    main()
