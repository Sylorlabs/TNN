#!/usr/bin/env python3
"""FL2 RT-C fork test: patch pristine copies per frozen PREREG, build, run twice.

Forks: f1 (general act->verify-effect->interpret + f3_survivor),
       f2 (quarantine read-back, 99 sentinel kept),
       r1 (H-R1 quarantine-only trigger policy, 99 sentinel kept),
       n1 (NEGATIVE CONTROL: sentinel fix alone).
Cells per fork: FID (fidelity gate), C (RT-C fault), A (RT-A regression),
       P2 (scope probe: quarantine write lands, main-flag flip dropped).
"""
import hashlib
import os
import re
import shutil
import subprocess
import sys

ZNC = os.path.expanduser("~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1")
ROOT = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.expanduser("~/workspace/fl2rt/orig")
FORKD = os.path.join(ROOT, "forks")
BUILD = os.path.join(ROOT, "build")
EV = os.path.join(ROOT, "evidence")

FORKS = ["f1", "f2", "r1", "n1"]
CELLS = ["FID", "C", "A", "P2"]

F3_SURVIVOR = """
// f3_survivor, verbatim the F3 function: skip the acted slot, genuine
// signals first, no 99 default.
fn f3_survivor(act:i32,sig0:i32,sig1:i32,sig2:i32)i32 {
    if(act!=0 && sig0>=1){return 0;}
    if(act!=1 && sig1>=1){return 1;}
    if(act!=2 && sig2>=1){return 2;}
    return -1;
}
"""

F1_HELPER = """
// F1: general act->verify-effect->interpret discipline.
// No contradiction signal is valid until the acted policy's expected world
// effect is confirmed present. One predicate per policy; no per-attack rules.
fn gl_effect_landed(act:i32,k:i32,v:i32,mkey:[]u8,mval:[]u8,mflag:[]u8,qkey:[]u8,qval:[]u8,qflag:[]u8)i32 {
    if(act==ACT_CONTEST){
        if(tn_quar_has_flag(qkey,qval,qflag,TN_NQUAR,k,v)==0){return 0;}
        if(tn_main_flag(mflag,TN_NMAIN,k,mkey)!=1){return 0;}
        return 1;
    }
    if(act==ACT_REKEY){
        if(tn_main_has_rekeyed(mkey,mval,TN_NMAIN,v)==0){return 0;}
        return 1;
    }
    if(act==ACT_OVERWRITE){
        if(tn_main_val(mkey,mval,TN_NMAIN,k)!=v){return 0;}
        if(tn_main_flag(mflag,TN_NMAIN,k,mkey)!=0){return 0;}
        return 1;
    }
    return 0;
}
"""

SIG_ANCHOR = "let sig_live:i32=gl_contradict(k,v,v_old,aa,mkey,mval,mflag,qkey,qval,qflag);"
SURV_ANCHOR = ("                if(sig_live==-1){\n"
               "                    let surv:i32=-1;\n"
               "                    if(sig0>=1){surv=0;}\n"
               "                    if(sig1>=1 && surv<0){surv=1;}\n"
               "                    if(sig2>=1 && surv<0){surv=2;}")
ARM_ANCHOR = "fn arm_gl("

F1_SIG_PATCH = (SIG_ANCHOR + "\n"
    "                // F1: close the loop - a signal from an unlanded effect is void.\n"
    "                if(gl_effect_landed(act,k,v,mkey,mval,mflag,qkey,qval,qflag)==0){sig_live=0;}")
F2_SIG_PATCH = (SIG_ANCHOR + "\n"
    "                // F2: quarantine read-back - revoke only from landed effects.\n"
    "                if(act==ACT_CONTEST && tn_quar_has_flag(qkey,qval,qflag,TN_NQUAR,k,v)==0){sig_live=0;}")
SURV_PATCH = ("                if(sig_live==-1){\n"
              "                    // f3_survivor: skip acted slot, genuine signals first.\n"
              "                    let surv:i32=f3_survivor(act,sig0,sig1,sig2);")
R1_TRIG_PATCH = ("                // R1 (H-R1): revocation triggers only from quarantine writes.\n"
                 "                if(sig_live==-1 && (act!=ACT_CONTEST || tn_quar_has_flag(qkey,qval,qflag,TN_NQUAR,k,v)==1)){")
R1_TRIG_ANCHOR = "                if(sig_live==-1){"

SUB_APPEND = """
const RT_MODE:i32=0;
fn rt_ep_info(ep:i32,etype:*i32,key:*i32,val:*i32,auth:*i32)void {
    tn_ep_info(ep,etype,key,val,auth);
    return;
}
"""

FAULT_FN = """
// RT-C actuator fault: the learner audits the CONTEST but the world drops
// the quarantine write and the flag sets.
fn rt_fault_contest(mkey:[]u8,mval:[]u8,mflag:[]u8,qkey:[]u8,qval:[]u8,qflag:[]u8,nq:i32,step:i32,audit:[]u8,acount:*i32,k:i32,v:i32)i32 {
    let s:i32=tn_find_main(mkey,TN_NMAIN,k);
    if(s<0){return TN_BAD;}
    let q:i32=tn_first_free(qkey,nq);
    if(q<0){return TN_BAD;}
    let r:i32=tn_audit(audit,acount,step,TN_OP_CONTEST,s+1,q+1);
    if(r!=TN_OK){return r;}
    return TN_OK;
}
"""

FAULT2_FN = """
// P2 scope probe: the world audits the CONTEST and LANDS the quarantine
// write, but DROPS the main-store flag flip. Same fault class (world does
// not honor the action), different part of the effect - invisible to a
// quarantine-only read-back.
fn rt_fault2_contest(mkey:[]u8,mval:[]u8,mflag:[]u8,qkey:[]u8,qval:[]u8,qflag:[]u8,nq:i32,step:i32,audit:[]u8,acount:*i32,k:i32,v:i32)i32 {
    let s:i32=tn_find_main(mkey,TN_NMAIN,k);
    if(s<0){return TN_BAD;}
    let q:i32=tn_first_free(qkey,nq);
    if(q<0){return TN_BAD;}
    let r:i32=tn_audit(audit,acount,step,TN_OP_CONTEST,s+1,q+1);
    if(r!=TN_OK){return r;}
    tn_s32(qkey,q*4,k);tn_s32(qval,q*4,v);tn_s32(qflag,q*4,1);
    return TN_OK;
}
"""

FACT_HELPER = """
// RT_FACT metrics (no behavior change).
fn rt_fact(px:[]u8,name:[]u8,val:i32)void {
    _zag_print("RT_FACT,");
    _zag_print(px);
    _zag_print(name);
    _zag_print(",");
    let s:[]u8=_zag_i64_to_str(val as i64);_zag_print(s);tn_free(s);
    _zag_println("");
    return;
}
"""

FACTS_BLOCK = """
    // RT_FACT metrics (no behavior change).
    let rtf_i:i32=0;let rtf_cpol:i32=-1;let rtf_upol:i32=-1;let rtf_ppol:i32=-1;let rtf_ncommit:i32=0;
    while(rtf_i<acount){
        let rtf_op:i32=tn_g32(audit,rtf_i*16+4);
        if(rtf_op==TN_OP_COMMIT){rtf_ncommit=rtf_ncommit+1;}
        if(rtf_op==TN_OP_COMMIT && rtf_cpol<0){rtf_cpol=tn_g32(audit,rtf_i*16+12);}
        if(rtf_op==TN_OP_UNINSTALL_PROVISIONAL && rtf_upol<0){rtf_upol=tn_g32(audit,rtf_i*16+12);}
        if(rtf_op==TN_OP_PROMOTE && rtf_ppol<0){rtf_ppol=tn_g32(audit,rtf_i*16+12);}
        rtf_i=rtf_i+1;
    }
    rt_fact(px,"commit_policy",rtf_cpol);
    rt_fact(px,"uninstall_policy",rtf_upol);
    rt_fact(px,"promote_policy",rtf_ppol);
    rt_fact(px,"ncommit",rtf_ncommit);
    rt_fact(px,"badep",badep);
"""

FREE_ANCHOR = "    tn_free(audit);tn_free(committed);\n    return f;"
AA_OLD = "if(ep>=29 && ep<=48){aa=1;}"
AA_NEW = "if(ep>=29 && ep<=48 && RT_MODE!=2 && RT_MODE!=3){aa=1;}"
FAULT_OLD = "rc=tn_do_contest(mkey,mval,mflag,qkey,qval,qflag,TN_NQUAR,ep,audit,&acount,k,v);"

CELL_MAIN = {
    "C": 'arm_gl(1,0,"{px}c_")',
    "A": 'arm_gl(0,0,"{px}a_")',
    "P2": 'arm_gl(1,0,"{px}p_")',
}


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


def apply_fork(fork):
    """Write the patched fork sources into forks/<fork>/. Asserts anchors."""
    d = os.path.join(FORKD, fork)
    if os.path.isdir(d):
        shutil.rmtree(d)
    os.makedirs(d)
    s = read(os.path.join(ORIG, "gl_learner.zag"))
    assert s.count(SIG_ANCHOR) == 1, (fork, "sig anchor")
    assert s.count(SURV_ANCHOR) == 1, (fork, "survivor anchor")
    assert s.count(R1_TRIG_ANCHOR) == 1, (fork, "trigger anchor")
    assert s.count(ARM_ANCHOR) == 1, (fork, "arm anchor")
    if fork == "f1":
        s = s.replace(ARM_ANCHOR, F3_SURVIVOR + "\n" + F1_HELPER + "\n" + ARM_ANCHOR)
        s = s.replace(SIG_ANCHOR, F1_SIG_PATCH)
        s = s.replace(SURV_ANCHOR, SURV_PATCH)
    elif fork == "f2":
        s = s.replace(SIG_ANCHOR, F2_SIG_PATCH)
    elif fork == "r1":
        s = s.replace(R1_TRIG_ANCHOR, R1_TRIG_PATCH)
    elif fork == "n1":
        s = s.replace(ARM_ANCHOR, F3_SURVIVOR + "\n" + ARM_ANCHOR)
        s = s.replace(SURV_ANCHOR, SURV_PATCH)
    else:
        raise ValueError(fork)
    write(os.path.join(d, "gl_learner.zag"), s)
    shutil.copy(os.path.join(ORIG, "gl_substrate.zag"),
                os.path.join(d, "gl_substrate.zag"))
    return d


def build_cell(fork, cell):
    tag = "%s_%s" % (fork, cell)
    fd = os.path.join(FORKD, fork)
    d = os.path.join(BUILD, tag)
    if os.path.isdir(d):
        shutil.rmtree(d)
    os.makedirs(d)
    shutil.copy(os.path.join(fd, "gl_learner.zag"), os.path.join(d, "gl_learner.zag"))
    shutil.copy(os.path.join(fd, "gl_substrate.zag"), os.path.join(d, "gl_substrate.zag"))

    # 1. substrate: RT_MODE + rt_ep_info (+ fault fn for C / P2)
    sp = os.path.join(d, "gl_substrate.zag")
    s = read(sp) + SUB_APPEND
    if cell == "C":
        s += FAULT_FN
    elif cell == "P2":
        s += FAULT2_FN
    write(sp, s)

    # 2. learner: tn_ep_info -> rt_ep_info; aa gate
    lp = os.path.join(d, "gl_learner.zag")
    s = read(lp)
    n = s.count("tn_ep_info(")
    assert n >= 1, (tag, "tn_ep_info anchor")
    s = s.replace("tn_ep_info(", "rt_ep_info(")
    n = s.count(AA_OLD)
    assert n == 1, (tag, "aa anchor")
    s = s.replace(AA_OLD, AA_NEW)

    # 3. fault swap on the live kind-3 contest call (all occurrences, as RT2)
    if cell == "C":
        n = s.count(FAULT_OLD)
        assert n >= 1, (tag, "fault anchor")
        s = s.replace(FAULT_OLD, FAULT_OLD.replace("tn_do_contest", "rt_fault_contest"))
    elif cell == "P2":
        n = s.count(FAULT_OLD)
        assert n >= 1, (tag, "fault anchor")
        s = s.replace(FAULT_OLD, FAULT_OLD.replace("tn_do_contest", "rt_fault2_contest"))

    # 4. RT_FACT instrumentation
    assert s.count(ARM_ANCHOR) == 1, (tag, "arm fn anchor")
    s = s.replace(ARM_ANCHOR, FACT_HELPER + "\n" + ARM_ANCHOR)
    assert s.count(FREE_ANCHOR) == 1, (tag, "free anchor")
    s = s.replace(FREE_ANCHOR, FACTS_BLOCK + FREE_ANCHOR)

    # 5. main() replacement
    mi = s.index("fn main()i32 {")
    s = s[:mi]
    if cell == "FID":
        orig_main = read(os.path.join(ORIG, "gl_learner.zag"))
        fmi = orig_main.index("fn main()i32 {")
        s += orig_main[fmi:]
    else:
        call = CELL_MAIN[cell].format(px=fork)
        s += ("fn main()i32 {\n    let f:i32=0;\n    f=f+%s;\n"
              "    _zag_print(\"RT_DONE,\");_zag_print(\"%s\");_zag_println(\"\");\n"
              "    return 0;\n}\n" % (call, tag))
    write(lp, s)

    # 6. static no-randomness check
    for fn in ("gl_learner.zag", "gl_substrate.zag"):
        code = re.sub(r"//.*", "", read(os.path.join(d, fn)))
        hits = re.findall(r"(?i)\brng\b|rand\(|srand|/dev/urandom|[^a-z]seed[^a-z]", code)
        assert not hits, (tag, fn, hits)

    # 7. compile
    binp = os.path.join(d, "rtbin")
    cp = subprocess.run([ZNC, os.path.join(d, "gl_learner.zag"), "--no-zagd",
                         "--no-analyze", "--no-foreground-cache", "-o", binp],
                        cwd=d, capture_output=True, text=True, timeout=600)
    if cp.returncode != 0:
        return (tag, False, "COMPILE FAIL: " + cp.stderr[-2000:])

    # 8. run twice, byte-compare
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
    for d in (FORKD, BUILD, EV):
        os.makedirs(d, exist_ok=True)
    for fork in FORKS:
        if only and fork not in only and not any(o.startswith(fork + "_") for o in only):
            continue
        apply_fork(fork)
        print("fork %s patched" % fork, flush=True)
    fails = []
    for fork in FORKS:
        for cell in CELLS:
            tag = "%s_%s" % (fork, cell)
            if only and fork not in only and tag not in only:
                continue
            t, det, msg = build_cell(fork, cell)
            print("%-8s det=%s %s" % (t, det, msg), flush=True)
            if not det or msg.startswith("COMPILE"):
                fails.append((t, msg))
    if fails:
        print("FAILURES:", fails)
        return 1
    print("ALL CELLS OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
