#!/usr/bin/env python3
"""Assemble h7_exp2c.zag from the frozen h7_main.zag.

Additive changes only (mechanism untouched):
 1. learn_sincere + run_2c fns inserted immediately before fn main()
    (forward-reference safe: all callees defined above).
 2. Endorse-pool capacities: ipool 32768->65536, ient 2560->6400, icap 64->160.
 3. Phase-2c dispatch + post-2c (2C_) scoring inserted before Phase 3.
 4. MDUMP observability block inserted before the (ix) negative control.
"""
import sys

SRC = "/home/hatch/workspace/tnn-native-lab-work/docs/lab/epistemics/utterance_types/crew2/learner/h7_main.zag"
OUT = "/home/hatch/workspace/sinc_exp/exp2d/build/h7_exp2d.zag"

with open(SRC) as f:
    src = f.read()

FNS_2C = r'''
// ---------- FL2 sincere-episode correction (Phase 2c, experimental) ----------
// Teacher corrects toward ENDORSE. predict=ENDORSE: correct, nothing installed.
// predict=WITHHOLD(T): contradiction - eliminative revocation of T's firing
// markers (the same loop as learn_exemplar's wrong-type path). Generic over
// the taught concept index; no type keywords or type constants in code.
fn learn_sincere(kent:[]u8,kn:i32,kpool:[]u8,ment:[]u8,mn:*i32,
    mpool:[]u8,
    utt_l:[]u8,ctx_l:[]u8,spk_l:[]u8,
    name_buf:[]u8,nlen:*i32,scores:[]u8,
    abuf:[]u8,acount:*i32,acap:i32,slot:i32)i32 {
    let v:i32=predict(kent,kn,kpool,ment,mn.*,mpool,utt_l,ctx_l,spk_l,
        name_buf,nlen,scores);
    let pname:[]u8=name_buf[0..nlen.*];
    au(abuf,acount,acap,5,slot,v,nlen.*,0,0);
    if(v==0){
        au(abuf,acount,acap,6,slot,0,0,0,0);
        return 0;
    }
    let wk:i32=know_find(kent,kn,kpool,pname);
    let revoked:i32=0;
    if(wk>=0){
        let m:i32=0;
        while(m<mn.*){
            let e0:i32=m*24;
            if(t_get32(ment,e0)==wk && t_get32(ment,e0+8)!=3){
                let f:i32=t_get32(ment,e0+4);
                let fb:[]u8=utt_l;
                if(f==1){ fb=ctx_l; }
                if(f==2){ fb=spk_l; }
                let mo:i32=t_get32(ment,e0+16);
                let ml:i32=t_get32(ment,e0+20);
                if(has_sub(fb,mpool[mo..mo+ml])==1){
                    marker_revoke(ment,m,abuf,acount,acap,slot,2);
                    revoked=revoked+1;
                }
            }
            m=m+1;
        }
    }
    au(abuf,acount,acap,6,slot,1,revoked,0,0);
    return 1;
}

// ---------- Phase 2c delivery (experimental) ----------
// One FL2 episode per item in file order. E signal -> learn_sincere
// (contradiction revocation). W signal -> learn_exemplar(true concept idx
// from the item's ti field) + typed-partition write, as 2b exemplars.
// design 0=alpha (endorse pool unchanged); design 1=beta (E items appended
// to the endorse pool, lowered, ev=0). One calibrate() after the block.
fn run_2c(root:i64,calfile:[]u8,design:i32,
    kent:[]u8,kn:i32,kpool:[]u8,ment:[]u8,mn:*i32,mcap:i32,mpool:[]u8,mu:*i32,
    ipool:[]u8,iu:*i32,ient:[]u8,ine:*i32,icap:i32,
    tent:[]u8,tn:*i32,tpool:[]u8,tu:*i32,
    utt_l:[]u8,ctx_l:[]u8,spk_l:[]u8,
    wstarts:[]u8,wends:[]u8,name_buf:[]u8,nlen:*i32,scores:[]u8,
    abuf:[]u8,acount:*i32,acap:i32,epslot:*i32)i32 {
    let data:[]u8=read_file(root,calfile);
    if(data.len==0){ _zag_print("ERR 2c file\n"); return -1; }
    let cpool:[]u8=nio_alloc(65536);
    let cu:i32=0;
    let cent:[]u8=nio_alloc(5120);
    let cn:i32=0;
    let e2ul:[]u8=nio_alloc(4096);
    let e2cl:[]u8=nio_alloc(2048);
    let e2sl:[]u8=nio_alloc(512);
    let pos:i32=0;
    while(pos<data.len){
        let line:[]u8=strip_cr(next_line(data,&pos));
        if(line.len>0){
            let sig:[]u8=field_at(line,4);
            let ev:i32=0;
            if(sig.len>0 && sig[0]==87){ ev=1; }
            let tif:[]u8=field_at(line,5);
            let ti:i32=0;
            let qi:i32=0;
            while(qi<tif.len){
                let dd:i32=(tif[qi] as i32)-48;
                if(dd>=0 && dd<=9){ ti=ti*10+dd; }
                qi=qi+1;
            }
            let r2:i32=ilist_add(cpool,&cu,cent,&cn,128,field_at(line,3),
                field_at(line,2),field_at(line,1),ev,field_at(line,0));
            if(r2<0){ _zag_print("ERR 2c list\n"); return -1; }
            t_put32(cent,r2*40+36,ti);
            if(design==1 && ev==0){
                let pr:i32=ilist_add(ipool,iu,ient,ine,icap,
                    to_lower(e2ul,field_at(line,3)),
                    to_lower(e2cl,field_at(line,2)),
                    to_lower(e2sl,field_at(line,1)),0,ipool[0..0]);
                if(pr<0){ _zag_print("ERR 2c pool\n"); return -1; }
            }
        }
    }
    _zag_print("2CITEMS|");
    _zag_print(i64s(cn as i64));
    _zag_print("|design|");
    _zag_print(i64s(design as i64));
    _zag_print("|pool|");
    _zag_print(i64s(ine.* as i64));
    _zag_print("\n");
    let x:i32=0;
    while(x<cn){
        let ul:[]u8=to_lower(utt_l,ifield(cpool,cent,x,0));
        let cl:[]u8=to_lower(ctx_l,ifield(cpool,cent,x,1));
        let sl:[]u8=to_lower(spk_l,ifield(cpool,cent,x,2));
        let evx:i32=t_get32(cent,x*40+24);
        let tix:i32=t_get32(cent,x*40+36);
        au(abuf,acount,acap,4,epslot.*,2,evx,cn,0);
        if(evx==0){
            let sr:i32=learn_sincere(kent,kn,kpool,ment,mn,mpool,ul,cl,sl,
                name_buf,nlen,scores,abuf,acount,acap,epslot.*);
            au(abuf,acount,acap,6,epslot.*,10+sr,0,0,0);
        } else {
            let lr:i32=learn_exemplar(kent,kn,kpool,ment,mn,mcap,mpool,mu,tix,
                ul,cl,sl,wstarts,wends,name_buf,nlen,scores,abuf,acount,acap,
                epslot.*);
            let enm:[]u8=know_name(kent,kpool,tix);
            let said:i32=0;
            if((know_flags(kent,tix)&2)!=0){ said=1; }
            let twr:i32=typed_write(tent,tn,tpool,tu,ifield(cpool,cent,x,0),
                enm,ifield(cpool,cent,x,2),said,abuf,acount,acap,epslot.*);
            if(twr<0){ _zag_print("ERR 2c typed\n"); return -1; }
            au(abuf,acount,acap,6,epslot.*,20+lr,0,0,0);
        }
        epslot.*=epslot.*+1;
        x=x+1;
    }
    let cr:i32=calibrate(ment,mn.*,mpool,ipool,ient,ine.*,abuf,acount,acap,
        epslot.*);
    epslot.*=epslot.*+1;
    _zag_print("2CCALIB|revoked|");
    _zag_print(i64s(cr as i64));
    _zag_print("\n");
    return 0;
}

'''

# 1. insert the 2c fns immediately before fn main() so every callee
# (ilist_add, next_line, strip_cr, field_at) is already defined: znc
# miscompiles forward references (bus error / corrupt binary).
anchor1 = "fn main()void {"
assert src.count(anchor1) == 1
src = src.replace(anchor1, FNS_2C + anchor1, 1)

# 2. endorse-pool capacities (variable-anchored; other nio_alloc(32768) untouched)
a = "    let ipool:[]u8=nio_alloc(32768);"
assert src.count(a) == 1
src = src.replace(a, "    let ipool:[]u8=nio_alloc(65536);", 1)
b = "    let ient:[]u8=nio_alloc(2560);"
assert src.count(b) == 1
src = src.replace(b, "    let ient:[]u8=nio_alloc(6400);", 1)
c = "ilist_add(ipool,&iu,ient,&ine,64,"
assert src.count(c) == 2
src = src.replace(c, "ilist_add(ipool,&iu,ient,&ine,160,", 2)

# 3. Phase-2c dispatch + post-2c scoring, before Phase 3
anchor3 = "    // ---------- Phase 3 ----------"
assert src.count(anchor3) == 1

MODES = [
    # exp2d: cleaned corpora (C1 dedupe) + extended novel-family probes (C2).
    # "base" needs no dispatch entry (matches nothing, skips run_2c).
    ("ab2-a", "cal2_ab.txt", 0),
    ("ab2-b", "cal2_ab.txt", 1),
    ("abc2-a", "cal2_abc.txt", 0),
    ("abc2-b", "cal2_abc.txt", 1),
    ("v96-a", "cal2_vol2.txt", 0),
    ("v96-b", "cal2_vol2.txt", 1),
    ("de2-a", "cal2_de.txt", 0),
    ("de2-b", "cal2_de.txt", 1),
]
CALL = ("rc2c=run_2c(root,\"%s\",%d,\n"
        "        kent,kn,kpool,ment,&mn,mcap,mpool,&mu,\n"
        "        ipool,&iu,ient,&ine,160,\n"
        "        tent,&tn,tpool,&tu,\n"
        "        utt_l,ctx_l,spk_l,\n"
        "        wstarts,wends,name_buf,&nlen,scores,\n"
        "        abuf,&acount,acap,&ep);")
dispatch = ("    // ---------- Phase 2c: sincere-discourse calibration (EXPERIMENTAL) ----------\n"
            "    let mode:[]u8=arg_copy(2);\n"
            "    // Empty/missing mode: exact frozen path (Stage-0 gate).\n"
            "    if(mode.len>0){\n"
            "    au(abuf,&acount,acap,17,0,0,21,0,0);\n"
            "    _zag_print(\"2CMODE|\");\n"
            "    _zag_print(mode);\n"
            "    _zag_print(\"\\n\");\n"
            "    let rc2c:i32=0;\n")
for mname, mfile, mdesign in MODES:
    dispatch += ("    if(eq(mode,\"%s\")==1){\n"
                 "        " + CALL + "\n"
                 "    }\n") % (mname, mfile, mdesign)
dispatch += ("    if(rc2c<0){ _zag_print(\"ERR 2c run\\n\"); return; }\n"
             "\n")

SCORING = r'''
    // ---------- Phase 2c scoring: post-calibration bars (EXPERIMENTAL) ----------
    // Re-scores TR/PA/NO/SINC per type at post-2c state (log=0: read-only,
    // no typed-partition writes). In base mode the 2c block is skipped, so
    // these lines must equal the frozen 32-exemplar CURVE lines exactly.
    let t3:i32=1;
    while(t3<=5){
        let ppool3:[]u8=nio_alloc(32768);
        let pu3:i32=0;
        let pent3:[]u8=nio_alloc(2560);
        let pn3:i32=0;
        let cc3:i32=0;
        let ct3:i32=0;
        pn3=0; pu3=0;
        if(load_set(root,fname("tr",t3,".txt",fnbuf),ppool3,&pu3,pent3,&pn3,64)<0){ _zag_print("ERR 2ct\n"); return; }
        score_set(kent,kn,kpool,ment,mn,mpool,ppool3,pent3,0,pn3,
            utt_l,ctx_l,spk_l,name_buf,&nlen,scores,0,
            tent,&tn,tpool,&tu,abuf,&acount,acap,ep,&cc3,&ct3);
        let trc3:i32=cc3;
        pn3=0; pu3=0;
        if(load_set(root,fname("pa",t3,".txt",fnbuf),ppool3,&pu3,pent3,&pn3,64)<0){ _zag_print("ERR 2cp\n"); return; }
        score_set(kent,kn,kpool,ment,mn,mpool,ppool3,pent3,0,pn3,
            utt_l,ctx_l,spk_l,name_buf,&nlen,scores,0,
            tent,&tn,tpool,&tu,abuf,&acount,acap,ep,&cc3,&ct3);
        let pac3:i32=cc3;
        pn3=0; pu3=0;
        if(load_set(root,fname("no",t3,".txt",fnbuf),ppool3,&pu3,pent3,&pn3,64)<0){ _zag_print("ERR 2cn\n"); return; }
        score_set(kent,kn,kpool,ment,mn,mpool,ppool3,pent3,0,pn3,
            utt_l,ctx_l,spk_l,name_buf,&nlen,scores,0,
            tent,&tn,tpool,&tu,abuf,&acount,acap,ep,&cc3,&ct3);
        let noc3:i32=cc3;
        pn3=0; pu3=0;
        if(load_set(root,fname("sinc",t3,".txt",fnbuf),ppool3,&pu3,pent3,&pn3,64)<0){ _zag_print("ERR 2cs\n"); return; }
        let dpc3:i32=0;
        let lkc3:i32=0;
        let dpt3:i32=0;
        let lkt3:i32=0;
        score_set(kent,kn,kpool,ment,mn,mpool,ppool3,pent3,0,10,
            utt_l,ctx_l,spk_l,name_buf,&nlen,scores,0,
            tent,&tn,tpool,&tu,abuf,&acount,acap,ep,&dpc3,&dpt3);
        score_set(kent,kn,kpool,ment,mn,mpool,ppool3,pent3,10,20,
            utt_l,ctx_l,spk_l,name_buf,&nlen,scores,0,
            tent,&tn,tpool,&tu,abuf,&acount,acap,ep,&lkc3,&lkt3);
        _zag_print("2C_CURVE|");
        _zag_print(i64s(t3 as i64));
        _zag_print("|TR|");
        _zag_print(i64s(trc3 as i64));
        _zag_print("|PA|");
        _zag_print(i64s(pac3 as i64));
        _zag_print("|NO|");
        _zag_print(i64s(noc3 as i64));
        _zag_print("|DP|");
        _zag_print(i64s(dpc3 as i64));
        _zag_print("|LK|");
        _zag_print(i64s(lkc3 as i64));
        _zag_print("\n");
        let bar3:i32=0;
        if(noc3>=16 && pac3>=16){ bar3=1; }
        let nok3:i32=1;
        if(trc3>=16 && (noc3<=10 || pac3<=10)){ nok3=0; }
        let nod3:i32=1;
        if(trc3<12){ nod3=0; }
        let dp93:i32=0;
        if(dpc3>=9){ dp93=1; }
        let lk93:i32=0;
        if(lkc3>=9){ lk93=1; }
        checkn("2c_learn_bar_",t3,bar3,1,&fails);
        checkn("2c_learn_nomem_",t3,nok3,1,&fails);
        checkn("2c_learn_nodis_",t3,nod3,1,&fails);
        checkn("2c_sinc_dp_",t3,dp93,1,&fails);
        checkn("2c_sinc_lk_",t3,lk93,1,&fails);
        t3=t3+1;
    }

    // ---------- Phase 2c extended novel-family probes (EXPERIMENTAL, exp2d) ----------
    // Sincere what-if / where-do lookalikes (sinc3x_wi.txt, sinc3x_wd.txt),
    // scored read-only (log=0) at post-2c state. Inside if(mode.len>0), so the
    // empty mode keeps the exact frozen path (Stage-0 gate unaffected).
    let xq_pool:[]u8=nio_alloc(32768);
    let xq_pu:i32=0;
    let xq_ent:[]u8=nio_alloc(2560);
    let xq_n:i32=0;
    let xq_cc:i32=0;
    let xq_ct:i32=0;
    if(load_set(root,"sinc3x_wi.txt",xq_pool,&xq_pu,xq_ent,&xq_n,64)<0){ _zag_print("ERR xwi\n"); return; }
    score_set(kent,kn,kpool,ment,mn,mpool,xq_pool,xq_ent,0,xq_n,
        utt_l,ctx_l,spk_l,name_buf,&nlen,scores,0,
        tent,&tn,tpool,&tu,abuf,&acount,acap,ep,&xq_cc,&xq_ct);
    _zag_print("X2C_CURVE|3|WI|");
    _zag_print(i64s(xq_cc as i64));
    _zag_print("|N|");
    _zag_print(i64s(xq_n as i64));
    _zag_print("\n");
    let xq_wi9:i32=0;
    if(xq_cc>=9){ xq_wi9=1; }
    checkn("x2c_sinc_lk_wi_",3,xq_wi9,1,&fails);
    xq_n=0; xq_pu=0; xq_cc=0; xq_ct=0;
    if(load_set(root,"sinc3x_wd.txt",xq_pool,&xq_pu,xq_ent,&xq_n,64)<0){ _zag_print("ERR xwd\n"); return; }
    score_set(kent,kn,kpool,ment,mn,mpool,xq_pool,xq_ent,0,xq_n,
        utt_l,ctx_l,spk_l,name_buf,&nlen,scores,0,
        tent,&tn,tpool,&tu,abuf,&acount,acap,ep,&xq_cc,&xq_ct);
    _zag_print("X2C_CURVE|3|WD|");
    _zag_print(i64s(xq_cc as i64));
    _zag_print("|N|");
    _zag_print(i64s(xq_n as i64));
    _zag_print("\n");
    let xq_wd9:i32=0;
    if(xq_cc>=9){ xq_wd9=1; }
    checkn("x2c_sinc_lk_wd_",3,xq_wd9,1,&fails);

    } // end if(mode.len>0) for 2c dispatch+scoring

'''
src = src.replace(anchor3, dispatch + SCORING + anchor3, 1)

# 4. MDUMP before the (ix) negative control
anchor4 = "    // (ix) negative control:"
assert src.count(anchor4) == 1
MDUMP = r'''
    if(mode.len>0){
    // MDUMP: every learned marker with status (observability for exp2c
    // mechanism analysis; read-only). Format:
    // MDUMP|concept+1|field|status|support|bytes  (field 0=UTT 1=CTX 2=SPK;
    // status 1=PROVISIONAL 2=COMMITTED 3=REVOKED)
    let qk:i32=0;
    while(qk<kn){
        let qm:i32=0;
        while(qm<mn){
            let qe:i32=qm*24;
            if(t_get32(ment,qe)==qk){
                _zag_print("MDUMP|");
                _zag_print(i64s(qk as i64 + 1));
                _zag_print("|");
                _zag_print(i64s(t_get32(ment,qe+4) as i64));
                _zag_print("|");
                _zag_print(i64s(t_get32(ment,qe+8) as i64));
                _zag_print("|");
                _zag_print(i64s(t_get32(ment,qe+12) as i64));
                _zag_print("|");
                let qo:i32=t_get32(ment,qe+16);
                let ql:i32=t_get32(ment,qe+20);
                _zag_print(mpool[qo..qo+ql]);
                _zag_print("\n");
            }
            qm=qm+1;
        }
        qk=qk+1;
    }
    } // end if(mode.len>0) for MDUMP

'''
src = src.replace(anchor4, MDUMP + anchor4, 1)

with open(OUT, "w") as f:
    f.write(src)
print("wrote", OUT, len(src), "bytes")
