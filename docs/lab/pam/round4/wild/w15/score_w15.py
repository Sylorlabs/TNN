#!/usr/bin/env python3
"""score_w15.py — independent scorer for W15 staged-quarantine PAM.

Replays the frozen stream through an independent Python tier machine
(dict-based, not the instrument's arena hash) and asserts the instrument's
logged transitions match exactly. Checks F-K5/K1/XC/RG/LIVE/K4/K5 and the
D-W15-* diagnostics. Deterministic.
"""
import sys
from collections import Counter, defaultdict

STREAM = "/home/hatch/workspace/tnn-lab/pam/round4/wild/w15/w15_stream.txt"
WIN = 5

def main():
    logpath = sys.argv[1]
    # --- parse instrument log ---
    trans = []   # (tag, frm, to, step, extra...)
    finals = {}  # tag -> (kind, tier, mask, t12)
    summary = None
    for ln in open(logpath):
        f = ln.rstrip("\n").split("|")
        if f[0] == "T":
            trans.append((int(f[1]), int(f[2]), int(f[3]), int(f[4]),
                          tuple(f[5:])))
        elif f[0] == "F":
            finals[int(f[1])] = (f[2], int(f[3]), int(f[4]), int(f[5]))
        elif f[0] == "SUMMARY":
            summary = ln.rstrip("\n")
    # --- independent Python tier machine ---
    tags = {}  # tag -> dict(tier, mask, t12, kind, ls[3], sig, max_tier)
    py_trans = []
    events = []
    for ln in open(STREAM):
        f = ln.rstrip("\n").split("|")
        events.append((int(f[0]), f[1], int(f[2]), int(f[3]), int(f[4]),
                       int(f[5])))
    assert len(events) == 5250
    for now, (eid, kind, ch, tag, sig, contra) in enumerate(events):
        st = tags.get(tag)
        if st is None:
            st = dict(tier=0, mask=0, t12=-1, kind=kind,
                      ls=[-1, -1, -1], sig=sig, max_tier=0)
            tags[tag] = st
        assert st["kind"] == kind, (tag, st["kind"], kind)
        if contra == 1:
            assert sig != st["sig"], tag
            if st["tier"] > 0:
                py_trans.append((tag, st["tier"], st["tier"] - 1, now,
                                 ("DEMOTE",)))
                st["tier"] -= 1
        else:
            if st["tier"] == 0:
                st["tier"] = 1; st["max_tier"] = 1
                st["mask"] |= (1 << ch); st["ls"][ch] = now
                py_trans.append((tag, 0, 1, now, ()))
            elif st["tier"] == 1:
                found = None
                for c in range(3):
                    if c != ch and st["ls"][c] >= 0 \
                       and now - st["ls"][c] <= WIN:
                        found = (c, st["ls"][c])
                st["mask"] |= (1 << ch); st["ls"][ch] = now
                if found:
                    st["tier"] = 2; st["max_tier"] = 2; st["t12"] = now
                    py_trans.append((tag, 1, 2, now,
                                     (str(found[0]), str(found[1]))))
            elif st["tier"] == 2:
                new_ch = not (st["mask"] & (1 << ch))
                st["mask"] |= (1 << ch); st["ls"][ch] = now
                if new_ch and now - st["t12"] <= WIN:
                    st["tier"] = 3; st["max_tier"] = 3
                    py_trans.append((tag, 2, 3, now, (str(ch),)))
            else:
                st["ls"][ch] = now
    # --- transition equality ---
    assert len(py_trans) == len(trans), (len(py_trans), len(trans))
    mism = 0
    for a, b in zip(py_trans, trans):
        if a != b:
            mism += 1
            if mism <= 5:
                print("MISMATCH py=", a, " inst=", b)
    assert mism == 0, mism
    # --- finals equality ---
    assert len(finals) == len(tags) == 1868
    for tag, st in tags.items():
        fk, ft, fm, ft12 = finals[tag]
        assert fk == st["kind"] and ft == st["tier"] \
            and fm == st["mask"] and ft12 == st["t12"], tag
    # --- bars ---
    g_tags = [t for t, s in tags.items() if s["kind"] == "G"
              and tags[t]["sig"] == s["sig"]]
    # genuine non-contradiction tags: 1668 (1666 triples + 2 singles)
    f_tags = [t for t, s in tags.items() if s["kind"] == "F"]
    assert len(f_tags) == 200
    wrong_tags = [t for t in f_tags if 900000 <= t <= 900029]
    assert len(wrong_tags) == 30
    f_at_t3 = [t for t in f_tags if tags[t]["tier"] == 3]
    w_at_t3 = [t for t in wrong_tags if tags[t]["tier"] == 3]
    # KB-W15-XC: every logged T1->T2 has a valid corroboration (recomputed)
    xc_bad = 0
    for (tag, frm, to, step, extra) in trans:
        if frm == 1 and to == 2:
            cc, cs = int(extra[0]), int(extra[1])
            # verify: same tag, different ch, within window of step
            ev = events[step]
            assert ev[3] == tag
            ok = False
            for s2 in range(max(0, step - WIN), step):
                e2 = events[s2]
                if e2[3] == tag and e2[2] == cc and e2[2] != ev[2]:
                    ok = True
            if not ok:
                xc_bad += 1
    # KB-W15-RG: 50 contradictions -> 50 demotions
    demotes = [t for t in trans if t[4] == ("DEMOTE",)]
    contra_tags = [events[i][3] for i in range(len(events))
                   if events[i][5] == 1]
    rg_ok = (len(demotes) == 50 and len(contra_tags) == 50
             and all(tags[t]["tier"] == 2 for t in contra_tags))
    # LIVE: genuine triple percepts reaching T3
    triple_percepts = sum(1 for (eid, k, ch, t, s, c) in events
                          if k == "G" and c == 0 and t < 1666)
    reached = sum(1 for (eid, k, ch, t, s, c) in events
                  if k == "G" and c == 0 and t < 1666
                  and tags[t]["max_tier"] == 3)
    live = reached / 5000
    # K3: genuine T3 rate (final)
    g_t3_final = sum(1 for t in tags if tags[t]["kind"] == "G"
                     and t < 1668 and tags[t]["tier"] == 3)
    # diagnostics
    hist = Counter((tags[t]["kind"], tags[t]["tier"]) for t in tags)
    f_maxtier = Counter(tags[t]["max_tier"] for t in f_tags)
    print("== W15 score ==")
    print(f"transitions={len(trans)} tags={len(tags)}")
    print(f"F-K5: false_at_T3={len(f_at_t3)}/200")
    print(f"K1: wrong_at_T3={len(w_at_t3)}/30")
    print(f"KB-W15-XC: bad_T1T2={xc_bad}")
    print(f"KB-W15-RG: demotions={len(demotes)}/50 all_T3_to_T2={rg_ok}")
    print(f"LIVE: triple_percepts_reached_T3={reached}/{triple_percepts}; "
          f"rate_vs_5000={live:.4f} (bar 0.90)")
    print(f"K3: genuine_final_T3_tags={g_t3_final}/1668")
    print(f"D-W15-1 tier_hist(kind,tier)={dict(sorted(hist.items()))}")
    print(f"D-W15-2 false_max_tier={dict(sorted(f_maxtier.items()))}")
    print(f"D-W15-3 demote_tags_sorted={sorted(contra_tags)[:5]}..."
          f"{sorted(contra_tags)[-3:]} (n=50)")
    print("summary:", summary)
    ok = (not f_at_t3 and not w_at_t3 and xc_bad == 0 and rg_ok)
    print(f"VERDICT_BOOLS FK5={not f_at_t3} K1={not w_at_t3} "
          f"XC={xc_bad==0} RG={rg_ok} LIVE={live>=0.90}")
    if not ok:
        print("RESULT: KILL")
    elif live < 0.90:
        print("RESULT: HOLD")
    else:
        print("RESULT: SURVIVE")

if __name__ == "__main__":
    main()
