#!/usr/bin/env python3
"""History-tape + §P wire helpers for the arm-3 variation-C teacher."""
import struct, subprocess, os

MAGIC = 0x48434454
VERSION = 1
STIM_LEN = 65536
REC = 256
HDR = 32

TAG_PROPOSE = 1
TAG_DECIDE = 2

# verdicts
ADOPT, REVISE, REJECT, DEFER = 1, 2, 3, 4
# reasons
R1, R2, R3, R4, R5, R6 = 1, 2, 3, 4, 5, 6

# §P layout
P_MAGIC = 0x54505250

def fnv1a64(data: bytes) -> int:
    h = 0xCBF29CE484222325
    for b in data:
        h ^= b
        h = (h * 0x100000001B3) & 0xFFFFFFFFFFFFFFFF
    return h

def parse_proposal(buf: bytes):
    """Parse §P wire bytes -> dict; raises ValueError on structural problems."""
    if len(buf) < 54:
        raise ValueError("too short")
    magic, ver, tid = struct.unpack_from("<IHI", buf, 0)
    if magic != P_MAGIC:
        raise ValueError("bad magic")
    if ver != 1:
        raise ValueError("bad version")
    if tid != 3:
        raise ValueError("bad teacher_id")
    session_id, seq = struct.unpack_from("<QQ", buf, 10)
    kind = buf[26]
    ss, se = struct.unpack_from("<QQ", buf, 27)
    ac = buf[43]
    if ac > 8:
        raise ValueError("bad aux_count")
    go = 44 + 16 * ac
    if len(buf) < go + 1:
        raise ValueError("truncated")
    gc = buf[go]
    if gc > 8:
        raise ValueError("bad ground_count")
    want = go + 1 + 16 * gc + 1 + 8
    if len(buf) != want:
        raise ValueError(f"length mismatch: {len(buf)} != {want}")
    co = go + 1 + 16 * gc
    conf = buf[co]
    ck, = struct.unpack_from("<Q", buf, co + 1)
    if fnv1a64(buf[:co + 1]) != ck:
        raise ValueError("checksum mismatch")
    aux = [struct.unpack_from("<QQ", buf, 44 + 16 * i) for i in range(ac)]
    gnd = [struct.unpack_from("<QQ", buf, go + 1 + 16 * i) for i in range(gc)]
    return dict(session_id=session_id, seq=seq, kind=kind, ss=ss, se=se,
                aux=aux, gnd=gnd, conf=conf, nbytes=len(buf))

def new_history(session_id: int) -> bytes:
    hdr = bytearray(HDR)
    struct.pack_into("<I", hdr, 0, MAGIC)
    struct.pack_into("<H", hdr, 4, VERSION)
    struct.pack_into("<Q", hdr, 8, session_id)
    struct.pack_into("<Q", hdr, 16, STIM_LEN)
    struct.pack_into("<I", hdr, 24, 0)
    return bytes(hdr)

def nevents(hist: bytes) -> int:
    return struct.unpack_from("<I", hist, 24)[0]

def append_propose(hist: bytes, p: dict) -> bytes:
    n = nevents(hist)
    h = bytearray(hist)
    rec = bytearray(REC)
    rec[0] = TAG_PROPOSE
    struct.pack_into("<Q", rec, 1, p["seq"])
    rec[9] = p["kind"]
    struct.pack_into("<QQ", rec, 10, p["ss"], p["se"])
    rec[26] = p["conf"]
    rec[27] = len(p["aux"])
    rec[28] = len(p["gnd"])
    for i, (s, e) in enumerate(p["aux"][:2]):
        struct.pack_into("<QQ", rec, 29 + 16 * i, s, e)
    for i, (s, e) in enumerate(p["gnd"][:4]):
        struct.pack_into("<QQ", rec, 61 + 16 * i, s, e)
    struct.pack_into("<I", h, 24, n + 1)
    return bytes(h) + bytes(rec)

def append_decide(hist: bytes, seq: int, verdict: int, reason: int = 0,
                  rs: int = 0, re: int = 0) -> bytes:
    n = nevents(hist)
    h = bytearray(hist)
    rec = bytearray(REC)
    rec[0] = TAG_DECIDE
    struct.pack_into("<Q", rec, 1, seq)
    rec[9] = verdict
    struct.pack_into("<H", rec, 10, reason)
    struct.pack_into("<QQ", rec, 12, rs, re)
    struct.pack_into("<I", h, 24, n + 1)
    return bytes(h) + bytes(rec)

class Teacher:
    def __init__(self, binary, wired_dir):
        self.binary = binary
        self.wired = wired_dir

    def run(self, mode, slice_idx, session_id, hist_path, want_stdout=True):
        """Run teacher; returns (exit_code, stdout_bytes, stderr_text)."""
        hdir, hname = os.path.split(os.path.abspath(hist_path))
        p = subprocess.run(
            [self.binary, mode, str(slice_idx), str(session_id),
             self.wired, hdir, hname],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return p.returncode, p.stdout, p.stderr.decode("utf-8", "replace")

    def propose(self, slice_idx, session_id, hist_path):
        rc, out, err = self.run("propose", slice_idx, session_id, hist_path)
        if rc != 0:
            raise RuntimeError(f"teacher propose failed rc={rc}: {err}")
        p = parse_proposal(out)
        # diagnostics line: last line of stderr like
        # E=120 BAND=warm ACT=fresh SEQ=3 KIND=1 SS=.. SE=.. CONF=.. AC=.. GC=..
        diag = {}
        for line in err.strip().split("\n"):
            if line.startswith("E="):
                for tok in line.split():
                    k, _, v = tok.partition("=")
                    diag[k] = v
        return p, diag
