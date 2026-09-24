#!/usr/bin/env python3
# merge_v3.py — assemble V3 ob_arbiter.zag and ob_pam.zag.
# ob_arbiter: L14 base + V1-h_organ (R1) + V2-h_sep (R3) edits.
# ob_pam:     L14 base + V1-h_organ (PAM_CONTRA register + novelty fns).
# Every replacement asserts exactly one occurrence.
import sys

W = "/home/hatch/workspace"
L14 = W + "/h1evo/ledger_l14/src"
V1O = W + "/h1evo/v1_novel/h_organ"
OUT = W + "/h1evo/v3_full"

def rep_once(text, old, new, tag):
    n = text.count(old)
    if n != 1:
        print(f"FATAL: {tag}: found {n} occurrences (want 1)")
        sys.exit(1)
    return text.replace(old, new, 1)

# ---------------- ob_arbiter.zag ----------------
t = open(L14 + "/ob_arbiter.zag").read()

# (V1-1) M_REVOKE: inform the PAM organ of the contradiction on kill.
old = """                    if(rc==MA_OK){ob_s32(routes,pc*4,-1);}
                } else {"""
new = """                    if(rc==MA_OK){ob_s32(routes,pc*4,-1);}
                    // R1 repair (H-organ): a killed install contradicts the
                    // policy — inform the PAM organ, which owns the
                    // contradiction record and the novelty judgment.
                    if(rc==MA_OK){pam_note_contradiction(pam,a1);}
                } else {"""
t = rep_once(t, old, new, "V1-1 revoke-note")

# (V1-2) M_COMMIT: novelty predicate drives FRESH/REVISE; REVISE-admit
# clears the contradiction mark. Keeps L14's arb_audit_gov for the verdict.
old = """        if(mtype==M_COMMIT){
            // survivor install: PAM gate in FRESH mode (M1/M3/M4) —
            // the documented intent. A first-time survivor install
            // has no prior corroboration, so REVISE mode would
            // withhold genuinely novel installs (fixed 2026-09-24).
            let slot:i32=arb_pam_claim(pam,a2,cal,ep);
            if(slot>=0){
                let verdict:i32=0;let reason:i32=0;
                pam_verdict(pam,slot,0,&verdict,&reason);
                arb_audit_gov(ep,ast,alog,aln,M_PAM_VERDICT,verdict,reason);
                if(verdict==PAM_ADMIT){
"""
new = """        if(mtype==M_COMMIT){
            // survivor install: PAM gate mode from the novelty predicate
            // (R1 repair, H-organ: the PAM organ owns the novelty judgment
            // over its own rows; the arbiter queries it). FRESH (M1/M3/M4)
            // iff the claim is novel; non-novel claims route through REVISE
            // corroboration (M1/M3/M4 AND M9/cf1). Novel (frozen): no live
            // or dead PAM row for that policy AND no unresolved contradiction
            // record for the policy. The novelty query MUST precede the row
            // append: the row being gated does not count as "a PAM row for
            // that policy" (novelty is judged on prior rows + records).
            let novel:i32=pam_is_novel(pam,a2);
            let slot:i32=arb_pam_claim(pam,a2,cal,ep);
            if(slot>=0){
                let verdict:i32=0;let reason:i32=0;
                let mode:i32=PAM_MODE_REVISE;
                if(novel==1){mode=PAM_MODE_FRESH;}
                pam_verdict(pam,slot,mode,&verdict,&reason);
                arb_audit_gov(ep,ast,alog,aln,M_PAM_VERDICT,verdict,reason);
                if(verdict==PAM_ADMIT){
                    // A REVISE-admitted commit resolves the contradiction
                    // for the policy by corroborated re-admission: clear
                    // the unresolved-contradiction mark.
                    if(mode==PAM_MODE_REVISE){pam_clear_contradiction(pam,a2);}
"""
t = rep_once(t, old, new, "V1-2 commit-novelty")

# (V2-1) separate namespace const for the commit ring.
old = """// L4': governance audit reservation (see arb_audit). Sized for the tested"""
new = """// H1EVO V2 H-sep (R3 repair): the commit ring lives in a SEPARATE namespace
// region of the routes allocation: region [ARB_ROUTES, 2*ARB_ROUTES).
// Commit-episode keys and claim-id keys never share a slot, so a commit can
// no longer clobber a claim route (R3a) or misroute a revoke/promote.
// M_REVOKE/M_PROMOTE keep reading the claim region via the provisional claim
// id in ast; they never consult the ring.
const ARB_RING_OFF:i32=129; // ring region base (== ARB_ROUTES)

// L4': governance audit reservation (see arb_audit). Sized for the tested"""
t = rep_once(t, old, new, "V2-1 ring-off-const")

# (V2-2) arb_new_routes: doubled allocation for the two namespaces.
old = """    let r:[]u8=ob_alloc(ARB_ROUTES*4);"""
new = """    // H1EVO V2 H-sep: two disjoint namespace regions in one allocation:
    // [0,ARB_ROUTES) claim-id routes, [ARB_ROUTES,2*ARB_ROUTES) commit ring.
    let r:[]u8=ob_alloc(ARB_ROUTES*4*2);"""
t = rep_once(t, old, new, "V2-2 routes-alloc")
old = """    while(i<ARB_ROUTES){ob_s32(r,i*4,-1);i=i+1;}"""
new = """    while(i<ARB_ROUTES*2){ob_s32(r,i*4,-1);i=i+1;}"""
t = rep_once(t, old, new, "V2-3 routes-init")

# (V2-3) M_COMMIT ring write into the separate namespace.
old = """                        // REPAIR 2026-09-24 (routes-table capacity panic):
                        // M_COMMIT carries no claim id, so the survivor's
                        // slot is keyed by the dispatch episode — but the
                        // episode clock is UNBOUNDED while routes has the
                        // fixed claim-id capacity ARB_ROUTES=129. Indexing
                        // by raw ep panicked (slice index out of bounds)
                        // the first time a commit landed at global ep >=
                        // 129 (lie bundle, 10x scale, ep 156). The commit
                        // entry is write-only (M_REVOKE/M_PROMOTE look up
                        // routes only via the provisional claim id in
                        // ast, which M_COMMIT never sets), so the key only
                        // needs to be in-bounds and per-episode distinct:
                        // a ring over the fixed capacity. Identity for
                        // ep < ARB_ROUTES, so all prior in-bounds behavior
                        // is bit-for-bit preserved; no horizon constant is
                        // invented, and no larger claim can panic again.
                        ob_s32(routes,(ep%ARB_ROUTES)*4,os);"""
new = """                        // H1EVO V2 H-sep (R3 repair): M_COMMIT carries no claim
                        // id, so the survivor's slot is keyed by the
                        // dispatch episode into the SEPARATE commit-ring
                        // namespace (region [ARB_ROUTES,2*ARB_ROUTES)),
                        // never into the claim-id region. The ring stays
                        // write-only (R3b(i) read-audit: no reader consults
                        // a commit-keyed slot) and can no longer clobber a
                        // claim route (R3a) or misroute revoke/promote.
                        ob_s32(routes,(ARB_RING_OFF+ep%ARB_ROUTES)*4,os);"""
t = rep_once(t, old, new, "V2-4 ring-write")

# (V2-4) M_PROPOSE_INSTALL: bounds-checked claim ids at ingress.
old = """        if(mtype==M_PROPOSE_INSTALL){
            // fresh install: PAM gate in FRESH mode (M1/M3/M4).
            let slot:i32=arb_pam_claim(pam,a1,cal,ep);
            if(slot>=0){
                let verdict:i32=0;let reason:i32=0;
                pam_verdict(pam,slot,0,&verdict,&reason);
                arb_audit_gov(ep,ast,alog,aln,M_PAM_VERDICT,verdict,reason);
                if(verdict==PAM_ADMIT){
                    let os:i32=-1;
                    let v:i32=mm_declare_value(trust,64,150,1);
                    let rc:i32=arb_mem_apply(live,value,pinned,region,tier,step,
                        maudit,hdr,trust,alog,aln,ep,MA_OP_ADD,-1,v,MA_REGION_USER,&os);
                    if(rc==MA_OK){
                        ob_s32(routes,a2*4,os);
                        ob_s32(ast,0,a2);ob_s32(ast,4,a1);
                    }
                } else {
                    arb_audit(alog,aln,ep,ARB_DROP,M_PROPOSE_INSTALL,reason);
                }
            } else {
                arb_audit(alog,aln,ep,ARB_DROP,M_PROPOSE_INSTALL,-1);
            }
        }"""
new = """        if(mtype==M_PROPOSE_INSTALL){
            // H1EVO V2 (R3b' repair): claim ids are bounds-checked at
            // ingress. An out-of-range id is a bounded, audited refusal
            // (ARB_DROP, refusal family): ledgered, mutates nothing, never
            // touches the routes table, burns no PAM row.
            if(a2<0 || a2>=ARB_ROUTES){
                arb_audit(alog,aln,ep,ARB_DROP,M_PROPOSE_INSTALL,a2);
            } else {
            // fresh install: PAM gate in FRESH mode (M1/M3/M4).
            let slot:i32=arb_pam_claim(pam,a1,cal,ep);
            if(slot>=0){
                let verdict:i32=0;let reason:i32=0;
                pam_verdict(pam,slot,0,&verdict,&reason);
                arb_audit_gov(ep,ast,alog,aln,M_PAM_VERDICT,verdict,reason);
                if(verdict==PAM_ADMIT){
                    let os:i32=-1;
                    let v:i32=mm_declare_value(trust,64,150,1);
                    let rc:i32=arb_mem_apply(live,value,pinned,region,tier,step,
                        maudit,hdr,trust,alog,aln,ep,MA_OP_ADD,-1,v,MA_REGION_USER,&os);
                    if(rc==MA_OK){
                        ob_s32(routes,a2*4,os);
                        ob_s32(ast,0,a2);ob_s32(ast,4,a1);
                    }
                } else {
                    arb_audit(alog,aln,ep,ARB_DROP,M_PROPOSE_INSTALL,reason);
                }
            } else {
                arb_audit(alog,aln,ep,ARB_DROP,M_PROPOSE_INSTALL,-1);
            }
            }
        }"""
t = rep_once(t, old, new, "V2-5 propose-bounds")

open(OUT + "/ob_arbiter.zag", "w").write(t)
print("ob_arbiter.zag merged OK")

# ---------------- ob_pam.zag ----------------
p = open(L14 + "/ob_pam.zag").read()

# Layout: PAM_EVICTED@7176 (4B, L4') then PAM_CONTRA@7180 (256B, R1').
old = """const PAM_EVICTED:i32=7176;      // i32 ring-eviction count (L4')
const PAM_STATE:i32=7180;"""
new = """const PAM_EVICTED:i32=7176;      // i32 ring-eviction count (L4')
const PAM_CONTRA:i32=7180;       // 64*4 = 256 bytes, policy+1 words (R1')
const PAM_STATE:i32=7436;"""
p = rep_once(p, old, new, "P1 pam-consts")

old = """// organ state: rows buffer (PAM_CAP*12*4) + count word + ledger + ledger_n
// + eviction counter. The test/brain allocates via pam_new()."""
new = """// organ state: rows buffer (PAM_CAP*12*4) + count word + ledger + ledger_n
// + eviction counter + contradiction register. The test/brain allocates via
// pam_new()."""
p = rep_once(p, old, new, "P2 pam-comment")

# Append the R1 novelty fns (from V1-h_organ), with PAM_CONTRA at 7180.
novelty_fns = """
// ---- R1 repair: novelty predicate (H-organ) ----
// Record an unresolved contradiction for a policy (called by the arbiter
// when it kills an install of that policy). Idempotent; returns 0, or -1
// if the register is full (unreachable while rows <= PAM_CAP).
fn pam_note_contradiction(s:[]u8,policy:i32)i32 {
    if(pam_has_contradiction(s,policy)==1){return 0;}
    let i:i32=0;
    while(i<PAM_CAP){
        if(ob_g32(s,PAM_CONTRA+i*4)==0){
            ob_s32(s,PAM_CONTRA+i*4,policy+1);
            return 0;
        }
        i=i+1;
    }
    return -1;
}

// 1 iff an unresolved contradiction record exists for the policy.
fn pam_has_contradiction(s:[]u8,policy:i32)i32 {
    let i:i32=0;
    while(i<PAM_CAP){
        if(ob_g32(s,PAM_CONTRA+i*4)==policy+1){return 1;}
        i=i+1;
    }
    return 0;
}

// Clear the unresolved-contradiction mark for a policy: a REVISE-admitted
// commit resolves the contradiction by corroborated re-admission.
fn pam_clear_contradiction(s:[]u8,policy:i32)i32 {
    let i:i32=0;
    while(i<PAM_CAP){
        if(ob_g32(s,PAM_CONTRA+i*4)==policy+1){
            ob_s32(s,PAM_CONTRA+i*4,0);
            return 0;
        }
        i=i+1;
    }
    return -1;
}

// The frozen novelty predicate (PREREG_H1EVO section 2, R1'): NOVEL iff no live
// or dead PAM row for that policy AND no unresolved contradiction record
// for that policy. Rows are append-only (never deleted), so "live or
// dead" is one scan over all rows' formation jcodes. Returns 1 = novel
// (FRESH route), 0 = non-novel (REVISE corroboration).
fn pam_is_novel(s:[]u8,policy:i32)i32 {
    let n:i32=pam_n(s);
    let i:i32=0;
    while(i<n){
        if(pam_row(s,i,PAMW_JF)==policy){return 0;}
        i=i+1;
    }
    if(pam_has_contradiction(s,policy)==1){return 0;}
    return 1;
}
"""
# V1 placed these right after pam_ledger_count_reason's region; appending at
# end of file is equivalent (Zag allows any order). Anchor on the file tail.
if not p.endswith("\n"):
    p = p + "\n"
p = p + novelty_fns
open(OUT + "/ob_pam.zag", "w").write(p)
print("ob_pam.zag merged OK")
