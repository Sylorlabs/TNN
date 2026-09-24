#!/usr/bin/env python3
"""Faithful simulation of crew2 h7_main.zag learning dynamics.
Purpose: determine install provenance of each live marker (which exemplar,
which occurrence) for the H7 scope-indexed-marker separation audit.
Mirrors the Zag code exactly: tokenizer, n-gram spans, marker_add dedup,
learn_exemplar branches, calibrate revocation, predict scoring + tiebreak.
"""
import re, sys

BASE = "/home/hatch/workspace/h7_broaderfix_staging/crew1/evidence_input"
CUR = BASE + "/curriculum"

def load(fname, cur=True):
    d = CUR if cur else BASE
    rows = []
    with open(f"{d}/{fname}") as f:
        for line in f:
            line = line.rstrip("\n").rstrip("\r")
            if line.strip():
                rows.append(line.split("|"))
    return rows

def words_of(field_bytes):
    """words = [a-z0-9]+ runs over lowered field bytes; returns (starts, ends)."""
    s = field_bytes.lower()
    starts, ends = [], []
    i = 0
    while i < len(s):
        c = s[i]
        isw = ('a' <= c <= 'z') or ('0' <= c <= '9')
        if isw:
            st = i
            while i < len(s) and (('a' <= s[i] <= 'z') or ('0' <= s[i] <= '9')):
                i += 1
            starts.append(st); ends.append(i)
        else:
            i += 1
    return s, starts, ends

def ngrams(field, min_n, max_n):
    """Yields (ngram_bytes, wstart_idx, wend_idx_excl) for each n-gram occurrence."""
    s, starts, ends = words_of(field)
    out = []
    nw = len(starts)
    for nn in range(min_n, max_n + 1):
        w = 0
        while w + nn <= nw:
            a = starts[w]; b = ends[w + nn - 1]
            out.append((s[a:b], w, w + nn))
            w += 1
    return out

# concept names from types.txt
types = load("types.txt")
concept_names = [r[0] for r in types]  # order taught
print("concepts:", concept_names)

# markers: list of dicts {know, field, status, support, bytes, installed_by, install_scope_ctx}
markers = []
def marker_add(know_idx, field, ng, installed_by):
    for m in markers:
        if m['know'] == know_idx and m['field'] == field and m['bytes'] == ng:
            if m['status'] != 3:
                m['support'] += 1
            return m
    m = {'know': know_idx, 'field': field, 'status': 1, 'support': 1,
         'bytes': ng, 'installed_by': installed_by}
    markers.append(m)
    return m

def marker_revoke(m):
    m['status'] = 3

def predict(utt, ctx, spk):
    scores = [0] * len(concept_names)
    for m in markers:
        if m['status'] in (1, 2):
            fb = [utt, ctx, spk][m['field']]
            if m['bytes'] in fb:
                scores[m['know']] += 1
    best, bests = -1, 0
    for k in range(len(concept_names)):
        s = scores[k]
        if s > 0:
            take = False
            if best == -1: take = True
            elif s > bests: take = True
            elif s == bests and concept_names[k] < concept_names[best]: take = True
            if take: best, bests = k, s
    if best == -1: return 0, None, scores
    return 1, concept_names[best], scores

def extract(know_idx, utt, ctx, spk, tag):
    for ng, w0, w1 in ngrams(utt, 2, 3):
        marker_add(know_idx, 0, ng, tag)
    for ng, w0, w1 in ngrams(ctx, 1, 3):
        marker_add(know_idx, 1, ng, tag)
    for ng, w0, w1 in ngrams(spk, 1, 3):
        marker_add(know_idx, 2, ng, tag)

def firing_markers(know_idx, utt, ctx, spk):
    out = []
    for m in markers:
        if m['know'] == know_idx and m['status'] != 3:
            fb = [utt, ctx, spk][m['field']]
            if m['bytes'] in fb:
                out.append(m)
    return out

# endorse pool: facts (utt only) + calib (utt,ctx,spk), lowered
endorse = []
for r in load("facts.txt"):
    endorse.append((r[1].lower(), "", ""))
for r in load("calib.txt", cur=False):
    endorse.append((r[3].lower(), r[2].lower(), r[1].lower()))

def calibrate():
    revoked = 0
    for m in markers:
        if m['status'] == 3: continue
        ng = m['bytes']
        for (u, c, s) in endorse:
            fb = [u, c, s][m['field']]
            if ng in fb:
                marker_revoke(m); revoked += 1
                break
    return revoked

def build():
    """Run Phase 2b learning; returns list of live marker dicts."""
    global markers
    markers = []
    # ---------- Phase 2b ----------
    for t in range(1, 6):
        ex = load(f"ex{t}.txt")
        assert len(ex) == 32, (t, len(ex))
        steps = [(2, 0), (4, 2), (8, 4), (16, 8), (32, 16)]
        for (hi, lo) in steps:
            for e in range(lo, hi):
                r = ex[e]
                utt, ctx, spk = r[3].lower(), r[2].lower(), r[1].lower()
                v, pname, scores = predict(utt, ctx, spk)
                tname = concept_names[t - 1]
                tag = f"ex{t}_{e+1:02d}"
                if v == 1 and pname == tname:
                    continue  # early return, no reinforcement
                if v == 1 and pname != tname:
                    wk = concept_names.index(pname)
                    for m in firing_markers(wk, utt, ctx, spk):
                        marker_revoke(m)
                extract(t - 1, utt, ctx, spk, tag)
            calibrate()


    return [m for m in markers if m['status'] != 3]

if __name__ == "__main__":
    live = build()
    live = [m for m in markers if m['status'] != 3]
    print(f"total live markers: {len(live)}")
    for k, name in enumerate(concept_names):
        lm = [m for m in live if m['know'] == k]
        cf0 = [m for m in lm if m['field'] == 0]
        print(f"concept {k} ({name}): {len(lm)} live, {len(cf0)} content")
        if name in ("joke", "hypothetical"):
            print("  content bytes:", sorted(set(m['bytes'] for m in cf0)))

    # provenance of the firing markers of interest
    for bg in ["do we", "if the", "it is", "why did"]:
        print(f"--- provenance of {bg!r} ---")
        for m in markers:
            if m['bytes'] == bg and m['field'] == 0:
                print(f"  know={concept_names[m['know']]} status={m['status']} support={m['support']} installed_by={m['installed_by']}")

    # verify the 7 misses reproduce
    sinc3 = load("sinc3.txt")
    miss_ids = ["si3_12","si3_13","si3_14","si3_15","si3_16","si3_18","si3_20"]
    print("--- miss reproduction ---")
    for r in sinc3:
        if r[0] in miss_ids:
            utt, ctx, spk = r[3].lower(), r[2].lower(), r[1].lower()
            v, pname, scores = predict(utt, ctx, spk)
            fm = []
            for m in live:
                fb = [utt, ctx, spk][m['field']]
                if m['bytes'] in fb:
                    fm.append((concept_names[m['know']], m['bytes']))
            print(f"{r[0]} verdict={v} name={pname} firing={fm}")
