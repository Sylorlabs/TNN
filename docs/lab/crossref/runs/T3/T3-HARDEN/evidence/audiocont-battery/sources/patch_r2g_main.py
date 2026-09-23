#!/usr/bin/env python3
"""Second-stage patch for work/r2g/r2g.zag: insert r2_scores.zag before main,
replace main() with the extended argv version."""
import sys

P = "/home/hatch/workspace/tnn-lab/imagination_discovery/aud/continuity_round2/work/r2g/r2g.zag"
S = "/home/hatch/workspace/tnn-lab/imagination_discovery/aud/continuity_round2/work/r2_scores.zag"
src = open(P).read()
scores = open(S).read()

def rep(old, new, n=1):
    global src
    c = src.count(old)
    assert c == n, f"expected {n}, found {c} for: {old[:70]!r}"
    src = src.replace(old, new)

# insert new scores before main
rep("fn main()i32{", scores + "\nfn main()i32{", n=1)

old_main = """fn main()i32{
    let a1:[]u8=_zag_arg(1);
    let subj:i32=0;
    if(_zag_strcmp(a1,"kids")==1){subj=1;}
    if(_zag_strcmp(a1,"planet")==1){subj=2;}
    if(_zag_strcmp(a1,"ocean")==1){subj=3;}
    if(_zag_strcmp(a1,"monster")==1){subj=4;}
    if(subj==0){return 90;}
    let a2:[]u8=_zag_arg(2);
    let pkp:[]u8="study_out/gamma.grpk";
    if(a2.len>0){pkp=a2;}
    let a3:[]u8=_zag_arg(3);
    let outp:[]u8="out.wav";
    if(a3.len>0){outp=a3;}
    let h:[]u8=pack_load(pkp);
    if(h.len==0){return 91;}
    let nsamp:i64=1323000;
    if(subj==2){nsamp=926100;}
    let m:[]u8=mix_new(nsamp);
    if(m.len==0){return 92;}
    if(subj==1){score_kids(h,m,nsamp);}
    else{if(subj==2){score_planet(h,m,nsamp);}
    else{if(subj==3){score_ocean(h,m,nsamp);}
    else{score_monster(h,m,nsamp);}}}
    let rc:i32=write_wav(outp,m,nsamp);
    return rc;
}"""

new_main = """fn main()i32{
    let a1:[]u8=_zag_arg(1);
    let subj:i32=0;
    if(_zag_strcmp(a1,"kids")==1){subj=1;}
    if(_zag_strcmp(a1,"planet")==1){subj=2;}
    if(_zag_strcmp(a1,"ocean")==1){subj=3;}
    if(_zag_strcmp(a1,"monster")==1){subj=4;}
    if(_zag_strcmp(a1,"oceanwf")==1){subj=5;}
    if(_zag_strcmp(a1,"long180")==1){subj=6;}
    if(_zag_strcmp(a1,"h3")==1){subj=7;}
    if(subj==0){return 90;}
    let a2:[]u8=_zag_arg(2);
    let pkp:[]u8="study_out/gamma.grpk";
    if(a2.len>0){pkp=a2;}
    let a3:[]u8=_zag_arg(3);
    let outp:[]u8="out.wav";
    if(a3.len>0){outp=a3;}
    let a4:[]u8=_zag_arg(4);
    if(a4.len>0){GSS=parse_i64(a4);}
    let a5:[]u8=_zag_arg(5);
    if(a5.len>0){GBMODE=parse_i64(a5);}
    let a6:[]u8=_zag_arg(6);
    if(a6.len>0){
        let cs6:[]u8=cstr(a6);
        LGFD=_zag_raw_syscall(2,(_zag_slice_ptr(cs6) as i64),577,438,0,0,0);
        _zag_free(_zag_slice_ptr(cs6));
    }
    let h:[]u8=pack_load(pkp);
    if(h.len==0){return 91;}
    let nsamp:i64=1323000;
    if(subj==2){nsamp=926100;}
    if(subj==6){nsamp=7938000;}
    if(subj==7){nsamp=13230000;}
    let m:[]u8=mix_new(nsamp);
    if(m.len==0){return 92;}
    if(subj==1){score_kids(h,m,nsamp);}
    else{if(subj==2){score_planet(h,m,nsamp);}
    else{if(subj==3){score_ocean(h,m,nsamp);}
    else{if(subj==4){score_monster(h,m,nsamp);}
    else{if(subj==5){score_ocean_wf(h,m,nsamp);}
    else{if(subj==6){score_long180(h,m,nsamp);}
    else{
        let a7:[]u8=_zag_arg(7);
        let cls:i64=0;
        if(a7.len>0){cls=parse_i64(a7);}
        let a8:[]u8=_zag_arg(8);
        let idx:i64=0;
        if(a8.len>0){idx=parse_i64(a8);}
        let a9:[]u8=_zag_arg(9);
        let bm:i64=0;
        if(a9.len>0){bm=parse_i64(a9);}
        score_h3(h,m,nsamp,cls,idx,bm);
    }}}}}}
    let rc:i32=write_wav(outp,m,nsamp);
    if(LGFD>=0){_zag_raw_syscall(3,LGFD,0,0,0,0,0);}
    return rc;
}"""
rep(old_main, new_main, n=1)

open(P, "w").write(src)
print("main patch OK")
