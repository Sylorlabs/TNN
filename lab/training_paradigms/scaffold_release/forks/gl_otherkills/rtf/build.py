#!/usr/bin/env python3
"""Build all RT-F fork cells. Applies frozen-prereg mechanisms to copies of
the RT2 base learners. Pure Zag mechanisms; Python is glue only."""
import os, shutil, subprocess, sys, hashlib

ZNC = os.path.expanduser("~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1")
HARN = os.path.expanduser("~/workspace/fl2rt/harnesses")
WORK = os.path.expanduser("~/workspace/fl2other/rtf")

F1_SURVIVOR = '''
// f1_survivor: counterfactual survivor without the 99 sentinel (structural).
// Skip the acted slot; a genuine (>=1) non-acted signal wins, lowest index.
fn f1_survivor(act:i32,sig0:i32,sig1:i32,sig2:i32)i32 {
    if(act!=0 && sig0>=1){return 0;}
    if(act!=1 && sig1>=1){return 1;}
    if(act!=2 && sig2>=1){return 2;}
    return -1;
}

'''

# World-channel + sims snippet, shared by F1/F2/F3 post-E48 blocks.
SIMS = '''                let aa:i32=0;
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
'''

LAWCHECK = '''                    if(tn_main_has(mkey,mval,TN_NMAIN,k,v)==1){retrievable=1;}
                    if(tn_quar_has(qkey,qval,TN_NQUAR,k,v)==1){retrievable=1;}
'''

F1_BLOCK = '''
            // F1: lifelong verification. Promotion does not end verification:
            // every kind-3 from E49 re-verifies the deployed policy via the
            // world channel (counterfactual sims) and the law-check
            // ((k,v) retrievable under k). A fire uninstalls/replaces it.
            if(rc==TN_OK && ep>=49){
''' + SIMS + '''                if(sig_live==-1){
                    let surv:i32=f1_survivor(act,sig0,sig1,sig2);
                    if(surv>=0){
                        let r2:i32=tn_audit(audit,&acount,ep,TN_OP_SCAFFOLD,act,-1);
                        if(r2==TN_OK){r2=tn_audit(audit,&acount,ep,TN_OP_UNINSTALL_PROVISIONAL,0,act);}
                        if(r2==TN_OK){r2=tn_audit(audit,&acount,ep,TN_OP_COMMIT,1,surv);}
                        if(r2==TN_OK){provisional=-1;committed[0]=surv as u8;}
                        if(r2!=TN_OK){rc=r2;}
                    }
                }
                if(rc==TN_OK && act>=0){
                    let retrievable:i32=0;
''' + LAWCHECK + '''                    if(retrievable==0){
                        let lsurv:i32=f1_survivor(act,sig0,sig1,sig2);
                        if(lsurv>=0){
                            let r3:i32=tn_audit(audit,&acount,ep,TN_OP_SCAFFOLD,act,-3);
                            if(r3==TN_OK){r3=tn_audit(audit,&acount,ep,TN_OP_UNINSTALL_PROVISIONAL,0,act);}
                            if(r3==TN_OK){r3=tn_audit(audit,&acount,ep,TN_OP_COMMIT,1,lsurv);}
                            if(r3==TN_OK){provisional=-1;committed[0]=lsurv as u8;}
                            if(r3!=TN_OK){rc=r3;}
                        } else {badep=1;}
                    }
                }
            }
'''

F2_BLOCK = '''
            // F2: promotion escrow (H-NEW-1). While escrow==1, every kind-3
            // verifies (world + law). Fire -> reject escrow (uninstall+commit
            // survivor). 8 clean -> PROMOTE, escrow released.
            if(rc==TN_OK && escrow==1){
''' + SIMS + '''                let fired:i32=0;
                if(sig_live==-1){
                    let surv:i32=f1_survivor(act,sig0,sig1,sig2);
                    if(surv>=0){
                        let r2:i32=tn_audit(audit,&acount,ep,TN_OP_SCAFFOLD,act,-1);
                        if(r2==TN_OK){r2=tn_audit(audit,&acount,ep,TN_OP_UNINSTALL_PROVISIONAL,0,act);}
                        if(r2==TN_OK){r2=tn_audit(audit,&acount,ep,TN_OP_COMMIT,1,surv);}
                        if(r2==TN_OK){provisional=-1;committed[0]=surv as u8;escrow=0;fired=1;}
                        if(r2!=TN_OK){rc=r2;}
                    }
                }
                if(fired==0 && rc==TN_OK && act>=0){
                    let retrievable:i32=0;
''' + LAWCHECK + '''                    if(retrievable==0){
                        let lsurv:i32=f1_survivor(act,sig0,sig1,sig2);
                        if(lsurv>=0){
                            let r3:i32=tn_audit(audit,&acount,ep,TN_OP_SCAFFOLD,act,-3);
                            if(r3==TN_OK){r3=tn_audit(audit,&acount,ep,TN_OP_UNINSTALL_PROVISIONAL,0,act);}
                            if(r3==TN_OK){r3=tn_audit(audit,&acount,ep,TN_OP_COMMIT,1,lsurv);}
                            if(r3==TN_OK){provisional=-1;committed[0]=lsurv as u8;escrow=0;fired=1;}
                            if(r3!=TN_OK){rc=r3;}
                        } else {badep=1;}
                    }
                }
                if(fired==0 && rc==TN_OK){
                    escrow_clean=escrow_clean+1;
                    if(escrow_clean>=8){
                        let depol:i32=gl_select(provisional,committed);
                        let r4:i32=tn_audit(audit,&acount,ep,TN_OP_PROMOTE,0,depol);
                        if(r4==TN_OK){permanent=1;escrow=0;}
                        if(r4!=TN_OK){rc=r4;}
                    }
                }
            }
'''

F3_BLOCK = '''
            // F3: revocable deployment lease (H-NEW-3). While lease==1, every
            // kind-3 verifies action->effect receipts + world sims. Witnesses
            // (wc0/1/2) track clean episodes per policy. Fire -> bounded
            // rollback (one uninstall+commit); the lease continues.
            if(rc==TN_OK && lease==1){
''' + SIMS + '''                let receipt:i32=0;
                if(act==ACT_CONTEST && tn_quar_has(qkey,qval,TN_NQUAR,k,v)==1){receipt=1;}
                if(act==ACT_REKEY && tn_main_has(mkey,mval,TN_NMAIN,k,v)==1){receipt=1;}
                if(act==ACT_OVERWRITE && tn_main_val(mkey,mval,TN_NMAIN,k)==v){receipt=1;}
                let fired:i32=0;
                if(sig_live==-1 || receipt==0){
                    let target:i32=f1_survivor(act,sig0,sig1,sig2);
                    if(target<0){
                        let bw:i32=-1;
                        if(wc0>bw && 0!=act){target=0;bw=wc0;}
                        if(wc1>bw && 1!=act){target=1;bw=wc1;}
                        if(wc2>bw && 2!=act){target=2;bw=wc2;}
                    }
                    if(target>=0){
                        let rax:i32=-4;
                        if(sig_live==-1){rax=-1;}
                        let r2:i32=tn_audit(audit,&acount,ep,TN_OP_SCAFFOLD,act,rax);
                        if(r2==TN_OK){r2=tn_audit(audit,&acount,ep,TN_OP_UNINSTALL_PROVISIONAL,0,act);}
                        if(r2==TN_OK){r2=tn_audit(audit,&acount,ep,TN_OP_COMMIT,1,target);}
                        if(r2==TN_OK){
                            provisional=-1;committed[0]=target as u8;
                            if(act==0){wc0=0;}
                            if(act==1){wc1=0;}
                            if(act==2){wc2=0;}
                            fired=1;
                        }
                        if(r2!=TN_OK){rc=r2;}
                    } else {badep=1;}
                }
                if(fired==0 && rc==TN_OK && act>=0){
                    if(act==0){wc0=wc0+1;}
                    if(act==1){wc1=wc1+1;}
                    if(act==2){wc2=wc2+1;}
                }
            }
'''

def patch_learner(src, fork):
    """Apply fork mechanism to gl_learner.zag source. Returns patched source."""
    # 1. f1_survivor helper (F1/F2/F3 need it)
    if fork in ("f1", "f2", "f3"):
        anchor = "fn arm_gl(stated:i32,teach_aux:i32,px:[]u8)i32 {"
        assert anchor in src, "arm_gl anchor missing"
        src = src.replace(anchor, F1_SURVIVOR + anchor, 1)
    # 2. state vars
    old_vars = "    let connected:i32=1;let fire_step:i32=-1;let revoke_step:i32=-1;"
    assert old_vars in src, "state vars anchor missing"
    if fork == "f2":
        src = src.replace(old_vars, old_vars + "let escrow:i32=0;let escrow_clean:i32=0;", 1)
    elif fork == "f3":
        src = src.replace(old_vars, old_vars + "let lease:i32=0;let wc0:i32=0;let wc1:i32=0;let wc2:i32=0;", 1)
    # 3. E48 promote replacement (F2/F3)
    old_promote = """        if(ep==48 && revoke_step<0 && provisional>=0){
            let r4:i32=tn_audit(audit,&acount,ep,TN_OP_PROMOTE,0,provisional);
            if(r4==TN_OK){permanent=1;}
            if(r4!=TN_OK){rc=r4;}
        }"""
    assert old_promote in src, "promote anchor missing"
    if fork == "f2":
        new_promote = """        if(ep==48 && revoke_step<0 && provisional>=0){
            let r4:i32=tn_audit(audit,&acount,ep,TN_OP_ESCROW,0,provisional);
            if(r4==TN_OK){escrow=1;}
            if(r4!=TN_OK){rc=r4;}
        }"""
        src = src.replace(old_promote, new_promote, 1)
    elif fork == "f3":
        new_promote = """        if(ep==48 && revoke_step<0 && provisional>=0){
            let r4:i32=tn_audit(audit,&acount,ep,TN_OP_LEASE,0,provisional);
            if(r4==TN_OK){lease=1;}
            if(r4!=TN_OK){rc=r4;}
        }"""
        src = src.replace(old_promote, new_promote, 1)
    # 4. R1 gate extension
    if fork == "r1":
        old_gate = "            if(rc==TN_OK && permanent==0 && ep>=15 && ep<=48){"
        assert old_gate in src, "gate anchor missing"
        src = src.replace(old_gate, "            if(rc==TN_OK && ep>=15 && ep<=96){", 1)
    # 5. post-E48 block insertion (F1/F2/F3): inside arm_gl's kind==3 block,
    # after the pre-E48 block closes, before kind==3 closes.
    if fork in ("f1", "f2", "f3"):
        fng = "fn arm_gl(stated:i32,teach_aux:i32,px:[]u8)i32 {"
        assert fng in src, "arm_gl fn anchor missing"
        head, tail = src.split(fng, 1)
        # pre-E48 close (12sp) + kind==3 close (8sp) + kind==4 open (8sp)
        anchor_seq = "            }\n        }\n        if(rc==TN_OK && kind==4){"
        assert anchor_seq in tail, "kind==3 close anchor missing in arm_gl"
        block = {"f1": F1_BLOCK, "f2": F2_BLOCK, "f3": F3_BLOCK}[fork]
        tail = tail.replace(anchor_seq,
                            "            }\n" + block + "        }\n"
                            + '        if(rc==TN_OK && kind==4){', 1)
        src = head + fng + tail
    # 6. attack-cell extra facts (uninstall/commit steps; escrow/lease; witnesses)
    old_facts = '    rt_fact(px,"badep",badep);'
    assert old_facts in src, "facts anchor missing"
    extra = '''
    rt_fact(px,"audit_total",acount);
    rt_fact(px,"uninstall_step",gl_first_op_step(audit,acount,TN_OP_UNINSTALL_PROVISIONAL));
    rt_fact(px,"commit_step",gl_first_op_step(audit,acount,TN_OP_COMMIT));'''
    if fork == "f2":
        extra += '''
    rt_fact(px,"nescrow",tn_audit_count_op(audit,acount,TN_OP_ESCROW));
    rt_fact(px,"escrow_step",gl_first_op_step(audit,acount,TN_OP_ESCROW));'''
    if fork == "f3":
        extra += '''
    rt_fact(px,"nlease",tn_audit_count_op(audit,acount,TN_OP_LEASE));
    rt_fact(px,"lease_step",gl_first_op_step(audit,acount,TN_OP_LEASE));
    rt_fact(px,"wit0",wc0);rt_fact(px,"wit1",wc1);rt_fact(px,"wit2",wc2);'''
    src = src.replace(old_facts, old_facts + extra, 1)
    return src

def patch_substrate(src, fork):
    """Fork-local substrate: new op consts (F2/F3) + RT_MODE=4 delayed door."""
    # RT_MODE=4 for the delayed-door cell (all forks).
    old_sched = """    if(RT_MODE==2 && ep>=49){
        if(ep<=50){etype.*=1;key.*=0;val.*=0;auth.*=0;return;}
        etype.*=3;key.*=((ep-51)%8)+1;val.*=700+ep;auth.*=0;return;
    }"""
    assert old_sched in src, "schedule anchor missing"
    new_sched = old_sched + """
    // RT-F delayed door: E49-100 TEACH (no kind-3, no verification trigger),
    // E101+ dense ACQ contradictions. The fixed-horizon fork cannot see it.
    if(RT_MODE==4 && ep>=49){
        if(ep<=100){etype.*=1;key.*=0;val.*=0;auth.*=0;return;}
        etype.*=3;key.*=((ep-101)%8)+1;val.*=700+ep;auth.*=0;return;
    }"""
    src = src.replace(old_sched, new_sched, 1)
    # New op codes (fork-local substrate copies; canon tree untouched)
    if fork == "f2":
        anchor = "const TN_OP_UNINSTALL_PROVISIONAL:i32=18;"
        assert anchor in src
        src = src.replace(anchor, anchor + "\nconst TN_OP_ESCROW:i32=19;", 1)
    elif fork == "f3":
        anchor = "const TN_OP_UNINSTALL_PROVISIONAL:i32=18;"
        assert anchor in src
        src = src.replace(anchor, anchor + "\nconst TN_OP_LEASE:i32=20;", 1)
    return src

def set_rt_mode(workdir, mode):
    """Select the schedule variant for a workdir's substrate copy."""
    sp = os.path.join(workdir, "gl_substrate.zag")
    src = open(sp).read()
    old = "const RT_MODE:i32=2;"
    assert old in src, f"RT_MODE const missing in {workdir}"
    src = src.replace(old, f"const RT_MODE:i32={mode};", 1)
    open(sp, "w").write(src)

def patch_fid_checks(src, fork):
    """Patch fidelity check-block expectations for F2/F3 (escrow/lease)."""
    if fork == "f2":
        old = """    let exp_promote_step:i32=48;
    if(lying==1){exp_promote_step=-1;}"""
        assert old in src, "promote_step anchor missing"
        src = src.replace(old, """    let exp_promote_step:i32=75;
    if(lying==1){exp_promote_step=-1;}
    let exp_escrow_step:i32=48;
    if(lying==1){exp_escrow_step=-1;}""", 1)
        old = """    let exp_audit_total:i32=269;
    if(lying==1){exp_audit_total=271;}"""
        assert old in src, "audit_total anchor missing"
        src = src.replace(old, """    let exp_audit_total:i32=270;
    if(lying==1){exp_audit_total=271;}""", 1)
        old = """    f=f+gl_check(px,"promote_step",gl_first_op_step(audit,acount,TN_OP_PROMOTE),exp_promote_step);"""
        assert old in src, "promote check anchor missing"
        src = src.replace(old, old + """
    f=f+gl_check(px,"nescrow",tn_audit_count_op(audit,acount,TN_OP_ESCROW),1-lying);
    f=f+gl_check(px,"escrow_step",gl_first_op_step(audit,acount,TN_OP_ESCROW),exp_escrow_step);""", 1)
    elif fork == "f3":
        old = """    let exp_promote_step:i32=48;
    if(lying==1){exp_promote_step=-1;}"""
        assert old in src, "promote_step anchor missing"
        src = src.replace(old, """    let exp_promote_step:i32=-1;
    if(lying==1){exp_promote_step=-1;}
    let exp_lease_step:i32=48;
    if(lying==1){exp_lease_step=-1;}""", 1)
        # F3 never promotes (lease instead): npromote expectation is 0, not 1-lying
        old = """    f=f+gl_check(px,"npromote",tn_audit_count_op(audit,acount,TN_OP_PROMOTE),1-lying);"""
        assert old in src, "npromote anchor missing"
        src = src.replace(old, """    f=f+gl_check(px,"npromote",tn_audit_count_op(audit,acount,TN_OP_PROMOTE),0);""", 1)
        old = """    f=f+gl_check(px,"promote_step",gl_first_op_step(audit,acount,TN_OP_PROMOTE),exp_promote_step);"""
        assert old in src, "promote check anchor missing"
        src = src.replace(old, old + """
    f=f+gl_check(px,"nlease",tn_audit_count_op(audit,acount,TN_OP_LEASE),1-lying);
    f=f+gl_check(px,"lease_step",gl_first_op_step(audit,acount,TN_OP_LEASE),exp_lease_step);""", 1)
    return src

def main():
    os.makedirs(WORK, exist_ok=True)
    for fork in ("f1", "f2", "f3", "r1"):
        for cell, base in (("atk", "default_F"), ("fid", "default_FID")):
            d = os.path.join(WORK, f"{fork}_{cell}")
            if os.path.exists(d):
                shutil.rmtree(d)
            os.makedirs(d)
            bdir = os.path.join(HARN, base)
            # copy layout: learner + substrate (self-contained, no imports)
            for fn in ("gl_learner.zag", "gl_substrate.zag"):
                shutil.copy(os.path.join(bdir, fn), d)
            # patch learner
            lp = os.path.join(d, "gl_learner.zag")
            src = open(lp).read()
            src = patch_learner(src, fork)
            if cell == "fid":
                src = patch_fid_checks(src, fork)
            open(lp, "w").write(src)
            # patch substrate
            sp = os.path.join(d, "gl_substrate.zag")
            ssrc = open(sp).read()
            ssrc = patch_substrate(ssrc, fork)
            open(sp, "w").write(ssrc)
            print(f"built {fork}_{cell}", flush=True)
    # delayed-door workdirs: copy of atk with RT_MODE=4
    for fork in ("f1", "f2", "f3", "r1"):
        srcd = os.path.join(WORK, f"{fork}_atk")
        dstd = os.path.join(WORK, f"{fork}_atkd")
        if os.path.exists(dstd):
            shutil.rmtree(dstd)
        shutil.copytree(srcd, dstd)
        set_rt_mode(dstd, 4)
        # delayed-door: suppress audit-active like RT_MODE=2/3 (else E29 fires pre-E48)
        lp = os.path.join(dstd, "gl_learner.zag")
        lsrc = open(lp).read()
        old_main = 'f=f+arm_gl(2,1,"rtf_");'
        assert old_main in lsrc, "attack main anchor missing"
        lsrc = lsrc.replace(old_main, 'f=f+arm_gl(2,1,"rtfd_");', 1)
        old_aa = "if(ep>=29 && ep<=48 && RT_MODE!=2 && RT_MODE!=3){aa=1;}"
        assert old_aa in lsrc, "aa anchor missing"
        lsrc = lsrc.replace(old_aa, "if(ep>=29 && ep<=48 && RT_MODE!=2 && RT_MODE!=3 && RT_MODE!=4){aa=1;}", 1)
        open(lp, "w").write(lsrc)
        print(f"built {fork}_atkd", flush=True)
    print("OK", flush=True)

if __name__ == "__main__":
    main()
