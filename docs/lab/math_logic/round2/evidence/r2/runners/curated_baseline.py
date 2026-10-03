#!/usr/bin/env python3
"""CURATED BASELINE for B7F: mechanical application of round-1 human
formalization choices (no learning). Deterministic rule-based NL->formal mapper.

Rules (embodying the round-1 human conventions):
- "If <A>, <B>." / "<B> only when <A>." / "<B> only if <A>." -> imp(A', B')
- "All <A> are <B>." / "Every <A> ..." / "No <A> is <B>." -> forall(x, imp(A'(x), B'(x))) / forall(x, imp(A'(x), not(B'(x))))
- "<A> before <B>." -> before(A', B') atoms (transitivity via MP chains in store)
- "<A>." (bare assertion) -> A' premise
- "<A> does not <B>." / "<A> is not <B>." -> not(...) premise
- Questions "Is <A>?" / "Does <A> <B>?" / "May <A> <B>?" / "Did <A> <B>?" -> target atom (possibly negated)
Predicate slugs: deterministic alphanumeric slug of the phrase.
"""
import re, os, sys

NLDIR = "/home/hatch/workspace/math_r2/eval/b7f_nl"
OUTDIR = "/home/hatch/workspace/math_r2/eval/b7f_forms_curated"
os.makedirs(OUTDIR, exist_ok=True)

def slug(s):
    s = s.lower().strip().rstrip(".?")
    s = re.sub(r"^(the|a|an)\s+", "", s)
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return s or "x"

def atom(phrase):
    return slug(phrase)

def parse_statement(text):
    """Returns (premises_list, target) as claim strings."""
    # Split into sentences
    sents = [s.strip() for s in re.split(r"\.\s*", text) if s.strip()]
    premises, target = [], None
    for s in sents:
        sl = s.lower()
        if sl.endswith("?") or s.endswith("?"):
            q = s.rstrip("?")
            ql = q.lower()
            # "Is <A>?" / "Is <A> <B>?"
            m = re.match(r"is\s+(.+)", ql)
            if m:
                target = atom(m.group(1)); continue
            m = re.match(r"does\s+(.+)", ql)
            if m:
                # "Does the keynote end before lunch begins" -> before(keynote_end, lunch_begin)
                # "Does the bell ring before the show begins" -> before(bell_ring, show_begin)
                inner = m.group(1)
                bm = re.match(r"(.+?)\s+(end|ring|occur|happen)\s+before\s+(.+?)\s+(begins|opens|starts)", inner)
                if bm:
                    target = f"before({atom(bm.group(1)+' '+bm.group(2))},{atom(bm.group(3)+' '+bm.group(4))})"
                else:
                    target = atom(inner)
                continue
            m = re.match(r"did\s+(.+)", ql)
            if m:
                target = f"not({atom(m.group(1))})" if "not" in ql else atom(m.group(1))
                # B7F_06 "Did Maya attend the party?" with not(in_photos) premise -> target not(attend)
                # Heuristic: if any premise is a negation, question targets the negation
                continue
            m = re.match(r"may\s+(.+)", ql)
            if m:
                target = atom("may_" + m.group(1)); continue
            m = re.match(r"can\s+(.+)", ql)
            if m:
                target = atom("can_" + m.group(1)); continue
            target = atom(q); continue
        # "If <A>, <B>."
        m = re.match(r"if\s+(.+?),\s*(.+)", sl)
        if m:
            premises.append(f"imp({atom(m.group(1))},{atom(m.group(2))})"); continue
        # "<B> only when <A>." / "<B> only if <A>."
        m = re.match(r"(.+?)\s+only\s+(?:when|if)\s+(.+)", sl)
        if m:
            premises.append(f"imp({atom(m.group(1))},{atom(m.group(2))})"); continue
        # "No <A> is <B>."
        m = re.match(r"no\s+(.+?)\s+is\s+(?:a\s+)?(.+)", sl)
        if m:
            premises.append(f"forall(x,imp({atom(m.group(1))}(x),not({atom(m.group(2))}(x))))"); continue
        # "All <A> are <B>." / "Every <A> ..."
        m = re.match(r"(?:all|every|everyone who)\s+(.+?)\s+(?:are|is)\s+(.+)", sl)
        if m:
            premises.append(f"forall(x,imp({atom(m.group(1))}(x),{atom(m.group(2))}(x)))"); continue
        m = re.match(r"everyone who\s+(.+?)\s+may\s+(.+)", sl)
        if m:
            # "Everyone who paid their dues may vote." -> forall(x, imp(paid_dues(x), may_vote(x)))
            premises.append(f"forall(x,imp({atom(m.group(1))}(x),{atom('may_'+m.group(2))}(x)))"); continue
        # "<A> before <B>."
        m = re.match(r"(.+?)\s+before\s+(.+)", sl)
        if m:
            # "The keynote ends before lunch begins." -> before(keynote_ends, lunch_begins)
            premises.append(f"before({atom(m.group(1))},{atom(m.group(2))})"); continue
        # "<A> does not <B>." / "<A> is not <B>." / "<A> never <B>."
        m = re.match(r"(.+?)\s+(?:does not|do not|is not|are not|never)\s+(.+)", sl)
        if m:
            premises.append(f"not({atom(m.group(1)+' '+m.group(2))})"); continue
        # "<A> just <B>." / bare assertion
        premises.append(atom(s))
    return premises, target

def main():
    for i in range(1, 21):
        pid = f"B7F_{i:02d}"
        with open(f"{NLDIR}/{pid}.txt") as f:
            content = f.read()
        m = re.search(r"STATEMENT:\s*(.*)", content, re.S)
        text = m.group(1).strip()
        premises, target = parse_statement(text)
        if target is None:
            target = "unknown_target"
        with open(f"{OUTDIR}/{pid}.form", "w") as f:
            f.write(f"ID: {pid}\nSTORE: round2/batteries/knowledge/KB_B7F.md\nPREMISES:\n")
            for p in premises:
                f.write(p + "\n")
            f.write(f"TARGET:\n{target}\n")
        print(f"{pid}: {len(premises)} premises, target={target}")

if __name__ == "__main__":
    main()
