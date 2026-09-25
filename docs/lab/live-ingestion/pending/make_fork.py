#!/usr/bin/env python3
"""Build instrument_kbp.zag: frozen fork base + pending library + command layer,
with the hold-intercept surgical edits. All edits are explicit string replaces;
any failed match aborts loudly (no silent drift)."""
import sys

BASE = "/home/hatch/workspace/tnn-lab/knowledge/web_guides/live_ingest/knowledge/sources/instrument_kb.zag"
LIB  = "/home/hatch/workspace/li_pending/impl/pending_track.zag"
CMDS = "/home/hatch/workspace/li_pending/impl/pending_cmds.zag"
OUT  = "/home/hatch/workspace/li_pending/impl/instrument_kbp.zag"

def rep_once(src, old, new, tag):
    n = src.count(old)
    if n != 1:
        print(f"FATAL: {tag}: expected 1 occurrence, found {n}", file=sys.stderr)
        sys.exit(1)
    return src.replace(old, new, 1)

base = open(BASE).read()
lib = open(LIB).read()
cmds = open(CMDS).read()

# --- Edit 1: verdict_core signature gains hold_on ---
base = rep_once(base,
    "o_provs:*i32,o_claims:*i32,o_fl:[]u8,o_fln:*i32)i32 {",
    "o_provs:*i32,o_claims:*i32,o_fl:[]u8,o_fln:*i32,hold_on:i32)i32 {",
    "verdict_core signature")

# --- Edit 2: multihop UNKNOWN-path hold intercept ---
# Inside the success block (n1/n2 in scope): stage the winning side's first
# page index and set rc=7 instead of 1. The outer return then yields 7 and
# the normal frees run. Under hold, the loud ANSWER| print above is skipped
# via the hold_on gate on the print block.
old_multi = """                o_claims[0]=2;
                rc=1;
            }else{
                if(loud==1){_zag_println("ANSWER|UNCHECKABLE");}
                rc=0;
            }"""
new_multi = """                o_claims[0]=2;
                if(hold_on==1){
                    let hpg:i32=0;
                    if(n2>n1){
                        if(w2n>0){hpg=g32(w2idx,0);}
                    }else{
                        if(w1n>0){hpg=g32(w1idx,0);}
                    }
                    p32(o_widx,0,hpg);
                    o_wn[0]=1;
                    rc=7;
                }else{
                    rc=1;
                }
            }else{
                if(loud==1){_zag_println("ANSWER|UNCHECKABLE");}
                rc=0;
            }"""
base = rep_once(base, old_multi, new_multi, "multihop hold intercept")

# --- Edit 2b: suppress the multihop factual ANSWER| print under hold ---
# (The hold intercept must not print the factual answer first.)
old_mh_print = """                if(loud==1){
                    _zag_print("ANSWER|");
                    _zag_println(win);"""
new_mh_print = """                if(loud==1 && hold_on==0){
                    _zag_print("ANSWER|");
                    _zag_println(win);"""
base = rep_once(base, old_mh_print, new_mh_print, "multihop print suppression")

# --- Edit 3: blind UNKNOWN-path hold intercept (o_ans/o_widx already staged, return 7) ---
old_blind = """        nio_free(bs);
        nio_free(qlow);
        nio_free(qt);
        nio_free(incl);
        return 1;
    }
    let widx:[]u8=nio_alloc(64*4);"""
new_blind = """        if(hold_on==1){
            nio_free(bs);
            nio_free(qlow);
            nio_free(qt);
            nio_free(incl);
            return 7;
        }
        nio_free(bs);
        nio_free(qlow);
        nio_free(qt);
        nio_free(incl);
        return 1;
    }
    let widx:[]u8=nio_alloc(64*4);"""
base = rep_once(base, old_blind, new_blind, "blind hold intercept")

# --- Edit 3b: suppress the blind factual ANSWER| print under hold ---
old_blind_print = """        if(loud==1){
            _zag_print("ANSWER|");
            _zag_println(bs);"""
new_blind_print = """        if(loud==1 && hold_on==0){
            _zag_print("ANSWER|");
            _zag_println(bs);"""
base = rep_once(base, old_blind_print, new_blind_print, "blind print suppression")

# --- Edit 4: G4 UNKNOWN-path hold intercept (rc2=7; o_ans/o_widx staged) ---
old_g4 = """        o_claims[0]=1;
        rc2=1;
    }else{"""
new_g4 = """        o_claims[0]=1;
        if(hold_on==1){rc2=7;}else{rc2=1;}
    }else{"""
base = rep_once(base, old_g4, new_g4, "G4 hold intercept")

# --- Edit 4b: suppress the G4 factual ANSWER| print under hold ---
old_g4_print = """        if(loud==1){
            _zag_print("ANSWER|");
            _zag_println(key);"""
new_g4_print = """        if(loud==1 && hold_on==0){
            _zag_print("ANSWER|");
            _zag_println(key);"""
base = rep_once(base, old_g4_print, new_g4_print, "G4 print suppression")

# --- Edit 5: calibration call sites keep hold_on=0 (frozen evidence preserved) ---
# The three calibration calls are textually identical; replace all, then fix
# cmd_verdict's separately by function context.
cal_old = "o_fl,&o_fln);"
n_cal = base.count(cal_old)
print(f"info: found {n_cal} verdict_core call sites", file=sys.stderr)
base = base.replace(cal_old, "o_fl,&o_fln,0);")

# --- Edit 6: cmd_verdict gains hold_on, captures vrc, runs phase B ---
base = rep_once(base,
    "fn cmd_verdict(sd:[]u8,nfp:[]u8,ppath:[]u8,kind:[]u8,query:[]u8,extra:[]u8)i32 {",
    "fn cmd_verdict(sd:[]u8,nfp:[]u8,ppath:[]u8,kind:[]u8,query:[]u8,extra:[]u8,hold_on:i32)i32 {",
    "cmd_verdict signature")

old_vcall = """    verdict_core(buf,np,pa,pt,tt,st,nst,ha,ht,query,kind,extra,kwstr,dt,dn,0,1,
        kba,kbt,kbn,
        o_ans,&o_ansn,o_widx,&o_wn,&o_provs,&o_claims,o_fl,&o_fln,0);"""
new_vcall = """    let vrc:i32=verdict_core(buf,np,pa,pt,tt,st,nst,ha,ht,query,kind,extra,kwstr,dt,dn,0,1,
        kba,kbt,kbn,
        o_ans,&o_ansn,o_widx,&o_wn,&o_provs,&o_claims,o_fl,&o_fln,hold_on);
    let hrc:i32=0;
    if(vrc==7){
        hrc=kpp_hold_from_verdict(sd,o_ans,o_ansn,o_widx,o_wn,ha,ht);
    }"""
base = rep_once(base, old_vcall, new_vcall, "cmd_verdict call + phase B")

old_vret = """    nio_free(kbt);
    nio_free(dt);
    return 0;
}

fn main()i32 {"""
new_vret = """    nio_free(kbt);
    nio_free(dt);
    if(vrc==7){return hrc;}
    return 0;
}

fn main()i32 {"""
base = rep_once(base, old_vret, new_vret, "cmd_verdict return")

# --- Edit 7: main dispatch ---
old_main_verdict = """    if(nio_equal(m,"verdict")==1){
        let sd4:[]u8=_zag_arg(2);
        let nfp:[]u8=_zag_arg(3);
        let pp:[]u8=_zag_arg(4);
        let kd:[]u8=_zag_arg(5);
        let qy:[]u8=_zag_arg(6);
        let ex2:[]u8=_zag_arg(7);
        if(sd4.len==0 || pp.len==0 || kd.len==0 || qy.len==0){return 2;}
        return cmd_verdict(sd4,nfp,pp,kd,qy,ex2);
    }
    return 2;
}"""
new_main = """    if(nio_equal(m,"verdict")==1){
        let sd4:[]u8=_zag_arg(2);
        let nfp:[]u8=_zag_arg(3);
        let pp:[]u8=_zag_arg(4);
        let kd:[]u8=_zag_arg(5);
        let qy:[]u8=_zag_arg(6);
        let ex2:[]u8=_zag_arg(7);
        if(sd4.len==0 || pp.len==0 || kd.len==0 || qy.len==0){return 2;}
        let ho:i32=kpc_hold_on(sd4);
        return cmd_verdict(sd4,nfp,pp,kd,qy,ex2,ho);
    }
    if(nio_equal(m,"kbpend")==1){
        let psrc:[]u8=_zag_arg(2);
        let psd:[]u8=_zag_arg(3);
        if(psrc.len==0 || psd.len==0){return 2;}
        return cmd_kbpend(psrc,psd);
    }
    if(nio_equal(m,"kbhold")==1){
        let hoo:[]u8=_zag_arg(2);
        let hsd:[]u8=_zag_arg(3);
        if(hoo.len==0 || hsd.len==0){return 2;}
        return cmd_kbhold(hoo,hsd);
    }
    if(nio_equal(m,"kbpendlist")==1){
        let lsd:[]u8=_zag_arg(2);
        if(lsd.len==0){return 2;}
        return cmd_kbpendlist(lsd);
    }
    if(nio_equal(m,"kbcorroborate")==1){
        let csd:[]u8=_zag_arg(2);
        let csq:[]u8=_zag_arg(3);
        let cpf:[]u8=_zag_arg(4);
        if(csd.len==0 || csq.len==0 || cpf.len==0){return 2;}
        return cmd_kbcorroborate(csd,atoi(csq),cpf);
    }
    if(nio_equal(m,"kbtest")==1){
        let tsd:[]u8=_zag_arg(2);
        let tsq:[]u8=_zag_arg(3);
        let trs:[]u8=_zag_arg(4);
        let tpr:[]u8=_zag_arg(5);
        if(tsd.len==0 || tsq.len==0 || trs.len==0 || tpr.len==0){return 2;}
        return cmd_kbtest(tsd,atoi(tsq),trs,tpr);
    }
    if(nio_equal(m,"kbrefute")==1){
        let rsd:[]u8=_zag_arg(2);
        let rsq:[]u8=_zag_arg(3);
        let rpf:[]u8=_zag_arg(4);
        if(rsd.len==0 || rsq.len==0 || rpf.len==0){return 2;}
        return cmd_kbrefute(rsd,atoi(rsq),rpf);
    }
    return 2;
}"""
base = rep_once(base, old_main_verdict, new_main, "main dispatch")

# Header documenting the fork.
header = """// instrument_kbp.zag — frozen fork of instrument_kb.zag with the live-ingestion
// pending epistemic state (prereg docs/lab/knowledge/web_guides/live_ingest/
// pending/PREREG_PENDING.md). Composition:
//   (1) fork base: instrument_kb.zag (frozen SHA-256
//       d7ce44ffe8866f7fb5869250cfba40fcd8140e22eb79d4a23b773969dedede41)
//   (2) pending_track.zag — the kpp_ pending-store library
//   (3) pending_cmds.zag — kbpend/kbhold/kbpendlist/kbcorroborate/kbtest/kbrefute
//       + kpp_hold_from_verdict (hold intercept phase B)
// Hold integration (frozen §4b): verdict_core gains a trailing hold_on:i32
// parameter. The three calibration call sites pass 0 (frozen evidence byte-
// preserved). cmd_verdict takes hold_on from the state dir's holdpolicy.txt
// (default OFF), captures the verdict rc, and on rc==7 runs
// kpp_hold_from_verdict BEFORE freeing the staged answer/host buffers.
// Hold intercepts fire ONLY on successful UNKNOWN-path installs:
//   - multihop branch (return 7; stages the winning side's first page index)
//   - blind branch (return 7; o_ans/o_widx already staged)
//   - G4 branch (rc2=7; o_ans/o_widx already staged)
// All three suppress the would-be factual ANSWER| print under hold.
// Verdict/recall code paths perform ZERO reads of pending.txt: grep this file
// for "pending.txt" and confirm the only matches are inside kpp_/kpc_ command
// helpers (kbpend/kbhold/kbpendlist/kbcorroborate/kbtest/kbrefute), never in
// verdict_core, cmd_verdict's verdict path, or cmd_query/cmd_select.

"""
out = header + base + "\n// ===== pending_track.zag =====\n" + lib + "\n// ===== pending_cmds.zag =====\n" + cmds
open(OUT, "w").write(out)
print(f"wrote {OUT} ({len(out)} bytes)", file=sys.stderr)
