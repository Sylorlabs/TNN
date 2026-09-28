#!/usr/bin/env python3
"""Measurement-only tooling for the Goal-A video fix crew.
Parses uncompressed 24-bit RGB AVI (RIFF) files written by f3_emit_avi_g:
extracts video frames (00dc chunks), computes per-frame mean abs diff,
temporal-median background estimates, subject presence, and writes PNGs.
No generation: reads bytes only.
"""
import struct, sys, os, math

def parse_avi(path):
    with open(path, 'rb') as f:
        data = f.read()
    assert data[:4] == b'RIFF' and data[8:12] == b'AVI ', 'not an AVI'
    # find movi list
    movi_off = data.find(b'movi')
    assert movi_off > 0
    # walk chunks inside LIST movi: chunk layout: id(4) size(4) data
    off = movi_off + 4
    frames = []
    audios = []
    while off + 8 <= len(data):
        cid = data[off:off+4]
        if cid == b'idx1':
            break
        (sz,) = struct.unpack('<I', data[off+4:off+8])
        if cid == b'00dc':
            frames.append(data[off+8:off+8+sz])
        elif cid == b'01wb':
            audios.append(data[off+8:off+8+sz])
        off += 8 + sz + (sz & 1)
    return frames, audios

def frame_to_rows(raw, W, H):
    # bottom-up BGR -> top-down RGB rows of bytes
    rowbytes = W * 3
    rows = []
    for r in range(H):
        srow = (H - 1 - r) * rowbytes
        brow = raw[srow:srow+rowbytes]
        # BGR -> RGB
        rgb = bytearray(rowbytes)
        rgb[0::3] = brow[2::3]
        rgb[1::3] = brow[1::3]
        rgb[2::3] = brow[0::3]
        rows.append(bytes(rgb))
    return rows

def mean_abs_diff(a, b):
    n = len(a)
    tot = 0
    for i in range(n):
        d = a[i] - b[i]
        if d < 0: d = -d
        tot += d
    return tot / n

def write_png(path, rows, W, H):
    import zlib
    raw = b''.join(b'\x00' + r for r in rows)
    def chunk(typ, payload):
        c = typ + payload
        return struct.pack('>I', len(payload)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)
    ihdr = struct.pack('>IIBBBBB', W, H, 8, 2, 0, 0, 0)
    png = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr) + chunk(b'IDAT', zlib.compress(raw, 6)) + chunk(b'IEND', b'')
    with open(path, 'wb') as f:
        f.write(png)

def luma_rows(rows):
    out = []
    for r in rows:
        lr = bytearray(len(r)//3)
        for i in range(len(lr)):
            lr[i] = (r[3*i]*77 + r[3*i+1]*150 + r[3*i+2]*29) >> 8
        out.append(bytes(lr))
    return out

if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'info':
        path = sys.argv[2]
        frames, audios = parse_avi(path)
        W = H = 480
        print(f'file={path} bytes={os.path.getsize(path)} nframes={len(frames)} naudios={len(audios)} framesz={len(frames[0]) if frames else 0}')
    elif cmd == 'extract':
        path, outdir = sys.argv[2], sys.argv[3]
        idxs = [int(x) for x in sys.argv[4].split(',')] if len(sys.argv) > 4 else None
        frames, _ = parse_avi(path)
        W = H = 480
        os.makedirs(outdir, exist_ok=True)
        for i, fr in enumerate(frames):
            if idxs is not None and i not in idxs:
                continue
            rows = frame_to_rows(fr, W, H)
            write_png(os.path.join(outdir, f'frame_{i:02d}.png'), rows, W, H)
        print(f'extracted {len(frames) if idxs is None else len(idxs)} frames to {outdir}')
    elif cmd == 'diffprofile':
        path = sys.argv[2]
        frames, _ = parse_avi(path)
        W = H = 480
        raws = [frame_to_rows(f, W, H) for f in frames]
        flats = [b''.join(r) for r in raws]
        diffs = [mean_abs_diff(flats[i], flats[i+1]) for i in range(len(flats)-1)]
        print('per-frame mean abs diff (i -> i+1):')
        for i, d in enumerate(diffs):
            print(f'  {i:02d}->{i+1:02d}: {d:.2f}')
        print(f'min={min(diffs):.2f} mean={sum(diffs)/len(diffs):.2f} max={max(diffs):.2f}')
        print(f'opening (0->1..4->5): {[f"{d:.2f}" for d in diffs[:5]]}')
