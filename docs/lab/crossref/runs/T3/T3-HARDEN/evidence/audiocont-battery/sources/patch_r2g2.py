#!/usr/bin/env python3
"""Patch work/r2g/r2g.zag (fresh copy of frozen b_gamma/gamma.zag) for round 2.

Design (no mutable globals -- znc rejects them):
- mix table carries runtime state: [0]=magic,[8]=nchunks,[16]=nsamp,
  [24]=logfd,[32]=seedoff,[40]=gbmode,[48]=constgain,
  [56+c*16]=chunk bytelen,[64+c*16]=chunk ptr.
- g_pick(h,m,...) adds get64(m,32) to its salt: 30 deterministic variants.
- bridge_world/bridge_ocean dispatch on get64(m,40); control mode sets the
  constgain flag slot while scoring the bridge.
- place() appends "start ns gi\\n" to get64(m,24) when >= 0.
Every replacement asserts its occurrence count. Frozen source untouched."""
import sys

P = "/home/hatch/workspace/tnn-lab/imagination_discovery/aud/continuity_round2/work/r2g/r2g.zag"
S = "/home/hatch/workspace/tnn-lab/imagination_discovery/aud/continuity_round2/work/r2_scores.zag"
src = open(P).read()

def rep(old, new, n=1):
    global src
    c = src.count(old)
    assert c == n, f"expected {n}, found {c} for: {old[:70]!r}"
    src = src.replace(old, new)

# ---- E1: chunked mix table with runtime state slots ----
rep("""fn mix_new(nsamp:i64)[]u8{
    let p:*u8=_zag_malloc(nsamp*8) as *u8;
    if(p==null as *u8){return "";}
    let m:[]u8=p[0..(nsamp*8)];
    let i:i64=0;
    while(i<nsamp*8){m[i]=0;i=i+1;}
    return m;
}""",
"""// chunked mix: table [magic, nchunks, nsamp, logfd, seedoff, gbmode,
// constgain, (bytelen,ptr)*]. A single 300 s i64 arena (105 MB) exceeds the
// znc 2^25-byte slice limit, so the mix is striped in 30 s chunks; the
// integer-add semantics are unchanged.
fn mix_new(nsamp:i64)[]u8{
    let nch:i64=(nsamp+CHSMP-1)/CHSMP;
    let tp:*u8=_zag_malloc((7+2*nch)*8) as *u8;
    if(tp==null as *u8){return "";}
    let t:[]u8=tp[0..((7+2*nch)*8)];
    put64(t,0,0x4348554E4B5F4D4958);
    put64(t,8,nch);
    put64(t,16,nsamp);
    put64(t,24,-1);
    put64(t,32,0);
    put64(t,40,0);
    put64(t,48,0);
    let c:i64=0;
    while(c<nch){
        let cs:i64=CHSMP;
        if(c==nch-1){cs=nsamp-c*CHSMP;}
        let cp:*u8=_zag_malloc(cs*8) as *u8;
        if(cp==null as *u8){return "";}
        let cb:[]u8=cp[0..(cs*8)];
        let i:i64=0;
        while(i<cs*8){cb[i]=0;i=i+1;}
        put64(t,56+c*16,cs*8);
        put64(t,64+c*16,cp as i64);
        c=c+1;
    }
    return t;
}
fn mchunk(m:[]u8,c:i64)[]u8{
    let p:i64=get64(m,64+c*16);
    let lb:i64=get64(m,56+c*16);
    return (p as *u8)[0..lb];
}""")

# ---- E1b: CHSMP const + decimal writers + parse_i64 ----
rep("const PH1:i64 = 281474976710656;",
"""const PH1:i64 = 281474976710656;
const CHSMP:i64 = 1323000; // 30 s chunk: chunked mix (znc 2^25 slice limit)
fn wdec(fd:i64,v:i64)void{
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
}""")

# ---- E2: place(): chunk-hoisted + placement log ----
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
    let lfd:i64=get64(m,24);
    if(lfd>=0){
        wdec(lfd,start);wch(lfd,32);
        wdec(lfd,g_nsamp(h,gi));wch(lfd,32);
        wdec(lfd,gi);wch(lfd,10);
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

# ---- E3: morph(): chunk-hoisted ----
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

# ---- E4: g_pick takes m; seed offset from the mix table ----
rep("fn g_pick(h:[]u8,cid:i64,voice:i64,salt:i64,seq:i64,ban:i64)i64{",
    "fn g_pick(h:[]u8,m:[]u8,cid:i64,voice:i64,salt:i64,seq:i64,ban:i64)i64{\n    let s2:i64=salt+get64(m,32);")
n_h32salt = src.count("let hh:i64=h32(salt+k*7919,seq*131+k);")
assert n_h32salt == 2, f"g_pick h32 sites: {n_h32salt}"
src = src.replace("let hh:i64=h32(salt+k*7919,seq*131+k);",
                  "let hh:i64=h32(s2+k*7919,seq*131+k);")
n_calls = src.count("g_pick(h,")
assert n_calls == 38, f"g_pick call sites: {n_calls}"
src = src.replace("g_pick(h,", "g_pick(h,m,")

# ---- E5: constgain flag (H2 control) in scatter / run_feet ----
rep("""            place(h,m,nsamp,gi,(t*SRF) as i64,g0*(0.7+0.6*h01(salt+41,q)),0);""",
"""            let gf2:f64=0.7+0.6*h01(salt+41,q);
            if(get64(m,48)==1){gf2=1.0;}
            place(h,m,nsamp,gi,(t*SRF) as i64,g0*gf2,0);""")
rep("""            let g:f64=g0*(0.85+0.3*h01(salt+13,q));""",
"""            let g:f64=g0*(0.85+0.3*h01(salt+13,q));
            if(get64(m,48)==1){g=g0;}""")

# ---- E6: bridge_world / bridge_ocean mode dispatch + ocean abl ----
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
    let gi:i64=g_pick(h,m,c_shout,salt%3,salt+13,0,-1);
    place(h,m,nsamp,gi,((t0+dur*0.55)*SRF) as i64,0.36,0);
}
// world-first bridge for the ocean corpus (G1): wash + rumble + distant
// swell + sparse crack. No kids voices anywhere (corpus honesty).
fn bridge_ocean(h:[]u8,m:[]u8,nsamp:i64,t0:f64,t1:f64,wt1:f64,salt:i64)void{
    let bm:i64=get64(m,40);
    if(bm==2){bridge_ocean_abl(h,m,nsamp,t0,t1,salt);return;}
    let c_wash:i64=cid_by_name(h,"wash");
    let c_rumble:i64=cid_by_name(h,"rumble");
    let c_swell:i64=cid_by_name(h,"swell");
    let c_crack:i64=cid_by_name(h,"crack");
    let e0:f64=t0; let e1:f64=t1; let ew:f64=wt1;
    if(bm==1){
        e0=t0-2.0; if(e0<0.0){e0=0.0;}
        e1=t1+2.0; if(e1>30.0){e1=30.0;}
        ew=wt1+2.0; if(ew>30.0){ew=30.0;}
        put64(m,48,1);
    }
    scatter(h,m,nsamp,c_wash,e0,ew,1.1,salt+3,0.16);
    scatter(h,m,nsamp,c_rumble,e0,ew,2.2,salt+1,0.10);
    scatter(h,m,nsamp,c_swell,e0,e1,3.5,salt,0.30);
    scatter(h,m,nsamp,c_crack,e0,e1,1.7,salt+2,0.12);
    put64(m,48,0);
}
fn bridge_ocean_abl(h:[]u8,m:[]u8,nsamp:i64,t0:f64,t1:f64,salt:i64)void{
    let c_swell:i64=cid_by_name(h,"swell");
    let c_crack:i64=cid_by_name(h,"crack");
    scatter(h,m,nsamp,c_swell,t0,t1,1.4,salt+21,0.42);
    scatter(h,m,nsamp,c_crack,t0,t1,0.5,salt+22,0.30);
}
fn bridge_world(h:[]u8,m:[]u8,nsamp:i64,t0:f64,t1:f64,wt1:f64,salt:i64)void{
    let bm:i64=get64(m,40);
    if(bm==2){bridge_abl(h,m,nsamp,t0,t1,salt);return;}
    let c_thump:i64=cid_by_name(h,"thump");
    let c_wind:i64=cid_by_name(h,"wind");
    let c_laugh:i64=cid_by_name(h,"laugh");
    let c_wash:i64=cid_by_name(h,"wash");
    // sustained world texture: long wash grains overlapping at 0.9 s
    // spacing -- a continuous low presence, scored content, never a fade.
    // wt1 caps the long (3 s) grains so the v2 natural ending (quiet from
    // 28.7 s) is preserved in the final bridge.
    // bm 1 (H2 control): same captured material scored 2 s before the
    // nominal insertion through 2 s after the nominal exit, gain trajectory
    // held constant (constgain slot), no insertion/removal boundary.
    let e0:f64=t0; let e1:f64=t1; let ew:f64=wt1;
    if(bm==1){
        e0=t0-2.0; if(e0<0.0){e0=0.0;}
        e1=t1+2.0; if(e1>28.0){e1=28.0;}
        ew=wt1+2.0; if(ew>28.0){ew=28.0;}
        put64(m,48,1);
    }
    scatter(h,m,nsamp,c_wash,e0,ew,0.9,salt+3,0.20);
    scatter(h,m,nsamp,c_wind,e0,ew,1.4,salt+1,0.055);  // breath / air
    run_feet(h,m,nsamp,c_thump,e0,e1,1.2,salt,0.10);    // shuffling feet
    scatter(h,m,nsamp,c_laugh,e0,e1,0.9,salt+2,0.09);   // distant play
    put64(m,48,0);
}""")

# ---- E7: insert round-2 scores before main ----
scores = open(S).read()
n_sc = scores.count("g_pick(h,")
assert n_sc == 11, f"r2_scores g_pick sites: {n_sc}"
scores = scores.replace("g_pick(h,", "g_pick(h,m,")
rep("fn main()i32{", scores + "\nfn main()i32{", n=1)

# ---- E8: main() with argv: pack, out, seedoff, bmode, logpath ----
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
    let seedoff:i64=0;
    if(a4.len>0){seedoff=parse_i64(a4);}
    let a5:[]u8=_zag_arg(5);
    let bmode:i64=0;
    if(a5.len>0){bmode=parse_i64(a5);}
    let a6:[]u8=_zag_arg(6);
    let lfd:i64=-1;
    if(a6.len>0){
        let cs6:[]u8=cstr(a6);
        lfd=_zag_raw_syscall(2,(_zag_slice_ptr(cs6) as i64),577,438,0,0,0);
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
    put64(m,24,lfd);
    put64(m,32,seedoff);
    put64(m,40,bmode);
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
    if(lfd>=0){_zag_raw_syscall(3,lfd,0,0,0,0,0);}
    return rc;
}"""
rep(old_main, new_main, n=1)

open(P, "w").write(src)
print("patch r2g v2 OK")
