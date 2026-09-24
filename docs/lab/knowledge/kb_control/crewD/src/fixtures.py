#!/usr/bin/env python3
"""Crew D deterministic fixtures.

Byte-exact mirror of the current store's record format and layout logic
(igb_append in ingest.zag @118251c5). No RNG. All generation is closed-form
from integer ids.
"""
import hashlib

HDR_LEN = 11  # kind(1) + id(4 LE) + klen(2 BE) + tlen(4 LE)


def keygen(fid: int) -> bytes:
    return ("k%06d" % fid).encode("ascii")


def textgen(fid: int, seq: int, tlen: int) -> bytes:
    return bytes(65 + ((fid * 31 + seq * 17 + j * 7) % 26) for j in range(tlen))


def bulk_tlen(fid: int, maxtextlen: int) -> int:
    return 1 + ((fid * 7919 + 13) % maxtextlen)


def record_bytes(kind: int, fid: int, key: bytes, text: bytes) -> bytes:
    return (
        bytes([kind])
        + fid.to_bytes(4, "little")
        + len(key).to_bytes(2, "big")
        + len(text).to_bytes(4, "little")
        + key
        + text
    )


def record_sha(kind: int, fid: int, key: bytes, text: bytes) -> str:
    return hashlib.sha256(record_bytes(kind, fid, key, text)).hexdigest()


def simulate_layout(n: int, chunk: int, maxtextlen: int, keylen: int = 7):
    """Mirror igb_append's TRUE byte layout.

    Returns (recs, boundaries) where recs[i] = dict(packed, chunk, inoff,
    reclen, tlen) and boundaries = list of (chunk_idx, last_id, tail_end).
    packed = b.total-style offset (padding-blind, what the slot stores).
    """
    recs = []
    boundaries = []
    off = 0          # in-chunk true offset (bb.used)
    ch = 0
    packed = 0       # b.total
    for i in range(n):
        tlen = bulk_tlen(i, maxtextlen)
        rl = HDR_LEN + keylen + tlen
        if off + rl > chunk:
            boundaries.append((ch, i - 1, off))
            ch += 1
            off = 0
        recs.append({"packed": packed, "chunk": ch, "inoff": off,
                     "reclen": rl, "tlen": tlen})
        off += rl
        packed += rl
    return recs, boundaries


def chunk_tail_padding(chunk: int, recs) -> dict:
    """Map chunk_idx -> padding bytes after its last record."""
    pad = {}
    for r in recs:
        pad[r["chunk"]] = chunk - (r["inoff"] + r["reclen"])
    return pad
