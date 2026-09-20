#!/usr/bin/env python3
"""Apply print-only chain instrumentation to a pristine copy of the INT-1
C5-redesign trial sources (wave9/integration/impl).

Print-only: every insertion is a _zag_print of a CHAIN_*/CAPCOMP line placed
adjacent to the exact ledger-append call sites. No computation is altered.
One provably-neutral let-hoist at the proactive-open site (loop.zag) so the
open rc is printable.

Two pipelines:
  instrument(src)          -> src with instrumentation, gate INTACT
  instrument_gateless(src) -> src with instrumentation, default verdict gate
                              EXCISED (calibration variant only; the arm-filter
                              gate stays, exactly as in the committed
                              calibration procedure).

Usage: python3 instrument.py <src0_dir> <out_inst_dir> <out_gateless_dir>
"""
import os, shutil, sys

def read(d, f):
    with open(os.path.join(d, f)) as fh:
        return fh.read()

def write(d, f, s):
    with open(os.path.join(d, f), "w") as fh:
        fh.write(s)

HELPER = '''
// EXP-1 verification instrumentation (print-only, 2026-09-20): numeric print
// helper for CHAIN_/CAPCOMP lines. Behavior-neutral.
fn chain_num(x:i64)void { let s:[]u8=_zag_i64_to_str(x);_zag_print(s);nio_free(s); }
'''

def add_helper(src):
    anchor = "const SEAM_REFUSED_PARTITION:i32=311;  // C5: backing verdict not in arm"
    assert src.count(anchor) == 1, "helper anchor not unique"
    return src.replace(anchor, anchor + HELPER, 1)

# --- refusal sites (both emit SEAM_REFUSED_PARTITION ledger entries) ---
ARM_REFUSAL_OLD = """            lg_append(l,LG_O4,LG_OP_COMPOSE,-1,SEAM_REFUSED_PARTITION,need_id as i64,cfg.*.c5_arm as i64,0,0,0,claim_cid,0,0,0,0,cfg.*.stage,0,ep as i64);
            return SEAM_REFUSED_PARTITION;"""
ARM_REFUSAL_NEW = """            lg_append(l,LG_O4,LG_OP_COMPOSE,-1,SEAM_REFUSED_PARTITION,need_id as i64,cfg.*.c5_arm as i64,0,0,0,claim_cid,0,0,0,0,cfg.*.stage,0,ep as i64);
            _zag_print("CHAIN_REFUSAL,");chain_num(ep as i64);_zag_print(",");chain_num(need_id as i64);_zag_print(",");chain_num(claim_cid);_zag_print(",");chain_num(cfg.*.c5_arm as i64);_zag_print(",311\\n");
            return SEAM_REFUSED_PARTITION;"""

GATE_REFUSAL_OLD = """            lg_append(l,LG_O4,LG_OP_COMPOSE,-1,SEAM_REFUSED_PARTITION,need_id as i64,0,0,0,0,claim_cid,0,0,0,0,cfg.*.stage,0,ep as i64);
            return SEAM_REFUSED_PARTITION;"""
GATE_REFUSAL_NEW = """            lg_append(l,LG_O4,LG_OP_COMPOSE,-1,SEAM_REFUSED_PARTITION,need_id as i64,0,0,0,0,claim_cid,0,0,0,0,cfg.*.stage,0,ep as i64);
            _zag_print("CHAIN_REFUSAL,");chain_num(ep as i64);_zag_print(",");chain_num(need_id as i64);_zag_print(",");chain_num(claim_cid);_zag_print(",0,311\\n");
            return SEAM_REFUSED_PARTITION;"""

# --- default gate excision (calibration variant only) ---
GATE_BLOCK_OLD = """    let cid2:i32=claim_cid as i32;
    if(cid2>0){
        let v2:i32=-1;
        if(o2_verdict(o2,cid2,&v2)==0 && v2==O2_V_REFUTED){
            trace.*=-1;
            lg_append(l,LG_O4,LG_OP_COMPOSE,-1,SEAM_REFUSED_PARTITION,need_id as i64,0,0,0,0,claim_cid,0,0,0,0,cfg.*.stage,0,ep as i64);
            return SEAM_REFUSED_PARTITION;
        }
    }"""
GATE_BLOCK_NEW = """    // CALIBRATION VARIANT (EXP-1, 2026-09-20): the default verdict gate is
    // excised here; the arm-filter gate above is untouched. Everything else
    // is byte-identical to the instrumented intact sources."""

# --- non-partition refusal sites (adversarial audit: must never chain to L1) ---
AGENCY_REFUSAL_OLD = """        lg_append(l,LG_O4,LG_OP_COMPOSE,-1,SEAM_REFUSED_AGENCY,0,0,0,0,0,0,0,0,0,0,cfg.*.stage,0,ep as i64);
        return SEAM_REFUSED_AGENCY;"""
AGENCY_REFUSAL_NEW = """        lg_append(l,LG_O4,LG_OP_COMPOSE,-1,SEAM_REFUSED_AGENCY,0,0,0,0,0,0,0,0,0,0,cfg.*.stage,0,ep as i64);
        _zag_print("CHAIN_REFUSAL,");chain_num(ep as i64);_zag_print(",0,0,0,304\\n");
        return SEAM_REFUSED_AGENCY;"""

TEACHER_REFUSAL_OLD = """        lg_append(l,LG_O4,LG_OP_COMPOSE,-1,SEAM_REFUSED_TEACHER,0,0,0,0,0,claim_cid,0,0,0,0,cfg.*.stage,0,ep as i64);
        return SEAM_REFUSED_TEACHER;"""
TEACHER_REFUSAL_NEW = """        lg_append(l,LG_O4,LG_OP_COMPOSE,-1,SEAM_REFUSED_TEACHER,0,0,0,0,0,claim_cid,0,0,0,0,cfg.*.stage,0,ep as i64);
        _zag_print("CHAIN_REFUSAL,");chain_num(ep as i64);_zag_print(",0,");chain_num(claim_cid);_zag_print(",0,312\\n");
        return SEAM_REFUSED_TEACHER;"""

# --- abstain site ---
ABSTAIN_OLD = """    if(rc==0){
        tr.*.l1_abstains=tr.*.l1_abstains+1;
        let orc:i32=seam2_open(l,o2,cid,slot,ep);
        if(orc==0){tr.*.l1_opened=tr.*.l1_opened+1;}
    }"""
ABSTAIN_NEW = """    if(rc==0){
        tr.*.l1_abstains=tr.*.l1_abstains+1;
        let orc:i32=seam2_open(l,o2,cid,slot,ep);
        if(orc==0){tr.*.l1_opened=tr.*.l1_opened+1;}
        _zag_print("CHAIN_ABSTAIN,");chain_num(ep as i64);_zag_print(",");chain_num(need_id as i64);_zag_print(",");chain_num(cid as i64);_zag_print(",");chain_num(rc as i64);_zag_print(",");chain_num(orc as i64);_zag_print("\\n");
    }"""

# --- hypothesis-open site (all opens: proactive + abstain-driven) ---
HYPOPEN_OLD = """    lg_append(l,LG_O2,LG_OP_HYP_OPEN,cid,rc,slot as i64,0,0,0,0,0,0,0,0,0,0,fl,ep as i64);
    return rc;"""
HYPOPEN_NEW = """    lg_append(l,LG_O2,LG_OP_HYP_OPEN,cid,rc,slot as i64,0,0,0,0,0,0,0,0,0,0,fl,ep as i64);
    _zag_print("CHAIN_HYPOPEN,");chain_num(ep as i64);_zag_print(",");chain_num(cid as i64);_zag_print(",");chain_num(rc as i64);_zag_print("\\n");
    return rc;"""

# --- proactive-open site (loop.zag section 2) ---
PROACTIVE_OLD = """            ls.*.next_cid=ls.*.next_cid+1;
            loop_claim_open(ls,cid,ls.*.anchor1,ep);"""
PROACTIVE_NEW = """            ls.*.next_cid=ls.*.next_cid+1;
            let prc:i32=loop_claim_open(ls,cid,ls.*.anchor1,ep);
            _zag_print("CHAIN_PROACTIVE,");chain_num(ep as i64);_zag_print(",");chain_num(cid as i64);_zag_print(",");chain_num(prc as i64);_zag_print("\\n");"""

# --- per-stage component telemetry (main.zag mn_stage) ---
CAPCOMP_OLD = """    _zag_print("COMPOSITES,");mn_num(ls.met.composites);
    _zag_print(",ok,");mn_num(ls.met.composites_ok);_zag_println("");"""
CAPCOMP_NEW = CAPCOMP_OLD + """
    _zag_print("CAPCOMP,");mn_num(sn as i64);
    _zag_print(",");mn_num(ls.met.composites_ok);
    _zag_print(",");mn_num(ls.met.commits_constr);
    _zag_print(",");mn_num(ls.met.hypotheses);
    _zag_print(",");mn_num(ls.tr.l1_abstains);
    _zag_print(",");mn_num(ls.tr.l1_opened);_zag_println("");"""

# --- C7 arm markers (controls.zag c7_run): segment CHAIN lines by arm ---
# c7_run executes intact-DC4, intact-DC5, dep-DC4, dep-DC5 sequentially as
# separate LoopStates whose episode numbers overlap; without markers the
# (ep,need) chain keys could collide across arms. Print-only.
C7ARM_OLD = [
    ("    let a:LoopState=loop_init(scale);\n    loop_run_stage(&a,CU_DC4,scale);",
     "    let a:LoopState=loop_init(scale);\n    _zag_print(\"C7ARM,intact4\\n\");\n    loop_run_stage(&a,CU_DC4,scale);"),
    ("    let b:LoopState=loop_init(scale);\n    let rc5:i32=loop_run_stage(&b,CU_DC5,scale);",
     "    let b:LoopState=loop_init(scale);\n    _zag_print(\"C7ARM,intact5\\n\");\n    let rc5:i32=loop_run_stage(&b,CU_DC5,scale);"),
    ("    let a2:LoopState=loop_init(scale);\n    a2.cfg.c7_teacher_dep=1;\n    loop_run_stage(&a2,CU_DC4,scale);",
     "    let a2:LoopState=loop_init(scale);\n    a2.cfg.c7_teacher_dep=1;\n    _zag_print(\"C7ARM,dep4\\n\");\n    loop_run_stage(&a2,CU_DC4,scale);"),
    ("    let b2:LoopState=loop_init(scale);\n    b2.cfg.c7_teacher_dep=1;\n    loop_run_stage(&b2,CU_DC5,scale);",
     "    let b2:LoopState=loop_init(scale);\n    b2.cfg.c7_teacher_dep=1;\n    _zag_print(\"C7ARM,dep5\\n\");\n    loop_run_stage(&b2,CU_DC5,scale);"),
]

# --- C7 arm component telemetry (controls.zag c7_run) ---
C7CAP_OLD = """    _zag_print("C7_POSCTRL,cap4d,");c7_num(cap4d);
    _zag_print(",cap5d,");c7_num(cap5d);_zag_print("\\n");"""
C7CAP_NEW = C7CAP_OLD + """
    _zag_print("C7CAP,intact4,");c7_num(a.met.composites_ok);
    _zag_print(",");c7_num(a.met.commits_constr);
    _zag_print(",");c7_num(a.met.hypotheses);
    _zag_print(",");c7_num(a.tr.l1_abstains);
    _zag_print(",");c7_num(a.tr.l1_opened);_zag_print("\\n");
    _zag_print("C7CAP,intact5,");c7_num(b.met.composites_ok);
    _zag_print(",");c7_num(b.met.commits_constr);
    _zag_print(",");c7_num(b.met.hypotheses);
    _zag_print(",");c7_num(b.tr.l1_abstains);
    _zag_print(",");c7_num(b.tr.l1_opened);_zag_print("\\n");
    _zag_print("C7CAP,dep4,");c7_num(a2.met.composites_ok);
    _zag_print(",");c7_num(a2.met.commits_constr);
    _zag_print(",");c7_num(a2.met.hypotheses);
    _zag_print(",");c7_num(a2.tr.l1_abstains);
    _zag_print(",");c7_num(a2.tr.l1_opened);_zag_print("\\n");
    _zag_print("C7CAP,dep5,");c7_num(b2.met.composites_ok);
    _zag_print(",");c7_num(b2.met.commits_constr);
    _zag_print(",");c7_num(b2.met.hypotheses);
    _zag_print(",");c7_num(b2.tr.l1_abstains);
    _zag_print(",");c7_num(b2.tr.l1_opened);_zag_print("\\n");"""

def patch(text, old, new, expect=1, name=""):
    n = text.count(old)
    assert n == expect, f"{name}: expected {expect} occurrence(s), found {n}"
    return text.replace(old, new, 1)

def instrument(srcdir, gateless):
    d = {}
    for f in ["seam.zag", "loop.zag", "main.zag", "controls.zag"]:
        d[f] = read(srcdir, f)

    seam = d["seam.zag"]
    seam = add_helper(seam)
    seam = patch(seam, ARM_REFUSAL_OLD, ARM_REFUSAL_NEW, name="arm_refusal")
    if gateless:
        seam = patch(seam, GATE_BLOCK_OLD, GATE_BLOCK_NEW, name="gate_excise")
        assert "CHAIN_REFUSAL" in seam  # arm site still instrumented
        assert seam.count("lg_append(l,LG_O4,LG_OP_COMPOSE,-1,SEAM_REFUSED_PARTITION,need_id as i64,0,0,0,0,claim_cid") == 0, \
            "default-gate refusal ledger site must be gone in gateless variant"
    else:
        seam = patch(seam, GATE_REFUSAL_OLD, GATE_REFUSAL_NEW, name="gate_refusal")
    seam = patch(seam, AGENCY_REFUSAL_OLD, AGENCY_REFUSAL_NEW, name="agency_refusal")
    seam = patch(seam, TEACHER_REFUSAL_OLD, TEACHER_REFUSAL_NEW, name="teacher_refusal")
    seam = patch(seam, ABSTAIN_OLD, ABSTAIN_NEW, name="abstain")
    seam = patch(seam, HYPOPEN_OLD, HYPOPEN_NEW, name="hypopen")
    d["seam.zag"] = seam

    loop = d["loop.zag"]
    loop = patch(loop, PROACTIVE_OLD, PROACTIVE_NEW, name="proactive")
    d["loop.zag"] = loop

    main = d["main.zag"]
    main = patch(main, CAPCOMP_OLD, CAPCOMP_NEW, name="capcomp")
    d["main.zag"] = main

    ctl = d["controls.zag"]
    ctl = patch(ctl, C7CAP_OLD, C7CAP_NEW, name="c7cap")
    for old, new in C7ARM_OLD:
        ctl = patch(ctl, old, new, name="c7arm")
    d["controls.zag"] = ctl
    return d

def main():
    src0, out_inst, out_gate = sys.argv[1], sys.argv[2], sys.argv[3]
    for out, gateless in ((out_inst, False), (out_gate, True)):
        if os.path.exists(out):
            shutil.rmtree(out)
        shutil.copytree(src0, out)
        patched = instrument(src0, gateless)
        for f, text in patched.items():
            write(out, f, text)
        print(f"wrote {'gateless' if gateless else 'intact'} instrumented tree -> {out}")

if __name__ == "__main__":
    main()
