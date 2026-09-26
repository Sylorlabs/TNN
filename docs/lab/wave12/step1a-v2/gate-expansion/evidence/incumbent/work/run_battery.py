#!/usr/bin/env python3
"""WI-4 incumbent reference: run the §3 battery (P01-P12) + clean set
(C01,C02,C04,C05,C06) through the fresh arena certifier.

For each module: build dir with the plant source (tier M) + pinned
substrate (tier S), manifest with M/S/BIN records, neutral replay
evidence (REPLAY=PASS inputs so the source rules decide the verdict),
then run the arena certifier and record verdict + firing rules.

Deterministic: fixed bytes everywhere; no RNG.
"""
import hashlib
import os
import subprocess
import sys

HOME = os.path.expanduser("~")
EV = os.path.join(HOME, "workspace/tnn-lab/wave12/step1a-v2/gate-expansion/evidence/incumbent")
WORK = os.path.join(EV, "work")
BAT = os.path.join(WORK, "battery")
ZNC = os.path.join(HOME, "workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1")
TC = os.path.join(WORK, "build1", "thincert_arena")
V1 = os.path.join(HOME, "workspace/tnn-lab/wave12/step1a-no-rng-audit/redteam/plants")
K2 = os.path.join(HOME, "workspace/tnn-lab/wave12/step1a-v2/thin-certifier/k2prime-redteam/plants")
M1S = os.path.join(HOME, "workspace/tnn-lab/wave12/step1a-v2/gate-expansion/evidence/m1/src")
M4C = os.path.join(HOME, "workspace/tnn-lab/wave12/step1a-v2/gate-expansion/evidence/m4/clean")
SUB = os.path.join(HOME, "workspace/tnn-lab/wave12/step1a-v2/thin-certifier/certifier/substrate/R33_NATIVE_IO_V1.zag")

PINNED_SUB_SHA = "e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8"
EXPECTED_TC_SHA = "362089d5a4405b69fe072e1aa8e91481b1237a1852bac9a29d65335c125ebe37"

# (case id, source path, kind label)
PLANTS = [
    ("P01", os.path.join(V1, "plant01.zag"), "getrandom(2) literal 318"),
    ("P02", os.path.join(V1, "plant06.zag"), "clock_gettime literal 228"),
    ("P03", os.path.join(V1, "plant03.zag"), "open(2) of /dev/urandom"),
    ("P04", os.path.join(V1, "plant11.zag"), "uninit heap read into output"),
    ("P05", os.path.join(V1, "plant20.zag"), "get_env_flag env indirection (v1 killer)"),
    ("P06", os.path.join(V1, "plant19.zag"), "ASLR/pointer leak into output"),
    ("P07", os.path.join(M1S, "t_p07.zag"), "rdtsc via ELF child (M1 crew build)"),
    ("P08", os.path.join(V1, "plant16.zag"), "hash-iteration order to output"),
    ("P09", os.path.join(M1S, "t_p09.zag"), "hand-rolled table innocent names (v3 blind plant17 @7b64c89)"),
    ("P10", os.path.join(K2, "plant19", "variation.zag"), "/etc/machine-id via allowlisted file IO (K2' 19)"),
    ("P11", os.path.join(K2, "plant20", "variation.zag"), "_zag_arg(0) path bytes (K2' 20)"),
    ("P12", os.path.join(M1S, "t_p12.zag"), "getrandom invoke-discard (M1 crew build)"),
]
CLEAN = [
    ("C01", os.path.join(M4C, "C01_canonical.zag"), "canonical variation"),
    ("C02", os.path.join(M4C, "C02_state_phrasing.zag"), "state-dependent phrasing"),
    ("C04", None, "pinned-substrate file IO (adapted, see ADAPT_C04)"),
    ("C05", os.path.join(M4C, "C05_step_budget.zag"), "step-budget timeout"),
    ("C06", None, "fixed-order map (adapted, see ADAPT_C06)"),
]

# C04 adapted to the pinned substrate idiom (module-local load helper using
# substrate nio_* calls only; no banned tokens). Based on M4 C04_pinned_io.
ADAPT_C04 = '''@import("R33_NATIVE_IO_V1.zag")

// C04: file IO via pinned substrate allowlist (read-only data files).
// Adapted from M4 C04_pinned_io.zag to the pinned-substrate idiom:
// module-local load helper using only substrate nio_* calls.
fn load_data(dir:[]u8, name:[]u8, buf:[]u8)i64 {
    let root:i64=nio_open_root(dir);
    if(root<0){return -1;}
    let fd:i64=nio_open_child(root,name,0);
    let cr:i64=nio_close(root);
    if(fd<0){return -2;}
    let n:i64=nio_read_exact(fd,buf,buf.len);
    let cc:i64=nio_close(fd);
    if(cc!=0){return -3;}
    return n;
}
fn vary_expr(input:[]u8, state:[]u8, out:[]u8)i32 {
    let buf:[]u8=nio_alloc(256);
    if(buf.len!=256){return 1;}
    let zi:i32=0;
    while(zi<buf.len){buf[zi]=0; zi=zi+1;}
    let n:i64=load_data("data", "phrases.bin", buf);
    if(n<0){nio_free(buf); return 1;}
    let i:i32=0;
    while(i<out.len && i<buf.len){out[i]=buf[i]; i=i+1;}
    nio_free(buf);
    return 0;
}

fn main()i32 {
    _zag_println("C04");
    return 0;
}
'''

# C06 adapted to the pinned substrate idiom: z_alloc_init -> nio_alloc +
# explicit zero loop (canonical init idiom). Based on M4 C06_fixed_order_map.
ADAPT_C06 = '''@import("R33_NATIVE_IO_V1.zag")

// C06: hash map with FIXED-ORDER iteration. Entries are collected and emitted
// in ascending key order (insertion sort over present keys) — iteration order
// is a deterministic function of content, never of table layout. Indexed
// arrays only, innocent names. Adapted from M4 C06_fixed_order_map.zag:
// z_alloc_init -> nio_alloc + explicit zero loop.
fn z_init(n:i32)[]u8 {
    let b:[]u8=nio_alloc(n);
    if(b.len!=n){return b;}
    let i:i32=0;
    while(i<n){b[i]=0; i=i+1;}
    return b;
}
fn tab_slot(k:u8)i32 { return ((k as i32)*37)%64; }
fn vary_expr(input:[]u8, state:[]u8, out:[]u8)i32 {
    let keys:[]u8=z_init(64);
    let vals:[]u8=z_init(64);
    let used:[]u8=z_init(64);
    if(keys.len!=64 || vals.len!=64 || used.len!=64){return 1;}
    let i:i32=0;
    while(i<input.len){
        let h:i32=tab_slot(input[i]);
        keys[h]=input[i]; vals[h]=input[i]; used[h]=1;
        i=i+1;
    }
    let order:[]u8=z_init(64);
    if(order.len!=64){return 1;}
    let cnt:i32=0;
    let s:i32=0;
    while(s<64){
        if(used[s]==1){order[cnt]=keys[s]; cnt=cnt+1;}
        s=s+1;
    }
    let a:i32=0;
    while(a<cnt){
        let m:i32=a;
        let b:i32=a+1;
        while(b<cnt){
            if(order[b]<order[m]){m=b;}
            b=b+1;
        }
        let t:u8=order[a]; order[a]=order[m]; order[m]=t;
        a=a+1;
    }
    let o:i32=0;
    let e:i32=0;
    while(e<cnt && o<out.len){out[o]=order[e]; o=o+1; e=e+1;}
    nio_free(keys); nio_free(vals); nio_free(used); nio_free(order);
    return 0;
}

fn main()i32 {
    _zag_println("C06");
    return 0;
}
'''

NEUTRAL_EVIDENCE = (
    "byte_identical=1\n"
    "varies_with_state=1\n"
    "exit_ok=1\n"
    "rebuild_ok=1\n"
    "runs=8\n"
    "tripwire_v2=PASS\n"
)


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def setup_case(cid, src, label, kind):
    d = os.path.join(BAT, cid)
    os.makedirs(d, exist_ok=True)
    modname = "plant.zag" if kind == "plant" else "clean.zag"
    binname = "plant.bin" if kind == "plant" else "clean.bin"
    dst = os.path.join(d, modname)
    if src is None:
        body = ADAPT_C04 if cid == "C04" else ADAPT_C06
        with open(dst, "w") as f:
            f.write(body)
    else:
        with open(src, "rb") as f:
            data = f.read()
        with open(dst, "wb") as f:
            f.write(data)
    # pinned substrate alongside (flat layout; @import resolves to it)
    subdst = os.path.join(d, "R33_NATIVE_IO_V1.zag")
    with open(SUB, "rb") as f:
        sdata = f.read()
    with open(subdst, "wb") as f:
        f.write(sdata)
    assert sha256_file(subdst) == PINNED_SUB_SHA, "substrate not pinned!"
    # C04 data file
    if cid == "C04":
        datadir = os.path.join(d, "data")
        os.makedirs(datadir, exist_ok=True)
        with open(os.path.join(M4C, "data", "phrases.bin"), "rb") as f:
            pdata = f.read()
        with open(os.path.join(datadir, "phrases.bin"), "wb") as f:
            f.write(pdata)
    # build the module binary with the pinned toolchain (cwd = builddir)
    r = subprocess.run([ZNC, "build", modname, "-o", binname],
                       cwd=d, capture_output=True, text=True, timeout=120)
    built = os.path.exists(os.path.join(d, binname))
    # manifest
    msha = sha256_file(dst)
    bsha = sha256_file(os.path.join(d, binname)) if built else ("0" * 64)
    man = (
        "# MANIFEST -- WI-4 incumbent reference %s (%s)\n"
        "M %s %s\n"
        "S R33_NATIVE_IO_V1.zag %s\n"
        "BIN %s %s\n"
    ) % (cid, label, modname, msha, PINNED_SUB_SHA, binname, bsha)
    with open(os.path.join(d, "MANIFEST.txt"), "w") as f:
        f.write(man)
    with open(os.path.join(d, "evidence.txt"), "w") as f:
        f.write(NEUTRAL_EVIDENCE)
    return d, built, r.returncode


def run_case(cid, kind):
    d = os.path.join(BAT, cid)
    modname = "plant.zag" if kind == "plant" else "clean.zag"
    binname = "plant.bin" if kind == "plant" else "clean.bin"
    att = os.path.join(d, "attestation.txt")
    r = subprocess.run([TC, os.path.join(d, "MANIFEST.txt"), d,
                        os.path.join(d, binname),
                        os.path.join(d, "evidence.txt"), att],
                       capture_output=True, text=True, timeout=120)
    verdict = "?"
    rules = []
    with open(att) as f:
        for line in f:
            line = line.strip()
            if line.startswith("verdict="):
                verdict = line.split("=", 1)[1]
            elif "=FAIL:" in line:
                rules.append(line)
    return r.returncode, verdict, rules

def main():
    tcsha = sha256_file(TC)
    print("arena certifier sha:", tcsha, "MATCH" if tcsha == EXPECTED_TC_SHA else "MISMATCH")
    assert tcsha == EXPECTED_TC_SHA, "arena binary SHA mismatch"
    os.makedirs(BAT, exist_ok=True)
    rows = []
    for cid, src, label in PLANTS:
        d, built, brc = setup_case(cid, src, label, "plant")
        rc, verdict, rules = run_case(cid, "plant")
        rows.append((cid, "plant", label, built, brc, rc, verdict, rules))
        print("%s plant %-42s built=%s brc=%d -> rc=%d verdict=%s rules=%s" % (
            cid, label[:42], built, brc, rc, verdict, rules if rules else "-"))
    for cid, src, label in CLEAN:
        d, built, brc = setup_case(cid, src, label, "clean")
        rc, verdict, rules = run_case(cid, "clean")
        rows.append((cid, "clean", label, built, brc, rc, verdict, rules))
        print("%s clean %-42s built=%s brc=%d -> rc=%d verdict=%s rules=%s" % (
            cid, label[:42], built, brc, rc, verdict, rules if rules else "-"))
    with open(os.path.join(WORK, "results.tsv"), "w") as f:
        f.write("case\tkind\tbuilt\tbuild_rc\tcert_rc\tverdict\tfailed_rules\n")
        for cid, kind, label, built, brc, rc, verdict, rules in rows:
            f.write("%s\t%s\t%s\t%d\t%d\t%s\t%s\n" % (
                cid, kind, built, brc, rc, verdict, "; ".join(rules)))


if __name__ == "__main__":
    main()
