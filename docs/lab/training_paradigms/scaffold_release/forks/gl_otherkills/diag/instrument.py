#!/usr/bin/env python3
"""FL2 other-kills diagnosis: instrument T-DEF (arm_gl) patched copies.

Copies ~/workspace/fl2rt/harnesses/default_<X>/ to diag build dirs, inserts
DIAG trace instrumentation (metrics-only, no behavior change), appends the
DIAG helper fns, compiles with znc, runs twice, cmp-checks, saves traces.

Usage: python3 instrument.py   (run from ~/workspace/fl2other/diag/)
"""
import os
import shutil
import subprocess
import sys

ZNC = os.path.expanduser("~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1")
DIAG = os.path.expanduser("~/workspace/fl2other/diag")
HARN = os.path.expanduser("~/workspace/fl2rt/harnesses")
BUILD = os.path.join(DIAG, "build")
TRACES = os.path.join(DIAG, "traces")

CELLS = ["A", "B", "C", "D", "E", "F", "FID"]

DIAG_FNS = r'''
// ---- DIAG instrumentation helpers (metrics only; read state, mutate nothing) ----
fn diag_i(b:[]u8,at:i32,v:i32)i32 {
    b[at]=44;at=at+1;
    let neg:i32=0;let x:i64=v as i64;
    if(x<0){neg=1;x=0-x;}
    if(neg==1){b[at]=45;at=at+1;}
    let d:[]u8=tn_alloc(12);
    let n:i32=0;
    if(x==0){d[0]=48;n=1;}
    while(x>0){d[n]=(((x%10) as i32)+48) as u8;x=x/10;n=n+1;}
    let i:i32=n-1;
    while(i>=0){b[at]=d[i];at=at+1;i=i-1;}
    tn_free(d);
    return at;
}

fn diag_k3(ep:i32,act:i32,aa:i32,sl:i32,s0:i32,s1:i32,s2:i32,sv:i32,q:i32,pv:i32,cm:i32,pm:i32)void {
    let b:[]u8=tn_alloc(192);
    b[0]=68;b[1]=73;b[2]=65;b[3]=71;b[4]=75;b[5]=51;
    let at:i32=6;
    at=diag_i(b,at,ep);at=diag_i(b,at,act);at=diag_i(b,at,aa);at=diag_i(b,at,sl);
    at=diag_i(b,at,s0);at=diag_i(b,at,s1);at=diag_i(b,at,s2);at=diag_i(b,at,sv);
    at=diag_i(b,at,q);at=diag_i(b,at,pv);at=diag_i(b,at,cm);at=diag_i(b,at,pm);
    b[at]=10;at=at+1;
    _zag_print(b[0..at]);
    tn_free(b);
    return;
}

fn diag_pinstall(ep:i32,stated:i32,prov:i32)void {
    let b:[]u8=tn_alloc(64);
    b[0]=68;b[1]=73;b[2]=65;b[3]=71;b[4]=80;b[5]=73;b[6]=78;
    let at:i32=7;
    at=diag_i(b,at,ep);at=diag_i(b,at,stated);at=diag_i(b,at,prov);
    b[at]=10;at=at+1;
    _zag_print(b[0..at]);
    tn_free(b);
    return;
}

fn diag_promote(ep:i32,revoke_step:i32,prov:i32,perm:i32)void {
    let b:[]u8=tn_alloc(80);
    b[0]=68;b[1]=73;b[2]=65;b[3]=71;b[4]=80;b[5]=82;b[6]=79;b[7]=77;
    let at:i32=8;
    at=diag_i(b,at,ep);at=diag_i(b,at,revoke_step);at=diag_i(b,at,prov);at=diag_i(b,at,perm);
    b[at]=10;at=at+1;
    _zag_print(b[0..at]);
    tn_free(b);
    return;
}

fn diag_wedge(ep:i32,q:i32)void {
    let b:[]u8=tn_alloc(48);
    b[0]=68;b[1]=73;b[2]=65;b[3]=71;b[4]=87;b[5]=69;b[6]=68;b[7]=71;b[8]=69;
    let at:i32=9;
    at=diag_i(b,at,ep);at=diag_i(b,at,q);
    b[at]=10;at=at+1;
    _zag_print(b[0..at]);
    tn_free(b);
    return;
}
'''


def one_replace(src, old, new, where):
    n = src.count(old)
    if n != 1:
        raise SystemExit(f"anchor x{n} (want 1) in {where}: {old[:70]!r}")
    return src.replace(old, new)


def instrument(learner_src):
    s = learner_src
    # E1: declare diag_surv next to aa
    s = one_replace(
        s,
        "                let aa:i32=0;",
        "                let aa:i32=0;\n                let diag_surv:i32=-1;",
        "aa-decl",
    )
    # E2: capture survivor when one is selected
    s = one_replace(
        s,
        "                    if(surv>=0){",
        "                    if(surv>=0){\n                        diag_surv=surv;",
        "surv-capture",
    )
    # E3: per-episode trace at end of the revocation window block
    old_tail = (
        "                        if(r2!=TN_OK){rc=r2;}\n"
        "                    }\n"
        "                }\n"
        "            }\n"
        "        }\n"
        "        if(rc==TN_OK && kind==4){"
    )
    new_tail = (
        "                        if(r2!=TN_OK){rc=r2;}\n"
        "                    }\n"
        "                }\n"
        "                diag_k3(ep,act,aa,sig_live,sig0,sig1,sig2,diag_surv,"
        "tn_count_used(qkey,TN_NQUAR),provisional,committed[0] as i32,permanent);\n"
        "            }\n"
        "        }\n"
        "        if(rc==TN_OK && kind==4){"
    )
    s = one_replace(s, old_tail, new_tail, "k3-tail")
    # E4: E14 pinstall decision
    s = one_replace(
        s,
        "                if(r2==TN_OK){provisional=stated;}",
        "                if(r2==TN_OK){provisional=stated;}\n"
        "                diag_pinstall(ep,stated,provisional);",
        "pinstall",
    )
    # E5: E48 promote-check inputs
    s = one_replace(
        s,
        "        if(ep==48 && revoke_step<0 && provisional>=0){",
        "        diag_promote(ep,revoke_step,provisional,permanent);\n"
        "        if(ep==48 && revoke_step<0 && provisional>=0){",
        "promote",
    )
    # E6: wedge event after the kind-3 contest action (both contest spellings)
    contest_old = (
        "            if(rc==TN_OK && act==ACT_CONTEST){\n"
        "                if(auth!=0){rc=tn_audit(audit,&acount,ep,TN_OP_REFUSE,auth,1);}\n"
        "                if(rc==TN_OK){rc=tn_do_contest(mkey,mval,mflag,qkey,qval,qflag,TN_NQUAR,ep,audit,&acount,k,v);}\n"
        "            }"
    )
    contest_new = (
        "            if(rc==TN_OK && act==ACT_CONTEST){\n"
        "                if(auth!=0){rc=tn_audit(audit,&acount,ep,TN_OP_REFUSE,auth,1);}\n"
        "                if(rc==TN_OK){rc=tn_do_contest(mkey,mval,mflag,qkey,qval,qflag,TN_NQUAR,ep,audit,&acount,k,v);}\n"
        "                if(rc!=TN_OK){diag_wedge(ep,tn_count_used(qkey,TN_NQUAR));}\n"
        "            }"
    )
    if contest_old in s:
        s = one_replace(s, contest_old, contest_new, "wedge-contest")
    else:
        fault_old = (
            "            if(rc==TN_OK && act==ACT_CONTEST){\n"
            "                if(auth!=0){rc=tn_audit(audit,&acount,ep,TN_OP_REFUSE,auth,1);}\n"
            "                if(rc==TN_OK){rc=rt_fault_contest(mkey,mval,mflag,qkey,qval,qflag,TN_NQUAR,ep,audit,&acount,k,v);}\n"
            "            }"
        )
        fault_new = (
            "            if(rc==TN_OK && act==ACT_CONTEST){\n"
            "                if(auth!=0){rc=tn_audit(audit,&acount,ep,TN_OP_REFUSE,auth,1);}\n"
            "                if(rc==TN_OK){rc=rt_fault_contest(mkey,mval,mflag,qkey,qval,qflag,TN_NQUAR,ep,audit,&acount,k,v);}\n"
            "                if(rc!=TN_OK){diag_wedge(ep,tn_count_used(qkey,TN_NQUAR));}\n"
            "            }"
        )
        s = one_replace(s, fault_old, fault_new, "wedge-fault")
    s = s + DIAG_FNS
    return s


def main():
    os.makedirs(BUILD, exist_ok=True)
    os.makedirs(TRACES, exist_ok=True)
    for cell in CELLS:
        d = os.path.join(BUILD, cell)
        if os.path.isdir(d):
            shutil.rmtree(d)
        shutil.copytree(os.path.join(HARN, "default_" + cell), d)
        lp = os.path.join(d, "gl_learner.zag")
        with open(lp) as f:
            src = f.read()
        with open(lp, "w") as f:
            f.write(instrument(src))
        # no rng tokens
        low = open(lp).read().lower()
        for tok in ("rng", "rand(", "seed"):
            if tok in low:
                raise SystemExit(f"forbidden token {tok} in {cell}")
        r = subprocess.run(
            [ZNC, "gl_learner.zag", "-o", "diag_bin"],
            cwd=d, capture_output=True, text=True, timeout=300,
        )
        if r.returncode != 0:
            raise SystemExit(f"znc failed for {cell}:\n{r.stderr[-3000:]}")
        outs = []
        for i in (1, 2):
            r = subprocess.run(
                ["./diag_bin"], cwd=d, capture_output=True, text=True, timeout=120,
            )
            if r.returncode != 0:
                raise SystemExit(f"run failed for {cell} run{i}:\n{r.stderr[-2000:]}")
            outs.append(r.stdout)
            with open(os.path.join(TRACES, f"{cell}_run{i}.txt"), "w") as f:
                f.write(r.stdout)
        if outs[0] != outs[1]:
            raise SystemExit(f"NON-DETERMINISTIC output in {cell}")
        print(f"{cell}: built, ran twice, byte-identical, trace={len(outs[0])} bytes")
    print("ALL CELLS OK")


if __name__ == "__main__":
    main()
