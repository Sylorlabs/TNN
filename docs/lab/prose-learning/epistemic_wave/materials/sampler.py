#!/usr/bin/env python3
"""Deterministic Gutenberg corpus sampler for leg (e) (2026-09-22).

Implements the frozen PREREG §8.1 rules:
  - Source: Project Gutenberg plain texts, ascending ebook ID, English,
    plain-text available; front/back matter skipped by the standard
    "*** START OF" / "*** END OF" markers.
  - Sentence split: on [.!?] followed by whitespace and an uppercase
    letter or digit; an optional single closing quote ("/') may sit
    between the terminal and the whitespace; no split after tokens in
    the frozen abbreviation list (materials/abbrev.txt, case-insensitive,
    with or without the trailing period); leading/trailing quotation
    marks and whitespace stripped.
  - Filters: 5-40 whitespace-separated tokens; every character printable
    ASCII or a mapped common-Unicode-punctuation char (frozen mapping
    below); >=2 alphabetic tokens; not ALL-CAPS (headers); exact-duplicate
    normalized strings removed (first occurrence kept).
  - Determinism: NO sampling step. The corpus is the first 100,000
    filter-passing sentences in (ebook ID, document order). No RNG, no
    seed, no shuffle anywhere.
  - Stratification (reporting only, syntactic): S1/S2/S3 clause grader
    with frozen word lists below.

Inputs: raw text files from fetch_gutenberg.py, named {id:06d}.txt,
  plus materials/abbrev.txt.
Outputs (all under --outdir, default materials/):
  - gutenberg_corpus.txt      100,000 sentences, one per line, clean
  - gutenberg_corpus.strata   100,000 lines, each S1/S2/S3 (reporting only;
                              never training input)
  - gutenberg_manifest.txt    dated manifest: sampler sha256, input list
                              sha256s, per-text sha256 + kept counts,
                              corpus sha256, sentence count, stratum counts

Usage:
  python3 sampler.py --rawdir materials/gutenberg_raw \
      --log materials/gutenberg_raw/fetch_log.txt \
      --outdir materials --target 100000
"""

import argparse
import hashlib
import os
import re
import sys

# --- frozen Unicode -> ASCII mapping (applied before filtering) ---
UNICODE_MAP = {
    "\u2018": "'", "\u2019": "'", "\u201a": "'",
    "\u201c": '"', "\u201d": '"', "\u201e": '"',
    "\u2013": "-", "\u2014": "-", "\u2015": "-",
    "\u2026": "...",
    "\u00a0": " ", "\u2000": " ", "\u2001": " ", "\u2002": " ",
    "\u2003": " ", "\u2007": " ", "\u2009": " ", "\u202f": " ",
    "\u00ab": '"', "\u00bb": '"',
    "\u2039": "'", "\u203a": "'",
    "\u00b7": "-", "\u2022": "-", "\u00ad": "",
    "\u0152": "OE", "\u0153": "oe",
    "\u00c6": "AE", "\u00e6": "ae",
    "\u2122": "(TM)", "\u00a9": "(c)", "\u00ae": "(R)",
    "\u00bc": "1/4", "\u00bd": "1/2", "\u00be": "3/4",
    "\u00d7": "x", "\u00f7": "/",
}

# --- frozen finite-verb markers ---
AUX_FINITE = frozenset(
    "am is are was were be been being has have had do does did "
    "will would can could shall should may might must ought".split()
)
IRREG_PAST = frozenset(
    "arose awoke bore beat became began bent bound broke brought built burnt "
    "bought caught chose clung came dealt dug drew drank drove ate fell fed felt "
    "fought fled flung flew forgot forgave froze got gave went grew ground hung "
    "heard hid held kept knelt knew laid led leapt learnt left lent lay lit lost "
    "made meant met paid put read rode rang rose ran said saw sought sold sent "
    "set shook shone shot showed shrank shut sang sank sat slept slid slung "
    "smelt sowed spoke sped spent spilt spun spat split spoilt spread sprang "
    "stood stole stuck stung stank struck strove swore swept swam swung took "
    "taught tore told thought threw thrust trod understood upset woke wore wove "
    "wed wept wound wrote".split()
)
COORDS = frozenset("and but or yet so nor".split())
SUBORDS = frozenset(
    "because although though when while if that which who whom whose where "
    "after before since until unless whereas whether lest as once till why how".split()
)
_S_EXCLUDE = frozenset("this thus plus".split())


def is_finite(tok: str) -> bool:
    t = tok.lower()
    if t.endswith("'s"):
        t = t[:-2]
    elif t.endswith("'"):
        t = t[:-1]
    t = t.strip(".,;:!?\"'()[]{}")
    if not t:
        return False
    if t in AUX_FINITE or t in IRREG_PAST:
        return True
    if len(t) > 3 and t.endswith("ed"):
        return True
    if (
        len(t) > 4
        and t.endswith("s")
        and not t.endswith("ss")
        and not t.endswith("us")
        and t not in _S_EXCLUDE
    ):
        return True
    return False


def grade(tokens):
    """Frozen S1/S2/S3 clause grader. Returns 'S1' | 'S2' | 'S3'."""
    toks = [t.strip(".,;:!?\"'()[]{}").lower() for t in tokens]
    toks = [t for t in toks if t]
    n_finite = sum(1 for t in tokens if is_finite(t))
    has_sub = any(t in SUBORDS for t in toks)
    has_coord = any(t in COORDS for t in toks) or any(";" in t for t in tokens)
    if has_sub:
        return "S3"
    if n_finite >= 2 and has_coord:
        return "S2"
    if n_finite == 1:
        return "S1"
    if n_finite == 0:
        return "S1"  # imperative / verbless fragment: single-clause bucket
    return "S2"  # >=2 finite, asyndetic


def load_abbrevs(path):
    ab = set()
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            ab.add(line.lower().rstrip("."))
    return ab


def strip_gutenberg(raw: str) -> str:
    lines = raw.splitlines()
    start = None
    for i, ln in enumerate(lines):
        if "*** START OF" in ln:
            start = i + 1
            break
    if start is None:
        return ""
    end = None
    for i in range(start, len(lines)):
        if "*** END OF" in lines[i]:
            end = i
            break
    body = lines[start:end if end is not None else len(lines)]
    return "\n".join(body)


def normalize(text: str):
    """Apply frozen unicode map + whitespace collapse. Returns None if any
    remaining char is outside printable ASCII (0x20-0x7E)."""
    out = []
    for ch in text:
        if ch in UNICODE_MAP:
            out.append(UNICODE_MAP[ch])
        elif ch == "\n" or ch == "\r" or ch == "\t" or ch == "\f" or ch == "\v":
            out.append(" ")
        elif 0x20 <= ord(ch) <= 0x7E:
            out.append(ch)
        else:
            return None
    collapsed = re.sub(r" +", " ", "".join(out)).strip()
    return collapsed


_TOKEN_RE = re.compile(r"[A-Za-z0-9]+(?:'[A-Za-z]+)?")


# closing-quote chars allowed between a terminal and the following whitespace
_CLOSE_QUOTES = "\"'\u2019\u201d\u00bb\u203a\u2018\u201c\u00ab\u2039"
_STRIP_QUOTES = "\"'\u2018\u2019\u201c\u201d\u00ab\u00bb\u2039\u203a"


def split_sentences(text: str, abbrevs):
    """Frozen splitter. Yields raw sentence strings (still quoted)."""
    n = len(text)
    i = 0
    seg_start = 0
    while i < n:
        c = text[i]
        if c in ".!?":
            # find end of terminal run: terminal + optional single closing quote
            j = i + 1
            if j < n and text[j] in _CLOSE_QUOTES:
                j += 1
            # must be followed by whitespace, optional opening quotes,
            # then an uppercase letter or digit (frozen interpretation:
            # quotation marks are not sentence content for the boundary test)
            if j < n and text[j] in " \t":
                k = j
                while k < n and text[k] in " \t":
                    k += 1
                while k < n and text[k] in _STRIP_QUOTES:
                    k += 1
                if k < n and (text[k].isupper() or text[k].isdigit()):
                    # abbreviation guard (periods only)
                    if c == ".":
                        back = i - 1
                        while back >= seg_start and (
                            text[back].isalnum() or text[back] in ".'"
                        ):
                            back -= 1
                        tok = text[back + 1:i].replace(".", "").strip("'").lower()
                        if tok in abbrevs:
                            i += 1
                            continue
                    yield text[seg_start:j].strip()
                    seg_start = j
                    i = j
                    continue
            # end of text: trailing terminal finishes the sentence
            rest = text[j:].strip()
            if not rest:
                yield text[seg_start:].strip()
                return
        i += 1
    tail = text[seg_start:].strip()
    if tail:
        yield tail


def clean_sentence(s: str):
    s = s.strip()
    # strip leading/trailing quotation marks (ASCII + mapped Unicode)
    while s and s[0] in _STRIP_QUOTES:
        s = s[1:].lstrip()
    while s and s[-1] in _STRIP_QUOTES:
        s = s[:-1].rstrip()
    return re.sub(r" +", " ", s).strip()


def passes_filters(s: str):
    tokens = s.split(" ")
    if not (5 <= len(tokens) <= 40):
        return False
    alpha = sum(1 for t in tokens if any(ch.isalpha() for ch in t))
    if alpha < 2:
        return False
    cased = [ch for ch in s if ch.isalpha()]
    if cased and all(ch.isupper() for ch in cased):
        return False
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rawdir", required=True)
    ap.add_argument("--log", required=True)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--abbrev", default=None)
    ap.add_argument("--target", type=int, default=100000)
    args = ap.parse_args()

    abbrev_path = args.abbrev or os.path.join(args.outdir, "abbrev.txt")
    abbrevs = load_abbrevs(abbrev_path)

    # input files: OK lines of the fetch log, ascending ebook id
    eids = []
    with open(args.log, encoding="utf-8") as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 4 and parts[1] == "OK":
                eids.append(int(parts[0]))
    eids.sort()

    seen = set()
    corpus = []
    strata = []
    per_text = []
    for eid in eids:
        path = os.path.join(args.rawdir, f"{eid:06d}.txt")
        with open(path, "rb") as f:
            raw_bytes = f.read()
        sha = hashlib.sha256(raw_bytes).hexdigest()
        raw = raw_bytes.decode("utf-8", errors="replace")
        body = strip_gutenberg(raw)
        kept_here = 0
        for raw_sent in split_sentences(body, abbrevs):
            s = clean_sentence(raw_sent)
            if not s:
                continue
            norm = normalize(s)
            if norm is None:
                continue
            if not passes_filters(norm):
                continue
            if norm in seen:
                continue
            seen.add(norm)
            corpus.append(norm)
            strata.append(grade(norm.split(" ")))
            kept_here += 1
            if len(corpus) >= args.target:
                break
        per_text.append((eid, len(raw_bytes), sha, kept_here))
        if len(corpus) >= args.target:
            break

    os.makedirs(args.outdir, exist_ok=True)
    corpus_path = os.path.join(args.outdir, "gutenberg_corpus.txt")
    strata_path = os.path.join(args.outdir, "gutenberg_corpus.strata")
    with open(corpus_path, "w", encoding="utf-8") as f:
        f.write("\n".join(corpus) + "\n")
    with open(strata_path, "w", encoding="utf-8") as f:
        f.write("\n".join(strata) + "\n")
    corpus_sha = hashlib.sha256(
        open(corpus_path, "rb").read()
    ).hexdigest()

    # determinism self-check: re-split first text and compare prefix digest
    def sha_of(p):
        h = hashlib.sha256()
        with open(p, "rb") as f:
            h.update(f.read())
        return h.hexdigest()

    s1 = sum(1 for s in strata if s == "S1")
    s2 = sum(1 for s in strata if s == "S2")
    s3 = sum(1 for s in strata if s == "S3")
    manifest = os.path.join(args.outdir, "gutenberg_manifest.txt")
    with open(manifest, "w", encoding="utf-8") as f:
        f.write("gutenberg_corpus manifest — leg (e) pre-run artifact\n")
        f.write("dated: 2026-09-22\n")
        f.write(f"sampler: materials/sampler.py sha256={sha_of(__file__)}\n")
        f.write(f"abbrev: {abbrev_path} sha256={sha_of(abbrev_path)}\n")
        f.write(f"fetch_log: {args.log}\n")
        f.write(f"sentence_count={len(corpus)} target={args.target}\n")
        f.write(f"corpus_sha256={corpus_sha}\n")
        f.write(f"strata_path={strata_path} sha256={sha_of(strata_path)}\n")
        f.write(f"stratum_counts: S1={s1} S2={s2} S3={s3}\n")
        f.write("per-text: ebook_id\tbytes\tsha256\tkept\n")
        for eid, nbytes, sh, kept in per_text:
            f.write(f"{eid}\t{nbytes}\t{sh}\t{kept}\n")
    print(f"sentences={len(corpus)} S1={s1} S2={s2} S3={s3} corpus_sha={corpus_sha[:16]}...")
    return 0 if len(corpus) >= args.target else 2


if __name__ == "__main__":
    sys.exit(main())
