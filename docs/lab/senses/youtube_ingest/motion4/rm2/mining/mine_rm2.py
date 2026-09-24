#!/usr/bin/env python3
"""mine_rm2.py — RM2 mining (MOTION4 prereg §6/RM2).

Zero RNG. Enumerates candidate 8-frame clips at baselines b in {2,3,4}
(source frames t + j*b, j=0..7), scores each with the numpy M3 replica
(bit-verified against the frozen verdict binary), and ranks uniform-
translation and still candidates for hand-labeling per the frozen
B3_LABELS.md rubric + pair-level vote-analysis procedure.

Outputs: rm2_mine_candidates.tsv (all scored candidates, sorted),
rm2_mine_top.tsv (shortlist for viewing).
"""
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m3_numpy as N  # noqa: E402

MINE = os.path.dirname(os.path.abspath(__file__))
FSZ = 64 * 64 * 3
BASELINES = [2, 3, 4]
STEP = 15  # source-frame stride between candidate starts
VIDS = ["0_jNjpVxUt0", "9AwUsf8HzVI", "Eoo4HzILB-M", "OQSNhk5ICTI",
        "bwJ-TNu0hGM", "kcfs1-ryKWE", "uKNQCPXDNdc"]
NAMES = ["STILL", "N", "NE", "E", "SE", "S", "SW", "W", "NW"]


def load_raw(vid):
    with open(os.path.join(MINE, vid + ".raw"), "rb") as f:
        data = f.read()
    n = len(data) // FSZ
    return [data[i * FSZ:(i + 1) * FSZ] for i in range(n)]


def main():
    cands = []
    for vid in VIDS:
        frames = load_raw(vid)
        n = len(frames)
        for b in BASELINES:
            span = 7 * b
            t = 0
            while t + span < n:
                clip = [frames[t + j * b] for j in range(8)]
                lums = [N.lum_plane(f) for f in clip]
                r = N.clip_result(lums)
                pw = r["pair_wins"]
                # uniform-motion: count pairs voting each direction
                counts = {}
                for w in pw:
                    counts[w] = counts.get(w, 0) + 1
                best_dir = max(counts, key=lambda k: (counts[k], -k))
                agree = counts[best_dir]
                still_like = r["e_total"] == 0 or (r["ebar"] < 64 and r["coh_pm"] < 667)
                cands.append({
                    "vid": vid, "b": b, "t": t,
                    "win": r["win"], "coh_pm": r["coh_pm"],
                    "g_pm": r["g_pm"], "ebar": r["ebar"],
                    "n_vote": r["n_vote"], "e_total": r["e_total"],
                    "pair_wins": ",".join(str(w) for w in pw),
                    "agree": agree, "agree_dir": best_dir,
                    "still_like": still_like,
                })
                t += STEP

    # rank motion candidates: strong pair agreement on a direction + evidence
    motion = [c for c in cands if c["agree_dir"] != 0 and c["agree"] >= 5]
    motion.sort(key=lambda c: (c["agree"], c["e_total"]), reverse=True)
    # rank still candidates: exact stills first
    still = [c for c in cands if c["still_like"]]
    still.sort(key=lambda c: c["e_total"])

    with open(os.path.join(MINE, "rm2_mine_candidates.tsv"), "w") as f:
        f.write("# vid\tb\tt\twin\tcoh_pm\tg_pm\tebar\tn_vote\te_total\t"
                "agree\tagree_dir\tpair_wins\tstill_like\n")
        for c in motion + still:
            f.write("\t".join(str(c[k]) for k in
                    ("vid", "b", "t", "win", "coh_pm", "g_pm", "ebar",
                     "n_vote", "e_total", "agree", "agree_dir",
                     "pair_wins", "still_like")) + "\n")

    # shortlist: top 3 motion + top 1 still per (vid, b) for viewing
    seen = set()
    short = []
    for c in motion:
        key = (c["vid"], c["b"], "M")
        if sum(1 for s in short if (s[0], s[1]) == (c["vid"], c["b"]) and s[2] == "M") < 2:
            short.append((c["vid"], c["b"], "M", c))
    for c in still:
        key = (c["vid"], c["b"], "S")
        if sum(1 for s in short if (s[0], s[1]) == (c["vid"], c["b"]) and s[2] == "S") < 1:
            short.append((c["vid"], c["b"], "S", c))
    short.sort(key=lambda s: (s[0], s[1], s[2], s[3]["t"]))
    with open(os.path.join(MINE, "rm2_mine_top.tsv"), "w") as f:
        f.write("# kind\tvid\tb\tt\tagree_dir\tpair_wins\te_total\n")
        for vid, b, kind, c in short:
            f.write("%s\t%s\t%d\t%d\t%s\t%s\t%d\n"
                    % (kind, vid, b, c["t"],
                       NAMES[c["agree_dir"]] if kind == "M" else "STILL",
                       c["pair_wins"], c["e_total"]))
    print("candidates scored: %d (motion-strong %d, still-like %d)"
          % (len(cands), len(motion), len(still)))
    print("shortlist: %d" % len(short))


if __name__ == "__main__":
    sys.exit(main())
