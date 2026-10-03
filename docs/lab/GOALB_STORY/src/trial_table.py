#!/usr/bin/env python3
"""Build evidence/TRIAL_TABLE.md from verifier + judge outputs."""
import re, sys
sys.path.insert(0, "/home/hatch/workspace/tnn-lab/GOALB_STORY/src")
from verify_goalb import parse_rep, load_words, b1, b3, load_corpus

GOALB = "/home/hatch/workspace/tnn-lab/GOALB_STORY"
trials = parse_rep(GOALB + "/runs/rep1.log")
words = load_words()
corpus = load_corpus()

def parse_scores(path, n):
    scores = {}
    with open(path) as f:
        for line in f:
            m = re.match(r"\s*(T\d{2})\s*[:=\-]\s*([1-5])\b", line)
            if m:
                scores[m.group(1)] = int(m.group(2))
    return scores

key = {}
with open(GOALB + "/evidence/b2_item_key.txt") as f:
    for line in f:
        m = re.match(r"(T\d{2}): (\S+) (\S+)", line)
        if m:
            key[m.group(1)] = (m.group(2), m.group(3))

try:
    s_sol = parse_scores(GOALB + "/evidence/b2_raw_gpt-5_6-sol.txt", 17)
    have_sol = len(s_sol) == 17
except FileNotFoundError:
    s_sol, have_sol = {}, False
# native supplementary scores (non-blind experimenter; NOT bar evidence)
s_nat = {"T01":2,"T02":3,"T03":2,"T04":4,"T05":2,"T06":3,"T07":2,"T08":3,
         "T09":2,"T10":4,"T11":2,"T12":3,"T13":2,"T14":3,"T15":2,"T16":3,"T17":5}
have_b2 = have_sol

tid_of = {}
for i, t in enumerate(trials):
    tid_of[(t["set"], t["var"])] = f"T{i+1:02d}"

L = []
L.append("# GOAL-B trial table")
L.append("")
L.append("B5: 3 fresh-process reruns byte-identical (cmp rep1/rep2/rep3). B4: kb.txt sha256 unchanged; 0/16 stories share a >=16-byte substring with kb.txt; composer source has no write path to kb.txt (O_RDONLY reads only).")
L.append("")
L.append("| trial | set | variant | B1 words | B2 sol | B2 native* | B3 novel |")
L.append("|---|---|---|---|---|---|---|")
for t in trials:
    tid = tid_of[(t["set"], t["var"])]
    miss = b1(t, words)
    b1s = "PASS" if not miss else "FAIL " + ",".join(miss)
    b3s = "PASS" if not b3(t, corpus) else "FAIL"
    if have_b2:
        a = s_sol.get(tid, "?")
        b = s_nat.get(tid, "?")
    else:
        a, b = "?", "?"
    L.append(f"| {tid} | {t['set']} | {t['var']} | {b1s} | {a} | {b} | {b3s} |")
L.append("")
L.append("*B2 native = non-blind experimenter supplementary rating (evidence/b2_native_supplementary.md), NOT bar evidence. Second blind LLM judge unevaluated (APIs hard-down); two-judge bar not met.")
if have_b2:
    L.append(f"Positive control T17: sol={s_sol['T17']} (bar >=4.0 single-judge; second judge pending API recovery)")
with open(GOALB + "/evidence/TRIAL_TABLE.md", "w") as f:
    f.write("\n".join(L) + "\n")
print("wrote evidence/TRIAL_TABLE.md, have_b2 =", have_b2)
