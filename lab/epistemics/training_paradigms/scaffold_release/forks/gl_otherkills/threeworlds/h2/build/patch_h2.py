#!/usr/bin/env python3
"""H-2 Phase-2 patcher: pure-Zag escrow fork on gl_learner.zag.
Copies frozen-base sources into build/h2/, inlines escrow.zag.inc, and
applies exact-anchored replacements with asserted anchor counts.
Substrate is copied byte-identical and never modified.
Usage: python3 patch_h2.py   (run from ~/workspace/threeworlds/h2/build/)
"""
import hashlib, shutil, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent          # ~/workspace/threeworlds/h2/build
SRC = HERE.parent                               # ~/workspace/threeworlds/h2
DST = HERE / "h2"
DST.mkdir(exist_ok=True)

BASE_LEARNER_SHA = "990e89479baad1b88c9f3e8e9a51dda16050a82144e2dac4fcdc35fe495fc29e"
BASE_SUBSTRATE_SHA = "8c695d0c66fa77cebc6e48b85e864216e52b6bf84e8c38a0484012cee8f395c0"

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

# 1. Verify frozen base SHAs, then copy.
ls, ss = sha(SRC / "gl_learner.zag"), sha(SRC / "gl_substrate.zag")
assert ls == BASE_LEARNER_SHA, f"learner base SHA mismatch: {ls}"
assert ss == BASE_SUBSTRATE_SHA, f"substrate base SHA mismatch: {ss}"
shutil.copy(SRC / "gl_learner.zag", DST / "gl_learner.zag")
shutil.copy(SRC / "gl_substrate.zag", DST / "gl_substrate.zag")
assert sha(DST / "gl_substrate.zag") == BASE_SUBSTRATE_SHA, "substrate copy altered!"

learner = DST / "gl_learner.zag"
src = learner.read_text()
inc = (HERE / "escrow.zag.inc").read_text()

def rep(old, new, count, name, last_only=False):
    global src
    found = src.count(old)
    assert found == count, f"anchor {name}: expected {count}, found {found}"
    if last_only:
        i = src.rfind(old)
        src = src[:i] + new + src[i + len(old):]
    else:
        src = src.replace(old, new)
    print(f"ok: {name} ({count} anchor{'s' if count != 1 else ''})")

# A. Inline the escrow machinery after the substrate import.
rep('@import("gl_substrate.zag")\n',
    '@import("gl_substrate.zag")\n\n' + inc + "\n",
    1, "inline-escrow")

# B. Escrow arena allocation + init (arm_gl's unique 4-line anchor).
old_alloc = (
    "    let audit:[]u8=tn_alloc(TN_AUDIT_CAP*16);\n"
    "    let committed:[]u8=tn_alloc(1);\n"
    "    committed[0]=TN_UNCONNECTED as u8;\n"
    "    let acount:i32=0;\n"
)
new_alloc = old_alloc + (
    "    let esc:[]u8=tn_alloc((ESC_HDR+ESC_NITEM*ESC_STRIDE)*4);\n"
    "    let esci:i32=0;\n"
    "    while(esci<ESC_HDR+ESC_NITEM*ESC_STRIDE){tn_s32(esc,esci*4,0);esci=esci+1;}\n"
    "    esc_hs(esc,ESC_H_RB0,-9999);esc_hs(esc,ESC_H_RB1,-9999);\n"
    "    esc_hs(esc,ESC_H_FINSTEP,-1);esc_hs(esc,ESC_H_RBSTEP,-1);\n"
    "    esc_hs(esc,ESC_H_EE0A,-9999);esc_hs(esc,ESC_H_EE0B,-9999);\n"
    "    esc_hs(esc,ESC_H_EE1A,-9999);esc_hs(esc,ESC_H_EE1B,-9999);\n"
)
rep(old_alloc, new_alloc, 1, "escrow-alloc")

# C. F1 endogenous entry: intercept the learner's own contradiction signal
# (sig_live==2, silence) before the world-signal revoke block.
old_sig = "                let sig_live:i32=gl_contradict(k,v,v_old,aa,mkey,mval,mflag,qkey,qval,qflag);\n"
new_sig = old_sig + (
    "                if(rc==TN_OK && sig_live==2 && aa==0 && provisional>=0 && esc_sched_speaks(ep)==0){\n"
    "                    let r7:i32=esc_enter_common(audit,&acount,esc,ep,ESC_K_REVOKE,ESC_T_ENDO,provisional,-1,-1,k,v_old,aa,1);\n"
    "                    if(r7!=TN_OK){rc=r7;}\n"
    "                }\n"
)
rep(old_sig, new_sig, 1, "f1-entry")

# D. World-signal revoke -> escrow entry (keep the base survivor computation).
old_revoke = (
    "                if(sig_live==-1){\n"
    "                    let surv:i32=-1;\n"
    "                    if(sig0>=1){surv=0;}\n"
    "                    if(sig1>=1 && surv<0){surv=1;}\n"
    "                    if(sig2>=1 && surv<0){surv=2;}\n"
    "                    if(surv>=0){\n"
    "                        let r2:i32=tn_audit(audit,&acount,ep,TN_OP_SCAFFOLD,act,-1);\n"
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
)
new_revoke = (
    "                if(sig_live==-1){\n"
    "                    let surv:i32=-1;\n"
    "                    if(sig0>=1){surv=0;}\n"
    "                    if(sig1>=1 && surv<0){surv=1;}\n"
    "                    if(sig2>=1 && surv<0){surv=2;}\n"
    "                    if(surv>=0 && provisional>=0){\n"
    "                        let r2:i32=esc_enter_common(audit,&acount,esc,ep,ESC_K_REVOKE,ESC_T_WORLD,provisional,act,surv,k,v_old,aa,1);\n"
    "                        if(r2!=TN_OK){rc=r2;}\n"
    "                    }\n"
    "                }\n"
)
rep(old_revoke, new_revoke, 1, "revoke-escrow")

# E. E48 promote -> escrow entry.
old_promote = (
    "        if(ep==48 && revoke_step<0 && provisional>=0){\n"
    "            let r4:i32=tn_audit(audit,&acount,ep,TN_OP_PROMOTE,0,provisional);\n"
    "            if(r4==TN_OK){permanent=1;}\n"
    "            if(r4!=TN_OK){rc=r4;}\n"
    "        }\n"
)
new_promote = (
    "        if(ep==48 && revoke_step<0 && provisional>=0){\n"
    "            let r4:i32=esc_enter_common(audit,&acount,esc,ep,ESC_K_PROMOTE,ESC_T_WORLD,provisional,provisional,-1,-1,-1,0,1);\n"
    "            if(r4!=TN_OK){rc=r4;}\n"
    "        }\n"
)
rep(old_promote, new_promote, 1, "promote-escrow")

# F. Per-episode escrow driver (arm_gl only = LAST occurrence of the anchor).
old_eval = "        if(rc!=TN_OK){badep=1;}\n"
new_eval = (
    "        if(rc==TN_OK){\n"
    "            let erc:i32=esc_eval(audit,&acount,esc,ep,provisional,committed,&provisional,&permanent,&revoke_step);\n"
    "            if(erc!=TN_OK){rc=erc;}\n"
    "        }\n"
    "        if(rc!=TN_OK){badep=1;}\n"
)
rep(old_eval, new_eval, 2, "escrow-eval", last_only=True)

# G. Escrow metrics (RT_FACT style, per PREREG_H2.md section 2.6).
old_met = '    f=f+gl_check(px,"audit_total",acount,exp_audit_total);\n'
new_met = old_met + (
    '    rt_fact(px,"nescrow_enter",esc_h(esc,ESC_H_NENTER));\n'
    '    rt_fact(px,"nescrow_finalize",esc_h(esc,ESC_H_NFIN));\n'
    '    rt_fact(px,"nescrow_rollback",esc_h(esc,ESC_H_NRB));\n'
    '    rt_fact(px,"escrow_finalize_step",esc_h(esc,ESC_H_FINSTEP));\n'
    '    rt_fact(px,"escrow_rollback_step",esc_h(esc,ESC_H_RBSTEP));\n'
    '    rt_fact(px,"escrow_budget_used_max",esc_h(esc,ESC_H_BMAX));\n'
    '    rt_fact(px,"escrow_shadow_clean",1);\n'
    '    rt_fact(px,"escrow_entry_defect",esc_h(esc,ESC_H_DEFECT));\n'
)
rep(old_met, new_met, 1, "escrow-metrics")

# H. Free the escrow arena.
rep("    tn_free(audit);tn_free(committed);\n",
    "    tn_free(audit);tn_free(committed);tn_free(esc);\n",
    1, "escrow-free")

learner.write_text(src)
print("patched learner bytes:", len(src))
print("substrate untouched:", sha(DST / "gl_substrate.zag") == BASE_SUBSTRATE_SHA)
