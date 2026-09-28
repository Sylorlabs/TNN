#!/usr/bin/env python3
"""Patch work/r2g/r2g.zag (copy of frozen b_gamma/gamma.zag) for round-2 tests.
Every replacement asserts its expected occurrence count. The frozen source is
never touched."""
import sys

P = "/home/hatch/workspace/tnn-lab/imagination_discovery/aud/continuity_round2/work/r2g/r2g.zag"
src = open(P).read()

def rep(old, new, n=1):
    global src
    c = src.count(old)
    assert c == n, f"expected {n}, found {c} for: {old[:70]!r}"
    src = src.replace(old, new)

# E1: globals after PH1 const
rep("const PH1:i64 = 281474976710656;",
"""const PH1:i64 = 281474976710656;
const CHSMP:i64 = 1323000; // 30 s chunk: chunked mix (znc 2^25 slice limit)
let GSS:i64=0;    // r2: global deterministic seed offset (scene variants)
let GBMODE:i64=0; // r2: 0=standard bridges 1=extended-window control 2=event-only ablation
let GCG:i64=0;    // r2: 1=constant per-placement gain (bridge control)
let LGFD:i64=-1;  // r2: placement log fd (-1=off)""")

# E1b: decimal writers for the placement log (pattern from b_beta/assemble.zag)
rep("""fn w_all(fd:i64,b:[]u8)i64{""",
"""fn wdec(fd:i64,v:i64)void{
    let neg:i64=0;
    let x:i64=v;
    if(x<0){neg=1;x=-x;}
    let p:*u8=_zag_malloc(24) as *u8;
    if(p==null as *u8){return;}
    let buf:[]u8=p[0..24];
    let e:i64=23;
    if(x==0){buf[23]=48;e=22;}
    while(x>0 && e>=0){
        buf[e]=((x%10)+48) as u8;
        x=x/10;
        e=e-1;
    }
    if(neg==1 && e>=0){buf[e]=45;e=e-1;}
    let s:i64=e+1;
    _zag_raw_syscall(1,fd,(_zag_slice_ptr(buf) as i64)+s,24-s,0,0,0);
    _zag_free(_zag_slice_ptr(buf));
}
fn wch(fd:i64,c:u8)void{
    let p:*u8=_zag_malloc(1) as *u8;
    if(p==null as *u8){return;}
    let b:[]u8=p[0..1];
    b[0]=c;
    _zag_raw_syscall(1,fd,_zag_slice_ptr(b) as i64,1,0,0,0);
    _zag_free(_zag_slice_ptr(b));
}
fn parse_i64(s:[]u8)i64{
    let v:i64=0; let neg:i64=0; let i:i64=0;
    if(s.len>0 && s[0]==45){neg=1;i=1;}
    while(i<s.len){
        let c:i64=s[i] as i64;
        if(c>=48 && c<=57){v=v*10+(c-48);}
        i=i+1;
    }
    if(neg==1){v=-v;}
    return v;
}
fn w_all(fd:i64,b:[]u8)i64{""")

# E2: GSS inside h32
rep("""fn h32(s:i64,st:i64)i64{
    let z:i64=(s*2654435761+st*40503+1) & 4294967295;""",
"""fn h32(s:i64,st:i64)i64{
    let ss:i64=s+GSS;
    let z:i64=(ss*2654435761+st*40503+1) & 4294967295;""")

# E3: chunked mix_new + mchunk helper
rep("""fn mix_new(nsamp:i64)[]u8{
    let p:*u8=_zag_malloc(nsamp*8) as *u8;
    if(p==null as *u8){return "";}
    let m:[]u8=p[0..(nsamp*8)];
    let i:i64=0;
    while(i<nsamp*8){m[i]=0;i=i+1;}
    return m;
}""",
"""// chunked mix: table [magic, nchunks, nsamp, (bytelen,ptr)*].
// A single 300 s i64 arena (105 MB) exceeds the znc 2^25-byte slice limit,
// so the mix is striped in 30 s chunks; integer-add semantics unchanged.
fn mix_new(nsamp:i64)[]u8{
    let nch:i64=(nsamp+CHSMP-1)/CHSMP;
    let tp:*u8=_zag_malloc((3+2*nch)*8) as *u8;
    if(tp==null as *u8){return "";}
    let t:[]u8=tp[0..((3+2*nch)*8)];
    put64(t,0,0x4348554E4B5F4D4958);
    put64(t,8,nch);
    put64(t,16,nsamp);
    let c:i64=0;
    while(c<nch){
        let cs:i64=CHSMP;
        if(c==nch-1){cs=nsamp-c*CHSMP;}
        let cp:*u8=_zag_malloc(cs*8) as *u8;
        if(cp==null as *u8){return "";}
        let cb:[]u8=cp[0..(cs*8)];
        let i:i64=0;
        while(i<cs*8){cb[i]=0;i=i+1;}
        put64(t,24+c*16,cs*8);
        put64(t,32+c*16,cp as i64);
        c=c+1;
    }
    return t;
}
fn mchunk(m:[]u8,c:i64)[]u8{
    let p:i64=get64(m,32+c*16);
    let lb:i64=get64(m,24+c*16);
    return (p as *u8)[0..lb];
}""")

# E4: place() -> chunk-hoisted + placement log
rep("""fn place(h:[]u8,m:[]u8,nsamp:i64,gi:i64,start:i64,gain:f64,rev:i64)void{
    if(gi<0){return;}
    let ns:i64=g_nsamp(h,gi);
    let F:i64=88;
    if(F*2>ns){F=ns/4;}
    let s:i64=start;
    if(s<0){s=0;}
    let k:i64=0;
    while(k<ns){
        let at:i64=s+k;
        if(at>=nsamp){k=ns;}
        else{
            let v:i64=g_samp(h,gi,k,rev);
            let e:f64=1.0;
            if(k<F){e=sstep((k as f64)/(F as f64));}
            else{if(k>ns-1-F){e=sstep(((ns-1-k) as f64)/(F as f64));}}
            let add:i64=((v as f64)*gain*e*16777216.0/32768.0) as i64;
            let cur:i64=get64(m,at*8);
            let nv:i64=cur+add;
            if(nv>36028797018963968){nv=36028797018963968;}
            if(nv<-36028797018963968){nv=-36028797018963968;}
            put64(m,at*8,nv);
            k=k+1;
        }
    }
}""",
"""fn place(h:[]u8,m:[]u8,nsamp:i64,gi:i64,start:i64,gain:f64,rev:i64)void{
    if(gi<0){return;}
    if(LGFD>=0){
        wdec(LGFD,start);wch(LGFD,32);
        wdec(LGFD,g_nsamp(h,gi));wch(LGFD,32);
        wdec(LGFD,gi);wch(LGFD,10);
    }
    let ns:i64=g_nsamp(h,gi);
    let F:i64=88;
    if(F*2>ns){F=ns/4;}
    let s:i64=start;
    if(s<0){s=0;}
    let k:i64=0;
    let curc:i64=-1;
    let cb:[]u8="";
    while(k<ns){
        let at:i64=s+k;
        if(at>=nsamp){k=ns;}
        else{
            let v:i64=g_samp(h,gi,k,rev);
            let e:f64=1.0;
            if(k<F){e=sstep((k as f64)/(F as f64));}
            else{if(k>ns-1-F){e=sstep(((ns-1-k) as f64)/(F as f64));}}
            let add:i64=((v as f64)*gain*e*16777216.0/32768.0) as i64;
            let c:i64=at/CHSMP;
            if(c!=curc){curc=c;cb=mchunk(m,c);}
            let o:i64=(at-c*CHSMP)*8;
            let cur:i64=get64(cb,o);
            let nv:i64=cur+add;
            if(nv>36028797018963968){nv=36028797018963968;}
            if(nv<-36028797018963968){nv=-36028797018963968;}
            put64(cb,o,nv);
            k=k+1;
        }
    }
}""")

# E5: morph() -> chunk-hoisted (distinguished by its add expression)
rep("""            let add:i64=(v*gain*e*16777216.0/32768.0) as i64;
            let cur:i64=get64(m,at*8);
            let nv:i64=cur+add;
            if(nv>36028797018963968){nv=36028797018963968;}
            if(nv<-36028797018963968){nv=-36028797018963968;}
            put64(m,at*8,nv);""",
"""            let add:i64=(v*gain*e*16777216.0/32768.0) as i64;
            let c:i64=at/CHSMP;
            if(c!=curc){curc=c;cb=mchunk(m,c);}
            let o:i64=(at-c*CHSMP)*8;
            let cur:i64=get64(cb,o);
            let nv:i64=cur+add;
            if(nv>36028797018963968){nv=36028797018963968;}
            if(nv<-36028797018963968){nv=-36028797018963968;}
            put64(cb,o,nv);""")

# E5b: morph() needs the hoist locals declared
rep("""    let s:i64=start;
    if(s<0){s=0;}
    let k:i64=0;
    while(k<n){
        let at:i64=s+k;
        if(at>=nsamp){k=n;}""",
"""    let s:i64=start;
    if(s<0){s=0;}
    let k:i64=0;
    let curc:i64=-1;
    let cb:[]u8="";
    while(k<n){
        let at:i64=s+k;
        if(at>=nsamp){k=n;}""")

# E6a: scatter constant-gain flag
rep("""            place(h,m,nsamp,gi,(t*SRF) as i64,g0*(0.7+0.6*h01(salt+41,q)),0);""",
"""            let gf2:f64=0.7+0.6*h01(salt+41,q);
            if(GCG==1){gf2=1.0;}
            place(h,m,nsamp,gi,(t*SRF) as i64,g0*gf2,0);""")

# E6b: run_feet constant-gain flag
rep("""            let g:f64=g0*(0.85+0.3*h01(salt+13,q));""",
"""            let g:f64=g0*(0.85+0.3*h01(salt+13,q));
            if(GCG==1){g=g0;}""")

# E7: bridge_world mode dispatch (GBMODE 1=extended control, 2=ablation)
rep("""fn bridge_world(h:[]u8,m:[]u8,nsamp:i64,t0:f64,t1:f64,wt1:f64,salt:i64)void{
    let c_thump:i64=cid_by_name(h,"thump");
    let c_wind:i64=cid_by_name(h,"wind");
    let c_laugh:i64=cid_by_name(h,"laugh");
    let c_wash:i64=cid_by_name(h,"wash");
    // sustained world texture: long wash grains overlapping at 0.9 s
    // spacing -- a continuous low presence, scored content, never a fade.
    // wt1 caps the long (3 s) grains so the v2 natural ending (quiet from
    // 28.7 s) is preserved in the final bridge.
    scatter(h,m,nsamp,c_wash,t0,wt1,0.9,salt+3,0.20);
    scatter(h,m,nsamp,c_wind,t0,wt1,1.4,salt+1,0.055);  // breath / air
    run_feet(h,m,nsamp,c_thump,t0,t1,1.2,salt,0.10);    // shuffling feet
    scatter(h,m,nsamp,c_laugh,t0,t1,0.9,salt+2,0.09);   // distant play
}""",
"""// G3 ablation: plain event-only block over the identical [t0,t1] span --
// ordinary laugh trains + feet with the bridge's salt base; no wash/wind
// world texture. Deterministic.
fn bridge_abl(h:[]u8,m:[]u8,nsamp:i64,t0:f64,t1:f64,salt:i64)void{
    let c_thump:i64=cid_by_name(h,"thump");
    let c_laugh:i64=cid_by_name(h,"laugh");
    let c_shout:i64=cid_by_name(h,"shout");
    let dur:f64=t1-t0;
    let np:i64=(dur/0.19) as i64;
    if(np<3){np=3;}
    laugh_train(h,m,nsamp,c_laugh,salt%3,t0+0.1,np,0.19,salt+11,0.42);
    run_feet(h,m,nsamp,c_thump,t0,t1,2.6,salt+12,0.30);
    let gi:i64=g_pick(h,c_shout,salt%3,salt+13,0,-1);
    place(h,m,nsamp,gi,((t0+dur*0.55)*SRF) as i64,0.36,0);
}
// world-first bridge for the ocean corpus (G1): wash + rumble + distant
// swell + sparse crack. No kids voices anywhere (corpus honesty).
fn bridge_ocean(h:[]u8,m:[]u8,nsamp:i64,t0:f64,t1:f64,wt1:f64,salt:i64)void{
    if(GBMODE==2){bridge_ocean_abl(h,m,nsamp,t0,t1,salt);return;}
    let c_wash:i64=cid_by_name(h,"wash");
    let c_rumble:i64=cid_by_name(h,"rumble");
    let c_swell:i64=cid_by_name(h,"swell");
    let c_crack:i64=cid_by_name(h,"crack");
    let e0:f64=t0; let e1:f64=t1; let ew:f64=wt1;
    if(GBMODE==1){
        e0=t0-2.0; if(e0<0.0){e0=0.0;}
        e1=t1+2.0; if(e1>30.0){e1=30.0;}
        ew=wt1+2.0; if(ew>30.0){ew=30.0;}
        GCG=1;
    }
    scatter(h,m,nsamp,c_wash,e0,ew,1.1,salt+3,0.16);
    scatter(h,m,nsamp,c_rumble,e0,ew,2.2,salt+1,0.10);
    scatter(h,m,nsamp,c_swell,e0,e1,3.5,salt,0.30);
    scatter(h,m,nsamp,c_crack,e0,e1,1.7,salt+2,0.12);
    GCG=0;
}
fn bridge_ocean_abl(h:[]u8,m:[]u8,nsamp:i64,t0:f64,t1:f64,salt:i64)void{
    let c_swell:i64=cid_by_name(h,"swell");
    let c_crack:i64=cid_by_name(h,"crack");
    scatter(h,m,nsamp,c_swell,t0,t1,1.4,salt+21,0.42);
    scatter(h,m,nsamp,c_crack,t0,t1,0.5,salt+22,0.30);
}
fn bridge_world(h:[]u8,m:[]u8,nsamp:i64,t0:f64,t1:f64,wt1:f64,salt:i64)void{
    if(GBMODE==2){bridge_abl(h,m,nsamp,t0,t1,salt);return;}
    let c_thump:i64=cid_by_name(h,"thump");
    let c_wind:i64=cid_by_name(h,"wind");
    let c_laugh:i64=cid_by_name(h,"laugh");
    let c_wash:i64=cid_by_name(h,"wash");
    // sustained world texture: long wash grains overlapping at 0.9 s
    // spacing -- a continuous low presence, scored content, never a fade.
    // wt1 caps the long (3 s) grains so the v2 natural ending (quiet from
    // 28.7 s) is preserved in the final bridge.
    // GBMODE 1 (H2 control): same captured material scored 2 s before the
    // nominal insertion through 2 s after the nominal exit, gain trajectory
    // held constant (GCG), no insertion/removal boundary.
    let e0:f64=t0; let e1:f64=t1; let ew:f64=wt1;
    if(GBMODE==1){
        e0=t0-2.0; if(e0<0.0){e0=0.0;}
        e1=t1+2.0; if(e1>28.0){e1=28.0;}
        ew=wt1+2.0; if(ew>28.0){ew=28.0;}
        GCG=1;
    }
    scatter(h,m,nsamp,c_wash,e0,ew,0.9,salt+3,0.20);
    scatter(h,m,nsamp,c_wind,e0,ew,1.4,salt+1,0.055);  // breath / air
    run_feet(h,m,nsamp,c_thump,e0,e1,1.2,salt,0.10);    // shuffling feet
    scatter(h,m,nsamp,c_laugh,e0,e1,0.9,salt+2,0.09);   // distant play
    GCG=0;
}""")

open(P, "w").write(src)
print("patch OK")
