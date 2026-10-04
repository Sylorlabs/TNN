#!/usr/bin/env python3
"""INTERNET HELL-HOLE TRIAL — thin transport bridge (Python, NOT TNN-side).

Phase 1: provenance-envelope helpers + frozen hash conventions + fixture
read/write + replay feed. Live web fetching lands in Phase 2 (gated on the
web-search sense delivery).

Hash conventions (frozen, shared with ws_sense.zag):
  result_hash v1 = sha256(url + "\\n" + title + "\\n" + snippet)   [hex]
  page_hash      = sha256(raw page bytes)                          [hex]
  sense entry    = sha256(prev_hash || seq_le64 || op || 0x00 || fact_id || 0x00
                          || query_hash || 0x00 || url_hash || 0x00
                          || value || 0x00 || domain)              [hex]

No decisions are made here: transport only. Deterministic given inputs.
"""
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def result_hash(url: str, title: str, snippet: str) -> str:
    """result_hash v1 — must match ws_sense.zag byte-for-byte."""
    return sha256_hex(("\n".join([url, title, snippet])).encode("utf-8"))


def page_hash(raw: bytes) -> str:
    return sha256_hex(raw)


def provenance_envelope(query, url, title, snippet, raw,
                        domain, seq, wall_time_iso):
    """The envelope every recorded page carries. wall_time lives ONLY here
    (Python side) — never in Zag — keeping scored reruns byte-identical."""
    return {
        "query": query,
        "url": url,
        "title": title,
        "snippet": snippet,
        "domain": domain,
        "result_hash": result_hash(url, title, snippet),
        "page_hash": page_hash(raw),
        "page_bytes": len(raw),
        "seq": seq,
        "recorded_at": wall_time_iso,  # envelope only; excluded from replay hashing
    }


def load_course():
    with open(os.path.join(HERE, "fixtures", "course.json")) as f:
        return json.load(f)


def write_events(path, events):
    with open(path, "w") as f:
        for e in events:
            f.write(json.dumps(e, sort_keys=True) + "\n")


def read_events(path):
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


# ---- Phase 2: live recording lands here ----
def record_live(query, max_pages=5):
    """Fetch live web results for query, return list of provenance envelopes
    (without raw bodies stored inline — bodies go to fixtures/pages/)."""
    raise NotImplementedError("Phase 2: gated on web-search sense delivery")
