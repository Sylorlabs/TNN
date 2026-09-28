#!/usr/bin/env python3
"""B7F schema-equivalence checker (test instrument, NOT an engine).

Scores a produced NL->schema formalization against the SEALED formal analog:
  schema-choice match (top-level form of each premise/target) +
  slot-binding match (predicate symbols + renaming-tolerant structure),
scaled to 0-100.

Usage: python3 b7f_checker.py SEALED_B7F_FORM.sol produced.form
  produced.form uses the same .form layout (ID, STORE, PREMISES, TARGET).

Deterministic: greedy best-match alignment with index tie-breaks; no RNG.
Sealed-safety: reads the sealed file only at scoring time and NEVER prints
sealed content -- output is numeric subscores only.
"""
import re
import sys

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from verify_batteries import parse, fmt  # claim-language parser (test instrument)

def load_blocks(path):
    """Parse ID/STORE/PREMISES/TARGET blocks; returns {id: (premises, target)}."""
    blocks, cur = {}, None
    pid, premises, target, mode = None, [], None, None
    def flush():
        if pid:
            blocks[pid] = (premises, target)
    with open(path) as f:
        for raw in f:
            line = raw.strip()
            if line.startswith("#") or line == "":
                continue
            if line.startswith("ID:"):
                flush(); pid = line[3:].strip(); premises, target, mode = [], None, None
            elif line == "PREMISES:":
                mode = "P"
            elif line == "TARGET:":
                mode = "T"
            elif line.startswith("STORE:"):
                mode = None
            elif mode == "P":
                premises.append(parse(line))
            elif mode == "T":
                target = parse(line); mode = None
    flush()
    return blocks

def shape(f):
    return f[0]  # false|not|imp|and|or|forall|atom

def predicates(f):
    out = []
    k = f[0]
    if k == "atom":
        out.append(f[1])
        for a in f[2]:
            out += predicates(a)
    elif k == "fn":
        for a in f[2]:
            out += predicates(a)
    elif k == "not":
        out += predicates(f[1])
    elif k in ("imp", "and", "or"):
        out += predicates(f[1]); out += predicates(f[2])
    elif k == "forall":
        out += predicates(f[2])
    return out

def canonical(f):
    """Rename each distinct const to c<N> by first-occurrence order (structure
    comparison tolerant to constant renaming; predicate names kept exact)."""
    env, n = {}, [0]
    def term(t):
        k = t[0]
        if k == "const":
            if t[1] not in env:
                env[t[1]] = "c%d" % n[0]; n[0] += 1
            return ("const", env[t[1]])
        if k == "fn":
            return ("fn", t[1], tuple(term(a) for a in t[2]))
        return t
    def rec(g):
        k = g[0]
        if k == "atom":
            return ("atom", g[1], tuple(term(a) for a in g[2]))
        if k == "not":
            return ("not", rec(g[1]))
        if k in ("imp", "and", "or"):
            return (k, rec(g[1]), rec(g[2]))
        if k == "forall":
            return ("forall", g[1], rec(g[2]))
        return g
    return fmt(rec(f))

def pair_score(pf, sf):
    pp, sp = predicates(pf), predicates(sf)
    if not pp and not sp:
        pred = 1.0
    else:
        inter = 0
        rest = list(sp)
        for x in pp:
            if x in rest:
                inter += 1; rest.remove(x)
        pred = inter / max(len(pp), len(sp))
    struct = 1.0 if canonical(pf) == canonical(sf) else 0.0
    return (pred + struct) / 2.0

def score_one(pid, sealed, produced):
    sp, st = sealed
    pp, pt = produced
    nS, nP = len(sp), len(pp)
    used = [False] * nP
    schema_pts = 0.0
    slot_pts = 0.0
    # greedy best-match alignment, deterministic tie-break by lowest index
    order = sorted(range(nS), key=lambda j: fmt(sp[j]))
    for j in order:
        best, bi = -1.0, -1
        for i in range(nP):
            if used[i]:
                continue
            s = (1.0 if shape(pp[i]) == shape(sp[j]) else 0.0, pair_score(pp[i], sp[j]), -i)
            if s[0] + s[1] > best:
                best, bi = s[0] + s[1], i
        if bi >= 0:
            used[bi] = True
            if shape(pp[bi]) == shape(sp[j]):
                schema_pts += 1.0
            slot_pts += pair_score(pp[bi], sp[j])
    den = max(nS, nP) + 1  # +1 for the target
    if shape(pt) == shape(st):
        schema_pts += 1.0
    slot_pts += pair_score(pt, st)
    schema = schema_pts / den
    slots = slot_pts / den
    total = round(100 * (schema + slots) / 2.0)
    return schema, slots, total

def main():
    if len(sys.argv) != 3:
        print("usage: b7f_checker.py SEALED_B7F_FORM.sol produced.form")
        sys.exit(2)
    sealed = load_blocks(sys.argv[1])
    produced = load_blocks(sys.argv[2])
    totals = []
    for pid in sorted(produced):
        if pid not in sealed:
            print("%s ERROR: id not in sealed analogs" % pid)
            continue
        sc, sl, t = score_one(pid, sealed[pid], produced[pid])
        totals.append(t)
        print("%s schema=%.2f slots=%.2f total=%d" % (pid, sc, sl, t))
    if totals:
        print("OVERALL n=%d mean=%.1f" % (len(totals), sum(totals) / len(totals)))

if __name__ == "__main__":
    main()
