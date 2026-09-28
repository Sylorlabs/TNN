#!/usr/bin/env python3
# analyze.py — error-map + pentagon-crop analysis for the adaptive-split fork.
# Reads 24-bit BMPs directly. Writes PNGs (via zlib, no PIL) into outdir.
import struct, zlib, math, os, sys

def read_bmp(path):
    d = open(path, 'rb').read()
    assert d[0:2] == b'BM', path
    off = struct.unpack('<I', d[10:14])[0]
    w = struct.unpack('<i', d[18:22])[0]
    h = struct.unpack('<i', d[22:26])[0]
    stride = (w * 3 + 3) // 4 * 4
    img = bytearray(w * h * 3)
    for y in range(h):
        src = h - 1 - y
        for x in range(w):
            q = off + src * stride + x * 3
            p = (y * w + x) * 3
            img[p] = d[q + 2]; img[p + 1] = d[q + 1]; img[p + 2] = d[q]
    return img, w, h

def write_png(path, rgb, w, h):
    raw = b''.join(b'\x00' + bytes(rgb[y * w * 3:(y + 1) * w * 3]) for y in range(h))
    def chunk(t, c):
        return struct.pack('>I', len(c)) + t + c + struct.pack('>I', zlib.crc32(t + c) & 0xffffffff)
    png = (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0))
           + chunk(b'IDAT', zlib.compress(raw)) + chunk(b'IEND', b''))
    open(path, 'wb').write(png)

def crop(rgb, w, h, x0, y0, cw, chh):
    out = bytearray(cw * chh * 3)
    for y in range(chh):
        for x in range(cw):
            sx, sy = x0 + x, y0 + y
            if 0 <= sx < w and 0 <= sy < h:
                q = (sy * w + sx) * 3
                p = (y * cw + x) * 3
                out[p:p + 3] = rgb[q:q + 3]
    return out

def upscale_nn(rgb, w, h, k):
    out = bytearray(w * k * h * k * 3)
    for y in range(h):
        for x in range(w):
            q = (y * w + x) * 3
            px = rgb[q:q + 3]
            for dy in range(k):
                for dx in range(k):
                    p = ((y * k + dy) * w * k + (x * k + dx)) * 3
                    out[p:p + 3] = px
    return out, w * k, h * k

def main():
    orig_p, adap_p, rigid_p, zoom_p, outdir = sys.argv[1:6]
    kmap_p = sys.argv[6] if len(sys.argv) > 6 else None
    os.makedirs(outdir, exist_ok=True)
    orig, w, h = read_bmp(orig_p)
    adap, _, _ = read_bmp(adap_p)
    rigid, _, _ = read_bmp(rigid_p)
    zoom, _, _ = read_bmp(zoom_p)
    n = w * h
    # per-pixel mean abs error maps
    err_ad = bytearray(n * 3)
    err_rg = bytearray(n * 3)
    band_err = [0.0] * 8  # 8 horizontal bands, adaptive
    band_err_r = [0.0] * 8
    band_n = [0] * 8
    tot_ad = 0.0
    tot_rg = 0.0
    for i in range(n):
        p = i * 3
        ea = (abs(orig[p] - adap[p]) + abs(orig[p + 1] - adap[p + 1]) + abs(orig[p + 2] - adap[p + 2])) / 3.0
        er = (abs(orig[p] - rigid[p]) + abs(orig[p + 1] - rigid[p + 1]) + abs(orig[p + 2] - rigid[p + 2])) / 3.0
        tot_ad += ea
        tot_rg += er
        v = min(255, int(ea * 6))
        err_ad[p] = v; err_ad[p + 1] = v; err_ad[p + 2] = v
        v2 = min(255, int(er * 6))
        err_rg[p] = v2; err_rg[p + 1] = v2; err_rg[p + 2] = v2
        b = min(7, (i // w) * 8 // h)
        band_err[b] += ea
        band_err_r[b] += er
        band_n[b] += 1
    write_png(f"{outdir}/errmap_adaptive.png", err_ad, w, h)
    write_png(f"{outdir}/errmap_rigid.png", err_rg, w, h)
    print(f"mean abs err: adaptive={tot_ad / n:.3f} rigid={tot_rg / n:.3f}")
    print("band: y-range        adaptive_share  rigid_share")
    for b in range(8):
        y0, y1 = b * h // 8, (b + 1) * h // 8
        sa = band_err[b] / tot_ad * 100
        sr = band_err_r[b] / tot_rg * 100
        print(f"  y {y0:3d}..{y1:3d}:        {sa:5.1f}%        {sr:5.1f}%")
    # pentagon verification: bridge-arch crop at 10x
    # Pont Vieux arches, left-center: x 90..170, y 60..110
    ax0, ay0, acw, ach = 90, 60, 80, 50
    for name, img in (("original", orig), ("adaptive", adap), ("rigid", rigid), ("zoom", zoom)):
        c = crop(img, w, h, ax0, ay0, acw, ach)
        u, uw, uh = upscale_nn(c, acw, ach, 10)
        write_png(f"{outdir}/arch10x_{name}.png", u, uw, uh)
    print("arch crops written (10x)")
    # white-box: boundary-vs-interior error (tile-boundary discontinuity check)
    if kmap_p:
        d = open(kmap_p, 'rb').read()
        assert d[0:8] == b'TNNKNLM1'
        o = 8
        w2 = struct.unpack('<Q', d[o:o + 8])[0]; o += 8
        h2 = struct.unpack('<Q', d[o:o + 8])[0]; o += 8
        assert (w2, h2) == (w, h)
        ns = struct.unpack('<Q', d[o:o + 8])[0]; o += 8
        for _ in range(ns):
            B = struct.unpack('<Q', d[o:o + 8])[0]; o += 8
            na = struct.unpack('<Q', d[o:o + 8])[0]; o += 8
            o += na * (B * B * 3 * 2 + 8)
        nreg = struct.unpack('<Q', d[o:o + 8])[0]; o += 8
        # boundary mask: pixel is on a tile edge if a neighbor belongs to another tile
        owner = [-1] * n
        regs = []
        for ri in range(nreg):
            x = struct.unpack('<H', d[o:o + 2])[0]; o += 2
            y = struct.unpack('<H', d[o:o + 2])[0]; o += 2
            s = d[o]; o += 1
            o += 2 + 3  # atom, r, g, b
            regs.append((x, y, s))
            for yy in range(y, min(h, y + s)):
                for xx in range(x, min(w, x + s)):
                    owner[yy * w + xx] = ri
        bnd_err = 0.0; bnd_n = 0
        int_err = 0.0; int_n = 0
        for y in range(h):
            for x in range(w):
                i = y * w + x
                p = i * 3
                ea = (abs(orig[p] - adap[p]) + abs(orig[p + 1] - adap[p + 1]) + abs(orig[p + 2] - adap[p + 2])) / 3.0
                is_bnd = False
                if x + 1 < w and owner[i] != owner[i + 1]:
                    is_bnd = True
                if y + 1 < h and owner[i] != owner[i + w]:
                    is_bnd = True
                if is_bnd:
                    bnd_err += ea; bnd_n += 1
                else:
                    int_err += ea; int_n += 1
        print(f"regions={nreg} boundary_px={bnd_n} ({100.0*bnd_n/n:.1f}%) "
              f"mean_abs_err: boundary={bnd_err/max(1,bnd_n):.3f} interior={int_err/max(1,int_n):.3f}")

if __name__ == '__main__':
    main()
