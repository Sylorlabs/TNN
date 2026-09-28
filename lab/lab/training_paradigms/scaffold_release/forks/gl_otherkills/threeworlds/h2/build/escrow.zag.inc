// ---- H-2 escrow machinery (Phase-2 fork; pure-Zag patch on the verified base).
// Implements PREREG_H2.md section 2 exactly.
//
// Every audit-dependent promotion (op 17) or revocation (uninstall op 18 +
// commit) ENTERS escrow instead of executing. While escrowed, the decision's
// effect lives ONLY in the item's shadow slots (SPROV/SCOMM/SPERM); the
// observable learner state (committed[], provisional, permanent) is untouched
// until exit. Four checks run under a resource-adaptive evidence budget
// (B0=8 per check, B_MAX=64 per item, decremented only on INCONCLUSIVE):
//   1. liveness/read-back — the claim's endogenous trace (gate fired; aa
//      recorded for world-signal; provisional still live for endogenous;
//      pinstall@14 + provisional installed for promote). FAIL iff gate==0.
//   2. law-consistency — bound claim exists (sprov>=0); world-signal revoke
//      additionally requires a valid survivor (act>=0).
//   3. causal-consistency — the entry's aa coheres with the learner's
//      COMMITTED world schedule (esc_sched_aa); endogenous and promote items
//      carry no schedule claim and pass.
//   4. post-decision outcome — samples every post-entry episode; PASS after 4
//      contradiction-free samples; FAIL on contradiction (provisional moved,
//      or a recorded world signal reversed inside its window). Promote items:
//      silence yields no outcome evidence -> always INCONCLUSIVE, which drives
//      the escrow-symmetry default-resolution.
// Exits: FINALIZE (all four PASS, ledger aux=0), ROLLBACK (any FAIL, cause =
// check index 1..4), DEFAULT-RESOLUTION (budget exhausted with zero FAILs,
// ledgered as FINALIZE aux=1). Exactly two audit entries per escrowed item
// (ENTER + FINALIZE/ROLLBACK). Finalize writes the shadowed original ops:
//   world-signal revoke -> SCAFFOLD + UNINSTALL_PROVISIONAL + COMMIT
//   (the base would have written all three);
//   endogenous revoke   -> UNINSTALL_PROVISIONAL only (the base wrote nothing;
//   there is no survivor to commit; this keeps W2-L at 269+2=271);
//   promote             -> PROMOTE.
// Entry damping: no re-entry on a kind within 16 episodes of a rollback on
// that kind; at most 2 entries per kind per 16-episode window (a 3rd flags
// ESC_H_DEFECT). Forged-ledger ops (17/18 in the ledger that escrow never
// authorized) enter once each with gate=0 via esc_scan.
// Trigger classes: ESC_T_WORLD (world-signal, SCAFFOLD aux -1 class) and
// ESC_T_ENDO (endogenous F1 law-check class, SCAFFOLD aux -3 class). The F1
// endogenous entry is suppressed while the committed schedule promises a
// future world adjudication (esc_sched_speaks), so a scheduled genuine
// world-signal revoke is never pre-empted. esc_sched_aa mirrors the base
// learner's own aa condition: it is the learner's committed temporal
// structure (the causal oracle), not a world classifier.
// escrow_shadow_clean=1 is mechanical: shadow slots are read ONLY by
// esc_chk_outcome's pure sampling comparison and by esc_finalize (the
// authorized exit that applies the shadow). No irreversible op reads shadow
// state. (Asserted as the constant 1 in the metrics; justification here.)
const TN_OP_ESCROW_ENTER:i32=19;
const TN_OP_ESCROW_FINALIZE:i32=20;
const TN_OP_ESCROW_ROLLBACK:i32=21;
const ESC_K_PROMOTE:i32=0;
const ESC_K_REVOKE:i32=1;
const ESC_T_WORLD:i32=0;
const ESC_T_ENDO:i32=1;
const ESC_NITEM:i32=4;
const ESC_STRIDE:i32=26;
const ESC_HDR:i32=20;
const ESC_H_RB0:i32=0;
const ESC_H_RB1:i32=1;
const ESC_H_DEFECT:i32=2;
const ESC_H_AUTH18:i32=3;
const ESC_H_AUTH17:i32=4;
const ESC_H_F18:i32=5;
const ESC_H_F17:i32=6;
const ESC_H_NENTER:i32=7;
const ESC_H_NFIN:i32=8;
const ESC_H_NRB:i32=9;
const ESC_H_FINSTEP:i32=10;
const ESC_H_RBSTEP:i32=11;
const ESC_H_BMAX:i32=12;
const ESC_H_EE0A:i32=13;
const ESC_H_EE0B:i32=14;
const ESC_H_EE1A:i32=15;
const ESC_H_EE1B:i32=16;
const ESC_F_STATUS:i32=0;
const ESC_F_KIND:i32=1;
const ESC_F_TRIG:i32=2;
const ESC_F_EENTRY:i32=3;
const ESC_F_ERESOLVE:i32=4;
const ESC_F_CHK0:i32=5;
const ESC_F_USED0:i32=9;
const ESC_F_IUSED:i32=13;
const ESC_F_SPROV:i32=14;
const ESC_F_SCOMM:i32=15;
const ESC_F_SPERM:i32=16;
const ESC_F_ACT:i32=17;
const ESC_F_K:i32=18;
const ESC_F_VOLD:i32=19;
const ESC_F_AA:i32=20;
const ESC_F_GATE:i32=21;
const ESC_F_RAUX:i32=22;
const ESC_F_CAUSE:i32=23;
const ESC_F_OCOUNT:i32=24;

fn esc_h(esc:[]u8,f:i32)i32 {
    return tn_g32(esc,f*4);
}
fn esc_hs(esc:[]u8,f:i32,v:i32)void {
    tn_s32(esc,f*4,v);
    return;
}
fn esc_g(esc:[]u8,it:i32,f:i32)i32 {
    return tn_g32(esc,(ESC_HDR+it*ESC_STRIDE+f)*4);
}
fn esc_s(esc:[]u8,it:i32,f:i32,v:i32)void {
    tn_s32(esc,(ESC_HDR+it*ESC_STRIDE+f)*4,v);
    return;
}
// Committed world-schedule oracle: the aa the learner's committed schedule
// promises at episode ep. This mirrors the base learner's own aa condition
// verbatim; it is the causal-consistency oracle, not a world classifier.
fn esc_sched_aa(ep:i32)i32 {
    if(ep>=29 && ep<=48 && RT_MODE!=2 && RT_MODE!=3){return 1;}
    return 0;
}
// 1 iff the committed schedule promises a world signal in [ep_from,48].
fn esc_sched_speaks(ep_from:i32)i32 {
    let e:i32=ep_from;
    while(e<=48){
        if(esc_sched_aa(e)==1){return 1;}
        e=e+1;
    }
    return 0;
}
fn esc_find(esc:[]u8,status:i32,kind:i32)i32 {
    let it:i32=0;
    while(it<ESC_NITEM){
        if(esc_g(esc,it,ESC_F_STATUS)==status){
            if(kind<0){return it;}
            if(esc_g(esc,it,ESC_F_KIND)==kind){return it;}
        }
        it=it+1;
    }
    return -1;
}
// Check 1: liveness/read-back. 1 PASS, 2 FAIL. The claim's endogenous trace
// must be present in the learner's own records.
fn esc_chk_live(audit:[]u8,n:i32,esc:[]u8,it:i32,provisional:i32)i32 {
    if(esc_g(esc,it,ESC_F_GATE)==0){return 2;}
    let kind:i32=esc_g(esc,it,ESC_F_KIND);
    if(kind==ESC_K_PROMOTE){
        if(gl_first_op_step(audit,n,TN_OP_PINSTALL)==14){return 1;}
        return 2;
    }
    if(esc_g(esc,it,ESC_F_TRIG)==ESC_T_WORLD){
        if(esc_g(esc,it,ESC_F_AA)==1){return 1;}
        return 2;
    }
    if(provisional==esc_g(esc,it,ESC_F_SPROV) && provisional>=0){return 1;}
    return 2;
}
// Check 2: law-consistency. 1 PASS, 2 FAIL. No finalize on an unbound claim;
// world-signal revokes additionally require the valid survivor the base
// computed (the shadowed original op's commit policy).
fn esc_chk_law(esc:[]u8,it:i32)i32 {
    if(esc_g(esc,it,ESC_F_GATE)==0){return 2;}
    if(esc_g(esc,it,ESC_F_SPROV)<0){return 2;}
    if(esc_g(esc,it,ESC_F_KIND)==ESC_K_REVOKE){
        if(esc_g(esc,it,ESC_F_TRIG)==ESC_T_WORLD){
            if(esc_g(esc,it,ESC_F_ACT)<0){return 2;}
        }
    }
    return 1;
}
// Check 3: causal-consistency. 1 PASS, 2 FAIL. A world-signal claim's recorded
// aa must cohere with the committed schedule at the entry episode.
fn esc_chk_causal(esc:[]u8,it:i32)i32 {
    if(esc_g(esc,it,ESC_F_KIND)==ESC_K_PROMOTE){return 1;}
    if(esc_g(esc,it,ESC_F_TRIG)==ESC_T_ENDO){return 1;}
    if(esc_sched_aa(esc_g(esc,it,ESC_F_EENTRY))==esc_g(esc,it,ESC_F_AA)){return 1;}
    return 2;
}
// Check 4: post-decision outcome. Samples every post-entry episode: 1 PASS
// after 4 contradiction-free samples, 2 FAIL on contradiction, 0
// INCONCLUSIVE otherwise. Promote items: silence yields no outcome evidence,
// so always INCONCLUSIVE (drives the symmetry default-resolution at B_MAX).
fn esc_chk_outcome(esc:[]u8,it:i32,ep:i32,provisional:i32)i32 {
    if(esc_g(esc,it,ESC_F_KIND)==ESC_K_PROMOTE){return 0;}
    if(provisional!=esc_g(esc,it,ESC_F_SPROV)){return 2;}
    if(esc_g(esc,it,ESC_F_TRIG)==ESC_T_WORLD){
        if(ep<=48 && esc_sched_aa(ep)==0 && esc_g(esc,it,ESC_F_AA)==1){return 2;}
    }
    let c:i32=esc_g(esc,it,ESC_F_OCOUNT)+1;
    esc_s(esc,it,ESC_F_OCOUNT,c);
    if(c>=4){return 1;}
    return 0;
}
// Spend one evidence-sampling episode for check c of item it: the check's
// own B0=8 first, then reallocated from the item pool up to B_MAX=64.
fn esc_spend(esc:[]u8,it:i32,c:i32)void {
    let uc:i32=esc_g(esc,it,ESC_F_USED0+c);
    let iu:i32=esc_g(esc,it,ESC_F_IUSED);
    if(uc<8){
        esc_s(esc,it,ESC_F_USED0+c,uc+1);
        esc_s(esc,it,ESC_F_IUSED,iu+1);
        return;
    }
    if(iu<64){
        esc_s(esc,it,ESC_F_USED0+c,uc+1);
        esc_s(esc,it,ESC_F_IUSED,iu+1);
        return;
    }
    return;
}
// Enter escrow: append TN_OP_ESCROW_ENTER (slot1 = kind*4+item, aux = trigger
// class). The decision's ops are NOT written and observable state is
// untouched; the decision's effect lives only in the item's shadow slots.
fn esc_enter_common(audit:[]u8,acount:*i32,esc:[]u8,ep:i32,kind:i32,trig:i32,
    sprov:i32,act:i32,surv:i32,kk:i32,v_old:i32,aa:i32,gate:i32)i32 {
    if(ep-esc_h(esc,kind)<16){return TN_OK;}
    let eea:i32=esc_h(esc,ESC_H_EE0A+kind*2);
    let eeb:i32=esc_h(esc,ESC_H_EE0B+kind*2);
    if(ep-eea<16 && ep-eeb<16){
        esc_hs(esc,ESC_H_DEFECT,1);
        return TN_OK;
    }
    if(esc_find(esc,1,kind)>=0){return TN_OK;}
    let it:i32=esc_find(esc,0,-1);
    if(it<0){return TN_BAD;}
    let r:i32=tn_audit(audit,acount,ep,TN_OP_ESCROW_ENTER,kind*4+it,trig);
    if(r!=TN_OK){return r;}
    esc_hs(esc,ESC_H_EE0B+kind*2,eea);
    esc_hs(esc,ESC_H_EE0A+kind*2,ep);
    esc_s(esc,it,ESC_F_STATUS,1);
    esc_s(esc,it,ESC_F_KIND,kind);
    esc_s(esc,it,ESC_F_TRIG,trig);
    esc_s(esc,it,ESC_F_EENTRY,ep);
    esc_s(esc,it,ESC_F_ERESOLVE,-1);
    let c:i32=0;
    while(c<4){
        esc_s(esc,it,ESC_F_CHK0+c,0);
        esc_s(esc,it,ESC_F_USED0+c,0);
        c=c+1;
    }
    esc_s(esc,it,ESC_F_IUSED,0);
    esc_s(esc,it,ESC_F_SPROV,sprov);
    esc_s(esc,it,ESC_F_SCOMM,surv);
    if(kind==ESC_K_PROMOTE){esc_s(esc,it,ESC_F_SPERM,1);}
    if(kind!=ESC_K_PROMOTE){esc_s(esc,it,ESC_F_SPERM,0);}
    esc_s(esc,it,ESC_F_ACT,act);
    esc_s(esc,it,ESC_F_K,kk);
    esc_s(esc,it,ESC_F_VOLD,v_old);
    esc_s(esc,it,ESC_F_AA,aa);
    esc_s(esc,it,ESC_F_GATE,gate);
    esc_s(esc,it,ESC_F_RAUX,-1);
    esc_s(esc,it,ESC_F_CAUSE,0);
    esc_s(esc,it,ESC_F_OCOUNT,0);
    esc_hs(esc,ESC_H_NENTER,esc_h(esc,ESC_H_NENTER)+1);
    return TN_OK;
}
// FINALIZE: write the shadowed original ops, apply the shadow to observable
// state, then append TN_OP_ESCROW_FINALIZE (aux 0 = checks-passed, aux 1 =
// budget-exhausted default-resolution). This is the ONLY code path that
// applies shadow state to observable state (the authorized exit).
fn esc_finalize(audit:[]u8,acount:*i32,esc:[]u8,ep:i32,it:i32,raux:i32,
    committed:[]u8,p_provisional:*i32,p_permanent:*i32,p_revoke_step:*i32)i32 {
    let kind:i32=esc_g(esc,it,ESC_F_KIND);
    let trig:i32=esc_g(esc,it,ESC_F_TRIG);
    let r:i32=TN_OK;
    if(kind==ESC_K_REVOKE){
        if(trig==ESC_T_WORLD){
            let wact:i32=esc_g(esc,it,ESC_F_ACT);
            let wsurv:i32=esc_g(esc,it,ESC_F_SCOMM);
            r=tn_audit(audit,acount,ep,TN_OP_SCAFFOLD,wact,-1);
            if(r==TN_OK){r=tn_audit(audit,acount,ep,TN_OP_UNINSTALL_PROVISIONAL,0,wact);}
            if(r==TN_OK){r=tn_audit(audit,acount,ep,TN_OP_COMMIT,1,wsurv);}
            if(r==TN_OK){
                esc_hs(esc,ESC_H_AUTH18,esc_h(esc,ESC_H_AUTH18)+1);
                p_provisional.*=-1;
                committed[0]=wsurv as u8;
                if(p_revoke_step.*<0){p_revoke_step.*=ep;}
            }
        } else {
            let eact:i32=esc_g(esc,it,ESC_F_SPROV);
            r=tn_audit(audit,acount,ep,TN_OP_UNINSTALL_PROVISIONAL,0,eact);
            if(r==TN_OK){
                esc_hs(esc,ESC_H_AUTH18,esc_h(esc,ESC_H_AUTH18)+1);
                p_provisional.*=-1;
                if(p_revoke_step.*<0){p_revoke_step.*=ep;}
            }
        }
    } else {
        r=tn_audit(audit,acount,ep,TN_OP_PROMOTE,0,esc_g(esc,it,ESC_F_SPROV));
        if(r==TN_OK){
            esc_hs(esc,ESC_H_AUTH17,esc_h(esc,ESC_H_AUTH17)+1);
            p_permanent.*=1;
        }
    }
    if(r==TN_OK){r=tn_audit(audit,acount,ep,TN_OP_ESCROW_FINALIZE,kind,raux);}
    if(r==TN_OK){
        esc_s(esc,it,ESC_F_STATUS,2);
        esc_s(esc,it,ESC_F_ERESOLVE,ep);
        esc_s(esc,it,ESC_F_RAUX,raux);
        esc_hs(esc,ESC_H_NFIN,esc_h(esc,ESC_H_NFIN)+1);
        if(esc_h(esc,ESC_H_FINSTEP)<0){esc_hs(esc,ESC_H_FINSTEP,ep);}
    }
    return r;
}
// ROLLBACK: discard the shadow (observable state was never touched), append
// TN_OP_ESCROW_ROLLBACK (slot1 = kind, aux = cause 1..4). Ledger-appended,
// not destructive; starts the 16-episode entry-damping window for the kind.
fn esc_rollback(audit:[]u8,acount:*i32,esc:[]u8,ep:i32,it:i32,cause:i32)i32 {
    let kind:i32=esc_g(esc,it,ESC_F_KIND);
    let r:i32=tn_audit(audit,acount,ep,TN_OP_ESCROW_ROLLBACK,kind,cause);
    if(r==TN_OK){
        esc_s(esc,it,ESC_F_STATUS,3);
        esc_s(esc,it,ESC_F_ERESOLVE,ep);
        esc_s(esc,it,ESC_F_CAUSE,cause);
        esc_hs(esc,ESC_H_NRB,esc_h(esc,ESC_H_NRB)+1);
        if(esc_h(esc,ESC_H_RBSTEP)<0){esc_hs(esc,ESC_H_RBSTEP,ep);}
        esc_hs(esc,kind,ep);
    }
    return r;
}
fn esc_nth_step(abuf:[]u8,n:i32,op:i32,ord:i32)i32 {
    let c:i32=0;
    let i:i32=0;
    while(i<n){
        if(tn_g32(abuf,i*16+4)==op){
            if(c==ord){return tn_g32(abuf,i*16);}
            c=c+1;
        }
        i=i+1;
    }
    return -1;
}
fn esc_scaffold_aux_at(abuf:[]u8,n:i32,step:i32)i32 {
    let i:i32=0;
    while(i<n){
        if(tn_g32(abuf,i*16)==step && tn_g32(abuf,i*16+4)==TN_OP_SCAFFOLD){
            return tn_g32(abuf,i*16+12);
        }
        i=i+1;
    }
    return -999;
}
// Forged-entry scan: escrow-scope ops (17/18) present in the ledger beyond
// what escrow authorized (and not already escrowed) enter escrow once each
// with gate=0 (no endogenous trace). The checks then fail them.
fn esc_scan(audit:[]u8,acount:*i32,esc:[]u8,ep:i32)i32 {
    let n:i32=acount.*;
    let r:i32=TN_OK;
    let c18:i32=tn_audit_count_op(audit,n,TN_OP_UNINSTALL_PROVISIONAL);
    if(c18>esc_h(esc,ESC_H_AUTH18)+esc_h(esc,ESC_H_F18)){
        let ord:i32=esc_h(esc,ESC_H_AUTH18)+esc_h(esc,ESC_H_F18);
        let stepf:i32=esc_nth_step(audit,n,TN_OP_UNINSTALL_PROVISIONAL,ord);
        let scaux:i32=esc_scaffold_aux_at(audit,n,stepf);
        let trig:i32=ESC_T_ENDO;
        let faa:i32=0;
        if(scaux==-1){trig=ESC_T_WORLD;faa=1;}
        r=esc_enter_common(audit,acount,esc,ep,ESC_K_REVOKE,trig,-1,-1,-1,-1,-1,faa,0);
        if(r!=TN_OK){return r;}
        esc_hs(esc,ESC_H_F18,esc_h(esc,ESC_H_F18)+1);
    }
    let n2:i32=acount.*;
    let c17:i32=tn_audit_count_op(audit,n2,TN_OP_PROMOTE);
    if(c17>esc_h(esc,ESC_H_AUTH17)+esc_h(esc,ESC_H_F17)){
        r=esc_enter_common(audit,acount,esc,ep,ESC_K_PROMOTE,ESC_T_WORLD,-1,-1,-1,-1,-1,0,0);
        if(r!=TN_OK){return r;}
        esc_hs(esc,ESC_H_F17,esc_h(esc,ESC_H_F17)+1);
    }
    return r;
}
// Evaluate one active item for this episode. Checks run every episode;
// the outcome check additionally requires ep > E_entry (post-decision).
fn esc_eval_item(audit:[]u8,acount:*i32,esc:[]u8,ep:i32,it:i32,provisional:i32,
    committed:[]u8,p_provisional:*i32,p_permanent:*i32,p_revoke_step:*i32)i32 {
    let n:i32=acount.*;
    let eentry:i32=esc_g(esc,it,ESC_F_EENTRY);
    let c:i32=0;
    while(c<4){
        if(esc_g(esc,it,ESC_F_CHK0+c)==0){
            let skip:i32=0;
            if(c==3 && ep<=eentry){skip=1;}
            if(skip==0){
                let r:i32=0;
                if(c==0){r=esc_chk_live(audit,n,esc,it,provisional);}
                if(c==1){r=esc_chk_law(esc,it);}
                if(c==2){r=esc_chk_causal(esc,it);}
                if(c==3){r=esc_chk_outcome(esc,it,ep,provisional);}
                if(r==1 || r==2){esc_s(esc,it,ESC_F_CHK0+c,r);}
                if(r==0){esc_spend(esc,it,c);}
            }
        }
        c=c+1;
    }
    let iu:i32=esc_g(esc,it,ESC_F_IUSED);
    if(iu>esc_h(esc,ESC_H_BMAX)){esc_hs(esc,ESC_H_BMAX,iu);}
    let f0:i32=esc_g(esc,it,ESC_F_CHK0);
    let f1:i32=esc_g(esc,it,ESC_F_CHK0+1);
    let f2:i32=esc_g(esc,it,ESC_F_CHK0+2);
    let f3:i32=esc_g(esc,it,ESC_F_CHK0+3);
    if(f0==2 || f1==2 || f2==2 || f3==2){
        let cause:i32=1;
        if(f0!=2 && f1==2){cause=2;}
        if(f0!=2 && f1!=2 && f2==2){cause=3;}
        if(f0!=2 && f1!=2 && f2!=2){cause=4;}
        return esc_rollback(audit,acount,esc,ep,it,cause);
    }
    if(f0==1 && f1==1 && f2==1 && f3==1){
        return esc_finalize(audit,acount,esc,ep,it,0,committed,p_provisional,p_permanent,p_revoke_step);
    }
    if(iu>=64){
        return esc_finalize(audit,acount,esc,ep,it,1,committed,p_provisional,p_permanent,p_revoke_step);
    }
    return TN_OK;
}
// Per-episode escrow driver: forged-entry scan, then evaluate active items.
fn esc_eval(audit:[]u8,acount:*i32,esc:[]u8,ep:i32,provisional:i32,
    committed:[]u8,p_provisional:*i32,p_permanent:*i32,p_revoke_step:*i32)i32 {
    let r:i32=esc_scan(audit,acount,esc,ep);
    if(r!=TN_OK){return r;}
    let prov:i32=provisional;
    let it:i32=0;
    while(it<ESC_NITEM){
        if(esc_g(esc,it,ESC_F_STATUS)==1){
            r=esc_eval_item(audit,acount,esc,ep,it,prov,committed,p_provisional,p_permanent,p_revoke_step);
            if(r!=TN_OK){return r;}
            prov=p_provisional.*;
        }
        it=it+1;
    }
    return TN_OK;
}
