#!/usr/bin/env python3
"""Author + verify C2 extended probes (what-if / where-do sincere lookalikes).

Rules (mirroring ANTICONFOUND.md + C2 mandate):
- 10 probes per family, format id|speaker|ctx|utterance|E
- target bigram present as case-insensitive substring (learner's has_sub)
- zero >=16-byte overlap with: all curriculum utterances, all corpus items
  (orig48, volnew48, de32)
- speakers rotated through the six frozen names; ctx mirrors frozen LK probes
- what-if probes use the NOMINALIZED sincere frame (the frame D E-items teach);
  where-do probes use genuine questions with third-person subjects, avoiding
  'where do we' / 'where do they' (surviving longer n-grams per red-team A4)
"""
import os, itertools

BASE = "/home/hatch/workspace/tnn-native-lab-work/docs/lab/epistemics/utterance_types"
CUR = BASE + "/crew2/curriculum"
WORK = "/home/hatch/workspace/sinc_exp/exp2c/work"
OUT = "/home/hatch/workspace/sinc_exp/exp2d/stage2"

def utts_of(path):
    out = []
    for line in open(path, encoding="utf-8", errors="replace"):
        line = line.rstrip("\n")
        if not line or line.startswith("#"):
            continue
        p = line.split("|")
        if len(p) >= 4:
            out.append(p[3].lower())
    return out

forbidden = []
for fn in sorted(os.listdir(CUR)):
    if fn.endswith(".txt"):
        forbidden += utts_of(os.path.join(CUR, fn))
for cf in ("cal_abc.txt", "cal_vol2.txt", "cal_de.txt"):
    forbidden += utts_of(os.path.join(WORK, cf))
print(f"forbidden utterances: {len(forbidden)}")

def violations(u):
    u = u.lower()
    hits = []
    for i in range(len(u)-15):
        s = u[i:i+16]
        for f in forbidden:
            if s in f:
                hits.append(s)
                break
    return hits

SPEAKERS = ["Mara", "Dev", "Priya", "Theo", "June", "Sam"]
CTX = "says evenly"  # mirrors frozen sinc3 LK probes (si3_11..20)

wi_candidates = [
    "The board rejected every what if as fantasy.",
    "Her memo answers the what ifs we raised.",
    "Park the what ifs until the audit ends.",
    "Their what if drills prepared the crew well.",
    "We shelved the what if memos for now.",
    "The handbook addresses each what if briefly.",
    "His what if sketches guided the redesign.",
    "Enough with what ifs; we need a verdict.",
    "The panel waved off each what if politely.",
    "She catalogued the what ifs by topic.",
    "Our charter bans idle what if debates.",
    "They archived the what if threads yesterday.",
    "The syllabus lists the what ifs by week.",
    "The minutes record each what if raised.",
    "We tabled the what if discussion early.",
    "The guide covers common what ifs first.",
]
wd_candidates = [
    "Where do the couriers leave parcels now?",
    "Where do night trains stop after midnight?",
    "Where do the bakers buy their flour?",
    "Where do visitors park near the harbor?",
    "Where do workers eat around here?",
    "Where do the gulls roost in winter?",
    "Where do newcomers register for classes?",
    "Where do the janitors store the ladders?",
    "Where do taxis wait at the station?",
    "Where do the gardeners draw water?",
    "Where do the clerks file the invoices?",
    "Where do hikers refill bottles nearby?",
]

def build(cands, prefix, bigram):
    ok = []
    for u in cands:
        assert bigram in u.lower(), (prefix, u)
        v = violations(u)
        # also forbid the surviving longer n-grams as substrings
        bad_ng = []
        for ng in ("where do we", "where do they", "what if the"):
            if ng in u.lower():
                bad_ng.append(ng)
        status = "OK" if (not v and not bad_ng) else "VIOL"
        print(f"[{status}] {prefix}: {u}" + (f" 16b:{v[:2]}" if v else "") + (f" ng:{bad_ng}" if bad_ng else ""))
        if not v and not bad_ng:
            ok.append(u)
    return ok

print("--- what-if candidates ---")
wi_ok = build(wi_candidates, "wi", "what if")
print("--- where-do candidates ---")
wd_ok = build(wd_candidates, "wd", "where do")
assert len(wi_ok) >= 10 and len(wd_ok) >= 10, "not enough clean candidates"

os.makedirs(OUT, exist_ok=True)
spk = itertools.cycle(SPEAKERS)
with open(f"{OUT}/sinc3x_wi.txt", "w") as f:
    for i, u in enumerate(wi_ok[:10]):
        f.write(f"sxwi_{i+1:02d}|{next(spk)}|{CTX}|{u}|E\n")
with open(f"{OUT}/sinc3x_wd.txt", "w") as f:
    for i, u in enumerate(wd_ok[:10]):
        f.write(f"sxwd_{i+1:02d}|{next(spk)}|{CTX}|{u}|E\n")
print("wrote", f"{OUT}/sinc3x_wi.txt", f"{OUT}/sinc3x_wd.txt")
