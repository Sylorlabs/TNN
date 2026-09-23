#!/usr/bin/env python3
"""Phase 1A baseline scorer (glue). Applies SCORING.md mechanical rules.
Usage: score.py  -> writes mechanical.tsv (knowledge+reasoning) and dialogue_turns.tsv
The audit pass is human and recorded separately.
"""
import os, re, sys

BASE = os.path.dirname(os.path.abspath(__file__))
RUNS = os.path.join(BASE, "runs")

def norm_tokens(s):
    return re.findall(r"[a-z0-9]+", s.lower())

DECLINE = [
    ["do","not","know"], ["don","t","know"], ["no","information"],
    ["cannot","answer"], ["unable","to","answer"], ["unknown"],
]

def subseq(hay, needle):
    n = len(needle)
    return any(hay[i:i+n] == needle for i in range(len(hay)-n+1))

def load_probes(path):
    probes = {}
    with open(path) as f:
        for line in f:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            probes[parts[0]] = (parts[1], parts[2], parts[3].split(";"))
    return probes

def load_responses(run_name):
    """(did, turn) -> (response_text, novel_flag)."""
    resp = {}
    did, turn, novel = None, 0, 0
    with open(os.path.join(RUNS, run_name + "_rep1", "output.log")) as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith("D "):
                did = line[2:].strip(); turn = 0
            elif line.startswith("NOVEL=1 T ") or line.startswith("T "):
                novel = 1 if line.startswith("NOVEL=1") else 0
                m = re.match(r"(?:NOVEL=1 )?T (\S+) (\d+) (PASS|FAIL)", line)
                assert m.group(1) == did
                turn = int(m.group(2))
            elif line.startswith("A "):
                resp[(did, turn)] = (line[2:], novel)
    return resp

def mech_verdict(keys, response):
    rt = norm_tokens(response)
    if keys == ["__WITHHOLD__"]:
        for d in DECLINE:
            if subseq(rt, d):
                return True, "decline:" + " ".join(d)
        return False, ""
    for k in keys:
        kt = norm_tokens(k)
        if kt and subseq(rt, kt):
            return True, k
    return False, ""

def main():
    know = load_probes(os.path.join(BASE, "KNOWLEDGE_PROBES.txt"))
    reas = load_probes(os.path.join(BASE, "REASONING_PROBES.txt"))
    kr = load_responses("knowledge")
    rr = load_responses("reasoning")
    assert len(kr) == 200 and len(rr) == 50, (len(kr), len(rr))
    with open(os.path.join(BASE, "mechanical.tsv"), "w") as f:
        f.write("id\tcat\tquestion\tresponse\tnovel\tmech\tmatched_key\n")
        for pid in sorted(set(know) | set(reas)):
            cat, q, keys = (know if pid in know else reas)[pid]
            resp, novel = (kr if pid in kr else rr)[(pid, 1)]
            ok, key = mech_verdict(keys, resp)
            f.write(f"{pid}\t{cat}\t{q}\t{resp}\t{novel}\t{'CORRECT' if ok else 'INCORRECT'}\t{key}\n")
    print("wrote mechanical.tsv")
    # dialogue: one DIALOGUE id (R2-01), 18 turns; dump for human judging
    dr = load_responses("dialogue")
    turns = [l[2:].rstrip("\n") for l in
             open(os.path.join(BASE, "DIALOGUE_BATTERY.txt")) if l.startswith("U ")]
    assert len(dr) == len(turns) == 18, (len(dr), len(turns))
    with open(os.path.join(BASE, "dialogue_turns.tsv"), "w") as f:
        f.write("turn\tquestion\tresponse\tnovel\n")
        for i, q in enumerate(turns, 1):
            resp, novel = dr[("R2-01", i)]
            f.write(f"{i}\t{q}\t{resp}\t{novel}\n")
    print("wrote dialogue_turns.tsv")

if __name__ == "__main__":
    main()
