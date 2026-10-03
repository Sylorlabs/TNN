#!/usr/bin/env python3
"""Insert stderr reasoning-trace hooks into dialogue.zag -> dialogue_trace.zag.
Traces go to fd 2 via raw syscall; stdout (answers) must stay byte-identical."""
import sys

SRC = "/home/hatch/workspace/dialogue_r4fix/docs/lab/dialogue/round4/dialogue.zag"
DST = "/home/hatch/workspace/dialogue_r4fix/docs/lab/dialogue/round4/dialogue_trace.zag"

HELPERS = '''fn tr(s:[]u8)void {
    _zag_raw_syscall(1,2,(_zag_slice_ptr(s) as i64),(s.len as i64),0,0,0);
    return;
}
fn trn(v:i64)void {
    let tb:[]u8=nio_alloc(64);
    let tnl:i32=i64str(v,tb);
    _zag_raw_syscall(1,2,(_zag_slice_ptr(tb) as i64),(tnl as i64),0,0,0);
    nio_free(tb);
    return;
}
fn trt(t:i32)void {
    tr("TR turn="); trn(t as i64); tr(" ");
    return;
}
fn tre(eid:i32,gnames:[]u8,ge:[]u8)void {
    if(eid<0){ tr("?"); return; }
    let tno:i32=g32(ge,8+eid*16) as i32;
    let tnl2:i32=g32(ge,8+eid*16+4) as i32;
    let tnm:[]u8=gnames[tno..tno+tnl2];
    tr(tnm);
    return;
}
'''

# (anchor, insertion) — insertion goes on the lines AFTER the anchor line.
HOOKS = [
    ("fn prl(s:[]u8)void { _zag_println(s); return; }", HELPERS),
    ("    let ut:i32=utter_type(ubuf,uo,ul);",
     '    trt(turn_no); tr("ut="); trn(ut as i64); tr("\\n");'),
    ("    if(ut>0){",
     '        trt(turn_no); tr("branch=utter-type\\n");'),
    ("    if(pkind==0 && pans>=0 && is_correction(ubuf,uo,ul)==1){",
     '        trt(turn_no); tr("branch=correction\\n");'),
    ("    if(is_resume(ubuf,uo,ul)==1){",
     '        trt(turn_no); tr("branch=resume\\n");'),
    ("    if(do_compose(ubuf,uo,ul,sal,pv,fm,fea,ftl,ftx,gnames,ge,gord,eout,eout2,bout,resp,nbuf,turn_no)==1){",
     '        trt(turn_no); tr("branch=compose\\n");'),
    ("    if(pans>=0 && is_challenge(ubuf,uo,ul)==1){",
     '        trt(turn_no); tr("branch=challenge\\n");'),
    ("        do_defense(resp,fm,ftx,nbuf,cfid,conf);",
     '        trt(turn_no); tr("challenge cfid="); trn(cfid as i64); tr(" conf="); trn(conf as i64); tr("\\n");'),
    ("    if(prov_match(ubuf,uo,ul,abuf)==1){",
     '        trt(turn_no); tr("branch=provenance\\n");'),
    ("            let conf:i32=uclaim_check(uc,subj,rel,val,turn_no,cturn,coval);",
     '            trt(turn_no); tr("branch=assertion subj="); tre(subj,gnames,ge); tr(" rel="); trn(rel as i64); tr(" val="); trn(val as i64); tr(" conf="); trn(conf as i64); tr("\\n");'),
    ("    let wd:i32=withhold_check(ubuf,uo,ul,qbuf,ql3,kid,plen2,keya,frko,frkl,fea,frfeo,frfen,eout,ne4,bout,bn,vbytes,vent,tmp,fout);",
     '    trt(turn_no); tr("branch=default fid="); trn(fid3 as i64); tr(" withhold="); trn(wd as i64); tr("\\n");'),
    ("        if(df<0){ df=0-df; }",
     '        tr("TR f3 ddim="); trn(ddim as i64); tr(" d1="); tre(d1,gnames,ge); tr(" v1="); trn(v1 as i64); tr(" d2="); tre(d2,gnames,ge); tr(" v2="); trn(v2 as i64); tr(" diff="); trn(df); tr("\\n");'),
    ("        if(ddim==1){ rput(resp,\" meters\",0,7); }",
     '        tr("TR f3 unit="); if(ddim==1){ tr("meters"); } if(ddim==2){ tr("years"); } tr("\\n");'),
    ("    if(v1<0 || v2<0){ return 0; }\n    // --- answer ---",
     '    tr("TR compare e1="); tre(e1,gnames,ge); tr(" v1="); trn(v1 as i64); tr(" e2="); tre(e2,gnames,ge); tr(" v2="); trn(v2 as i64); tr(" tall="); trn(tall as i64); tr(" dmin="); trn(dmin as i64); tr("\\n");\n    // --- answer ---'),
]

# (old, new) — whole-function replacements for the trace-note stubs.
REPLACEMENTS = [
    ("fn tr_method_note(mfid:i32)void {\n    return;\n}",
     'fn tr_method_note(mfid:i32)void {\n    tr("TR method="); trn(mfid as i64); tr("\\n");\n    return;\n}'),
    ("fn tr_withhold_note(wh:i32)void {\n    return;\n}",
     'fn tr_withhold_note(wh:i32)void {\n    tr("TR correct-withhold="); trn(wh as i64); tr("\\n");\n    return;\n}'),
    ("fn tr_predmm_note(pm:i32)void {\n    return;\n}",
     'fn tr_predmm_note(pm:i32)void {\n    tr("TR pred-mismatch="); trn(pm as i64); tr("\\n");\n    return;\n}'),
    ("fn tr_correct_shape_note(shaped:i32)void {\n    return;\n}",
     'fn tr_correct_shape_note(shaped:i32)void {\n    tr("TR correct-shaped="); trn(shaped as i64); tr("\\n");\n    return;\n}'),
    ("fn tr_joke_note(se:i32,te:i32,sv:i64,tv:i64)void {\n    return;\n}",
     'fn tr_joke_note(se:i32,te:i32,sv:i64,tv:i64)void {\n    tr("TR joke pair se="); trn(se as i64); tr(" te="); trn(te as i64); tr(" sv="); trn(sv); tr(" tv="); trn(tv); tr("\\n");\n    return;\n}'),
]

src = open(SRC).read()
for anchor, ins in HOOKS:
    n = src.count(anchor)
    if n != 1:
        print(f"FATAL: hook anchor {n}x: {anchor[:70]}")
        sys.exit(1)
    src = src.replace(anchor, anchor + "\n" + ins, 1)
for old, new in REPLACEMENTS:
    n = src.count(old)
    if n != 1:
        print(f"FATAL: replacement anchor {n}x: {old[:70]}")
        sys.exit(1)
    src = src.replace(old, new, 1)
open(DST, "w").write(src)
print("ok, hooks inserted:", len(HOOKS), "replacements:", len(REPLACEMENTS))
