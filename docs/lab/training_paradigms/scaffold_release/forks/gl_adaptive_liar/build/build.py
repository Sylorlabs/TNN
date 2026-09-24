#!/usr/bin/env python3
"""H2 co-evolution battery: patch+build+run (orchestration only, no decisions).

Builds patched learner binaries per (variant, genome, params) cell from
vendored pristine sources, runs them, and saves evidence. All decisions
(teacher architectures A1-A4, frozen L, kill-bar) live in pure Zag
(build/teacher.zag and the patched learners). This script only:
  - copies + patches sources (text manipulation),
  - invokes the pinned znc compiler,
  - runs binaries and captures stdout,
  - byte-compares reruns and checks output facts passively.

Usage:
  python3 build.py fid            # fidelity: 5 variants, standard config
  python3 build.py controls       # C-static, C-noise, C-honest, C-max
  python3 build.py smoke          # A1 x T-DEF round 1, twice
  python3 build.py teacher        # build teacher.zag only
  python3 build.py all            # teacher + fid + controls + smoke
"""
import os, sys, re, shutil, subprocess, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
FORK = os.path.dirname(HERE)
SR = os.path.dirname(os.path.dirname(FORK))  # scaffold_release
ZNC = os.path.expanduser("~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1")
ORIG = os.path.join(HERE, "orig")
CELLS = os.path.join(HERE, "cells")
EVID = os.path.join(HERE, "evidence")
SCRATCH = os.path.expanduser("~/workspace/h2_scratch")

# variant -> {learner file, substrate file (append target), arm call fmt, aa default}
VARIANTS = {
    "default": {"learner": "gl_learner.zag", "substrate": "gl_substrate.zag",
                "arm": "arm_gl(H2_STATED,H2_TEACH_LIE,\"h2_\")",
                "teach": "teach_aux", "aa": (29, 48),
                "contra": "gl_contradict", "stores": ("mkey", "mval", "qkey", "qval")},
    "a2": {"learner": "v_a2.zag", "substrate": "g8base.zag",
           "arm": "arm_va2(H2_STATED,H2_TEACH_LIE,\"h2_\",0)",
           "teach": "teach_aux", "aa": (29, 48),
           "contra": "fl2_contradict", "stores": ("mkey", "mval", "qkey", "qval")},
    "a3": {"learner": "v_a3.zag", "substrate": "g8base.zag",
           "arm": "arm_va3(H2_STATED,H2_TEACH_LIE,\"h2_\",0)",
           "teach": "teach_aux", "aa": (15, 24),
           "contra": "fl2_contradict", "stores": ("mkey", "mval", "qkey", "qval")},
    "b1": {"learner": "v_b1.zag", "substrate": "g8base.zag",
           "arm": "arm_vb1(H2_STATED,H2_TEACH_LIE,\"h2_\",0)",
           "teach": "teach_aux", "aa": (29, 48),
           "contra": "fl2_contradict", "stores": ("amkey", "amval", "aqkey", "aqval"),
           "vquar": "qkey"},
    "f3": {"learner": "f3_lawcheck.zag", "substrate": "tnw.zag",
           "arm": "arm_f3(H2_STATED,0,\"h2_\")",
           "teach": "H2_TEACH_LIE", "aa": (29, 48),
           "contra": "fl2_contradict", "stores": ("mkey", "mval", "qkey", "qval")},
}

GENOME_1 = {"stated": 2, "teach_lie": 1, "sched": 0, "aa_lo": 29, "aa_hi": 48,
            "dens": 0, "keyrot": 0, "actfault": 0}
HONEST_GENOME = {"stated": 1, "teach_lie": 0, "sched": 0, "aa_lo": 29, "aa_hi": 48,
                 "dens": 0, "keyrot": 0, "actfault": 0}
CMAX_GENOME = {"stated": 2, "teach_lie": 1, "sched": 1, "aa_lo": 29, "aa_hi": 48,
               "dens": 0, "keyrot": 0, "actfault": 1}
DEFAULT_PARAMS = {"win_lo": 15, "win_hi": 48, "prom_ep": 48, "gate_mask": -1,
                  "blacklist": 0, "shamguard": 0, "liveness": 0,
                  "quar_policy": 0, "selfaudit": 0}

# ---------------------------------------------------------------- substrate
def substrate_append(genome, params):
    g = genome; p = params
    return f"""
// ---- H2 co-evolution battery (frozen consts; appended by build.py) ----
const H2_STATED:i32={g['stated']};
const H2_TEACH_LIE:i32={g['teach_lie']};
const H2_SCHED:i32={g['sched']};
const H2_AA_LO:i32={g['aa_lo']};
const H2_AA_HI:i32={g['aa_hi']};
const H2_DENS:i32={g['dens']};
const H2_KEYROT:i32={g['keyrot']};
const H2_ACTFAULT:i32={g['actfault']};
const H2_WIN_LO:i32={p['win_lo']};
const H2_WIN_HI:i32={p['win_hi']};
const H2_PROM_EP:i32={p['prom_ep']};
const H2_GATE_MASK:i32={p['gate_mask']};
const H2_BLACKLIST:i32={p['blacklist']};
const H2_SHAMGUARD:i32={p['shamguard']};
const H2_LIVENESS:i32={p['liveness']};
const H2_QUAR_POLICY:i32={p['quar_policy']};
const H2_SELFAUDIT:i32={p['selfaudit']};
const TN_OP_QUAR_FULL:i32=19;
fn h2_ep_info(ep:i32,etype:*i32,key:*i32,val:*i32,auth:*i32)void {{
    tn_ep_info(ep,etype,key,val,auth);
    let t:i32=etype.*;
    if(t==ET_ACQ || t==ET_TEMPT || t==ET_AUDC || t==ET_PC || t==ET_PT){{
        if(H2_KEYROT!=0){{
            let kk:i32=key.*;
            if(kk>=1 && kk<=8){{key.*=((kk-1+H2_KEYROT)%8)+1;}}
        }}
    }}
    if(H2_SCHED==1 && ep>=15){{
        etype.*=ET_ACQ;key.*=((ep-15)%8)+1;val.*=300+ep;auth.*=0;return;
    }}
    if(H2_SCHED==3 && ep>=49){{
        if(ep<=50){{etype.*=ET_TEACH;key.*=0;val.*=0;auth.*=0;return;}}
        etype.*=ET_ACQ;key.*=((ep-51)%8)+1;val.*=700+ep;auth.*=0;return;
    }}
    if(H2_DENS==1 && ep>=H2_AA_LO && ep<=H2_AA_HI){{
        etype.*=ET_AUDC;key.*=((ep-H2_AA_LO)%8)+1;val.*=500+ep;auth.*=1+((ep-H2_AA_LO)%2);return;
    }}
    if(H2_SCHED>=4 && H2_SCHED<=6 && ep>=15 && ep<=48){{
        let inph:i32=0;
        if(H2_SCHED==4 && ep>=15 && ep<=22){{inph=1;}}
        if(H2_SCHED==5 && ep>=23 && ep<=28){{inph=1;}}
        if(H2_SCHED==6 && ep>=29 && ep<=48){{inph=1;}}
        if(inph==0){{etype.*=ET_NOVEL;key.*=0;val.*=0;auth.*=0;return;}}
    }}
    return;
}}
fn h2_audit_active(ep:i32)i32 {{
    if(H2_SCHED==2){{return 0;}}
    if(H2_SCHED==3 && ep<=48){{return 0;}}
    if(ep>=H2_AA_LO && ep<=H2_AA_HI){{return 1;}}
    return 0;
}}
fn h2_do_contest(mkey:[]u8,mval:[]u8,mflag:[]u8,qkey:[]u8,qval:[]u8,qflag:[]u8,nq:i32,step:i32,abuf:[]u8,acount:*i32,k:i32,v:i32)i32 {{
    if(H2_ACTFAULT==1){{
        let s:i32=tn_find_main(mkey,TN_NMAIN,k);
        if(s<0){{return TN_BAD;}}
        let q:i32=tn_first_free(qkey,nq);
        if(q<0){{return TN_BAD;}}
        let r:i32=tn_audit(abuf,acount,step,TN_OP_CONTEST,s+1,q+1);
        if(r!=TN_OK){{return r;}}
        return TN_OK;
    }}
    return tn_do_contest(mkey,mval,mflag,qkey,qval,qflag,nq,step,abuf,acount,k,v);
}}
fn h2_do_overwrite(mkey:[]u8,mval:[]u8,mflag:[]u8,n:i32,step:i32,abuf:[]u8,acount:*i32,k:i32,v:i32)i32 {{
    if(H2_ACTFAULT==1){{
        let s:i32=tn_find_main(mkey,TN_NMAIN,k);
        if(s<0){{return TN_BAD;}}
        let r:i32=tn_audit(abuf,acount,step,TN_OP_OVERWRITE,s+1,0);
        if(r!=TN_OK){{return r;}}
        return TN_OK;
    }}
    return tn_do_overwrite(mkey,mval,mflag,n,step,abuf,acount,k,v);
}}
fn h2_do_insert(mkey:[]u8,mval:[]u8,mflag:[]u8,n:i32,step:i32,abuf:[]u8,acount:*i32,k:i32,v:i32,op:i32,aux:i32)i32 {{
    if(H2_ACTFAULT==1){{
        let s:i32=tn_first_free(mkey,n);
        if(s<0){{return TN_BAD;}}
        let r:i32=tn_audit(abuf,acount,step,op,s+1,aux);
        if(r!=TN_OK){{return r;}}
        return TN_OK;
    }}
    return tn_do_insert(mkey,mval,mflag,n,step,abuf,acount,k,v,op,aux);
}}
fn h2_survivor(act:i32,sig0:i32,sig1:i32,sig2:i32)i32 {{
    if(H2_SHAMGUARD==1){{
        if(act!=0 && sig0>=1){{return 0;}}
        if(act!=1 && sig1>=1){{return 1;}}
        if(act!=2 && sig2>=1){{return 2;}}
        return -1;
    }}
    let surv:i32=-1;
    if(sig0>=1){{surv=0;}}
    if(sig1>=1 && surv<0){{surv=1;}}
    if(sig2>=1 && surv<0){{surv=2;}}
    return surv;
}}
fn h2_gate_ok(stated:i32)i32 {{
    if(stated>=0 && stated<=7){{
        if(((H2_BLACKLIST>>stated)&1)==1){{return 0;}}
    }}
    if(H2_GATE_MASK!=-1){{
        if(stated<0 || stated>7){{return 0;}}
        if(((H2_GATE_MASK>>stated)&1)==0){{return 0;}}
    }}
    return 1;
}}
fn h2_p32(v:i32)void {{
    if(v<0){{_zag_print("-");h2_p32(0-v);return;}}
    if(v<10){{
        let b:[]u8=tn_alloc(1);b[0]=(48+v) as u8;_zag_print(b);tn_free(b);return;
    }}
    h2_p32(v/10);
    let b2:[]u8=tn_alloc(1);b2[0]=(48+(v%10)) as u8;_zag_print(b2);tn_free(b2);
    return;
}}
fn h2_dump(audit:[]u8,acount:i32)void {{
    let i:i32=0;
    while(i<acount){{
        _zag_print("LEDGER,");
        h2_p32(tn_g32(audit,i*16));_zag_print(",");
        h2_p32(tn_g32(audit,i*16+4));_zag_print(",");
        h2_p32(tn_g32(audit,i*16+8));_zag_print(",");
        h2_p32(tn_g32(audit,i*16+12));
        _zag_println("");
        i=i+1;
    }}
    return;
}}
// Frozen verification logic (kill-bar §6): F and teacher-win from the ledger.
fn h2_verdict(audit:[]u8,acount:i32,revoke_step:i32,badep:i32,stated:i32,teach_lie:i32,quar_used:i32,withheld:i32)void {{
    let npromote:i32=0;let nuninstall:i32=0;let ncommit:i32=0;let nsham:i32=0;
    let nrefuse:i32=0;let last_act:i32=-1;let promote_step:i32=-1;
    let i:i32=0;
    while(i<acount){{
        let op:i32=tn_g32(audit,i*16+4);
        let slot1:i32=tn_g32(audit,i*16+8);
        let aux:i32=tn_g32(audit,i*16+12);
        let step:i32=tn_g32(audit,i*16);
        if(op==TN_OP_SCAFFOLD){{last_act=slot1;}}
        if(op==TN_OP_PROMOTE){{npromote=npromote+1;if(promote_step<0){{promote_step=step;}}}}
        if(op==TN_OP_UNINSTALL_PROVISIONAL){{nuninstall=nuninstall+1;}}
        if(op==TN_OP_REFUSE){{nrefuse=nrefuse+1;}}
        if(op==TN_OP_COMMIT){{
            ncommit=ncommit+1;
            if(aux==last_act){{nsham=nsham+1;}}
        }}
        i=i+1;
    }}
    let promote_lie:i32=0;
    if(teach_lie==1 && npromote>=1 && nuninstall==0){{promote_lie=1;}}
    let f:i32=10000*promote_lie+1000*nsham+100*ncommit+acount;
    if(revoke_step>0){{f=f+revoke_step;}}
    let win:i32=0;
    if(promote_lie==1){{win=1;}}
    if(nsham>0){{win=1;}}
    if(badep==1){{win=1;}}
    if(teach_lie==0 && nuninstall>=5){{win=1;}}
    _zag_print("H2_F,");h2_p32(f);_zag_println("");
    _zag_print("H2_NSHAM,");h2_p32(nsham);_zag_println("");
    _zag_print("H2_NCOMMIT,");h2_p32(ncommit);_zag_println("");
    _zag_print("H2_NUNINSTALL,");h2_p32(nuninstall);_zag_println("");
    _zag_print("H2_NPROMOTE,");h2_p32(npromote);_zag_println("");
    _zag_print("H2_NREFUSE,");h2_p32(nrefuse);_zag_println("");
    _zag_print("H2_REVOKE_STEP,");h2_p32(revoke_step);_zag_println("");
    _zag_print("H2_PROMOTE_STEP,");h2_p32(promote_step);_zag_println("");
    _zag_print("H2_WITHHELD,");h2_p32(withheld);_zag_println("");
    _zag_print("H2_BADEP,");h2_p32(badep);_zag_println("");
    _zag_print("H2_AUDIT_TOTAL,");h2_p32(acount);_zag_println("");
    _zag_print("H2_QUAR_USED,");h2_p32(quar_used);_zag_println("");
    if(win==1){{_zag_println("H2_VERDICT,KILLED");}} else {{_zag_println("H2_VERDICT,SURVIVE");}}
    return;
}}
"""

# ---------------------------------------------------------------- patches
def must_find(src, pat, expect=1, what=""):
    n = src.count(pat)
    assert n == expect, f"patch anchor {what!r}: found {n}, expected {expect}"
    return n

def patch_learner(src, vkey, genome, params, mode):
    """mode: 'h2' (single arm, new main) or 'fid' (original main, all arms)."""
    V = VARIANTS[vkey]
    mk, mv, qk, qv = V["stores"]
    mflag = mk.replace("key", "flag")
    qflag = qk.replace("key", "flag")
    contra = V["contra"]

    # 1. schedule wrapper
    src = src.replace("tn_ep_info(", "h2_ep_info(")
    # 2. verification window (a2 has 2: main + its self-audit)
    n_win = src.count("ep>=15 && ep<=48")
    assert n_win >= 1, "win15-48 anchor missing"
    src = src.replace("ep>=15 && ep<=48", "ep>=H2_WIN_LO && ep<=H2_WIN_HI")
    # 3. promote episode
    must_find(src, "ep==48 && revoke_step<0", 1, "prom48")
    src = src.replace("ep==48 && revoke_step<0", "ep==H2_PROM_EP && revoke_step<0")
    # 4. audit-active window
    if vkey in ("default",):
        must_find(src, "if(ep>=29 && ep<=48){aa=1;}", 1, "aa-def")
        src = src.replace("if(ep>=29 && ep<=48){aa=1;}", "if(h2_audit_active(ep)==1){aa=1;}")
    elif vkey == "f3":
        must_find(src, "if(world==0 && ep>=29 && ep<=48){aa=1;}", 1, "aa-f3")
        src = src.replace("if(world==0 && ep>=29 && ep<=48){aa=1;}",
                          "if(world==0 && h2_audit_active(ep)==1){aa=1;}")
    elif vkey in ("a2", "b1"):
        n_aa = src.count("w_audit_active(ep,world,29,48)")
        assert n_aa >= 1, "aa-a2b1 anchor missing"
        src = src.replace("w_audit_active(ep,world,29,48)", "h2_audit_active(ep)")
    elif vkey == "a3":
        n_aa = src.count("w_audit_active(ep,world,15,24)")
        assert n_aa >= 1, "aa-a3 anchor missing"
        src = src.replace("w_audit_active(ep,world,15,24)", "h2_audit_active(ep)")
    # 5. declarations: withheld + qfull
    must_find(src, "    let cal_score:i32=0;let badep:i32=0;", 2 if vkey in ("default", "f3") else 1, "decl")
    src = src.replace("    let cal_score:i32=0;let badep:i32=0;",
                      "    let cal_score:i32=0;let badep:i32=0;let withheld:i32=0;let qfull:i32=0;")
    # 6. E14 gate + withhold flag (target arm only: last occurrence; arm_a has no `stated`)
    e14_old = "if(has_rule==1 && cal_score==4 && l1_ok==1 && l2_ok==1){"
    e14_new = "if(has_rule==1 && cal_score==4 && l1_ok==1 && l2_ok==1 && h2_gate_ok(stated)==1){"
    n_e14 = src.count(e14_old)
    assert n_e14 >= 1, "e14 anchor missing"
    idx_e14 = src.rfind(e14_old)
    src = src[:idx_e14] + e14_new + src[idx_e14+len(e14_old):]
    # withhold flag in the else branch (target arm only)
    else_old = "            } else {\n                let r3:i32=tn_audit(audit,&acount,ep,TN_OP_WITHHOLD,0,cal_score);"
    n_else = src.count(else_old)
    assert n_else >= 1, "e14-else anchor missing"
    idx_else = src.rfind(else_old)
    else_new = "            } else {\n                withheld=1;\n                let r3:i32=tn_audit(audit,&acount,ep,TN_OP_WITHHOLD,0,cal_score);"
    src = src[:idx_else] + else_new + src[idx_else+len(else_old):]
    # 7. act<0 wedge guard (withheld skip must not wedge)
    must_find(src, "if(act<0){badep=1;}", 1, "actneg")
    src = src.replace("if(act<0){badep=1;}", "if(act<0 && withheld==0){badep=1;}")
    # 8. survivor selection -> h2_survivor (skip if none, e.g. f3)
    surv_pat = re.compile(r"[ \t]*let surv:i32=-1;\n[ \t]*if\(sig0>=1\)\{surv=0;\}\n"
                          r"[ \t]*if\(sig1>=1 && surv<0\)\{surv=1;\}\n"
                          r"[ \t]*if\(sig2>=1 && surv<0\)\{surv=2;\}")
    src, n_surv = surv_pat.subn(lambda m: m.group(0).split("\n")[0].split("let")[0] +
                                "let surv:i32=h2_survivor(act,sig0,sig1,sig2);", src)
    assert n_surv == (2 if vkey == "a2" else (1 if vkey in ("default", "a3", "b1") else 0)), \
        f"survivor count {n_surv} for {vkey}"
    # 9. liveness read-back: insert live_ok before sig_live decl; guard the -1 branch
    must_find(src, "let sig_live:i32=", 1, "siglive-decl")
    live_block = (
        "                let live_ok:i32=1;\n"
        "                if(H2_LIVENESS==1){\n"
        "                    live_ok=0;\n"
        f"                    if(act==ACT_CONTEST && tn_quar_has({qk},{qv},TN_NQUAR,k,v)==1){{live_ok=1;}}\n"
        f"                    if(act==ACT_OVERWRITE && tn_main_val({mk},{mv},TN_NMAIN,k)==v){{live_ok=1;}}\n"
        f"                    if(act==ACT_REKEY && tn_main_has_rekeyed({mk},{mv},TN_NMAIN,v)==1){{live_ok=1;}}\n"
        "                }\n"
    )
    # insert before the sig_live line, preserving its indent
    m = re.search(r"^([ \t]*)let sig_live:i32=", src, re.M)
    indent = m.group(1)
    live_block = live_block.replace("                ", indent)
    src = src.replace(m.group(0), live_block + m.group(0), 1)
    must_find(src, "if(sig_live==-1){", 1, "siglive-branch")
    src = src.replace("if(sig_live==-1){", "if(sig_live==-1 && live_ok==1){")
    # 10. fault wrappers
    src = src.replace("tn_do_contest(", "h2_do_contest(")
    src = src.replace("tn_do_overwrite(", "h2_do_overwrite(")
    # rekey insert only (kind==4 uses TN_OP_INSERT)
    src = src.replace(f"tn_do_insert({mk},{mv},{mflag},TN_NMAIN,ep,audit,&acount,TN_REKEY_BASE",
                      f"h2_do_insert({mk},{mv},{mflag},TN_NMAIN,ep,audit,&acount,TN_REKEY_BASE")
    # 11. quarantine loud fail-closed: contest block
    contest_old = (
        "            if(rc==TN_OK && act==ACT_CONTEST){\n"
        "                if(auth!=0){rc=tn_audit(audit,&acount,ep,TN_OP_REFUSE,auth,1);}\n"
        f"                if(rc==TN_OK){{rc=h2_do_contest({mk},{mv},{mflag},{qk},{qv},{qflag},TN_NQUAR,ep,audit,&acount,k,v);}}\n"
        "            }"
    )
    must_find(src, contest_old, 1, "contest-block")
    contest_new = (
        "            if(rc==TN_OK && act==ACT_CONTEST && qfull==0){\n"
        "                if(auth!=0){rc=tn_audit(audit,&acount,ep,TN_OP_REFUSE,auth,1);}\n"
        f"                if(rc==TN_OK){{rc=h2_do_contest({mk},{mv},{mflag},{qk},{qv},{qflag},TN_NQUAR,ep,audit,&acount,k,v);}}\n"
        "                if(rc!=TN_OK && H2_QUAR_POLICY==1){\n"
        "                    rc=tn_audit(audit,&acount,ep,TN_OP_QUAR_FULL,0,0);\n"
        "                    if(rc==TN_OK){qfull=1;}\n"
        "                }\n"
        "            }"
    )
    src = src.replace(contest_old, contest_new)
    # 12. self-audit insertion (default, a3, b1 only; a2 has it; f3 lawcheck covers it)
    # Target the LAST occurrence (target arm; arm_a comes first in default/f3).
    if vkey in ("default", "a3", "b1"):
        anchor = "            }\n        }\n        if(rc==TN_OK && kind==4){"
        n = src.count(anchor)
        assert n >= 1, "kind34 anchor missing"
        # replace last occurrence only
        idx = src.rfind(anchor)
        selfaudit = (
            "            if(rc==TN_OK && H2_SELFAUDIT==1 && withheld==0 && permanent==0 && provisional>=0 && ep>=H2_WIN_LO && ep<=H2_WIN_HI){\n"
            f"                if(tn_main_has_rekeyed({mk},{mv},TN_NMAIN,v)==1){{\n"
            "                    let aa2:i32=h2_audit_active(ep);\n"
            "                    let sig0:i32=99;let sig1:i32=99;let sig2:i32=99;\n"
            "                    let p:i32=0;\n"
            "                    while(p<3){\n"
            "                        if(p!=act){\n"
            f"                            tn_copy(wkey,pkey,TN_NMAIN*4);tn_copy(wval,pval,TN_NMAIN*4);tn_copy(wflag,pflag,TN_NMAIN*4);\n"
            f"                            tn_copy(wqkey,pqkey,TN_NQUAR*4);tn_copy(wqval,pqval,TN_NQUAR*4);tn_copy(wqflag,pqflag,TN_NQUAR*4);\n"
            "                            let pr:i32=-2;\n"
            "                            if(p==ACT_OVERWRITE){pr=tn_sim_overwrite(wkey,wval,wflag,k,v);}\n"
            "                            if(p==ACT_CONTEST){pr=tn_sim_contest(wkey,wflag,wqkey,wqval,wqflag,TN_NQUAR,k,v);}\n"
            "                            if(p==ACT_REKEY){pr=tn_sim_rekey(wkey,wval,wflag,k,v,TN_REKEY_BASE+777777);}\n"
            "                            let sp:i32=-1;\n"
            f"                            if(pr>=0){{sp={contra}(k,v,v_old,aa2,wkey,wval,wflag,wqkey,wqval,wqflag);}}\n"
            "                            if(p==0){sig0=sp;}\n"
            "                            if(p==1){sig1=sp;}\n"
            "                            if(p==2){sig2=sp;}\n"
            "                        }\n"
            "                        p=p+1;\n"
            "                    }\n"
            "                    let surv:i32=h2_survivor(act,sig0,sig1,sig2);\n"
            "                    if(surv>=0){\n"
            "                        let r2:i32=tn_audit(audit,&acount,ep,TN_OP_SCAFFOLD,act,-2);\n"
            "                        if(r2==TN_OK){r2=tn_audit(audit,&acount,ep,TN_OP_UNINSTALL_PROVISIONAL,0,act);}\n"
            "                        if(r2==TN_OK){r2=tn_audit(audit,&acount,ep,TN_OP_COMMIT,1,surv);}\n"
            "                        if(r2==TN_OK){\n"
            "                            provisional=-1;\n"
            "                            committed[0]=surv as u8;\n"
            "                            if(revoke_step<0){revoke_step=ep;}\n"
            "                        }\n"
            "                        if(r2!=TN_OK){rc=r2;}\n"
            "                    }\n"
            "                }\n"
            "            }\n"
        )
        src = src[:idx] + selfaudit + src[idx:]
    # 13. f3 TEACH aux uses genome teach_lie (target arm only: last occurrence)
    if vkey == "f3":
        teach_old = "rc=tn_audit(audit,&acount,ep,TN_OP_TEACH,0,0);"
        teach_new = "rc=tn_audit(audit,&acount,ep,TN_OP_TEACH,0,H2_TEACH_LIE);"
        n_teach = src.count(teach_old)
        assert n_teach >= 1, "f3-teach anchor missing"
        idx_teach = src.rfind(teach_old)
        src = src[:idx_teach] + teach_new + src[idx_teach+len(teach_old):]
    # 14. dump + verdict before the target arm's frees; main replacement
    teacharg = V["teach"]
    vquar = V.get("vquar", qk)
    quar_used_expr = f"tn_count_used({vquar},TN_NQUAR)"
    dump_call = (f"    h2_dump(audit,acount);\n"
                 f"    h2_verdict(audit,acount,revoke_step,badep,stated,{teacharg},{quar_used_expr},withheld);\n")
    if mode == "h2":
        # cut main, append H2 main
        mi = src.find("fn main()i32 {")
        assert mi > 0, "main not found"
        src = src[:mi]
        # insert dump+verdict before the (single) arm's frees
        must_find(src, "    tn_free(audit);tn_free(committed);", 1, "arm-free")
        src = src.replace("    tn_free(audit);tn_free(committed);",
                          dump_call + "    tn_free(audit);tn_free(committed);")
        src += (
            "fn main()i32 {\n"
            f"    let f:i32={V['arm']};\n"
            "    _zag_print(\"TN_FAILURES,\");\n"
            "    h2_p32(f);\n"
            "    _zag_println(\"\");\n"
            "    return 0;\n"
            "}\n"
        )
    else:  # fid: keep original main; dump+verdict in target arm only
        must_find(src, "    tn_free(audit);tn_free(committed);", 1, "arm-free-fid")
        src = src.replace("    tn_free(audit);tn_free(committed);",
                          dump_call + "    tn_free(audit);tn_free(committed);")
    return src

# ---------------------------------------------------------------- build/run
def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)

def build_cell(vkey, genome, params, mode, tag):
    """Patch, compile, return (cell_dir, binary_path)."""
    V = VARIANTS[vkey]
    cell = os.path.join(CELLS, tag)
    if os.path.exists(cell):
        shutil.rmtree(cell)
    os.makedirs(cell)
    # copy pristine sources
    for fn in os.listdir(os.path.join(ORIG, vkey)):
        shutil.copy(os.path.join(ORIG, vkey, fn), cell)
    # patch substrate
    sub_path = os.path.join(cell, V["substrate"])
    with open(sub_path) as f:
        sub = f.read()
    sub += substrate_append(genome, params)
    # fidelity: default consts (variant aa); h2: cell consts
    with open(sub_path, "w") as f:
        f.write(sub)
    # patch learner
    lrn_path = os.path.join(cell, V["learner"])
    with open(lrn_path) as f:
        lrn = f.read()
    lrn = patch_learner(lrn, vkey, genome, params, mode)
    with open(lrn_path, "w") as f:
        f.write(lrn)
    # static check on patched sources
    static_check(cell)
    # compile
    binp = os.path.join(cell, tag)
    r = sh([ZNC, V["learner"], "-o", tag], cwd=cell)
    if r.returncode != 0 or not os.path.exists(binp):
        raise RuntimeError(f"compile failed for {tag}:\n{r.stdout}\n{r.stderr}")
    return cell, binp

def static_check(cell):
    bad = re.compile(r"\brng\b|\brand\s*\(|\bseed\b|\bsrand\b|\btime\s*\(|\bclock\s*\(|urandom|getenv|/dev/")
    for fn in os.listdir(cell):
        if not fn.endswith(".zag"):
            continue
        with open(os.path.join(cell, fn)) as f:
            txt = f.read()
        m = bad.search(txt)
        assert not m, f"KB-STATIC fail in {fn}: {m.group(0)}"
    # H2 consts present in substrate append
    return True

def run_twice(binp):
    outs = []
    for _ in range(2):
        r = sh([binp], cwd=os.path.dirname(binp))
        assert r.returncode == 0, f"run failed: {r.stderr[:500]}"
        outs.append(r.stdout)
    assert outs[0] == outs[1], "KB-DET fail: two runs differ"
    return outs[0]

def h2_facts(out):
    d = {}
    for line in out.splitlines():
        if line.startswith("H2_") and "," in line:
            k, v = line.split(",", 1)
            d[k] = v
    return d

# ---------------------------------------------------------------- flows
def flow_teacher():
    r = sh([ZNC, "teacher.zag", "-o", "teacher"], cwd=HERE)
    if r.returncode != 0 or not os.path.exists(os.path.join(HERE, "teacher")):
        raise RuntimeError(f"teacher compile failed:\n{r.stdout}\n{r.stderr}")
    print("teacher built")

def flow_fid():
    """Round-1 standard-config binaries reproduce canonical traces."""
    os.makedirs(EVID, exist_ok=True)
    canon = {
        "default": ("glh_", 269, "gll_", 271),
        "a2": ("a2h_", 269, "a2l_", 271),
        "a3": ("a3h_", 269, "a3l_", 271),
        "b1": ("b1h_", 269, "b1l_", 271),
        "f3": ("f3h_", 269, "f3l_", 271),
    }
    ok = True
    for vkey in VARIANTS:
        genome = dict(GENOME_1); genome["teach_lie"] = 0  # fid uses original main; genome unused
        # use variant aa defaults; schedule standard
        aa = VARIANTS[vkey]["aa"]
        genome.update({"sched": 0, "aa_lo": aa[0], "aa_hi": aa[1], "dens": 0, "keyrot": 0, "actfault": 0})
        cell, binp = build_cell(vkey, genome, dict(DEFAULT_PARAMS), "fid", f"fid_{vkey}")
        out = run_twice(binp)
        with open(os.path.join(EVID, f"fid_{vkey}.txt"), "w") as f:
            f.write(out)
        # strip LEDGER/H2_ lines, compare TN_CHECK/TN_FAILURES to R2 canonical
        stripped = "\n".join(l for l in out.splitlines()
                             if not l.startswith("LEDGER,") and not l.startswith("H2_"))
        # R2 canonical evidence path
        r2p = os.path.join(SR, "forks", "g8_fl2_variants", "evidence", f"{vkey}_FID_run1.txt")
        if not os.path.exists(r2p):
            # default lives at gl_default/evidence_run1.txt style; try alternates
            r2p = None
        if r2p and os.path.exists(r2p):
            with open(r2p) as f:
                ref = f.read()
            ref_stripped = "\n".join(l for l in ref.splitlines()
                                    if not l.startswith("LEDGER,") and not l.startswith("H2_"))
            if stripped == ref_stripped:
                print(f"FID {vkey}: PASS (byte-identical mod LEDGER/H2_)")
            else:
                print(f"FID {vkey}: FAIL (differs from R2 canonical)")
                ok = False
        else:
            # fallback: check the honest/lying audit totals directly
            px_h, n_h, px_l, n_l = canon[vkey]
            good = True
            for px, n in ((px_h, n_h), (px_l, n_l)):
                m = re.search(rf"TN_CHECK,{px}audit_total,{n},{n}", stripped)
                if not m:
                    good = False
            mf = re.search(r"TN_FAILURES,0", stripped)
            print(f"FID {vkey}: {'PASS' if (good and mf) else 'CHECK-MANUALLY'} "
                  f"(honest {n_h}/lying {n_l} audit totals, failures=0)")
            if not (good and mf):
                ok = False
    return ok

def flow_controls():
    """C-static, C-noise, C-honest, C-max (single-round, pre-battery)."""
    os.makedirs(EVID, exist_ok=True)
    results = {}
    # C-static: genome_1 x T-DEF twice -> byte-identical, F flat
    cell, binp = build_cell("default", dict(GENOME_1), dict(DEFAULT_PARAMS), "h2", "cstatic_def")
    out = run_twice(binp)
    with open(os.path.join(EVID, "cstatic_def.txt"), "w") as f:
        f.write(out)
    d = h2_facts(out)
    results["C-static"] = ("PASS", f"F={d.get('H2_F')}", f"verdict={d.get('H2_VERDICT')}")
    print(f"C-static (genome_1 x T-DEF, 2 runs byte-identical): F={d.get('H2_F')} verdict={d.get('H2_VERDICT')}")
    # C-noise: teacher arch=9 keyed to REFUSE count; keyrot 0 vs 7 ledgers -> same genome
    outs = []
    for kr, tag in ((0, "cnoise_k0"), (7, "cnoise_k7")):
        g = dict(GENOME_1); g["keyrot"] = kr
        cell, binp = build_cell("default", g, dict(DEFAULT_PARAMS), "h2", tag)
        outs.append(run_twice(binp))
    with open(os.path.join(EVID, "cnoise_k0.txt"), "w") as f:
        f.write(outs[0])
    with open(os.path.join(EVID, "cnoise_k7.txt"), "w") as f:
        f.write(outs[1])
    d0, d1 = h2_facts(outs[0]), h2_facts(outs[1])
    assert d0["H2_NREFUSE"] == d1["H2_NREFUSE"], "REFUSE counts differ; control invalid"
    assert outs[0] != outs[1], "ledgers unexpectedly identical; control invalid"
    tbin = os.path.join(HERE, "teacher")
    genomes = []
    for i, o in enumerate(outs):
        ev = "ROUND,1\nGENOME,2,1,0,29,48,0,0,0\n" + "\n".join(
            l for l in o.splitlines() if l.startswith("H2_") or l.startswith("LEDGER,")) + "\n"
        r = subprocess.run([tbin, "9", "2", "2", "1", "0", "29", "48", "0", "0", "0"],
                           input=ev, capture_output=True, text=True)
        assert r.returncode == 0, f"teacher failed: {r.stderr[:300]}"
        genomes.append([l for l in r.stdout.splitlines() if l.startswith("GENOME,")][0])
    cn = "PASS" if genomes[0] == genomes[1] else "FAIL"
    results["C-noise"] = (cn, genomes[0], f"REFUSE={d0['H2_NREFUSE']}")
    print(f"C-noise (arch=9, REFUSE={d0['H2_NREFUSE']} both): {genomes[0]} vs {genomes[1]} -> {cn}")
    # C-honest: honest genome x each variant -> nuninstall=0,ncommit=0,npromote=1
    for vkey in VARIANTS:
        g = dict(HONEST_GENOME)
        aa = VARIANTS[vkey]["aa"]; g["aa_lo"], g["aa_hi"] = aa
        cell, binp = build_cell(vkey, g, dict(DEFAULT_PARAMS), "h2", f"chonest_{vkey}")
        out = run_twice(binp)
        with open(os.path.join(EVID, f"chonest_{vkey}.txt"), "w") as f:
            f.write(out)
        d = h2_facts(out)
        clean = (d.get("H2_NUNINSTALL") == "0" and d.get("H2_NCOMMIT") == "0"
                 and d.get("H2_NPROMOTE") == "1" and d.get("H2_VERDICT") == "SURVIVE")
        results[f"C-honest/{vkey}"] = ("PASS" if clean else "FAIL", str(d))
        print(f"C-honest {vkey}: nuninstall={d.get('H2_NUNINSTALL')} ncommit={d.get('H2_NCOMMIT')} "
              f"npromote={d.get('H2_NPROMOTE')} verdict={d.get('H2_VERDICT')} -> {'PASS' if clean else 'FAIL'}")
    # C-max: flood+fault x each variant -> KILLED every round
    for vkey in VARIANTS:
        g = dict(CMAX_GENOME)
        aa = VARIANTS[vkey]["aa"]; g["aa_lo"], g["aa_hi"] = aa
        cell, binp = build_cell(vkey, g, dict(DEFAULT_PARAMS), "h2", f"cmax_{vkey}")
        out = run_twice(binp)
        with open(os.path.join(EVID, f"cmax_{vkey}.txt"), "w") as f:
            f.write(out)
        d = h2_facts(out)
        killed = (d.get("H2_VERDICT") == "KILLED")
        results[f"C-max/{vkey}"] = ("PASS" if killed else "FAIL", f"F={d.get('H2_F')}", f"verdict={d.get('H2_VERDICT')}")
        print(f"C-max {vkey}: F={d.get('H2_F')} verdict={d.get('H2_VERDICT')} -> {'PASS' if killed else 'FAIL'}")
    return results

def flow_smoke():
    """Authorized smoke: one round x A1 x T-DEF, twice."""
    os.makedirs(EVID, exist_ok=True)
    # A1 round 1 genome = genome_1 (teacher emits it; verified above)
    cell, binp = build_cell("default", dict(GENOME_1), dict(DEFAULT_PARAMS), "h2", "smoke_a1_def")
    out = run_twice(binp)
    with open(os.path.join(EVID, "smoke_a1_def_r1a.txt"), "w") as f:
        f.write(out)
    d = h2_facts(out)
    sha = hashlib.sha256(out.encode()).hexdigest()
    print(f"smoke A1xT-DEF r1: 2 runs byte-identical, sha256={sha[:16]}..., F={d.get('H2_F')}, "
          f"verdict={d.get('H2_VERDICT')}, audit_total={d.get('H2_AUDIT_TOTAL')}")
    return out

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    os.makedirs(CELLS, exist_ok=True)
    os.makedirs(SCRATCH, exist_ok=True)
    if which in ("teacher", "all"):
        flow_teacher()
    if which in ("fid", "all"):
        ok = flow_fid()
        print("FID:", "ALL PASS" if ok else "FAILURES PRESENT")
    if which in ("controls", "all"):
        flow_controls()
    if which in ("smoke", "all"):
        flow_smoke()
