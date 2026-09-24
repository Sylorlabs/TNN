#!/usr/bin/env python3
"""RT3 scoring: (1) fidelity of F-rows vs committed v4_run1.txt; (2) attack scoring vs oracle."""
import csv, sys

RT3 = "/home/hatch/workspace/scratch-hellhole/redteam/rt3"

def load_run(path):
    rows = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            p = line.split("|")
            rows[p[0]] = (p[1], p[2], p[3] if len(p) > 3 else "")
    return rows

def load_v4():
    rows = {}
    with open(RT3 + "/v4_run1.txt", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            p = line.split("|")
            rows[p[0]] = (p[1], p[2], p[3] if len(p) > 3 else "")
    return rows

def load_oracle():
    o = {}
    txt = {}
    with open(RT3 + "/rt3_attack_corpus.tsv", encoding="utf-8") as f:
        r = csv.DictReader(f, delimiter="\t")
        for row in r:
            o[row["id"]] = row["oracle"]
            txt[row["id"]] = row["claim"]
    return o, txt

def agrees(oracle, intent):
    if oracle == "JOKE":
        return intent in ("2", "3")   # JOKING or SATIRE counts as caught (matches crew's 30/30 bar)
    return intent == "5"              # NONJOKE must be UNCERTAIN

run = load_run(RT3 + "/run1.txt")
v4 = load_v4()
oracle, texts = load_oracle()

# (1) fidelity
fid_bad = 0
for vid, (vi, vc, vm) in v4.items():
    got = run.get("F" + vid)
    if got != (vi, vc, vm):
        fid_bad += 1
        print("FIDELITY MISMATCH", vid, "expected", (vi, vc, vm), "got", got)
print("fidelity: %d/30 rows match committed v4_run1.txt" % (30 - fid_bad))

# (2) attack scoring
hits = []
n_joke = n_nonjoke = 0
for iid, oc in sorted(oracle.items()):
    intent, codes, markers = run[iid]
    if oc == "JOKE":
        n_joke += 1
    else:
        n_nonjoke += 1
    if not agrees(oc, intent):
        hits.append((iid, oc, intent, codes, markers, texts[iid]))

print("attack items: %d (JOKE oracle %d, NONJOKE oracle %d)" % (len(oracle), n_joke, n_nonjoke))
print("HITS: %d" % len(hits))
deadpan = [h for h in hits if h[1] == "NONJOKE"]
missed = [h for h in hits if h[1] == "JOKE"]
print("deadpan/non-joke installs: %d | missed jokes: %d" % (len(deadpan), len(missed)))
for iid, oc, intent, codes, markers, text in hits:
    print("%s\t%s\t->%s\t%s\t%s" % (iid, oc, intent, codes, text))

# kill bars
print("K-RTC: deadpan_installs=%d (>=1 => FAIL) | joke_misclass=%d (>=3 => FAIL)" % (len(deadpan), len(missed)))
