#!/usr/bin/env python3
"""Reconstruct per-probe predict() outcomes from a committed run's MDUMP lines.

Implements the frozen predict() voting rule exactly:
- live markers: status 1 (PROVISIONAL) or 2 (COMMITTED); concept status==2
  (all 5 utterance-type concepts are taught with status 2 via know_teach).
- a marker fires iff its bytes are a plain substring of the probe's lowered
  field (0=UTT, 1=CTX, 2=SPK).
- concept score = # firing markers; winner = strictly greatest score;
  ties broken by name_less (lexicographic on concept name).
- v=1 (WITHHOLD) iff some concept scores >0 else v=0 (ENDORSE).
- probe correct iff v == ev (ev=0 for E/SINC probes).

Validates by comparing reconstructed aggregates to the run's 2C_CURVE lines.
"""
import sys, re

NAMES = ["sarcasm", "joke", "hypothetical", "quotation", "roleplay"]

def parse_mdump(path):
    markers = []  # (concept0, field, status, support, bytes)
    for line in open(path, encoding="utf-8", errors="replace"):
        if line.startswith("MDUMP|"):
            p = line.rstrip("\n").split("|", 5)
            markers.append((int(p[1]) - 1, int(p[2]), int(p[3]), int(p[4]), p[5]))
    return markers

def predict(markers, utt, ctx, spk):
    fields = [utt.lower(), ctx.lower(), spk.lower()]
    scores = [0] * 5
    fired = []  # (concept, bytes) for diagnosis
    for (k, f, st, sup, b) in markers:
        if st not in (1, 2):
            continue
        if 0 <= k < 5 and b and b in fields[f]:
            scores[k] += 1
            fired.append((NAMES[k], b))
    best, bests = -1, 0
    for k in range(5):
        s = scores[k]
        if s > 0:
            take = False
            if best == -1:
                take = True
            elif s > bests:
                take = True
            elif s == bests and NAMES[k] < NAMES[best]:
                take = True
            if take:
                best, bests = k, s
    v = 1 if best != -1 else 0
    return v, (NAMES[best] if best != -1 else None), scores, fired

def load_probes(path):
    probes = []
    for line in open(path):
        line = line.rstrip("\n")
        if not line or line.startswith("#"):
            continue
        p = line.split("|")
        # id|speaker|ctx|utterance|signal
        sig = p[4] if len(p) > 4 else "E"
        ev = 1 if sig == "W" else 0
        probes.append((p[0], p[1], p[2], p[3], ev))
    return probes

def curve2c(path):
    out = {}
    for line in open(path, encoding="utf-8", errors="replace"):
        if line.startswith("2C_CURVE|"):
            p = line.rstrip("\n").split("|")
            t = int(p[1])
            d = {}
            for i in range(2, len(p) - 1, 2):
                d[p[i]] = int(p[i + 1])
            out[t] = d
    return out

def main():
    run_path, probe_path, tnum = sys.argv[1], sys.argv[2], int(sys.argv[3])
    markers = parse_mdump(run_path)
    probes = load_probes(probe_path)
    dp = [p for p in probes[0:10]]
    lk = [p for p in probes[10:20]]
    ok_dp = ok_lk = 0
    print(f"--- {run_path} type {tnum}: {len(markers)} markers ---")
    for section, plist, tag in (("DP", dp, 0), ("LK", lk, 10)):
        for j, (pid, spk, ctx, utt, ev) in enumerate(plist):
            v, winner, scores, fired = predict(markers, utt, ctx, spk)
            ok = (v == ev)
            if section == "DP" and ok:
                ok_dp += 1
            if section == "LK" and ok:
                ok_lk += 1
            if not ok:
                fire_str = ", ".join(f"{c}:{b}" for c, b in fired[:8])
                print(f"  MISS {pid} [{utt[:48]}] -> v={v} winner={winner} scores={scores} fired=[{fire_str}]")
    print(f"reconstructed: DP={ok_dp}/10 LK={ok_lk}/10")
    curves = curve2c(run_path)
    if tnum in curves:
        c = curves[tnum]
        print(f"committed 2C_CURVE: DP={c['DP']} LK={c['LK']}  match={c['DP']==ok_dp and c['LK']==ok_lk}")

if __name__ == "__main__":
    main()
