#!/usr/bin/env python3
"""Apply CREW GAMMA experiment patches to a field.zag variant copy.

Patches (experiment scaffolding only; emitter behavior untouched unless the
variant spec says so):
  1. Insert diagnostic helpers + two new main modes (f3mixpeak, f3mixdump)
     before the final error=unknown-cmd line.
  2. Variant-specific edits applied separately by the caller.

Usage: patch_variant.py <in.zag> <out.zag> [--h2 num den] [--revert] [--h1]
"""
import sys

HELPERS = r'''
// ============ CREW GAMMA experiment scaffolding (not emitter behavior) ============
// f3_mixpeak: unclipped max|mix| of the hifi synth for one field (diagnostic).
fn f3_mixpeak(ar:[]u8, lut:[]u8) i64 {
    let total:i64 = f3_synth_total_hifi(ar);
    let mix:[]u8 = f3_synth_hifi(ar, lut, total);
    if (mix.len == 0) { return -1; }
    let pk:i64 = 0;
    let s:i64 = 0;
    while (s < total) {
        let v:i64 = f3_get32s(mix, s);
        if (v < 0) { v = -v; }
        if (v > pk) { pk = v; }
        s = s + 1;
    }
    nio_free(mix);
    return pk;
}
// f3_mixdump_one: write raw s32 LE pre-emit mix to outdir/name (mix-level identity).
fn f3_mixdump_one(ar:[]u8, dir:[]u8, name:[]u8, lut:[]u8) i64 {
    let total:i64 = f3_synth_total_hifi(ar);
    let mix:[]u8 = f3_synth_hifi(ar, lut, total);
    if (mix.len == 0) { return -10; }
    let root:i64 = f3_open_root_z(dir);
    if (root < 0) { nio_free(mix); return -1; }
    let fd:i64 = f3_open_child_z(root, name, 1);
    nio_close(root);
    if (fd < 0) { nio_free(mix); return -2; }
    let w:i64 = nio_write_all(fd, mix);
    nio_close(fd);
    nio_free(mix);
    if (w != total * 4) { return -3; }
    return 0;
}
'''

MODES = r'''
    // CREW GAMMA diagnostics (experiment scaffolding, not emitter behavior):
    // f3mixpeak prints the unclipped mix peak per hifi fixture;
    // f3mixdump writes raw s32 pre-emit mixes (mix-level identity checks).
    if (_zag_strcmp(a1, "f3mixpeak") == 1) {
        let lutd:[]u8 = nio_alloc(512);
        j2_sin_init(lutd);
        let ahd:[]u8 = nio_alloc(24576);
        f3_build(ahd, 17);
        _zag_print("MIXPEAK song ");
        _zag_println(_zag_i64_to_str(f3_mixpeak(ahd, lutd)));
        let md2:i64 = 0;
        while (md2 < 3) {
            f3_gen_mood(ahd, md2);
            _zag_print("MIXPEAK mood ");
            _zag_print(_zag_i64_to_str(md2));
            _zag_print(" ");
            _zag_println(_zag_i64_to_str(f3_mixpeak(ahd, lutd)));
            md2 = md2 + 1;
        }
        nio_free(ahd);
        nio_free(lutd);
        return 0;
    }
    if (_zag_strcmp(a1, "f3mixdump") == 1) {
        if (a2.len == 0) {
            _zag_println("error=f3mixdump-needs-outdir");
            return 1;
        }
        let lute:[]u8 = nio_alloc(512);
        j2_sin_init(lute);
        let ahe:[]u8 = nio_alloc(24576);
        f3_build(ahe, 17);
        _zag_print("MIXDUMP song rc=");
        _zag_println(_zag_i64_to_str(f3_mixdump_one(ahe, a2, "mix_song.s32", lute)));
        let md3:i64 = 0;
        while (md3 < 3) {
            f3_gen_mood(ahe, md3);
            _zag_print("MIXDUMP mood ");
            _zag_print(_zag_i64_to_str(md3));
            _zag_print(" rc=");
            let nm:[]u8 = "mix_mood0.s32";
            if (md3 == 1) { nm = "mix_mood1.s32"; }
            if (md3 == 2) { nm = "mix_mood2.s32"; }
            _zag_println(_zag_i64_to_str(f3_mixdump_one(ahe, a2, nm, lute)));
            md3 = md3 + 1;
        }
        nio_free(ahe);
        nio_free(lute);
        return 0;
    }
'''

def main():
    inp, outp = sys.argv[1], sys.argv[2]
    args = sys.argv[3:]
    with open(inp) as f:
        src = f.read()

    # 1. helpers before fn main (idempotent: skip if already present)
    if "fn f3_mixpeak(" not in src:
        anchor = "fn main() i32 {"
        assert src.count(anchor) == 1
        src = src.replace(anchor, HELPERS + "\n" + anchor, 1)

    # 2. modes before error=unknown-cmd (idempotent)
    if '"f3mixpeak"' not in src:
        anchor2 = '    _zag_println("error=unknown-cmd");'
        assert src.count(anchor2) == 1
        src = src.replace(anchor2, MODES + anchor2, 1)

    # 3. H2: fixed plan-pure mastering gain in f3_emit_wav_hifi
    if "--h2" in args:
        i = args.index("--h2")
        num, den = args[i+1], args[i+2]
        old = """        let v:i64 = f3_get32s(mix, s2);
        if (v > 32767) { v = 32767; }"""
        new = """        let v:i64 = f3_get32s(mix, s2);
        // CREW GAMMA H2: fixed plan-pure mastering gain (constant, never
        // output-derived): v = v * %s / %s. Fixed rails stay below.
        v = v * %s / %s;
        if (v > 32767) { v = 32767; }""" % (num, den, num, den)
        assert src.count(old) == 1, "h2 anchor not found"
        src = src.replace(old, new, 1)

    # 4. revert: restore the OLD output-derived normalizer in f3_emit_wav_hifi
    if "--revert" in args:
        old = """    // GAMMA REPAIR 2026-09-24: output-derived peak normalizer deleted
    // (was: v = v*24000/peak). Plan-pure gain = 1: the synth stages levels
    // by construction (clipping impossible by design); the fixed clamps
    // below are constant safety rails, not output-derived scaling.
    let pcm:[]u8 = nio_alloc((44 + total * 2) as i32);
    if (pcm.len == 0) { nio_free(mix); return -11; }
    let s2:i64 = 0;
    while (s2 < total) {
        let v:i64 = f3_get32s(mix, s2);
        if (v > 32767) { v = 32767; }
        if (v < -32768) { v = -32768; }
        j2_put16(pcm, 22 + s2, v);
        s2 = s2 + 1;
    }"""
        new = """    // CREW GAMMA control (revert): OLD output-derived peak normalizer
    // restored in f3_emit_wav_hifi: peak scan + v = v*24000/peak (always).
    let pk2:i64 = 0;
    let q2:i64 = 0;
    while (q2 < total) {
        let vv:i64 = f3_get32s(mix, q2);
        if (vv < 0) { vv = -vv; }
        if (vv > pk2) { pk2 = vv; }
        q2 = q2 + 1;
    }
    if (pk2 < 1) { pk2 = 1; }
    let pcm:[]u8 = nio_alloc((44 + total * 2) as i32);
    if (pcm.len == 0) { nio_free(mix); return -11; }
    let s2:i64 = 0;
    while (s2 < total) {
        let v:i64 = f3_get32s(mix, s2);
        v = v * 24000 / pk2;
        if (v > 32767) { v = 32767; }
        if (v < -32768) { v = -32768; }
        j2_put16(pcm, 22 + s2, v);
        s2 = s2 + 1;
    }"""
        assert src.count(old) == 1, "revert anchor not found"
        src = src.replace(old, new, 1)

    with open(outp, "w") as f:
        f.write(src)
    print("patched ->", outp)

main()
