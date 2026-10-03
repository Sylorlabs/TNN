#!/usr/bin/env python3
"""Merge F4b checker hunks + ck_verify_delete into the F1-forkA base checker.

Inputs:  ~/workspace/strength-delete/strength_checker.zag (F1-forkA base)
Outputs: merged file in place. Exact-match replacements; aborts on mismatch.
"""
W = "/home/hatch/workspace/strength-delete/"
P = W + "strength_checker.zag"
src = open(P).read()

def rep(old, new, tag, count=1):
    global src
    n = src.count(old)
    assert n == count, f"MISMATCH [{tag}]: found {n}, expected {count}\n---old---\n{old[:400]}"
    src = src.replace(old, new)

# ---- ck_verify_kill: F4b fresh-count (total-spent) ----
old_k = """    // distinct cites in (lss, kill_idx)
    let buf:[]u8=nio_alloc(16);
    let n:i32=st_collect_cites(s,slot,lss,kill_idx,buf);
"""
new_k = """    // F4b cite-consumption: only FRESH (unconsumed) cites count toward the
    // price; cites spent on an earlier destruction cannot pay again.
    let buf:[]u8=nio_alloc(16);
    let ktotal:i32=st_collect_cites(s,slot,lss,kill_idx,buf);
    nio_free(buf);
    let kspent:i32=st_count_spent_cites(s,slot,lss,kill_idx);
    let n:i32=ktotal-kspent;
"""
rep(old_k, new_k, "kill-fresh-count")

# ---- ck_verify_kill: genuineness only on unconsumed cites ----
old_kg = """        if(st_aw(s,i,0)==ST_OP_EVIDENCE && st_aw(s,i,1)==slot && st_aw(s,i,4)==ST_OK){
            total_ok=total_ok+1;
            if(gate_mode==0 && cand_m>=0){
                let cite:i32=st_aw(s,i,2);
                f=f+cl_check("ck_cite_genuine",ck_is_contra_ep(cur,cand_m,cite,v,h),1);
            }
        }
"""
new_kg = """        if(st_aw(s,i,0)==ST_OP_EVIDENCE && st_aw(s,i,1)==slot && st_aw(s,i,4)==ST_OK){
            if(st_cite_consumed(s,slot,st_aw(s,i,2),lss,kill_idx)==0){
                total_ok=total_ok+1;
                if(gate_mode==0 && cand_m>=0){
                    let cite:i32=st_aw(s,i,2);
                    f=f+cl_check("ck_cite_genuine",ck_is_contra_ep(cur,cand_m,cite,v,h),1);
                }
            }
        }
"""
rep(old_kg, new_kg, "kill-genuine-fresh")

# ---- ck_verify_kill: drop the now-early nio_free (moved up with fresh-count)
old_kf = """    f=f+cl_check("ck_justify_present",jf,1);
    nio_free(buf);
    return f;
}
"""
new_kf = """    f=f+cl_check("ck_justify_present",jf,1);
    return f;
}
"""
rep(old_kf, new_kf, "kill-free-move")

# ---- ck_verify_overwrite: F4b fresh-count ----
old_o = """    let lss:i32=st_last_strength_idx(s,slot,ow_idx);
    let buf:[]u8=nio_alloc(16);
    let n:i32=st_collect_cites(s,slot,lss,ow_idx,buf);
    nio_free(buf);
"""
new_o = """    let lss:i32=st_last_strength_idx(s,slot,ow_idx);
    // F4b cite-consumption: only FRESH (unconsumed) cites count toward the
    // overwrite price.
    let buf:[]u8=nio_alloc(16);
    let ototal:i32=st_collect_cites(s,slot,lss,ow_idx,buf);
    nio_free(buf);
    let ospent:i32=st_count_spent_cites(s,slot,lss,ow_idx);
    let n:i32=ototal-ospent;
"""
rep(old_o, new_o, "ow-fresh-count")

# ---- ck_verify_overwrite: genuineness only on unconsumed cites ----
old_og = """        if(st_aw(s,gi,0)==ST_OP_EVIDENCE && st_aw(s,gi,1)==slot && st_aw(s,gi,4)==ST_OK){
            total_ok=total_ok+1;
            if(gate_mode==0 && cand_m>=0){
                let cite:i32=st_aw(s,gi,2);
                f=f+cl_check("ck_ow_cite_genuine",ck_is_contra_ep(cur,cand_m,cite,v,h),1);
            }
        }
"""
new_og = """        if(st_aw(s,gi,0)==ST_OP_EVIDENCE && st_aw(s,gi,1)==slot && st_aw(s,gi,4)==ST_OK){
            if(st_cite_consumed(s,slot,st_aw(s,gi,2),lss,ow_idx)==0){
                total_ok=total_ok+1;
                if(gate_mode==0 && cand_m>=0){
                    let cite:i32=st_aw(s,gi,2);
                    f=f+cl_check("ck_ow_cite_genuine",ck_is_contra_ep(cur,cand_m,cite,v,h),1);
                }
            }
        }
"""
rep(old_og, new_og, "ow-genuine-fresh")

# ---- ck_strength_lineage: DELETE_STRONG is a legal strength delta ----
old_lin = """                if(op==ST_OP_ADD || op==ST_OP_STRENGTHEN || op==ST_OP_WEAKEN ||
                   op==ST_OP_TRAINER_DECLARE || op==ST_OP_OVERWRITE ||
                   op==ST_OP_KILL || op==ST_OP_KILL_EVIDENCED ||
                   op==ST_OP_ROLLBACK){legal=1;}
"""
new_lin = """                if(op==ST_OP_ADD || op==ST_OP_STRENGTHEN || op==ST_OP_WEAKEN ||
                   op==ST_OP_TRAINER_DECLARE || op==ST_OP_OVERWRITE ||
                   op==ST_OP_KILL || op==ST_OP_KILL_EVIDENCED ||
                   op==ST_OP_DELETE_STRONG || op==ST_OP_ROLLBACK){legal=1;}
"""
rep(old_lin, new_lin, "lineage-delete")

# ---- ck_verify_delete: mirror ck_verify_kill's merged logic for DELETE_STRONG ----
# Insert right before ck_verify_overwrite's R4-HARDENING comment block.
old_ins = """// R4 HARDENING (2026-09-25): effort-before-overwrite verification.
"""
new_fn = """// DELETE-STRONG verification (2026-09-26): mirror ck_verify_kill's merged
// logic for ST_OP_DELETE_STRONG entries. Prices the strongest judgment
// destroyed (high-water since the last judgment epoch, cur-at-op is the
// before-word at del_idx), counts only FRESH (unconsumed) cites, and runs
// genuineness only on unconsumed cites. baseline=1: P3 BASELINE delete
// (expired protection) — needs >=1 cite.
fn ck_verify_delete(s:*StStore,slot:i32,del_idx:i32,cur:i32,v:i32,h:i32,gate_mode:i32,cand_m:i32,baseline:i32)i32 {
    let f:i32=0;
    // mirror st_kill_effort_check — price the strongest judgment destroyed
    // (high-water since the last judgment epoch). cur-at-op is the
    // before-word at del_idx.
    let str_before:i32=(st_aw(s,del_idx,8)&255);
    let hw:i32=st_epoch_highwater(s,slot,del_idx,str_before);
    if(hw<0){f=f+cl_check("ck_del_hw_epoch",0,1);hw=str_before;}
    let need:i32=ck_n(hw);
    let lss:i32=st_last_strength_idx(s,slot,del_idx);
    // F4b cite-consumption: only FRESH (unconsumed) cites count toward the
    // price; cites spent on an earlier destruction cannot pay again.
    let buf:[]u8=nio_alloc(16);
    let dtotal:i32=st_collect_cites(s,slot,lss,del_idx,buf);
    nio_free(buf);
    let dspent:i32=st_count_spent_cites(s,slot,lss,del_idx);
    let n:i32=dtotal-dspent;
    if(baseline==1){
        let has_cite:i32=0;
        if(n>=1){has_cite=1;}
        f=f+cl_check("ck_del_cite_baseline",has_cite,1);
    } else {
        f=f+cl_check("ck_del_cite_count",n,need);
    }
    let total_ok:i32=0;
    let i:i32=lss+1;
    while(i<del_idx){
        if(st_aw(s,i,0)==ST_OP_EVIDENCE && st_aw(s,i,1)==slot && st_aw(s,i,4)==ST_OK){
            if(st_cite_consumed(s,slot,st_aw(s,i,2),lss,del_idx)==0){
                total_ok=total_ok+1;
                if(gate_mode==0 && cand_m>=0){
                    let cite:i32=st_aw(s,i,2);
                    f=f+cl_check("ck_del_cite_genuine",ck_is_contra_ep(cur,cand_m,cite,v,h),1);
                }
            }
        }
        i=i+1;
    }
    f=f+cl_check("ck_del_cite_distinct",total_ok,n);
    // properly-clocked JUSTIFY: OK JUSTIFY for slot in (lss, del_idx)
    let j:i32=lss+1;let jf:i32=0;
    while(j<del_idx){
        if(st_aw(s,j,0)==ST_OP_JUSTIFY && st_aw(s,j,1)==slot && st_aw(s,j,4)==ST_OK){
            let code:i32=st_aw(s,j,3);
            if(code>=ST_J_CONFIRMED_IMPORTANT && code<=ST_J_TRAINER_DIRECTIVE){jf=1;break;}
        }
        j=j+1;
    }
    f=f+cl_check("ck_del_justify",jf,1);
    return f;
}
// R4 HARDENING (2026-09-25): effort-before-overwrite verification.
"""
rep(old_ins, new_fn, "ck-verify-delete-fn")

# ---- ck_verify dispatch: wire DELETE_STRONG alongside kill/overwrite ----
old_disp = """            if((op==ST_OP_KILL || op==ST_OP_KILL_EVIDENCED) && sl>=0){
                let b1:i32=st_aw(s,i,5);
                let pinned_b:i32=((b1>>8)&255);let region_b:i32=((b1>>24)&255);
                let fp_b:i32=(st_aw(s,i,10)&255);
                if(pinned_b==1 || fp_b==1 || region_b==ST_REGION_CORE){bad_kill=1;}
                if(op==ST_OP_KILL_EVIDENCED && arm!=1){
                    let cm:i32=(cur_m[sl*4] as i32)|((cur_m[sl*4+1] as i32)<<8)|
                        ((cur_m[sl*4+2] as i32)<<16)|((cur_m[sl*4+3] as i32)<<24);
                    let bl:i32=0;
                    if(arm==3 && ck_pexp[sl]==1){bl=1;}
                    f=f+ck_verify_kill(s,sl,i,cur,variant,h,gate_mode,cm,bl);
                }
                // clear P3 tracking after the kill (verification above used it)
                st_i32_set(ck_lc,sl*4,-1);
                st_i32_set(ck_adm,sl*4,-1);
                ck_pexp[sl]=0;
            }
"""
new_disp = """            if((op==ST_OP_KILL || op==ST_OP_KILL_EVIDENCED) && sl>=0){
                let b1:i32=st_aw(s,i,5);
                let pinned_b:i32=((b1>>8)&255);let region_b:i32=((b1>>24)&255);
                let fp_b:i32=(st_aw(s,i,10)&255);
                if(pinned_b==1 || fp_b==1 || region_b==ST_REGION_CORE){bad_kill=1;}
                if(op==ST_OP_KILL_EVIDENCED && arm!=1){
                    let cm:i32=(cur_m[sl*4] as i32)|((cur_m[sl*4+1] as i32)<<8)|
                        ((cur_m[sl*4+2] as i32)<<16)|((cur_m[sl*4+3] as i32)<<24);
                    let bl:i32=0;
                    if(arm==3 && ck_pexp[sl]==1){bl=1;}
                    f=f+ck_verify_kill(s,sl,i,cur,variant,h,gate_mode,cm,bl);
                }
                // clear P3 tracking after the kill (verification above used it)
                st_i32_set(ck_lc,sl*4,-1);
                st_i32_set(ck_adm,sl*4,-1);
                ck_pexp[sl]=0;
            }
            if(op==ST_OP_DELETE_STRONG && sl>=0){
                let b1:i32=st_aw(s,i,5);
                let pinned_b:i32=((b1>>8)&255);let region_b:i32=((b1>>24)&255);
                let fp_b:i32=(st_aw(s,i,10)&255);
                if(pinned_b==1 || fp_b==1 || region_b==ST_REGION_CORE){bad_kill=1;}
                if(arm!=1){
                    let cm:i32=(cur_m[sl*4] as i32)|((cur_m[sl*4+1] as i32)<<8)|
                        ((cur_m[sl*4+2] as i32)<<16)|((cur_m[sl*4+3] as i32)<<24);
                    let bl:i32=0;
                    if(arm==3 && ck_pexp[sl]==1){bl=1;}
                    f=f+ck_verify_delete(s,sl,i,cur,variant,h,gate_mode,cm,bl);
                }
                // clear P3 tracking after the delete (verification above used it)
                st_i32_set(ck_lc,sl*4,-1);
                st_i32_set(ck_adm,sl*4,-1);
                ck_pexp[sl]=0;
            }
"""
rep(old_disp, new_disp, "ck-dispatch-delete")

open(P, "w").write(src)
print("CHECKER MERGE OK")
