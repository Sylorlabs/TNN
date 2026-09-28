#!/usr/bin/env python3
"""H-1 build: exact-anchored patch of gl_learner.zag, per-cell builds, 2x runs, verify."""
import os, re, shutil, subprocess, sys

HERE = os.path.expanduser("~/workspace/threeworlds/h1")
BUILD = os.path.join(HERE, "build")
EV = os.path.join(HERE, "evidence")
ZNC = os.path.expanduser("~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1")
BASES = {
    "B": "/home/hatch/workspace/fl2rt/harnesses/default_B",
    "FID": "/home/hatch/workspace/fl2rt/harnesses/default_FID",
}

CONSTS = """const H1_CLAIM_CAP:i32=256;
const H1_CK_AA:i32=1;
const H1_SRC_WORLD:i32=1;
const H1_FORGE_AA_EP:i32=0;
const H1_FORGE_AUDITOP:i32=0;
const H1_NO_ENDO:i32=0;
"""

HELPERS = """// H-1 claim ledger: world signals are CLAIMS (kind, source, episode,
// bound flag), never facts. Separate arena; never printed; never consulted
// by the audit-reporting checks.
fn h1_claim_add(cbuf:[]u8,ccount:*i32,ep:i32,kind:i32,src:i32)i32 {
    let n:i32=ccount.*;
    if(n<0 || n>=H1_CLAIM_CAP){return TN_BAD;}
    tn_s32(cbuf,n*16,kind);
    tn_s32(cbuf,n*16+4,src);
    tn_s32(cbuf,n*16+8,ep);
    tn_s32(cbuf,n*16+12,0);
    ccount.*=n+1;
    return TN_OK;
}

fn h1_claim_mark_bound(cbuf:[]u8,n:i32,ep:i32)void {
    let i:i32=0;
    while(i<n){
        if(tn_g32(cbuf,i*16+8)==ep && tn_g32(cbuf,i*16)==H1_CK_AA){
            tn_s32(cbuf,i*16+12,1);
        }
        i=i+1;
    }
    return;
}

"""

NEW_SUBBLOCK = """            if(rc==TN_OK && permanent==0 && ep>=15 && ep<=48){
                let aa:i32=0;
                if(ep>=29 && ep<=48 && RT_MODE!=2 && RT_MODE!=3){aa=1;}
                if(H1_FORGE_AA_EP>0 && ep==H1_FORGE_AA_EP){aa=1;}
                if(aa==1){
                    let h1cr:i32=h1_claim_add(claim,&ccount,ep,H1_CK_AA,H1_SRC_WORLD);
                    if(h1cr!=TN_OK){rc=h1cr;}
                }
                let sig_live:i32=gl_contradict(k,v,v_old,aa,mkey,mval,mflag,qkey,qval,qflag);
                let sig0:i32=99;let sig1:i32=99;let sig2:i32=99;
                let p:i32=0;
                while(p<3){
                    if(p!=act){
                        tn_copy(wkey,pkey,TN_NMAIN*4);tn_copy(wval,pval,TN_NMAIN*4);tn_copy(wflag,pflag,TN_NMAIN*4);
                        tn_copy(wqkey,pqkey,TN_NQUAR*4);tn_copy(wqval,pqval,TN_NQUAR*4);tn_copy(wqflag,pqflag,TN_NQUAR*4);
                        let pr:i32=-2;
                        if(p==ACT_OVERWRITE){pr=tn_sim_overwrite(wkey,wval,wflag,k,v);}
                        if(p==ACT_CONTEST){pr=tn_sim_contest(wkey,wflag,wqkey,wqval,wqflag,TN_NQUAR,k,v);}
                        if(p==ACT_REKEY){pr=tn_sim_rekey(wkey,wval,wflag,k,v,TN_REKEY_BASE+777777);}
                        let sp:i32=-1;
                        if(pr>=0){sp=gl_contradict(k,v,v_old,aa,wkey,wval,wflag,wqkey,wqval,wqflag);}
                        if(p==0){sig0=sp;}
                        if(p==1){sig1=sp;}
                        if(p==2){sig2=sp;}
                    }
                    p=p+1;
                }
                let law_holds:i32=0;
                if(tn_main_has(mkey,mval,TN_NMAIN,k,v)==1){law_holds=1;}
                if(tn_quar_has(qkey,qval,TN_NQUAR,k,v)==1){law_holds=1;}
                if(law_holds==0){law_fail=1;}
                let revoke_now:i32=0;
                if(law_holds==0 && revoke_step<0 && provisional>=0){revoke_now=1;}
                if(H1_NO_ENDO==1 && aa==0){revoke_now=0;}
                if(revoke_now==1){
                    let surv:i32=-1;
                    if(sig0>=1){surv=0;}
                    if(sig1>=1 && surv<0){surv=1;}
                    if(sig2>=1 && surv<0){surv=2;}
                    if(surv>=0){
                        let faux:i32=-3;
                        if(aa==1){
                            faux=-1;
                            h1_claim_mark_bound(claim,ccount,ep);
                        }
                        let r2:i32=tn_audit(audit,&acount,ep,TN_OP_SCAFFOLD,act,faux);
                        if(r2==TN_OK){r2=tn_audit(audit,&acount,ep,TN_OP_UNINSTALL_PROVISIONAL,0,act);}
                        if(r2==TN_OK){r2=tn_audit(audit,&acount,ep,TN_OP_COMMIT,1,surv);}
                        if(r2==TN_OK){
                            provisional=-1;
                            committed[0]=surv as u8;
                            if(revoke_step<0){revoke_step=ep;}
                        }
                        if(r2!=TN_OK){rc=r2;}
                    }
                }
            }
        }
"""

FORGE_AUDITOP = """        if(H1_FORGE_AUDITOP==1 && ep==35){
            let h1fr:i32=tn_audit(audit,&acount,35,TN_OP_SCAFFOLD,2,-1);
            if(h1fr!=TN_OK){rc=h1fr;}
        }
        if(H1_FORGE_AUDITOP==2 && ep==35){
            let h1fr:i32=tn_audit(audit,&acount,35,TN_OP_UNINSTALL_PROVISIONAL,0,2);
            if(h1fr!=TN_OK){rc=h1fr;}
        }
"""

def replace_once(src, old, new, what):
    n = src.count(old)
    assert n == 1, f"anchor {what}: found {n}, want 1"
    return src.replace(old, new, 1)

def patch_learner(base_learner_path):
    with open(base_learner_path) as f:
        src = f.read()
    # P1: consts after import
    src = replace_once(src, '@import("gl_substrate.zag")\n',
                       '@import("gl_substrate.zag")\n' + CONSTS, "P1 consts")
    # P2: helpers before arm_gl
    src = replace_once(src, "fn arm_gl(stated:i32,teach_aux:i32,px:[]u8)i32 {",
                       HELPERS + "fn arm_gl(stated:i32,teach_aux:i32,px:[]u8)i32 {", "P2 helpers")
    # P3: locals
    src = replace_once(src,
        "    let acount:i32=0;\n    let has_rule:i32=0;let provisional:i32=-1;let permanent:i32=0;",
        "    let acount:i32=0;\n    let claim:[]u8=tn_alloc(H1_CLAIM_CAP*16);\n    let ccount:i32=0;\n    let law_fail:i32=0;\n    let has_rule:i32=0;let provisional:i32=-1;let permanent:i32=0;",
        "P3 locals")
    # P4: sub-block replacement via slice between unique anchors
    start_a = "            if(rc==TN_OK && permanent==0 && ep>=15 && ep<=48){"
    end_a = "        if(rc==TN_OK && kind==4){"
    i = src.index(start_a)
    j = src.index(end_a, i)
    old_block = src[i:j]
    assert "if(sig_live==-1){" in old_block, "P4: old trigger missing"
    assert old_block.count("if(sig_live==-1){") == 1
    src = src[:i] + NEW_SUBBLOCK + src[j:]
    # P5: promote gate
    src = replace_once(src, "        if(ep==48 && revoke_step<0 && provisional>=0){",
                       "        if(ep==48 && revoke_step<0 && provisional>=0 && law_fail==0){", "P5 promote")
    # P6: forged audit-op injection
    src = replace_once(src,
        "        if(rc!=TN_OK){badep=1;}\n        ep=ep+1;\n    }\n    let exp_revoke_step:i32=-1;",
        FORGE_AUDITOP + "        if(rc!=TN_OK){badep=1;}\n        ep=ep+1;\n    }\n    let exp_revoke_step:i32=-1;",
        "P6 forgeauditop")
    # P7: free claim arena
    src = replace_once(src, "    tn_free(audit);tn_free(committed);",
                       "    tn_free(audit);tn_free(committed);tn_free(claim);", "P7 free")
    assert "if(sig_live==-1){" not in src, "old trigger still present"
    assert "law_fail" in src and "h1_claim_add" in src
    return src

def set_const(src, name, val):
    pat = re.compile(r"const %s:i32=\d+;" % re.escape(name))
    new, n = pat.subn("const %s:i32=%d;" % (name, val), src)
    assert n == 1, f"const {name}: {n}"
    return new

MAIN_TMPL = """fn main()i32 {
    let f:i32=0;
    f=f+arm_gl(%s);
    _zag_print("TN_FAILURES,");
    let s:[]u8=_zag_i64_to_str(f as i64);_zag_print(s);tn_free(s);
    _zag_println("");
    _zag_print("RT_DONE,");_zag_print("%s");_zag_println("");
    return (f!=0) as i32;
}
"""

CELLS = [
    # name, base, arm_call, rtdone, const overrides
    ("H1_FID_H", "FID", 'ACT_CONTEST,0,"glh_"', "h1_fid_h", {}),
    ("H1_FID_L", "FID", 'ACT_REKEY,1,"gll_"', "h1_fid_l", {}),
    ("H1_B", "B", None, None, {}),  # keep base main
    ("H1_PSH", "B", 'ACT_CONTEST,0,"psh_"', "h1_psh", {}),
    ("W3_H1", "FID", 'ACT_CONTEST,0,"w3h1_"', "w3_h1", {"H1_FORGE_AA_EP": 20}),
    ("W3_H2", "B", 'ACT_CONTEST,0,"w3h2_"', "w3_h2", {"H1_FORGE_AA_EP": 29}),
    ("W3_H3", "FID", 'ACT_CONTEST,0,"w3h3_"', "w3_h3", {"H1_FORGE_AA_EP": 30}),
    ("W3_H4", "FID", 'ACT_CONTEST,0,"w3h4_"', "w3_h4", {"H1_FORGE_AUDITOP": 1}),
    ("W3_H5", "FID", 'ACT_CONTEST,0,"w3h5_"', "w3_h5", {"H1_FORGE_AUDITOP": 2}),
    ("W3_L2", "B", 'ACT_REKEY,1,"w3l2_"', "w3_l2", {"H1_FORGE_AA_EP": 15}),
    ("W3_L1", "B", 'ACT_REKEY,1,"w3l1_"', "w3_l1", {"H1_NO_ENDO": 1, "H1_FORGE_AA_EP": 35}),
    ("W3_H6", "B", 'ACT_CONTEST,0,"w3h6_"', "w3_h6", {"H1_NO_ENDO": 1, "H1_FORGE_AA_EP": 35}),
]

def sha256_file(p):
    import hashlib
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def rng_scan(src, cell):
    bad = ["_zag_random", "rand(", "srand(", "RDRAND", "rdtsc(", "getentropy", "/dev/urandom"]
    hits = [t for t in bad if t in src]
    assert not hits, f"{cell}: RNG tokens {hits}"

def build_and_run(cell):
    name, base, arm_call, rtdone, overrides = cell
    bdir = os.path.join(BUILD, name)
    if os.path.exists(bdir):
        shutil.rmtree(bdir)
    os.makedirs(bdir)
    shutil.copy(os.path.join(BASES[base], "gl_substrate.zag"), bdir)
    learner_src = patch_learner(os.path.join(BASES[base], "gl_learner.zag"))
    for k, v in overrides.items():
        learner_src = set_const(learner_src, k, v)
    if arm_call is not None:
        idx = learner_src.index("fn main()i32 {")
        learner_src = learner_src[:idx] + MAIN_TMPL % (arm_call, rtdone)
    rng_scan(learner_src, name)
    lp = os.path.join(bdir, "gl_learner.zag")
    with open(lp, "w") as f:
        f.write(learner_src)
    r = subprocess.run([ZNC, "gl_learner.zag", "--no-zagd", "--no-analyze",
                        "--no-foreground-cache", "-o", "rtbin"],
                       cwd=bdir, capture_output=True, text=True, timeout=300)
    assert r.returncode == 0, f"{name}: build failed\n{r.stderr[-2000:]}"
    outs = []
    rcs = []
    for run in (1, 2):
        r = subprocess.run(["./rtbin"], cwd=bdir, capture_output=True, text=True, timeout=120)
        assert r.returncode in (0, 1), f"{name}: run{run} rc={r.returncode}"
        p = os.path.join(bdir, f"run{run}.txt")
        with open(p, "w") as f:
            f.write(r.stdout)
        outs.append(r.stdout)
        rcs.append(r.returncode)
    assert outs[0] == outs[1], f"{name}: runs differ!"
    assert rcs[0] == rcs[1], f"{name}: rc differs across runs!"
    # evidence
    edir = os.path.join(EV, name)
    os.makedirs(edir, exist_ok=True)
    shutil.copy(os.path.join(bdir, "run1.txt"), os.path.join(edir, "run1.txt"))
    shutil.copy(os.path.join(bdir, "run2.txt"), os.path.join(edir, "run2.txt"))
    with open(os.path.join(edir, "meta.txt"), "w") as f:
        f.write(f"cell={name} base={base} overrides={overrides}\n")
        f.write(f"learner_sha={sha256_file(lp)}\n")
        f.write(f"substrate_sha={sha256_file(os.path.join(bdir,'gl_substrate.zag'))}\n")
        f.write(f"run_sha={sha256_file(os.path.join(bdir,'run1.txt'))}\n")
        f.write("runs_byte_identical=1\n")
        f.write(f"exit_rc={rcs[0]}\n")
    print(f"OK {name}: built, 2 runs byte-identical", flush=True)
    return outs[0]

def parse_checks(out):
    d = {}
    for line in out.splitlines():
        m = re.match(r"^TN_CHECK,([^,]+),(-?\d+),(-?\d+)$", line)
        if m:
            d[m.group(1)] = (int(m.group(2)), int(m.group(3)))
    return d

def stream_lines(out, px):
    return [l for l in out.splitlines()
            if re.match(r"^(TN_CHECK|RT_FACT),%s_" % re.escape(px), l)]

def main():
    os.makedirs(BUILD, exist_ok=True)
    os.makedirs(EV, exist_ok=True)
    want = sys.argv[1].split(",") if len(sys.argv) > 1 else None
    outs = {}
    for cell in CELLS:
        if want and cell[0] not in want:
            continue
        outs[cell[0]] = build_and_run(cell)
    # save summary
    with open(os.path.join(EV, "cells.txt"), "w") as f:
        for cell in CELLS:
            f.write(cell[0] + "\n")
    print("ALL CELLS BUILT AND DETERMINISTIC")

if __name__ == "__main__":
    main()
