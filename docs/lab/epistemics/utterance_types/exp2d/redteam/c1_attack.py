#!/usr/bin/env python3
"""Red-team C1/C2 leak scanner v2 (fast, exact flags).

Scans CLEANED exp2d corpora against:
  (a) all curriculum utterances (2C probe universe),
  (b) the extended X2C probes (sinc3x_wi/wd) -- NOT covered by the
      coordinator's scan or by author_xprobes.py's pre-clean check.

Flag rules (exact):
  preregistered: 16-byte substring overlap (16-gram set intersection),
                 shared word-4-gram, word-unigram Jaccard >= 0.60
  tightened    : 12-byte overlap, shared word-3-gram, Jaccard >= 0.50
Deterministic, zero RNG.
"""
import os

EXP = os.path.expanduser("~/workspace/exp2d_redteam/wt/docs/lab/epistemics/utterance_types/exp2d")
CUR = os.path.expanduser("~/workspace/exp2d_redteam/wt/docs/lab/epistemics/utterance_types/crew2/curriculum")

def utts_of(path):
    out = []
    for line in open(path, encoding="utf-8", errors="replace"):
        line = line.rstrip("\n")
        if not line or line.startswith("#"):
            continue
        p = line.split("|")
        if len(p) >= 4:
            out.append((p[0], p[3].lower()))
    return out

def words(t):
    return [w for w in "".join(c if c.isalnum() else " " for c in t).split()]

def ngrams(ws, n):
    return set(tuple(ws[i:i+n]) for i in range(len(ws)-n+1))

def cgrams(t, n):
    t = t.lower()
    return set(t[i:i+n] for i in range(len(t)-n+1)) if len(t) >= n else set()

def jacc(a, b):
    a, b = set(a), set(b)
    if not a and not b: return 1.0
    if not a or not b: return 0.0
    return len(a & b) / len(a | b)

cur_all = []
for fn in sorted(os.listdir(CUR)):
    if fn.endswith(".txt"):
        for pid, u in utts_of(os.path.join(CUR, fn)):
            cur_all.append((f"{fn}:{pid}", u))
sinc_probes = [(t, u) for t, u in cur_all if t.startswith("sinc")]
x2c_wi = [(f"wi:{pid}", u) for pid, u in utts_of(os.path.join(EXP, "items/sinc3x_wi.txt"))]
x2c_wd = [(f"wd:{pid}", u) for pid, u in utts_of(os.path.join(EXP, "items/sinc3x_wd.txt"))]
x2c_all = x2c_wi + x2c_wd

# precompute probe features once
def feats(u):
    w = words(u)
    return (cgrams(u, 16), cgrams(u, 12), ngrams(w, 4), ngrams(w, 3), set(w))
probe_feats = {label: [(t, u, feats(u)) for t, u in probes]
               for label, probes in (("sinc", sinc_probes), ("x2c", x2c_all), ("cur", cur_all))}

corpora = {
    "cal2_ab":   os.path.join(EXP, "items/cal2_ab.txt"),
    "cal2_abc":  os.path.join(EXP, "items/cal2_abc.txt"),
    "cal2_de":   os.path.join(EXP, "items/cal2_de.txt"),
    "cal2_vol2": os.path.join(EXP, "items/cal2_vol2.txt"),
}

def scan(items, plabel, clabel):
    P = probe_feats[plabel]
    pre_flags, tight_flags = [], []
    for pid, u in items:
        c16, c12, w4, w3, wu = feats(u)
        for ptag, pu, (g16, g12, p4, p3, pw) in P:
            s16 = len(c16 & g16) > 0
            s12 = len(c12 & g12) > 0
            sh4 = len(w4 & p4) > 0
            sh3 = len(w3 & p3) > 0
            j1 = jacc(wu, pw)
            if s16 or sh4 or j1 >= 0.60:
                pre_flags.append((pid, ptag, s16, sh4, j1, u, pu))
            elif s12 or sh3 or j1 >= 0.50:
                tight_flags.append((pid, ptag, s12, sh3, j1, u, pu))
    print(f"\n===== {clabel} vs {plabel}: {len(items)} items =====")
    print(f"PREREGISTERED flags: {len(pre_flags)}")
    for r in pre_flags[:20]:
        print(f"  PRE {r[0]} vs {r[1]} sub16={int(r[2])} sh4={int(r[3])} J1={r[4]:.2f}\n    I:{r[5][:72]}\n    P:{r[6][:72]}")
    print(f"TIGHTENED-only flags: {len(tight_flags)}")
    for r in tight_flags[:30]:
        print(f"  TIGHT {r[0]} vs {r[1]} sub12={int(r[2])} sh3={int(r[3])} J1={r[4]:.2f}\n    I:{r[5][:72]}\n    P:{r[6][:72]}")
    return pre_flags, tight_flags

all_pre, all_tight = [], []
for tag, path in corpora.items():
    items = utts_of(path)
    for plabel in ("sinc", "x2c", "cur"):
        p, t = scan(items, plabel, tag)
        all_pre += [(tag, plabel) + r for r in p]
        all_tight += [(tag, plabel) + r for r in t]

print(f"\n\nTOTAL preregistered flags: {len(all_pre)} | TOTAL tightened-only: {len(all_tight)}")
