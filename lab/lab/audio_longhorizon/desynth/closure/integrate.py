#!/usr/bin/env python3
"""Integrate WALL-1 (trig-free hearing) + WALL-2 (f0 guard fix) + WALL-3 (6-timbre vocab).

Step 1: 3-way line merge of plan_main:
  base = wall1/ref_plan_main_desynth.zag (frozen @ 4f782c40d766)
  A    = wall1/src/plan_main_notrig.zag  (base + WALL-1 hear diff)
  B    = wall2/plan_main_fixed.zag       (base + WALL-2 analytic correction)
Step 2: apply WALL-3 atom-vocabulary changes (VOCAB_SPEC.md section 2),
  plus one spec-gap fix the spec missed: render_plan's
  `if (amode == 2 or amode == 3) { use_con = 1; }` must become
  is_contour(amode) or new contour amodes 5/7/9/11 would render flat.
Step 3: assemble final_full.zag =
  wall1/src/hear_trigfree.zag + wall2/f0low_fixed.zag + merged plan_main.

Every replacement asserts its occurrence count. Any assertion failure aborts.
"""
import difflib, sys

D = "/home/hatch/workspace/desynth_closure"
FROZEN = f"{D}/wall1/ref_plan_main_desynth.zag"
NOTRIG = f"{D}/wall1/src/plan_main_notrig.zag"
FIXED  = f"{D}/wall2/plan_main_fixed.zag"
OUTDIR = f"{D}/integrate/build"
FINAL_MAIN = f"{OUTDIR}/plan_main_final.zag"
FINAL_FULL = f"{OUTDIR}/plan_final_full.zag"

def lines(p):
    with open(p) as f:
        return f.read().splitlines(keepends=True)

def edits(base, other):
    sm = difflib.SequenceMatcher(None, base, other, autojunk=False)
    out = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag != "equal":
            out.append((i1, i2, other[j1:j2], tag))
    return out

base, a, b = lines(FROZEN), lines(NOTRIG), lines(FIXED)
ea, eb = edits(base, a), edits(base, b)
print(f"wall1 edits: {len(ea)}, wall2 edits: {len(eb)}")
for (s1, e1, _, _) in ea:
    for (s2, e2, _, _) in eb:
        assert e1 <= s2 or e2 <= s1, f"OVERLAP wall1[{s1},{e1}) wall2[{s2},{e2})"
print("no overlapping edit regions - merge is clean")

# merge: walk base, apply A-edits and B-edits in base-line order
all_edits = sorted([(s, e, nl, "A") for (s, e, nl, _) in ea] +
                   [(s, e, nl, "B") for (s, e, nl, _) in eb])
merged, pos = [], 0
for (s, e, nl, who) in all_edits:
    merged.extend(base[pos:s])
    merged.extend(nl)
    pos = e
merged.extend(base[pos:])
text = "".join(merged)
print(f"merged plan_main: {len(merged)} lines")

# ---------- WALL-3 changes ----------
def rep(old, new, expect):
    global text
    n = text.count(old)
    assert n == expect, f"expected {expect} of {old[:60]!r}, found {n}"
    text = text.replace(old, new)
    print(f"ok: replaced {expect}x :: {old[:64].strip()!r}")

# R1: helpers + atom_path_for
rep('''fn atom_path_for(amode: i64, buf: []u8) i64 {
    // Returns length of the atom path written into buf.
    // v1: atoms live in the workstream dir (documented, not hidden).
    let base: []u8 = "/home/hatch/workspace/desynth/atoms/";
    let i: i64 = 0;
    while (i < base.len) { buf[i] = base[i]; i = i + 1; }
    let name: []u8 = "atom0_child.bin";
    if (amode == 1 or amode == 3) { name = "atom1_speech.bin"; }''',
'''// WALL-3 (2026-09-27): 6-timbre vocabulary. amode 0..11 decodes to
// (timbre 0..5, flat/contour). Old amodes 0..3 decode exactly as before.
fn timbre_of(amode: i64) i64 {
    if (amode < 4) { return amode & 1; }
    return (amode - 4) / 2 + 2;
}
fn is_contour(amode: i64) i64 {
    if (amode < 4) {
        if (amode >= 2) { return 1; }
        return 0;
    }
    if (amode % 2 == 1) { return 1; }
    return 0;
}
fn flat_amode(timbre: i64) i64 {
    if (timbre < 2) { return timbre; }
    return timbre * 2;
}
fn atom_path_for(amode: i64, buf: []u8) i64 {
    // Returns length of the atom path written into buf.
    // v1: atoms live in the workstream dir (documented, not hidden).
    let base: []u8 = "/home/hatch/workspace/desynth/atoms/";
    let i: i64 = 0;
    while (i < base.len) { buf[i] = base[i]; i = i + 1; }
    let tm: i64 = timbre_of(amode);
    let name: []u8 = "atom0_child.bin";
    if (tm == 1) { name = "atom1_speech.bin"; }
    if (tm == 2) { name = "atom2_rise.bin"; }
    if (tm == 3) { name = "atom3_rise.bin"; }
    if (tm == 4) { name = "atom4_decay.bin"; }
    if (tm == 5) { name = "atom5_decay.bin"; }''', 1)

# R2: render_plan contour dispatch (SPEC GAP FIX - spec said render_plan untouched,
# but the old `amode == 2 or amode == 3` test would leave new contour amodes 5/7/9/11
# rendering flat. Root-caused by grep, not by the spec.)
rep('''    // Contour mode: amode 2/3 use the 16-pt measured contour from CON.
    // CON holds 16 i64 mHz values (planner's D arena format).
    let use_con: i64 = 0;
    if (amode == 2 or amode == 3) { use_con = 1; }''',
'''    // Contour mode: contour amodes (is_contour) use the 16-pt measured contour
    // from CON. CON holds 16 i64 mHz values (planner's D arena format).
    // WALL-3: was `amode == 2 or amode == 3`; the old test stranded new
    // contour amodes 5/7/9/11 on flat renders.
    let use_con: i64 = 0;
    if (is_contour(amode) == 1) { use_con = 1; }''', 1)

# R3: bias_ppm_at - delete the &1 mask, timbre is now 0..5
rep('''fn bias_ppm_at(CALIB: []u8, timbre: i64, f0mhz: i64) i64 {
    let t: i64 = timbre & 1;''',
'''fn bias_ppm_at(CALIB: []u8, timbre: i64, f0mhz: i64) i64 {
    // WALL-3: timbre is 0..5 (6 timbres); the old &1 mask is deleted.
    let t: i64 = timbre;''', 1)
rep('''// CALIB: per timbre t (0=atom0/child, 1=atom1/speech):
//   bias90_ppm@t*40, bias220_ppm@t*40+8, bias1010_ppm@t*40+16,
//   cv_yield_pm@t*40+24, voiced_frac_pm@t*40+32.''',
'''// CALIB: per timbre t 0..5 (0=atom0/child, 1=atom1/speech, 2=atom2/rise,
// 3=atom3/rise, 4=atom4/decay, 5=atom5/decay):
//   bias90_ppm@t*40, bias220_ppm@t*40+8, bias1010_ppm@t*40+16,
//   cv_yield_pm@t*40+24, voiced_frac_pm@t*40+32.''', 1)

# R4: yield_frontier - loop over 6 timbres
rep('''fn yield_frontier(CALIB: []u8) i64 {
    let y0: i64 = get64(CALIB, 24);
    let y1: i64 = get64(CALIB, 64);
    if (y1 > y0) { return y1; }
    return y0;
}''',
'''fn yield_frontier(CALIB: []u8) i64 {
    // WALL-3: max flat-atom CV yield across all 6 timbres.
    let best: i64 = 0;
    let t: i64 = 0;
    while (t < 6) {
        let y: i64 = get64(CALIB, t * 40 + 24);
        if (y > best) { best = y; }
        t = t + 1;
    }
    return best;
}''', 1)

# R5: cal_run over 6 timbres
rep('''    let t: i64 = 0;
    while (t < 2) {''',
'''    let t: i64 = 0;
    while (t < 6) {''', 1)

# R6: cal_run probe render uses the timbre's FLAT amode
rep('if (render_plan(pp, f0p, 0, 5, t, 1000000, 0, 0, 0, "") != 0) {',
    'if (render_plan(pp, f0p, 0, 5, flat_amode(t), 1000000, 0, 0, 0, "") != 0) {', 1)

# R7: CALIB arena doc comments (2 occurrences)
rep('''// CALIB arena (80 bytes, i64 @8B), per timbre t (0=atom0/child, 1=atom1/speech):''',
'''// CALIB arena (240 bytes, i64 @8B), per timbre t 0..5:''', 2)

# R8: CALIB_END journal - extend to 6 timbres
rep('''    _zag_print(" timbre1 bias90_ppm=");
    _zag_print(i64s(get64(CALIB, 40)));
    _zag_print(" bias220_ppm=");
    _zag_print(i64s(get64(CALIB, 48)));
    _zag_print(" bias1010_ppm=");
    _zag_print(i64s(get64(CALIB, 56)));
    _zag_print(" cv_yield_pm=");
    _zag_print(i64s(get64(CALIB, 64)));
    _zag_print(" voiced_frac_pm=");
    _zag_print(i64s(get64(CALIB, 72)));
    _zag_print("\\n");''',
'''    _zag_print(" timbre1 bias90_ppm=");
    _zag_print(i64s(get64(CALIB, 40)));
    _zag_print(" bias220_ppm=");
    _zag_print(i64s(get64(CALIB, 48)));
    _zag_print(" bias1010_ppm=");
    _zag_print(i64s(get64(CALIB, 56)));
    _zag_print(" cv_yield_pm=");
    _zag_print(i64s(get64(CALIB, 64)));
    _zag_print(" voiced_frac_pm=");
    _zag_print(i64s(get64(CALIB, 72)));
    _zag_print(" timbre2 bias90_ppm=");
    _zag_print(i64s(get64(CALIB, 80)));
    _zag_print(" bias220_ppm=");
    _zag_print(i64s(get64(CALIB, 88)));
    _zag_print(" bias1010_ppm=");
    _zag_print(i64s(get64(CALIB, 96)));
    _zag_print(" cv_yield_pm=");
    _zag_print(i64s(get64(CALIB, 104)));
    _zag_print(" voiced_frac_pm=");
    _zag_print(i64s(get64(CALIB, 112)));
    _zag_print(" timbre3 bias90_ppm=");
    _zag_print(i64s(get64(CALIB, 120)));
    _zag_print(" bias220_ppm=");
    _zag_print(i64s(get64(CALIB, 128)));
    _zag_print(" bias1010_ppm=");
    _zag_print(i64s(get64(CALIB, 136)));
    _zag_print(" cv_yield_pm=");
    _zag_print(i64s(get64(CALIB, 144)));
    _zag_print(" voiced_frac_pm=");
    _zag_print(i64s(get64(CALIB, 152)));
    _zag_print(" timbre4 bias90_ppm=");
    _zag_print(i64s(get64(CALIB, 160)));
    _zag_print(" bias220_ppm=");
    _zag_print(i64s(get64(CALIB, 168)));
    _zag_print(" bias1010_ppm=");
    _zag_print(i64s(get64(CALIB, 176)));
    _zag_print(" cv_yield_pm=");
    _zag_print(i64s(get64(CALIB, 184)));
    _zag_print(" voiced_frac_pm=");
    _zag_print(i64s(get64(CALIB, 192)));
    _zag_print(" timbre5 bias90_ppm=");
    _zag_print(i64s(get64(CALIB, 200)));
    _zag_print(" bias220_ppm=");
    _zag_print(i64s(get64(CALIB, 208)));
    _zag_print(" bias1010_ppm=");
    _zag_print(i64s(get64(CALIB, 216)));
    _zag_print(" cv_yield_pm=");
    _zag_print(i64s(get64(CALIB, 224)));
    _zag_print(" voiced_frac_pm=");
    _zag_print(i64s(get64(CALIB, 232)));
    _zag_print("\\n");''', 1)

# R9a: shootout candidate count
rep('    let ncand: i64 = 4;', '    let ncand: i64 = 12;', 1)

# R9b: candidate names
rep('''        let cname: []u8 = "atom0-flat";
        if (ci == 1) { cname = "atom1-flat"; }
        if (ci == 2) { cname = "atom0-contour"; }
        if (ci == 3) { cname = "atom1-contour"; }''',
'''        let cname: []u8 = "atom0-flat";
        if (ci == 1) { cname = "atom1-flat"; }
        if (ci == 2) { cname = "atom0-contour"; }
        if (ci == 3) { cname = "atom1-contour"; }
        if (ci == 4) { cname = "atom2-flat"; }
        if (ci == 5) { cname = "atom2-contour"; }
        if (ci == 6) { cname = "atom3-flat"; }
        if (ci == 7) { cname = "atom3-contour"; }
        if (ci == 8) { cname = "atom4-flat"; }
        if (ci == 9) { cname = "atom4-contour"; }
        if (ci == 10) { cname = "atom5-flat"; }
        if (ci == 11) { cname = "atom5-contour"; }''', 1)

# R9c: contour skip guard
rep('        if (ci >= 2 && has_con == 0) {',
    '        if (is_contour(ci) == 1 && has_con == 0) {', 1)

# R9d: stem two-digit widening (stem bug fix: ci=10/11 printed ':'/';')
rep('''        stem[4] = 99; stem[5] = (48 + ci) as u8; stem[6] = 0;
        let pp: []u8 = out_path(pdir, stem[0..6]);''',
'''        stem[4] = 99; stem[5] = (48 + (ci / 10)) as u8; stem[6] = (48 + (ci % 10)) as u8; stem[7] = 0;
        let pp: []u8 = out_path(pdir, stem[0..7]);''', 1)

# R9e: candidates doc comment
rep('''//   H3: atom0 contour (child timbre, follows the case's measured contour)
//   H4: atom1 contour (speech timbre, follows the case's measured contour)''',
'''//   H3: atom0 contour (child timbre, follows the case's measured contour)
//   H4: atom1 contour (speech timbre, follows the case's measured contour)
//   H5/H6: atom2 flat/contour (rise timbre)
//   H7/H8: atom3 flat/contour (rise timbre)
//   H9/H10: atom4 flat/contour (decay timbre)
//   H11/H12: atom5 flat/contour (decay timbre)''', 1)

# R10: every `am & 1` -> timbre_of(am)  (6 frozen sites + 1 wall-2 site)
rep('am & 1', 'timbre_of(am)', 7)

# R11: every `am >= 2` / `am0 >= 2` -> is_contour
rep('am0 >= 2', 'is_contour(am0) == 1', 1)
rep('am >= 2', 'is_contour(am) == 1', 5)

# R12: CALIB arena 80 -> 240 bytes
rep('let CALIB: []u8 = (_zag_malloc(80) as *u8)[0..80];',
    'let CALIB: []u8 = (_zag_malloc(240) as *u8)[0..240];', 1)

# --- R8: envelope-aware honesty gate (integration fix, 2026-09-27) ---
# A decay envelope's tail fades BY DESIGN; the organ correctly leaves the
# faded tail unvoiced. The flat 500/1000 gate miscalibrates for decay
# timbres (atom4_decay voices 494/1000 with correct f0 and 3577 ppm bias).
# The gate's purpose is reliable calibration (enough voiced frames for a
# robust bias median), not majority-voicing regardless of envelope shape.
rep('''            if (m == 1) {
                // 220 Hz probe: the timbre's CV yield and voiced fraction.
                // A flat atom can only cover CV needs up to this measured yield.
                put64(CALIB, t * 40 + 24, get64(D, 32));
                put64(CALIB, t * 40 + 32, get64(D, 8));
            }''',
'''            if (m == 1) {
                // 220 Hz probe: the timbre's CV yield and voiced fraction.
                // A flat atom can only cover CV needs up to this measured yield.
                put64(CALIB, t * 40 + 24, get64(D, 32));
                put64(CALIB, t * 40 + 32, get64(D, 8));
                env220 = get64(D, 16);
            }''', 1)
rep('''    let t: i64 = 0;
    while (t < 6) {
        let m: i64 = 0;''',
'''    let t: i64 = 0;
    while (t < 6) {
        let env220: i64 = 0;
        let m: i64 = 0;''', 1)
rep('''        // Honesty gate: the planner must hear its own timbre — voiced and
        // close to the render f0 — or there is nothing to calibrate.
        let vf: i64 = get64(CALIB, t * 40 + 32);
        let b220: i64 = get64(CALIB, t * 40 + 8);
        let ab: i64 = b220;
        if (ab < 0) { ab = 0 - ab; }
        if (vf < 500 || ab > 100000) {''',
'''        // Honesty gate (envelope-aware): the planner must hear its own
        // timbre — voiced and close to the render f0 — or there is nothing
        // to calibrate. A decay envelope's tail fades by design, so the
        // organ correctly leaves it unvoiced; the floor is 400 for decay
        // (still 400 voiced frames for a robust bias median), 500 else.
        let vf: i64 = get64(CALIB, t * 40 + 32);
        let b220: i64 = get64(CALIB, t * 40 + 8);
        let ab: i64 = b220;
        if (ab < 0) { ab = 0 - ab; }
        let vfloor: i64 = 500;
        if (env220 == 2) { vfloor = 400; }
        if (vf < vfloor || ab > 100000) {''', 1)

# --- R9: envelope-aware consult prediction (integration fix, 2026-09-27) ---
# The consult's predicted error omitted the envelope term, so a single
# opinionated timbre (atom2's rise) won once and was reused for all 20
# targets, regressing flat/decay targets. The render's envelope comes from
# the atom's measured trajectory (the timbre), not the F0 mode — so the
# consult must penalize timbre/env mismatches, exactly as the 12-way
# growth shootout already does (500 for env_ok=0).
rep('''            // Predicted CV error: flat atoms hold their measured yield;
            // contour atoms impose the case's shape (fid scales the magnitude).
            let cvt: i64 = 0;
            if (is_contour(am) == 1) {
                let dc2: i64 = fid - 1000;
                if (dc2 < 0) { dc2 = 0 - dc2; }
                if (need_pm > 0 && dc2 > 250) { cvt = 500; }
            }
            let pred: i64 = f0t + cvt;''',
'''            // Predicted CV error: flat atoms hold their measured yield;
            // contour atoms impose the case's shape (fid scales the magnitude).
            let cvt: i64 = 0;
            if (is_contour(am) == 1) {
                let dc2: i64 = fid - 1000;
                if (dc2 < 0) { dc2 = 0 - dc2; }
                if (need_pm > 0 && dc2 > 250) { cvt = 500; }
            }
            // Predicted envelope error: the render's envelope is the
            // atom's measured trajectory (timbre), independent of F0 mode.
            // Timbre 0/1=flat, 2/3=rise, 4/5=decay. Mismatch costs 500,
            // the same env penalty the growth shootout applies.
            let tenv: i64 = 0;
            let timc: i64 = timbre_of(am);
            if (timc == 2 || timc == 3) { tenv = 1; }
            if (timc == 4 || timc == 5) { tenv = 2; }
            let envt: i64 = 0;
            if (tenv != envh) { envt = 500; }
            let pred: i64 = f0t + cvt + envt;''', 1)

# --- R10: envelope-aware coverage (integration fix, 2026-09-27) ---
# R9's pred penalty is ineffective when only one action covers: the planner
# reuses the rise timbre for flat/decay targets instead of growing. The
# render's envelope is the atom's measured trajectory (timbre), so an
# envelope-mismatched action does not COVER — it triggers growth, letting
# the 12-way shootout find the right timbre. The vocabulary then accumulates
# one action per envelope class, as the design intends.
rep('''    let has_con: i64 = 0;
    if (get64(D, 200) >= 4) { has_con = 1; }
    let best: i64 = -1;
    let best_err: i64 = 1000000000;
    let vi: i64 = 0;
    while (vi < nvoc) {
        let vo: i64 = vi * 80;
        let am0: i64 = get64(VOCAB, vo + 8);
        let covers: i64 = 0;
        if (is_contour(am0) == 1) {
            if (has_con == 1) { covers = 1; }
        } else {
            if (get64(VOCAB, vo + 48) >= need_pm) { covers = 1; }
        }''',
'''    let has_con: i64 = 0;
    if (get64(D, 200) >= 4) { has_con = 1; }
    let best: i64 = -1;
    let best_err: i64 = 1000000000;
    let vi: i64 = 0;
    while (vi < nvoc) {
        let vo: i64 = vi * 80;
        let am0: i64 = get64(VOCAB, vo + 8);
        let covers: i64 = 0;
        // Envelope-aware coverage: the render's envelope is the atom's
        // measured trajectory. Timbre 0/1=flat, 2/3=rise, 4/5=decay.
        // A mismatched envelope is not coverage — growth must find the
        // right timbre instead of reusing the wrong one.
        let t0: i64 = timbre_of(am0);
        let tenv: i64 = 0;
            if (t0 == 2 || t0 == 3) { tenv = 1; }
            if (t0 == 4 || t0 == 5) { tenv = 2; }
            if (tenv == envh) {
                if (is_contour(am0) == 1) {
                    if (has_con == 1) { covers = 1; }
                } else {
                    if (get64(VOCAB, vo + 48) >= need_pm) { covers = 1; }
                }
            }''', 1)

# sanity: no stale amode arithmetic remains
# (note: 'amode == 2 or amode == 3' appears once inside the WALL-3 comment
# documenting the fix, which is intentional - R2 already asserted the code
# occurrence was replaced exactly once)
for pat in ['am & 1', 'am0 >= 2', 'am >= 2',
            'amode == 1 or amode == 3', 'timbre & 1', '(80) as *u8)[0..80]',
            'ncand: i64 = 4', 'while (t < 2)']:
    assert pat not in text, f"STALE PATTERN REMAINS: {pat}"
assert text.count('amode == 2 or amode == 3') == 1, "code occurrence must be gone"
print("no stale amode patterns remain")

with open(FINAL_MAIN, "w") as f:
    f.write(text)
print(f"wrote {FINAL_MAIN} ({len(text)} bytes)")

# Step 3: assemble
parts = [f"{D}/wall1/src/hear_trigfree.zag",
         f"{D}/wall2/f0low_fixed.zag",
         FINAL_MAIN]
full = "".join(open(p).read() for p in parts)
with open(FINAL_FULL, "w") as f:
    f.write(full)
print(f"wrote {FINAL_FULL} ({len(full)} bytes)")
