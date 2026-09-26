#!/usr/bin/env python3
# merge_port.py — deterministic port of the F6 wedge-fix into the delete-strong mainline.
# Base: ~/workspace/strength-delete/strength_core.zag (post-holefix, S-D1..S-D5).
# Donor: ~/workspace/strength-f6-wedgefix/strength_core.zag (F6 fix, commits de7f59c91+20497b8f0).
# Every edit is an exact-anchor replacement; any missing anchor aborts loudly.
# Decisions are recorded in PORT_DECISIONS.md; this script records none itself.
import sys

BASE = "/home/hatch/workspace/strength-delete/strength_core.zag"
OUT = "/home/hatch/workspace/strength-port/strength_core.zag"

def need(hay, needle, tag):
    if hay.count(needle) != 1:
        print(f"ANCHOR FAIL [{tag}]: count={hay.count(needle)}")
        sys.exit(1)

src = open(BASE).read()
assert "cite_mode" not in src, "base already has cite_mode?!"
assert "ST_OP_CITELOCK" not in src, "base already has citelock?!"

# ---- E1: cite-lock op consts (renumbered: DELETE_STRONG=20 is live mainline law) ----
a = "const ST_OP_DELETE_STRONG:i32=20;\n"
need(src, a, "E1")
src = src.replace(a, a + """// PORT (2026-09-26, F6 wedge-fix D4/D2): cite-lock visibility signals.
// Audit-only, before==after, never mutate state, never change an op's rc.
// Renumbered from the F6 workstream's 20/21: ST_OP_DELETE_STRONG=20 is live
// mainline law, so existing ledgers keep their op numbering.
const ST_OP_CITELOCK:i32=21;      // slot-level: a 121-refused priced destruction hit a cite-locked slot
const ST_OP_CITELOCK_SYS:i32=22;  // system-level: every user slot is cite-locked
""", 1)

# ---- E2: cite-mode consts ----
a = "const ST_REFUSED_CONSUMED:i32=121;\n\nconst ST_STAGE_NONE:i32=0;"
need(src, a, "E2")
src = src.replace(a, """const ST_REFUSED_CONSUMED:i32=121;

// PORT (2026-09-26, F6 wedge-fix): cite-consumption modes. WINDOWED (0) is the
// default and implements the signed mainline law S-D2: per-slot,
// generation-scoped tombstoning — a cite that paid for a destruction stays
// spent for that slot across ADD reuse (this is NOT the F4b window reset the
// F6 workstream's W-mode tested; W is out per Micah's 2026-09-25 ruling).
// GLOBAL (1): F6 D4 — store-wide tombstone: a cite consumed by an OK priced
// destruction is consumed on any slot, forever. HYBRID (2): kept for source
// compatibility only — DISQUALIFIED by Micah's 2026-09-25 ruling ("slot reuse
// resurrecting spent cites" is a big issue); drivers must not select it.
const ST_CITE_WINDOWED:i32=0;
const ST_CITE_GLOBAL:i32=1;
const ST_CITE_HYBRID:i32=2;

const ST_STAGE_NONE:i32=0;""", 1)

# ---- E3: StStore.cite_mode field ----
a = """    p3k: i32,          // P3 expiry horizon K in episodes
    ep: i32            // current episode (set by learner; unaudited)
}"""
need(src, a, "E3")
src = src.replace(a, """    p3k: i32,          // P3 expiry horizon K in episodes
    ep: i32,           // current episode (set by learner; unaudited)
    cite_mode: i32     // PORT: ST_CITE_WINDOWED/GLOBAL/HYBRID (see above)
}""", 1)

# ---- E4: st_init default + st_set_cite_mode ----
a = """        .stage=ST_STAGE_NONE,.clock=0,.p3=0,.p3k=0,.ep=0};
}
fn st_free(s:*StStore)void {"""
need(src, a, "E4")
src = src.replace(a, """        .stage=ST_STAGE_NONE,.clock=0,.p3=0,.p3k=0,.ep=0,.cite_mode=ST_CITE_WINDOWED};
}
// PORT (2026-09-26, F6 wedge-fix): set the cite-consumption mode
// (WINDOWED=0 law default, GLOBAL=1, HYBRID=2 disqualified — see consts).
// Must be set before any ops; the checker reads it from the store.
fn st_set_cite_mode(s:*StStore,mode:i32)void {
    if(mode==ST_CITE_GLOBAL || mode==ST_CITE_HYBRID){s.*.cite_mode=mode;}
    else {s.*.cite_mode=ST_CITE_WINDOWED;}
}
fn st_free(s:*StStore)void {""", 1)

# ---- E5: st_last_add_idx + st_consume_lo + st_pay_lo (after st_last_strength_idx) ----
a = """fn st_last_strength_idx(s:*StStore,slot:i32,upto:i32)i32 {
    let i:i32=upto-1;
    while(i>=0){
        let op:i32=st_aw(s,i,0);
        if(st_aw(s,i,1)==slot && st_aw(s,i,4)==ST_OK){
            if(op==ST_OP_ADD || op==ST_OP_STRENGTHEN || op==ST_OP_WEAKEN ||
               op==ST_OP_TRAINER_DECLARE || op==ST_OP_OVERWRITE){return i;}
        }
        i=i-1;
    }
    return -1;
}
"""
need(src, a, "E5")
src = src.replace(a, a + """// Index of the most recent OK ADD for slot before `upto`; -1 if none.
// (PORT/F6: the ADD lineage bound — a genuinely new memory.)
fn st_last_add_idx(s:*StStore,slot:i32,upto:i32)i32 {
    let i:i32=upto-1;
    while(i>=0){
        if(st_aw(s,i,0)==ST_OP_ADD && st_aw(s,i,1)==slot && st_aw(s,i,4)==ST_OK){return i;}
        i=i-1;
    }
    return -1;
}
// PORT (2026-09-26): lower bound of the consumption scan for a check ending
// at `upto`.
// WINDOWED (mainline S-D2 law): -1 — the FULL ledger is scanned, so a cite
//   that paid for a destruction stays tombstoned across ADD slot reuse.
//   (Diverges from the F6 workstream's W-mode, which reset at after_idx per
//   the F4b window law — that law is superseded by S-D2; PORT_DECISIONS.md.)
// GLOBAL (F6 D4): -1 — store-wide tombstone: no reset, ever.
// HYBRID (disqualified; F6 semantics kept verbatim): last ADD.
fn st_consume_lo(s:*StStore,slot:i32,upto:i32,after_idx:i32)i32 {
    let mode:i32=s.*.cite_mode;
    if(mode==ST_CITE_GLOBAL){return -1;}
    if(mode==ST_CITE_HYBRID){return st_last_add_idx(s,slot,upto);}
    return -1;
}
// PORT (2026-09-26): lower bound of one destruction's payment set (which
// cites it consumed).
// WINDOWED (mainline law): last strength-set before the destruction — a cite
//   counts as paid iff cited in the destroyed judgment's own effort window.
// GLOBAL/HYBRID (F6 D4 semantics, verbatim): last ADD before the destruction
//   — a cite counts as paid only if cited during the destroyed memory's own
//   ADD lineage (cites for long-dead memories are not burned by later
//   destructions).
fn st_pay_lo(s:*StStore,slot:i32,d:i32)i32 {
    let mode:i32=s.*.cite_mode;
    if(mode==ST_CITE_GLOBAL || mode==ST_CITE_HYBRID){return st_last_add_idx(s,slot,d);}
    return st_last_strength_idx(s,slot,d);
}
""", 1)

# ---- E6: replace st_cite_consumed with the composed predicate ----
a = """// F4 FIX (F4b cite-consumption, 2026-09-25), HOLE-2 HARDENING (2026-09-26):
// a cite_ep is CONSUMED iff it sits in the effort window of an OK priced
// destruction (KILL, KILL_EVIDENCED, OVERWRITE, or DELETE_STRONG) on the
// same slot. Consumption records are bound to (slot, generation) and
// TOMBSTONED per generation: a cite that paid for a destruction on this
// slot stays spent for the slot across reuses — a new ADD starts a new
// judgment but never resurrects spent cites (signed S-D2: a citation
// episode pays for at most one destruction). The destruction scan therefore
// covers the FULL history (0, upto), not just the current effort window.
// Each candidate destruction's OWN window check (dlss_d, d) still decides
// whether THIS cite_ep paid for THAT destruction, so a weaken-detached cite
// (R1: strength-write starts a new window) is correctly NOT tombstoned —
// only genuinely-spent episodes are. Derived from the ledger itself: no new
// state, no new entries, so the checker recomputes the identical predicate.
fn st_cite_consumed(s:*StStore,slot:i32,cite_ep:i32,after_idx:i32,upto:i32)i32 {
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
}
"""
need(src, a, "E6")
src = src.replace(a, """// PORT (2026-09-26): F6 D4 (store-wide consumption) x mainline S-D2
// (per-slot generation-scoped tombstoning), composed. A cite_ep is CONSUMED
// iff it sits in the payment window of an OK priced destruction
// (KILL, KILL_EVIDENCED, OVERWRITE, or DELETE_STRONG — the mainline priced
// set; the F6 workstream predated the holefix and priced only KILL_EVIDENCED
// and OVERWRITE). WINDOWED: per-slot, full-history scan (S-D2: cites stay
// spent across ADD reuse; identical predicate to the pre-port mainline —
// the dslot==slot filter plus st_pay_lo's strength-set bound reproduce it
// exactly). GLOBAL: store-wide — the destruction may be on ANY slot, and
// each destruction's payment window is its own slot's ADD lineage (F6 D4
// semantics, verbatim). HYBRID: F6 semantics, disqualified (see consts).
// No double-counting (one destruction burns each episode once) and no
// resurrection (tombstones never clear). Derived from the ledger itself —
// no new state, no new entries — so the checker recomputes the identical
// predicate from its own copy of the ledger.
fn st_cite_consumed(s:*StStore,slot:i32,cite_ep:i32,after_idx:i32,upto:i32)i32 {
    // The scan bounds are mode-dependent (see st_consume_lo/st_pay_lo).
    let lo:i32=st_consume_lo(s,slot,upto,after_idx);
    let d:i32=lo+1;
    while(d<upto){
        let op:i32=st_aw(s,d,0);
        if((op==ST_OP_KILL || op==ST_OP_KILL_EVIDENCED || op==ST_OP_OVERWRITE ||
            op==ST_OP_DELETE_STRONG) && st_aw(s,d,4)==ST_OK){
            let dslot:i32=st_aw(s,d,1);
            if(dslot==slot || s.*.cite_mode==ST_CITE_GLOBAL){
                let plo:i32=st_pay_lo(s,dslot,d);
                let i:i32=plo+1;
                while(i<d){
                    if(st_aw(s,i,0)==ST_OP_EVIDENCE && st_aw(s,i,1)==dslot &&
                       st_aw(s,i,4)==ST_OK && st_aw(s,i,2)==cite_ep){return 1;}
                    i=i+1;
                }
            }
        }
        d=d+1;
    }
    return 0;
}
// PORT (2026-09-26, F6 wedge-fix): batched form of st_cite_consumed.
// Collects the DISTINCT cite_eps consumed in the query's scope (identical
// predicate, one O(destructions x window) pass) into out[0..cap) as
// little-endian i32s; returns the count stored. Lets callers that test many
// episodes (e.g. an honest driver's candidate scan) pay one pass instead of
// one per episode. Semantics are exactly st_cite_consumed per element.
fn st_consumed_list(s:*StStore,slot:i32,after_idx:i32,upto:i32,out:[]u8,cap:i32)i32 {
    let lo:i32=st_consume_lo(s,slot,upto,after_idx);
    let n:i32=0;
    let d:i32=lo+1;
    while(d<upto){
        let op:i32=st_aw(s,d,0);
        if((op==ST_OP_KILL || op==ST_OP_KILL_EVIDENCED || op==ST_OP_OVERWRITE ||
            op==ST_OP_DELETE_STRONG) && st_aw(s,d,4)==ST_OK){
            let dslot:i32=st_aw(s,d,1);
            if(dslot==slot || s.*.cite_mode==ST_CITE_GLOBAL){
                let plo:i32=st_pay_lo(s,dslot,d);
                let i:i32=plo+1;
                while(i<d){
                    if(st_aw(s,i,0)==ST_OP_EVIDENCE && st_aw(s,i,1)==dslot &&
                       st_aw(s,i,4)==ST_OK){
                        let ep:i32=st_aw(s,i,2);
                        let seen:i32=0;let q:i32=0;
                        while(q<n){if(st_i32_get(out,q*4)==ep){seen=1;break;}q=q+1;}
                        if(seen==0 && n<cap){st_i32_set(out,n*4,ep);n=n+1;}
                    }
                    i=i+1;
                }
            }
        }
        d=d+1;
    }
    return n;
}
""", 1)

# ---- E8: cite-lock signal fns before "// ---- ops ----" ----
a = """// ---- ops ----"""
need(src, a, "E8")
src = src.replace(a, """// ---- PORT (2026-09-26, F6 wedge-fix): cite-lock signals ----
// A slot is cite-locked iff it is live, holds a non-core judgment, has at
// least one distinct cited episode in its effort window (lss, upto), and
// every one of them is consumed. Under GLOBAL consumption is permanent, so
// a cite-locked slot cannot be destroyed through any priced path without
// genuinely fresh episodes: it is stuck, visibly. Pure ledger-derived; no
// new state. (In WINDOWED the S-D2 tombstone is per-slot but an ADD starts
// a new judgment on the slot, so the wedge signal is GLOBAL-only.)
fn st_slot_citelocked(s:*StStore,slot:i32,upto:i32)i32 {
    if(st_badslot(s,slot)==1){return 0;}
    if(s.*.live[slot]==0){return 0;}
    if(s.*.region[slot]==ST_REGION_CORE as u8){return 0;}
    let lss:i32=st_last_strength_idx(s,slot,upto);
    if(lss<0){return 0;}
    let buf:[]u8=nio_alloc(16);
    let total:i32=st_collect_cites(s,slot,lss,upto,buf);
    nio_free(buf);
    if(total<1){return 0;}
    let spent:i32=st_count_spent_cites(s,slot,lss,upto);
    if(spent==total){return 1;}
    return 0;
}
// Emit the cite-locked signal after a 121 refusal of a priced destruction
// on a cite-locked slot (GLOBAL mode only). Appends ST_OP_CITELOCK
// (rc=0, before==after: pure diagnosis, no state change, no cite
// consumption, no window movement), then ST_OP_CITELOCK_SYS when every
// user slot is cite-locked AND the all-locked state is new since the last
// system signal (transition-triggered; the ledger scan below dedupes so a
// stuck store emits exactly one system signal per wedge episode). Never
// changes the op's rc. Fail-silent when the ledger is full.
fn st_citelock_signal(s:*StStore,slot:i32)void {
    if(s.*.cite_mode!=ST_CITE_GLOBAL){return;}
    if(st_audit_room(s)==0){return;}
    let upto:i32=s.*.audit_n;
    if(st_slot_citelocked(s,slot,upto)==0){return;}
    let b1:i32=0;let b2:i32=0;let b3:i32=0;let b4:i32=0;let b5:i32=0;let b6:i32=0;
    st_snap(s,slot,&b1,&b2,&b3,&b4,&b5,&b6);
    let lss0:i32=st_last_strength_idx(s,slot,upto);
    let buf:[]u8=nio_alloc(16);
    let total:i32=st_collect_cites(s,slot,lss0,upto,buf);
    nio_free(buf);
    let spent:i32=st_count_spent_cites(s,slot,lss0,upto);
    st_audit_append(s,ST_OP_CITELOCK,slot,total,spent,ST_OK,
        b1,b2,b3,b4,b5,b6,b1,b2,b3,b4,b5,b6,ST_ROLE_SYSTEM,0);
    // system-level: all user slots cite-locked and no free slot?
    let locked_n:i32=0;let liveuser_n:i32=0;let all:i32=1;
    let sl:i32=0;
    while(sl<s.*.slot_cap){
        if(s.*.live[sl]==1 && s.*.region[sl]==ST_REGION_USER as u8){
            liveuser_n=liveuser_n+1;
            if(st_slot_citelocked(s,sl,upto)==1){locked_n=locked_n+1;}
            else {all=0;}
        } else if(s.*.live[sl]==0){
            all=0;
        }
        sl=sl+1;
    }
    if(all==0 || liveuser_n==0){return;}
    // transition dedupe: emit only if no system signal exists yet, or a
    // state/window-changing OK entry on a real slot landed after the last
    // one (lock membership may have changed since). Pure spam filter: the
    // all-locked predicate above is always recomputed fresh.
    let sys_i:i32=-1;
    let j:i32=upto-1;
    while(j>=0){
        if(st_aw(s,j,0)==ST_OP_CITELOCK_SYS && st_aw(s,j,4)==ST_OK){sys_i=j;break;}
        j=j-1;
    }
    let changed:i32=0;
    if(sys_i<0){changed=1;}
    else {
        let k:i32=sys_i+1;
        while(k<upto){
            let kop:i32=st_aw(s,k,0);
            if(st_aw(s,k,4)==ST_OK && st_aw(s,k,1)>=0 &&
               kop!=ST_OP_CITELOCK && kop!=ST_OP_CITELOCK_SYS &&
               kop!=ST_OP_EVIDENCE && kop!=ST_OP_JUSTIFY &&
               kop!=ST_OP_PEXPIRED && kop!=ST_OP_ABANDON){changed=1;break;}
            k=k+1;
        }
    }
    if(changed==0){return;}
    st_audit_append(s,ST_OP_CITELOCK_SYS,-1,locked_n,liveuser_n,ST_OK,
        0,0,0,0,0,0,0,0,0,0,0,0,ST_ROLE_SYSTEM,0);
}

// ---- ops ----""", 1)

# ---- E9a: signal wiring in st_kill (trainer-priced path; TNN path returns 113 first) ----
a = """    let arc:i32=st_audit_append(s,ST_OP_KILL,slot,-1,-1,rc,
        b1,b2,b3,b4,b5,b6,a1,a2,a3,a4,a5,a6,role,trainer);
    if(arc!=ST_OK){return arc;}
    return rc;
}"""
need(src, a, "E9a")
src = src.replace(a, """    let arc:i32=st_audit_append(s,ST_OP_KILL,slot,-1,-1,rc,
        b1,b2,b3,b4,b5,b6,a1,a2,a3,a4,a5,a6,role,trainer);
    if(arc!=ST_OK){return arc;}
    // PORT (2026-09-26, F6 wedge-fix): cite-lock visibility for the trainer
    // priced-kill path. GLOBAL only; audited; never changes rc. (TNN-role
    // calls return 113 above, before any effort check.)
    if(rc==ST_REFUSED_CONSUMED){st_citelock_signal(s,slot);}
    return rc;
}""", 1)

# ---- E9b: signal wiring in st_kill_evidenced ----
a = """    let arc:i32=st_audit_append(s,ST_OP_KILL_EVIDENCED,slot,-1,-1,rc,
        b1,b2,b3,b4,b5,b6,a1,a2,a3,a4,a5,a6,ST_ROLE_TNN,0);
    if(arc!=ST_OK){return arc;}
    return rc;
}"""
need(src, a, "E9b")
src = src.replace(a, """    let arc:i32=st_audit_append(s,ST_OP_KILL_EVIDENCED,slot,-1,-1,rc,
        b1,b2,b3,b4,b5,b6,a1,a2,a3,a4,a5,a6,ST_ROLE_TNN,0);
    if(arc!=ST_OK){return arc;}
    // PORT (2026-09-26, F6 wedge-fix): cite-lock visibility. GLOBAL only;
    // audited; never changes rc.
    if(rc==ST_REFUSED_CONSUMED){st_citelock_signal(s,slot);}
    return rc;
}""", 1)

# ---- E9c: signal wiring in st_delete_strong ----
a = """    let arc:i32=st_audit_append(s,ST_OP_DELETE_STRONG,slot,-1,-1,rc,
        b1,b2,b3,b4,b5,b6,a1,a2,a3,a4,a5,a6,ST_ROLE_TNN,0);
    if(arc!=ST_OK){return arc;}
    return rc;
}"""
need(src, a, "E9c")
src = src.replace(a, """    let arc:i32=st_audit_append(s,ST_OP_DELETE_STRONG,slot,-1,-1,rc,
        b1,b2,b3,b4,b5,b6,a1,a2,a3,a4,a5,a6,ST_ROLE_TNN,0);
    if(arc!=ST_OK){return arc;}
    // PORT (2026-09-26, F6 wedge-fix): cite-lock visibility for the one-step
    // delete path. GLOBAL only; audited; never changes rc.
    if(rc==ST_REFUSED_CONSUMED){st_citelock_signal(s,slot);}
    return rc;
}""", 1)

# ---- E9d: signal wiring in st_overwrite ----
a = """    let arc:i32=st_audit_append(s,ST_OP_OVERWRITE,slot,aux_ep,-1,rc,
        b1,b2,b3,b4,b5,b6,a1,a2,a3,a4,a5,a6,ST_ROLE_TNN,0);
    if(arc!=ST_OK){return arc;}
    return rc;
}"""
need(src, a, "E9d")
src = src.replace(a, """    let arc:i32=st_audit_append(s,ST_OP_OVERWRITE,slot,aux_ep,-1,rc,
        b1,b2,b3,b4,b5,b6,a1,a2,a3,a4,a5,a6,ST_ROLE_TNN,0);
    if(arc!=ST_OK){return arc;}
    // PORT (2026-09-26, F6 wedge-fix): cite-lock visibility. GLOBAL only;
    // audited; never changes rc.
    if(rc==ST_REFUSED_CONSUMED){st_citelock_signal(s,slot);}
    return rc;
}""", 1)

# ---- E10: replay copies cite_mode ----
a = """fn st_replay_check(s:*StStore)i32 {
    let sh:StStore=st_init(s.*.slot_cap,16);
"""
need(src, a, "E10")
src = src.replace(a, """fn st_replay_check(s:*StStore)i32 {
    let sh:StStore=st_init(s.*.slot_cap,16);
    sh.cite_mode=s.*.cite_mode;
""", 1)

open(OUT, "w").write(src)
print("core port OK ->", OUT)
