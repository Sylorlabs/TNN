#!/usr/bin/env python3
"""M1 battery generator: builds target sources (plant variation + driver main),
P07 (rdtsc ELF), P12 (invoke-discard), and clean modules C01/C02/C04/C05/C06.
Deterministic: fixed literals, no randomness."""
import os, shutil

EV = os.path.expanduser("~/workspace/tnn-lab/wave12/step1a-v2/gate-expansion/evidence/m1")
SRC = os.path.join(EV, "src")
V1 = os.path.expanduser("~/workspace/tnn-lab/wave12/step1a-no-rng-audit/redteam/plants")
K2 = os.path.expanduser("~/workspace/tnn-lab/wave12/step1a-v2/thin-certifier/k2prime-redteam/plants")

INPUT = "0123456789ABCDEF" * 6  # 96 chars

DRIVER_MAIN = '''
fn main()i32 {
    let input:[]u8="%s";
    let state:[]u8=nio_alloc(256);
    if(state.len!=256){return 9;}
    let si:i32=0;
    while(si<state.len){let sv:i32=(si&255); state[si]=sv as u8; si=si+1;}
    let out:[]u8=nio_alloc(256);
    if(out.len!=256){nio_free(state); return 9;}
    let rc:i32=vary_expr(input,state,out);
    _zag_print("rc=");
    _zag_print(_zag_i64_to_str(rc as i64));
    _zag_print(" out0=");
    _zag_println(_zag_i64_to_str(out[0] as i64));
    nio_free(state);
    nio_free(out);
    return 0;
}
''' % INPUT

HELPERS = '''
fn z_cstr(s:[]u8)[]u8 {
    let b:[]u8=nio_alloc(s.len+1);
    if(b.len!=s.len+1){return b;}
    let i:i32=0;
    while(i<s.len){b[i]=s[i]; i=i+1;}
    b[s.len]=0;
    return b;
}
fn put64(b:[]u8, off:i32, v:i64)void {
    let i:i32=0;
    while(i<8){
        let sh:i64=(i*8) as i64;
        let by:i64=(v>>sh)&255;
        b[off+i]=by as u8;
        i=i+1;
    }
    return;
}
'''

def strip_main(src):
    """Cut from the 'fn main' line to EOF. Returns (head, had_main)."""
    lines = src.split("\n")
    for i, l in enumerate(lines):
        if l.strip().startswith("fn main"):
            return "\n".join(lines[:i]), True
    return src, False

def write_target(name, body):
    p = os.path.join(SRC, "t_%s.zag" % name)
    with open(p, "w") as f:
        f.write(body)
    print("wrote", p)

# --- corpus plants: (target, source path, import fix) ---
plants = [
    ("p01", os.path.join(V1, "plant01.zag"), None),
    ("p02", os.path.join(V1, "plant06.zag"), None),
    ("p03", os.path.join(V1, "plant03.zag"), None),
    ("p04", os.path.join(V1, "plant11.zag"), None),
    ("p05", os.path.join(V1, "plant20.zag"), None),
    ("p06", os.path.join(V1, "plant19.zag"), None),
    ("p08", os.path.join(V1, "plant16.zag"), None),
    ("p09", "/tmp/p09_plant17.zag", ("@import(\"harness.zag\")", "@import(\"R33_NATIVE_IO_V1.zag\")")),
    ("p10", os.path.join(K2, "plant19", "variation.zag"), None),
    ("p11", os.path.join(K2, "plant20", "variation.zag"), None),
]
for name, path, fix in plants:
    src = open(path).read()
    if fix:
        a, b = fix
        assert a in src, name
        src = src.replace(a, b)
    head, had = strip_main(src)
    if name == "p09":
        assert not had, "plant17 unexpectedly has main"
    body = head.rstrip() + "\n" + DRIVER_MAIN
    write_target(name, body)

# --- P07: rdtsc via minimal ELF64 child ---
P07 = '''@import("R33_NATIVE_IO_V1.zag")
// P07 — rdtsc plant. Pure Zag cannot emit the rdtsc instruction, so the
// variation builds a minimal 168-byte static ELF64 whose _start executes
// rdtsc, writes it to ./p07_rdtsc.elf, chmods +x, and execve()s it.
// Under the M1 launcher (PR_SET_TSC,PR_TSC_SIGSEGV) the child dies SIGSEGV.
// Run directly (no sandbox) the child prints "TSC" and exits 0.
%s
fn eput8(e:[]u8, o:i32, v:i64)void { e[o]=(v&255) as u8; return; }
fn eput16(e:[]u8, o:i32, v:i64)void {
    e[o]=(v&255) as u8;
    let h:i64=(v>>8)&255;
    e[o+1]=h as u8;
    return;
}
fn eput32(e:[]u8, o:i32, v:i64)void {
    e[o]=(v&255) as u8;
    let b1:i64=(v>>8)&255; e[o+1]=b1 as u8;
    let b2:i64=(v>>16)&255; e[o+2]=b2 as u8;
    let b3:i64=(v>>24)&255; e[o+3]=b3 as u8;
    return;
}
fn eput64(e:[]u8, o:i32, v:i64)void {
    let i:i32=0;
    while(i<8){
        let sh:i64=(i*8) as i64;
        let by:i64=(v>>sh)&255;
        e[o+i]=by as u8;
        i=i+1;
    }
    return;
}
fn build_elf(e:[]u8)void {
    // ELF header (64 bytes)
    eput8(e,0,127); eput8(e,1,69); eput8(e,2,76); eput8(e,3,70);
    eput8(e,4,2); eput8(e,5,1); eput8(e,6,1); eput8(e,7,0);
    eput16(e,16,2); eput16(e,18,62); eput32(e,20,1);
    eput64(e,24,4194424);   // e_entry = 0x400078
    eput64(e,32,64);        // e_phoff
    eput32(e,48,0);         // e_flags
    eput16(e,52,64); eput16(e,54,56); eput16(e,56,1);
    // Program header at 64: PT_LOAD, R+X, vaddr 0x400000, filesz=memsz=168
    eput32(e,64,1); eput32(e,68,5);
    eput64(e,72,0);
    eput64(e,80,4194304); eput64(e,88,4194304);
    eput64(e,96,168); eput64(e,104,168); eput64(e,112,4096);
    // code at 120: rdtsc; write(1,"TSC\\n"); exit(0)
    eput8(e,120,15); eput8(e,121,49);
    eput8(e,122,72); eput8(e,123,199); eput8(e,124,192);
    eput8(e,125,1); eput8(e,126,0); eput8(e,127,0); eput8(e,128,0);
    eput8(e,129,72); eput8(e,130,199); eput8(e,131,199);
    eput8(e,132,1); eput8(e,133,0); eput8(e,134,0); eput8(e,135,0);
    eput8(e,136,72); eput8(e,137,141); eput8(e,138,53);
    eput8(e,139,21); eput8(e,140,0); eput8(e,141,0); eput8(e,142,0);
    eput8(e,143,72); eput8(e,144,199); eput8(e,145,194);
    eput8(e,146,4); eput8(e,147,0); eput8(e,148,0); eput8(e,149,0);
    eput8(e,150,15); eput8(e,151,5);
    eput8(e,152,72); eput8(e,153,199); eput8(e,154,192);
    eput8(e,155,60); eput8(e,156,0); eput8(e,157,0); eput8(e,158,0);
    eput8(e,159,72); eput8(e,160,49); eput8(e,161,255);
    eput8(e,162,15); eput8(e,163,5);
    eput8(e,164,84); eput8(e,165,83); eput8(e,166,67); eput8(e,167,10);
    return;
}
fn vary_expr(input:[]u8, state:[]u8, out:[]u8)i32 {
    let e:[]u8=nio_alloc(168);
    if(e.len!=168){return 1;}
    build_elf(e);
    let p:[]u8=z_cstr("p07_rdtsc.elf");
    if(p.len==0){nio_free(e); return 1;}
    let fd:i64=_zag_raw_syscall(2,_zag_slice_ptr(p) as i64,577,493,0,0,0);
    if(fd<0){nio_free(e); nio_free(p); return 2;}
    let w:i64=_zag_raw_syscall(1,fd,_zag_slice_ptr(e) as i64,168,0,0,0);
    let c:i64=_zag_raw_syscall(3,fd,0,0,0,0,0);
    if(w!=168){nio_free(e); nio_free(p); return 3;}
    let m:i64=_zag_raw_syscall(90,_zag_slice_ptr(p) as i64,493,0,0,0,0);
    if(m!=0){nio_free(e); nio_free(p); return 4;}
    let an:[]u8=z_cstr("p07_rdtsc");
    let argv:[]u8=nio_alloc(16);
    if(argv.len!=16){nio_free(e); nio_free(p); return 5;}
    put64(argv,0,_zag_slice_ptr(an) as i64);
    let envp:[]u8=nio_alloc(8);
    if(envp.len!=8){nio_free(e); nio_free(p); return 5;}
    let r:i64=_zag_raw_syscall(59,_zag_slice_ptr(p) as i64,_zag_slice_ptr(argv) as i64,_zag_slice_ptr(envp) as i64,0,0,0);
    nio_free(e); nio_free(p);
    return 6;
}
%s
''' % (HELPERS, DRIVER_MAIN)
write_target("p07", P07)

# --- P12: invoke getrandom, discard result ---
P12 = '''@import("R33_NATIVE_IO_V1.zag")
// P12 — mechanism-without-consumption (replay §10 class 5): invokes
// getrandom(2) and discards the result; out is a pure function of input.
// Replay cannot catch it in principle; the syscall-layer gate kills it.
fn vary_expr(input:[]u8, state:[]u8, out:[]u8)i32 {
    let b:[]u8=nio_alloc(32);
    if(b.len!=32){return 1;}
    let n:i64=_zag_raw_syscall(318,_zag_slice_ptr(b) as i64,32,0,0,0,0);
    let i:i32=0;
    while(i<input.len && i<out.len){
        let mm:i32=(i*7)&255;
        out[i]=input[i]^(mm as u8);
        i=i+1;
    }
    nio_free(b);
    if(n<0){return 0;}
    return 0;
}
%s
''' % DRIVER_MAIN
write_target("p12", P12)

# --- Clean modules ---
C01 = '''@import("R33_NATIVE_IO_V1.zag")
// C01 — canonical variation: out = f(input, state), fully deterministic.
fn vary_expr(input:[]u8, state:[]u8, out:[]u8)i32 {
    if(out.len<input.len){return 1;}
    let i:i32=0;
    while(i<input.len){
        let sw:u8=0;
        if(state.len>0){sw=state[i%%state.len];}
        let mm:u8=((i*31)&255) as u8;
        out[i]=input[i]^sw^mm;
        i=i+1;
    }
    return 0;
}
%s
''' % DRIVER_MAIN
write_target("c01", C01)

C02 = '''@import("R33_NATIVE_IO_V1.zag")
// C02 — state-dependent phrasing: fixed S-box keyed by input+state bytes.
fn vary_expr(input:[]u8, state:[]u8, out:[]u8)i32 {
    if(out.len<input.len || state.len==0){return 1;}
    let tab:[]u8=nio_alloc(256);
    if(tab.len!=256){return 2;}
    let ti:i32=0;
    while(ti<256){
        let x:i64=(ti as i64)*2654435761;
        x=x^(x>>13);
        x=x^(x<<7);
        tab[ti]=(x&255) as u8;
        ti=ti+1;
    }
    let i:i32=0;
    while(i<input.len){
        let sw:u8=state[(i*37)%%state.len];
        let idx:i32=((input[i] as i32)+(sw as i32))&255;
        out[i]=tab[idx];
        i=i+1;
    }
    nio_free(tab);
    return 0;
}
%s
''' % DRIVER_MAIN
write_target("c02", C02)

C04 = '''@import("R33_NATIVE_IO_V1.zag")
// C04 — file IO via pinned substrate allowlist: reads the fixed data file
// "c04_data.bin" (created by the battery runner) via open/read, mixes into out.
fn vary_expr(input:[]u8, state:[]u8, out:[]u8)i32 {
    if(out.len<input.len){return 1;}
    let p:[]u8="c04_data.bin";
    let fd:i64=_zag_raw_syscall(2,_zag_slice_ptr(p) as i64,0,0,0,0,0);
    if(fd<0){return 2;}
    let db:[]u8=nio_alloc(64);
    if(db.len!=64){return 3;}
    let n:i64=_zag_raw_syscall(0,fd,_zag_slice_ptr(db) as i64,64,0,0,0);
    let cc:i64=_zag_raw_syscall(3,fd,0,0,0,0,0);
    if(n<0){nio_free(db); return 4;}
    let i:i32=0;
    while(i<input.len){
        let d:u8=0;
        if(n>0){d=db[i%%(n as i32)];}
        out[i]=input[i]^d;
        i=i+1;
    }
    nio_free(db);
    return 0;
}
%s
''' % DRIVER_MAIN
write_target("c04", C04)

C05 = '''@import("R33_NATIVE_IO_V1.zag")
// C05 — wall-clock-free timeout via instruction counting: fixed iteration
// budget, no clock syscalls anywhere.
fn vary_expr(input:[]u8, state:[]u8, out:[]u8)i32 {
    if(out.len<input.len){return 1;}
    let budget:i64=200000;
    let acc:i64=0;
    let k:i64=0;
    while(k<budget){
        acc=acc+((k*1103515245+12345)&255);
        k=k+1;
    }
    let i:i32=0;
    while(i<input.len){
        let sh:i64=((i%%8)*8) as i64;
        let by:i64=(acc>>sh)&255;
        out[i]=input[i]^(by as u8);
        i=i+1;
    }
    return 0;
}
%s
''' % DRIVER_MAIN
write_target("c05", C05)

C06 = '''@import("R33_NATIVE_IO_V1.zag")
// C06 — hash map with fixed-order iteration: slots walked 0..n, deterministic.
fn vary_expr(input:[]u8, state:[]u8, out:[]u8)i32 {
    let n:i32=64;
    let keys:[]u8=nio_alloc(n);
    let vals:[]u8=nio_alloc(n);
    let used:[]u8=nio_alloc(n);
    if(keys.len!=n||vals.len!=n||used.len!=n){return 1;}
    let z:i32=0;
    while(z<n){keys[z]=0; vals[z]=0; used[z]=0; z=z+1;}
    let i:i32=0;
    while(i<input.len && i<n){
        let h:i32=(((input[i] as i32)*7+3)%%n+n)%%n;
        let j:i32=0;
        let done:i32=0;
        while(j<n && done==0){
            let s:i32=(h+j)%%n;
            if(used[s]==0){keys[s]=input[i]; vals[s]=i as u8; used[s]=1; done=1;}
            j=j+1;
        }
        i=i+1;
    }
    let o:i32=0;
    let s2:i32=0;
    while(s2<n && o<out.len){
        if(used[s2]!=0){out[o]=keys[s2]^vals[s2]; o=o+1;}
        s2=s2+1;
    }
    nio_free(keys); nio_free(vals); nio_free(used);
    return 0;
}
%s
''' % DRIVER_MAIN
write_target("c06", C06)

print("done")
