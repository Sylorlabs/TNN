#!/usr/bin/env python3
"""KB-H7-HARD0 static scanner: zero-hardcode audit of learner Zag source.

Deterministic, zero RNG. Usage:
  hard0_scan.py <learner_src_dir> <report_out>

Strips `//` comments from every *.zag under <learner_src_dir>, then
enumerates:
  (a) string literals containing utterance-type name stems;
  (b) identifier occurrences of those stems in control-flow positions
      (if/while conditions);
  (c) keyword-list-shaped literals (arrays of string literals or
      |-joined alternations).

Every occurrence is reported as file:line:kind:excerpt. The red team
adjudicates each: mechanism logic -> KILL (n=1); learned-knowledge-store
handling only -> allowed with justification (recorded in the report).

Exit codes: 0 = report written; 2 = bad input. OVERALL=HITS (needs
adjudication) or OVERALL=CLEAN.
"""
import sys
import os
import re

STEMS = [
    "sarcasm", "sarcastic",
    "joke", "joking", "jokester",
    "hypothetical",
    "quot", "citation", "cite",
    "roleplay", "persona", "character",
    "utterance", "speechact", "speech_act",
    "deadpan", "irony", "ironic",
]

CTRL_RE = re.compile(r"\b(if|while)\s*\(")
STR_RE = re.compile(r'"(?:[^"\\]|\\.)*"')
IDENT_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def strip_comments(text):
    out = []
    for ln in text.split("\n"):
        # naive: cut at first // not inside a string literal
        res = []
        i = 0
        in_str = False
        while i < len(ln):
            c = ln[i]
            if in_str:
                res.append(c)
                if c == "\\" and i + 1 < len(ln):
                    res.append(ln[i + 1])
                    i += 2
                    continue
                if c == '"':
                    in_str = False
            else:
                if c == '"':
                    in_str = True
                    res.append(c)
                elif c == "/" and i + 1 < len(ln) and ln[i + 1] == "/":
                    break
                else:
                    res.append(c)
            i += 1
        out.append("".join(res))
    return "\n".join(out)


def stem_hit(word):
    w = word.lower()
    for s in STEMS:
        if s in w:
            return s
    return None


def main():
    if len(sys.argv) < 3:
        print("usage: hard0_scan.py <learner_src_dir> <report_out>",
              file=sys.stderr)
        return 2
    srcdir, out = sys.argv[1], sys.argv[2]
    if not os.path.isdir(srcdir):
        print("not a directory: %s" % srcdir, file=sys.stderr)
        return 2

    zag_files = []
    for root, _, files in os.walk(srcdir):
        for fn in sorted(files):
            if fn.endswith(".zag"):
                zag_files.append(os.path.join(root, fn))
    zag_files.sort()
    if not zag_files:
        print("no .zag files under %s" % srcdir, file=sys.stderr)
        return 2

    hits = []  # (file, line, kind, excerpt)
    for path in zag_files:
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read()
        code = strip_comments(raw)
        rel = os.path.relpath(path, srcdir)
        for ln_no, ln in enumerate(code.split("\n"), 1):
            excerpt = ln.strip()[:160]
            # (a) string literals with type-name stems
            for m in STR_RE.finditer(ln):
                lit = m.group(0)
                s = stem_hit(lit)
                if s:
                    hits.append((rel, ln_no, "TYPE_NAME_LITERAL[%s]" % s,
                                 excerpt))
            # (b) identifiers with stems in control-flow conditions
            for m in CTRL_RE.finditer(ln):
                cond = ln[m.end():]
                depth = 1
                cond_text = ""
                for ch in cond:
                    if ch == "(":
                        depth += 1
                    elif ch == ")":
                        depth -= 1
                        if depth == 0:
                            break
                    cond_text += ch
                for ident in IDENT_RE.findall(cond_text):
                    s = stem_hit(ident)
                    if s and ident.lower() != s:
                        # identifier merely containing the stem is
                        # still a hit; exact-stem identifiers too
                        pass
                    if s:
                        hits.append((rel, ln_no,
                                     "TYPE_NAME_IN_CONTROL_FLOW[%s]" % s,
                                     excerpt))
                        break
            # (c) keyword-list shapes: 3+ string literals on one line,
            #     or a |-alternation inside a literal
            lits = STR_RE.findall(ln)
            if len(lits) >= 3:
                hits.append((rel, ln_no, "KEYWORD_LIST_SHAPE",
                             excerpt))
            for lit in lits:
                if "|" in lit and stem_hit(lit):
                    hits.append((rel, ln_no, "ALTERNATION_WITH_TYPE_NAME",
                                 excerpt))
                    break

    # dedupe, deterministic order
    seen = set()
    uniq = []
    for h in hits:
        if h not in seen:
            seen.add(h)
            uniq.append(h)
    uniq.sort()

    with open(out, "w", encoding="utf-8") as f:
        f.write("# KB-H7-HARD0 scan report\n")
        f.write("# src: %s\n" % srcdir)
        f.write("# files scanned: %d\n" % len(zag_files))
        for rel, ln_no, kind, excerpt in uniq:
            f.write("HIT %s:%d:%s:%s\n" % (rel, ln_no, kind, excerpt))
        f.write("HIT_COUNT=%d\n" % len(uniq))
        f.write("OVERALL=%s\n"
                % ("HITS-NEED-ADJUDICATION" if uniq else "CLEAN"))

    print("files=%d hits=%d" % (len(zag_files), len(uniq)))
    print("OVERALL=%s" % ("HITS-NEED-ADJUDICATION" if uniq else "CLEAN"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
