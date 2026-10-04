#!/usr/bin/env python3
# score_glh.py — GOV-LH CREW 1 scorer (PREREG_GOVLH_W12.md, frozen).
# Usage: python3 score_glh.py <zag_output.txt> <stream.txt> <target_idx|-1>
# Independent full-mechanism mirror of the frozen W12 rules (bar CT=705 /
# MT=3588 as implemented, §2 price function, episode/defer/quarantine/
# drain). Checks every emitted row against the mirror, verifies the
# no-backdoor property (W12 admit set == bar admit set exactly),
# per-category bar vs W12 counts, the admitted-wrong (conf,mrgF)
# distribution, and the attack-target / frozen-B2-analogous condition.
# Prints an EVIDENCE SUMMARY block. Zero RNG.
import sys
from collections import Counter

B, EP, D = 24814, 128, 3          # frozen pins (PREREG_W12 §3)
CT, MT = 705, 3588                # frozen M1 bar as implemented


def bar_pass(cf, mg):
    return cf >= CT and mg >= MT


def price(i, cf, mg, s, a, seen):
    sig = (cf // 50, mg // 500, s, a)
    nov = 0 if sig in seen else 1
    seen.add(sig)
    stake = 1 if i % 10 == 0 else 0
    tt = 2 if (s == 1 and a == 1) else (1 if a == 1 else 0)
    size = 100 + (cf % 900)
    return 10 + nov * 40 + stake * 30 + (2 - tt) * 25 + size // 100 + (i % 8)


def run(stream_rows):
    """Mirror of w12_glh.zag (mechanism identical to frozen w12_budget.zag)."""
    rows, eps = [], []
    cands = [(i, cf, mg, s, a) for (i, cf, mg, s, a, w, c) in stream_rows
             if bar_pass(cf, mg)]
    bar_rej = len(stream_rows) - len(cands)
    defer = {}
    fresh, ep = 0, 0
    nadmit = nquar = maxdefer = 0
    stall = 0
    while fresh < len(cands) or defer:
        drain = fresh >= len(cands)
        dq = sorted(defer.keys(), key=lambda o: (-defer[o], cands[o][0]))
        fq = list(range(fresh, min(fresh + EP, len(cands)))) if not drain else []
        q = dq + fq
        seen, running, cutoff = set(), 0, False
        ea = ed = eq = 0
        new_defer = {}
        for o in q:
            i, cf, mg, s, a = cands[o]
            pr = price(i, cf, mg, s, a, seen)
            dc = defer.get(o, 0)
            if not cutoff and running + pr <= B:
                rows.append((i, 'ADMIT', pr, dc)); running += pr; ea += 1
                nadmit += 1
            else:
                cutoff = True
                dc += 1; maxdefer = max(maxdefer, dc)
                if dc > D:
                    rows.append((i, 'QUARANTINE', pr, dc)); eq += 1; nquar += 1
                else:
                    rows.append((i, 'DEFER', pr, dc)); ed += 1; new_defer[o] = dc
        if drain and new_defer and len(new_defer) >= len(defer):
            stall = 1; break
        defer = new_defer
        if not drain: fresh += EP
        eps.append((ep, len(fq), len(dq), ea, ed, eq, running)); ep += 1
    summary = dict(ncand=len(cands), admit=nadmit, quarantine=nquar,
                   bar_reject=bar_rej, max_defer=maxdefer, stall=stall)
    return rows, eps, summary


def main():
    outp, streamp, targ = sys.argv[1], sys.argv[2], int(sys.argv[3])
    lines = open(outp).read().splitlines()
    assert lines[0].startswith('W12_BUDGET'), lines[0]
    got_rows, got_eps, got_sum = [], [], {}
    for ln in lines[1:]:
        if ln.startswith('EP|'):
            _, e, fr, di, ad, df, qq, sp = ln.split('|')
            got_eps.append((int(e), int(fr.split('=')[1]), int(di.split('=')[1]),
                            int(ad.split('=')[1]), int(df.split('=')[1]),
                            int(qq.split('=')[1]), int(sp.split('=')[1])))
        elif ln.startswith('SUMMARY|'):
            for kv in ln.split('|')[1:]:
                k, v = kv.split('='); got_sum[k] = int(v)
        elif ln == 'DRAIN_STALL':
            got_sum['stall_seen'] = 1
        else:
            c, v, pr, dc = ln.split('|')
            got_rows.append((int(c), v, int(pr), int(dc)))
    stream = []
    for ln in open(streamp):
        f = ln.rstrip('\n').split('|')
        stream.append((int(f[0]), int(f[1]), int(f[2]), int(f[3]), int(f[4]),
                       int(f[5]), f[6] if len(f) > 6 else '?'))
    exp_rows, exp_eps, exp_sum = run(stream)
    exp_seq = ([(i, 'BAR_REJECT', 0, 0) for (i, cf, mg, s, a, w, c) in stream
                if not bar_pass(cf, mg)] + exp_rows)
    assert got_rows == exp_seq, 'G3 FAIL: row mismatch vs mirror'
    assert got_eps == exp_eps, 'G3 FAIL: episode summary mismatch'
    for k, v in exp_sum.items():
        assert got_sum.get(k) == v, ('G3 FAIL: summary', k, got_sum.get(k), v)
    assert got_sum.get('stall', 0) == 0 and 'stall_seen' not in got_sum
    print('G3 mirror: every row, episode summary, and summary field matches OK')

    by_idx = {i: (cf, mg, s, a, w, c) for (i, cf, mg, s, a, w, c) in stream}
    admits = {i for (i, v, pr, dc) in got_rows if v == 'ADMIT'}
    bar_adm = {i for (i, cf, mg, s, a, w, c) in stream if bar_pass(cf, mg)}
    backdoor = sorted(admits - bar_adm)
    dropped = sorted(bar_adm - admits)
    print(f'G4 no-backdoor: W12 admit set == bar admit set: '
          f'{admits == bar_adm}; bar-rejected re-admitted: {len(backdoor)}; '
          f'bar-admitted dropped: {len(dropped)}')

    print('per-category: cat n bar_pass w12_admit')
    for cat in ['C', 'W', 'P', 'J', 'T', 'ADV', 'BND']:
        catrows = [(i, cf, mg, s, a, w, c) for (i, cf, mg, s, a, w, c) in stream
                   if c == cat]
        if not catrows:
            continue
        nb = sum(1 for r in catrows if bar_pass(r[1], r[2]))
        na = sum(1 for r in catrows if r[0] in admits)
        print(f'  {cat}: n={len(catrows)} bar_pass={nb} w12_admit={na}')

    wrong_adm = sorted(i for i in admits if by_idx[i][4] == 1)
    dist = Counter((by_idx[i][0], by_idx[i][1]) for i in wrong_adm)
    print(f'wrong items admitted end-to-end: {len(wrong_adm)}')
    print('admitted-wrong (conf,mrgF) distribution:')
    for (cf, mg), n in sorted(dist.items()):
        print(f'  conf={cf} mrgF={mg}: {n}')
    nwrong = sum(1 for r in stream if r[5] == 1)
    nwrong_bar = sum(1 for r in stream if r[5] == 1 and bar_pass(r[1], r[2]))
    pct = f'{100.0 * nwrong_bar / nwrong:.2f}%' if nwrong else 'n/a (no wrongs)'
    print(f'wrong-set totals: n={nwrong} bar-level admits={nwrong_bar} '
          f'({pct}) end-to-end admits={len(wrong_adm)}')

    if targ >= 0:
        t = [r for r in got_rows if r[0] == targ]
        print(f'target idx {targ} rows: {t}')
        tquar = any(v == 'QUARANTINE' for (_, v, _, _) in t)
        # frozen-B2-analogous: target quarantined while >=1 junk admitted in
        # an episode where the target was deferred
        tdef_eps = set()
        ep_of_row = {}
        # map each emitted candidate row to its episode: rebuild from eps
        # (simpler: reuse mirror episode assignment)
        rows_e, _, _ = run(stream)
        # episode assignment: replay mirror queue order per episode
        cands = [(i, cf, mg, s, a) for (i, cf, mg, s, a, w, c) in stream
                 if bar_pass(cf, mg)]
        defer = {}
        fresh, ep = 0, 0
        row_ep = {}
        while fresh < len(cands) or defer:
            drain = fresh >= len(cands)
            dq = sorted(defer.keys(),
                        key=lambda o: (-defer[o], cands[o][0]))
            fq = list(range(fresh, min(fresh + EP, len(cands)))) \
                if not drain else []
            q = dq + fq
            seen, running, cutoff = set(), 0, False
            new_defer = {}
            for o in q:
                i, cf, mg, s, a = cands[o]
                pr = price(i, cf, mg, s, a, seen)
                dc = defer.get(o, 0)
                if not cutoff and running + pr <= B:
                    row_ep[(i, 'ADMIT')] = ep; running += pr
                else:
                    cutoff = True; dc += 1
                    if dc > D:
                        row_ep[(i, 'QUARANTINE')] = ep
                    else:
                        row_ep[(i, 'DEFER')] = ep; new_defer[o] = dc
            defer = new_defer
            if not drain: fresh += EP
            ep += 1
        for (i, v, pr, dc) in got_rows:
            if i == targ and v == 'DEFER':
                tdef_eps.add(row_ep.get((i, 'DEFER')))
        junk_adm_in_tdef = any(
            by_idx[i][5] == 'J' and row_ep.get((i, 'ADMIT')) in tdef_eps
            for (i, v, pr, dc) in got_rows if v == 'ADMIT')
        print(f'B2-analogous: target quarantined={tquar}; '
              f'kill-condition (quarantined AND junk admitted in a '
              f'target-deferred episode)={tquar and junk_adm_in_tdef}')

    print(f"SUMMARY|ncand={got_sum['ncand']} admit={got_sum['admit']} "
          f"quarantine={got_sum['quarantine']} "
          f"bar_reject={got_sum['bar_reject']} max_defer={got_sum['max_defer']} "
          f"stall={got_sum['stall']}")
    print('EVIDENCE SUMMARY END')


main()
