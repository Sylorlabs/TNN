#!/usr/bin/env python3
"""Combine the two blind B2 judges (sol, grok-4.7) into the two-judge verdict.
Reads evidence/b2_raw_gpt-5_6-sol.txt, evidence/b2_raw_grok-4_7.txt,
evidence/b2_item_key.txt. Writes evidence/b2_combined.md."""
import re

GOALB = "/home/hatch/workspace/tnn-lab/GOALB_STORY"

def parse(path):
    scores = {}
    for line in open(path):
        m = re.match(r"\s*(T\d{2})\s*[:=\-]\s*([1-5])\b", line)
        if m:
            scores[m.group(1)] = int(m.group(2))
    return scores

key = {}
for line in open(GOALB + "/evidence/b2_item_key.txt"):
    m = re.match(r"(T\d{2}):\s*(\S+)\s+(\S+)", line)
    if m:
        key[m.group(1)] = (m.group(2), m.group(3))

sol = parse(GOALB + "/evidence/b2_raw_gpt-5_6-sol.txt")
grok = parse(GOALB + "/evidence/b2_raw_grok-4_7.txt")
assert len(key) == 17 and len(sol) == 17 and len(grok) == 17, (len(key), len(sol), len(grok))

rows = []
for i in range(17):
    tid = f"T{i+1:02d}"
    s, g = sol[tid], grok[tid]
    mean = (s + g) / 2
    rows.append((tid, key[tid][0], key[tid][1], s, g, mean, abs(s - g)))

out = ["# B2 combined two-judge table", "",
       "Judge #1: gpt-5.6-sol (UnoRouter, blind). Judge #2: grok-4.7 (ExperientialLabs, blind).",
       "Frozen prompt: evidence/b2_prompt.txt (same text, same blind TIDs for both judges).", "",
       "| trial | set | variant | sol | grok-4.7 | mean | |diff| |",
       "|---|---|---|---|---|---|---|"]
for r in rows:
    out.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]:.1f} | {r[6]} |")

variants = {"POS": [r for r in rows if r[2] == "POS" and r[1] != "CTRL"],
            "DEL": [r for r in rows if r[2] == "DEL"]}
out += ["", "## Per-variant counts (mean >= 3.5)", ""]
for var, rs in variants.items():
    ok = sum(1 for r in rs if r[5] >= 3.5)
    out.append(f"- {var}: {ok}/{len(rs)} trials with two-judge mean >= 3.5 (bar: >=6/8)")
out += ["", "## Per-judge counts (single-judge reading, mean>=3.5 per judge)", ""]
for jname, js in [("sol", sol), ("grok-4.7", grok)]:
    for var, rs in variants.items():
        ok = sum(1 for r in rs if js[r[0]] >= 3.5)
        out.append(f"- {jname} {var}: {ok}/{len(rs)}")
out += ["", "## Head-to-head variant means", ""]
real = [r for r in rows if r[1] != "CTRL"]
for jname, jf in [("sol", lambda r: r[3]),
                  ("grok-4.7", lambda r: r[4]),
                  ("combined", lambda r: r[5])]:
    d = [jf(r) for r in real if r[2] == "DEL"]
    p = [jf(r) for r in real if r[2] == "POS"]
    out.append(f"- {jname}: DEL {sum(d)/len(d):.2f}, POS {sum(p)/len(p):.2f}, gap {sum(d)/len(d) - sum(p)/len(p):.2f}")
ctrl = [r for r in rows if r[1] == "CTRL"][0]
out += ["", f"## Positive control T17: sol={ctrl[3]}, grok={ctrl[4]} (bar: both >= 4.0)",
        "", "## Inter-rater disagreements >2 points", ""]
big = [r for r in rows if r[6] > 2]
out.append("- none" if not big else "\n".join(f"- {r[0]}: sol={r[3]} grok={r[4]} diff={r[6]}" for r in big))
out += ["", f"Max |diff| = {max(r[6] for r in rows)}", ""]
open(GOALB + "/evidence/b2_combined.md", "w").write("\n".join(out))
print("\n".join(out))
