#!/usr/bin/env python3
# gen_pert.py — build adversarial wire perturbations for C5 (S0 baseline).
# All perturbations preserve file framing (same lengths); only targeted
# fields change. FNV-1a-64 checksum recomputed only where stated.
#
#   P-a: session_id +1 on EVERY wire, checksum recomputed
#        -> session_id must not leak into deliberation: decisions identical.
#   P-b: wire seq 3: teacher_id = 0, checksum recomputed
#        -> ingress must reject with rc=3 (P_V_BAD_TEACHER) for that seq only.
#   P-c: wire seq 5: flip one checksum byte, no recompute
#        -> ingress must reject with rc=7 (P_V_CHECKSUM) for that seq only.
#   P-d: wire seq 7: zero the magic, checksum left as-is
#        -> ingress must reject with rc=1 (P_V_BAD_MAGIC) for that seq only.
import struct, sys, os

FNV_BASIS = 14695981039346656037
FNV_PRIME = 1099511628211
MASK = (1 << 64) - 1

def fnv(data: bytes) -> int:
    h = FNV_BASIS
    for b in data:
        h = ((h ^ b) * FNV_PRIME) & MASK
    return h

def parse_wires(data: bytes):
    offs = []
    off = 0
    while off + 54 <= len(data):
        if data[off:off+4] != b'PRPT':  # 0x54505250 little-endian on the wire
            raise ValueError(f"bad magic at {off}")
        aux = data[off+43]
        gc = data[off+44+aux*16]
        total = 54 + (aux+gc)*16
        seq = struct.unpack_from('<Q', data, off+18)[0]
        offs.append((off, total, seq))
        off += total
    return offs

def main():
    c5 = sys.argv[1]
    src = os.path.join(c5, 'wires_S0.bin')
    data = bytearray(open(src, 'rb').read())
    wires = parse_wires(bytes(data))

    # P-a: session_id +1 everywhere, checksum recomputed
    # Frozen §B.3: session_id u64 @10 (seq u64 @18 — do NOT touch).
    pa = bytearray(data)
    for off, total, seq in wires:
        sid = struct.unpack_from('<Q', pa, off+10)[0]
        struct.pack_into('<Q', pa, off+10, (sid + 1) & MASK)
        c = fnv(bytes(pa[off:off+total-8]))
        struct.pack_into('<Q', pa, off+total-8, c)
    open(os.path.join(c5, 'wires_S0_Pa.bin'), 'wb').write(pa)

    # P-b: seq 3 -> teacher_id 0, checksum recomputed
    pb = bytearray(data)
    for off, total, seq in wires:
        if seq == 3:
            struct.pack_into('<I', pb, off+6, 0)
            c = fnv(bytes(pb[off:off+total-8]))
            struct.pack_into('<Q', pb, off+total-8, c)
    open(os.path.join(c5, 'wires_S0_Pb.bin'), 'wb').write(pb)

    # P-c: seq 5 -> flip a checksum byte, no recompute
    pc = bytearray(data)
    for off, total, seq in wires:
        if seq == 5:
            pc[off+total-1] ^= 0xFF
    open(os.path.join(c5, 'wires_S0_Pc.bin'), 'wb').write(pc)

    # P-d: seq 7 -> zero magic, checksum untouched (magic check fires first)
    pd = bytearray(data)
    for off, total, seq in wires:
        if seq == 7:
            pd[off:off+4] = b'\x00\x00\x00\x00'
    open(os.path.join(c5, 'wires_S0_Pd.bin'), 'wb').write(pd)

    print(f"parsed {len(wires)} wires; wrote P-a..P-d")

if __name__ == '__main__':
    main()
