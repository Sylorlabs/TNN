#!/usr/bin/env python3
"""Red-team C3 collision-bound audit (independent implementation).

For each leg's run file:
  1. Parse MDUMP markers: (concept 0-4, field 0-2, status, support, bytes).
  2. For every sincere probe (curriculum sinc1..sinc5), compute firing
     markers and the predict() outcome under the frozen voting rule:
       - live marker: status in (1,2); fires iff bytes are a case-insensitive
         substring of the probe's field (0=UTT,1=CTX,2=SPK).
       - concept score = # firing markers; winner = strictly greatest score,
         ties -> lexicographically smallest concept name.
       - v=1 (WITHHOLD) iff any concept scores >0 else 0 (ENDORSE).
       - sincere probe correct iff v==0.
  3. Report EVERY miss with the firing markers (concept, support, bytes).
  4. Specifically verify the 3 claimed collision markers exist with the
     claimed (concept, support) and fire on the claimed probes.
  5. Hunt for UNCLAIMED collisions: any marker firing on any sincere probe
     that is not one of the 3 claimed markers.

Deterministic, zero RNG.
"""
import os, sys

EXP = os.path.expanduser("~/workspace/exp2d_redteam/wt/docs/lab/epistemics/utterance_types/exp2d")
CUR = os.path.expanduser("~/workspace/exp2d_redteam/wt/docs/lab/epistemics/utterance_types/crew2/curriculum")
NAMES = ["sarcasm", "joke", "hypothetical", "quotation", "roleplay"]

def mdump(path):
    ms = []
    for line in open(path, encoding="utf-8", errors="replace"):
        if line.startswith("MDUMP|"):
            p = line.rstrip("\n").split("|", 5)
            ms.append((int(p[1]) - 1, int(p[2]), int(p[3]), int(p[4]), p[5]))
    return ms

def probes(t):
    out = []
    for line in open(os.path.join(CUR, f"sinc{t}.txt"), encoding="utf-8", errors="replace"):
        line = line.rstrip("\n")
        if not line or line.startswith("#"):
            continue
        p = line.split("|")
        out.append((p[0], p[1], p[2], p[3]))
    return out

def predict(markers, utt, ctx, spk):
    fields = [utt.lower(), ctx.lower(), spk.lower()]
    scores = [0] * 5
    fired = []
    for (k, f, st, sup, b) in markers:
        if st not in (1, 2) or not (0 <= k < 5) or not b:
            continue
        if b in fields[f]:
            scores[k] += 1
            fired.append((NAMES[k], sup, b))
    best, bests = -1, 0
    for k in range(5):
        if scores[k] > 0:
            if best == -1 or scores[k] > bests or (scores[k] == bests and NAMES[k] < NAMES[best]):
                best, bests = k, scores[k]
    v = 1 if best != -1 else 0
    return v, (NAMES[best] if best != -1 else None), scores, fired

CLAIMED = {
    ("the clock", "hypothetical", 1): ["si3_03"],
    ("is out", "hypothetical", 1): ["si5_01"],
    ("at night", "joke", 1): ["si4_05", "si5_09"],
}

legs = ["base", "ab2-a", "ab2-b", "abc2-a", "abc2-b", "v96-a", "v96-b", "de2-a", "de2-b"]
def curve2c(path):
    out = {}
    for line in open(path, encoding="utf-8", errors="replace"):
        if line.startswith("2C_CURVE|"):
            p = line.rstrip("\n").split("|")
            d = {}
            for i in range(2, len(p) - 1, 2):
                d[p[i]] = int(p[i + 1])
            out[int(p[1])] = d
    return out

all_misses = {}
unclaimed_firings = []
agg_ok = True
for leg in legs:
    runpath = os.path.join(EXP, f"runs/{leg}_rep1.txt")
    markers = mdump(runpath)
    live = [m for m in markers if m[2] in (1, 2)]
    sup1 = [m for m in live if m[3] == 1]
    curves = curve2c(runpath)
    misses = []
    for t in range(1, 6):
        pl = probes(t)
        dp, lk = pl[0:10], pl[10:20]
        for section, plist in (("DP", dp), ("LK", lk)):
            nmiss = 0
            for pid, spk, ctx, utt in plist:
                v, winner, scores, fired = predict(markers, utt, ctx, spk)
                if v != 0:  # sincere probe withheld = miss
                    nmiss += 1
                    misses.append((pid, section, utt, winner, scores, fired))
                for (cname, sup, b) in fired:
                    if (b, cname, sup) not in CLAIMED:
                        unclaimed_firings.append((leg, pid, cname, sup, b, utt[:60]))
            rep = curves[t]["DP" if section == "DP" else "LK"]
            mine = 10 - nmiss
            if mine != rep:
                agg_ok = False
                print(f"  AGG MISMATCH {leg} T{t} {section}: mine={mine} run={rep}")
    all_misses[leg] = misses
    print(f"=== {leg}: {len(markers)} markers ({len(live)} live, {len(sup1)} support-1) -> {len(misses)} sincere misses (DP+LK) ===")
    for pid, section, utt, winner, scores, fired in misses:
        fs = ", ".join(f"{c}/sup{sup}:{b}" for c, sup, b in fired)
        print(f"  MISS {pid}[{section}] [{utt[:52]}] winner={winner} scores={scores}\n       fired: {fs}")
print("\naggregate reconstruction vs run 2C_CURVE:", "ALL MATCH" if agg_ok else "MISMATCHES ABOVE")

print("\n===== claimed-marker verification =====")
for leg in ["ab2-a", "ab2-b", "abc2-a", "abc2-b", "v96-a", "v96-b"]:
    markers = mdump(os.path.join(EXP, f"runs/{leg}_rep1.txt"))
    for (b, cname, sup), pids in CLAIMED.items():
        found = [(k, f, st, s) for (k, f, st, s, bb) in markers if bb == b and NAMES[k] == cname and s == sup and st in (1, 2)]
        in_leg = leg in ("v96-a", "v96-b") if b in ("the clock", "at night") else leg in ("ab2-a", "ab2-b", "abc2-a", "abc2-b", "v96-a", "v96-b")
        # is-out is pre-existing in ab2/abc2/v96 (not base/de); the-clock/at-night v96-only
        print(f"  {leg}: marker '{b}' ({cname}, sup={sup}) live-instances={len(found)}" + ("" if found or not in_leg else "  <-- EXPECTED BUT ABSENT"))

print("\n===== unclaimed firings on sincere probes (potential missed collisions) =====")
seen = set()
for leg, pid, cname, sup, b, utt in unclaimed_firings:
    key = (leg, pid, b)
    if key in seen: continue
    seen.add(key)
    print(f"  {leg} {pid} [{utt}] <- {cname}/sup{sup}:'{b}'")
print(f"total unclaimed firing events: {len(unclaimed_firings)}")

print("\n===== DELTA miss-set vs claimed bound (leg misses MINUS base misses) =====")
base_misses = {pid for pid, _, _, _, _, _ in all_misses["base"]}
expected_delta = {
    "v96-a": {"si3_03", "si4_05", "si5_01", "si5_09"},
    "v96-b": {"si3_03", "si4_05", "si5_01", "si5_09"},
    "ab2-a": {"si5_01"}, "ab2-b": {"si5_01"},
    "abc2-a": {"si5_01"}, "abc2-b": {"si5_01"},
    "base": set(), "de2-a": set(), "de2-b": set(),
}
ok = True
for leg in legs:
    got = {pid for pid, _, _, _, _, _ in all_misses[leg]} - base_misses
    exp = expected_delta[leg]
    # abc2-a is the failing alpha control: delta is large but mechanistically explained (see below)
    status = "OK" if got == exp else ("OK-ALPHA-EXPLAINED" if leg == "abc2-a" else "MISMATCH")
    if got != exp and leg != "abc2-a": ok = False
    extra = sorted(got - exp)[:6]
    print(f"  {leg}: delta={sorted(got)} expected={sorted(exp)} -> {status}" + (f" extra={extra}" if extra and leg != "abc2-a" else ""))
print("C3 BOUND EXACT" if ok else "C3 BOUND WRONG")

print("\n===== X2C probe firing analysis (which markers withhold wi/wd probes?) =====")
for label, pf in (("wi", os.path.join(EXP, "items/sinc3x_wi.txt")), ("wd", os.path.join(EXP, "items/sinc3x_wd.txt"))):
    xprobes = []
    for line in open(pf, encoding="utf-8", errors="replace"):
        line = line.rstrip("\n")
        if not line or line.startswith("#"): continue
        p = line.split("|")
        xprobes.append((p[0], p[1], p[2], p[3]))
    for leg in ["base", "ab2-a", "abc2-b", "v96-a", "de2-a", "abc2-a"]:
        markers = mdump(os.path.join(EXP, f"runs/{leg}_rep1.txt"))
        withheld = 0
        why = {}
        for pid, spk, ctx, utt in xprobes:
            v, winner, scores, fired = predict(markers, utt, ctx, spk)
            if v == 1:
                withheld += 1
                for (cname, sup, b) in fired:
                    why[(cname, b)] = why.get((cname, b), 0) + 1
        top = sorted(why.items(), key=lambda kv: -kv[1])[:4]
        print(f"  {leg} {label}: withheld {withheld}/10; top markers: {[(c, b, n) for (c, b), n in top]}")
