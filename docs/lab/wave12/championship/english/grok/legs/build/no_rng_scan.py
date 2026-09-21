#!/usr/bin/env python3
"""Static no-RNG scan for the grok English-box legs.

Checks every .zag under legs/{legA,legB,legC,shared}/src (including
substrate/) for:
  1. randomness / nondeterminism source tokens (urandom, rand(, srand,
     rdtsc, clock_gettime, gettimeofday, time(, getpid, RDRAND, ...),
  2. the full inventory of `_zag_*` intrinsics used per file,
  3. identifiers containing 'rand' (case-insensitive).

The behavioral gate is the N=5 byte-identical replay of every run command;
this scan is the static complement. Writes legs/build/NO_RNG_SCAN.md.
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))   # grok/legs/build
LEGS = os.path.dirname(HERE)

RNG_TOKENS = [
    "urandom", "/dev/random", "rand(", "srand", "random(", "drand48",
    "rdtsc", "RDRAND", "rdrand", "clock_gettime", "gettimeofday",
    "getpid", "getppid", "_zag_time", "_zag_clock", "_zag_rand",
    "_zag_seed", "time(", "nanosleep",
]

hits = []
intrinsics = {}   # file -> set of _zag_* tokens
rand_idents = []
scanned = []

for root, dirs, files in os.walk(LEGS):
    if "build" in root.split(os.sep):
        continue
    for fn in sorted(files):
        if not fn.endswith(".zag"):
            continue
        p = os.path.join(root, fn)
        rel = os.path.relpath(p, LEGS)
        scanned.append(rel)
        t = open(p).read()
        for tok in RNG_TOKENS:
            for m in re.finditer(re.escape(tok), t):
                line = t.count("\n", 0, m.start()) + 1
                hits.append((rel, line, tok))
        for m in re.finditer(r"_zag_[A-Za-z0-9_]+", t):
            intrinsics.setdefault(rel, set()).add(m.group(0))
        for m in re.finditer(r"[A-Za-z_][A-Za-z0-9_]*rand[A-Za-z0-9_]*",
                             t, re.IGNORECASE):
            line = t.count("\n", 0, m.start()) + 1
            rand_idents.append((rel, line, m.group(0)))

L = []
L.append("# Static no-RNG scan — grok English-box legs")
L.append("")
L.append(f"files scanned: {len(scanned)} .zag files")
L.append("")
L.append("## 1. Randomness-source tokens")
if hits:
    L.append(f"FOUND {len(hits)} hits (FAIL):")
    for rel, line, tok in hits:
        L.append(f"- {rel}:{line}: `{tok}`")
else:
    L.append("none found (PASS): no urandom/rand/srand/rdtsc/clock_gettime/")
    L.append("gettimeofday/time(/getpid/RDRAND/_zag_time/_zag_clock/_zag_rand tokens.")
L.append("")
L.append("## 2. `_zag_*` intrinsic inventory (per file)")
for rel in sorted(intrinsics):
    toks = sorted(intrinsics[rel])
    L.append(f"- {rel}: {', '.join(toks)}")
L.append("")
L.append("## 3. Identifiers containing 'rand'")
if rand_idents:
    for rel, line, ident in rand_idents:
        L.append(f"- {rel}:{line}: `{ident}`")
else:
    L.append("none (PASS).")
L.append("")
L.append("## Verdict")
if not hits and not rand_idents:
    L.append("STATIC SCAN PASS: no randomness/nondeterminism sources in the leg sources.")
else:
    L.append("STATIC SCAN FAIL: see hits above.")

out = os.path.join(HERE, "NO_RNG_SCAN.md")
with open(out, "w") as f:
    f.write("\n".join(L) + "\n")
print("\n".join(L))
print(f"wrote {out}")
