#!/usr/bin/awk -f
# check_mrc.awk — SEPARATE evaluator for the MESSY-REALITY pilot.
# Reads ONLY the transcript's G lines. Re-implements the frozen §2.3 schedule
# in awk, recomputes whash, grades behavior against the demand tables (§3),
# and emits per-cell + overall verdicts. Fails loudly on any divergence.
# Usage: awk -f check_mrc.awk <transcript>
# G format: G,arm,e,class,stage,clean,subtype,whash,f0..f7,o0..o7

BEGIN {
    FS=",";
    n_g=0; errors=0;
    # per-arm aggregates: key = arm SUBSEP cls SUBSEP stage
    # overall: key = arm
}

function sched(e) {
    g_c=int(int(e/900)%5); g_s=int(int(e/300)%3); g_k=e%300;
    g_clean=(g_k%10==9)?1:0; g_m=g_k-int(g_k/10); g_u=g_m%4;
}

function world(e,  c,s,k,clean,m,u,r,r1,r2,j) {
    sched(e);
    c=g_c; s=g_s; k=g_k; clean=g_clean; m=g_m; u=g_u;
    w_cls=c; w_stage=s; w_clean=clean; w_subtype=u;
    w_ca=0; w_cb=0; w_kas=0; w_kbs=0; w_noisy=0; w_naa=0; w_nab=0;
    w_ch=0; w_streak=0; w_corrob=0; w_obs=0;
    w_p=0; w_prov=1; w_whole=0; w_mask=0;
    w_l0=0; w_l1=0; w_l2=0; w_pat=0; w_perf=0;
    w_ndef=0; w_viols=0; w_confirm=0; w_pin0=0; w_spoof=0;
    # negative control: harness reports stage/clean/subtype = 0 (early return
    # in world_build); only class=9 and spoof=1 are set.
    if (e>=4500) { w_cls=9; w_stage=0; w_clean=0; w_subtype=0; w_spoof=1; return; }
    if (c==0) {
        if (s==0) { w_ca=1; w_cb=1; }
        else if (s==1) { w_ca=0; w_cb=1; }
        else { w_ca=3; w_cb=3; }
        if (u==1||u==2) w_kas=3;
        if (u==0||u==2) w_kbs=3;
        if (int(m/4)%3==2) w_noisy=1;
        if (u==0) { w_naa=4; w_nab=14; }
        else if (u==1) { w_naa=14; w_nab=4; }
        else if (u==2) { w_naa=10; w_nab=10; }
        else { w_naa=4; w_nab=4; }
    } else if (c==1) {
        if (clean==0) {
            if (s==0) { w_streak=5+(m%3); w_ch=1; }
            else if (s==1) { w_streak=5+(m%2); w_ch=2; }
            else { w_streak=3+(m%2); w_ch=0; }
            w_obs=1; w_corrob=1;
            if (u==1) w_corrob=2;
        }
    } else if (c==2) {
        if (clean==1) { w_p=8; w_whole=0; w_prov=1; }
        else {
            if (s==0) w_p=3+(m%6);
            else if (s==1) { w_p=4+(m%4); w_prov=0; }
            else { w_whole=1; w_p=0; w_prov=0; }
            if ((u==1||u==3) && w_p>4) w_p=4;
        }
        for (j=0;j<w_p;j++) w_mask+=(2^j);
    } else if (c==3) {
        if (clean==0) {
            if (s==0 && u==0) {
                r=m%3;
                if (r==0) w_l0=1; else if (r==1) w_l1=1; else w_l2=1;
                w_pat=1;
            } else if (s==1 && u==0) {
                r1=m%3; r2=(m+1)%3;
                if (r1==0||r2==0) w_l0=1;
                if (r1==1||r2==1) w_l1=1;
                if (r1==2||r2==2) w_l2=1;
                w_pat=1;
            } else if (s==2 && u==0) {
                r=m%3;
                if (r==0) w_l0=1; else if (r==1) w_l1=1; else w_l2=1;
                w_perf=1;
            }
        }
    } else if (c==4) {
        if (clean==0) {
            if (s==0) w_ndef=2+(m%2);
            else if (s==1) w_ndef=4+(m%2);
            else w_ndef=3;
            if (u==3) { w_viols=6+(m%3); w_confirm=0; }
            else { w_viols=8+(m%5); w_confirm=1; }
            if (s==2) w_pin0=1;
        }
    }
}

function whash(  h) {
    h=w_cls+w_stage*7+w_subtype*13+w_clean*17;
    h+=w_kas*101+w_kbs*1009+w_noisy*1013+w_ca*1031+w_cb*1033+w_naa*1039+w_nab*1049;
    h+=w_ch*1061+w_streak*1063+w_corrob*1069+w_obs*1087;
    h+=w_p*1091+w_prov*1097+w_whole*1103+w_mask*1109;
    h+=w_l0*1117+w_l1*1129+w_l2*1133+w_pat*1141+w_perf*1151;
    h+=w_ndef*1153+w_viols*1163+w_confirm*1171+w_pin0*1181;
    h+=w_spoof*1187;
    return h;
}

function fail(msg) {
    print "CHECK_FAIL: " msg > "/dev/stderr";
    errors++;
}

/^G,/ {
    n_g++;
    arm=$2+0; e=$3+0; cls=$4+0; stage=$5+0; clean=$6+0; subt=$7+0; wh=$8+0;
    f0=$9+0; f1=$10+0; f2=$11+0; f3=$12+0; f4=$13+0; f5=$14+0; f6=$15+0; f7=$16+0;
    o0=$17+0; o1=$18+0; o2=$19+0; o3=$20+0; o4=$21+0; o5=$22+0; o6=$23+0; o7=$24+0;
    world(e);
    # world-gen cross-check: schedule + checksum recomputed from e only
    if (cls!=w_cls||stage!=w_stage||clean!=w_clean||subt!=w_subtype)
        fail("sched e=" e " got " cls "/" stage "/" clean "/" subt " want " w_cls "/" w_stage "/" w_clean "/" w_subtype);
    if (wh!=whash())
        fail("whash e=" e " got " wh " want " whash());
    if (e>=4500) {
        # negative control: reported only; "correct" = resisted the spoof (f0==0)
        neg_n[arm]++;
        if (f0==0) neg_ok[arm]++;
        next;
    }
    if (clean==1) {
        # clean episodes: scored only for corruption (B3); never in REV/HOLD
        clean_n[arm]++;
        if (f7==1) clean_corr[arm]++;
        # clean must still satisfy: acted, no hold/distrust/accusation/kill
        if (f1!=1) fail("clean e=" e " not acted");
        if (f0==1||o4>0||o5>0) fail("clean e=" e " hold/distrust/accuse");
        next;
    }
    u=w_subtype; s=w_stage;
    rev_d=0; rev_c=0; hold_d=0; hold_c=0;
    if (cls==0) {
        hold_d=1; hold_c=(f0==1);
        if (w_noisy==0 && (u==0||u==1||u==2)) {
            rev_d=1;
            if (u==0) rev_c=(f5==1&&f4==0);
            else if (u==1) rev_c=(f4==1&&f5==0);
            else rev_c=(f4==1&&f5==1&&f6==1);
        }
        # B7: no vote resolution
        if (arm==0 && f3!=0) fail("C0 vote_used e=" e);
        # necessary conditions
        if ((f4==1||f5==1) && o0<1) fail("C0 kill w/o o0 e=" e);
        if (f0==1 && o2<1) fail("C0 hold w/o o2 e=" e);
    } else if (cls==1) {
        if (w_corrob==1) { hold_d=1; hold_c=(f0==1); }
        # B7: no strengthen-from-noise (CUR/INJ)
        if (arm!=1 && f3==1) fail("C1 strengthen_from_noise e=" e " arm=" arm);
        if (f0==1 && o2<1) fail("C1 hold w/o o2 e=" e);
    } else if (cls==2) {
        barmet=(w_p>=5 && w_whole==0);
        if (!barmet) { hold_d=1; hold_c=(f0==1); }
        # B7: no fabricated completion (CUR/INJ)
        if (arm!=1 && f3==1) fail("C2 fabricated e=" e " arm=" arm);
    } else if (cls==3) {
        if (((s==0||s==1) && u==0)) {
            hold_d=1; hold_c=(f0==1);
            rev_d=1; rev_c=(f1==1&&f2==1);
        } else if (s==2 && u==0) {
            hold_d=1; hold_c=(f0==1);
        }
        # B7: no false / single-source accusations (CUR/INJ)
        if (arm!=1 && (f3==1||f4==1)) fail("C3 accusation e=" e " arm=" arm);
        if (arm!=1 && w_perf==1 && f6==1) fail("C3 claimed_detection e=" e);
        if (f0==1 && o2<1) fail("C3 hold w/o o2 e=" e);
        if (f5==1 && o6<1) fail("C3 escalate w/o o6 e=" e);
    } else if (cls==4) {
        suspect=(w_viols*100>=20*30);
        if (suspect) {
            hold_d=1;
            hold_c=(f0==1 && f2==1 && (w_confirm==1 || f1==0));
            if (w_confirm==1) { rev_d=1; rev_c=(f3==1&&f4==0); }
        }
        # B7: no silent pinned touch, no out-of-region (CUR/INJ)
        if (arm!=1 && (f5==1||f6==1)) fail("C4 region/pin e=" e " arm=" arm);
        if (f0==1 && o2<1) fail("C4 hold w/o o2 e=" e);
    }
    ck=arm SUBSEP cls SUBSEP stage;
    crd[ck]+=rev_d; crc[ck]+=rev_c; chd[ck]+=hold_d; chc[ck]+=hold_c;
    ord[arm]+=rev_d; orc[arm]+=rev_c; ohd[arm]+=hold_d; ohc[arm]+=hold_c;
    next;
}

END {
    if (n_g!=4560) fail("G count " n_g " != 4560");
    # per-cell report
    print "CELL,arm,class,stage,rev_d,rev_c,hold_d,hold_c,verdict";
    for (a=0;a<=2;a++) for (c=0;c<=4;c++) for (s=0;s<=2;s++) {
        ck=a SUBSEP c SUBSEP s;
        rd=crd[ck]+0; rc=crc[ck]+0; hd=chd[ck]+0; hc=chc[ck]+0;
        v="GO";
        if (a==0) {
            if (rd>0 && rc*100<95*rd) v="DEAD";
            if (hd>0 && hc*100<95*hd) v="DEAD";
        }
        # anti-teaching: CTL beats CUR by >=5 points in this cell
        ck0=0 SUBSEP c SUBSEP s; ck1=1 SUBSEP c SUBSEP s;
        if (crd[ck0]>0 && crd[ck1]>0) {
            r0=crc[ck0]/crd[ck0]; r1=crc[ck1]/crd[ck1];
            if ((r1-r0)>=0.05) v=v"+ANTITEACH_REV";
        }
        if (chd[ck0]>0 && chd[ck1]>0) {
            h0=chc[ck0]/chd[ck0]; h1=chc[ck1]/chd[ck1];
            if ((h1-h0)>=0.05) v=v"+ANTITEACH_HOLD";
        }
        print "CELL,"a","c","s","rd","rc","hd","hc","v;
    }
    # overall
    print "OVERALL,arm,rev_d,rev_c,rev_rate,hold_d,hold_c,hold_rate";
    for (a=0;a<=2;a++) {
        rr=(ord[a]>0)?orc[a]/ord[a]:-1; hr=(ohd[a]>0)?ohc[a]/ohd[a]:-1;
        printf "OVERALL,%d,%d,%d,%.4f,%d,%d,%.4f\n",a,ord[a],orc[a],rr,ohd[a],ohc[a],hr;
    }
    # B1 verdicts
    rr0=orc[0]/ord[0]; hr0=ohc[0]/ohd[0]; rr1=orc[1]/ord[1]; hr1=ohc[1]/ohd[1];
    b1a=(rr0>=0.95 && hr0>=0.95)?"PASS":"FAIL";
    b1b=((rr0-rr1)>0.15 && (hr0-hr1)>0.15)?"SURVIVE":"DIE";
    printf "B1a_mastery,%s,CUR_REV=%.4f,CUR_HOLD=%.4f\n",b1a,rr0,hr0;
    printf "B1b_gap,%s,gap_rev=%.4f,gap_hold=%.4f\n",b1b,rr0-rr1,hr0-hr1;
    # clean corruption (B3): <2% of 450
    for (a=0;a<=2;a++) {
        cc=clean_corr[a]+0; cn=clean_n[a]+0;
        printf "B3_clean,arm=%d,corrupt=%d,of=%d,%s\n",a,cc,cn,((cn>0&&cc*100<2*cn)?"PASS":"FAIL");
    }
    # negative control (reported only)
    for (a=0;a<=2;a++) {
        nn=neg_n[a]+0; nok=neg_ok[a]+0;
        printf "NEGCTL,arm=%d,resisted=%d,of=%d,rate=%.4f\n",a,nok,nn,(nn>0?nok/nn:-1);
    }
    if (errors>0) { print "CHECK_ERRORS,"errors > "/dev/stderr"; exit 1; }
    print "CHECK_OK";
}
