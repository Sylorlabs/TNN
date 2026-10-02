#!/usr/bin/env python3
"""Phase 1A baseline glue: validate frozen probe files and generate battery.txt files.
Pure glue — nothing here is in TNN's path. The binary under test is untouched.
Usage: validate.py  (validates + writes batteries/knowledge_battery.txt, batteries/reasoning_battery.txt)
"""
import os, re, sys

BASE = os.path.dirname(os.path.abspath(__file__))
DIAL = os.path.join(BASE, "..", "..", "..", "dialogue")

def kb_tokens():
    toks = set()
    with open(os.path.join(DIAL, "kb.txt")) as f:
        for line in f:
            for t in re.findall(r"[a-z0-9]+", line.strip().lower()):
                toks.add(t)
    return toks

def norm_tokens(s):
    return re.findall(r"[a-z0-9]+", s.lower())

def load_probes(path, expect_n):
    probes = []
    seen = set()
    with open(path) as f:
        for ln, line in enumerate(f, 1):
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            assert len(parts) >= 5, f"{path}:{ln}: want >=5 tab fields, got {len(parts)}"
            pid, cat, q, ans = parts[0], parts[1], parts[2], parts[3]
            notes = parts[-1] if len(parts) > 4 else ""
            assert pid not in seen, f"dup id {pid}"
            seen.add(pid)
            assert "\t" not in q and q.strip() == q and q, f"{path}:{ln}: bad question"
            assert ans, f"{path}:{ln}: empty answers"
            probes.append((pid, cat, q, ans.split(";"), notes))
    assert len(probes) == expect_n, f"{path}: got {len(probes)}, want {expect_n}"
    return probes

def main():
    kb = kb_tokens()
    kb_digits = {t for t in kb if t.isdigit()}
    know = load_probes(os.path.join(BASE, "KNOWLEDGE_PROBES.txt"), 200)
    reas = load_probes(os.path.join(BASE, "REASONING_PROBES.txt"), 50)
    errs = []
    # collision checks
    # collision checks: full key phrase as contiguous subsequence of a KB fact
    kb_fact_toks = []
    with open(os.path.join(DIAL, "kb.txt")) as f:
        for line in f:
            kb_fact_toks.append(norm_tokens(line))
    def in_kb(kt):
        n = len(kt)
        for ft in kb_fact_toks:
            for i in range(len(ft) - n + 1):
                if ft[i:i+n] == kt:
                    return True
        return False
    for pid, cat, q, keys, notes in know + reas:
        if "__WITHHOLD__" in keys:
            continue
        for k in keys:
            kt = norm_tokens(k)
            if not kt:
                errs.append(f"{pid}: empty key after norm")
            if cat == "MATH" or (pid.startswith("R-") and cat == "R-MATH"):
                for t in kt:
                    if t.isdigit() and t in kb_digits:
                        errs.append(f"{pid}: math answer token {t!r} is a KB digit token")
            if "KB-ANCHOR" not in notes and "SPURIOUS-RISK" not in notes:
                if in_kb(kt):
                    errs.append(f"{pid}: full key phrase {kt} occurs in a KB fact (flag SPURIOUS-RISK or KB-ANCHOR)")
    if errs:
        print("VALIDATION ERRORS:")
        for e in errs:
            print(" ", e)
        sys.exit(1)
    # id prefixes / categories sanity
    cats = {}
    for pid, cat, q, keys, notes in know:
        cats[cat] = cats.get(cat, 0) + 1
    print("knowledge categories:", cats)
    cats = {}
    for pid, cat, q, keys, notes in reas:
        cats[cat] = cats.get(cat, 0) + 1
    print("reasoning categories:", cats)
    # generate batteries
    bdir = os.path.join(BASE, "batteries")
    os.makedirs(bdir, exist_ok=True)
    def gen(probes, name):
        n = 0
        with open(os.path.join(bdir, name), "w") as f:
            for pid, cat, q, keys, notes in probes:
                n += 1
                f.write(f"DIALOGUE {pid} TOPIC\nU {q}\nE <sentinel-no-match-{pid.lower()}>\n")
        print(f"wrote {name}: {n} single-turn dialogues")
    gen(know, "knowledge_battery.txt")
    gen(reas, "reasoning_battery.txt")
    print("VALIDATION OK")

if __name__ == "__main__":
    main()
