#!/usr/bin/env python3
"""Patch work/r2b/mech_kids.zag (copy of b_beta/mech_kids.zag) and
work/r2b/assemble.zag (copy of b_beta/assemble.zag) for round-2 H1.

- score_kids takes (outpath, a3, seed, mode, logpath).
- K_SEED -> runtime seed (default 20260922 reproduces v3 SHA).
- ev_place_p: foreground-only +/-40ms deterministic onset permutation
  (keyed by catalog idx; control flow keeps scored onsets so spacing is
  preserved). Bed placements keep calling 9-arg ev_place untouched.
- mode==2: bed-only control (early exit after the bed loops).
- placement log path from argv[6].
Every replacement asserts its occurrence count. Frozen source untouched."""
import re

P = "/home/hatch/workspace/tnn-lab/imagination_discovery/aud/continuity_round2/work/r2b/mech_kids.zag"
src = open(P).read()

def rep(old, new, n=1):
    global src
    c = src.count(old)
    assert c == n, f"expected {n}, found {c} for: {old[:70]!r}"
    src = src.replace(old, new)

# 1. score_kids signature
rep("fn score_kids(outpath:[]u8,a3:[]u8)i32{",
    "fn score_kids(outpath:[]u8,a3:[]u8,seed:i64,mode:i64,logpath:[]u8)i32{")

# 2. drop the K_SEED const, use runtime seed
rep("const K_SEED:i64 = 20260922;\n", "")
n_ks = src.count("K_SEED")
assert n_ks == 31, f"K_SEED uses: {n_ks}"
src = src.replace("K_SEED", "seed")

# 3. ev_place_p wrapper after ev_place's definition
rep("""    return dst_ms+cat_durms(cat,idx);
}""",
"""    return dst_ms+cat_durms(cat,idx);
}
// round-2 H1: foreground-only deterministic +/-40ms onset permutation.
// pm=1: shift this placement's onset by (h32(seed+31337,idx)%81)-40 ms;
// the LOG records the permuted onset, but control flow keeps the scored
// onset so event spacing/order/gains are unchanged. pm=0: identical to ev_place.
fn ev_place_p(m:[]u8,mns:i64,t:[]u8,cat:[]u8,idx:i64,dst_ms:i64,target:i64,rev:i64,logfd:i64,seed:i64,pm:i64) i64{
    let pdst:i64=dst_ms;
    if(pm==1){pdst=pdst+(h32(seed+31337,idx)%81)-40;}
    ev_place(m,mns,t,cat,idx,pdst,target,rev,logfd);
    return dst_ms+cat_durms(cat,idx);
}""")

# 4. rename all ev_place CALL sites (not the fn definition) to ev_place_p.
# NOTE: this also renames the inner ev_place() call inside ev_place_p's own
# body (inserted in step 3) -- restored in 4b below.
n_def = len(re.findall(r'fn ev_place\(', src))
assert n_def == 1, f"ev_place defs: {n_def}"
src2 = re.sub(r'(?<!fn )ev_place\(', 'ev_place_p(', src)
n_ren = src2.count('ev_place_p(')
assert n_ren == 26, f"renamed sites (25 calls + 1 def): {n_ren}"
src = src2

# 4b. restore ev_place_p's inner call to the original 9-arg ev_place
rep("ev_place_p(m,mns,t,cat,idx,pdst,target,rev,logfd);",
    "ev_place(m,mns,t,cat,idx,pdst,target,rev,logfd);")

# 5. append (seed,pfg) to every ev_place_p CALL's trailing ,logfd).
# Only on ev_place_p( lines: the restored inner 9-arg ev_place call and the
# 2 bed calls (handled in step 6) must not match.
n_lf = len(re.findall(r'ev_place_p\([^;]*?,logfd\)', src))
assert n_lf == 24, f"ev_place_p ,logfd) sites: {n_lf}"
src = re.sub(r'(ev_place_p\([^;]*?),logfd\)', r'\1,logfd,seed,pfg)', src)

# 6. restore the 2 BED calls to plain 9-arg ev_place (no permutation, no extra args)
rep("let bend:i64=ev_place_p(m,ns,t,cat,bi,bedt,2500,0,logfd,seed,pfg);",
    "let bend:i64=ev_place(m,ns,t,cat,bi,bedt,2500,0,logfd);")
rep("ev_place_p(m,ns,t,cat,qb,bedt,2500,0,logfd,seed,pfg);",
    "ev_place(m,ns,t,cat,qb,bedt,2500,0,logfd);")

# 7. pfg local + logpath-based log open (replaces the a3=="log" block)
rep("""    let ns:i64=K_DUR_MS*441/10; // 1323000
    let logfd:i64=-1;
    if(_zag_strcmp(a3,"log")==1){
        let lp:[]u8=cstr("work/place_kids.log");
        if(lp.len>0){
            logfd=_zag_raw_syscall(2,(_zag_slice_ptr(lp) as i64),577,438,0,0,0);
            _zag_free(_zag_slice_ptr(lp));
        }
    }""",
"""    let ns:i64=K_DUR_MS*441/10; // 1323000
    let pfg:i64=0;
    if(mode==1){pfg=1;} // H1: permute foreground onsets +/-40ms
    let logfd:i64=-1;
    if(logpath.len>0){
        let lp:[]u8=cstr(logpath);
        if(lp.len>0){
            logfd=_zag_raw_syscall(2,(_zag_slice_ptr(lp) as i64),577,438,0,0,0);
            _zag_free(_zag_slice_ptr(lp));
        }
    }""")

# 8. bed-only control: early exit right after the bed tail loop, before P0
rep("""    // P0 TAUNT 0-5s: sparse shouts/calls across the playground
    now=400;""",
"""    // H1 bed-only control (mode==2): the bed above is byte-identical to the
    // full scene's bed (same seed, same ctr sequence); no foreground at all.
    if(mode==2){
        let rc2:i32=write_wav(outpath,m,ns);
        if(logfd>=0){_zag_raw_syscall(3,logfd,0,0,0,0,0);}
        return rc2;
    }
    // P0 TAUNT 0-5s: sparse shouts/calls across the playground
    now=400;""")

open(P, "w").write(src)
print("mech_kids patch OK")

# ---- assemble.zag: argv seed/mode/logpath ----
Q = "/home/hatch/workspace/tnn-lab/imagination_discovery/aud/continuity_round2/work/r2b/assemble.zag"
q = open(Q).read()

def qrep(old, new, n=1):
    global q
    c = q.count(old)
    assert c == n, f"expected {n}, found {c} for: {old[:70]!r}"
    q = q.replace(old, new)

qrep("""fn main()i32{
    let a1:[]u8=_zag_arg(1);
    let a2:[]u8=_zag_arg(2);
    let a3:[]u8=_zag_arg(3);
    let subj:i32=0;
    if(_zag_strcmp(a1,"kids")==1){subj=1;}
    if(_zag_strcmp(a1,"kethra")==1){subj=2;}
    if(_zag_strcmp(a1,"ocean")==1){subj=3;}
    if(subj==0){return 7;}
    let rc:i32=0;
    if(subj==1){rc=score_kids(a2,a3);}
    if(subj==2){rc=score_kethra(a2,a3);}
    if(subj==3){rc=score_ocean(a2,a3);}
    return rc;
}""",
"""fn parse_i64(s:[]u8)i64{
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
fn main()i32{
    let a1:[]u8=_zag_arg(1);
    let a2:[]u8=_zag_arg(2);
    let a3:[]u8=_zag_arg(3);
    let a4:[]u8=_zag_arg(4);
    let seed:i64=20260922;
    if(a4.len>0){seed=parse_i64(a4);}
    let a5:[]u8=_zag_arg(5);
    let mode:i64=0;
    if(a5.len>0){mode=parse_i64(a5);}
    let a6:[]u8=_zag_arg(6);
    let subj:i32=0;
    if(_zag_strcmp(a1,"kids")==1){subj=1;}
    if(_zag_strcmp(a1,"kethra")==1){subj=2;}
    if(_zag_strcmp(a1,"ocean")==1){subj=3;}
    if(subj==0){return 7;}
    let rc:i32=0;
    if(subj==1){rc=score_kids(a2,a3,seed,mode,a6);}
    if(subj==2){rc=score_kethra(a2,a3);}
    if(subj==3){rc=score_ocean(a2,a3);}
    return rc;
}""")

open(Q, "w").write(q)
print("assemble patch OK")
