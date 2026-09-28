"""vidio.py — .vid fixture writer for the youtube_ingest pipeline.

Format contract (must match harness gen.py write_vid EXACTLY):
    header  = struct "<III": (nframes, w, h), little-endian
    payload = for each frame (in order): w*h*3 raw RGB bytes,
              row-major (y down), 3 bytes per pixel (R,G,B)

No RNG. Pure byte layout. validate_vid.py proves layout equivalence against
both gen.py's write_vid and a real harness .vid fixture.
"""
import struct


def write_vid(path, w, h, frames):
    """frames: iterable of bytes-like, each exactly w*h*3 RGB bytes."""
    n = 0
    with open(path, "wb") as f:
        n = 0
        buf = []
        for fr in frames:
            if len(fr) != w * h * 3:
                raise ValueError("frame %d has %d bytes, expected %d"
                                 % (n, len(fr), w * h * 3))
            buf.append(bytes(fr))
            n += 1
        f.write(struct.pack("<III", n, w, h))
        for b in buf:
            f.write(b)
    return n


def read_vid_header(path):
    with open(path, "rb") as f:
        head = f.read(12)
    return struct.unpack("<III", head)
