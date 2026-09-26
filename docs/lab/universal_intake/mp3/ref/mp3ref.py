#!/usr/bin/env python3
"""Independent Python reference for MP3 Layer III (MPEG-1, 44.1 kHz).
Faithful port of the public-domain dr_mp3/minimp3 Layer III core to
Python/numpy float64. B1/B2/B3 oracle for the pure-Zag decoder.

Usage: mp3ref.py <mp3> <outdir>
Writes: sideinfo.json, b1_deq.npy, b1_symbols.json, b1_scf.json, b2.npy, b3.npy, b4.s16
"""
import sys, os, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(os.path.join(HERE, 'mp3_tables.json')))
G_SCF_LONG = T['g_scf_long']
G_SCF_SHORT = T['g_scf_short']
G_SCF_MIXED_ROWS = T['g_scf_mixed_rows']
G_SCF_PARTITIONS = T['g_scf_partitions']
G_SCFC_DECODE = T['g_scfc_decode']
G_PREAMP = T['g_preamp']
G_EXPFRAC = np.array(T['g_expfrac'], dtype=np.float64)
G_POW43 = np.array(T['g_pow43'], dtype=np.float64)
TABS = np.array(T['tabs'], dtype=np.int16)
TABINDEX = T['tabindex']
TAB32 = np.array(T['tab32'], dtype=np.uint8)
TAB33 = np.array(T['tab33'], dtype=np.uint8)
G_LINBITS = T['g_linbits']
G_AA = np.array(T['g_aa'], dtype=np.float64).reshape(2, 8)
G_TWID9 = np.array(T['g_twid9'], dtype=np.float64)
G_TWID3 = np.array(T['g_twid3'], dtype=np.float64)
G_MDCT_WINDOW = np.array(T['g_mdct_window'], dtype=np.float64).reshape(2, 18)
G_SEC = np.array(T['g_sec'], dtype=np.float64)
G_WIN = np.array(T['g_win'], dtype=np.float64)
G_PAN = np.array(T['g_pan'], dtype=np.float64)

BITRATE_TAB = [0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320]
SR_TAB = [44100, 48000, 32000]
MAX_BITRESERVOIR_BYTES = 512
MAX_SCFI = 44


def ldexp_q2(y, exp_q2):
    y = float(y)
    while True:
        e = min(30 * 4, exp_q2)
        y = y * (G_EXPFRAC[e & 3] * (1 << 30 >> (e >> 2)))
        exp_q2 -= e
        if exp_q2 <= 0:
            break
    return y


def pow_43(x):
    if x < 129:
        return G_POW43[16 + x]
    mult = 256
    if x < 1024:
        mult = 16
        x <<= 3
    sign = (2 * x) & 64
    frac = ((x & 63) - sign) / ((x & ~63) + sign)
    return G_POW43[16 + ((x + sign) >> 6)] * (1.0 + frac * ((4.0 / 3) + frac * (2.0 / 9))) * mult


class BS:
    def __init__(self, buf, pos_bits=0):
        self.buf = buf
        self.pos = pos_bits
        self.limit = len(buf) * 8

    def get_bits(self, n):
        p = self.pos >> 3
        s = self.pos & 7
        self.pos += n
        if self.pos > self.limit:
            return 0
        shl = n + s
        nxt = self.buf[p] & (255 >> s)
        p += 1
        cache = 0
        while True:
            shl -= 8
            if shl <= 0:
                break
            cache |= nxt << shl
            nxt = self.buf[p] if p < len(self.buf) else 0
            p += 1
        return cache | (nxt >> (-shl))


class HuffReader:
    def __init__(self, buf, pos):
        self.buf = buf
        self.next_ptr = (pos >> 3) + 4
        b = bytes(buf[(pos >> 3):(pos >> 3) + 4])
        b = b + b'\x00' * (4 - len(b))
        self.cache = (((b[0] * 256 + b[1]) * 256 + b[2]) * 256 + b[3])
        self.cache = (self.cache << (pos & 7)) & 0xFFFFFFFF
        self.sh = (pos & 7) - 8

    def peek(self, n):
        return (self.cache >> (32 - n)) & ((1 << n) - 1)

    def flush(self, n):
        self.cache = (self.cache << n) & 0xFFFFFFFF
        self.sh += n

    def check(self):
        while self.sh >= 0:
            byte = self.buf[self.next_ptr] if self.next_ptr < len(self.buf) else 0
            self.next_ptr += 1
            self.cache = (self.cache | ((byte << self.sh) & 0xFFFFFFFF)) & 0xFFFFFFFF
            self.sh -= 8

    def bspos(self):
        return self.next_ptr * 8 - 24 + self.sh


def read_side_info(bs, hdr):
    mono = (hdr[3] & 0xC0) == 0xC0
    sr = (hdr[2] >> 2) & 0x03
    my_sr = sr + (((hdr[1] >> 3) & 1) + ((hdr[1] >> 4) & 1)) * 3
    sr_idx = my_sr - (1 if my_sr != 0 else 0)
    gr_count = (1 if mono else 2) * 2
    main_data_begin = bs.get_bits(9)
    scfsi = bs.get_bits(7 + gr_count)
    gr_info = []
    part23sum = 0
    gc = gr_count
    while gc > 0:
        if mono:
            scfsi <<= 4
        gi = {}
        gi['part_23_length'] = bs.get_bits(12); part23sum += gi['part_23_length']
        gi['big_values'] = bs.get_bits(9)
        if gi['big_values'] > 288:
            raise ValueError('big_values > 288')
        gi['global_gain'] = bs.get_bits(8)
        gi['scalefac_compress'] = bs.get_bits(4)
        gi['sfbtab'] = G_SCF_LONG[sr_idx * 23:(sr_idx + 1) * 23]
        gi['n_long_sfb'] = 22; gi['n_short_sfb'] = 0
        gi['block_type'] = 0; gi['mixed_block_flag'] = 0
        gi['subblock_gain'] = [0, 0, 0]
        if bs.get_bits(1):
            gi['block_type'] = bs.get_bits(2)
            if gi['block_type'] == 0:
                raise ValueError('block_type 0')
            gi['mixed_block_flag'] = bs.get_bits(1)
            gi['region_count'] = [7, 255, 255]
            if gi['block_type'] == 2:
                scfsi &= 0x0F0F
                if not gi['mixed_block_flag']:
                    gi['region_count'][0] = 8
                    gi['sfbtab'] = G_SCF_SHORT[sr_idx * 40:(sr_idx + 1) * 40]
                    gi['n_long_sfb'] = 0; gi['n_short_sfb'] = 39
                else:
                    gi['sfbtab'] = G_SCF_MIXED_ROWS[sr_idx]
                    gi['n_long_sfb'] = 8; gi['n_short_sfb'] = 30
            tables = bs.get_bits(10) << 5
            gi['subblock_gain'] = [bs.get_bits(3), bs.get_bits(3), bs.get_bits(3)]
        else:
            tables = bs.get_bits(15)
            gi['region_count'] = [bs.get_bits(4), bs.get_bits(3), 255]
        gi['table_select'] = [(tables >> 10) & 31, (tables >> 5) & 31, tables & 31]
        gi['preflag'] = bs.get_bits(1)
        gi['scalefac_scale'] = bs.get_bits(1)
        gi['count1_table'] = bs.get_bits(1)
        gi['scfsi'] = (scfsi >> 12) & 15
        scfsi <<= 4
        gr_info.append(gi)
        gc -= 1
    if part23sum + bs.pos > bs.limit + main_data_begin * 8:
        raise ValueError('part23 overrun')
    return gr_info, main_data_begin, sr_idx


def decode_scalefactors(hdr, ist_pos, bs, gr):
    n_long = gr['n_long_sfb']; n_short = gr['n_short_sfb']
    idx = (1 if n_short else 0) + (0 if n_long else 1)
    scf_partition = G_SCF_PARTITIONS[idx * 28:(idx + 1) * 28]
    part = G_SCFC_DECODE[gr['scalefac_compress']]
    scf_size = [(part >> 2) & 0xFF, (part >> 2) & 0xFF, part & 3, part & 3]
    scfsi = gr['scfsi']
    iscf = [0] * 40
    ip = 0; sp = 0
    for i in range(4):
        cnt = scf_partition[i]
        if not cnt:
            break
        if scfsi & 8:
            for k in range(cnt):
                iscf[sp + k] = ist_pos[ip + k]
        else:
            bits = scf_size[i]
            if not bits:
                for k in range(cnt):
                    iscf[sp + k] = 0
                    ist_pos[ip + k] = 0
            else:
                max_scf = (1 << bits) - 1 if scfsi < 0 else -1
                for k in range(cnt):
                    s = bs.get_bits(bits)
                    ist_pos[ip + k] = -1 if s == max_scf else s
                    iscf[sp + k] = s
        ip += cnt; sp += cnt
        scfsi *= 2
    if n_short:
        sh = 3 - (gr['scalefac_scale'] + 1)
        for i in range(0, n_short, 3):
            iscf[n_long + i + 0] += gr['subblock_gain'][0] << sh
            iscf[n_long + i + 1] += gr['subblock_gain'][1] << sh
            iscf[n_long + i + 2] += gr['subblock_gain'][2] << sh
    elif gr['preflag']:
        for i in range(10):
            iscf[11 + i] += G_PREAMP[i]
    scf_shift = gr['scalefac_scale'] + 1
    is_ms = (hdr[3] & 0xE0) == 0x60
    gain_exp = gr['global_gain'] - 4 - 210 - (2 if is_ms else 0)
    gain = ldexp_q2(1 << (MAX_SCFI // 4), MAX_SCFI - gain_exp)
    scf = [ldexp_q2(gain, iscf[i] << scf_shift) for i in range(n_long + n_short)]
    return scf, iscf


def huffman(dst, hr, gr, scf, layer3gr_limit, symbols):
    sfb = list(gr['sfbtab'])
    sfb_i = 0; scf_i = 0
    big_val_cnt = gr['big_values']
    one = 0.0
    ireg = 0; di = 0
    while big_val_cnt > 0:
        tab_num = gr['table_select'][ireg]
        sfb_cnt = gr['region_count'][ireg]
        ireg += 1
        codebook = TABS[TABINDEX[tab_num]:]
        linbits = G_LINBITS[tab_num]
        while True:
            npairs = sfb[sfb_i] // 2; sfb_i += 1
            pairs_to_decode = min(big_val_cnt, npairs)
            one = scf[scf_i]; scf_i += 1
            for _ in range(pairs_to_decode):
                w = 5
                leaf = int(codebook[hr.peek(w)])
                while leaf < 0:
                    hr.flush(w)
                    w = leaf & 7
                    leaf = int(codebook[hr.peek(w) - (leaf >> 3)])
                hr.flush(leaf >> 8)
                for j in range(2):
                    lsb = leaf & 0x0F
                    orig_lsb = lsb
                    if linbits and lsb == 15:
                        lsb += hr.peek(linbits)
                        hr.flush(linbits)
                        hr.check()
                        sign = -1.0 if (hr.cache & 0x80000000) else 1.0
                        dst[di] = one * pow_43(lsb) * sign
                        symbols.append([int(lsb), int(sign)])
                    else:
                        sbit = (hr.cache >> 31) & 1
                        dst[di] = G_POW43[16 + lsb - 16 * sbit] * one
                        symbols.append([int(lsb) if sbit == 0 else -int(lsb)])
                    hr.flush(1 if orig_lsb != 0 else 0)
                    leaf >>= 4
                    di += 1
                hr.check()
            big_val_cnt -= npairs
            sfb_cnt -= 1
            if not (big_val_cnt > 0 and sfb_cnt >= 0):
                break
    cb = TAB33 if gr['count1_table'] else TAB32
    np_ = 1 - big_val_cnt
    while True:
        leaf = int(cb[hr.peek(4)])
        if not (leaf & 8):
            leaf = int(cb[(leaf >> 3) + (((hr.cache << 4) & 0xFFFFFFFF) >> (32 - (leaf & 3)))])
        hr.flush(leaf & 7)
        if hr.bspos() > layer3gr_limit:
            break
        for half in range(2):
            np_ -= 1
            if np_ == 0:
                np_ = sfb[sfb_i] // 2; sfb_i += 1
                if np_ == 0:
                    hr.check()
                    return
                one = scf[scf_i]; scf_i += 1
            for s in range(2):
                idx_s = half * 2 + s
                if leaf & (128 >> idx_s):
                    sign = -1.0 if (hr.cache & 0x80000000) else 1.0
                    dst[di + idx_s] = sign * one
                    symbols.append(['c1', idx_s, int(sign)])
                    hr.flush(1)
                else:
                    dst[di + idx_s] = 0.0
        di += 4
        hr.check()


def midside_stereo(stacked, n):
    left = stacked[:n]; right = stacked[576:576 + n]
    a = left.copy(); b = right.copy()
    stacked[:n] = a + b
    stacked[576:576 + n] = a - b


def stereo_top_band(right, sfb, nbands):
    max_band = [-1, -1, -1]
    off = 0
    for i in range(nbands):
        ln = sfb[i]
        for k in range(0, ln, 2):
            if right[off + k] != 0 or right[off + k + 1] != 0:
                max_band[i % 3] = i
                break
        off += ln
    return max_band


def intensity_stereo(stacked, ist_pos, gr, hdr):
    # gr: gr_info[ch0] of this granule; gr[1] is ch1
    n_sfb = gr['n_long_sfb'] + gr['n_short_sfb']
    max_blocks = 3 if gr['n_short_sfb'] else 1
    right = stacked[576:576 + 576]
    max_band = stereo_top_band(right, gr['sfbtab'], n_sfb)
    if gr['n_long_sfb']:
        m = max(max_band)
        max_band = [m, m, m]
    default_pos = 3  # MPEG-1
    for i in range(max_blocks):
        itop = n_sfb - max_blocks + i
        prev = itop - max_blocks
        ist_pos[itop] = default_pos if max_band[i] >= prev else ist_pos[prev]
    # stereo_process
    sfb = gr['sfbtab']
    is_ms = (hdr[3] & 0xE0) == 0x60
    max_pos = 7
    off = 0
    i = 0
    while sfb[i]:
        ipos = ist_pos[i]
        ln = sfb[i]
        if i > max_band[i % 3] and ipos < max_pos:
            s = 1.41421356 if is_ms else 1.0
            kl = G_PAN[2 * ipos] * s
            kr = G_PAN[2 * ipos + 1] * s
            l = stacked[off:off + ln].copy()
            stacked[576 + off:576 + off + ln] = l * kr
            stacked[off:off + ln] = l * kl
        elif is_ms:
            l = stacked[off:off + ln].copy()
            r = stacked[576 + off:576 + off + ln].copy()
            stacked[off:off + ln] = l + r
            stacked[576 + off:576 + off + ln] = l - r
        off += ln
        i += 1


def reorder(grbuf, n_long_bands, sfbtab, n_long_sfb):
    # drmp3_L3_reorder with scratch
    src = grbuf[n_long_bands * 18:].copy()
    dst = np.zeros_like(src)
    sfb = sfbtab[n_long_sfb:]
    si = 0; sp = 0; dp = 0
    while True:
        ln = sfb[si]
        if ln == 0:
            break
        for i in range(ln):
            dst[dp] = src[sp + i]
            dst[dp + 1] = src[sp + i + ln]
            dst[dp + 2] = src[sp + i + 2 * ln]
            dp += 3
        sp += 3 * ln
        si += 3
    grbuf[n_long_bands * 18:n_long_bands * 18 + dp] = dst[:dp]


def antialias(grbuf, nbands):
    g = grbuf
    for b in range(nbands):
        base = b * 18
        for i in range(8):
            u = g[base + 18 + i]
            d = g[base + 17 - i]
            g[base + 18 + i] = u * G_AA[0, i] - d * G_AA[1, i]
            g[base + 17 - i] = u * G_AA[1, i] + d * G_AA[0, i]


def dct3_9(y):
    y = y.copy()
    s0, s2, s4, s6, s8 = y[0], y[2], y[4], y[6], y[8]
    t0 = s0 + s6 * 0.5
    s0 -= s6
    t4 = (s4 + s2) * 0.93969262
    t2 = (s8 + s2) * 0.76604444
    s6 = (s4 - s8) * 0.17364818
    s4 += s8 - s2
    s2 = s0 - s4 * 0.5
    y[4] = s4 + s0
    s8 = t0 - t2 + s6
    s0 = t0 - t4 + t2
    s4 = t0 + t4 - s6
    s1, s3, s5, s7 = y[1], y[3], y[5], y[7]
    s3 *= 0.86602540
    t0 = (s5 + s1) * 0.98480775
    t4 = (s5 - s7) * 0.34202014
    t2 = (s1 + s7) * 0.64278761
    s1 = (s1 - s5 - s7) * 0.86602540
    s5 = t0 - s3 - t2
    s7 = t4 - s3 - t0
    s3 = t4 + s3 - t2
    y[0] = s4 - s7
    y[1] = s2 + s1
    y[2] = s0 - s3
    y[3] = s8 + s5
    y[5] = s8 - s5
    y[6] = s0 + s3
    y[7] = s2 - s1
    y[8] = s4 + s7
    return y


def imdct36(grbuf, overlap, window, nbands):
    for j in range(nbands):
        gb = j * 18; ob = j * 9
        co = np.zeros(9); si = np.zeros(9)
        co[0] = -grbuf[gb]
        si[0] = grbuf[gb + 17]
        for i in range(4):
            si[8 - 2 * i] = grbuf[gb + 4 * i + 1] - grbuf[gb + 4 * i + 2]
            co[1 + 2 * i] = grbuf[gb + 4 * i + 1] + grbuf[gb + 4 * i + 2]
            si[7 - 2 * i] = grbuf[gb + 4 * i + 4] - grbuf[gb + 4 * i + 3]
            co[2 + 2 * i] = -(grbuf[gb + 4 * i + 3] + grbuf[gb + 4 * i + 4])
        co = dct3_9(co); si = dct3_9(si)
        si[1] = -si[1]; si[3] = -si[3]; si[5] = -si[5]; si[7] = -si[7]
        for i in range(9):
            ovl = overlap[ob + i]
            sm = co[i] * G_TWID9[9 + i] + si[i] * G_TWID9[i]
            overlap[ob + i] = co[i] * G_TWID9[i] - si[i] * G_TWID9[9 + i]
            grbuf[gb + i] = ovl * window[i] - sm * window[9 + i]
            grbuf[gb + 17 - i] = ovl * window[9 + i] + sm * window[i]


def idct3(x0, x1, x2):
    m1 = x1 * 0.86602540
    a1 = x0 - x2 * 0.5
    return np.array([a1 + m1, x0 + x2, a1 - m1])


def imdct12(x, dst, overlap):
    co = idct3(-x[0], x[6] + x[3], x[12] + x[9])
    si = idct3(x[15], x[12] - x[9], x[6] - x[3])
    si[1] = -si[1]
    for i in range(3):
        ovl = overlap[i]
        sm = co[i] * G_TWID3[3 + i] + si[i] * G_TWID3[i]
        overlap[i] = co[i] * G_TWID3[i] - si[i] * G_TWID3[3 + i]
        dst[i] = ovl * G_TWID3[2 - i] - sm * G_TWID3[5 - i]
        dst[5 - i] = ovl * G_TWID3[5 - i] + sm * G_TWID3[2 - i]


def imdct_short(grbuf, overlap, nbands):
    for b in range(nbands):
        gb = b * 18; ob = b * 9
        tmp = grbuf[gb:gb + 18].copy()
        ov = overlap[ob:ob + 9].copy()
        grbuf[gb:gb + 6] = ov[:6]
        imdct12(tmp, grbuf[gb + 6:gb + 12], ov[6:9])
        imdct12(tmp[1:], grbuf[gb + 12:gb + 18], ov[6:9])
        imdct12(tmp[2:], grbuf[gb:gb + 6], ov[6:9])
        overlap[ob:ob + 6] = grbuf[gb:gb + 6]  # careful: imdct12 wrote into grbuf; fix below
    # NOTE: imdct12(dst=grbuf slice) writes dst AND overlap; replicate C pointer semantics:
    # C: imdct12(tmp, grbuf+gb+6, overlap+ob+6); imdct12(tmp+1, grbuf+gb+12, overlap+ob+6);
    #    imdct12(tmp+2, overlap+ob, overlap+ob+6);
    # So third call writes dst=overlap[ob:ob+6]. Redo correctly:


def imdct_short2(grbuf, overlap, nbands):
    for b in range(nbands):
        gb = b * 18; ob = b * 9
        tmp = grbuf[gb:gb + 18].copy()
        ov = overlap[ob:ob + 9]
        dst1 = np.zeros(6); dst2 = np.zeros(6); dst3 = np.zeros(6)
        ov76 = ov[6:9].copy()
        imdct12(tmp, dst1, ov76)
        ov76b = ov[6:9].copy()  # C reuses overlap[ob+6] which was MODIFIED by first call!
        # Actually C passes overlap+ob+6 (same pointer) to all three; each modifies it.
        # Replicate sequentially:
        o = ov[6:9].copy()
        imdct12(tmp, dst1, o)
        imdct12(tmp[1:], dst2, o)
        imdct12(tmp[2:], dst3, o)
        grbuf[gb:gb + 6] = ov[0:6]
        grbuf[gb + 6:gb + 12] = dst1
        grbuf[gb + 12:gb + 18] = dst2
        overlap[ob:ob + 6] = dst3
        overlap[ob + 6:ob + 9] = o


def change_sign(grbuf):
    for b in range(0, 32, 2):
        base = (b + 1) * 18
        grbuf[base + 1:base + 18:2] *= -1


def imdct_gr(grbuf, overlap, block_type, n_long_bands):
    if n_long_bands:
        imdct36(grbuf, overlap, G_MDCT_WINDOW[0], n_long_bands)
        return imdct_gr_off(grbuf[n_long_bands * 18:], overlap[n_long_bands * 9:], block_type, n_long_bands)
    if block_type == 2:
        imdct_short2(grbuf, overlap, 32)
    else:
        imdct36(grbuf, overlap, G_MDCT_WINDOW[1 if block_type == 3 else 0], 32)


def imdct_gr_off(grbuf, overlap, block_type, n_long_bands):
    if block_type == 2:
        imdct_short2(grbuf, overlap, 32 - n_long_bands)
    else:
        imdct36(grbuf, overlap, G_MDCT_WINDOW[1 if block_type == 3 else 0], 32 - n_long_bands)


def scale_pcm(sample):
    if sample >= 32766.5:
        return 32767
    if sample <= -32767.5:
        return -32768
    s = int(sample + 0.5)
    if s < 0:
        s -= 1
    return s


def dct_II(grbuf, n):
    # scalar replica
    for k in range(n):
        t = np.zeros((4, 8))
        y = grbuf[k:]
        for i in range(8):
            x0 = y[i * 18]; x1 = y[(15 - i) * 18]; x2 = y[(16 + i) * 18]; x3 = y[(31 - i) * 18]
            t0 = x0 + x3; t1 = x1 + x2
            t2 = (x1 - x2) * G_SEC[3 * i]; t3 = (x0 - x3) * G_SEC[3 * i + 1]
            t[0, i] = t0 + t1
            t[1, i] = (t0 - t1) * G_SEC[3 * i + 2]
            t[2, i] = t3 + t2
            t[3, i] = (t3 - t2) * G_SEC[3 * i + 2]
        for i in range(4):
            x0, x1, x2, x3, x4, x5, x6, x7 = t[i]
            xt = x0 - x7; x0 += x7
            x7 = x1 - x6; x1 += x6
            x6 = x2 - x5; x2 += x5
            x5 = x3 - x4; x3 += x4
            x4 = x0 - x3; x0 += x3
            x3 = x1 - x2; x1 += x2
            t[i, 0] = x0 + x1
            t[i, 4] = (x0 - x1) * 0.70710677
            x5 = x5 + x6
            x6 = (x6 + x7) * 0.70710677
            x7 = x7 + xt
            x3 = (x3 + x4) * 0.70710677
            x5 -= x7 * 0.198912367
            x7 += x5 * 0.382683432
            x5 -= x7 * 0.198912367
            x0 = xt - x6; xt += x6
            t[i, 1] = (xt + x7) * 0.50979561
            t[i, 2] = (x4 + x3) * 0.54119611
            t[i, 3] = (x0 - x5) * 0.60134488
            t[i, 5] = (x0 + x5) * 0.89997619
            t[i, 6] = (x4 - x3) * 1.30656302
            t[i, 7] = (xt - x7) * 2.56291556
        yy = grbuf[k:]
        if k > n - 3:
            for i in range(7):
                s = t[3, i] + t[3, i + 1]
                yy[i * 72] = t[0, i]
                yy[i * 72 + 18] = t[2, i] + s
                yy[i * 72 + 36] = t[1, i] + t[1, i + 1]
                yy[i * 72 + 54] = t[2, i + 1] + s
            yy[7 * 72] = t[0, 7]
            yy[7 * 72 + 18] = t[2, 7] + t[3, 7]
            yy[7 * 72 + 36] = t[1, 7]
            yy[7 * 72 + 54] = t[3, 7]
        else:
            for i in range(7):
                s = t[3, i] + t[3, i + 1]
                yy[i * 72] = t[0, i]
                yy[i * 72 + 18] = t[2, i] + s
                yy[i * 72 + 36] = t[1, i] + t[1, i + 1]
                yy[i * 72 + 54] = t[2, i + 1] + s
            yy[7 * 72] = t[0, 7]
            yy[7 * 72 + 18] = t[2, 7] + t[3, 7]
            yy[7 * 72 + 36] = t[1, 7]
            yy[7 * 72 + 54] = t[3, 7]


def synth_pair(pcm, pcm_off, nch, z, zb):
    a = ((z[zb + 14 * 64] - z[zb]) * 29 + (z[zb + 1 * 64] + z[zb + 13 * 64]) * 213 +
         (z[zb + 12 * 64] - z[zb + 2 * 64]) * 459 + (z[zb + 3 * 64] + z[zb + 11 * 64]) * 2037 +
         (z[zb + 10 * 64] - z[zb + 4 * 64]) * 5153 + (z[zb + 5 * 64] + z[zb + 9 * 64]) * 6574 +
         (z[zb + 8 * 64] - z[zb + 6 * 64]) * 37489 + z[zb + 7 * 64] * 75038)
    pcm[pcm_off] = scale_pcm(a)
    zb2 = zb + 2
    a = (z[zb2 + 14 * 64] * 104 + z[zb2 + 12 * 64] * 1567 + z[zb2 + 10 * 64] * 9727 +
         z[zb2 + 8 * 64] * 64019 + z[zb2 + 6 * 64] * -9975 + z[zb2 + 4 * 64] * -45 +
         z[zb2 + 2 * 64] * 146 + z[zb2] * -5)
    pcm[pcm_off + 16 * nch] = scale_pcm(a)


def synth(xl, xr, dstl, dst_off, nch, lins, lb):
    # lins: FULL scratch array; lb: base offset (= C's lins+i*64 pointer)
    ZB = lb + 15 * 64
    lins[ZB + 4 * 15] = xl[18 * 16]; lins[ZB + 4 * 15 + 1] = xr[18 * 16]
    lins[ZB + 4 * 15 + 2] = xl[0]; lins[ZB + 4 * 15 + 3] = xr[0]
    lins[ZB + 4 * 31] = xl[1 + 18 * 16]; lins[ZB + 4 * 31 + 1] = xr[1 + 18 * 16]
    lins[ZB + 4 * 31 + 2] = xl[1]; lins[ZB + 4 * 31 + 3] = xr[1]
    dstr_off = dst_off + (nch - 1)
    synth_pair(dstl, dstr_off, nch, lins, lb + 4 * 15 + 1)
    synth_pair(dstl, dstr_off + 32 * nch, nch, lins, lb + 4 * 15 + 64 + 1)
    synth_pair(dstl, dst_off, nch, lins, lb + 4 * 15)
    synth_pair(dstl, dst_off + 32 * nch, nch, lins, lb + 4 * 15 + 64)
    w = G_WIN
    wi = 0
    for i in range(14, -1, -1):
        lins[ZB + 4 * i] = xl[18 * (31 - i)]; lins[ZB + 4 * i + 1] = xr[18 * (31 - i)]
        lins[ZB + 4 * i + 2] = xl[1 + 18 * (31 - i)]; lins[ZB + 4 * i + 3] = xr[1 + 18 * (31 - i)]
        lins[ZB + 4 * (i + 16)] = xl[1 + 18 * (1 + i)]; lins[ZB + 4 * (i + 16) + 1] = xr[1 + 18 * (1 + i)]
        lins[ZB + 4 * (i - 16) + 2] = xl[18 * (1 + i)]; lins[ZB + 4 * (i - 16) + 3] = xr[18 * (1 + i)]
        a = np.zeros(4); b = np.zeros(4)
        for k in range(8):
            w0 = w[wi]; w1 = w[wi + 1]; wi += 2
            vz = lins[ZB + 4 * i - k * 64:ZB + 4 * i - k * 64 + 4]
            vy = lins[ZB + 4 * i - (15 - k) * 64:ZB + 4 * i - (15 - k) * 64 + 4]
            if k == 0:
                b = vz * w1 + vy * w0
                a = vz * w0 - vy * w1
            elif k % 2 == 1:  # S2
                b += vz * w1 + vy * w0
                a += vy * w1 - vz * w0
            else:  # S1
                b += vz * w1 + vy * w0
                a += vz * w0 - vy * w1
        dstl[dstr_off + (15 - i) * nch] = scale_pcm(a[1])
        dstl[dstr_off + (17 + i) * nch] = scale_pcm(b[1])
        dstl[dst_off + (15 - i) * nch] = scale_pcm(a[0])
        dstl[dst_off + (17 + i) * nch] = scale_pcm(b[0])
        dstl[dstr_off + (47 - i) * nch] = scale_pcm(a[3])
        dstl[dstr_off + (49 + i) * nch] = scale_pcm(b[3])
        dstl[dst_off + (47 - i) * nch] = scale_pcm(a[2])
        dstl[dst_off + (49 + i) * nch] = scale_pcm(b[2])


def synth_granule(qmf_state, grbuf, nch, pcm, pcm_off, lins):
    # grbuf: stacked [ch0 576][ch1 576] after IMDCT+sign; pcm int array
    for i in range(nch):
        dct_II(grbuf[i * 576:(i + 1) * 576], 18)
    lins[:15 * 64] = qmf_state[:15 * 64]
    for i in range(0, 18, 2):
        xl = grbuf[i:]
        xr = grbuf[i + 576 * (nch - 1):] if nch > 1 else xl
        synth(xl, xr, pcm, pcm_off + 32 * nch * i, nch, lins, i * 64)
    if nch == 1:
        for i in range(0, 15 * 64, 2):
            qmf_state[i] = lins[18 * 64 + i]
    else:
        qmf_state[:15 * 64] = lins[18 * 64:18 * 64 + 15 * 64]


class MP3Ref:
    def __init__(self, path):
        self.data = open(path, 'rb').read()
        self.reserv_buf = bytearray()
        self.reserv = 0
        self.overlap = [np.zeros(9 * 32, dtype=np.float64) for _ in range(2)]
        self.qmf_state = np.zeros(15 * 64, dtype=np.float64)
        self.lins = np.zeros(34 * 64, dtype=np.float64)
        self.sideinfo = []
        self.b1_deq = []
        self.b1_symbols = []
        self.b1_scf = []
        self.b2 = []
        self.b3 = []
        self.pcm_all = []
        self._parse_all()

    def _parse_all(self):
        d = self.data
        pos = 0
        if d[:3] == b'ID3':
            size = ((d[6] & 0x7F) << 21) | ((d[7] & 0x7F) << 14) | ((d[8] & 0x7F) << 7) | (d[9] & 0x7F)
            pos = 10 + size
        nframes = 0
        while pos + 4 <= len(d):
            if d[pos] == 0xFF and (d[pos + 1] & 0xE0) == 0xE0:
                ver = (d[pos + 1] >> 3) & 0x03
                layer = (d[pos + 1] >> 1) & 0x03
                br = (d[pos + 2] >> 4) & 0x0F
                sr = (d[pos + 2] >> 2) & 0x03
                if ver != 0x03 or layer != 0x01 or br in (0, 0x0F) or sr == 0x03:
                    pos += 1
                    continue
                frame_len = (144 * BITRATE_TAB[br] * 1000) // SR_TAB[sr] + ((d[pos + 2] >> 1) & 0x01)
                if pos + frame_len > len(d):
                    break
                pcm = self._decode_frame(d[pos:pos + frame_len], nframes)
                if pcm is not None:
                    self.pcm_all.append(pcm)
                    nframes += 1
                pos += frame_len
            else:
                pos += 1
        self.nframes = nframes
        self.pcm = np.concatenate(self.pcm_all) if self.pcm_all else np.zeros(0, dtype=np.int64)

    def _decode_frame(self, frame, frame_idx):
        hdr = frame[:4]
        mono = (hdr[3] & 0xC0) == 0xC0
        nch = 1 if mono else 2
        bs = BS(frame, 32)
        if (frame[1] & 0x01) == 0:
            bs.get_bits(16)
        try:
            gr_info, main_data_begin, sr_idx = read_side_info(bs, hdr)
        except ValueError:
            return None
        frame_bytes = (bs.limit - bs.pos) // 8
        bytes_have = min(self.reserv, main_data_begin)
        maindata = bytearray()
        if bytes_have:
            start = max(0, self.reserv - main_data_begin)
            maindata += self.reserv_buf[start:start + bytes_have]
        start_byte = bs.pos // 8
        maindata += frame[start_byte:start_byte + frame_bytes]
        if self.reserv < main_data_begin:
            return None
        mbs = BS(bytes(maindata), 0)
        frame_side = {'frame': frame_idx, 'mono': mono, 'main_data_begin': main_data_begin, 'granules': []}
        b1f_deq, b1f_sym, b1f_scf, b2f, b3f = [], [], [], [], []
        granule_pcm = []
        for igr in range(2):
            grbuf = [np.zeros(576, dtype=np.float64) for _ in range(nch)]
            ist_pos = [[0] * 40 for _ in range(nch)]
            scfs = []
            for ch in range(nch):
                gr = gr_info[igr * nch + ch]
                layer3gr_limit = mbs.pos + gr['part_23_length']
                scf, iscf = decode_scalefactors(hdr, ist_pos[ch], mbs, gr)
                scfs.append(scf)
                hr = HuffReader(mbs.buf, mbs.pos)
                symbols = []
                huffman(grbuf[ch], hr, gr, scf, layer3gr_limit, symbols)
                mbs.pos = layer3gr_limit
                b1f_deq.append(grbuf[ch].copy())
                b1f_sym.append(symbols)
                b1f_scf.append(iscf)
            stacked = np.concatenate(grbuf)  # [ch0 576][ch1 576]
            if (hdr[3] & 0x10) != 0:
                intensity_stereo(stacked, ist_pos[1], gr_info[igr * nch], hdr)
            elif (hdr[3] & 0xE0) == 0x60:
                midside_stereo(stacked, 576)
            for ch in range(nch):
                grbuf[ch] = stacked[ch * 576:(ch + 1) * 576].copy()
            my_sr = ((hdr[2] >> 2) & 0x03) + (((hdr[1] >> 3) & 1) + ((hdr[1] >> 4) & 1)) * 3
            for ch in range(nch):
                gr = gr_info[igr * nch + ch]
                n_long_bands = (2 if gr['mixed_block_flag'] else 0) << (1 if my_sr == 2 else 0)
                if gr['n_short_sfb']:
                    reorder(grbuf[ch], n_long_bands, gr['sfbtab'], gr['n_long_sfb'])
                b2f.append(grbuf[ch].copy())
            for ch in range(nch):
                gr = gr_info[igr * nch + ch]
                n_long_bands = (2 if gr['mixed_block_flag'] else 0) << (1 if my_sr == 2 else 0)
                aa_bands = n_long_bands - 1 if gr['n_short_sfb'] else 31
                antialias(grbuf[ch], aa_bands)
                imdct_gr(grbuf[ch], self.overlap[ch], gr['block_type'], n_long_bands)
                change_sign(grbuf[ch])
                b3f.append(grbuf[ch].copy())
            stacked2 = np.concatenate(grbuf)
            pcm_gr = np.zeros(18 * 32 * nch, dtype=np.int64)
            synth_granule(self.qmf_state, stacked2, nch, pcm_gr, 0, self.lins)
            granule_pcm.append(pcm_gr)
            frame_side['granules'].append([self._gr_summary(gr_info[igr * nch + ch]) for ch in range(nch)])
        pos_b = (mbs.pos + 7) // 8
        remains = len(maindata) - pos_b
        if remains > MAX_BITRESERVOIR_BYTES:
            pos_b += remains - MAX_BITRESERVOIR_BYTES
            remains = MAX_BITRESERVOIR_BYTES
        self.reserv_buf = bytearray(maindata[pos_b:pos_b + remains]) if remains > 0 else bytearray()
        self.reserv = remains
        self.sideinfo.append(frame_side)
        self.b1_deq.append(b1f_deq); self.b1_symbols.append(b1f_sym); self.b1_scf.append(b1f_scf)
        self.b2.append(b2f); self.b3.append(b3f)
        return np.concatenate(granule_pcm) if granule_pcm else None

    def _gr_summary(self, gr):
        return {k: gr[k] for k in ('part_23_length', 'big_values', 'global_gain',
                'scalefac_compress', 'block_type', 'mixed_block_flag', 'table_select',
                'region_count', 'preflag', 'scalefac_scale', 'count1_table', 'scfsi',
                'subblock_gain', 'n_long_sfb', 'n_short_sfb')}


def main():
    path, outdir = sys.argv[1], sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    ref = MP3Ref(path)
    print('frames:', ref.nframes, 'pcm samples:', len(ref.pcm), flush=True)
    json.dump(ref.sideinfo, open(os.path.join(outdir, 'sideinfo.json'), 'w'))
    np.save(os.path.join(outdir, 'b1_deq.npy'), np.array(ref.b1_deq))
    np.save(os.path.join(outdir, 'b2.npy'), np.array(ref.b2))
    np.save(os.path.join(outdir, 'b3.npy'), np.array(ref.b3))
    ref.pcm.astype('<i2').tofile(os.path.join(outdir, 'b4.s16'))
    json.dump(ref.b1_symbols, open(os.path.join(outdir, 'b1_symbols.json'), 'w'))
    json.dump(ref.b1_scf, open(os.path.join(outdir, 'b1_scf.json'), 'w'))
    print('wrote', outdir, flush=True)


if __name__ == '__main__':
    main()
