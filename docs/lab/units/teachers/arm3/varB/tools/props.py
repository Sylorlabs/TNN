#!/usr/bin/env python3
"""§P v1 proposal codec + validator (frozen PREREG §4 B.3, teacher_id=3).

Used by the arm-3 varB verification harness. Pure Python, deterministic.
"""
import struct

MAGIC = 1414550096
VERSION = 1

def fnv1a(data: bytes) -> int:
    h = 14695981039346656037
    for b in data:
        h ^= b
        h = (h * 1099511628211) & 0xFFFFFFFFFFFFFFFF
    return h

def parse_stream(buf: bytes, stim_len: int, expect_tid=3, expect_sess=None,
                 expect_seq0=0):
    """Parse concatenated §P proposals. Returns list of dicts. Raises on any
    iron-rule violation (mirrors the student's ingress gate)."""
    props = []
    off = 0
    seq = expect_seq0
    while off < len(buf):
        if len(buf) - off < 44:
            raise ValueError(f"truncated proposal header at {off}")
        magic, ver, tid, sess, pseq = struct.unpack_from("<IHIQQ", buf, off)
        if magic != MAGIC:
            raise ValueError(f"bad magic at {off}")
        if ver != VERSION:
            raise ValueError(f"bad version at {off}")
        if tid not in (1, 3, 4, 5):
            raise ValueError(f"bad teacher_id {tid}")
        if expect_tid is not None and tid != expect_tid:
            raise ValueError(f"teacher_id {tid} != {expect_tid}")
        if expect_sess is not None and sess != expect_sess:
            raise ValueError(f"session_id {sess} != {expect_sess}")
        if pseq != seq:
            raise ValueError(f"seq {pseq} != expected {seq} (monotonic)")
        kind = buf[off + 26]
        if kind not in (1, 2, 3, 4, 5):
            raise ValueError(f"bad kind {kind}")
        ss, se = struct.unpack_from("<QQ", buf, off + 27)
        auxn = buf[off + 43]
        if kind in (1, 2, 5) and auxn != 0:
            raise ValueError("aux_count nonzero for WORD_SPAN/BOUNDARY/RETRACT")
        p = off + 44
        aux = []
        for _ in range(auxn):
            a, b = struct.unpack_from("<QQ", buf, p)
            if not (a < b <= stim_len):
                raise ValueError(f"bad aux span {(a, b)}")
            aux.append((a, b))
            p += 16
        gn = buf[p]
        p += 1
        grounds = []
        for _ in range(gn):
            a, b = struct.unpack_from("<QQ", buf, p)
            if not (a < b <= stim_len):
                raise ValueError(f"bad grounding span {(a, b)}")
            grounds.append((a, b))
            p += 16
        conf = buf[p]
        p += 1
        ck = struct.unpack_from("<Q", buf, p)[0]
        if fnv1a(buf[off:p]) != ck:
            raise ValueError(f"checksum mismatch at seq {pseq}")
        if kind == 5:
            if not (ss >= 1 and se == ss + 1):
                raise ValueError("RETRACT must encode target/target+1")
        else:
            if not (ss < se <= stim_len):
                raise ValueError(f"bad span {(ss, se)}")
        if conf == 255:
            raise ValueError("confidence 255 forbidden (tripwire bait)")
        p += 8
        props.append(dict(seq=pseq, kind=kind, ss=ss, se=se, aux=aux,
                          grounds=grounds, conf=conf, length=p - off))
        off = p
        seq += 1
    return props

HIST_MAGIC = 1414744392

def write_history(path, records):
    """records: list of (seq, kind, verdict, reason, ss, se)."""
    with open(path, "wb") as f:
        f.write(struct.pack("<IHI", HIST_MAGIC, 1, len(records)))
        for (seq, kind, verdict, reason, ss, se) in records:
            f.write(struct.pack("<Q", seq))
            f.write(bytes([kind, verdict, reason, 0]))
            f.write(struct.pack("<QQ", ss, se))
            f.write(struct.pack("<I", 0))

def verdict_name(v):
    return {0: "ADOPT", 1: "REVISE", 2: "REJECT", 3: "DEFER"}[v]

def kind_name(k):
    return {1: "WORD_SPAN", 2: "BOUNDARY", 3: "GROUP", 4: "SAME_AS",
            5: "RETRACT"}[k]
