#!/usr/bin/env python3
"""Apply the Track-B knowledge-store fork to a copy of webg_bf1.zag.

Produces instrument_kb.zag. All edits are additive except the verdict_core
signature and its single call site in cmd_verdict.
"""
import sys

SRC = sys.argv[1]
DST = sys.argv[2]

src = open(SRC).read()

KB_FUNCS = r'''
// ================= TRACK B: committed-knowledge store + retrieval prior ===
// Claims enter the store ONLY via the deliberate `kbcommit` command
// (consistent with the MA1 deliberate kill/pin/promote line). The verdict
// path opens knowledge.txt READ-ONLY and never writes it.
// Retrieval match rules (frozen):
//   content tokens = lowercase, tokenize(minl=2), exact-drop of the taught
//     G1 DROP stoplist (same pipeline as kw_query).
//   sh_ck = # candidate content tokens prefix-matched (tok_match) by some
//     committed-claim content token.  bind = 3*sh_ck >= 2*sn.
//   sh_kc = # committed-claim content tokens prefix-matched by some
//     candidate token.  fullcov = sh_kc >= kn.
//   digits = content tokens containing >=1 ASCII digit; compared by EXACT
//     multiset equality (tok_eq), not prefix.
//   AGREE      = bind && fullcov && digits-equal
//   CONTRADICT = bind && !agree && candidate has >=1 digit && !digits-equal
//   else UNKNOWN -> frozen G4 verdict path.

// kb_load: read <sd>/knowledge.txt; lines "KB|<seq>|<claim>".
// kba: arena holding claim bytes; kbt: (off,len) u32 pairs; kn: count.
// Returns 1 if the file was present (even when empty), 0 when absent
// (Arm N: no deliberate commit -> the prior is skipped entirely).
fn kb_load(sd:[]u8,kba:[]u8,kbt:[]u8,kn:*i32)i32 {
    kn[0]=0;
    let ok:i32=0;
    let buf:[]u8=read_file(sd,"knowledge.txt",&ok);
    if(ok==0){return 0;}
    let apos:i32=0;
    let pos:i32=0;
    let ls:i32=0;
    let ll:i32=0;
    while(next_line(buf,&pos,&ls,&ll)==1){
        let ln:i32=ll;
        if(ln>0 && buf[ls+ln-1]==13){ln=ln-1;}
        if(ln>4 && buf[ls]==75 && buf[ls+1]==66 && buf[ls+2]==124){
            let p:i32=ls+3;
            while(p<ls+ln && buf[p]!=124){p=p+1;}
            if(p<ls+ln){
                let cs:i32=p+1;
                let cl:i32=ls+ln-cs;
                if(cl>0 && kn[0]<64 && apos+cl<=kba.len){
                    let c:i32=0;
                    while(c<cl){kba[apos+c]=buf[cs+c]; c=c+1;}
                    p32(kbt,kn[0]*8,apos);
                    p32(kbt,kn[0]*8+4,cl);
                    apos=apos+cl;
                    kn[0]=kn[0]+1;
                }
            }
        }
    }
    nio_free(buf);
    return 1;
}

// content_toks: lowercase s, tokenize(minl=2), exact-drop DROP tokens.
// Token bytes are copied into the caller's arena ab at apos; (off,len)
// pairs go into tb (cap entries). Mirrors kw_query's pipeline exactly.
fn content_toks(s:[]u8,dropb:[]u8,dropt:[]u8,dropn:i32,ab:[]u8,apos:*i32,tb:[]u8,cap:i32,cn:*i32)void {
    cn[0]=0;
    let low:[]u8=lower_copy(s);
    let tt:[]u8=nio_alloc(512*8);
    let tn:i32=0;
    tokenize(low,tt,512,2,&tn);
    let i:i32=0;
    while(i<tn && cn[0]<cap){
        let ts:i32=g32(tt,i*8);
        let tl:i32=g32(tt,i*8+4);
        let dropme:i32=0;
        let k:i32=0;
        while(k<dropn){
            if(tok_eq(low,ts,tl,dropb,g32(dropt,k*8),g32(dropt,k*8+4))==1){dropme=1; break;}
            k=k+1;
        }
        if(dropme==0 && apos[0]+tl<=ab.len){
            let c:i32=0;
            while(c<tl){ab[apos[0]+c]=low[ts+c]; c=c+1;}
            p32(tb,cn[0]*8,apos[0]);
            p32(tb,cn[0]*8+4,tl);
            apos[0]=apos[0]+tl;
            cn[0]=cn[0]+1;
        }
        i=i+1;
    }
    nio_free(low);
    nio_free(tt);
    return;
}

fn tok_has_digit(b:[]u8,off:i32,ln:i32)i32 {
    let i:i32=0;
    while(i<ln){
        let c:u8=b[off+i];
        if(c>=48 && c<=57){return 1;}
        i=i+1;
    }
    return 0;
}

// digit_toks: content tokens containing at least one ASCII digit.
fn digit_toks(ab:[]u8,at:[]u8,an:i32,db:[]u8,dapos:*i32,dt2:[]u8,dn2:*i32)void {
    dn2[0]=0;
    let i:i32=0;
    while(i<an && dn2[0]<32){
        let off:i32=g32(at,i*8);
        let ln:i32=g32(at,i*8+4);
        if(tok_has_digit(ab,off,ln)==1 && dapos[0]+ln<=db.len){
            let c:i32=0;
            while(c<ln){db[dapos[0]+c]=ab[off+c]; c=c+1;}
            p32(dt2,dn2[0]*8,dapos[0]);
            p32(dt2,dn2[0]*8+4,ln);
            dapos[0]=dapos[0]+ln;
            dn2[0]=dn2[0]+1;
        }
        i=i+1;
    }
    return;
}

// digits_eq: EXACT multiset equality of digit tokens (tok_eq, not prefix).
fn digits_eq(ab:[]u8,at:[]u8,an:i32,bb:[]u8,bt:[]u8,bn:i32)i32 {
    if(an!=bn){return 0;}
    let used:[]u8=nio_alloc(64);
    let z:i32=0;
    while(z<64){used[z]=0; z=z+1;}
    let i:i32=0;
    while(i<an){
        let ao:i32=g32(at,i*8);
        let al:i32=g32(at,i*8+4);
        let hit:i32=0;
        let j:i32=0;
        while(j<bn){
            if(used[j]==0 && tok_eq(ab,ao,al,bb,g32(bt,j*8),g32(bt,j*8+4))==1){used[j]=1; hit=1; break;}
            j=j+1;
        }
        if(hit==0){nio_free(used); return 0;}
        i=i+1;
    }
    nio_free(used);
    return 1;
}

// kb_prior: the retrieval stage. For each included (post-injection-scan)
// page, take its G3 best sentence and compare against every committed
// claim. AGREE pages are collected into o_agp (page numbers); the agreed
// claim seq (1-based, matching the KB|<seq>| commit lines) into o_seq.
// Returns 2=AGREE, 1=CONTRADICT, 0=UNKNOWN.
fn kb_prior(buf:[]u8,incl:[]u8,ninc:i32,st:[]u8,nst:i32,
    qlow:[]u8,qt:[]u8,qn:i32,
    kba:[]u8,kbt:[]u8,kbn:i32,
    dropb:[]u8,dropt:[]u8,dropn:i32,
    o_agp:[]u8,o_agn:*i32,o_seq:*i32)i32 {
    o_agn[0]=0;
    o_seq[0]=-1;
    // precompute per-claim content-token and digit tables (claims fixed)
    let kab:[]u8=nio_alloc(65536);
    let kapos:i32=0;
    let kat:[]u8=nio_alloc(64*64*8);
    let kan:[]u8=nio_alloc(64*4);
    let kdb:[]u8=nio_alloc(16384);
    let kdpos:i32=0;
    let kdt:[]u8=nio_alloc(64*32*8);
    let kdn:[]u8=nio_alloc(64*4);
    let kc:i32=0;
    while(kc<kbn && kc<64){
        let koff:i32=g32(kbt,kc*8);
        let kln:i32=g32(kbt,kc*8+4);
        let ks:[]u8=kba[koff..koff+kln];
        let cn:i32=0;
        content_toks(ks,dropb,dropt,dropn,kab,&kapos,kat[kc*512..kc*512+512],64,&cn);
        p32(kan,kc*4,cn);
        let dn2:i32=0;
        digit_toks(kab,kat[kc*512..kc*512+512],cn,kdb,&kdpos,kdt[kc*256..kc*256+256],&dn2);
        p32(kdn,kc*4,dn2);
        kc=kc+1;
    }
    let sab:[]u8=nio_alloc(65536);
    let sdb:[]u8=nio_alloc(16384);
    let agseq:i32=-1;
    let ctseq:i32=-1;
    let ctpg:i32=-1;
    let j:i32=0;
    while(j<ninc){
        let pg:i32=g32(incl,j*4);
        let bs:[]u8=best_for_page(buf,pg,st,nst,qlow,qt,qn);
        if(bs.len>0){
            let sapos:i32=0;
            let st2:[]u8=nio_alloc(64*8);
            let sn:i32=0;
            content_toks(bs,dropb,dropt,dropn,sab,&sapos,st2,64,&sn);
            let sdpos:i32=0;
            let sdt:[]u8=nio_alloc(32*8);
            let sdn:i32=0;
            digit_toks(sab,st2,sn,sdb,&sdpos,sdt,&sdn);
            let k:i32=0;
            while(k<kbn && k<64){
                let kn2:i32=g32(kan,k*4);
                let kdn2:i32=g32(kdn,k*4);
                let ctab:[]u8=kat[k*512..k*512+512];
                let dtab:[]u8=kdt[k*256..k*256+256];
                let sh_ck:i32=overlap(sab,st2,sn,kab,ctab,kn2);
                let bind:i32=0;
                if(sn>0 && 3*sh_ck>=2*sn){bind=1;}
                if(bind==1){
                    let sh_kc:i32=overlap(kab,ctab,kn2,sab,st2,sn);
                    let deq:i32=digits_eq(sab,sdt,sdn,kdb,dtab,kdn2);
                    if(sh_kc>=kn2 && deq==1){
                        if(agseq==-1){agseq=k;}
                        if(o_agn[0]<64){p32(o_agp,o_agn[0]*4,pg); o_agn[0]=o_agn[0]+1;}
                    }else{
                        if(sdn>=1 && deq==0 && ctseq==-1){ctseq=k; ctpg=pg;}
                    }
                }
                k=k+1;
            }
            nio_free(st2);
            nio_free(sdt);
        }
        nio_free(bs);
        j=j+1;
    }
    nio_free(kab);
    nio_free(kat);
    nio_free(kan);
    nio_free(kdb);
    nio_free(kdt);
    nio_free(kdn);
    nio_free(sab);
    nio_free(sdb);
    if(agseq!=-1){o_seq[0]=agseq+1; return 2;}
    if(ctseq!=-1){o_seq[0]=ctseq+1; p32(o_agp,0,ctpg); o_agn[0]=1; return 1;}
    return 0;
}

// cmd_kbcommit: the DELIBERATE install path for the knowledge store.
// Reads <src> (one claim per line), validates every line against the
// PARSE gate (>=4 tokens, <=600 chars), all-or-nothing, then writes
// <sd>/knowledge.txt as "KB|<seq>|<claim>" lines. The verdict path only
// ever reads this file; nothing in the ingestion path writes it.
fn cmd_kbcommit(src:[]u8,sd:[]u8)i32 {
    let ok:i32=0;
    let buf:[]u8=read_path(src,&ok);
    if(ok==0){_zag_println("KB|ERROR|read-fail"); return 2;}
    let n:i32=0;
    let pos:i32=0;
    let ls:i32=0;
    let ll:i32=0;
    while(next_line(buf,&pos,&ls,&ll)==1){
        let ln:i32=ll;
        if(ln>0 && buf[ls+ln-1]==13){ln=ln-1;}
        let t:[]u8=trim(buf[ls..ls+ln]);
        if(t.len==0){continue;}
        let low:[]u8=lower_copy(t);
        let tt:[]u8=nio_alloc(512*8);
        let tn:i32=0;
        tokenize(low,tt,512,2,&tn);
        nio_free(low);
        nio_free(tt);
        if(tn<4 || t.len>600){
            _zag_print("KB|REJECT|line ");
            _zag_print(i64s((n+1) as i64));
            _zag_println("|PARSE-GATE");
            nio_free(buf);
            return 3;
        }
        n=n+1;
    }
    if(n==0 || n>64){_zag_println("KB|ERROR|empty-or-too-many"); nio_free(buf); return 3;}
    let ob:[]u8=nio_alloc(65536);
    let o:i32=0;
    let seq:i32=0;
    pos=0;
    while(next_line(buf,&pos,&ls,&ll)==1){
        let ln2:i32=ll;
        if(ln2>0 && buf[ls+ln2-1]==13){ln2=ln2-1;}
        let t2:[]u8=trim(buf[ls..ls+ln2]);
        if(t2.len==0){continue;}
        seq=seq+1;
        let sq:[]u8=i64s(seq as i64);
        let need:i32=4+sq.len+t2.len;
        if(o+need<=ob.len){
            ob[o]=75; ob[o+1]=66; ob[o+2]=124; o=o+3;
            let c:i32=0;
            while(c<sq.len){ob[o+c]=sq[c]; c=c+1;}
            o=o+sq.len;
            ob[o]=124; o=o+1;
            c=0;
            while(c<t2.len){ob[o+c]=t2[c]; c=c+1;}
            o=o+t2.len;
            ob[o]=10; o=o+1;
        }
        _zag_print("KB|COMMIT|");
        _zag_println(sq);
        nio_free(sq);
    }
    write_file(sd,"knowledge.txt",ob[0..o]);
    nio_free(ob);
    nio_free(buf);
    return 0;
}
'''

# E1: insert KB functions before "fn first_int"
anchor1 = "fn first_int(s:[]u8)i64 {"
assert src.count(anchor1) == 1, "anchor1 not unique"
src = src.replace(anchor1, KB_FUNCS + "\n" + anchor1)

# E2: verdict_core signature - add kb params after loud:i32,
old_sig = """    dt:[]u8,dn:i32,force_blind:i32,loud:i32,
    o_ans:[]u8,o_ansn:*i32,o_widx:[]u8,o_wn:*i32,"""
new_sig = """    dt:[]u8,dn:i32,force_blind:i32,loud:i32,kba:[]u8,kbt:[]u8,kbn:i32,
    o_ans:[]u8,o_ansn:*i32,o_widx:[]u8,o_wn:*i32,"""
assert src.count(old_sig) == 1, "sig anchor not unique"
src = src.replace(old_sig, new_sig)

# E3: insert the KB-PRIOR block before the MULTIHOP comment
anchor3 = "    // MULTIHOP: per-entity best-sentence clustering with need-keyword relevance."
assert src.count(anchor3) == 1, "anchor3 not unique"

PRIOR_BLOCK = r'''    // ---- TRACK B KB-PRIOR: retrieval against committed knowledge ----
    // The verdict for an incoming page-claim is made against committed
    // knowledge: consistent-with-known -> corroborated (the knowledge base
    // itself is the corroborating source, so MIN-SOURCES is satisfied by
    // knowledge + page); contradicts-known -> rejected with
    // GATE|KB_CONTRADICTION (never installed); unknown -> frozen G4 path.
    // kbn==0 (Arm N: no deliberate commit) -> prior skipped entirely.
    // Precedence: AGREE is checked across all (page, claim) pairs before
    // any CONTRADICT fires.
    if(kbn>0 && blind==0){
        let dropv:[]u8=dget(dt,dn,"DROP");
        let droplow:[]u8=lower_copy(dropv);
        let dropt:[]u8=nio_alloc(128*8);
        let dropn:i32=0;
        tokenize(droplow,dropt,128,1,&dropn);
        let kpag:[]u8=nio_alloc(64*4);
        let kagn:i32=0;
        let kseq:i32=-1;
        let kpd:i32=kb_prior(buf,incl,ninc,st,nst,qlow,qt,qn,
            kba,kbt,kbn,droplow,dropt,dropn,kpag,&kagn,&kseq);
        nio_free(droplow);
        nio_free(dropt);
        if(kpd==2 && kagn>0){
            let bs2:[]u8=best_for_page(buf,g32(kpag,0),st,nst,qlow,qt,qn);
            if(loud==1){
                let q3:i32=0;
                while(q3<kagn){
                    _zag_print("KB|AGREE|");
                    _zag_print(i64s(kseq as i64));
                    _zag_print("|");
                    _zag_println(pid_of(pa,pt,g32(kpag,q3*4)));
                    q3=q3+1;
                }
                _zag_print("KB|CORROBORATED|");
                _zag_println(i64s(kseq as i64));
                _zag_print("ANSWER|");
                _zag_println(bs2);
                _zag_print("CLAIM|1|");
                _zag_print(bs2);
                _zag_print("|");
                print_pids_csv(pa,pt,kpag,kagn);
                _zag_println("");
                let q4:i32=0;
                while(q4<kagn){
                    _zag_print("PROV|1|");
                    _zag_println(pid_of(pa,pt,g32(kpag,q4*4)));
                    q4=q4+1;
                }
            }
            let c7:i32=0;
            while(c7<bs2.len && c7<o_ans.len){o_ans[c7]=bs2[c7]; c7=c7+1;}
            o_ansn[0]=c7;
            let q5:i32=0;
            while(q5<kagn){p32(o_widx,q5*4,g32(kpag,q5*4)); q5=q5+1;}
            o_wn[0]=kagn;
            o_provs[0]=kagn;
            o_claims[0]=1;
            nio_free(bs2);
            nio_free(kpag);
            nio_free(qlow);
            nio_free(qt);
            nio_free(incl);
            return 1;
        }
        if(kpd==1){
            if(loud==1){
                _zag_print("KB|CONTRADICT|");
                _zag_print(i64s(kseq as i64));
                _zag_print("|");
                _zag_println(pid_of(pa,pt,g32(kpag,0)));
                _zag_print("GATE|KB_CONTRADICTION|");
                _zag_println(i64s(kseq as i64));
                _zag_println("ANSWER|UNCHECKABLE");
            }
            nio_free(kpag);
            nio_free(qlow);
            nio_free(qt);
            nio_free(incl);
            return 0;
        }
        nio_free(kpag);
    }

'''
src = src.replace(anchor3, PRIOR_BLOCK + anchor3)

# E4: cmd_verdict - load kb and pass to verdict_core
old_call = """    verdict_core(buf,np,pa,pt,tt,st,nst,ha,ht,query,kind,extra,kwstr,dt,dn,0,1,
        o_ans,&o_ansn,o_widx,&o_wn,&o_provs,&o_claims,o_fl,&o_fln);"""
new_call = """    let kba:[]u8=nio_alloc(65536);
    let kbt:[]u8=nio_alloc(64*8);
    let kbn:i32=0;
    kb_load(sd,kba,kbt,&kbn);
    verdict_core(buf,np,pa,pt,tt,st,nst,ha,ht,query,kind,extra,kwstr,dt,dn,0,1,
        kba,kbt,kbn,
        o_ans,&o_ansn,o_widx,&o_wn,&o_provs,&o_claims,o_fl,&o_fln);"""
assert src.count(old_call) == 1, "call anchor not unique"
src = src.replace(old_call, new_call)

old_free = """    nio_free(o_ans);
    nio_free(o_widx);
    nio_free(o_fl);
    nio_free(dt);
    return 0;
}"""
new_free = """    nio_free(o_ans);
    nio_free(o_widx);
    nio_free(o_fl);
    nio_free(kba);
    nio_free(kbt);
    nio_free(dt);
    return 0;
}"""
assert src.count(old_free) == 1, "free anchor not unique"
src = src.replace(old_free, new_free)

# E5: main() dispatch for kbcommit
old_main = """    if(nio_equal(m,"query")==1){"""
new_main = """    if(nio_equal(m,"kbcommit")==1){
        let kb1:[]u8=_zag_arg(2);
        let kb2:[]u8=_zag_arg(3);
        if(kb1.len==0 || kb2.len==0){return 2;}
        return cmd_kbcommit(kb1,kb2);
    }
    if(nio_equal(m,"query")==1){"""
assert src.count(old_main) == 1, "main anchor not unique"
src = src.replace(old_main, new_main)

open(DST, "w").write(src)
print("wrote", DST, len(src), "bytes")
