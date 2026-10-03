#!/usr/bin/env python3
"""Generate mp3tab64.zag: integer Huffman/scalefactor tables (byte strings)
plus f64 signal tables (f32 bit patterns -> f32_to_f64 for exact widening).
Writes to stdout; redirect to mp3tab64.zag."""
import json, struct, sys

t = json.load(open('harvest/ref/mp3_tables.json'))

def esc(data: bytes) -> str:
    out = []
    for b in data:
        if b == 34: out.append('\\"')
        elif b == 92: out.append('\\\\')
        elif 32 <= b < 127: out.append(chr(b))
        else: out.append('\\x%02x' % b)
    return ''.join(out)

def u16le_str(vals):
    return esc(struct.pack('<%dH' % len(vals), *[v & 0xFFFF for v in vals]))

def u8_str(vals):
    flat = []
    for v in vals:
        if isinstance(v, list):
            flat.extend(v + [0] * (39 - len(v)))
        else: flat.append(v)
    return esc(bytes(x & 0xFF for x in flat))

def i16le_str(vals):
    return esc(struct.pack('<%dh' % len(vals), *vals))

def f32bits_str(vals):
    # store raw f32 bit patterns (little-endian u32)
    bits = [struct.unpack('<I', struct.pack('<f', v))[0] for v in vals]
    return esc(struct.pack('<%dI' % len(bits), *bits))

o = []
o.append('// mp3tab64.zag - MP3 tables for the pure-Zag decoder.')
o.append('// Integer tables as byte strings; f64 signal tables as f32 bit patterns')
o.append('// widened at load via f32_to_f64 (exact f32->f64).')
o.append('@import("./common.zag")')
o.append('')

# --- integer tables ---
o.append('fn t_tabs() []u8 { return "%s"; }' % i16le_str(t['tabs']))
o.append('fn t_tabindex() []u8 { return "%s"; }' % u16le_str(t['tabindex']))
o.append('fn t_tab32() []u8 { return "%s"; }' % u8_str(t['tab32']))
o.append('fn t_tab33() []u8 { return "%s"; }' % u8_str(t['tab33']))
o.append('fn t_linbits() []u8 { return "%s"; }' % u8_str(t['g_linbits']))
o.append('fn t_scf_long() []u8 { return "%s"; }' % u8_str(t['g_scf_long']))
o.append('fn t_scf_short() []u8 { return "%s"; }' % u8_str(t['g_scf_short']))
o.append('fn t_scf_mixed_rows() []u8 { return "%s"; }' % u8_str(t['g_scf_mixed_rows']))
o.append('fn t_scf_partitions() []u8 { return "%s"; }' % u8_str(t['g_scf_partitions']))
o.append('fn t_scfc_decode() []u8 { return "%s"; }' % u8_str(t['g_scfc_decode']))
o.append('fn t_preamp() []u8 { return "%s"; }' % u8_str(t['g_preamp']))
o.append('fn t_mod() []u8 { return "%s"; }' % u8_str(t['g_mod']))
o.append('')
# --- f64 tables (f32 bits) ---
o.append('fn t_pow43b() []u8 { return "%s"; }' % f32bits_str(t['g_pow43']))
o.append('fn t_expfracb() []u8 { return "%s"; }' % f32bits_str(t['g_expfrac']))
o.append('fn t_aab() []u8 { return "%s"; }' % f32bits_str(t['g_aa']))
o.append('fn t_twid9b() []u8 { return "%s"; }' % f32bits_str(t['g_twid9']))
o.append('fn t_twid3b() []u8 { return "%s"; }' % f32bits_str(t['g_twid3']))
o.append('fn t_mdctwinb() []u8 { return "%s"; }' % f32bits_str(t['g_mdct_window']))
o.append('fn t_secb() []u8 { return "%s"; }' % f32bits_str(t['g_sec']))
o.append('fn t_winb() []u8 { return "%s"; }' % f32bits_str(t['g_win']))
o.append('fn t_panb() []u8 { return "%s"; }' % f32bits_str(t['g_pan']))
o.append('')

# --- accessors ---
o.append('''// ---- integer accessors ----
fn tab_get(i: i64) i64 {
    let d: []u8 = t_tabs();
    let b: i64 = i * 2;
    let v: i64 = ((d[b + 1] as i64) << 8) | (d[b] as i64);
    if (v >= 32768) { v = v - 65536; }
    return v;
}
fn tabindex_get(i: i64) i64 {
    let d: []u8 = t_tabindex();
    let b: i64 = i * 2;
    return (((d[b + 1] as i64) << 8) | (d[b] as i64));
}
fn tab32_get(i: i64) i64 { return (t_tab32()[i] as i64) & 255; }
fn tab33_get(i: i64) i64 { return (t_tab33()[i] as i64) & 255; }
fn linbits_get(i: i64) i64 { return (t_linbits()[i] as i64) & 255; }
fn scf_long_get(i: i64) i64 { return (t_scf_long()[i] as i64) & 255; }
fn scf_short_get(i: i64) i64 { return (t_scf_short()[i] as i64) & 255; }
fn scf_part_get(i: i64) i64 { return (t_scf_partitions()[i] as i64) & 255; }
fn scfc_get(i: i64) i64 { return (t_scfc_decode()[i] as i64) & 255; }
fn preamp_get(i: i64) i64 { return (t_preamp()[i] as i64) & 255; }
fn expfrac_get(i: i64) i64 { return (t_expfrac()[i] as i64) & 255; }
fn mod_get(i: i64) i64 { return (t_mod()[i] as i64) & 255; }
fn mixed_row_get(row: i64, i: i64) i64 { return (t_scf_mixed_rows()[(row * 39 + i)] as i64) & 255; }

// ---- f64 table loader: widen f32 bits exactly ----
fn f32_to_f64_z(bits: i64) f64 {
    let mant: i64 = bits & 8388607;
    let exp: i64 = (bits >> 23) & 255;
    let neg: i64 = (bits >> 31) & 1;
    let v: f64 = 0.0;
    if (exp == 0) {
        if (mant != 0) { v = (mant as f64) / 8388608.0 * pow2f_z(-126); }
    } else {
        v = (1.0 + (mant as f64) / 8388608.0) * pow2f_z(exp - 127);
    }
    if (neg == 1) { v = 0.0 - v; }
    return v;
}
fn pow2f_z(k: i64) f64 {
    let v: f64 = 1.0;
    if (k >= 0) { let i: i64 = 0; while (i < k) { v = v * 2.0; i = i + 1; } }
    else { let i: i64 = 0; while (i > k) { v = v / 2.0; i = i - 1; } }
    return v;
}
fn load_f64tab(src: []u8, n: i64) []f64 {
    let raw: *u8 = _zag_malloc(n * 8) as *u8;
    let a: []f64 = raw[0..n*8] as []f64;
    let i: i64 = 0;
    while (i < n) {
        let b: i64 = i * 4;
        let bits: i64 = ((src[b+3] as i64) << 24) | ((src[b+2] as i64) << 16) | ((src[b+1] as i64) << 8) | (src[b] as i64);
        a[i] = f32_to_f64_z(bits);
        i = i + 1;
    }
    return a;
}
''')
sys.stdout.write('\n'.join(o) + '\n')
