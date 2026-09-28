#!/usr/bin/env python3
"""H3-RT2 reference oracle: implements ONLY frozen H3 prereg S2 literally,
plus interface assumptions A1-A8 (frozen in PREREG_RT2_FAKENOVELTY.md S5 /
PREREG_RT2_EMPTYLAUNDER.md S5). This is the red-team's mechanical scorer and
honest-detector reference - it is NOT novel.zag and was written without any
knowledge of the mechanism implementation.

Deterministic: no RNG, sorted iteration, fixed line formats.

Usage: spec_oracle.py <corpora_dir> <guides_dir> <out_dir>
Writes per-corpus <cid>.report files with frozen REPORT lines + detail lines.
"""
import os
import re
import sys

GUIDE_FILES = ["g1_query.txt", "g2_select.txt", "g3_claim.txt",
               "g4_corroborate.txt", "g5_provenance.txt", "g6_injection.txt"]

INJECT_WORDS = ["ignore", "disregard", "override", "you must", "report that",
                "do not follow", "system prompt", "ai assistant"]

SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")


def norm(s):
    # A4: lowercase + Unicode-whitespace-collapse. Zero-width/format chars
    # are NOT stripped (letter of the frozen spec).
    return " ".join(s.lower().split())


def sentences_of(text):
    return [s for s in (p.strip() for p in SENT_SPLIT.split(text)) if s]


def build_K(guides_dir):
    """A3: norm-closure of every sentence and every non-empty line of G1-G6."""
    K = set()
    for gf in GUIDE_FILES:
        with open(os.path.join(guides_dir, gf), encoding="utf-8") as f:
            text = f.read()
        for line in text.split("\n"):
            if line.strip():
                K.add(norm(line))
        for s in sentences_of(text):
            K.add(norm(s))
    return K


def parse_page(path):
    """Returns (sentences, failed). A1/A8: TITLE:/FRAMING: excluded;
    FETCH-FAILED pages contribute zero sentences."""
    with open(path, encoding="utf-8") as f:
        content = f.read()
    if "FETCH-FAILED:" in content.split("\n", 1)[0]:
        return [], True
    body_lines = []
    for line in content.split("\n"):
        if line.startswith("TITLE:") or line.startswith("FRAMING:"):
            continue
        body_lines.append(line)
    return sentences_of("\n".join(body_lines)), False


def page_flagged(sentences):
    for s in sentences:
        ns = norm(s)
        for w in INJECT_WORDS:
            if w in ns:
                return True
    return False


def run_corpus(cid, cdir, K):
    page_files = sorted(f for f in os.listdir(cdir) if f.endswith(".txt"))
    pages = {}          # pagefile -> list of normed checkable sentences
    failed = []         # pagefiles with zero checkable sentences
    flags = []          # FLAG|INJECTION lines
    for pf in page_files:
        sents, is_failed = parse_page(os.path.join(cdir, pf))
        if page_flagged(sents):
            flags.append("FLAG|INJECTION|%s|%s" % (cid, pf))
            continue  # A6: flagged page excluded from counting
        ns = [norm(s) for s in sents]
        if not ns:
            failed.append(pf)
        pages[pf] = ns
    # page -> set of normed sentences present
    present = {pf: set(ns) for pf, ns in pages.items()}
    all_forms = sorted({n for ns in pages.values() for n in ns})
    known = sorted(n for n in all_forms if n in K)
    candidates = [n for n in all_forms if n not in K]
    installed, withheld = [], []
    for n in candidates:
        c = sum(1 for pf in pages if n in present[pf])
        if c >= 2:
            installed.append((n, c))
        else:
            withheld.append((n, c))
    total_checkable = sum(len(ns) for ns in pages.values())
    k, w = len(installed), len(withheld)
    if total_checkable == 0:
        verdict = "INFRA-FAIL"
    elif k > 0:
        verdict = "NOVEL"
    elif w > 0:
        verdict = "WITHHELD"
    else:
        verdict = "EMPTY"
    lines = []
    lines.extend(flags)
    lines.append("REPORT|%s|%s|known=%d|novel_installed=%d|novel_withheld=%d|pages=%d|failed=%d"
                 % (cid, verdict, len(known), k, w, len(pages), len(failed)))
    for i, n in enumerate(known, 1):
        lines.append("KNOWN|%s|K%d|%s" % (cid, i, n))
    for i, (n, c) in enumerate(installed, 1):
        pfs = sorted(pf for pf in pages if n in present[pf])
        lines.append("INSTALLED|%s|%s-N%d|pages=%s|%s" % (cid, cid, i, ",".join(pfs), n))
    for i, (n, c) in enumerate(withheld, 1):
        pfs = sorted(pf for pf in pages if n in present[pf])
        gate = "SINGLE_SOURCE" if c == 1 else "NO_CORROBORATION"
        lines.append("WITHHELD|%s|%s-W%d|%s|pages=%s|%s" % (cid, cid, i, gate, ",".join(pfs), n))
    return "\n".join(lines) + "\n"


def main():
    corpora_dir, guides_dir, out_dir = sys.argv[1], sys.argv[2], sys.argv[3]
    os.makedirs(out_dir, exist_ok=True)
    K = build_K(guides_dir)
    with open(os.path.join(out_dir, "K_SIZE.txt"), "w") as f:
        f.write("K_forms=%d\n" % len(K))
    for cid in sorted(os.listdir(corpora_dir)):
        cdir = os.path.join(corpora_dir, cid)
        if not os.path.isdir(cdir):
            continue
        report = run_corpus(cid, cdir, K)
        with open(os.path.join(out_dir, cid + ".report"), "w", encoding="utf-8", newline="\n") as f:
            f.write(report)
    print("scored %d corpora" % len([d for d in os.listdir(corpora_dir)
                                     if os.path.isdir(os.path.join(corpora_dir, d))]))


if __name__ == "__main__":
    main()
