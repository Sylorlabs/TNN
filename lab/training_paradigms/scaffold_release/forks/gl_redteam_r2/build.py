#!/usr/bin/env python3
"""FL2 red-team R2 battery: patch pristine copies, build, run twice, save evidence.

Reads pristine sources from orig/, generates one build dir per (variant, attack)
cell under build/, compiles with znc, runs each binary twice, and stores
transcripts under evidence/. Verdicts are evaluated by verify.py.
"""
import hashlib
import os
import re
import shutil
import subprocess
import sys

ZNC = os.path.expanduser("~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1")
ROOT = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.join(ROOT, "orig")
BUILD = os.path.join(ROOT, "build")
EV = os.path.join(ROOT, "evidence")

VARIANTS = {
    "default": {"files": ["gl_learner.zag", "gl_substrate.zag"],
                "substrate": "gl_substrate.zag", "learner": "gl_learner.zag",
                "extra_ep_info": ["gl_learner.zag"],
                "arm_fn": "fn arm_gl(",
                "arm_call": 'arm_gl({st},{ta},"{px}")',
                "fault_old": "rc=tn_do_contest(mkey,mval,mflag,qkey,qval,qflag,TN_NQUAR,ep,audit,&acount,k,v);",
                "fault_new": "rc=rt_fault_contest(mkey,mval,mflag,qkey,qval,qflag,TN_NQUAR,ep,audit,&acount,k,v);",
                "aa_patch": True},
    "a2": {"files": ["v_a2.zag", "g8base.zag", "tn.zag"],
           "substrate": "tn.zag", "learner": "v_a2.zag",
           "extra_ep_info": ["v_a2.zag", "g8base.zag"],
           "arm_fn": "fn arm_va2(",
           "arm_call": 'arm_va2({st},{ta},"{px}",{w})',
           "fault_old": "rc=tn_do_contest(mkey,mval,mflag,qkey,qval,qflag,TN_NQUAR,ep,audit,&acount,k,v);",
           "fault_new": "rc=rt_fault_contest(mkey,mval,mflag,qkey,qval,qflag,TN_NQUAR,ep,audit,&acount,k,v);",
           "aa_patch": False},
    "a3": {"files": ["v_a3.zag", "g8base.zag", "tn.zag"],
           "substrate": "tn.zag", "learner": "v_a3.zag",
           "extra_ep_info": ["v_a3.zag", "g8base.zag"],
           "arm_fn": "fn arm_va3(",
           "arm_call": 'arm_va3({st},{ta},"{px}",{w})',
           "fault_old": "rc=tn_do_contest(mkey,mval,mflag,qkey,qval,qflag,TN_NQUAR,ep,audit,&acount,k,v);",
           "fault_new": "rc=rt_fault_contest(mkey,mval,mflag,qkey,qval,qflag,TN_NQUAR,ep,audit,&acount,k,v);",
           "aa_patch": False},
    "b1": {"files": ["v_b1.zag", "g8base.zag", "tn.zag"],
           "substrate": "tn.zag", "learner": "v_b1.zag",
           "extra_ep_info": ["v_b1.zag", "g8base.zag"],
           "arm_fn": "fn arm_vb1(",
           "arm_call": 'arm_vb1({st},{ta},"{px}",{w})',
           "fault_old": "rc=tn_do_contest(amkey,amval,amflag,aqkey,aqval,aqflag,TN_NQUAR,ep,audit,&acount,k,v);",
           "fault_new": "rc=rt_fault_contest(amkey,amval,amflag,aqkey,aqval,aqflag,TN_NQUAR,ep,audit,&acount,k,v);",
           "aa_patch": False},
    "f3": {"files": ["f3_lawcheck.zag", "tnw.zag"],
           "substrate": "tnw.zag", "learner": "f3_lawcheck.zag",
           "extra_ep_info": ["f3_lawcheck.zag"],
           "arm_fn": "fn arm_f3(",
           "arm_call": 'arm_f3({st},{w},"{px}")',
           "fault_old": "rc=tn_do_contest(mkey,mval,mflag,qkey,qval,qflag,TN_NQUAR,ep,audit,&acount,k,v);",
           "fault_new": "rc=rt_fault_contest(mkey,mval,mflag,qkey,qval,qflag,TN_NQUAR,ep,audit,&acount,k,v);",
           "aa_patch": False},
}

# stated, teach_aux, world, RT_MODE, fault?, px. world=-1 means "unused" (default).
ATTACKS = {
    "A": {"stated": 0, "teach": 0, "world": 0, "mode": 0, "fault": False, "px": "rta_"},
    "B": {"stated": 2, "teach": 1, "world": 1, "mode": 0, "fault": False, "px": "rtb_"},
    "C": {"stated": 1, "teach": 0, "world": 0, "mode": 0, "fault": True, "px": "rtc_"},
    "D": {"stated": 1, "teach": 0, "world": 0, "mode": 1, "fault": False, "px": "rtd_"},
    "E": {"stated": 7, "teach": 0, "world": 0, "mode": 0, "fault": False, "px": "rte_"},
    "F": {"stated": 2, "teach": 1, "world": 1, "mode": 2, "fault": False, "px": "rtf_"},
}
# default-variant overrides: B uses silent-aa mode 3, F uses displace mode 2 (no world param)
DEFAULT_MODE_OVERRIDE = {"B": 3, "F": 2}

SUB_APPEND = """
// RT2 red-team schedule wrapper. RT_MODE: 0=standard, 1=flood (E15+ dense ACQ),
// 2=displace (E49-50 TEACH, E51+ ACQ contradictions), 3=silent-aa (standard schedule).
// etype literals: 3=ET_ACQ, 1=ET_TEACH (same values in every substrate copy).
const RT_MODE:i32={mode};
fn rt_ep_info(ep:i32,etype:*i32,key:*i32,val:*i32,auth:*i32)void {{
    if(RT_MODE==1 && ep>=15){{
        etype.*=3;key.*=((ep-15)%8)+1;val.*=300+ep;auth.*=0;return;
    }}
    if(RT_MODE==2 && ep>=49){{
        if(ep<=50){{etype.*=1;key.*=0;val.*=0;auth.*=0;return;}}
        etype.*=3;key.*=((ep-51)%8)+1;val.*=700+ep;auth.*=0;return;
    }}
    tn_ep_info(ep,etype,key,val,auth);
    return;
}}
"""

FAULT_FN = """
// RT2 RT-C actuator fault: the learner audits the CONTEST (its ledger believes
// it acted) but the world drops the quarantine write and the flag sets.
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

FACT_HELPER = """
// RT2 instrumentation: one RT_FACT metrics line (no behavior change).
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
    // RT2 instrumentation: first-aux facts (metrics only).
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


def build_cell(v, a, fidelity=False):
    spec = VARIANTS[v]
    atk = ATTACKS.get(a) or {"stated": 0, "teach": 0, "world": 0, "mode": 0,
                             "fault": False, "px": "fid_"}
    tag = "%s_%s" % (v, "FID" if fidelity else a)
    d = os.path.join(BUILD, tag)
    if os.path.isdir(d):
        shutil.rmtree(d)
    os.makedirs(d)
    for fn in spec["files"]:
        shutil.copy(os.path.join(ORIG, fn), os.path.join(d, fn))

    mode = atk["mode"]
    if v == "default" and a in DEFAULT_MODE_OVERRIDE:
        mode = DEFAULT_MODE_OVERRIDE[a]

    # 1. substrate: append RT_MODE + rt_ep_info (+ fault fn for RT-C)
    sp = os.path.join(d, spec["substrate"])
    s = read(sp)
    s += SUB_APPEND.format(mode=mode)
    if not fidelity and atk["fault"]:
        s += FAULT_FN
    write(sp, s)

    # 2. learner (+ g8base copy): tn_ep_info -> rt_ep_info
    for fn in spec["extra_ep_info"]:
        p = os.path.join(d, fn)
        s = read(p)
        n = s.count("tn_ep_info(")
        assert n >= 1, (tag, fn, "tn_ep_info anchor")
        s = s.replace("tn_ep_info(", "rt_ep_info(")
        write(p, s)

    # 3. default-only aa gate
    lp = os.path.join(d, spec["learner"])
    s = read(lp)
    if spec["aa_patch"]:
        n = s.count(AA_OLD)
        assert n >= 1, (tag, "aa anchor")
        s = s.replace(AA_OLD, AA_NEW)

    # 4. RT-C fault swap on the live kind-3 action
    if not fidelity and atk["fault"]:
        n = s.count(spec["fault_old"])
        assert n >= 1, (tag, "fault anchor")
        s = s.replace(spec["fault_old"], spec["fault_new"])

    # 5. RT_FACTS instrumentation: helper before arm fn, facts before free anchor
    assert s.count(spec["arm_fn"]) == 1, (tag, "arm fn anchor")
    s = s.replace(spec["arm_fn"], FACT_HELPER + "\n" + spec["arm_fn"])
    assert s.count(FREE_ANCHOR) == 1, (tag, "free anchor")
    s = s.replace(FREE_ANCHOR, FACTS_BLOCK + FREE_ANCHOR)

    # 6. main() replacement
    mi = s.index("fn main()i32 {")
    s = s[:mi]
    if fidelity:
        orig_main = read(os.path.join(ORIG, spec["learner"]))
        fmi = orig_main.index("fn main()i32 {")
        s += orig_main[fmi:]
    else:
        world = atk["world"]
        call = spec["arm_call"].format(st=atk["stated"], ta=atk["teach"],
                                       px=atk["px"], w=world)
        s += ("fn main()i32 {\n    let f:i32=0;\n    f=f+%s;\n"
              "    _zag_print(\"RT_DONE,\");_zag_print(\"%s\");_zag_println(\"\");\n"
              "    return 0;\n}\n" % (call, tag))
    write(lp, s)

    # 7. static no-randomness check on patched sources
    for fn in spec["files"]:
        code = re.sub(r"//.*", "", read(os.path.join(d, fn)))
        hits = re.findall(r"(?i)\brng\b|rand\(|srand|/dev/urandom|[^a-z]seed[^a-z]", code)
        assert not hits, (tag, fn, hits)

    # 8. compile
    binp = os.path.join(d, "rtbin")
    cp = subprocess.run([ZNC, os.path.join(d, spec["learner"]), "--no-zagd",
                         "--no-analyze", "--no-foreground-cache", "-o", binp],
                        cwd=d, capture_output=True, text=True, timeout=600)
    if cp.returncode != 0:
        return (tag, False, "COMPILE FAIL: " + cp.stderr[-2000:])

    # 9. run twice, byte-compare
    outs = []
    for i in (1, 2):
        r = subprocess.run([binp], cwd=d, capture_output=True, text=True, timeout=600)
        outs.append(r.stdout)
        if r.returncode != 0 and not fidelity:
            pass  # attack binaries return 0 by construction; note anyway
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
    # record patched-source shas for reproducibility
    with open(os.path.join(EV, "%s_sources.txt" % tag), "w") as f:
        for fn in spec["files"]:
            f.write("%s  %s\n" % (sha256_file(os.path.join(d, fn)), fn))
    return (tag, det, "OK sha=%s" % h1[:12])


def main():
    only = sys.argv[1:] or None
    os.makedirs(BUILD, exist_ok=True)
    os.makedirs(EV, exist_ok=True)
    cells = []
    for v in VARIANTS:
        cells.append((v, "FID", True))
        for a in ATTACKS:
            cells.append((v, a, False))
    if only:
        cells = [c for c in cells if c[0] in only or "%s_%s" % (c[0], c[1]) in only]
    fails = []
    for (v, a, fid) in cells:
        tag, det, msg = build_cell(v, a, fid)
        print("%-12s det=%s %s" % (tag, det, msg), flush=True)
        if not det or msg.startswith("COMPILE"):
            fails.append(tag)
    print("CELLS=%d FAILS=%d %s" % (len(cells), len(fails), fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
