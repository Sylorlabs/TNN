#!/usr/bin/env python3
"""Build blinded trace pairs for Micah's readability judgment (criterion c).

Reads nat_scores.json and en_scores.json (produced by grade.py), writes:
  BLINDED_PAIRS.md — per problem: questions, Trace A, Trace B, each with its answers.
  KEY.md           — which of A/B is NAT / EN per problem (keep separate).

Blinding: for each problem, parity of the first hex digit of
sha256("trace-trial-blind:" + problem_id). Even -> NAT = Trace A; odd -> NAT = Trace B.
Deterministic, zero RNG, no pattern visible to the judge.
"""
import hashlib, json

def side(problem_id):
    h = hashlib.sha256(("trace-trial-blind:" + problem_id).encode()).hexdigest()
    return int(h[0], 16) % 2  # 0 -> NAT is A, 1 -> NAT is B

def load(path):
    r = json.load(open(path))
    by_prob = {}
    for t in r["traces"]:
        by_prob.setdefault(t["did"], []).append(t)
    return by_prob

def main():
    nat = load("nat_scores.json")
    en = load("en_scores.json")
    battery = open("battery20.txt").read().splitlines()
    # questions per problem
    qs = {}
    did = None
    for line in battery:
        if line.startswith("DIALOGUE "):
            did = line.split()[1]; qs[did] = []
        elif line.startswith("U "):
            qs[did].append(line[2:])

    pairs = ["# Blinded trace pairs — readability judgment",
             "",
             "For each problem, read **Trace A** and **Trace B** and pick the one whose",
             "reasoning trace is clearer / easier to follow. Ignore the answers themselves",
             "as much as you can — judge the TRACE.",
             ""]
    key = ["# Blinding key (keep separate from BLINDED_PAIRS.md)", "",
           "| Problem | Trace A | Trace B |",
           "|---------|---------|---------|"]
    for did in sorted(qs.keys()):
        s = side(did)
        a_arm, b_arm = ("NAT", "EN") if s == 0 else ("EN", "NAT")
        a_src = nat if s == 0 else en
        b_src = en if s == 0 else nat
        key.append(f"| {did} | {a_arm} | {b_arm} |")
        pairs.append(f"## {did}")
        for i, q in enumerate(qs[did], start=1):
            pairs.append(f"**Q{i}:** {q}")
        pairs.append("")
        for label, src in (("A", a_src), ("B", b_src)):
            pairs.append(f"### Trace {label}")
            for t in src[did]:
                pairs.append(f"*Turn {t['turn']} trace:*")
                pairs.append("```")
                pairs.extend(t["trace"])
                pairs.append("```")
                pairs.append(f"*Turn {t['turn']} answer:* {t['answer']}")
                pairs.append("")
    open("BLINDED_PAIRS.md", "w").write("\n".join(pairs) + "\n")
    open("KEY.md", "w").write("\n".join(key) + "\n")
    print("wrote BLINDED_PAIRS.md and KEY.md")

if __name__ == "__main__":
    main()
