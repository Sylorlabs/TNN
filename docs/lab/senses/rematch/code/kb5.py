#!/usr/bin/env python3
"""KB5: 3 reruns of the full fitted pipeline, byte-identical.

Each rerun: fresh binary runs on TEST_FRESH + ADV_R1 (fresh process pool,
new OS scheduling) into the standard filenames + deterministic fit.py
sweep + metrics. Compares sha256 of the results JSON across the 3 runs.
Exit 0 iff identical. Original eval caches are backed up and restored.
"""
import hashlib, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def main():
    std = {"TEST_FRESH": "primary", "ADV_R1": "adversarial"}
    backups = {}
    for name in std:
        p = os.path.join(HERE, "runs_%s.jsonl" % name)
        backups[name] = p + ".kb5bak"
        shutil.copy(p, backups[name])
    digests = []
    try:
        for i in (1, 2, 3):
            print("KB5 rerun %d" % i, flush=True)
            for name, variants in std.items():
                out = os.path.join(HERE, "runs_%s.jsonl" % name)
                r = subprocess.run(
                    [sys.executable, "run_all.py",
                     os.path.join(DATA, name), out, variants],
                    cwd=HERE, capture_output=True, text=True, timeout=3600)
                assert r.returncode == 0, (r.stderr or r.stdout)[-500:]
                print("  %s: %s" % (name, r.stdout.strip().splitlines()[-1]), flush=True)
            env = dict(os.environ, STAMP="kb5_r%d" % i)
            r = subprocess.run([sys.executable, "fit.py"], cwd=HERE,
                               capture_output=True, text=True, timeout=3600,
                               env=env)
            assert r.returncode == 0, (r.stderr or r.stdout)[-500:]
            d = sha(os.path.join(HERE, "results_kb5_r%d.json" % i))
            digests.append(d)
            print("  digest: %s" % d, flush=True)
    finally:
        for name, bak in backups.items():
            shutil.move(bak, os.path.join(HERE, "runs_%s.jsonl" % name))
    ok = len(set(digests)) == 1
    print("KB5 %s: %s" % ("PASS" if ok else "FAIL", digests))
    sys.exit(0 if ok else 1)

main()
