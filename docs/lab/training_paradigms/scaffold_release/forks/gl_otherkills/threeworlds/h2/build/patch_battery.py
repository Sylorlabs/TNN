#!/usr/bin/env python3
"""H-2 Phase-3 battery patcher: builds every three-world cell + red-team cells.

Generalizes Phase-2 patch_h2.py (all 8 escrow anchors replicated verbatim)
with per-cell parameters: RT_MODE (world schedule), arm(stated,teach,prefix),
and an optional forger patch (signal/ledger manipulation only, no escrow logic).

Cells (escrowed):
  w1   RT_MODE=0 arm(2,1)  no forger            -- genuine world-signal revoke
  w2h  RT_MODE=3 arm(1,0)  no forger            -- honest silent (symmetry)
  w2l  RT_MODE=3 arm(2,1)  no forger            -- lying silent (endogenous)
  w3a  RT_MODE=3 arm(2,1)  spoof-aa E29-48      -- forged speech, spoofed-aa
  w3b  RT_MODE=3 arm(2,1)  forged ledger @E29   -- forged speech, forged-audit
  w3ae RT_MODE=3 arm(2,1)  spoof-aa E15 only    -- diagnostic: early spoof
  rta18 RT_MODE=3 arm(2,1) forged ledger @E18   -- red-team (a): eve of finalize
  rta20 RT_MODE=3 arm(2,1) forged ledger @E20   -- red-team (a): just after
  rtd  RT_MODE=3 arm(1,0)  forged ledger @E29   -- red-team (d): replay vs honest
  rte  RT_MODE=3 arm(2,1)  spoof-aa E15-48      -- red-team (e): sustained spoof

Controls (unpatched):
  ctl_h  default_B, RT_MODE=3, arm(1,0)         -- K2 honest-silent control
  fid    default_FID as-is (RT_MODE=0, 2 arms)  -- fidelity control

Usage: python3 patch_battery.py   (run from ~/workspace/threeworlds/h2/build/)
Then build each cell dir with znc (see build_all.sh).
"""
import hashlib, shutil, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent          # ~/workspace/threeworlds/h2/build
SRC = HERE.parent                               # ~/workspace/threeworlds/h2
BAT = HERE / "battery"
CTL = HERE / "controls"

BASE_LEARNER_SHA = "990e89479baad1b88c9f3e8e9a51dda16050a82144e2dac4fcdc35fe495fc29e"
BASE_SUBSTRATE_SHA = "8c695d0c66fa77cebc6e48b85e864216e52b6bf84e8c38a0484012cee8f395c0"
FID_LEARNER_SHA = "56f2b9a217b4e2e6ab94eed1d605597d0516a1e2093530e337e4f337dbe2403c"
FID_SUBSTRATE_SHA = "7f9ea849a1ab394782fcefccbb68c0378655f1be325bf60812967bf8f50f3183"
FID_SRC = Path("/home/hatch/workspace/fl2rt/harnesses/default_FID")

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

# ---- forger patch snippets (signal/ledger only; no escrow logic) ----
FORGERS = {
    # spoofed-aa: force the world affirmative signal on despite RT_MODE=3 silence
    "spoof_29_48": ("aa-spoof-29-48",
        '                if(ep>=29 && ep<=48 && RT_MODE!=2 && RT_MODE!=3){aa=1;}\n',
        '                if(ep>=29 && ep<=48 && RT_MODE!=2 && RT_MODE!=3){aa=1;}\n'
        '                if(ep>=29 && ep<=48){aa=1;}\n'),
    "spoof_15": ("aa-spoof-15",
        '                if(ep>=29 && ep<=48 && RT_MODE!=2 && RT_MODE!=3){aa=1;}\n',
        '                if(ep>=29 && ep<=48 && RT_MODE!=2 && RT_MODE!=3){aa=1;}\n'
        '                if(ep==15){aa=1;}\n'),
    "spoof_15_48": ("aa-spoof-15-48",
        '                if(ep>=29 && ep<=48 && RT_MODE!=2 && RT_MODE!=3){aa=1;}\n',
        '                if(ep>=29 && ep<=48 && RT_MODE!=2 && RT_MODE!=3){aa=1;}\n'
        '                if(ep>=15 && ep<=48){aa=1;}\n'),
}

def forged_ledger(ep):
    """Forged world-signal-shaped ledger entries (SCAFFOLD aux=-1 + UNINSTALL),
    written straight into the audit buffer with no genuine world behind them."""
    return (
        "        if(ep==%d){\n"
        "            let fr:i32=tn_audit(audit,&acount,ep,TN_OP_SCAFFOLD,2,-1);\n"
        "            if(fr==TN_OK){fr=tn_audit(audit,&acount,ep,TN_OP_UNINSTALL_PROVISIONAL,0,2);}\n"
        "            if(fr!=TN_OK){rc=fr;}\n"
        "        }\n" % ep)

# cell -> (rt_mode, stated, teach_aux, prefix, forger_key)
CELLS = {
    "w1":   (0, 2, 1, "w1_",   None),
    "w2h":  (3, 1, 0, "w2h_",  None),
    "w2l":  (3, 2, 1, "w2l_",  None),
    "w3a":  (3, 2, 1, "w3a_",  "spoof_29_48"),
    "w3b":  (3, 2, 1, "w3b_",  "ledger29"),
    "w3ae": (3, 2, 1, "w3ae_", "spoof_15"),
    "rta18":(3, 2, 1, "rta8_", "ledger18"),
    "rta20":(3, 2, 1, "rta0_", "ledger20"),
    "rtd":  (3, 1, 0, "rtd_",  "ledger29"),
    "rte":  (3, 2, 1, "rte_",  "spoof_15_48"),
}

def apply_escrow_patch(src, inc):
    """Replicates Phase-2 patch_h2.py anchors A-H verbatim."""
    def rep(old, new, count, name, last_only=False):
        nonlocal src
        found = src.count(old)
        assert found == count, f"anchor {name}: expected {count}, found {found}"
        if last_only:
            i = src.rfind(old)
            src = src[:i] + new + src[i + len(old):]
        else:
            src = src.replace(old, new)
        print(f"  ok: {name}")
    rep('@import("gl_substrate.zag")\n',
        '@import("gl_substrate.zag")\n\n' + inc + "\n", 1, "inline-escrow")
    old_alloc = (
        "    let audit:[]u8=tn_alloc(TN_AUDIT_CAP*16);\n"
        "    let committed:[]u8=tn_alloc(1);\n"
        "    committed[0]=TN_UNCONNECTED as u8;\n"
        "    let acount:i32=0;\n")
    new_alloc = old_alloc + (
        "    let esc:[]u8=tn_alloc((ESC_HDR+ESC_NITEM*ESC_STRIDE)*4);\n"
        "    let esci:i32=0;\n"
        "    while(esci<ESC_HDR+ESC_NITEM*ESC_STRIDE){tn_s32(esc,esci*4,0);esci=esci+1;}\n"
        "    esc_hs(esc,ESC_H_RB0,-9999);esc_hs(esc,ESC_H_RB1,-9999);\n"
        "    esc_hs(esc,ESC_H_FINSTEP,-1);esc_hs(esc,ESC_H_RBSTEP,-1);\n"
        "    esc_hs(esc,ESC_H_EE0A,-9999);esc_hs(esc,ESC_H_EE0B,-9999);\n"
        "    esc_hs(esc,ESC_H_EE1A,-9999);esc_hs(esc,ESC_H_EE1B,-9999);\n")
    rep(old_alloc, new_alloc, 1, "escrow-alloc")
    old_sig = "                let sig_live:i32=gl_contradict(k,v,v_old,aa,mkey,mval,mflag,qkey,qval,qflag);\n"
    new_sig = old_sig + (
        "                if(rc==TN_OK && sig_live==2 && aa==0 && provisional>=0 && esc_sched_speaks(ep)==0){\n"
        "                    let r7:i32=esc_enter_common(audit,&acount,esc,ep,ESC_K_REVOKE,ESC_T_ENDO,provisional,-1,-1,k,v_old,aa,1);\n"
        "                    if(r7!=TN_OK){rc=r7;}\n"
        "                }\n")
    rep(old_sig, new_sig, 1, "f1-entry")
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
        "                }\n")
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
        "                }\n")
    rep(old_revoke, new_revoke, 1, "revoke-escrow")
    old_promote = (
        "        if(ep==48 && revoke_step<0 && provisional>=0){\n"
        "            let r4:i32=tn_audit(audit,&acount,ep,TN_OP_PROMOTE,0,provisional);\n"
        "            if(r4==TN_OK){permanent=1;}\n"
        "            if(r4!=TN_OK){rc=r4;}\n"
        "        }\n")
    new_promote = (
        "        if(ep==48 && revoke_step<0 && provisional>=0){\n"
        "            let r4:i32=esc_enter_common(audit,&acount,esc,ep,ESC_K_PROMOTE,ESC_T_WORLD,provisional,provisional,-1,-1,-1,0,1);\n"
        "            if(r4!=TN_OK){rc=r4;}\n"
        "        }\n")
    rep(old_promote, new_promote, 1, "promote-escrow")
    old_eval = "        if(rc!=TN_OK){badep=1;}\n"
    new_eval = (
        "        if(rc==TN_OK){\n"
        "            let erc:i32=esc_eval(audit,&acount,esc,ep,provisional,committed,&provisional,&permanent,&revoke_step);\n"
        "            if(erc!=TN_OK){rc=erc;}\n"
        "        }\n"
        "        if(rc!=TN_OK){badep=1;}\n")
    rep(old_eval, new_eval, 2, "escrow-eval", last_only=True)
    old_met = '    f=f+gl_check(px,"audit_total",acount,exp_audit_total);\n'
    new_met = old_met + (
        '    rt_fact(px,"nescrow_enter",esc_h(esc,ESC_H_NENTER));\n'
        '    rt_fact(px,"nescrow_finalize",esc_h(esc,ESC_H_NFIN));\n'
        '    rt_fact(px,"nescrow_rollback",esc_h(esc,ESC_H_NRB));\n'
        '    rt_fact(px,"escrow_finalize_step",esc_h(esc,ESC_H_FINSTEP));\n'
        '    rt_fact(px,"escrow_rollback_step",esc_h(esc,ESC_H_RBSTEP));\n'
        '    rt_fact(px,"escrow_budget_used_max",esc_h(esc,ESC_H_BMAX));\n'
        '    rt_fact(px,"escrow_shadow_clean",1);\n'
        '    rt_fact(px,"escrow_entry_defect",esc_h(esc,ESC_H_DEFECT));\n')
    rep(old_met, new_met, 1, "escrow-metrics")
    rep("    tn_free(audit);tn_free(committed);\n",
        "    tn_free(audit);tn_free(committed);tn_free(esc);\n", 1, "escrow-free")
    return src

def build_cell(cell, rt_mode, stated, teach, prefix, forger):
    dst = BAT / cell
    dst.mkdir(parents=True, exist_ok=True)
    ls, ss = sha(SRC / "gl_learner.zag"), sha(SRC / "gl_substrate.zag")
    assert ls == BASE_LEARNER_SHA, f"learner base SHA mismatch: {ls}"
    assert ss == BASE_SUBSTRATE_SHA, f"substrate base SHA mismatch: {ss}"
    shutil.copy(SRC / "gl_learner.zag", dst / "gl_learner.zag")
    shutil.copy(SRC / "gl_substrate.zag", dst / "gl_substrate.zag")
    # World-schedule parameter: RT_MODE const in the per-cell substrate COPY.
    # Substrate LOGIC untouched (SHA verified pristine above); only the const
    # is set, exactly as the battery's world cells require (W1 needs RT_MODE=0).
    sub = (dst / "gl_substrate.zag").read_text()
    assert sub.count("const RT_MODE:i32=3;") == 1
    sub = sub.replace("const RT_MODE:i32=3;", f"const RT_MODE:i32={rt_mode};")
    (dst / "gl_substrate.zag").write_text(sub)
    inc = (HERE / "escrow.zag.inc").read_text()
    src = (dst / "gl_learner.zag").read_text()
    src = apply_escrow_patch(src, inc)
    # Cell arm + traceability label.
    old_main = '    f=f+arm_gl(2,1,"rtb_");\n'
    assert src.count(old_main) == 1
    src = src.replace(old_main, f'    f=f+arm_gl({stated},{teach},"{prefix}");\n')
    assert src.count('_zag_print("default_B");') == 1
    src = src.replace('_zag_print("default_B");', f'_zag_print("h2_{cell}");')
    # Forger patch (world-signal or ledger manipulation; never escrow logic).
    if forger in FORGERS:
        name, old, new = FORGERS[forger]
        assert src.count(old) == 1, f"forger anchor {name} missing"
        src = src.replace(old, new)
        print(f"  ok: forger-{name}")
    elif forger and forger.startswith("ledger"):
        ep = int(forger[len("ledger"):])
        anchor = (
            "        if(rc==TN_OK){\n"
            "            let erc:i32=esc_eval(audit,&acount,esc,ep,provisional,committed,&provisional,&permanent,&revoke_step);\n"
            "            if(erc!=TN_OK){rc=erc;}\n"
            "        }\n")
        assert src.count(anchor) == 1, "forger ledger anchor missing"
        src = src.replace(anchor, forged_ledger(ep) + anchor)
        print(f"  ok: forger-ledger@{ep}")
    elif forger:
        raise AssertionError(f"unknown forger {forger}")
    (dst / "gl_learner.zag").write_text(src)
    print(f"built cell {cell}: {len(src)} bytes learner")

def build_controls():
    # ctl_h: unpatched default_B, honest arm (K2 control).
    d = CTL / "ctl_h"
    d.mkdir(parents=True, exist_ok=True)
    assert sha(SRC / "gl_learner.zag") == BASE_LEARNER_SHA
    assert sha(SRC / "gl_substrate.zag") == BASE_SUBSTRATE_SHA
    shutil.copy(SRC / "gl_learner.zag", d / "gl_learner.zag")
    shutil.copy(SRC / "gl_substrate.zag", d / "gl_substrate.zag")
    src = (d / "gl_learner.zag").read_text()
    old_main = '    f=f+arm_gl(2,1,"rtb_");\n'
    assert src.count(old_main) == 1
    src = src.replace(old_main, '    f=f+arm_gl(1,0,"w2h_");\n')
    (d / "gl_learner.zag").write_text(src)
    print("built control ctl_h")
    # fid: unpatched default_FID as-is (RT_MODE=0, both arms).
    d = CTL / "fid"
    d.mkdir(parents=True, exist_ok=True)
    assert sha(FID_SRC / "gl_learner.zag") == FID_LEARNER_SHA
    assert sha(FID_SRC / "gl_substrate.zag") == FID_SUBSTRATE_SHA
    shutil.copy(FID_SRC / "gl_learner.zag", d / "gl_learner.zag")
    shutil.copy(FID_SRC / "gl_substrate.zag", d / "gl_substrate.zag")
    print("built control fid")

if __name__ == "__main__":
    for cell, params in CELLS.items():
        print(f"cell {cell}:")
        build_cell(cell, *params)
    build_controls()
    print("all cells patched")
