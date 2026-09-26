#!/usr/bin/env python3
"""Merge F4b hunks + ST_OP_DELETE_STRONG into the F1-forkA base core.

Inputs:  ~/workspace/strength-delete/strength_core.zag (F1-forkA base)
Outputs: merged file in place. Every replacement is exact-match; aborts on
any mismatch (fail loud).
"""
import sys

W = "/home/hatch/workspace/strength-delete/"
P = W + "strength_core.zag"
src = open(P).read()

def rep(old, new, tag, count=1):
    global src
    n = src.count(old)
    assert n == count, f"MISMATCH [{tag}]: found {n}, expected {count}\n---old---\n{old[:400]}"
    src = src.replace(old, new)

# ---- 3a. ST_REFUSED_CONSUMED = 121 after ST_REFUSED_BADOP = 120 ----
rep("const ST_REFUSED_BADOP:i32=120;",
    "const ST_REFUSED_BADOP:i32=120;\nconst ST_REFUSED_CONSUMED:i32=121;",
    "refused-consumed")

# ---- New op constant after ST_OP_PEXPIRED = 19 ----
rep("const ST_OP_PEXPIRED:i32=19;",
    "const ST_OP_PEXPIRED:i32=19;\nconst ST_OP_DELETE_STRONG:i32=20;",
    "op-delete-strong")

# ---- 3b. st_collect_cites bufferless fix (F4b exact code) ----
old_seen = """            let cite:i32=st_aw(s,i,2);
            let seen:i32=0;let k:i32=0;
            while(k<n){if(st_i32_get(out,k*4)==cite){seen=1;break;}k=k+1;}
"""
new_seen = """            let cite:i32=st_aw(s,i,2);
            // F4b bufferless fix (2026-09-26): the old seen-scan re-read the
            // 16-byte `out` buffer for k<n, but only 4 slots are ever written.
            // With >4 distinct cites in the effort window (a second cite round
            // after kill->rollback accumulates 8) the read ran past the buffer
            // and the binary panicked ("slice index out of bounds") -- on the
            // PRISTINE core, not caused by the F4b edits (bisection 2026-09-26:
            // pristine + probe reproduces; first crew's miscompile theory
            // retracted). Distinctness is now decided against the ledger itself
            // (exact on every input), the 4-write cap stays, the returned
            // distinct count is unchanged on all non-panicking inputs.
            let seen:i32=0;let k:i32=after_idx+1;
            while(k<i){
                if(st_aw(s,k,0)==ST_OP_EVIDENCE && st_aw(s,k,1)==slot &&
                   st_aw(s,k,4)==ST_OK && st_aw(s,k,2)==cite){seen=1;break;}
                k=k+1;
            }
"""
rep(old_seen, new_seen, "collect-cites-bufferless")

# ---- 3d. st_cite_consumed + st_count_spent_cites (F4b exact, extended with
#        ST_OP_DELETE_STRONG as a consuming destruction) ----
# Insert right after st_collect_cites's closing "    return n;\n}\n"
old_tail = """            if(seen==0){
                if(n<4){st_i32_set(out,n*4,cite);}
                n=n+1;
            }
        }
        i=i+1;
    }
    return n;
}
"""
new_fns = """            if(seen==0){
                if(n<4){st_i32_set(out,n*4,cite);}
                n=n+1;
            }
        }
        i=i+1;
    }
    return n;
}
// F4 FIX (F4b cite-consumption, 2026-09-25): a cite_ep is CONSUMED iff it
// sits in the effort window of an OK destruction (KILL_EVIDENCED,
// OVERWRITE, or DELETE_STRONG) on the same slot with index in
// (after_idx, upto). Derived from the ledger itself -- no new state, no new
// entries -- so the checker recomputes the identical predicate from its own
// copy of the ledger. Destructions at or before after_idx cannot have
// consumed a cite newer than after_idx, which bounds the scan.
fn st_cite_consumed(s:*StStore,slot:i32,cite_ep:i32,after_idx:i32,upto:i32)i32 {
    let d:i32=after_idx+1;
    while(d<upto){
        let op:i32=st_aw(s,d,0);
        if((op==ST_OP_KILL_EVIDENCED || op==ST_OP_OVERWRITE ||
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
}
// Count distinct OK EVIDENCE cite_eps for slot in (after_idx, upto) that
// were consumed by an earlier destruction. Pure Zag, no indexed narrow
// casts (uses st_aw); effort windows are small (bounded by the cite rate),
// so the O(W^2) distinctness scan needs no buffer and no cap.
fn st_count_spent_cites(s:*StStore,slot:i32,after_idx:i32,upto:i32)i32 {
    let n:i32=0;
    let i:i32=after_idx+1;
    while(i<upto){
        if(st_aw(s,i,0)==ST_OP_EVIDENCE && st_aw(s,i,1)==slot && st_aw(s,i,4)==ST_OK){
            let cite:i32=st_aw(s,i,2);
            let seen:i32=0;let k:i32=after_idx+1;
            while(k<i){
                if(st_aw(s,k,0)==ST_OP_EVIDENCE && st_aw(s,k,1)==slot &&
                   st_aw(s,k,4)==ST_OK && st_aw(s,k,2)==cite){seen=1;break;}
                k=k+1;
            }
            if(seen==0 && st_cite_consumed(s,slot,cite,after_idx,upto)==1){n=n+1;}
        }
        i=i+1;
    }
    return n;
}
"""
rep(old_tail, new_fns, "cite-consumed-fns")

# ---- 3e. st_kill_effort_check: total/spent/fresh trio + 121/109 split ----
old_cnt = """    let buf:[]u8=nio_alloc(16);
    let cnt:i32=st_collect_cites(s,slot,lss,s.*.audit_n,buf);
    nio_free(buf);
    if(baseline==1){
        if(cnt<1){return ST_REFUSED_EFFORT;}
    } else {
        if(cnt!=need){return ST_REFUSED_EFFORT;}
    }
"""
new_cnt = """    let buf:[]u8=nio_alloc(16);
    let total:i32=st_collect_cites(s,slot,lss,s.*.audit_n,buf);
    nio_free(buf);
    // F4b: cites spent paying for an earlier destruction on this slot are
    // consumed and cannot pay again -- only FRESH cites count toward the
    // price. A destruction after a kill->rollback must bring new episodes,
    // not the pre-kill ones (round-4 finding F4).
    let spent:i32=st_count_spent_cites(s,slot,lss,s.*.audit_n);
    let cnt:i32=total-spent;
    if(baseline==1){
        if(cnt<1){return ST_REFUSED_EFFORT;}
    } else {
        if(cnt!=need){
            if(spent>0){return ST_REFUSED_CONSUMED;}
            return ST_REFUSED_EFFORT;
        }
    }
"""
rep(old_cnt, new_cnt, "kill-effort-f4b")

# ---- 3c. st_evidence dup-check bufferless fix (F4b exact code) ----
old_dup = """        let buf:[]u8=nio_alloc(16);
        let n:i32=st_collect_cites(s,slot,lss,s.*.audit_n,buf);
        let k:i32=0;let dup:i32=0;
        while(k<n){if(st_i32_get(buf,k*4)==cite_ep){dup=1;break;}k=k+1;}
        nio_free(buf);
        if(dup==1){rc=ST_REFUSED_DUPCITE;}
"""
new_dup = """        // F4b bufferless fix (2026-09-26): dup-scan the ledger directly. The old
        // code re-read the 16-byte buffer for k<n with only 4 slots written --
        // >4 distinct cites in the effort window (second cite round after
        // kill->rollback) panicked with "slice index out of bounds" on the
        // pristine core (bisection 2026-09-26; not an F4b miscompile). The
        // direct scan is exactly the dup predicate on all non-panicking inputs.
        let k:i32=lss+1;let dup:i32=0;
        while(k<s.*.audit_n){
            if(st_aw(s,k,0)==ST_OP_EVIDENCE && st_aw(s,k,1)==slot &&
               st_aw(s,k,4)==ST_OK && st_aw(s,k,2)==cite_ep){dup=1;break;}
            k=k+1;
        }
        if(dup==1){rc=ST_REFUSED_DUPCITE;}
"""
rep(old_dup, new_dup, "evidence-bufferless")

# ---- NEW: st_delete_strong after st_kill_evidenced ----
old_kill_tail = """    let arc:i32=st_audit_append(s,ST_OP_KILL_EVIDENCED,slot,-1,-1,rc,
        b1,b2,b3,b4,b5,b6,a1,a2,a3,a4,a5,a6,ST_ROLE_TNN,0);
    if(arc!=ST_OK){return arc;}
    return rc;
}
"""
new_delete = """    let arc:i32=st_audit_append(s,ST_OP_KILL_EVIDENCED,slot,-1,-1,rc,
        b1,b2,b3,b4,b5,b6,a1,a2,a3,a4,a5,a6,ST_ROLE_TNN,0);
    if(arc!=ST_OK){return arc;}
    return rc;
}
// DELETE-STRONG (Micah directive 2026-09-25): the one-step delete button.
// Modeled exactly on st_kill_evidenced: same fail-closed guard order
// (badslot -> audit-room -> snap -> effort check), the merged HW-priced,
// consumption-aware effort check, st_kill_clear on OK, audit ST_OP_DELETE_STRONG.
// Law meaning: destroying a judgment in ONE step costs the full high-water
// erase price of the STRONGEST judgment it destroys (n(HW)). The old
// weaken-then-delete dance stays legal but is priced identically (n(HW)
// either way), hence pointless by construction -- it buys no discount.
// A delete is neither a strength-write nor a judgment birth: it is excluded
// from st_last_strength_idx and st_epoch_highwater by design (the HW epoch
// tracks judgments the delete DESTROYS, not the delete itself).
fn st_delete_strong(s:*StStore,slot:i32)i32 {
    if(st_badslot(s,slot)==1){return cl_bad();}
    if(st_audit_room(s)==0){return ST_REFUSED_AUDITFULL;}
    let b1:i32=0;let b2:i32=0;let b3:i32=0;let b4:i32=0;let b5:i32=0;let b6:i32=0;
    let rc:i32=st_kill_effort_check(s,slot,&b1,&b2,&b3,&b4,&b5,&b6);
    if(rc==ST_OK){st_kill_clear(s,slot);}
    let a1:i32=b1;let a2:i32=b2;let a3:i32=b3;let a4:i32=b4;let a5:i32=b5;let a6:i32=b6;
    if(rc==ST_OK){st_snap(s,slot,&a1,&a2,&a3,&a4,&a5,&a6);}
    let arc:i32=st_audit_append(s,ST_OP_DELETE_STRONG,slot,-1,-1,rc,
        b1,b2,b3,b4,b5,b6,a1,a2,a3,a4,a5,a6,ST_ROLE_TNN,0);
    if(arc!=ST_OK){return arc;}
    return rc;
}
"""
rep(old_kill_tail, new_delete, "st-delete-strong")

# ---- st_rollback_last: add DELETE_STRONG to mutating-op list ----
old_rb = """    if(op==ST_OP_ADD || op==ST_OP_KILL || op==ST_OP_KILL_EVIDENCED || op==ST_OP_PIN ||
       op==ST_OP_UNPIN || op==ST_OP_PROMOTE || op==ST_OP_DEMOTE ||
       op==ST_OP_STRENGTHEN || op==ST_OP_WEAKEN || op==ST_OP_TRAINER_DECLARE ||
       op==ST_OP_OVERWRITE || op==ST_OP_FORCE_PIN || op==ST_OP_FORCE_UNPIN){mutating=1;}
"""
new_rb = """    if(op==ST_OP_ADD || op==ST_OP_KILL || op==ST_OP_KILL_EVIDENCED || op==ST_OP_PIN ||
       op==ST_OP_UNPIN || op==ST_OP_PROMOTE || op==ST_OP_DEMOTE ||
       op==ST_OP_STRENGTHEN || op==ST_OP_WEAKEN || op==ST_OP_TRAINER_DECLARE ||
       op==ST_OP_OVERWRITE || op==ST_OP_FORCE_PIN || op==ST_OP_FORCE_UNPIN ||
       op==ST_OP_DELETE_STRONG){mutating=1;}
"""
rep(old_rb, new_rb, "rollback-mutating")

# ---- st_replay_check: restore list + derived P3 branch ----
old_replay = """                if(op==ST_OP_ADD || op==ST_OP_KILL || op==ST_OP_KILL_EVIDENCED ||
                   op==ST_OP_PIN || op==ST_OP_UNPIN || op==ST_OP_PROMOTE ||
                   op==ST_OP_DEMOTE || op==ST_OP_STRENGTHEN || op==ST_OP_WEAKEN ||
                   op==ST_OP_TRAINER_DECLARE || op==ST_OP_OVERWRITE ||
                   op==ST_OP_FORCE_PIN || op==ST_OP_FORCE_UNPIN){
"""
new_replay = """                if(op==ST_OP_ADD || op==ST_OP_KILL || op==ST_OP_KILL_EVIDENCED ||
                   op==ST_OP_PIN || op==ST_OP_UNPIN || op==ST_OP_PROMOTE ||
                   op==ST_OP_DEMOTE || op==ST_OP_STRENGTHEN || op==ST_OP_WEAKEN ||
                   op==ST_OP_TRAINER_DECLARE || op==ST_OP_OVERWRITE ||
                   op==ST_OP_FORCE_PIN || op==ST_OP_FORCE_UNPIN ||
                   op==ST_OP_DELETE_STRONG){
"""
rep(old_replay, new_replay, "replay-restore")

old_p3 = """                } else if(op==ST_OP_KILL || op==ST_OP_KILL_EVIDENCED){
                    st_i32_set(sh.last_cite,sl*4,-1);
                    st_i32_set(sh.step_ep,sl*4,-1);
"""
new_p3 = """                } else if(op==ST_OP_KILL || op==ST_OP_KILL_EVIDENCED ||
                            op==ST_OP_DELETE_STRONG){
                    st_i32_set(sh.last_cite,sl*4,-1);
                    st_i32_set(sh.step_ep,sl*4,-1);
"""
rep(old_p3, new_p3, "replay-p3")

open(P, "w").write(src)
print("CORE MERGE OK")
