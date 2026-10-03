#!/usr/bin/env python3
"""Flip mixed_block_flag 0->1 on all short-block (block_type=2) granules.
MPEG-1 Layer III side-info bit parser. Deterministic, no RNG.
Usage: flip_mixed.py in.mp3 out.mp3
"""
import sys

class BitW:
    def __init__(self, data):
        self.d = bytearray(data)
    def get(self, pos, n):
        v = 0
        for i in range(n):
            b = self.d[(pos + i) // 8]
            v = (v << 1) | ((b >> (7 - ((pos + i) % 8))) & 1)
        return v
    def set(self, pos, n, v):
        for i in range(n):
            bit = (v >> (n - 1 - i)) & 1
            idx = (pos + i) // 8
            sh = 7 - ((pos + i) % 8)
            if bit:
                self.d[idx] |= (1 << sh)
            else:
                self.d[idx] &= ~(1 << sh)

BR = {1:32,2:40,3:48,4:56,5:64,6:80,7:96,8:112,9:128,10:160,11:192,12:224,13:256,14:320}
SR = {0:44100,1:48000,2:32000}

def main():
    src, dst = sys.argv[1], sys.argv[2]
    data = bytearray(open(src,'rb').read())
    bw = BitW(data)
    # skip ID3 if present
    off = 0
    if data[0:3] == b'ID3':
        sz = 0
        for b in data[6:10]:
            sz = (sz << 7) | (b & 0x7F)
        off = 10 + sz
    nflip = 0
    nshort = 0
    frame = 0
    while off + 4 < len(data):
        if not (data[off] == 0xFF and (data[off+1] & 0xE0) == 0xE0):
            off += 1
            continue
        h1,h2,h3 = data[off+1], data[off+2], data[off+3]
        # require MPEG-1 Layer III
        if ((h1>>3)&3) != 3 or ((h1>>1)&3) != 1:
            off += 1
            continue
        br_i, sr_i, pad = (h2>>4)&15, (h2>>2)&3, (h2>>1)&1
        if br_i in (0,15) or sr_i == 3:
            off += 1
            continue
        mono = 1 if (h3 & 0xC0) == 0xC0 else 0
        flen = (144*BR[br_i]*1000)//SR[sr_i] + pad
        # side info starts at off+4 (byte), bit pos
        # NB: oracle reads 9 (main_data_begin) + (7+gr_count) bits before granules
        # (empirically exact: 17-byte mono side info aligns); do NOT use 3+4.
        pos = (off+4)*8
        pos += 9  # main_data_begin
        nch = 1 if mono else 2
        pos += 7 + 2*nch  # private_bits+scfsi combined (oracle layout)
        for gr in range(2):
            for ch in range(nch):
                pos += 12+9+8+4  # part23, big_values, global_gain, scf_compress
                ws = bw.get(pos,1); pos += 1
                if ws:
                    bt = bw.get(pos,2); pos += 2
                    if bt == 2:
                        nshort += 1
                        # mixed_block_flag is the next bit
                        if bw.get(pos,1) == 0:
                            bw.set(pos,1,1)
                            nflip += 1
                    pos += 1  # mixed_block_flag
                    pos += 5+5+3+3+3  # table_select x2, subblock_gain x3
                else:
                    pos += 5+5+5+4+3
                pos += 1+1+1  # preflag, scalefac_scale, count1
        off += flen
        frame += 1
    open(dst,'wb').write(bytes(bw.d))
    print(f'frames={frame} short_granules={nshort} mixed_flipped={nflip} -> {dst}')

main()
