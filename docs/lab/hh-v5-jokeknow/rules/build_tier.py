#!/usr/bin/env python3
"""Build a v5k tier/ablation binary.
Usage: build_tier.py <name> <tier> [--only pun|idiom|world|phon]
  name: output dir under tiers/
  tier: 1/1, 1/2, 1/4 (interleave)
  --only: ablation (only that partition populated)
Compiles with the pinned znc and runs determinism check (2x SHA).
"""
import sys, os, subprocess, hashlib, shutil

ZNC = os.path.expanduser("~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1")
HH = os.path.expanduser("~/workspace/hh-v5-jokeknow")

name = sys.argv[1]
tier = sys.argv[2]
only = None
if "--only" in sys.argv:
    only = sys.argv[sys.argv.index("--only") + 1]

workdir = os.path.join(HH, "tiers", name)
os.makedirs(workdir, exist_ok=True)

# 1. tables
tsvs = []
for s in ["pun", "idiom", "world", "phon"]:
    if only and s != only:
        tsvs.append(os.path.join(HH, "stores_empty", s + ".tsv"))
    else:
        tsvs.append(os.path.join(HH, "stores", s + ".tsv"))
r = subprocess.run(
    [sys.executable, os.path.join(HH, "rules", "tsv2zag.py"),
     "--tier", tier, "--out", os.path.join(workdir, "k_tables_tmp.zag")] + tsvs,
    capture_output=True, text=True)
print(r.stdout, r.stderr)
assert r.returncode == 0, "tsv2zag failed"

# 2. assemble classifier
r = subprocess.run(
    [sys.executable, os.path.join(HH, "rules", "build_v5k.py"),
     os.path.join(workdir, "k_tables_tmp.zag"), workdir],
    capture_output=True, text=True, cwd=HH)
print(r.stdout, r.stderr)
assert r.returncode == 0, "build_v5k failed"
os.remove(os.path.join(workdir, "k_tables_tmp.zag"))

# 3. compile
binary = os.path.join(workdir, "v5k_bin")
r = subprocess.run([ZNC, "run4.zag", "-o", "v5k_bin"],
                   capture_output=True, text=True, cwd=workdir)
errs = [l for l in r.stdout.splitlines() + r.stderr.splitlines()
        if "error" in l.lower()]
assert r.returncode == 0 and not errs, f"compile failed: {errs[:5]}"
print(f"compiled {binary}")

# 4. determinism: 2x run on rt3e jokes, SHA compare
corpus = os.path.join(HH, "corpora", "rt3e_jokes.tsv")
outs = []
for i in (1, 2):
    out = os.path.join(HH, "runs", f"{name}_jokes_{i}.txt")
    subprocess.run([binary, corpus], stdout=open(out, "w"), cwd=HH,
                   check=True)
    outs.append(out)
h = [hashlib.sha256(open(o, "rb").read()).hexdigest() for o in outs]
assert h[0] == h[1], f"NON-DETERMINISTIC: {h}"
print(f"determinism OK: {h[0][:16]}...")
print(f"TIER {name} READY")
