#!/usr/bin/env python3
"""Follow-up patch: chunk-aware write_wav for work/r2g/r2g.zag."""
P = "/home/hatch/workspace/tnn-lab/imagination_discovery/aud/continuity_round2/work/r2g/r2g.zag"
src = open(P).read()

def rep(old, new, n=1):
    global src
    c = src.count(old)
    assert c == n, f"expected {n}, found {c} for: {old[:70]!r}"
    src = src.replace(old, new)

rep("""fn write_wav(path:[]u8,m:[]u8,nsamp:i64)i32{
    let s:i64=0;
    let peak:i64=0;
    while(s<nsamp){
        let v:i64=get64(m,s*8);
        let a:i64=v;
        if(a<0){a=-a;}
        if(a>peak){peak=a;}
        s=s+1;
    }
    if(peak<1000){return -1;}
    // DC removal (mastering hygiene, A-NATIVE law): subtract the mean.
    let dc:i64=0;
    s=0;
    while(s<nsamp){
        dc=dc+get64(m,s*8);
        s=s+1;
    }
    dc=dc/nsamp;
    s=0;
    while(s<nsamp){
        put64(m,s*8,get64(m,s*8)-dc);
        s=s+1;
    }""",
"""fn write_wav(path:[]u8,m:[]u8,nsamp:i64)i32{
    let nch:i64=get64(m,8);
    let s:i64=0;
    let peak:i64=0;
    while(s<nsamp){
        let cb:[]u8=mchunk(m,s/CHSMP);
        let v:i64=get64(cb,(s-s/CHSMP*CHSMP)*8);
        let a:i64=v;
        if(a<0){a=-a;}
        if(a>peak){peak=a;}
        s=s+1;
    }
    if(peak<1000){return -1;}
    // DC removal (mastering hygiene, A-NATIVE law): subtract the mean.
    let dc:i64=0;
    s=0;
    while(s<nsamp){
        let cb:[]u8=mchunk(m,s/CHSMP);
        dc=dc+get64(cb,(s-s/CHSMP*CHSMP)*8);
        s=s+1;
    }
    dc=dc/nsamp;
    s=0;
    while(s<nsamp){
        let cb:[]u8=mchunk(m,s/CHSMP);
        let o:i64=(s-s/CHSMP*CHSMP)*8;
        put64(cb,o,get64(cb,o)-dc);
        s=s+1;
    }""")

rep("""    s=0;
    while(s<nsamp){
        let v:i64=get64(m,s*8);
        let x:f64=((v as f64)/16777216.0)*norm;""",
"""    s=0;
    while(s<nsamp){
        let cb:[]u8=mchunk(m,s/CHSMP);
        let v:i64=get64(cb,(s-s/CHSMP*CHSMP)*8);
        let x:f64=((v as f64)/16777216.0)*norm;""")

open(P, "w").write(src)
print("write_wav patch OK")
