#!/usr/bin/env python3
"""RT-E fork battery: patch harness copies per fork/cell, build, run twice.

Base: ~/workspace/fl2rt/harnesses/default_E/ (canonical + RT2 E-cell
instrumentation; verified by diff). Fork patches are applied by
exact-anchor replacement with asserted hit counts. Pure-Zag mechanisms;
this script is glue only.
"""
import hashlib
import os
import re
import shutil
import subprocess
import sys

ZNC = os.path.expanduser("~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1")
ROOT = os.path.dirname(os.path.abspath(__file__))
HARNESS = os.path.expanduser("~/workspace/fl2rt/harnesses/default_E")
BUILD = os.path.join(ROOT, "build")
EV = os.path.join(ROOT, "evidence")

# ---------------------------------------------------------------- patches

SUB_REPERTOIRE = """const ACT_REKEY:i32=2;
// ---- Executable-repertoire invariant (fork F1/F2) ----
// The learner's executable repertoire: ids 0..GL_NACT-1 each name a
// procedure the learner can execute (kind-3 action branch + sim twin).
// Commitments (install or commit) range over this repertoire —
// "commitments range over procedures I can execute".
const GL_NACT:i32=3;
fn gl_can_execute(pol:i32)i32 {
    if(pol>=0 && pol<GL_NACT){return 1;}
    return 0;
}
"""

SUB_PROBE_F1 = """const ACT_REKEY:i32=2;
const ACT_VERIFY:i32=3;
// ---- Executable-repertoire invariant (fork F1 + probe) ----
const GL_NACT:i32=4;
fn gl_can_execute(pol:i32)i32 {
    if(pol>=0 && pol<GL_NACT){return 1;}
    return 0;
}
// Probe procedure: audited read-back of the quarantine record for (k,v).
const TN_OP_VERIFY:i32=19;
fn tn_do_verify(qkey:[]u8,qval:[]u8,qflag:[]u8,nq:i32,step:i32,abuf:[]u8,acount:*i32,k:i32,v:i32)i32 {
    let hit:i32=tn_quar_has_flag(qkey,qval,qflag,nq,k,v);
    let r:i32=tn_audit(abuf,acount,step,TN_OP_VERIFY,hit,0);
    if(r!=TN_OK){return r;}
    return TN_OK;
}
"""

SUB_PROBE_R1 = """const ACT_REKEY:i32=2;
const ACT_VERIFY:i32=3;
// Probe procedure: audited read-back of the quarantine record for (k,v).
const TN_OP_VERIFY:i32=19;
fn tn_do_verify(qkey:[]u8,qval:[]u8,qflag:[]u8,nq:i32,step:i32,abuf:[]u8,acount:*i32,k:i32,v:i32)i32 {
    let hit:i32=tn_quar_has_flag(qkey,qval,qflag,nq,k,v);
    let r:i32=tn_audit(abuf,acount,step,TN_OP_VERIFY,hit,0);
    if(r!=TN_OK){return r;}
    return TN_OK;
}
"""

# Shared refusal-handling machinery (all forks): with no installed rule,
# kind-3 episodes are inert-but-audited, never badep.
L_NORULE_1_OLD = """            let act:i32=gl_select(provisional,committed);
            if(act<0){badep=1;}
"""
L_NORULE_1_NEW = """            let act:i32=gl_select(provisional,committed);
            let no_rule:i32=0;
            if(provisional<0 && (committed[0] as i32)==TN_UNCONNECTED){no_rule=1;}
            if(act<0 && no_rule==0){badep=1;}
"""

L_GATE_F1F2_OLD = """        if(ep==14){
            let l1_ok:i32=1;let l2_ok:i32=1;
            if(has_rule==1 && cal_score==4 && l1_ok==1 && l2_ok==1){
                let r2:i32=tn_audit(audit,&acount,ep,TN_OP_PINSTALL,0,stated);
                if(r2==TN_OK){provisional=stated;}
                if(r2!=TN_OK){rc=r2;}
            } else {
                let r3:i32=tn_audit(audit,&acount,ep,TN_OP_WITHHOLD,0,cal_score);
                if(r3!=TN_OK){rc=r3;}
            }
        }
"""
L_GATE_F1F2_NEW = """        if(ep==14){
            let l1_ok:i32=1;let l2_ok:i32=1;
            let gate_exec:i32=gl_can_execute(stated);
            let wreason:i32=0;
            if(gate_exec==0){wreason=1;}
            if(has_rule==1 && cal_score==4 && l1_ok==1 && l2_ok==1 && gate_exec==1){
                let r2:i32=tn_audit(audit,&acount,ep,TN_OP_PINSTALL,0,stated);
                if(r2==TN_OK){provisional=stated;}
                if(r2!=TN_OK){rc=r2;}
            } else {
                let r3:i32=tn_audit(audit,&acount,ep,TN_OP_WITHHOLD,wreason,cal_score);
                if(r3!=TN_OK){rc=r3;}
            }
        }
"""
L_GATE_R1_NEW = """        if(ep==14){
            let l1_ok:i32=1;let l2_ok:i32=1;
            let wl_ok:i32=0;
            if(stated==0 || stated==1 || stated==2){wl_ok=1;}
            let wreason:i32=0;
            if(wl_ok==0){wreason=2;}
            if(has_rule==1 && cal_score==4 && l1_ok==1 && l2_ok==1 && wl_ok==1){
                let r2:i32=tn_audit(audit,&acount,ep,TN_OP_PINSTALL,0,stated);
                if(r2==TN_OK){provisional=stated;}
                if(r2!=TN_OK){rc=r2;}
            } else {
                let r3:i32=tn_audit(audit,&acount,ep,TN_OP_WITHHOLD,wreason,cal_score);
                if(r3!=TN_OK){rc=r3;}
            }
        }
"""

L_LOOP_F1F2_OLD = "                while(p<3){"
L_LOOP_F1F2_NEW = "                while(p<GL_NACT){"

L_COMMIT_F1_OLD = "                    if(surv>=0){"
L_COMMIT_F1_NEW = "                    if(surv>=0 && gl_can_execute(surv)==1){"

# Probe-only learner wiring (RTX cells): VERIFY procedure support.
L_PROBE_DISPATCH_OLD = """            if(rc==TN_OK && act==ACT_OVERWRITE && no_rule==0){
                rc=tn_do_overwrite(mkey,mval,mflag,TN_NMAIN,ep,audit,&acount,k,v);
            }
"""
L_PROBE_DISPATCH_NEW = """            if(rc==TN_OK && act==ACT_OVERWRITE && no_rule==0){
                rc=tn_do_overwrite(mkey,mval,mflag,TN_NMAIN,ep,audit,&acount,k,v);
            }
            if(rc==TN_OK && act==ACT_VERIFY && no_rule==0){
                let r5:i32=tn_do_verify(qkey,qval,qflag,TN_NQUAR,ep,audit,&acount,k,v);
                if(r5!=TN_OK){rc=r5;}
            }
"""
L_PROBE_CAL_OLD = """                } else {
                    let s:i32=tn_first_free(skey,TN_NMAIN);
"""
L_PROBE_CAL_NEW = """                } else if(stated==ACT_VERIFY){
                    let vqs:i32=tn_sim_contest(skey,sflag,sqkey,sqval,sqflag,TN_NQUAR,k,v);
                    if(vqs>=0 && tn_sim_verify(sqkey,sqval,sqflag,TN_NQUAR,k,v)==0){ok=1;}
                    if(ok==1 && tn_count_used(sqkey,TN_NQUAR)!=tn_count_used(qkey,TN_NQUAR)+1){ok=0;}
                    if(ok==1 && tn_main_val(skey,sval,TN_NMAIN,k)!=v_old){ok=0;}
                } else {
                    let s:i32=tn_first_free(skey,TN_NMAIN);
"""
L_PROBE_SIM_OLD = "// GL-SIM-REGION-END"
L_PROBE_SIM_NEW = """fn tn_sim_verify(wqkey:[]u8,wqval:[]u8,wqflag:[]u8,nq:i32,k:i32,v:i32)i32 {
    if(tn_quar_has_flag(wqkey,wqval,wqflag,nq,k,v)==1){return 0;}
    return -1;
}
// GL-SIM-REGION-END"""
L_PROBE_SURV_OLD = "                        if(p==ACT_REKEY){pr=tn_sim_rekey(wkey,wval,wflag,k,v,TN_REKEY_BASE+777777);}"
L_PROBE_SURV_NEW = ("                        if(p==ACT_REKEY){pr=tn_sim_rekey(wkey,wval,wflag,k,v,TN_REKEY_BASE+777777);}\n"
                    "                        if(p==ACT_VERIFY){pr=tn_sim_verify(wqkey,wqval,wqflag,TN_NQUAR,k,v);}")
L_PROBE_SIG_OLD = "                let sig0:i32=99;let sig1:i32=99;let sig2:i32=99;"
L_PROBE_SIG_NEW = "                let sig0:i32=99;let sig1:i32=99;let sig2:i32=99;let sig3:i32=99;"
L_PROBE_SIGP_OLD = "                        if(p==2){sig2=sp;}"
L_PROBE_SIGP_NEW = "                        if(p==2){sig2=sp;}\n                        if(p==3){sig3=sp;}"
L_PROBE_SEL_OLD = "                    if(sig2>=1 && surv<0){surv=2;}"
L_PROBE_SEL_NEW = ("                    if(sig2>=1 && surv<0){surv=2;}\n"
                   "                    if(sig3>=1 && surv<0){surv=3;}")

# Extra FACT lines: withhold count + reason (metrics only).
FACT_HELPER_ADD = """
fn rt_first_slot1(abuf:[]u8,n:i32,op:i32)i32 {
    let i:i32=0;
    while(i<n){
        if(tn_g32(abuf,i*16+4)==op){return tn_g32(abuf,i*16+8);}
        i=i+1;
    }
    return -1;
}
"""
FACTS_ADD_OLD = '    rt_fact(px,"badep",badep);\n'
FACTS_ADD_NEW = ('    rt_fact(px,"badep",badep);\n'
                 '    rt_fact(px,"withhold_n",tn_audit_count_op(audit,acount,TN_OP_WITHHOLD));\n'
                 '    rt_fact(px,"withhold_reason",rt_first_slot1(audit,acount,TN_OP_WITHHOLD));\n')

# ---------------------------------------------------------------- cells

MAINS = {
    "fid": None,  # canonical main, extracted from canon_learner.zag
    "rte": 'f=f+arm_gl(7,0,"rte_");',
    "rte2": 'f=f+arm_gl(13,0,"rte2_");',
    "rtx": 'f=f+arm_gl(3,0,"rtx_");',
}
CELL_PX = {"fid": "fid", "rte": "rte_", "rte2": "rte2_", "rtx": "rtx_"}

# (fork, cell, probe?)
CELLS = [
    ("ctrl", "fid", False), ("ctrl", "rte", False),
    ("f1", "fid", False), ("f1", "rte", False), ("f1", "rte2", False),
    ("f1", "rtx", True),
    ("f2", "fid", False), ("f2", "rte", False), ("f2", "rte2", False),
    ("r1", "fid", False), ("r1", "rte", False), ("r1", "rte2", False),
    ("r1", "rtx", True),
]


def read(p):
    with open(p, "r", encoding="utf-8") as f:
        return f.read()


def write(p, s):
    with open(p, "w", encoding="utf-8") as f:
        f.write(s)


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def sub_once(s, old, new, tag, what):
    n = s.count(old)
    assert n == 1, (tag, what, "anchor hits=%d" % n)
    return s.replace(old, new)


def sub_all(s, old, new, tag, what, expect):
    n = s.count(old)
    assert n == expect, (tag, what, "anchor hits=%d expected %d" % (n, expect))
    return s.replace(old, new)


def build_cell(fork, cell, probe):
    tag = "%s_%s" % (fork, cell.upper())
    d = os.path.join(BUILD, tag)
    if os.path.isdir(d):
        shutil.rmtree(d)
    os.makedirs(d)
    for fn in ("gl_learner.zag", "gl_substrate.zag"):
        shutil.copy(os.path.join(HARNESS, fn), os.path.join(d, fn))

    # --- substrate patches
    sp = os.path.join(d, "gl_substrate.zag")
    s = read(sp)
    if probe:
        if fork == "f1":
            s = sub_once(s, "const ACT_REKEY:i32=2;", SUB_PROBE_F1, tag, "sub probe f1")
        else:
            s = sub_once(s, "const ACT_REKEY:i32=2;", SUB_PROBE_R1, tag, "sub probe r1")
    elif fork in ("f1", "f2"):
        s = sub_once(s, "const ACT_REKEY:i32=2;", SUB_REPERTOIRE, tag, "sub repertoire")
    write(sp, s)

    # --- learner patches
    lp = os.path.join(d, "gl_learner.zag")
    s = read(lp)
    if fork in ("f1", "f2", "r1"):
        s = sub_once(s, L_NORULE_1_OLD, L_NORULE_1_NEW, tag, "no_rule head")
        s = sub_all(s, "            if(rc==TN_OK && act==ACT_CONTEST){",
                    "            if(rc==TN_OK && act==ACT_CONTEST && no_rule==0){", tag, "no_rule contest", 1)
        s = sub_all(s, "            if(rc==TN_OK && act==ACT_REKEY){",
                    "            if(rc==TN_OK && act==ACT_REKEY && no_rule==0){", tag, "no_rule rekey", 1)
        s = sub_all(s, "            if(rc==TN_OK && act==ACT_OVERWRITE){",
                    "            if(rc==TN_OK && act==ACT_OVERWRITE && no_rule==0){", tag, "no_rule overwrite", 1)
        s = sub_once(s, "            if(rc==TN_OK && permanent==0 && ep>=15 && ep<=48){",
                     "            if(rc==TN_OK && permanent==0 && ep>=15 && ep<=48 && no_rule==0){",
                     tag, "no_rule revocation")
    if fork in ("f1", "f2"):
        s = sub_once(s, L_GATE_F1F2_OLD, L_GATE_F1F2_NEW, tag, "gate f1f2")
        s = sub_once(s, L_LOOP_F1F2_OLD, L_LOOP_F1F2_NEW, tag, "survivor loop")
    elif fork == "r1":
        s = sub_once(s, L_GATE_F1F2_OLD, L_GATE_R1_NEW, tag, "gate r1")
    if fork == "f1":
        s = sub_once(s, L_COMMIT_F1_OLD, L_COMMIT_F1_NEW, tag, "commit guard")
    if probe:
        s = sub_once(s, L_PROBE_DISPATCH_OLD, L_PROBE_DISPATCH_NEW, tag, "probe dispatch")
        s = sub_once(s, L_PROBE_CAL_OLD, L_PROBE_CAL_NEW, tag, "probe cal")
        s = sub_once(s, L_PROBE_SIM_OLD, L_PROBE_SIM_NEW, tag, "probe sim")
        s = sub_once(s, L_PROBE_SURV_OLD, L_PROBE_SURV_NEW, tag, "probe surv")
        s = sub_once(s, L_PROBE_SIG_OLD, L_PROBE_SIG_NEW, tag, "probe sig")
        s = sub_once(s, L_PROBE_SIGP_OLD, L_PROBE_SIGP_NEW, tag, "probe sigp")
        s = sub_once(s, L_PROBE_SEL_OLD, L_PROBE_SEL_NEW, tag, "probe sel")

    # --- extra FACT lines (metrics only)
    s = sub_once(s, "fn rt_fact(px:[]u8,name:[]u8,val:i32)void {",
                 FACT_HELPER_ADD + "\nfn rt_fact(px:[]u8,name:[]u8,val:i32)void {",
                 tag, "fact helper")
    s = sub_once(s, FACTS_ADD_OLD, FACTS_ADD_NEW, tag, "fact withhold")

    # --- main swap
    mi = s.index("fn main()i32 {")
    s = s[:mi]
    if cell == "fid":
        canon = read(os.path.join(ROOT, "canon_learner.zag"))
        fmi = canon.index("fn main()i32 {")
        s += canon[fmi:]
    else:
        s += ("fn main()i32 {\n    let f:i32=0;\n    %s\n"
              "    _zag_print(\"RT_DONE,\");_zag_print(\"%s\");_zag_println(\"\");\n"
              "    return 0;\n}\n" % (MAINS[cell], tag))
    write(lp, s)

    # --- static no-randomness check
    for fn in ("gl_learner.zag", "gl_substrate.zag"):
        code = re.sub(r"//.*", "", read(os.path.join(d, fn)))
        hits = re.findall(r"(?i)\brng\b|rand\(|srand|/dev/urandom|[^a-z]seed[^a-z]", code)
        assert not hits, (tag, fn, hits)

    # --- compile
    binp = os.path.join(d, "rtbin")
    cp = subprocess.run([ZNC, os.path.join(d, "gl_learner.zag"), "--no-zagd",
                         "--no-analyze", "--no-foreground-cache", "-o", binp],
                        cwd=d, capture_output=True, text=True, timeout=600)
    if cp.returncode != 0:
        return (tag, False, "COMPILE FAIL: " + cp.stderr[-2000:])

    # --- run twice, byte-compare
    outs = []
    for _ in (1, 2):
        r = subprocess.run([binp], cwd=d, capture_output=True, text=True, timeout=600)
        outs.append(r.stdout)
    h1 = hashlib.sha256(outs[0].encode()).hexdigest()
    h2 = hashlib.sha256(outs[1].encode()).hexdigest()
    det = (h1 == h2)
    os.makedirs(EV, exist_ok=True)
    with open(os.path.join(EV, "%s_run1.txt" % tag), "w") as f:
        f.write(outs[0])
    with open(os.path.join(EV, "%s_run2.txt" % tag), "w") as f:
        f.write(outs[1])
    with open(os.path.join(EV, "%s_meta.txt" % tag), "w") as f:
        f.write("tag=%s\nsha1=%s\nsha2=%s\ndeterministic=%s\n" % (tag, h1, h2, det))
    with open(os.path.join(EV, "%s_sources.txt" % tag), "w") as f:
        for fn in ("gl_learner.zag", "gl_substrate.zag"):
            f.write("%s  %s\n" % (sha256_file(os.path.join(d, fn)), fn))
    return (tag, det, "OK sha=%s" % h1[:12])


def main():
    only = sys.argv[1:] or None
    os.makedirs(BUILD, exist_ok=True)
    os.makedirs(EV, exist_ok=True)
    cells = CELLS
    if only:
        cells = [c for c in cells if "%s_%s" % (c[0], c[1]) in
                 [o.lower() for o in only] or c[0] in [o.lower() for o in only]]
    fails = []
    for (fork, cell, probe) in cells:
        tag, det, msg = build_cell(fork, cell, probe)
        print("%-10s det=%s %s" % (tag, det, msg), flush=True)
        if not det or msg.startswith("COMPILE"):
            fails.append(tag)
    print("CELLS=%d FAILS=%d %s" % (len(cells), len(fails), fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
