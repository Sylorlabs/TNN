#!/usr/bin/env python3
"""GOAL-B verifier: B1 (coverage), B3 (novelty), B4 (leakage-substring). B5 via cmp; B2 via judges."""
import re, sys, hashlib, glob

LAB = "/home/hatch/workspace/tnn-lab"
GOALB = LAB + "/GOALB_STORY"

def parse_rep(path):
    trials = []
    cur = None
    with open(path) as f:
        for line in f:
            line = line.rstrip("\n")
            m = re.match(r"### STORY (\S+) (POS|DEL)$", line)
            if m:
                cur = {"set": m.group(1), "var": m.group(2), "story": [], "plan": []}
                trials.append(cur)
                mode = "story"
                continue
            m = re.match(r"### PLAN (\S+) (POS|DEL)$", line)
            if m:
                mode = "plan"
                continue
            if line == "### END":
                mode = None
                cur = None
                continue
            if cur is not None and mode in ("story", "plan") and line.strip():
                cur[mode].append(line.strip())
    return trials

def load_words():
    sets = {}
    with open(GOALB + "/inputs/words.txt") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            sid, rest = line.split(":", 1)
            sets[sid.strip()] = [w.strip().lower() for w in rest.split(",") if w.strip()]
    return sets

def b1(trial, words):
    text = " ".join(trial["story"]).lower()
    missing = [w for w in words[trial["set"]] if re.search(r"\b" + re.escape(w) + r"\b", text) is None]
    return missing

def load_corpus():
    blobs = []
    for p in [LAB + "/dialogue/kb.txt", LAB + "/dialogue/battery.txt"]:
        with open(p, "rb") as f:
            blobs.append(f.read().decode("utf-8", "replace").lower())
    for p in glob.glob(LAB + "/prose-learning/v3/inputs3*/*.txt") + glob.glob(LAB + "/prose-learning/v3/inputs3*.txt"):
        try:
            with open(p, "rb") as f:
                blobs.append(f.read().decode("utf-8", "replace").lower())
        except Exception:
            pass
    return "\n".join(blobs)

def b3(trial, corpus):
    hits = []
    for s in trial["story"]:
        sl = s.lower().strip()
        if len(sl.split()) < 6:
            continue
        if sl in corpus:
            hits.append(s)
    return hits

def b4_substring(trials):
    with open(LAB + "/dialogue/kb.txt", "rb") as f:
        kb = f.read().decode("utf-8", "replace")
    leaks = []
    for t in trials:
        blob = " ".join(t["story"])
        # sliding 16-byte windows
        for i in range(0, len(blob) - 15):
            if blob[i:i+16] in kb:
                leaks.append((t["set"], t["var"], blob[i:i+16]))
                break
    return leaks

def main():
    trials = parse_rep(GOALB + "/runs/rep1.log")
    words = load_words()
    print(f"trials={len(trials)}")
    # B1
    b1fails = []
    for t in trials:
        miss = b1(t, words)
        if miss:
            b1fails.append((t["set"], t["var"], miss))
    print(f"B1-COVERAGE: {len(trials)-len(b1fails)}/{len(trials)} pass")
    for s, v, m in b1fails:
        print(f"  FAIL {s} {v} missing={m}")
    # B3
    corpus = load_corpus()
    print(f"corpus-bytes={len(corpus)}")
    b3fails = []
    for t in trials:
        hits = b3(t, corpus)
        if hits:
            b3fails.append((t["set"], t["var"], hits))
    print(f"B3-NOVELTY: {len(trials)-len(b3fails)}/{len(trials)} pass")
    for s, v, h in b3fails:
        print(f"  FAIL {s} {v} hits={h}")
    # B4 substring
    leaks = b4_substring(trials)
    print(f"B4-SUBSTRING: {len(trials)-len(leaks)}/{len(trials)} clean")
    for s, v, sub in leaks:
        print(f"  LEAK {s} {v} {sub!r}")
    # per-variant B1 summary
    for var in ("POS", "DEL"):
        ok = sum(1 for t in trials if t["var"] == var and not b1(t, words))
        print(f"B1-{var}: {ok}/8")

if __name__ == "__main__":
    main()
