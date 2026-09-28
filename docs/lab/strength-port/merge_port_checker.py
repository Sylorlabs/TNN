#!/usr/bin/env python3
# merge_port_checker.py — deterministic port of the F6 wedge-fix checker
# additions into the delete-strong mainline checker.
# Base: ~/workspace/strength-delete/strength_checker.zag
# Donor: ~/workspace/strength-f6-wedgefix/strength_checker.zag
import sys

BASE = "/home/hatch/workspace/strength-delete/strength_checker.zag"
OUT = "/home/hatch/workspace/strength-port/strength_checker.zag"

def need(hay, needle, tag):
    if hay.count(needle) != 1:
        print(f"ANCHOR FAIL [{tag}]: count={hay.count(needle)}")
        sys.exit(1)

src = open(BASE).read()
assert "ST_OP_CITELOCK" not in src, "base already has citelock?!"

# ---- C1: checker fns for the cite-lock signals, before ck_strength_lineage ----
# PORT NOTE: these are VERBATIM the F6 workstream's proven checker functions
# (strength_checker.zag lines 176-235), NOT the simplified sketch in
# F6_VERDICT.md (which used wrong word indices and checks the real code
# never had). The only port change is the priced-set extension in the tie
# (KILL and DELETE_STRONG join KILL_EVIDENCED and OVERWRITE).
a = "fn ck_strength_lineage(s:*StStore)i32 {"
need(src, a, "C1")
src = src.replace(a, """// ---- PORT (2026-09-26, F6 wedge-fix): cite-lock signal checks ----
// (verbatim F6 workstream source; see note above)
fn ck_verify_citelock(s:*StStore,slot:i32,i:i32)i32 {
    let f:i32=0;
    let tied:i32=0;
    if(i>0){
        let pop:i32=st_aw(s,i-1,0);let prc:i32=st_aw(s,i-1,4);let psl:i32=st_aw(s,i-1,1);
        if(psl==slot && prc==ST_REFUSED_CONSUMED &&
           (pop==ST_OP_KILL_EVIDENCED || pop==ST_OP_OVERWRITE ||
            pop==ST_OP_KILL || pop==ST_OP_DELETE_STRONG)){tied=1;}
    }
    f=f+cl_check("ck_sig_tie",tied,1);
    let beq:i32=1;let w:i32=0;
    while(w<6){if(st_aw(s,i,5+w)!=st_aw(s,i,11+w)){beq=0;break;}w=w+1;}
    f=f+cl_check("ck_sig_nochange",beq,1);
    let lss:i32=st_last_strength_idx(s,slot,i);
    let has_lss:i32=0;if(lss>=0){has_lss=1;}
    f=f+cl_check("ck_sig_lss",has_lss,1);
    let locked:i32=0;
    if(lss>=0){
        let sbuf:[]u8=nio_alloc(16);
        let stot:i32=st_collect_cites(s,slot,lss,i,sbuf);
        nio_free(sbuf);
        let sspent:i32=st_count_spent_cites(s,slot,lss,i);
        if(stot>=1 && sspent==stot){locked=1;}
    }
    f=f+cl_check("ck_sig_locked",locked,1);
    return f;
}
// A system-level signal is legitimate iff it is addressed to the store
// (slot -1), immediately follows an OK slot-level signal, and is
// audit-only.
fn ck_verify_citelock_sys(s:*StStore,slot:i32,i:i32)i32 {
    let f:i32=0;
    f=f+cl_check("ck_syssig_slot",slot,-1);
    let tied:i32=0;
    if(i>0 && st_aw(s,i-1,0)==ST_OP_CITELOCK && st_aw(s,i-1,4)==ST_OK){tied=1;}
    f=f+cl_check("ck_syssig_tie",tied,1);
    let beq:i32=1;let w:i32=0;
    while(w<6){if(st_aw(s,i,5+w)!=st_aw(s,i,11+w)){beq=0;break;}w=w+1;}
    f=f+cl_check("ck_syssig_nochange",beq,1);
    return f;
}
// Every G-mode 121 refusal of a priced destruction on a cite-locked slot
// must be followed by that slot's CITELOCK signal (the diagnosis is not
// droppable).
fn ck_require_citelock(s:*StStore,slot:i32,i:i32)i32 {
    let f:i32=0;
    let lss:i32=st_last_strength_idx(s,slot,i);
    let locked:i32=0;
    if(lss>=0){
        let gbuf:[]u8=nio_alloc(16);
        let gtot:i32=st_collect_cites(s,slot,lss,i,gbuf);
        nio_free(gbuf);
        let gspent:i32=st_count_spent_cites(s,slot,lss,i);
        if(gtot>=1 && gspent==gtot){locked=1;}
    }
    let present:i32=0;
    if(locked==0){present=1;}
    else if(i+1<s.*.audit_n && st_aw(s,i+1,0)==ST_OP_CITELOCK &&
            st_aw(s,i+1,1)==slot && st_aw(s,i+1,4)==ST_OK){present=1;}
    f=f+cl_check("ck_sig_present",present,1);
    return f;
}
fn ck_strength_lineage(s:*StStore)i32 {""", 1)

# ---- C2: dispatch signal checks inside ck_verify ----
a = """            if((op==ST_OP_JUSTIFY || op==ST_OP_EVIDENCE || op==ST_OP_STRENGTHEN || op==ST_OP_WEAKEN) &&
               (aux2<ST_J_CONFIRMED_IMPORTANT || aux2>ST_J_TRAINER_DIRECTIVE)){bad_code=1;}
"""
need(src, a, "C2")
src = src.replace(a, a + """            // PORT (2026-09-26, F6 wedge-fix): cite-lock signals are
            // audit-only and causally tied.
            if(op==ST_OP_CITELOCK && sl>=0){f=f+ck_verify_citelock(s,sl,i);}
            if(op==ST_OP_CITELOCK_SYS){f=f+ck_verify_citelock_sys(s,sl,i);}
""", 1)

# ---- C3: require the signal after genuine GLOBAL 121s ----
# NOTE: C2 already inserted the signal-dispatch lines after the bad_code line;
# anchor on them.
a = """            // PORT (2026-09-26, F6 wedge-fix): cite-lock signals are
            // audit-only and causally tied.
            if(op==ST_OP_CITELOCK && sl>=0){f=f+ck_verify_citelock(s,sl,i);}
            if(op==ST_OP_CITELOCK_SYS){f=f+ck_verify_citelock_sys(s,sl,i);}
        }
        i=i+1;
    }
"""
need(src, a, "C3")
src = src.replace(a, """            // PORT (2026-09-26, F6 wedge-fix): cite-lock signals are
            // audit-only and causally tied.
            if(op==ST_OP_CITELOCK && sl>=0){f=f+ck_verify_citelock(s,sl,i);}
            if(op==ST_OP_CITELOCK_SYS){f=f+ck_verify_citelock_sys(s,sl,i);}
        }
        // PORT (2026-09-26, F6 wedge-fix): every GLOBAL-mode 121 refusal of
        // a priced destruction on a cite-locked slot must carry its signal.
        // (Extended vs the F6 workstream: the mainline priced set includes
        // KILL and DELETE_STRONG alongside KILL_EVIDENCED and OVERWRITE.)
        if(s.*.cite_mode==ST_CITE_GLOBAL && rc==ST_REFUSED_CONSUMED &&
           (op==ST_OP_KILL_EVIDENCED || op==ST_OP_OVERWRITE ||
            op==ST_OP_KILL || op==ST_OP_DELETE_STRONG) && sl>=0){
            f=f+ck_require_citelock(s,sl,i);
        }
        i=i+1;
    }
""", 1)

open(OUT, "w").write(src)
print("checker port OK ->", OUT)
