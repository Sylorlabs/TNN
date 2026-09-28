#!/usr/bin/env python3
"""Forbidden-content sweep for RSI run-2 teaching curriculum (design-time check).
Implements the sweep spec: F-CORE list, case rules, whole-token matching.
Exit 0 + 'SWEEP PASS' iff no forbidden content in any target file.
Exit 1 + 'SWEEP FAIL' listing every hit otherwise.
"""
import re, sys, pathlib

HERE = pathlib.Path(__file__).resolve().parent
RUN2 = HERE.parent
TEACH = RUN2 / "work" / "teach"
CUR = TEACH / "curriculum"
BAT = TEACH / "scenarios"
KEYS_FILE = TEACH / "keys.txt"

# Fixed substrings, case-insensitive
FIXED_CI = ["ask-first", "askfirst", "N-clean", "O-clean", "ADV-OLD",
            "GAP-1", "GAP-3", "mode 4"]
# Whole tokens, case-insensitive
TOKEN_CI = ["coherence", "recency", "consult", "channel", "cidx", "margin",
            "withhold", "install", "decide", "fld", "rel_sat2", "score_pick",
            "slot_mask", "ops", "gt", "clean",
            "C1", "C2", "C3", "C4", "C5"]
# Whole tokens, case-SENSITIVE (engine verdict constants)
TOKEN_CS = ["NEW", "OLD", "ADV", "NEITHER", "WITHHOLD", "INSTALL"]
# Whole-token digit runs (any)
DIGIT_RE = re.compile(r'^[0-9]+$')
TOKEN_RE = re.compile(r'[A-Za-z0-9_]+')

def check_file(path, skip_digit=False):
    hits = []
    text = path.read_text()
    low = text.lower()
    for s in FIXED_CI:
        if s.lower() in low:
            hits.append(f"FIXED-CI:{s}")
    for m in TOKEN_RE.finditer(text):
        tok = m.group(0)
        if DIGIT_RE.match(tok):
            if not skip_digit:
                hits.append(f"DIGIT:{tok}")
        elif tok.lower() in TOKEN_CI:
            hits.append(f"TOKEN-CI:{tok}")
        elif tok in TOKEN_CS:
            hits.append(f"TOKEN-CS:{tok}")
    return hits

def main():
    targets = sorted(CUR.glob("*.txt")) + sorted(BAT.glob("V*.txt")) + [KEYS_FILE]
    assert targets, "no targets"
    # F-CORE cross-check note: every F-CORE token above must be non-empty by construction.
    failed = False
    for t in targets:
        hits = check_file(t, skip_digit=(t.name == "keys.txt"))
        # de-dup preserving order
        seen, uniq = set(), []
        for h in hits:
            if h not in seen:
                seen.add(h); uniq.append(h)
        if uniq:
            failed = True
            print(f"SWEEP FAIL {t.name}: {', '.join(uniq)}")
    if failed:
        print("RESULT: SWEEP FAIL")
        return 1
    print(f"RESULT: SWEEP PASS ({len(targets)} files)")
    return 0

sys.exit(main())
