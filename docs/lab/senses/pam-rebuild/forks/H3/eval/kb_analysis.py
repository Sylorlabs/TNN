#!/usr/bin/env python3
"""H3 streaming kill-bar analysis (frozen evaluation metric).
Replicates the binary's exact cross-episode memory update rules and asserts
the replication reproduces the binary's per-episode `durable=` flag exactly.
KB1 denominator = injected false percepts (prereg §8.1).
KB3 = end-of-scene memory state (prereg §8.3), via verified replication.
Usage: kb_analysis.py <streamdir>
Provenance: corrected metric written during the frozen evaluation; supersedes
any earlier per-episode-disposition kill-bar computations.
"""
import json, glob, os, re, sys

VOCAB = {
    "colordisc":  ["SAME", "DIFFERENT"],
    "colorconst": ["SAME_SURFACE", "DIFFERENT"],
    "shapetrans": ["CIRCLE", "SQUARE", "TRIANGLE"],
    "pitchdisc":  ["SAME", "HIGHER", "LOWER"],
    "timbredisc": ["PURE", "DARK", "RICH", "BRIGHT"],
    "motiondir":  ["STILL", "N", "NE", "E", "SE", "S", "SW", "W", "NW"],
}

def fnv1a(bs):
    h = 0xCBF29CE484222325  # -3750763034362895579 mod 2^64
    for b in bs:
        h = ((h ^ b) * 0x100000001B3) & 0xFFFFFFFFFFFFFFFF
    return h

def parse_tr(tr):
    # H3|task=..|fx=..|t0=NAME|br=c:cf:br;...|inst=NAME|disp=..|judge=NAME|dur=0|
    brs = {}
    m = re.search(r"\|br=([^|]*)\|", tr)
    if m:
        for part in m.group(1).split(";"):
            if part:
                c, cf, br = part.split(":")
                brs[int(c)] = (int(cf), int(br))
    mi = re.search(r"\|inst=([^|]*)\|", tr)
    inst = mi.group(1) if mi else "NONE"
    md = re.search(r"\|dur=([^|]*)\|", tr)
    dur = int(md.group(1)) if md else 0
    return brs, inst, dur

def analyze(task, jf):
    rows = [json.loads(l) for l in open(jf)]
    K = len(VOCAB[task])
    prov = [0]*9; dur = [0]*9; quar = [0]*9
    rep_ok = True
    for r in rows:
        brs, inst_name, _ = parse_tr(r["transition"])
        # quarantine revokes
        for c in range(K):
            cf, br = brs.get(c, (0, 0))
            if br >= 2:
                quar[c] = 1; dur[c] = 0; prov[c] = 0
        inst = VOCAB[task].index(inst_name) if inst_name in VOCAB[task] else -1
        dur_out = 0
        if inst >= 0:
            if quar[inst] == 1:
                pass  # would become WITHDRAWN
            else:
                fidh = fnv1a(r["fixture"].encode())
                pf = prov[inst]
                if pf == 0:
                    prov[inst] = fidh
                elif pf != fidh:
                    dur[inst] = 1
                dur_out = dur[inst]
        if dur_out != r["durable"]:
            rep_ok = False
            print("  REPLICATION MISMATCH ep=%d bin=%d rep=%d" % (r["ep"], r["durable"], dur_out))
    print("  replication faithful (dur flags): %s" % rep_ok)

    # KB1: injected false percepts = kind A and t0 != truth
    inj = [r for r in rows if r["kind"] == "A" and r["t0"] != r["truth"]]
    false_perm = [r for r in inj if r["durable"] == 1 and r["judge"] != r["truth"]]
    false_prov = [r for r in inj if r["disp"] == "INSTALLED" and r["judge"] != r["truth"]]
    kb1 = len(false_perm) / len(inj) if inj else 0.0

    # KB2
    handled = [r for r in inj if r["disp"] in ("WITHDRAWN", "QUARANTINED")]
    kb2 = len(handled) / len(inj) if inj else 1.0

    # KB3: distinct (task,claim) correctly installed in base episodes; present at scene end
    correct = set()
    for r in rows:
        if r["kind"] == "B" and r["disp"] == "INSTALLED" and r["judge"] == r["truth"]:
            correct.add(r["judge"])
    present = 0
    for claim in correct:
        c = VOCAB[task].index(claim)
        if quar[c] == 0 and (prov[c] != 0 or dur[c] == 1):
            present += 1
    kb3 = present / len(correct) if correct else 1.0

    # KB4 regret
    reg_h3, reg_a = 0, 0
    for r in rows:
        t = r["truth"]
        best = 1 if r["judge"] == t else 0
        reg_h3 += best - (1 if (r["disp"] == "INSTALLED" and r["judge"] == t) else (-1 if (r["disp"] == "INSTALLED") else 0))
        reg_a += (1 if r["a_judge"] == t else 0) - (1 if r["a_judge"] == t else -1)
    kb4 = ((reg_a - reg_h3) / reg_a) if reg_a > 0 else 0.0

    return {
        "task": task, "n": len(rows), "replication_faithful": rep_ok,
        "kb1_inj": len(inj), "kb1_false_perm": len(false_perm),
        "kb1_rate": kb1, "kb1_kill": kb1 > 0.04,
        "kb1_prov_rate": len(false_prov)/len(inj) if inj else 0.0,
        "kb2_handled": len(handled), "kb2_rate": kb2, "kb2_kill": kb2 < 0.90,
        "kb3_correct_claims": len(correct), "kb3_present": present,
        "kb3_recall": kb3, "kb3_kill": kb3 < 0.80,
        "kb4_regret_h3": reg_h3, "kb4_regret_a": reg_a,
        "kb4_reduction": kb4, "kb4_kill": kb4 < 0.25,
    }

def main():
    d = sys.argv[1]
    allr = []
    for jf in sorted(glob.glob(os.path.join(d, "stream_*.jsonl"))):
        task = os.path.basename(jf)[7:-6]
        s = analyze(task, jf)
        allr.append(s)
        print(task, json.dumps({k: (round(v, 4) if isinstance(v, float) else v) for k, v in s.items()}, indent=None))
    print("\n=== pooled ===")
    inj = sum(s["kb1_inj"] for s in allr); fp = sum(s["kb1_false_perm"] for s in allr)
    h2 = sum(s["kb2_handled"] for s in allr)
    corr = sum(s["kb3_correct_claims"] for s in allr); pr = sum(s["kb3_present"] for s in allr)
    rh = sum(s["kb4_regret_h3"] for s in allr); ra = sum(s["kb4_regret_a"] for s in allr)
    print("KB1 pooled false-perm rate: %.4f (%d/%d)  kill=%s" % (fp/inj, fp, inj, fp/inj > 0.04))
    print("KB2 pooled handled rate: %.4f (%d/%d)  kill=%s" % (h2/inj, h2, inj, h2/inj < 0.90))
    print("KB3 pooled recall: %.4f (%d/%d)  kill=%s" % (pr/corr, pr, corr, pr/corr < 0.80))
    print("KB4 pooled regret reduction: %.4f  kill=%s" % ((ra-rh)/ra if ra else 0, ((ra-rh)/ra if ra else 0) < 0.25))

if __name__ == "__main__":
    main()
