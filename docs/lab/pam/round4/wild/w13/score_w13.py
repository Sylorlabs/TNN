#!/usr/bin/env python3
"""score_w13.py — independent scorer for W13 epistemic-lease PAM.

Recomputes corroboration / renewal eligibility / staleness from the
instrument log + frozen stream, using the FULL existential (tag-indexed,
not the instrument's partner pointer). Checks K1/K6/LIVE/K3/K4/K5 and the
D-W13-* diagnostics. Deterministic.
"""
import hashlib, sys
from collections import Counter, defaultdict

STREAM = "/home/hatch/workspace/tnn-lab/pam/round4/wild/w13/w13_stream.txt"

def snap_time(t):
    return t - (t % 3)

def main():
    logpath = sys.argv[1]
    lines = open(logpath).read().splitlines()
    grants, checks, finals, summary = {}, [], {}, None
    for ln in lines:
        f = ln.split("|")
        if f[0] == "G":
            grants[int(f[1])] = dict(kind=f[2], granted=int(f[3]),
                                     expires=int(f[4]), src=f[5])
        elif f[0] == "C":
            checks.append((int(f[1]), int(f[2]), int(f[3]), f[4]))
        elif f[0] == "L":
            finals[int(f[1])] = dict(kind=f[2], granted=int(f[3]),
                                     expires=int(f[4]), renewed=int(f[5]),
                                     last_check=int(f[6]), staleness=int(f[7]))
        elif f[0] == "SUMMARY":
            summary = ln
    # --- stream cross-check ---
    stream = {}
    for ln in open(STREAM):
        f = ln.rstrip("\n").split("|")
        stream[int(f[0])] = dict(kind=f[1], ch=int(f[2]), tag=int(f[3]),
                                 conf=int(f[4]), mrgF=int(f[5]))
    assert len(stream) == 10050 and len(grants) == 10050
    assert len(checks) == 10050 and len(finals) == 10050
    g_ids = [i for i, s in stream.items() if s["kind"] == "G"]
    f_ids = [i for i, s in stream.items() if s["kind"] == "F"]
    assert len(g_ids) == 10000 and len(f_ids) == 50
    # M1 basic gate re-verified on genuine rows
    bad = [i for i in g_ids
           if not (stream[i]["conf"] >= 705 and stream[i]["mrgF"] >= 3588)]
    assert not bad, bad[:5]
    # tag uniqueness: genuine tags pair, false tags unique
    tagmap = defaultdict(list)
    for i, s in stream.items():
        tagmap[s["tag"]].append(i)
    for i in g_ids:
        assert len(tagmap[stream[i]["tag"]]) == 2, i
    for i in f_ids:
        assert len(tagmap[stream[i]["tag"]]) == 1, i
    # per-lease table keyed by stream ordinal
    ord_of = {}
    leases = []
    for idx, ln in enumerate(open(STREAM)):
        lid = int(ln.split("|")[0])
        ord_of[lid] = idx
    N = 10050
    tag = [0] * N; ch = [0] * N; kind = [0] * N
    granted = [0] * N
    for lid, o in ord_of.items():
        s = stream[lid]
        tag[o] = s["tag"]; ch[o] = s["ch"]
        kind[o] = 0 if s["kind"] == "G" else 1
        granted[o] = o
        g = grants[lid]
        assert g["granted"] == o and g["expires"] == o + 10, lid
        assert (g["kind"] == "G") == (kind[o] == 0)
    fin_renewed = [0] * N; fin_last = [0] * N; fin_exp = [0] * N
    for lid, o in ord_of.items():
        fl = finals[lid]
        fin_renewed[o] = fl["renewed"]; fin_last[o] = fl["last_check"]
        fin_exp[o] = fl["expires"]
        assert fl["granted"] == o
    # --- independent check verification (full existential via tag index) ---
    tagidx = defaultdict(list)
    for o in range(N):
        tagidx[tag[o]].append(o)
    max_stale = 0
    stale_hist = Counter()
    per_step = Counter()
    mism = 0
    for (lid, t, st, dec) in checks:
        o = ord_of[lid]
        s = snap_time(t)
        assert st == t - s, (lid, t, st)
        assert st <= 3, (lid, st)
        max_stale = max(max_stale, st)
        stale_hist[st] += 1
        per_step[t] += 1
        # snapshot expires_at for every lease as of s:
        # renewal visible iff renewed and last_check < s (refresh-before-scan)
        cor = False
        for j in tagidx[tag[o]]:
            if j == o:
                continue
            if ch[j] == ch[o]:
                continue
            if abs(granted[j] - granted[o]) > 3:
                continue
            if granted[j] > s:
                continue
            sexp = granted[j] + 10 + (10 if (fin_renewed[j] and fin_last[j] < s) else 0)
            if granted[j] <= t < sexp:
                cor = True
                break
        want = "RENEW" if cor else "EXPIRE"
        if want != dec:
            mism += 1
            if mism <= 5:
                print("MISMATCH", lid, t, "want", want, "got", dec)
    assert mism == 0, mism
    # --- bars ---
    g_renew = sum(1 for o in range(N) if kind[o] == 0 and fin_renewed[o])
    f_renew = sum(1 for o in range(N) if kind[o] == 1 and fin_renewed[o])
    # K1: no false renewed; none active past first expiry
    k1_renew = f_renew
    k1_active = sum(1 for o in range(N) if kind[o] == 1 and fin_exp[o] != granted[o] + 10)
    # K6: false-check staleness (already asserted <=3 for all; isolate falses)
    f_stale_max = max(st for (lid, t, st, dec) in checks if kind[ord_of[lid]] == 1)
    live = g_renew / 10000
    k3 = g_renew / 10000  # all leases checked; none "still within first window"
    maxwork = max(per_step.values())
    assert maxwork <= 64
    assert N <= 16384
    # --- diagnostics ---
    # D-W13-2 backlog: due(t) = granted+10 <= t <= last_check ; checked(t)
    due_hist = Counter(); chk_hist = Counter()
    for o in range(N):
        chk_hist[fin_last[o]] += 1
        for t in range(granted[o] + 10, fin_last[o] + 1):
            due_hist[t] += 1
    max_backlog = max((due_hist[t] - chk_hist.get(t, 0)) for t in due_hist)
    # D-W13-3 false lifetimes
    f_life = [(lid, finals[lid]["granted"], finals[lid]["expires"],
               finals[lid]["last_check"]) for lid in sorted(f_ids)]
    print("== W13 score ==")
    print(f"grants={len(grants)} checks={len(checks)} finals={len(finals)}")
    print(f"K1: false_renewed={k1_renew} false_past_first_expiry={k1_active}")
    print(f"K6: max_false_staleness={f_stale_max} max_all_staleness={max_stale}")
    print(f"LIVE(F3): genuine_renew={g_renew}/10000 = {live:.4f} (bar 0.90)")
    print(f"K3: influence={g_renew}/10000 = {k3:.4f} (bar 0.6678)")
    print(f"K4: max_per_step_checks={maxwork} (budget 64); table {N}<=16384")
    print(f"K5: all_checked={all(fin_last[o]>=0 for o in range(N))}")
    print(f"D-W13-1 staleness_hist={dict(sorted(stale_hist.items()))}")
    print(f"D-W13-2 max_backlog(due-checked)={max_backlog}")
    print(f"D-W13-3 false lifetimes (lid,granted,expires,checked): "
          f"{f_life[0]} ... {f_life[-1]} (n={len(f_life)})")
    print("summary:", summary)
    # verdict booleans
    ok_k1 = (k1_renew == 0 and k1_active == 0)
    ok_k6 = f_stale_max <= 3
    ok_live = live >= 0.90
    ok_k3 = k3 >= 0.6678
    ok_k4 = maxwork <= 64
    print(f"VERDICT_BOOLS K1={ok_k1} K6={ok_k6} LIVE={ok_live} K3={ok_k3} K4={ok_k4}")
    if not (ok_k1 and ok_k6 and ok_k4):
        print("RESULT: KILL")
    elif not (ok_live and ok_k3):
        print("RESULT: HOLD")
    else:
        print("RESULT: SURVIVE")

if __name__ == "__main__":
    main()
