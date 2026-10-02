#!/usr/bin/env python3
"""H7 scope-indexed-marker SEPARATION AUDIT (crew1, broader-fix). See header."""
import sys
sys.path.insert(0, "/home/hatch/workspace/h7_broaderfix_staging/crew1")
import sim_learn as S

CUR = "/home/hatch/workspace/h7_broaderfix_staging/crew1/evidence_input/curriculum"

def load(fname):
    rows = []
    with open(f"{CUR}/{fname}") as f:
        for line in f:
            line = line.rstrip("\n").rstrip("\r")
            if line.strip():
                rows.append(line.split("|"))
    return rows

def first_occ(hay, ndl):
    i = hay.find(ndl)
    return i  # -1 if absent

def scope_features(utt, ndl):
    """Generic structural features of the first occurrence of ndl in utt.
    utt: lowered utterance string. Returns dict of integer features."""
    s, starts, ends = S.words_of(utt)
    pos = first_occ(s, ndl)
    assert pos >= 0, (utt, ndl)
    # word index of the word containing pos
    widx = None
    for wi, (a, b) in enumerate(zip(starts, ends)):
        if a <= pos < b:
            widx = wi
            break
    assert widx is not None
    nwords = len(starts)
    commas_before = s[:pos].count(",")
    # sentence index: count of [.?!] before pos
    sent_idx = sum(1 for ch in s[:pos] if ch in ".?!")
    return {
        "S_comma": commas_before,
        "S_widx": widx,
        "S_quart": (4 * widx) // nwords if nwords else 0,
        "S_sent": sent_idx,
        "nwords": nwords,
    }

ex_cache = {}
def install_field(m):
    """Installing exemplar's bytes for the marker's own field (lowered)."""
    tag = m["installed_by"]  # e.g. "ex3_01"
    t, n = tag[2], int(tag[4:])
    key = f"ex{t}.txt"
    if key not in ex_cache:
        ex_cache[key] = load(key)
    rows = ex_cache[key]
    r = rows[n - 1]
    return [r[3].lower(), r[2].lower(), r[1].lower()][m["field"]]

def install_utt(m):
    return install_field(m)  # kept for reporting; field-aware version above

def firing_markers_on(utt, ctx, spk, live):
    out = []
    for m in live:
        fb = [utt, ctx, spk][m["field"]]
        if m["bytes"] in fb:
            out.append(m)
    return out

live = S.build()
by_concept = {}
for m in live:
    by_concept.setdefault(S.concept_names[m["know"]], []).append(m)

FEATS = ["S_comma", "S_widx", "S_quart", "S_sent"]

print("=" * 78)
print("PART A: the 7 sinc_lk_3 misses — per-miss scope separation")
print("=" * 78)
sinc3 = load("sinc3.txt")
miss_ids = ["si3_12", "si3_13", "si3_14", "si3_15", "si3_16", "si3_18", "si3_20"]
results = {}
for r in sinc3:
    if r[0] not in miss_ids:
        continue
    iid, utt = r[0], r[3].lower()
    ctx, spk = r[2].lower(), r[1].lower()
    fm = firing_markers_on(utt, ctx, spk, live)
    assert len(fm) == 1, (iid, fm)
    m = fm[0]
    cname = S.concept_names[m["know"]]
    bg = m["bytes"]
    inst_fb = install_field(m)
    probe_fb = [utt, ctx, spk][m["field"]]
    fs_install = scope_features(inst_fb, bg)
    fs_probe = scope_features(probe_fb, bg)
    results[iid] = {}
    print(f"\n{iid} | {r[3]!r}")
    print(f"  firing marker: ({cname}, {bg!r}) installed by {m['installed_by']}: {inst_fb!r}")
    for f in FEATS:
        a, b = fs_install[f], fs_probe[f]
        sep = "SEPARATES" if a != b else "same"
        results[iid][f] = (a != b)
        print(f"  {f:8s}: install={a} probe={b} -> {sep}")

print("\n" + "=" * 78)
print("PART B: joke NO items (must stay WITHHOLD, need >=16/20) — regression check")
print("=" * 78)
no2 = load("no2.txt")
for f in FEATS:
    still = 0
    lost = []
    for r in no2:
        utt = r[3].lower()
        fm = firing_markers_on(utt, r[2].lower(), r[1].lower(), live)
        ok = False
        for m in fm:
            ifb = install_field(m)
            pfb = [utt, r[2].lower(), r[1].lower()][m["field"]]
            try:
                if scope_features(ifb, m["bytes"])[f] == scope_features(pfb, m["bytes"])[f]:
                    ok = True
                    break
            except AssertionError:
                pass
        if ok:
            still += 1
        else:
            lost.append(r[0])
    print(f"{f:8s}: {still}/20 still WITHHOLD" + (f"  LOST: {lost}" if lost else ""))

print("\n" + "=" * 78)
print("PART C: tr3 genuine hypotheticals (must stay WITHHOLD) — regression check")
print("=" * 78)
tr3 = load("tr3.txt")
for f in FEATS:
    still = 0
    lost = []
    for r in tr3:
        utt = r[3].lower()
        fm = firing_markers_on(utt, r[2].lower(), r[1].lower(), live)
        ok = False
        for m in fm:
            ifb = install_field(m)
            pfb = [utt, r[2].lower(), r[1].lower()][m["field"]]
            try:
                if scope_features(ifb, m["bytes"])[f] == scope_features(pfb, m["bytes"])[f]:
                    ok = True
                    break
            except AssertionError:
                pass
        if ok:
            still += 1
        else:
            lost.append(r[0])
    print(f"{f:8s}: {still}/20 still WITHHOLD" + (f"  LOST: {lost}" if lost else ""))

print("\n" + "=" * 78)
print("SUMMARY: misses fixed per scope function (need >=5/7 to build)")
print("=" * 78)
for f in FEATS:
    fixed = [iid for iid in miss_ids if results[iid][f]]
    print(f"{f:8s}: {len(fixed)}/7 fixed -> {fixed}")
