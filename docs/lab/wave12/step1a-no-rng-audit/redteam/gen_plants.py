#!/usr/bin/env python3
"""Deterministic red-team plant generator for RNGSCAN-2026-09-20-v1.
No RNG anywhere: 20 fixed plants in a fixed order, covering all five banned
categories with varied disguises (computed immediates, split paths, partial
init, early-return init, renamed maps, disguised pointer arithmetic).
Each plant is a complete, compilable variation.zag module.
Usage: python3 gen_plants.py <outdir>
"""
import os, sys

HDR = '@import("R33_NATIVE_IO_V1.zag")\n\n'
MAIN = '\nfn main()i32 {\n    _zag_println("P%02d");\n    return 0;\n}\n'
VARY_OPEN = 'fn vary_expr(input:[]u8, state:[]u8, out:[]u8)i32 {\n'
VARY_CLOSE = '    return 0;\n}\n'

# shared: alloc 16 zeroed bytes named b
ZERO16 = ('    let b:[]u8=nio_alloc(16);\n'
          '    if(b.len!=16){return 1;}\n'
          '    let zi:i32=0;\n'
          '    while(zi<b.len){b[zi]=0; zi=zi+1;}\n')

plants = {}

# ---- 4.1 entropy ----
plants[1] = ("getrandom literal 318", "",
    VARY_OPEN + ZERO16 +
    '    let n:i64=_zag_raw_syscall(318,_zag_slice_ptr(b) as i64,16,0,0,0,0);\n'
    '    if(n<0){nio_free(b); return 0;}\n'
    '    if(out.len>0){out[0]=b[0];}\n'
    '    nio_free(b);\n' + VARY_CLOSE)

plants[2] = ("getrandom computed 300+18 (object-scan test)", "",
    VARY_OPEN + ZERO16 +
    '    let n:i64=_zag_raw_syscall(300+18,_zag_slice_ptr(b) as i64,16,0,0,0,0);\n'
    '    if(n<0){nio_free(b); return 0;}\n'
    '    if(out.len>0){out[0]=b[0];}\n'
    '    nio_free(b);\n' + VARY_CLOSE)

plants[3] = ("open(2) of /dev/urandom literal", "",
    VARY_OPEN +
    '    let p:[]u8="/dev/urandom";\n'
    '    let fd:i64=_zag_raw_syscall(2,_zag_slice_ptr(p) as i64,0,0,0,0,0);\n'
    '    if(fd>=0){let c:i64=_zag_raw_syscall(3,fd,0,0,0,0,0); if(c<0){return 0;}}\n'
    '    if(out.len>0 && input.len>0){out[0]=input[0];}\n' + VARY_CLOSE)

plants[4] = ("open(2) of runtime-split /dev/urandom path", "",
    VARY_OPEN +
    '    let a:[]u8="/dev/";\n'
    '    let u:[]u8="urandom";\n'
    '    let c:[]u8=nio_alloc(13);\n'
    '    if(c.len!=13){return 1;}\n'
    '    let zi:i32=0;\n'
    '    while(zi<c.len){c[zi]=0; zi=zi+1;}\n'
    '    let i:i32=0;\n'
    '    while(i<5){c[i]=a[i]; i=i+1;}\n'
    '    i=0;\n'
    '    while(i<7){c[5+i]=u[i]; i=i+1;}\n'
    '    let fd:i64=_zag_raw_syscall(2,_zag_slice_ptr(c) as i64,0,0,0,0,0);\n'
    '    if(fd>=0){let cc:i64=_zag_raw_syscall(3,fd,0,0,0,0,0); if(cc<0){nio_free(c); return 0;}}\n'
    '    nio_free(c);\n'
    '    if(out.len>0 && input.len>0){out[0]=input[0];}\n' + VARY_CLOSE)

plants[5] = ("rdseed token in helper fn", "",
    'fn rdseed_mix(x:i64)i64 {\n    return x^91138233;\n}\n' +
    VARY_OPEN +
    '    if(out.len>0 && input.len>0){out[0]=((rdseed_mix(input[0] as i64))&255) as u8;}\n' +
    VARY_CLOSE)

# ---- 4.2 wall-clock ----
plants[6] = ("clock_gettime literal 228", "",
    VARY_OPEN +
    '    let rc:i64=_zag_raw_syscall(228,1,0,0,0,0,0);\n'
    '    if(rc<0){return 0;}\n'
    '    if(out.len>0 && input.len>0){out[0]=input[0];}\n' + VARY_CLOSE)

plants[7] = ("clock_gettime computed 200+28 (object-scan test)", "",
    VARY_OPEN +
    '    let rc:i64=_zag_raw_syscall(200+28,1,0,0,0,0,0);\n'
    '    if(rc<0){return 0;}\n'
    '    if(out.len>0 && input.len>0){out[0]=input[0];}\n' + VARY_CLOSE)

plants[8] = ("gettimeofday literal 96", "",
    VARY_OPEN +
    '    let rc:i64=_zag_raw_syscall(96,0,0,0,0,0,0);\n'
    '    if(rc<0){return 0;}\n'
    '    if(out.len>0 && input.len>0){out[0]=input[0];}\n' + VARY_CLOSE)

plants[9] = ("gettimeofday computed 100-4 (object-scan test)", "",
    VARY_OPEN +
    '    let rc:i64=_zag_raw_syscall(100-4,0,0,0,0,0,0);\n'
    '    if(rc<0){return 0;}\n'
    '    if(out.len>0 && input.len>0){out[0]=input[0];}\n' + VARY_CLOSE)

plants[10] = ("clock_gettime token wrapper fn", "",
    'fn clock_gettime_wrap()i64 {\n    return _zag_raw_syscall(228,0,0,0,0,0,0);\n}\n' +
    VARY_OPEN +
    '    let t:i64=clock_gettime_wrap();\n'
    '    if(out.len>0){out[0]=(t&255) as u8;}\n' + VARY_CLOSE)

# ---- 4.3 uninitialized reads ----
plants[11] = ("read before any write", "",
    VARY_OPEN +
    '    let s:[]u8=nio_alloc(16);\n'
    '    if(s.len!=16){return 1;}\n'
    '    let v:u8=s[3];\n'
    '    if(out.len>0){out[0]=v;}\n'
    '    nio_free(s);\n' + VARY_CLOSE)

plants[12] = ("partial init loop then read beyond", "",
    VARY_OPEN +
    '    let s:[]u8=nio_alloc(16);\n'
    '    if(s.len!=16){return 1;}\n'
    '    let i:i32=0;\n'
    '    while(i<8){s[i]=0; i=i+1;}\n'
    '    let v:u8=s[10];\n'
    '    if(out.len>0){out[0]=v;}\n'
    '    nio_free(s);\n' + VARY_CLOSE)

plants[13] = ("early return inside init loop", "",
    VARY_OPEN +
    '    let s:[]u8=nio_alloc(16);\n'
    '    if(s.len!=16){return 1;}\n'
    '    let i:i32=0;\n'
    '    while(i<s.len){\n'
    '        s[i]=0;\n'
    '        if(i==4){nio_free(s); return 0;}\n'
    '        i=i+1;\n'
    '    }\n'
    '    let v:u8=s[10];\n'
    '    if(out.len>0){out[0]=v;}\n'
    '    nio_free(s);\n' + VARY_CLOSE)

plants[14] = ("read after nio_free", "",
    VARY_OPEN +
    '    let s:[]u8=nio_alloc(16);\n'
    '    if(s.len!=16){return 1;}\n'
    '    let i:i32=0;\n'
    '    while(i<s.len){s[i]=0; i=i+1;}\n'
    '    nio_free(s);\n'
    '    let v:u8=s[0];\n'
    '    if(out.len>0){out[0]=v;}\n' + VARY_CLOSE)

plants[15] = ("two buffers, init one read other", "",
    VARY_OPEN +
    '    let a:[]u8=nio_alloc(16);\n'
    '    let q:[]u8=nio_alloc(16);\n'
    '    if(a.len!=16 || q.len!=16){return 1;}\n'
    '    let i:i32=0;\n'
    '    while(i<a.len){a[i]=0; i=i+1;}\n'
    '    let v:u8=q[0];\n'
    '    if(out.len>0){out[0]=v;}\n'
    '    nio_free(a); nio_free(q);\n' + VARY_CLOSE)

# ---- 4.4 hash-iteration ----
plants[16] = ("hashmap insert + bucket-order emit", "",
    'fn hashmap_slot(k:u8)i32 { return ((k as i32)*37)%64; }\n' +
    VARY_OPEN +
    '    let keys:[]u8=nio_alloc(64);\n'
    '    let vals:[]u8=nio_alloc(64);\n'
    '    let used:[]u8=nio_alloc(64);\n'
    '    if(keys.len!=64 || vals.len!=64 || used.len!=64){return 1;}\n'
    '    let i:i32=0;\n'
    '    while(i<64){keys[i]=0; i=i+1;}\n'
    '    i=0;\n'
    '    while(i<64){vals[i]=0; i=i+1;}\n'
    '    i=0;\n'
    '    while(i<64){used[i]=0; i=i+1;}\n'
    '    i=0;\n'
    '    while(i<input.len){let h:i32=hashmap_slot(input[i]); keys[h]=input[i]; vals[h]=input[i]; used[h]=1; i=i+1;}\n'
    '    let o:i32=0;\n'
    '    let b2:i32=0;\n'
    '    while(b2<64){if(used[b2]==1 && o<out.len){out[o]=vals[b2]; o=o+1;} b2=b2+1;}\n'
    '    nio_free(keys); nio_free(vals); nio_free(used);\n' + VARY_CLOSE)

plants[17] = ("renamed slotmap", "",
    'fn slotmap_put(keys:[]u8, vals:[]u8, k:u8, v:u8)void {\n'
    '    let h:i32=((k as i32)*37)%64;\n'
    '    keys[h]=k; vals[h]=v;\n'
    '}\n'
    'fn slotmap_emit(vals:[]u8, out:[]u8)i32 {\n'
    '    let o:i32=0;\n'
    '    let s2:i32=0;\n'
    '    while(s2<64){if(o<out.len){out[o]=vals[s2]; o=o+1;} s2=s2+1;}\n'
    '    return o;\n'
    '}\n' +
    VARY_OPEN +
    '    let sk:[]u8=nio_alloc(64);\n'
    '    let sv:[]u8=nio_alloc(64);\n'
    '    if(sk.len!=64 || sv.len!=64){return 1;}\n'
    '    let i:i32=0;\n'
    '    while(i<64){sk[i]=0; i=i+1;}\n'
    '    i=0;\n'
    '    while(i<64){sv[i]=0; i=i+1;}\n'
    '    i=0;\n'
    '    while(i<input.len){slotmap_put(sk,sv,input[i],input[i]); i=i+1;}\n'
    '    let n2:i32=slotmap_emit(sv,out);\n'
    '    nio_free(sk); nio_free(sv);\n'
    '    if(n2<0){return 1;}\n' + VARY_CLOSE)

plants[18] = ("BUCKETS + bucket_iter", "",
    'fn bucket_iter(vals:[]u8, out:[]u8)i32 {\n'
    '    let o:i32=0;\n'
    '    let q2:i32=0;\n'
    '    while(q2<64){if(o<out.len){out[o]=vals[q2]; o=o+1;} q2=q2+1;}\n'
    '    return o;\n'
    '}\n' +
    VARY_OPEN +
    '    let BUCKETS:[]u8=nio_alloc(64);\n'
    '    if(BUCKETS.len!=64){return 1;}\n'
    '    let i:i32=0;\n'
    '    while(i<BUCKETS.len){BUCKETS[i]=input[i%input.len]; i=i+1;}\n'
    '    let n3:i32=bucket_iter(BUCKETS,out);\n'
    '    nio_free(BUCKETS);\n'
    '    if(n3<0){return 1;}\n' + VARY_CLOSE)

# ---- 4.5 impure-of-inputs ----
plants[19] = ("disguised ASLR leak (ptr/4096 into output)", "",
    VARY_OPEN + ZERO16 +
    '    let p:i64=(_zag_slice_ptr(b) as i64)/4096;\n'
    '    if(out.len>0){out[0]=(p&255) as u8;}\n'
    '    nio_free(b);\n' + VARY_CLOSE)

plants[20] = ("getenv token helper", "",
    'fn get_env_flag()i32 {\n    return 0;\n}\n' +
    VARY_OPEN +
    '    let e:i32=get_env_flag();\n'
    '    if(out.len>0 && input.len>0){out[0]=input[0]^(e as u8);}\n' + VARY_CLOSE)

def main():
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    for n in range(1, 21):
        desc, extra, body = plants[n]
        src = HDR + extra + body + (MAIN % n)
        p = os.path.join(outdir, "plant%02d.zag" % n)
        with open(p, "w") as f:
            f.write(src)
        print("plant%02d: %s" % (n, desc))

if __name__ == "__main__":
    main()
