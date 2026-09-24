#!/usr/bin/env python3
"""Glue: derive Zag-readable case file for O3-rebriefed from frozen R2-4 evidence.
Glue is never the instrument; it only reformats bytes.
Input: sweep.jsonl (frozen), records.txt (frozen, for jcode).
Output: case_o3.txt, pipe-delimited:
  seq|tcode|prog|progF|agree|strong|conf|mrgF|jcode|pred|measure|correct|truth|isadv
  prog/progF: 0=PASS, 1=FAIL, 2=UNRESOLVED ; pred: 0/1 (== final_pred, post-deliberation)
  isadv: 1 iff kind=='adv' (for KB-O3b gate-level sealed analog)
"""
import json, sys

def pc(s):
    return {"PASS": 0, "FAIL": 1, "UNRESOLVED": 2}[s]

def fpc(i):
    return {0: 0, 1: 1, 2: 2}[i]

jcode = {}
with open("records.txt") as f:
    for line in f:
        p = line.rstrip("\n").split("|")
        jcode[int(p[0])] = p[4]

tcode = {"colordisc": 0, "colorconst": 1, "shapetrans": 2,
         "pitchdisc": 3, "timbredisc": 4, "motiondir": 5}

n = 0
with open("sweep.jsonl") as fin, open("case_o3.txt", "w") as fout:
    for line in fin:
        r = json.loads(line)
        s = r["seq"]
        correct = 1 if r["judgment"] == r["truth"] else 0
        isadv = 1 if r["kind"] == "adv" else 0
        row = [str(s), str(tcode[r["task"]]), str(fpc(r["final_prog"])),
               str(pc(r["progF"])), str(r["agree"]), str(r["strong"]),
               str(r["conf"]), str(r["mrgF"]), jcode[s], str(r["final_pred"]),
               str(r["measure"]), str(correct), r["truth"], str(isadv)]
        fout.write("|".join(row) + "\n")
        n += 1
print(f"wrote case_o3.txt: {n} rows")
