#!/usr/bin/env python3
"""KB5: 3 reruns of the full fitted pipeline, byte-identical.

Each rerun performs FRESH binary evaluation (cache deleted first, new
process pool) on TEST_FRESH (primary) and ADV_R1 (adversarial, from the
round-1 fixture tree), then the deterministic fit.py sweep (STAMP-scoped
output). Compares sha256 of the complete results JSON across the 3 runs.
Exit 0 iff all three digests are identical. Standard caches are backed
up and restored afterwards.
"""
import hashlib, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
R1FIX = os.path.expanduser("~/workspace/senses-rebuild/harness/fixtures")

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def fresh_binary_eval(root, out, variants):
    if os.path.exists(out):
        os.remove(out)  # force truly fresh evaluation, no cache reuse
    r = subprocess.run(
        [sys.executable, "run_all.py", root, out, variants],
        cwd=HERE, capture_output=True, text=True, timeout=7200)
    assert r.returncode == 0, (r.stderr or r.stdout)[-800:]
    return r.stdout.strip().splitlines()[-1]

def main():
    std = {
        "TEST_FRESH": (os.path.join(DATA, "TEST_FRESH"), "primary"),
        "ADV_R1": (R1FIX, "adversarial"),
    }
    backups = {}
    for name in std:
        p = os.path.join(HERE, "runs_%s.jsonl" % name)
        backups[name] = p + ".kb5bak"
        shutil.copy(p, backups[name])
    digests = []
    try:
        for i in (1, 2, 3):
            print("KB5 rerun %d" % i, flush=True)
            for name, (root, variants) in std.items():
                out = os.path.join(HERE, "runs_%s.jsonl" % name)
                tail = fresh_binary_eval(root, out, variants)
                print("  %s: %s" % (name, tail), flush=True)
            env = dict(os.environ, STAMP="kb5_r%d" % i)
            r = subprocess.run([sys.executable, "fit.py", "kb5_r%d" % i],
                               cwd=HERE, capture_output=True, text=True,
                               timeout=7200, env=env)
            assert r.returncode == 0, (r.stderr or r.stdout)[-800:]
            d = sha(os.path.join(HERE, "results_kb5_r%d.json" % i))
            digests.append(d)
            print("  digest: %s" % d, flush=True)
    finally:
        for name, bak in backups.items():
            shutil.move(bak, os.path.join(HERE, "runs_%s.jsonl" % name))
    ok = len(set(digests)) == 1
    print("KB5 %s: %s" % ("PASS" if ok else "FAIL", digests))
    with open(os.path.join(HERE, "kb5_digests.txt"), "w") as f:
        f.write("\n".join(digests) + "\nKB5_%s\n" % ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)

main()
