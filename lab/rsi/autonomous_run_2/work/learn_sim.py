#!/usr/bin/env python3
"""Simulate the frozen learning protocol over the curriculum lesson files.
Parses LESSON/JUDGMENT/IS/USED/RULE/CAL, evaluates every CAL under the
frozen derivation rules, and reports INSTALL/REJECT per lesson.
The bad lesson must be REJECTED; all others INSTALLED.
"""
import re, pathlib, sys

CUR = pathlib.Path.home() / "workspace/tnn-lab/rsi/autonomous_run_2/work/curriculum"

# ---------- RULE grammar: atoms=fact names, ! & | parens ----------
TOK = re.compile(r'!|&|\||\(|\)|->|;|[A-Za-z0-9_-]+')
def parse_rule(s):
    toks = [t for t in TOK.findall(s) if t not in ('->', ';')]
    pos = 0
    def peek(): return toks[pos] if pos < len(toks) else None
    def expr():
        nonlocal pos
        node = term()
        while peek() == '|':
            pos += 1; rhs = term(); node = ('or', node, rhs)
        return node
    def term():
        nonlocal pos
        node = factor()
        while peek() == '&':
            pos += 1; rhs = factor(); node = ('and', node, rhs)
        return node
    def factor():
        nonlocal pos
        t = peek()
        if t == '!':
            pos += 1; return ('not', factor())
        if t == '(':
            pos += 1; node = expr()
            assert peek() == ')', f"missing ) in {s}"
            pos += 1; return node
        assert re.fullmatch(r'[A-Za-z0-9_-]+', t), f"bad atom {t} in {s}"
        pos += 1; return ('atom', t)
    node = expr()
    assert pos == len(toks), f"trailing tokens in {s}: {toks[pos:]}"
    return node

def ev(node, facts):
    k = node[0]
    if k == 'atom': return node[1] in facts
    if k == 'not': return not ev(node[1], facts)
    if k == 'and': return ev(node[1], facts) and ev(node[2], facts)
    if k == 'or': return ev(node[1], facts) or ev(node[2], facts)
    raise AssertionError(k)

def parse_lesson(path):
    d = {"cals": []}
    for line in path.read_text().splitlines():
        if line.startswith("LESSON:"): d["id"] = line[7:].strip()
        elif line.startswith("JUDGMENT:"):
            pos, neg = [x.strip() for x in line[9:].split("/")]
            d["pos"], d["neg"] = pos, neg
        elif line.startswith("RULE:"):
            body = line[5:].strip()
            m = re.fullmatch(r'(.*)\s*->\s*(\S+)\s*;\s*else\s+(\S+)', body)
            assert m, f"RULE parse fail in {path.name}: {body}"
            d["rule"] = parse_rule(m.group(1))
            assert m.group(2) == d["pos"] and m.group(3) == d["neg"], \
                f"RULE verdict mismatch in {path.name}"
        elif line.startswith("CAL:"):
            rest = line[4:].strip()
            assert rest.startswith("FACTS:"), f"CAL format in {path.name}"
            parts = [p.strip() for p in rest[6:].split("|")]
            assert parts[-1].startswith("EXPECT:"), f"CAL EXPECT in {path.name}"
            d["cals"].append((set(parts[:-1]), parts[-1][7:].strip()))
    assert d["cals"], f"no CALs in {path.name}"
    return d

def main():
    order = sorted(CUR.glob("lesson_[0-9]*.txt")) + [CUR / "lesson_bad.txt"]
    installed = []  # (id, rule, kind) kind in G/I/M/D
    log = []
    ok = True
    for p in order:
        L = parse_lesson(p)
        kind = "G" if L["pos"] in ("GAMING", "OVERFIT", "CORRUPT") else ("I" if L["pos"] == "IMPROVEMENT" else "X")
        verdicts = []
        for facts, expect in L["cals"]:
            if kind == "G":
                v = L["pos"] if ev(L["rule"], facts) else L["neg"]
            elif kind == "I":
                defeated = any(ev(r, facts) for _, r, k in installed if k == "G")
                v = L["pos"] if (ev(L["rule"], facts) and not defeated) else L["neg"]
            else:
                v = L["pos"] if ev(L["rule"], facts) else L["neg"]
            verdicts.append((v, expect, facts))
        bad = [(v, e) for v, e, _ in verdicts if v != e]
        if not bad:
            installed.append((L["id"], L["rule"], kind if kind in "GI" else "X"))
            log.append(f"INSTALL {L['id']} ({len(verdicts)}/{len(verdicts)} CALs)")
        else:
            v, e = bad[0]
            log.append(f"REJECT  {L['id']} (CAL derived {v}, expected {e})")
            if L["id"] != "bad-score-alone":
                ok = False
    bad_installed = any(i == "bad-score-alone" for i, _, _ in installed)
    print("\n".join(log))
    print(f"installed={len(installed)} bad_installed={bad_installed}")
    if bad_installed:
        print("TEACHING VOID: bad lesson installed"); return 1
    if not ok:
        print("TEACHING VOID: a good lesson was rejected"); return 1
    print("LEARN-SIM PASS: 19 installed, bad rejected")
    return 0

sys.exit(main())
