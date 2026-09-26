#!/usr/bin/env python3
"""sense_trace_py.py — Python emitter for SENSE-TRACE v1 (same grammar as sense_trace.zag).

Purpose: instrument the Python side of the audio intake (proto5g.py hear())
with the identical per-stage SHA-256 trace format the Zag drivers emit, so one
verifier (trace_verify.py) checks both.

The sibling repairing the hear() head-sample bug (samples 0-63 never stored)
wraps hear()'s stages with this emitter. The repair's verification:
  1. run the traced hear() on fixture_strike.wav,
  2. compare its audio.head_samples_0_63 out-checksum to the golden
     f183085e661eabe4a09acf919b3c30bca568ea36828cd2ad3895eab45d996271
     (from the Zag audio driver's trace log — the true head bytes),
  3. trace_verify.py checks the whole chain.

Stage map for hear() (see TRACELOG_FORMAT.md for the full inventory):
  audio.wav_parse        in: wav bytes            out: payload bytes (data chunk)
  audio.head_samples_0_63 in: payload[0:128]      out: stored head bytes (fork)
  audio.lpc64            in: payload bytes        out: a.tobytes() (P f64)
  audio.residual         in: payload bytes        out: res.tobytes() (f64)
  audio.pitch            in: res.tobytes()        out: str(pT).encode()
  audio.t0_refine        in: res.tobytes()        out: struct.pack('<dd',T0,NBINS)
  audio.plm              in: res.tobytes()        out: plm.tobytes()
  audio.period_pmf       in: res.tobytes()        out: PMF.tobytes()
  audio.kmeans64         in: nres.tobytes()       out: proto.tobytes()+q.tobytes()
  audio.bigram_ep        in: q.tobytes()          out: bg.tobytes()+EP.tobytes()
  audio.boost_calib      in: res.tobytes()        out: struct.pack('<d',boost)
  audio.held_m5g         in: (model bytes)        out: m5g file bytes

Hashing rule: numpy arrays are hashed as arr.tobytes() (native dtype bytes);
dtype+shape go in params so the bytes are interpretable.

Zero RNG: this module hashes and writes; it never alters the data path.
Deterministic: no timestamps — same inputs give byte-identical logs.
"""

import hashlib
import struct


def sha_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


class TraceLog:
    def __init__(self, path: str, sense: str, fmt: str, params: str = ""):
        self.f = open(path, "w", encoding="utf-8")
        self.f.write("# SENSE-TRACE v1\n")
        self.sense = sense
        self.fmt = fmt
        self.params = params
        self._run_written = False

    def run(self, src_bytes: bytes, params: str = ""):
        p = params or self.params
        self.f.write(
            "RUN sense=%s format=%s src=%s params=%s\n"
            % (self.sense, self.fmt, sha_hex(src_bytes), p)
        )
        self._run_written = True

    def stage(self, seq: int, name: str, in_bytes, out_bytes, params: str = "",
              in_len: int = None, out_len: int = None):
        ib = in_bytes if isinstance(in_bytes, (bytes, bytearray)) else None
        ob = out_bytes if isinstance(out_bytes, (bytes, bytearray)) else None
        in_hex = sha_hex(bytes(ib)) if ib is not None else "-"
        out_hex = sha_hex(bytes(ob)) if ob is not None else "-"
        il = len(ib) if (ib is not None and in_len is None) else (in_len or 0)
        ol = len(ob) if (ob is not None and out_len is None) else (out_len or 0)
        self.f.write(
            "STAGE %d %s in=%s out=%s in_len=%d out_len=%d params=%s\n"
            % (seq, name, in_hex, out_hex, il, ol, params)
        )

    def head_stage(self, seq: int, payload_bytes: bytes, n_head: int = 64,
                   stored_bytes: bytes = None, fork_of: str = "audio.wav_parse"):
        """The traced head-sample stage. stored_bytes=None means 'not stored'
        (the bug): records stored=0 and out=- so verification fails loudly."""
        nbytes = n_head * 2
        head_in = bytes(payload_bytes[:nbytes])
        if stored_bytes is None:
            self.stage(seq, "audio.head_samples_0_63", head_in, None,
                       "fork_of=%s,stored=0,n_head=%d" % (fork_of, n_head))
        else:
            self.stage(seq, "audio.head_samples_0_63", head_in,
                       bytes(stored_bytes[:nbytes]),
                       "fork_of=%s,stored=1,n_head=%d" % (fork_of, n_head))

    def held(self, out_bytes: bytes, desc: str):
        ob = bytes(out_bytes)
        self.f.write("HELD sha=%s len=%d desc=%s\n"
                     % (sha_hex(ob), len(ob), desc))

    def end(self, rc: int = 0):
        self.f.write("END rc=%d\n" % rc)
        self.f.close()


def pack_f64(*vals) -> bytes:
    return struct.pack("<%dd" % len(vals), *vals)


def arr_bytes(a) -> bytes:
    """Hashable bytes of a numpy array (tobytes); params should carry dtype+shape."""
    return a.tobytes()
