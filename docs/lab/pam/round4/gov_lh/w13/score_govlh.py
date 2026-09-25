#!/usr/bin/env python3
"""score_govlh.py — independent scorer for W13 GOV-LH variants (PREREG_W13_GOVLH.md).

Recomputes renewal eligibility per the variant rule from the instrument log +
stream, using the FULL existential (tag-indexed, not the instrument's partner
pointer). Checks K1/K1-adv/K6/LIVE/K4/K5 and the D-GOVLH-* diagnostics.
Deterministic. Usage: score_govlh.py <log> <stream> <variant f|a|b>
(log may be .gz — read via gzip.)
"""
import gzip, sys
from array import array
from collections import Counter, defaultdict

def snap_time(t):
    return t - (t % 3)

def opener(p):
    return gzip.open(p, "rt") if p.endswith(".gz") else open(p)

def main():
    logpath, streampath, variant = sys.argv[1], sys.argv[2], sys.argv[3]
    assert variant in ("f", "a", "b")

    # ---- stream ----
    stream = {}
    for ln in open(streampath):
        f = ln.rstrip("\n").split("|")
        stream[int(f[0])] = dict(kind=f[1], ch=int(f[2]), tag=int(f[3]),
                                 conf=int(f[4]), mrgF=int(f[5]))
    N = len(stream)
    ord_of = {}
    for idx, ln in enumerate(open(streampath)):
        ord_of[int(ln.split("|")[0])] = idx
    tag = [0] * N; ch = [0] * N; kind = [0] * N  # 0=G 1=F-unique 2=F-pair
    for lid, o in ord_of.items():
        s = stream[lid]
        tag[o] = s["tag"]; ch[o] = s["ch"]
        kind[o] = 0 if s["kind"] == "G" else (2 if s["tag"] >= 2000000 else 1)
    g_ids = [o for o in range(N) if kind[o] == 0]
    fu_ids = [o for o in range(N) if kind[o] == 1]
    fp_ids = [o for o in range(N) if kind[o] == 2]
    ngen = len(g_ids)
    lid_of = [0] * N
    for lid, o in ord_of.items():
        lid_of[o] = lid
    # M1 gate re-verified on genuine rows
    bad = [o for o in g_ids
           if not (stream[lid_of[o]]["conf"] >= 705
                   and stream[lid_of[o]]["mrgF"] >= 3588)]
    assert not bad, bad[:5]
    # tag structure
    tagmap = defaultdict(list)
    for o in range(N):
        tagmap[tag[o]].append(o)
    for o in g_ids:
        assert len(tagmap[tag[o]]) == 2, o
    for o in fu_ids:
        assert len(tagmap[tag[o]]) == 1, o
    for o in fp_ids:
        assert len(tagmap[tag[o]]) == 2, o
    npairs = len(fp_ids) // 2

    # ---- single pass: grants + finals + check records ----
    fin_renewed = bytearray(N)
    fin_last = array("i", [-1]) * N
    fin_exp = array("i", [0]) * N
    c_ord = array("i")
    c_t = array("i")
    c_st = array("b")
    c_dec = bytearray()
    n_grants = 0
    with opener(logpath) as fh:
        for ln in fh:
            f = ln.split("|")
            if f[0] == "G":
                o = ord_of[int(f[1])]
                assert int(f[3]) == o and int(f[4]) == o + 10, f[1]
                n_grants += 1
            elif f[0] == "L":
                o = ord_of[int(f[1])]
                assert int(f[3]) == o
                fin_renewed[o] = int(f[5]); fin_last[o] = int(f[6])
                fin_exp[o] = int(f[4])
            elif f[0] == "C":
                c_ord.append(ord_of[int(f[1])])
                c_t.append(int(f[2])); c_st.append(int(f[3]))
                c_dec.append(1 if f[4].strip() == "RENEW" else 0)
    assert n_grants == N, (n_grants, N)
    n_checks = len(c_ord)
    assert n_checks == N, (n_checks, N)

    # ---- verify checks against the variant rule ----
    tagidx = defaultdict(list)
    for o in range(N):
        tagidx[tag[o]].append(o)
    max_stale = 0; f_stale_max = 0; fu_stale_max = 0
    stale_hist = Counter()
    per_step = array("i", [0]) * (N + 200)
    mism = 0
    div_live_snap = 0  # D-GOVLH-1
    for ci in range(n_checks):
        o = c_ord[ci]; t = c_t[ci]; st = c_st[ci]; dec = c_dec[ci]
        s = snap_time(t)
        assert st == t - s, (o, t, st)
        assert st <= 3, (o, st)
        max_stale = max(max_stale, st)
        if kind[o]:
            f_stale_max = max(f_stale_max, st)
            if kind[o] == 1:
                fu_stale_max = max(fu_stale_max, st)
        stale_hist[st] += 1
        per_step[t] += 1
        cor = False
        for j in tagidx[tag[o]]:
            if j == o or ch[j] == ch[o]:
                continue
            if abs(j - o) > 3:  # granted == ordinal
                continue
            # prereg §5 assertion: partner never renewed in the same step
            assert not (fin_renewed[j] and fin_last[j] == t), (o, j, t)
            gj = j
            if variant == "f":
                if gj > s:
                    continue
                sexp = gj + 10 + (10 if (fin_renewed[j] and fin_last[j] < s) else 0)
                if gj <= t < sexp:
                    cor = True
            elif variant == "a":
                if gj > s:
                    continue
                lexp = gj + 10 + (10 if (fin_renewed[j] and fin_last[j] < t) else 0)
                if t < lexp:
                    cor = True
            else:  # b
                if t < gj + 10:
                    cor = True
                elif fin_renewed[j] and fin_last[j] < t and t < gj + 20:
                    cor = True
        # D-GOVLH-1: live-ACTIVE vs snapshot-ACTIVE divergence (per check,
        # existential over corroborators)
        live_any = False; snap_any = False
        for j in tagidx[tag[o]]:
            if j == o or ch[j] == ch[o] or abs(j - o) > 3:
                continue
            gj = j
            lexp = gj + 10 + (10 if (fin_renewed[j] and fin_last[j] < t) else 0)
            if t < lexp:
                live_any = True
            if gj <= s:
                sexp = gj + 10 + (10 if (fin_renewed[j] and fin_last[j] < s) else 0)
                if gj <= t < sexp:
                    snap_any = True
        if live_any != snap_any:
            div_live_snap += 1
        want = 1 if cor else 0
        if want != dec:
            mism += 1
            if mism <= 5:
                print("MISMATCH", o, t, "want", want, "got", dec)
    assert mism == 0, mism

    # ---- bars ----
    g_renew = sum(1 for o in g_ids if fin_renewed[o])
    fu_renew = sum(1 for o in fu_ids if fin_renewed[o])
    fp_renew = sum(1 for o in fp_ids if fin_renewed[o])
    k1_active = sum(1 for o in fu_ids if fin_exp[o] > o + 10)
    live = g_renew / ngen
    maxwork = max(per_step)
    all_checked = all(fin_last[o] >= 0 for o in range(N))
    # D-GOVLH-2: per-pair outcomes
    pair_both = pair_m1 = pair_m2 = pair_none = 0
    for tj in sorted(set(tag[o] for o in fp_ids)):
        ms = sorted(tagmap[tj])
        r = [fin_renewed[m] for m in ms]
        if r == [1, 1]:
            pair_both += 1
        elif r == [1, 0]:
            pair_m1 += 1
        elif r == [0, 1]:
            pair_m2 += 1
        else:
            pair_none += 1
    # D-W13-2 backlog
    due = Counter(); chk = Counter()
    for o in range(N):
        chk[fin_last[o]] += 1
        for t in range(o + 10, fin_last[o] + 1):
            due[t] += 1
    max_backlog = max((due[t] - chk.get(t, 0)) for t in due) if due else 0

    print("== W13-GOVLH score variant=%s ==" % variant)
    print(f"stream: N={N} genuine={ngen} unique_false={len(fu_ids)} pair_false={len(fp_ids)} ({npairs} pairs)")
    print(f"K1: unique_false_renewed={fu_renew} unique_false_past_first_expiry={k1_active}")
    print(f"K1-adv: pair_member_renewed={fp_renew}/{len(fp_ids)} "
          f"(pairs: both={pair_both} m1only={pair_m1} m2only={pair_m2} none={pair_none})")
    print(f"K6: max_staleness_all={max_stale} max_false={f_stale_max} max_unique_false={fu_stale_max}")
    print(f"LIVE: genuine_renew={g_renew}/{ngen} = {live:.4f} (bar 0.90)")
    print(f"K4: max_per_step_checks={maxwork} (budget 64)")
    print(f"K5: all_checked={all_checked}")
    print(f"D-GOVLH-1 live_vs_snapshot_ACTIVE_divergent_checks={div_live_snap}/{N}")
    print(f"D-W13-1 staleness_hist={dict(sorted(stale_hist.items()))}")
    print(f"D-W13-2 max_backlog={max_backlog}")
    ok_k1 = (fu_renew == 0 and k1_active == 0)
    ok_k1adv = (fp_renew == 0)
    ok_k6 = max_stale <= 3
    ok_live = live >= 0.90
    ok_k4 = maxwork <= 64
    print(f"VERDICT_BOOLS K1={ok_k1} K1adv={ok_k1adv} K6={ok_k6} LIVE={ok_live} K4={ok_k4}")
    if not (ok_k1 and ok_k6 and ok_k4):
        print("RESULT: KILL")
    elif not ok_k1adv:
        print("RESULT: DEAD (K1-adv)")
    elif not ok_live:
        print("RESULT: HOLD")
    else:
        print("RESULT: SURVIVE")

if __name__ == "__main__":
    main()
