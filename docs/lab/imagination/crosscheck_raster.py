#!/usr/bin/env python3
"""HARNESS ONLY (verification, never generation): independently re-rasterize field
dumps with a from-spec Python reimplementation of the Zag rasterizers and
byte-compare against the Zag-emitted BMPs and AVI video frames.

Usage: python3 crosscheck_raster.py <field_bin> <bmp_dir> <dump_log>
Exit 0 iff every byte matches.
"""
import struct, subprocess, sys, math

BIN, BMPDIR, DUMPLOG = sys.argv[1], sys.argv[2], sys.argv[3]
W = H = 240

def truncdiv(a, b):
    return math.trunc(a / b)

# ---------- parse dumps ----------
def parse_dumps(path):
    scenes = {}
    cur_type = {}
    for line in open(path):
        p = line.split()
        if not p:
            continue
        if p[0] == 'F3H':
            sc = int(p[1]); t = int(p[2].split('=')[1])
            cur_type[sc] = t
            scenes[sc] = {'type': t, 'rows': {}}
        elif p[0] == 'F3G':
            sc = int(p[1]); row = int(p[2])
            scenes[sc]['rows'][row] = [int(x) for x in p[3:]]
    return scenes

def visual_cells(sc):
    rows = sc['rows']
    return [[ [rows[y][x*4+c] for c in range(3)] for x in range(24)] for y in range(24)]

def audio_energy(sc):
    rows = sc['rows']
    return [[rows[t][b*2] for b in range(48)] for t in range(48)]

def struct_h(sc):
    rows = sc['rows']
    return [[rows[y][x] for x in range(24)] for y in range(24)]

# ---------- reimplemented rasterizers (integer math mirroring field.zag) ----------
def raster_visual(cells):
    px = bytearray(W*H*3)
    for oy in range(H):
        gy = oy*23*256//(H-1); y0 = gy >> 8; ty = gy & 255; y1 = min(y0+1, 23)
        for ox in range(W):
            gx = ox*23*256//(W-1); x0 = gx >> 8; tx = gx & 255; x1 = min(x0+1, 23)
            for ch in range(3):
                c00 = cells[y0][x0][ch]; c10 = cells[y0][x1][ch]
                c01 = cells[y1][x0][ch]; c11 = cells[y1][x1][ch]
                v = (c00*(256-tx)*(256-ty) + c10*tx*(256-ty)
                     + c01*(256-tx)*ty + c11*tx*ty) >> 16
                px[(oy*W+ox)*3+ch] = max(0, min(255, v))
    return px

def heat(e, ch):
    e = max(0, min(1000, e))
    if ch == 0:
        if e <= 333: return e*60//333
        if e <= 666: return 60 + (e-333)*140//333
        return 200 + (e-666)*55//334
    if ch == 1:
        if e <= 333: return e*120//333
        if e <= 666: return 120 + (e-333)*100//333
        return 220 + (e-666)*35//334
    if e <= 333: return 80 + e*175//333
    if e <= 666: return 255 - (e-333)*120//333
    return 135 + (e-666)*120//334

def raster_spec(energy):
    px = bytearray(W*H*3)
    for oy in range(H):
        t = min(oy*48//H, 47)
        for ox in range(W):
            b = min(ox*48//W, 47)
            e = energy[t][b]
            for ch in range(3):
                px[(oy*W+ox)*3+ch] = max(0, min(255, heat(e, ch)))
    return px

def raster_relief(h):
    px = bytearray(W*H*3)
    for oy in range(H):
        gy = oy*23*256//(H-1); y0 = gy >> 8; ty = gy & 255; y1 = min(y0+1, 23)
        yu = max(y0-1, 0); yd = min(y0+1, 23)
        for ox in range(W):
            gx = ox*23*256//(W-1); x0 = gx >> 8; tx = gx & 255; x1 = min(x0+1, 23)
            h00 = h[y0][x0]; h10 = h[y0][x1]; h01 = h[y1][x0]; h11 = h[y1][x1]
            hv = (h00*(256-tx)*(256-ty) + h10*tx*(256-ty)
                  + h01*(256-tx)*ty + h11*tx*ty) >> 16
            xl = max(x0-1, 0); xr = min(x0+1, 23)
            dx = h[y0][xl]-h[y0][xr]; dy = h[yu][x0]-h[yd][x0]
            lum = 60 + hv*150//1000 + truncdiv(dx+dy, 6)
            g = max(0, min(255, lum))
            px[(oy*W+ox)*3] = g; px[(oy*W+ox)*3+1] = g; px[(oy*W+ox)*3+2] = g
    return px

def assemble_bmp(px):
    rowbytes = W*3; imgsz = rowbytes*H
    hdr = bytearray(54)
    hdr[0:2] = b'BM'
    struct.pack_into('<I', hdr, 2, 54+imgsz)
    struct.pack_into('<I', hdr, 10, 54)
    struct.pack_into('<I', hdr, 14, 40)
    struct.pack_into('<i', hdr, 18, W)
    struct.pack_into('<i', hdr, 22, H)
    struct.pack_into('<H', hdr, 26, 1)
    struct.pack_into('<H', hdr, 28, 24)
    struct.pack_into('<I', hdr, 34, imgsz)
    body = bytearray(imgsz)
    for r in range(H):
        srow = r*rowbytes; drow = (H-1-r)*rowbytes
        for c in range(W):
            body[drow+c*3] = px[srow+c*3+2]
            body[drow+c*3+1] = px[srow+c*3+1]
            body[drow+c*3+2] = px[srow+c*3]
    return bytes(hdr) + bytes(body)

def main():
    scenes = parse_dumps(DUMPLOG)
    # scene number -> bmp index: briefs 1..6 -> 0..5, novels 11..18 -> 6..13
    names = ['f3b1','f3b2','f3b3','f3b4','f3b5','f3b6',
             'f3n11','f3n12','f3n13','f3n14','f3n15','f3n16','f3n17','f3n18']
    scnums = [1,2,3,4,5,6,11,12,13,14,15,16,17,18]
    fails = 0
    for name, sc in zip(names, scnums):
        s = scenes[sc]
        t = s['type']
        if t == 1: px = raster_visual(visual_cells(s))
        elif t == 2: px = raster_spec(audio_energy(s))
        else: px = raster_relief(struct_h(s))
        expect = assemble_bmp(px)
        got = open(f'{BMPDIR}/{name}.bmp','rb').read()
        if got == expect:
            print(f'{name}.bmp MATCH ({len(got)} bytes)')
        else:
            fails += 1
            print(f'{name}.bmp MISMATCH: got {len(got)} expect {len(expect)}')
            for i,(a,b) in enumerate(zip(got, expect)):
                if a != b:
                    print(f'  first diff at byte {i}: got {a} expect {b}')
                    break
    # AVI video frames: re-derive from keyframe dumps (scenes 110..113, 120..123)
    for v, base in ((1,110),(2,120)):
        kf = [visual_cells(scenes[base+k]) for k in range(4)]
        d = open(f'{BMPDIR}/f3vid{v}.avi','rb').read()
        m = d.find(b'movi')+4; o = m; frames = []
        while len(frames) < 24:
            cid = d[o:o+4]; sz = struct.unpack('<I', d[o+4:o+8])[0]
            if cid == b'00dc': frames.append(d[o+8:o+8+sz])
            o += 8+sz
        ok = True
        for fr in range(24):
            a = min(fr//8, 2); t8 = fr - a*8
            A, B = kf[a], kf[a+1]
            interp = [[[A[y][x][c] + truncdiv((B[y][x][c]-A[y][x][c])*t8, 8)
                        for c in range(3)] for x in range(24)] for y in range(24)]
            px = raster_visual(interp)
            # AVI chunk is bottom-up BGR
            exp = bytearray(172800)
            for r in range(H):
                srow = (H-1-r)*W*3
                for c in range(W):
                    exp[r*W*3+c*3] = px[srow+c*3+2]
                    exp[r*W*3+c*3+1] = px[srow+c*3+1]
                    exp[r*W*3+c*3+2] = px[srow+c*3]
            if bytes(exp) != frames[fr]:
                ok = False; print(f'  vid{v} frame {fr} MISMATCH'); break
        print(f'f3vid{v}.avi frames', 'ALL MATCH' if ok else 'MISMATCH')
        fails += 0 if ok else 1
    print('CROSSCHECK', 'PASS' if fails == 0 else 'FAIL')
    return 1 if fails else 0

sys.exit(main())
