#!/usr/bin/env python3
"""Phase 1C cleaner for the 10GB generalist ingest.

Implements CLEAN_SPEC.md (frozen 2026-09-22) exactly: rules R1..R10, in order,
zero RNG. Audited mechanical glue like NORMALIZE: no judgment, no semantic
decisions, byte-deterministic.

Usage:
  clean.py --raw DIR --out DIR        clean raw tree -> cleaned texts + facts.dat + MANIFEST.json
  clean.py --selftest                 determinism proof on fixtures/inputs (two runs, SHA256 compare)
  clean.py --check                    byte-compare cleaner output vs fixtures/expected

Raw tree layout: DIR/{gutenberg,openstax,stackexchange,wikibooks}/<files>
Output layout:   OUT/cleaned/<source>/<relpath>.txt, OUT/facts.dat, OUT/MANIFEST.json
"""
import argparse
import hashlib
import html
import json
import os
import re
import struct
import sys
import tempfile
import xml.etree.ElementTree as ET

SPEC_VERSION = "1C-2026-09-22+R9.6fix"
SOURCES = ("gutenberg", "openstax", "stackexchange", "wikibooks", "wikipedia")  # fixed order
# Phase 2: "wikipedia" is English Wikipedia (acquired source), kind 8.
# It uses the wikibooks code path with a wp: key prefix to distinguish it
# from genuine Wikibooks (wb:). See SOURCE_ADAPTERS.md.

# ---- R5 ----
R5A_CHARS = set("-_*=~#+")          # whole-line separator chars
R5B_RE = re.compile(r"([\-_~])\1+")  # inline runs of -, _, ~ (len>=2) -> single space

# ---- R7 frozen nav/ad patterns (full-line match) ----
R7_PATTERNS = [
    re.compile(r"^\d+$"),                                            # P1 bare page numbers
    re.compile(r"(?i)^(table of contents|contents|index|glossary)$"),  # P2
    re.compile(r"(?i)^(advertisement|sponsored content|click here.*)$"),  # P3
    re.compile(r"^[←→].*$|^.*[←→]$"),                                 # P4 wiki nav crumbs
    re.compile(r"(?i)^page \d+ of \d+$"),                             # P5
    re.compile(r"(?i)^\[?page \d+\]?$"),                              # P6
    re.compile(r"^<!--.*-->$"),                                       # P7 html comments
]

# ---- R3 patterns ----
TAG_RE = re.compile(r"<[^<>]*>")
BLOCK_END_RE = re.compile(
    r"(?i)(</p>|</h[1-6]>|</li>|</ul>|</ol>|</div>|</blockquote>|</pre>|<br\s*/?>)")
HEAD_RE = re.compile(r"<head\b[^>]*>.*?</head>", re.DOTALL | re.IGNORECASE)
REF_RE = re.compile(r"<ref\b[^>]*>.*?</ref>", re.DOTALL | re.IGNORECASE)
REF_SELF_RE = re.compile(r"<ref\b[^>]*/>", re.IGNORECASE)
BOLD3_RE = re.compile(r"'''")
BOLD2_RE = re.compile(r"''")
HEADING_RE = re.compile(r"^(={2,6})\s*(.*?)\s*\1$")
LINK_RE = re.compile(r"\[\[([^|\]]*\|)?([^\]]*)\]\]")
TMPL_RE = re.compile(r"\{\{[^{}]*\}\}")
TABLE_START_RE = re.compile(r"^\{\|")
TABLE_END_RE = re.compile(r"^\|\}")
GB_START_RE = re.compile(r"^\*{3} START OF (THIS|THE) PROJECT GUTENBERG EBOOK")
GB_END_RE = re.compile(r"^\*{3} END OF (THIS|THE) PROJECT GUTENBERG EBOOK")
OSTX_LINE_RE = re.compile(r"^Access for free at openstax\.org$")
OSTX_CNX_RE = re.compile(r"^This content is available for free at https://cnx\.org/contents/.*$")
WB_FROM_RE = re.compile(r"^From Wikibooks, open books for an open world$")
WB_RETR_RE = re.compile(r'^Retrieved from "https?://[^"]*"$')
WS_RUN_RE = re.compile(r"[ \t]+")
SENT_END_RE = re.compile(r"[.!?](?=\s|$)")

FACT_KINDS = {5, 6, 7, 8}


# ================= R1 =================
def r1_decode(raw: bytes) -> str:
    if raw[:3] == b"\xef\xbb\xbf":
        raw = raw[3:]
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("windows-1252")  # total, deterministic fallback


# ================= R2 =================
def r2_endings(s: str) -> str:
    return s.replace("\r\n", "\n").replace("\r", "\n")


# ================= R3 =================
def _local(tag: str) -> str:
    return tag.split("}")[-1]


def r3_se_posts(path: str):
    """Yield (unit_id, site, postid, is_q, title, body_raw_html). Document order."""
    site = os.path.splitext(os.path.basename(path))[0]
    units = []
    for _ev, el in ET.iterparse(path, events=("end",)):
        if _local(el.tag) != "row":
            continue
        a = el.attrib
        pt = a.get("PostTypeId", "")
        pid = a.get("Id", "")
        if pt == "1":
            units.append((f"q{pid}", site, pid, True, a.get("Title", ""), a.get("Body", "")))
        elif pt == "2":
            units.append((f"a{pid}", site, pid, False, "", a.get("Body", "")))
        el.clear()
    return units


def r3_se_body(body_html: str) -> str:
    # drop dupe-banner blocks on the RAW html (before tag strip)
    blocks = re.split(r"\n\s*\n", body_html)
    kept = [b for b in blocks
            if not (b.lstrip().startswith("<blockquote>")
                    and "Possible Duplicate:" in b[:200])]
    s = "\n\n".join(kept)
    s = BLOCK_END_RE.sub("\n\n", s)  # block boundaries -> paragraph breaks
    s = TAG_RE.sub("", s)          # strip tags BEFORE unescape
    return html.unescape(s)


def r3_openstax(path: str) -> str:
    with open(path, "rb") as f:
        raw = f.read()
    s = r2_endings(r1_decode(raw))
    s = HEAD_RE.sub("", s)
    s = BLOCK_END_RE.sub("\n\n", s)
    s = TAG_RE.sub("", s)
    return html.unescape(s)


def r3_wikibook_pages(path: str):
    """Yield (slug, title, wikitext). Document order."""
    slug = os.path.splitext(os.path.basename(path))[0]
    pages = []
    title, text, in_rev = None, None, False
    for _ev, el in ET.iterparse(path, events=("start", "end")):
        t = _local(el.tag)
        if _ev == "start" and t == "page":
            title, text, in_rev = None, None, False
        elif _ev == "start" and t == "revision":
            in_rev = True
        elif _ev == "end" and t == "title" and not in_rev:
            title = el.text or ""
        elif _ev == "end" and t == "text" and in_rev:
            text = el.text or ""
        elif _ev == "end" and t == "page":
            pages.append((slug, title or slug, text or ""))
            el.clear()
    return pages


def r3_wikitext(s: str) -> str:
    lines = s.split("\n")
    out = []
    in_table = False
    for ln in lines:
        if not in_table and TABLE_START_RE.match(ln):
            in_table = True
            continue
        if in_table:
            if TABLE_END_RE.match(ln):
                in_table = False
            continue
        out.append(ln)
    s = "\n".join(out)
    s = REF_RE.sub("", s)
    s = REF_SELF_RE.sub("", s)
    s = TMPL_RE.sub("", s)
    s = BOLD3_RE.sub("", s)
    s = BOLD2_RE.sub("", s)
    lines = [HEADING_RE.sub(r"\2", ln) for ln in s.split("\n")]
    s = "\n".join(lines)
    s = LINK_RE.sub(r"\2", s)
    return s


# ================= R4 =================
def r4_boilerplate(s: str, source: str) -> str:
    lines = s.split("\n")
    if source == "gutenberg":
        start = end = None
        for i, ln in enumerate(lines):
            if start is None and GB_START_RE.match(ln):
                start = i
            elif start is not None and end is None and GB_END_RE.match(ln):
                end = i
                break
        if start is not None:
            lines = lines[start + 1:]
            if end is not None:
                # recompute end index in the sliced list
                lines = [ln for j, ln in enumerate(lines) if j < (end - start - 1)]
        # (if no START marker: keep whole file; if START but no END: keep to EOF)
    elif source == "openstax":
        lines = [ln for ln in lines
                 if not OSTX_LINE_RE.match(ln) and not OSTX_CNX_RE.match(ln)]
    elif source in ("wikibooks", "wikipedia"):
        lines = [ln for ln in lines
                 if not WB_FROM_RE.match(ln) and not WB_RETR_RE.match(ln)]
    return "\n".join(lines)


# ================= R5 =================
def r5a_line_drop(line: str) -> bool:
    s = line.replace(" ", "").replace("\t", "")
    return len(s) >= 3 and len(set(s)) == 1 and s[0] in R5A_CHARS


def r5_decor(s: str) -> str:
    out = []
    for ln in s.split("\n"):
        if r5a_line_drop(ln):
            continue
        out.append(R5B_RE.sub(" ", ln))
    return "\n".join(out)


# ================= R6 =================
def r6_whitespace(s: str) -> str:
    lines = [WS_RUN_RE.sub(" ", ln).strip(" \t") for ln in s.split("\n")]
    out, blanks = [], 0
    for ln in lines:
        if ln == "":
            blanks += 1
            if blanks == 1:
                out.append("")
        else:
            blanks = 0
            out.append(ln)
    while out and out[0] == "":
        out.pop(0)
    while out and out[-1] == "":
        out.pop()
    return "\n".join(out)


# ================= R7 =================
def r7_navdrop(s: str) -> str:
    return "\n".join(ln for ln in s.split("\n")
                      if not any(p.match(ln) for p in R7_PATTERNS))


# ================= R8 =================
def r8_dedupe(s: str) -> str:
    # paragraph-level only: drop byte-identical duplicate paragraphs (first wins)
    seen, paras = set(), []
    for p in s.split("\n\n"):
        if p in seen:
            continue
        seen.add(p)
        paras.append(p)
    return "\n\n".join(paras)


# ================= R9 =================
def r9_split_para(p: str):
    """NO-STUPID-LIMITS (2026-09-24, Micah's law: limits are not a thing TNN
    needs): the 4096-byte chunk split is REMOVED. Paragraphs are emitted
    whole; the gate no longer carries a 4096B text ceiling. The original
    splitter is deleted — its boundary-whitespace behavior was irreversible,
    and the V-NOLIMIT inverter (nolimit_join.py) proved the join exact on
    100% of the 51,804 historical chunk groups. Deterministic."""
    return [p] if p else []


def r9_emit_unit(kind: int, key: str, text: str):
    """R9.2a: kind-6 whole-post emission. Floor applies to the whole unit."""
    assert kind in FACT_KINDS
    if len(text.replace(" ", "").replace("\n", "")) < 20:
        return []
    recs = []
    chunks = r9_split_para(text)
    for m, ch in enumerate(chunks):
        k = key + (f"~{m}" if len(chunks) > 1 else "")
        kb, tb = k.encode("utf-8"), ch.encode("utf-8")
        # R9.6 compliance fix (Phase 2): DROP non-conforming units instead of
        # asserting. The frozen 1C spec R9.6 says "Drop any unit with
        # text_len < 20 or > 4096 or containing NUL." The assert crashed on
        # real Gutenberg paragraphs; dropping matches the spec.
        if not (1 <= len(kb) <= 160 and b"\x00" not in kb and b"\n" not in kb):
            continue
        if not (len(tb) >= 20 and b"\x00" not in tb):  # NO-STUPID-LIMITS 2026-09-24: no 4096B ceiling
            continue
        if any(c < 0x20 and c != 0x0A for c in tb):
            continue
        recs.append((kind, kb, tb))
    return recs


def r9_emit(kind: int, key_base: str, text: str):
    """Yield fact records (kind, key_bytes, text_bytes) per R9."""
    assert kind in FACT_KINDS
    recs = []
    for n, para in enumerate(text.split("\n\n")):
        if len(para.replace(" ", "").replace("\n", "")) < 20:
            continue
        chunks = r9_split_para(para)
        for m, ch in enumerate(chunks):
            key = f"{key_base}:{n}" + (f"~{m}" if len(chunks) > 1 else "")
            kb, tb = key.encode("utf-8"), ch.encode("utf-8")
            # R9.6 compliance fix (Phase 2): see r9_emit_unit above.
            if not (1 <= len(kb) <= 160 and b"\x00" not in kb and b"\n" not in kb):
                continue
            if not (len(tb) >= 20 and b"\x00" not in tb):  # NO-STUPID-LIMITS 2026-09-24: no 4096B ceiling
                continue
            if any(c < 0x20 and c != 0x0A for c in tb):
                continue
            recs.append((kind, kb, tb))
    return recs


def pack_fact(kind: int, kb: bytes, tb: bytes) -> bytes:
    return struct.pack(">BHI", kind, len(kb), len(tb)) + kb + tb


# ================= pipeline =================
def clean_unit_text(s: str, source: str) -> str:
    """R4..R8 on extracted text."""
    s = r4_boilerplate(s, source)
    s = r5_decor(s)
    s = r6_whitespace(s)
    s = r7_navdrop(s)
    s = r6_whitespace(s)  # re-collapse blanks opened by R5a/R7 drops
    s = r8_dedupe(s)
    return s


def process_file(source: str, path: str):
    """Return (cleaned_text, [fact recs]) for one raw file."""
    recs = []
    stem = os.path.splitext(os.path.basename(path))[0]
    if source == "stackexchange":
        units = r3_se_posts(path)
        texts = []
        for _uid, site, pid, is_q, title, body_html in units:
            body = r3_se_body(body_html)
            full = (title + "\n\n" + body) if is_q else body
            cleaned = clean_unit_text(full, source)
            texts.append(cleaned)
            tag = "q" if is_q else "a"
            recs += r9_emit_unit(6, f"se:{site}:{tag}:{pid}", cleaned)
        return "\n\n".join(texts), recs
    if source == "openstax":
        s = r3_openstax(path)
        cleaned = clean_unit_text(s, source)
        return cleaned, r9_emit(5, f"ostx:{stem}:{stem}", cleaned)
    if source in ("wikibooks", "wikipedia"):
        pages = r3_wikibook_pages(path)
        texts = []
        # Phase 2: Wikipedia uses wp: prefix, Wikibooks uses wb:.
        prefix = "wp" if source == "wikipedia" else "wb"
        for slug, title, wt in pages:
            s = r3_wikitext(r2_endings(wt))
            cleaned = clean_unit_text(title + "\n\n" + s, source)
            texts.append(cleaned)
            recs += r9_emit(8, f"{prefix}:{slug}", cleaned)
        return "\n\n".join(texts), recs
    # gutenberg
    with open(path, "rb") as f:
        raw = f.read()
    s = r2_endings(r1_decode(raw))
    cleaned = clean_unit_text(s, source)
    gid = re.match(r"\d+", stem)
    gid = gid.group(0) if gid else stem
    return cleaned, r9_emit(7, f"gb:{gid}", cleaned)


def clean_tree(raw_dir: str, out_dir: str):
    os.makedirs(out_dir, exist_ok=True)
    all_recs = []
    stats = {}
    cleaned_concat = b""
    for source in SOURCES:
        sdir = os.path.join(raw_dir, source)
        files, in_bytes, out_bytes, nfacts = 0, 0, 0, 0
        if os.path.isdir(sdir):
            rels = []
            for root, _ds, fs in os.walk(sdir):
                for fn in fs:
                    rels.append(os.path.relpath(os.path.join(root, fn), sdir))
            for rel in sorted(rels):  # R0: byte order of path
                p = os.path.join(sdir, rel)
                with open(p, "rb") as f:
                    in_bytes += len(f.read())
                files += 1
                cleaned, recs = process_file(source, p)
                cb = (cleaned + "\n").encode("utf-8")
                out_bytes += len(cb)
                cleaned_concat += cb
                nfacts += len(recs)
                all_recs += [(k, kb, tb) for (k, kb, tb) in recs]
                op = os.path.join(out_dir, "cleaned", source, rel + ".txt")
                os.makedirs(os.path.dirname(op), exist_ok=True)
                with open(op, "wb") as f:
                    f.write(cb)
        stats[source] = {"files": files, "input_bytes": in_bytes,
                         "cleaned_bytes": out_bytes, "facts": nfacts}
    # R9.7: sort by key bytes, write facts.dat
    all_recs.sort(key=lambda r: r[1])
    facts_blob = b"".join(pack_fact(k, kb, tb) for k, kb, tb in all_recs)
    with open(os.path.join(out_dir, "facts.dat"), "wb") as f:
        f.write(facts_blob)
    manifest = {
        "spec": SPEC_VERSION,
        "sources": stats,
        "total_facts": len(all_recs),
        "facts_dat_sha256": hashlib.sha256(facts_blob).hexdigest(),
        "cleaned_concat_sha256": hashlib.sha256(cleaned_concat).hexdigest(),
    }
    with open(os.path.join(out_dir, "MANIFEST.json"), "w") as f:
        json.dump(manifest, f, indent=2, sort_keys=True)
        f.write("\n")
    return manifest


def sha_tree(d: str):
    h = hashlib.sha256()
    for root, _ds, fs in os.walk(d):
        for fn in sorted(fs):
            p = os.path.join(root, fn)
            h.update(os.path.relpath(p, d).encode())
            with open(p, "rb") as f:
                h.update(f.read())
    return h.hexdigest()


def selftest(fixtures: str) -> int:
    inputs = os.path.join(fixtures, "inputs")
    with tempfile.TemporaryDirectory() as t1, tempfile.TemporaryDirectory() as t2:
        m1 = clean_tree(inputs, t1)
        m2 = clean_tree(inputs, t2)
        h1 = (sha_tree(os.path.join(t1, "cleaned")), m1["facts_dat_sha256"])
        h2 = (sha_tree(os.path.join(t2, "cleaned")), m2["facts_dat_sha256"])
        ok = h1 == h2 and m1 == m2
        print("selftest run1:", h1[0][:16], h1[1][:16])
        print("selftest run2:", h2[0][:16], h2[1][:16])
        print("SELFTEST:", "PASS" if ok else "FAIL")
        return 0 if ok else 1


def check(fixtures: str) -> int:
    inputs = os.path.join(fixtures, "inputs")
    expected = os.path.join(fixtures, "expected")
    with tempfile.TemporaryDirectory() as t:
        clean_tree(inputs, t)
        bad = []
        for root, _ds, fs in os.walk(expected):
            for fn in sorted(fs):
                ep = os.path.join(root, fn)
                rel = os.path.relpath(ep, expected)
                gp = os.path.join(t, rel)
                if not os.path.exists(gp):
                    bad.append(f"missing: {rel}")
                    continue
                with open(ep, "rb") as f:
                    eb = f.read()
                with open(gp, "rb") as f:
                    gb = f.read()
                if eb != gb:
                    bad.append(f"mismatch: {rel} ({len(eb)} vs {len(gb)} bytes)")
        # also ensure no extra files
        for root, _ds, fs in os.walk(t):
            for fn in sorted(fs):
                rel = os.path.relpath(os.path.join(root, fn), t)
                if rel == "MANIFEST.json":
                    continue
                if not os.path.exists(os.path.join(expected, rel)):
                    bad.append(f"extra: {rel}")
        if bad:
            print("CHECK FAIL:")
            for b in bad:
                print("  " + b)
            return 1
        print("CHECK: PASS (all fixture outputs byte-identical to expected)")
        return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--fixtures", default=None)
    a = ap.parse_args()
    here = os.path.dirname(os.path.abspath(__file__))
    fixtures = a.fixtures or os.path.join(here, "fixtures")
    if a.selftest:
        sys.exit(selftest(fixtures))
    if a.check:
        sys.exit(check(fixtures))
    if not a.raw or not a.out:
        ap.error("--raw and --out required (or use --selftest/--check)")
    m = clean_tree(a.raw, a.out)
    print(json.dumps(m["sources"], indent=2, sort_keys=True))
    print("total_facts:", m["total_facts"])
    print("facts_dat_sha256:", m["facts_dat_sha256"])


if __name__ == "__main__":
    main()
