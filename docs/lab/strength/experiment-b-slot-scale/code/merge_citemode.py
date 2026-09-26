#!/usr/bin/env python3
"""Experiment B (slot scale): merge the F6 cite_mode switch into the
current-law strength core (base commit 5610c1215d7f, strength-recycle).

Input:  ~/workspace/strength-recycle/strength_core.zag
Output: ~/workspace/slot-scale/strength_core.zag

Every replacement is exact-match; aborts on any mismatch (fail loud).
Law invariant: cite_mode defaults to ST_CITE_WINDOWED, and the WINDOWED
path of st_cite_consumed is the base-commit body VERBATIM, so all prior
evidence is byte-identical under the default. The G/H branches port the
mode-dependent scan bounds (st_consume_lo/st_pay_lo/st_last_add_idx) from
strength-f6/strength_core.zag onto the current-law consuming op set
(KILL/KILL_EVIDENCED/OVERWRITE/DELETE_STRONG — hole-1/hole-2/F4b intact).
"""
import sys

SRC = "/home/hatch/workspace/strength-recycle/strength_core.zag"
DST = "/home/hatch/workspace/slot-scale/strength_core.zag"
src = open(SRC).read()

def rep(old, new, tag, count=1):
    global src
    n = src.count(old)
    assert n == count, f"MISMATCH [{tag}]: found {n}, expected {count}\n---old---\n{old[:500]}"
    src = src.replace(old, new)

# ---- 1. cite-mode constants after ST_REFUSED_CONSUMED ----
rep("const ST_REFUSED_CONSUMED:i32=121;",
    "const ST_REFUSED_CONSUMED:i32=121;\n"
    "\n"
    "// B-mode cite-consumption modes (2026-09-26, ported from F6\n"
    "// strength-f6/strength_core.zag): how far back a citation episode\n"
    "// stays \"consumed\" (single-use) after paying for an OK destruction.\n"
    "// WINDOWED (0): base-commit law — consumption resets on any strength-set\n"
    "//   (ADD/STRENGTHEN/WEAKEN/TRAINER_DECLARE/OVERWRITE). DEFAULT; all\n"
    "//   pre-B evidence is byte-identical under this mode.\n"
    "// GLOBAL (1): a cite_ep consumed by ANY earlier OK destruction on the\n"
    "//   slot can never pay again — no reset, ever.\n"
    "// HYBRID (2): consumption carries over overwrite/strengthen/weaken/\n"
    "//   trainer-declare; resets only on ADD. (Disqualified by Micah's\n"
    "//   2026-09-25 ruling; present for completeness, not used in B.)\n"
    "const ST_CITE_WINDOWED:i32=0;\n"
    "const ST_CITE_GLOBAL:i32=1;\n"
    "const ST_CITE_HYBRID:i32=2;",
    "cite-mode-consts")

# ---- 2. cite_mode field on StStore ----
rep("    ep: i32            // current episode (set by learner; unaudited)\n}",
    "    ep: i32,           // current episode (set by learner; unaudited)\n"
    "    cite_mode: i32     // B-mode: ST_CITE_WINDOWED/GLOBAL/HYBRID (see above)\n"
    "}",
    "cite-mode-field")

# ---- 3. init default + setter (after st_init's closing brace) ----
rep(".stage=ST_STAGE_NONE,.clock=0,.p3=0,.p3k=0,.ep=0};\n}\nfn st_free(s:*StStore)void {",
    ".stage=ST_STAGE_NONE,.clock=0,.p3=0,.p3k=0,.ep=0,.cite_mode=ST_CITE_WINDOWED};\n"
    "}\n"
    "// B-mode: set the cite-consumption mode (WINDOWED=0 law default,\n"
    "// GLOBAL=1, HYBRID=2). Must be set before any ops; the checker reads it\n"
    "// from the store, so mechanism and checker cannot disagree.\n"
    "fn st_set_cite_mode(s:*StStore,mode:i32)void {\n"
    "    if(mode==ST_CITE_GLOBAL || mode==ST_CITE_HYBRID){s.*.cite_mode=mode;}\n"
    "    else {s.*.cite_mode=ST_CITE_WINDOWED;}\n"
    "}\n"
    "fn st_free(s:*StStore)void {",
    "cite-mode-init")

# ---- 4. mode-dependent scan bounds before st_collect_cites ----
rep("fn st_collect_cites(s:*StStore,slot:i32,after_idx:i32,upto:i32,out:[]u8) i32 {",
    "// Index of the most recent OK ADD for slot before `upto`; -1 if none.\n"
    "// (B-mode global/hybrid: the ADD lineage bound — a genuinely new memory.)\n"
    "fn st_last_add_idx(s:*StStore,slot:i32,upto:i32)i32 {\n"
    "    let i:i32=upto-1;\n"
    "    while(i>=0){\n"
    "        if(st_aw(s,i,0)==ST_OP_ADD && st_aw(s,i,1)==slot && st_aw(s,i,4)==ST_OK){return i;}\n"
    "        i=i-1;\n"
    "    }\n"
    "    return -1;\n"
    "}\n"
    "// B-mode: lower bound of the consumption scan for a check ending at `upto`.\n"
    "// WINDOWED: the caller's after_idx (last strength-set — base-commit law).\n"
    "// GLOBAL: -1 (scan the whole ledger: no reset, ever).\n"
    "// HYBRID: last ADD (consumption carries over everything but a new memory).\n"
    "fn st_consume_lo(s:*StStore,slot:i32,upto:i32,after_idx:i32)i32 {\n"
    "    let mode:i32=s.*.cite_mode;\n"
    "    if(mode==ST_CITE_GLOBAL){return -1;}\n"
    "    if(mode==ST_CITE_HYBRID){return st_last_add_idx(s,slot,upto);}\n"
    "    return after_idx;\n"
    "}\n"
    "// B-mode: lower bound of a destruction's payment set (which cites it consumed).\n"
    "// WINDOWED: last strength-set before the destruction (base-commit law).\n"
    "// GLOBAL/HYBRID: last ADD before the destruction — a cite counts as paid\n"
    "// only if it was cited during the destroyed memory's own ADD lineage\n"
    "// (cites for long-dead memories are not burned by later destructions).\n"
    "fn st_pay_lo(s:*StStore,slot:i32,d:i32)i32 {\n"
    "    let mode:i32=s.*.cite_mode;\n"
    "    if(mode==ST_CITE_GLOBAL || mode==ST_CITE_HYBRID){return st_last_add_idx(s,slot,d);}\n"
    "    return st_last_strength_idx(s,slot,d);\n"
    "}\n"
    "fn st_collect_cites(s:*StStore,slot:i32,after_idx:i32,upto:i32,out:[]u8) i32 {",
    "scan-bounds")

# ---- 5. st_cite_consumed: G/H branch + WINDOWED verbatim ----
old_consumed = """fn st_cite_consumed(s:*StStore,slot:i32,cite_ep:i32,after_idx:i32,upto:i32)i32 {
    let d:i32=0;
    while(d<upto){
        let op:i32=st_aw(s,d,0);
        if((op==ST_OP_KILL || op==ST_OP_KILL_EVIDENCED || op==ST_OP_OVERWRITE ||
            op==ST_OP_DELETE_STRONG) &&
           st_aw(s,d,1)==slot && st_aw(s,d,4)==ST_OK){
            let dlss:i32=st_last_strength_idx(s,slot,d);
            let i:i32=dlss+1;
            while(i<d){
                if(st_aw(s,i,0)==ST_OP_EVIDENCE && st_aw(s,i,1)==slot &&
                   st_aw(s,i,4)==ST_OK && st_aw(s,i,2)==cite_ep){return 1;}
                i=i+1;
            }
        }
        d=d+1;
    }
    return 0;
}"""
new_consumed = """fn st_cite_consumed(s:*StStore,slot:i32,cite_ep:i32,after_idx:i32,upto:i32)i32 {
    let mode:i32=s.*.cite_mode;
    if(mode==ST_CITE_GLOBAL || mode==ST_CITE_HYBRID){
        // B-mode G/H branch (2026-09-26): mode-dependent scan bounds ported
        // from F6 (st_consume_lo/st_pay_lo), applied to the CURRENT-LAW
        // consuming op set (KILL/KILL_EVIDENCED/OVERWRITE/DELETE_STRONG —
        // hole-1/hole-2/F4b fixes intact). The WINDOWED branch below is the
        // base-commit body VERBATIM.
        let lo:i32=st_consume_lo(s,slot,upto,after_idx);
        let d:i32=lo+1;
        while(d<upto){
            let op:i32=st_aw(s,d,0);
            if((op==ST_OP_KILL || op==ST_OP_KILL_EVIDENCED || op==ST_OP_OVERWRITE ||
                op==ST_OP_DELETE_STRONG) &&
               st_aw(s,d,1)==slot && st_aw(s,d,4)==ST_OK){
                let plo:i32=st_pay_lo(s,slot,d);
                let i:i32=plo+1;
                while(i<d){
                    if(st_aw(s,i,0)==ST_OP_EVIDENCE && st_aw(s,i,1)==slot &&
                       st_aw(s,i,4)==ST_OK && st_aw(s,i,2)==cite_ep){return 1;}
                    i=i+1;
                }
            }
            d=d+1;
        }
        return 0;
    }
    // WINDOWED: base-commit law VERBATIM (byte-identical behavior to the
    // unmerged core under the default mode).
    let d:i32=0;
    while(d<upto){
        let op:i32=st_aw(s,d,0);
        if((op==ST_OP_KILL || op==ST_OP_KILL_EVIDENCED || op==ST_OP_OVERWRITE ||
            op==ST_OP_DELETE_STRONG) &&
           st_aw(s,d,1)==slot && st_aw(s,d,4)==ST_OK){
            let dlss:i32=st_last_strength_idx(s,slot,d);
            let i:i32=dlss+1;
            while(i<d){
                if(st_aw(s,i,0)==ST_OP_EVIDENCE && st_aw(s,i,1)==slot &&
                   st_aw(s,i,4)==ST_OK && st_aw(s,i,2)==cite_ep){return 1;}
                i=i+1;
            }
        }
        d=d+1;
    }
    return 0;
}"""
rep(old_consumed, new_consumed, "cite-consumed-modes")

open(DST, "w").write(src)
print(f"merged OK -> {DST} ({len(src)} bytes)")
