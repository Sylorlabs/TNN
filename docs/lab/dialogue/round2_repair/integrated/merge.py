#!/usr/bin/env python3
"""Round-2 integration merge (PREREG_INT.md).

Merges the five repair families into one dialogue.zag, copying each family's
code from its frozen fork verbatim except for the prereg-frozen pv-slot
remaps:
  F1 pair  32/36 -> 40/44   (persists across unrelated turns; needed for R2T7)
  F3 pair  32/36 -> 48/52   (expires after one turn)
  F3 dim   48    -> 56      (F3-style write-only)
  F3 turn  52    -> 60
  F4 prevbn stays at 32.

Pipeline (do_turn): F5 step-0 router -> correction -> resume -> F4
challenge/provenance -> composition (F3 difference FIRST, then F1
do_compare, then did-write/birth-year) -> assertion -> default step 5
with the F2 gate between retrieve() and emit_fact().

F3-before-F1 is principled, not a hack: an explicit quantitative demand
("how much", "how many years between", "difference in ...") is answered by
the difference engine; do_compare answers qualitative comparisons only and
cannot emit a number. Letting do_compare answer "how much older is X than
Y?" would emit a winner sentence -- a wrong-shape answer of the class this
repair fixes (cf. F3 H8: "how much older is herman melville than charles
darwin?" must be 10, not "charles darwin was born first.").
"""
import re, sys

LAB = '/home/hatch/workspace/tnn-lab'
R2  = LAB + '/dialogue/round2_repair'
CANON = LAB + '/dialogue/dialogue.zag'

def lines(p):
    return open(p).read().split('\n')

def rng(p, a, b):
    """1-based inclusive line range."""
    return '\n'.join(lines(p)[a-1:b])

src = open(CANON).read()
n_edits = 0

def sub_once(old, new, tag):
    global src, n_edits
    n = src.count(old)
    if n != 1:
        raise SystemExit(f'ANCHOR FAIL [{tag}]: found {n} times')
    src = src.replace(old, new, 1)
    n_edits += 1

# ---------- 1. F3 comparative-adjective mappings in irregular_norm ----------
F3 = R2 + '/f3_arithmetic/dialogue.zag'
f3_cmp = rng(F3, 334, 348)   # comment + 7 closed-list mappings
old_win = '    if(beq(b,0,len,"winning")==1){ copy_bytes(b,0,"win",0,3); return 3; }\n    return len;\n}'
sub_once(old_win,
         '    if(beq(b,0,len,"winning")==1){ copy_bytes(b,0,"win",0,3); return 3; }\n'
         + f3_cmp + '\n    return len;\n}',
         'irregular_norm extension')

# ---------- 2. F4 stopword extension (whole is_stop replaced) ----------
F4 = R2 + '/f4_defend/dialogue.zag'
start = src.index('fn is_stop(sb:[]u8,so:i32,sl:i32)i32 {')
end = src.index('\n}\n', start) + 3
old_stop = src[start:end]
new_stop = rng(F4, 484, 573)   # F4's complete is_stop (diff showed only the added tail)
sub_once(old_stop, new_stop, 'is_stop replacement')

# ---------- 3. helper blocks, inserted before fn do_compose ----------
F5 = R2 + '/f5_router/dialogue.zag'
F1 = R2 + '/f1_compare/dialogue.zag'
F2 = R2 + '/f2_withhold/dialogue.zag'

f4_helpers = rng(F4, 1500, 1618)   # is_challenge..do_provenance
f5_helpers = rng(F5, 1454, 1520) + '\n\n' + rng(F5, 1604, 1647)   # tok_has..mem_ord + mem_answer
# (canonical push_ents..hist_add sit between at 1522-1603; mem_answer's own comment at 1604)
f1_helpers = rng(F1, 1301, 1548)   # do_compare engine
f3_helpers = rng(F3, 1316, 1420)   # diff_dim..ent_year_val (F3 do_compose starts at 1421)
f2_helpers = rng(F2, 1537, 1762)   # withhold gate suite (withhold_check closes at 1761)

# pv-slot remaps (prereg-frozen). F3 first 52->60, then 32->48, 36->52,
# so the 36->52 write is not clobbered by the 52->60 pass.
def remap_f1(t):
    t = re.sub(r'pv,32\b', 'pv,40', t)
    t = re.sub(r'pv,36\b', 'pv,44', t)
    t = t.replace('the compared pair at pv+32/36', 'the compared pair at pv+40/44')
    assert 'pv,32' not in re.sub(r'pv,32\d', '', t), 'F1 remap missed a pv,32'
    return t

def remap_f3(t):
    t = re.sub(r'pv,52\b', 'pv,60', t)
    t = re.sub(r'pv,32\b', 'pv,48', t)
    t = re.sub(r'pv,36\b', 'pv,52', t)
    return t

f1_helpers = remap_f1(f1_helpers)
f3_helpers = remap_f3(f3_helpers)

blocks = ('// ================= INTEGRATED round-2 repair =================\n'
          '// Five families merged per PREREG_INT.md. Slot map:\n'
          '//   prevbn@32 (F4) | F1 compared pair@40/44 | F3 carry pair@48/52\n'
          '//   F3 dim@56 (write-only) | F3 carry turn@60\n'
          '// =================================================================\n\n'
          + f4_helpers + '\n\n' + f5_helpers + '\n\n'
          + f1_helpers + '\n\n' + f3_helpers + '\n\n' + f2_helpers + '\n\n')

sub_once('fn do_compose(ubuf:[]u8,uo:i32,ul:i32,fm:[]u8',
         blocks + 'fn do_compose(ubuf:[]u8,uo:i32,ul:i32,fm:[]u8',
         'helper block insert')

# ---------- 4. do_compose: REPLACE the two old prefix branches ----------
# (old_sig through the end of the "which is taller" branch) with the merged
# body: F3 difference branch FIRST, then the F1 engine + F3 carry write.
f3_branch = rng(F3, 1481, 1528)          # ddim branch through closing }
f3_branch = remap_f3(f3_branch)
old_sig = ('fn do_compose(ubuf:[]u8,uo:i32,ul:i32,fm:[]u8,fea:[]u8,ftl:[]u8,ftx:[]u8,'
           'gnames:[]u8,ge:[]u8,gord:[]u8,eout:[]u8,eout2:[]u8,resp:[]u8,nbuf:[]u8)i32 {')
new_sig = ('fn do_compose(ubuf:[]u8,uo:i32,ul:i32,sal:[]u8,pv:[]u8,fm:[]u8,fea:[]u8,ftl:[]u8,ftx:[]u8,'
           'gnames:[]u8,ge:[]u8,gord:[]u8,eout:[]u8,eout2:[]u8,bout:[]u8,resp:[]u8,nbuf:[]u8,turn_no:i32)i32 {')
merged_body = (
    f3_branch + '\n'
    '    // F1-COMPARE: general comparison engine (replaces the two frozen\n'
    '    // string-prefix branches above; did-write and birth-year below unchanged).\n'
    '    if(do_compare(ubuf,uo,ul,sal,pv,fm,fea,ftl,gnames,ge,gord,eout,eout2,bout,resp)==1){\n'
    '        // F3-ARITHMETIC carry (merged): the just-compared pair is carried\n'
    '        // for an immediate follow-up difference question. In F3\'s fork this\n'
    '        // write lived inside the old "which is taller" branch; F1\'s engine\n'
    '        // replaces that branch, so the carry is written here after ANY\n'
    '        // successful comparison. Slots per PREREG_INT: pair@48/52, dim@56\n'
    '        // (write-only, as in F3), turn@60; the F1 pair lives at 40/44.\n'
    '        p32(pv,48,g32(pv,40) as i32); p32(pv,52,g32(pv,44) as i32);\n'
    '        p32(pv,56,1); p32(pv,60,turn_no);\n'
    '        return 1;\n'
    '    }\n'
)
# the old "which is taller" branch ends with this (8-space indent, own lines);
# do_compare's " is taller." is inside one-line ifs, so this anchor is unique.
old_tail = '        rput(resp," is taller.",0,11);\n        return 1;\n    }\n'
assert src.count(old_sig + '\n') == 1, 'do_compose sig anchor'
assert src.count(old_tail) == 1, 'old taller-branch tail anchor'
si = src.index(old_sig + '\n')
ei = src.index(old_tail) + len(old_tail)
src = src[:si] + new_sig + '\n' + merged_body + src[ei:]
n_edits += 1

# ---------- 5a. do_turn signature: add fout (F2) ----------
old_dtsig_tail = 'qbuf:[]u8,abuf:[]u8,nbuf:[]u8,novelf:[]u8,last_fid:i32)i32 {'
sub_once(old_dtsig_tail,
         'qbuf:[]u8,abuf:[]u8,nbuf:[]u8,novelf:[]u8,last_fid:i32,fout:[]u8)i32 {',
         'do_turn signature')

# ---------- 5b. F5 step-0 utterance-type dispatch ----------
f5_step0 = rng(F5, 1655, 1680)   # ut-dispatch if closes at 1680
sub_once('    let pkind:i32=g32(pv,28) as i32;\n    let pans:i32=g32(pv,0) as i32;\n',
         '    let pkind:i32=g32(pv,28) as i32;\n    let pans:i32=g32(pv,0) as i32;\n' + f5_step0 + '\n',
         'F5 step-0 dispatch')

# ---------- 5c. F4 correction-block insert ----------
sub_once('        p32(pv,28,0);\n        if(pe>=0 && pe!=top_peek(top)){ top_push(top,pe); }\n        return fid;',
         '        p32(pv,28,0);\n        if(pe>=0 && pe!=top_peek(top)){ top_push(top,pe); }\n        p32(pv,32,0);\n        return fid;',
         'F4 correction insert')

# ---------- 5d. F4 resume insert ----------
sub_once('        p32(pv,0,fid2); p32(pv,4,te); p32(pv,8,te); p32(pv,28,1);',
         '        p32(pv,0,fid2); p32(pv,4,te); p32(pv,8,te); p32(pv,28,1);\n        p32(pv,32,0);',
         'F4 resume insert')

# ---------- 5e. F4 challenge/provenance dispatch (after resume, before composition) ----------
f4_dispatch = rng(F4, 1794, 1837)   # prov_match if closes at 1837
sub_once('    // ---- 4. user assertion / contradiction ----',
         f4_dispatch + '\n    // ---- 4. user assertion / contradiction ----',
         'F4 dispatch')

# ---------- 5f. F4 compose-guard insert ----------
sub_once('        p32(pv,4,pe2); p32(pv,8,pe2); p32(pv,28,1);\n        p32(novelf,0,novelty_ok(resp,fm,ftl,hist,histb));',
         '        p32(pv,4,pe2); p32(pv,8,pe2); p32(pv,28,1);\n'
         '        // F4-DEFEND: a composed yes./no. is not a defendable retrieved fact;\n'
         '        // it must not become prevbn\'s fact.\n'
         '        p32(pv,0,-1);\n'
         '        p32(pv,32,0);\n'
         '        p32(novelf,0,novelty_ok(resp,fm,ftl,hist,histb));',
         'F4 compose guard')

# ---------- 5g. F4 ellipsis gate ----------
sub_once('    if(use_ellip==0 && ne4==0 && bn==0){',
         '    // F4-DEFEND: ellipsis (carry the previous question\'s shape with the new\n'
         '    // entity) is only valid when the previous turn actually resolved a query.\n'
         '    if(use_ellip==0 && ne4==0 && bn==0 && (g32(pv,32) as i32)<=0){',
         'F4 ellipsis gate')

# ---------- 5h. F4 assertion-block insert ----------
sub_once('            p32(pv,0,-1); p32(pv,4,subj); p32(pv,8,subj); p32(pv,28,1);',
         '            p32(pv,0,-1); p32(pv,4,subj); p32(pv,8,subj); p32(pv,28,1);\n'
         '            p32(pv,32,0);',
         'F4 assertion insert')

# ---------- 5i. F4 end-of-step-5 insert ----------
sub_once('    p32(pv,0,fid3); p32(pv,4,pe3); p32(pv,8,pe3); p32(pv,28,0);',
         '    p32(pv,0,fid3); p32(pv,4,pe3); p32(pv,8,pe3); p32(pv,28,0);\n    p32(pv,32,bn);',
         'F4 step-5 insert')

# ---------- 5j. F2 withhold gate between retrieve() and emit_fact() ----------
# NOTE: F2's block at 1965 starts with its own `let fid3:i32=retrieve(...)`;
# the merge anchor already has that line, so extract from 1966 to avoid a
# duplicate retrieve() call (which broke retrieval ranking via side effects).
f2_gate = rng(F2, 1966, 2005)   # comment through decline block's closing }
sub_once('    let fid3:i32=retrieve(fm,keya,kid,plen2,-1,-1,fea,last_fid);\n    emit_fact(resp,fm,ftx,fid3);',
         '    let fid3:i32=retrieve(fm,keya,kid,plen2,-1,-1,fea,last_fid);\n'
         + f2_gate + '\n    emit_fact(resp,fm,ftx,fid3);',
         'F2 gate')

# ---------- 5k. do_compose call site inside do_turn ----------
sub_once('    if(do_compose(ubuf,uo,ul,fm,fea,ftl,ftx,gnames,ge,gord,eout,eout2,resp,nbuf)==1){',
         '    if(do_compose(ubuf,uo,ul,sal,pv,fm,fea,ftl,ftx,gnames,ge,gord,eout,eout2,bout,resp,nbuf,turn_no)==1){',
         'do_compose call site')

# ---------- 5l. pv layout comment documents the new slots ----------
sub_once('// --- pv layout: ans@0 eid@4 peid@8 qraw_off@12 qraw_len@16 q_off@20 q_len@24 kind@28 ---',
         '// --- pv layout: ans@0 eid@4 peid@8 qraw_off@12 qraw_len@16 q_off@20 q_len@24 kind@28\n'
         '//           prevbn@32 (F4-DEFEND: bound-pronoun count of previous turn\'s\n'
         '//           resolved query; gates step-5 ellipsis) |\n'
         '//           F1 compared pair@40/44 (persists) | F3 carry pair@48/52\n'
         '//           (one-turn) dim@56 (write-only) turn@60 ---',
         'pv layout comment')

# ---------- 6. main: fout alloc + do_turn call site ----------
sub_once('    let novelf:[]u8=nio_alloc(8);\n    let spass:[]u8=nio_alloc(64);',
         '    let novelf:[]u8=nio_alloc(8);\n    let fout:[]u8=nio_alloc(512);\n    let spass:[]u8=nio_alloc(64);',
         'fout alloc')
sub_once('qbuf,abuf,nbuf,novelf,last_fid);',
         'qbuf,abuf,nbuf,novelf,last_fid,fout);',
         'do_turn call site')

out = LAB + '/dialogue/round2_repair/integrated/dialogue.zag'
open(out, 'w').write(src)
print(f'OK: {n_edits} edits applied -> {out}')
print(f'lines: {len(src.split(chr(10)))}')
