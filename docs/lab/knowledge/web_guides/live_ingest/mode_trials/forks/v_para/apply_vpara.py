#!/usr/bin/env python3
"""Apply V-PARA edits to a copy of frozen webg.zag. Pure text surgery; the
frozen file is never touched."""
import sys

SRC = '/home/hatch/workspace/scratch-li-f2/v_para.zag'
src = open(SRC).read()
orig_len = len(src)

def rep(old, new, count=1):
    global src
    assert src.count(old) == count, 'anchor count %d != %d for: %r' % (src.count(old), count, old[:80])
    src = src.replace(old, new)

# ---- V-PARA block: insert before cluster_best ----
vpara = r'''
// ================= V-PARA: paraphrase-tolerant corroboration =================
// Corroboration = deterministic conjunction (ALL required):
//  (1) numeric-exactness: multiset of digit-bearing tokens identical across
//      the two sentences (numbers/units/dates under instrument normalization);
//  (2) rare-content-token Jaccard >= 0.60 (stopword-stripped sets; "rare" is
//      operationalized by stopword stripping per the frozen prereg);
//  (3) >= MIN-SOURCES distinct hosts among member pages (H| metadata parsed by
//      parse_hosts; pages without H| each count as their own host);
//  (4) injection scan clean (excluded pages never enter `incl`).
// Frozen stoplist: filed as stoplist.txt with the variant; the embedded copy
// below must be byte-identical to the filed copy (checked by BUILD_VPARA.sh).

fn para_stoplist_raw()[]u8 {
    return "a|an|the|and|or|of|to|in|on|for|with|is|are|was|were|be|been|being|have|has|had|do|does|did|will|would|can|could|should|may|might|must|shall|it|its|this|that|these|those|as|at|by|from|but|not|no|so|if|then|too|very|i|you|he|she|they|we|them|him|her|us|our|your|their|his|my|me|each|every|all|any|both|either|neither|here|there|when|where|which|who|whom|what|how|why|over|under|again|further|such|only|own|same|than|into|out|up|down|off|about|between|through|during|before|after|above|below|until|while|because|nor|am";
}

// parse pipe-delimited stoplist into table of (start,len) over raw
fn para_stoplist(raw:[]u8,tab:[]u8,n:*i32)void {
    n[0]=0;
    let i:i32=0;
    let ws:i32=0;
    while(i<=raw.len){
        if(i==raw.len || raw[i]==124){
            if(i>ws && n[0]<256){
                p32(tab,n[0]*8,ws);
                p32(tab,n[0]*8+4,i-ws);
                n[0]=n[0]+1;
            }
            ws=i+1;
        }
        i=i+1;
    }
    return;
}

fn para_is_stop(raw:[]u8,s:[]u8,so:i32,sl:i32,st:[]u8,sn:i32)i32 {
    let k:i32=0;
    while(k<sn){
        if(tok_eq(s,so,sl,raw,g32(st,k*8),g32(st,k*8+4))==1){return 1;}
        k=k+1;
    }
    return 0;
}

fn para_has_digit(s:[]u8,so:i32,ln:i32)i32 {
    let q:i32=so;
    while(q<so+ln){
        let e:u8=s[q];
        if(e>=48 && e<=57){return 1;}
        q=q+1;
    }
    return 0;
}

// numeric tokens of s: tokenize minl=1 (instrument tokenizer), keep tokens
// bearing >=1 digit. table of (base+start,len); starts are absolute in the
// caller's arena (base = s's offset in that arena).
fn para_numtoks(s:[]u8,base:i32,tt:[]u8,cap:i32,n:*i32)void {
    let tmp:[]u8=nio_alloc(256*8);
    let tn:i32=0;
    tokenize(s,tmp,256,1,&tn);
    n[0]=0;
    let i:i32=0;
    while(i<tn){
        let so:i32=g32(tmp,i*8);
        let sl:i32=g32(tmp,i*8+4);
        if(para_has_digit(s,so,sl)==1 && n[0]<cap){
            p32(tt,n[0]*8,base+so);
            p32(tt,n[0]*8+4,sl);
            n[0]=n[0]+1;
        }
        i=i+1;
    }
    nio_free(tmp);
    return;
}

// multiset equality of numeric token lists
fn para_num_eq(ab:[]u8,at:[]u8,an:i32,bb:[]u8,bt:[]u8,bn:i32)i32 {
    if(an!=bn){return 0;}
    let i:i32=0;
    while(i<an){
        let ao:i32=g32(at,i*8);
        let al:i32=g32(at,i*8+4);
        let ca:i32=0;
        let cb:i32=0;
        let j:i32=0;
        while(j<an){
            if(tok_eq(ab,ao,al,ab,g32(at,j*8),g32(at,j*8+4))==1){ca=ca+1;}
            j=j+1;
        }
        j=0;
        while(j<bn){
            if(tok_eq(ab,ao,al,bb,g32(bt,j*8),g32(bt,j*8+4))==1){cb=cb+1;}
            j=j+1;
        }
        if(ca!=cb){return 0;}
        i=i+1;
    }
    return 1;
}

// rare-content tokens of s: tokenize minl=2 (instrument convention),
// drop stopwords, dedupe -> set. table of (base+start,len); starts absolute.
fn para_content(raw:[]u8,s:[]u8,base:i32,st:[]u8,sn:i32,tt:[]u8,cap:i32,n:*i32)void {
    let tmp:[]u8=nio_alloc(512*8);
    let tn:i32=0;
    tokenize(s,tmp,512,2,&tn);
    n[0]=0;
    let i:i32=0;
    while(i<tn){
        let so:i32=g32(tmp,i*8);
        let sl:i32=g32(tmp,i*8+4);
        if(para_is_stop(raw,s,so,sl,st,sn)==0){
            let dup:i32=0;
            let j:i32=0;
            while(j<n[0]){
                // tt stores base-absolute starts; s is the relative slice,
                // so subtract base for the in-slice comparison.
                if(tok_eq(s,so,sl,s,g32(tt,j*8)-base,g32(tt,j*8+4))==1){dup=1; break;}
                j=j+1;
            }
            if(dup==0 && n[0]<cap){
                p32(tt,n[0]*8,base+so);
                p32(tt,n[0]*8+4,sl);
                n[0]=n[0]+1;
            }
        }
        i=i+1;
    }
    nio_free(tmp);
    return;
}

// Jaccard >= 0.60  <=>  inter*5 >= 3*union ; both-empty => 0 (fail-safe)
fn para_jacc_ok(ab:[]u8,at:[]u8,an:i32,bb:[]u8,bt:[]u8,bn:i32)i32 {
    if(an==0 && bn==0){return 0;}
    let inter:i32=0;
    let i:i32=0;
    while(i<an){
        let j:i32=0;
        while(j<bn){
            if(tok_eq(ab,g32(at,i*8),g32(at,i*8+4),bb,g32(bt,j*8),g32(bt,j*8+4))==1){inter=inter+1; break;}
            j=j+1;
        }
        i=i+1;
    }
    let union:i32=an+bn-inter;
    if(union<=0){return 0;}
    if(inter*5>=3*union){return 1;}
    return 0;
}

// parse H|host lines from a pages buffer: zeroes hpt[0..maxp), attaches each
// H| to the most recently seen P| page. Hosts stored lowercase+trimmed in ha.
fn parse_hosts(buf:[]u8,np:i32,ha:[]u8,hapos:*i32,hpt:[]u8,maxp:i32)void {
    hapos[0]=0;
    let zh:i32=0;
    while(zh<maxp){p32(hpt,zh*8,0); p32(hpt,zh*8+4,0); zh=zh+1;}
    let pos:i32=0;
    let ls:i32=0;
    let ll:i32=0;
    let cur:i32=-1;
    while(next_line(buf,&pos,&ls,&ll)==1){
        let ln:i32=ll;
        if(ln>0 && buf[ls+ln-1]==13){ln=ln-1;}
        if(ln>2 && buf[ls]==80 && buf[ls+1]==124){
            cur=cur+1;
        }else{
            if(ln>2 && buf[ls]==72 && buf[ls+1]==124){
                if(cur>=0 && cur<np && cur<maxp){
                    let hs0:i32=ls+2;
                    let he0:i32=ls+ln;
                    while(hs0<he0 && (buf[hs0]==32 || buf[hs0]==9)){hs0=hs0+1;}
                    while(he0>hs0 && (buf[he0-1]==32 || buf[he0-1]==9)){he0=he0-1;}
                    let hl0:i32=he0-hs0;
                    if(hl0>0 && hapos[0]+hl0<=ha.len){
                        let hp0:i32=hapos[0];
                        let kc:i32=0;
                        while(kc<hl0){
                            let ch0:u8=buf[hs0+kc];
                            if(ch0>=65 && ch0<=90){ch0=(ch0 as i32+32) as u8;}
                            ha[hp0+kc]=ch0;
                            kc=kc+1;
                        }
                        p32(hpt,cur*8,hp0);
                        p32(hpt,cur*8+4,hl0);
                        hapos[0]=hp0+hl0;
                    }
                }
            }
        }
    }
    return;
}

// count distinct hosts among pages[0..m) (u32 page indices).
// pages without H| each count as their own host (BUGFIX-1 backward compat).
fn para_distinct_hosts(pages:[]u8,m:i32,ha:[]u8,hpt:[]u8)i32 {
    let d:i32=0;
    let i:i32=0;
    while(i<m){
        let pg:i32=g32(pages,i*4);
        let hs:i32=g32(hpt,pg*8);
        let hl:i32=g32(hpt,pg*8+4);
        let seen:i32=0;
        let j:i32=0;
        while(j<i){
            let pg2:i32=g32(pages,j*4);
            let hs2:i32=g32(hpt,pg2*8);
            let hl2:i32=g32(hpt,pg2*8+4);
            if(hl==0 && hl2==0){
                if(pg==pg2){seen=1; break;}
            }else{
                if(hl==hl2 && hl>0 && bsub_eq(ha,hs,ha,hs2,hl)==1){seen=1; break;}
            }
            j=j+1;
        }
        if(seen==0){d=d+1;}
        i=i+1;
    }
    return d;
}

// V-PARA candidates = per included page best sentence (by qb tokens), exactly
// like cluster_best; clustering by the para conjunction instead of
// byte-equality; winner = largest cluster with >= minsrc distinct hosts,
// tie -> earliest-listed page. o_idx = winner page indices.
fn cluster_best_para(buf:[]u8,incl:[]u8,ninc:i32,st:[]u8,nst:i32,
    qb:[]u8,qt:[]u8,qn:i32,minsrc:i32,ha:[]u8,hpt:[]u8,
    o_idx:[]u8,o_n:*i32)[]u8 {
    o_n[0]=0;
    let ca:[]u8=nio_alloc(65536);
    let ct:[]u8=nio_alloc(64*8);
    let cp:[]u8=nio_alloc(64*4);
    let nc:i32=0;
    let capos:i32=0;
    let ii:i32=0;
    while(ii<ninc){
        let pg:i32=g32(incl,ii*4);
        if(page_nsent(st,nst,pg)>0 && nc<64){
            let bs:[]u8=best_for_page(buf,pg,st,nst,qb,qt,qn);
            if(capos+bs.len<=ca.len){
                let c2:i32=0;
                while(c2<bs.len){ca[capos+c2]=bs[c2]; c2=c2+1;}
                p32(ct,nc*8,capos);
                p32(ct,nc*8+4,bs.len);
                p32(cp,nc*4,pg);
                nc=nc+1;
                capos=capos+bs.len;
            }
            nio_free(bs);
        }
        ii=ii+1;
    }
    if(nc==0){
        nio_free(ca);
        nio_free(ct);
        nio_free(cp);
        return "";
    }
    let raw:[]u8=para_stoplist_raw();
    let slt:[]u8=nio_alloc(256*8);
    let sln:i32=0;
    para_stoplist(raw,slt,&sln);
    let nnt:[]u8=nio_alloc(64*4);
    let ntt:[]u8=nio_alloc(64*64*8);
    let cnt:[]u8=nio_alloc(64*4);
    let ctt:[]u8=nio_alloc(64*256*8);
    let j:i32=0;
    while(j<nc){
        let s2:i32=g32(ct,j*8);
        let l2:i32=g32(ct,j*8+4);
        let sen:[]u8=ca[s2..s2+l2];
        let nn:i32=0;
        para_numtoks(sen,s2,ntt[j*512..j*512+512],64,&nn);
        p32(nnt,j*4,nn);
        let cn:i32=0;
        para_content(raw,sen,s2,slt,sln,ctt[j*2048..j*2048+2048],256,&cn);
        p32(cnt,j*4,cn);
        j=j+1;
    }
    let ck:[]u8=nio_alloc(64*8);
    let cc:[]u8=nio_alloc(64*4);
    let cf:[]u8=nio_alloc(64*4);
    let cm:[]u8=nio_alloc(64*64*4);
    let ncl:i32=0;
    let j2:i32=0;
    while(j2<nc){
        let c:i32=0;
        let found:i32=-1;
        while(c<ncl){
            let kk:i32=g32(ck,c*8);
            let an1:i32=g32(nnt,j2*4);
            let an2:i32=g32(nnt,kk*4);
            let numok:i32=para_num_eq(ca,ntt[j2*512..j2*512+512],an1,ca,ntt[kk*512..kk*512+512],an2);
            let joc:i32=0;
            if(numok==1){
                let bn1:i32=g32(cnt,j2*4);
                let bn2:i32=g32(cnt,kk*4);
                joc=para_jacc_ok(ca,ctt[j2*2048..j2*2048+2048],bn1,ca,ctt[kk*2048..kk*2048+2048],bn2);
            }
            if(numok==1 && joc==1){found=c; break;}
            c=c+1;
        }
        if(found==-1){
            if(ncl<64){
                p32(ck,ncl*8,j2);
                p32(cc,ncl*4,1);
                p32(cf,ncl*4,j2);
                p32(cm,ncl*256,g32(cp,j2*4));
                ncl=ncl+1;
            }
        }else{
            let cnt2:i32=g32(cc,found*4);
            if(cnt2<64){
                p32(cm,found*256+cnt2*4,g32(cp,j2*4));
                p32(cc,found*4,cnt2+1);
            }
        }
        j2=j2+1;
    }
    let w:i32=-1;
    let wc:i32=-1;
    let wf:i32=999999;
    let c3:i32=0;
    while(c3<ncl){
        let cnt3:i32=g32(cc,c3*4);
        let fo:i32=g32(cf,c3*4);
        let dh:i32=para_distinct_hosts(cm[c3*256..c3*256+256],cnt3,ha,hpt);
        if(dh>=minsrc){
            if(cnt3>wc || (cnt3==wc && fo<wf)){w=c3; wc=cnt3; wf=fo;}
        }
        c3=c3+1;
    }
    let ans:[]u8="";
    if(w>=0){
        let m:i32=0;
        while(m<wc){
            p32(o_idx,m*4,g32(cm,w*256+m*4));
            m=m+1;
        }
        o_n[0]=wc;
        let ks2:i32=g32(ck,w*8);
        let ks3:i32=g32(ct,ks2*8);
        let kl3:i32=g32(ct,ks2*8+4);
        ans=ca[ks3..ks3+kl3];
    }
    // NB: ca is NOT freed: ans aliases it (same as frozen cluster_best).
    nio_free(ct);
    nio_free(cp);
    nio_free(slt);
    nio_free(nnt);
    nio_free(ntt);
    nio_free(cnt);
    nio_free(ctt);
    nio_free(ck);
    nio_free(cc);
    nio_free(cf);
    nio_free(cm);
    return ans;
}

// ================= end V-PARA =================

'''

rep('fn cluster_best(buf:[]u8,incl:[]u8,ninc:i32,st:[]u8,nst:i32,',
    vpara + 'fn cluster_best(buf:[]u8,incl:[]u8,ninc:i32,st:[]u8,nst:i32,')

# ---- verdict_core signature: add ha/hpt ----
rep('''fn verdict_core(buf:[]u8,np:i32,pa:[]u8,pt:[]u8,tt:[]u8,st:[]u8,nst:i32,
    query:[]u8,kind:[]u8,extra:[]u8,needkw:[]u8,''',
'''fn verdict_core(buf:[]u8,np:i32,pa:[]u8,pt:[]u8,tt:[]u8,st:[]u8,nst:i32,ha:[]u8,hpt:[]u8,
    query:[]u8,kind:[]u8,extra:[]u8,needkw:[]u8,''')

# ---- cluster call site: minsrc moved up, para call ----
rep('''    let key:[]u8=cluster_best(buf,incl,ninc,st,nst,qlow,qt,qn,widx,&wn2);''',
'''    let minsrc:i32=dgeti(dt,dn,"MIN-SOURCES",1);
    if(minsrc<1){minsrc=1;}
    let key:[]u8=cluster_best_para(buf,incl,ninc,st,nst,qlow,qt,qn,minsrc,ha,hpt,widx,&wn2);''')

# ---- remove the now-duplicate minsrc computation ----
rep('''    let minsrc:i32=dgeti(dt,dn,"MIN-SOURCES",1);
    if(minsrc<1){minsrc=1;}
    let rc2:i32=0;''',
'''    let rc2:i32=0;''')

# ---- GATE|PARA emission on acceptance ----
rep('''            let m5:i32=0;
            while(m5<wn2){
                _zag_print("PROV|1|");
                _zag_println(pid_of(pa,pt,g32(widx,m5*4)));
                m5=m5+1;
            }
        }''',
'''            let m5:i32=0;
            while(m5<wn2){
                _zag_print("PROV|1|");
                _zag_println(pid_of(pa,pt,g32(widx,m5*4)));
                m5=m5+1;
            }
            _zag_print("GATE|PARA|");
            print_pids_csv(pa,pt,widx,wn2);
            _zag_println("");
        }''')

# ---- verdict_core call sites: calib_g4/g5/g6 + cmd_verdict ----
rep('''        let got:i32=verdict_core(cpages[0..cpn],np,pa,pt,tt,st,nst,
            buf[cqs..cqs+cql],"FACT","","",dt,dn,0,0,''',
'''        let got:i32=verdict_core(cpages[0..cpn],np,pa,pt,tt,st,nst,hah,hpth,
            buf[cqs..cqs+cql],"FACT","","",dt,dn,0,0,''')
rep('''        verdict_core(cpages[0..cpn],np,pa,pt,tt,st,nst,
            buf[cqs..cqs+cql],"FACT","","",dt,dn,0,0,''',
'''        verdict_core(cpages[0..cpn],np,pa,pt,tt,st,nst,hah,hpth,
            buf[cqs..cqs+cql],"FACT","","",dt,dn,0,0,''')
rep('''        verdict_core(cpages[0..cpn],np,pa,pt,tt,st,nst,
            q,"FACT","","",dt,dn,0,0,''',
'''        verdict_core(cpages[0..cpn],np,pa,pt,tt,st,nst,hah,hpth,
            q,"FACT","","",dt,dn,0,0,''')
rep('''    verdict_core(buf,np,pa,pt,tt,st,nst,query,kind,extra,kwstr,dt,dn,0,1,
        o_ans,&o_ansn,o_widx,&o_wn,&o_provs,&o_claims,o_fl,&o_fln);''',
'''    verdict_core(buf,np,pa,pt,tt,st,nst,haV,hptV,query,kind,extra,kwstr,dt,dn,0,1,
        o_ans,&o_ansn,o_widx,&o_wn,&o_provs,&o_claims,o_fl,&o_fln);''')

# ---- calib_g4/g5/g6: allocate+parse hosts before calib_pages; free at end ----
# The three call sites are textually identical; replace one at a time in order.
rep('''    calib_pages(cpages,cpn,pa,&papos,pt,tt,st,&nst,&np);
    let ok:i32=0;
    if(np>0){''',
'''    let hah:[]u8=nio_alloc(1024);
    let haph:i32=0;
    let hpth:[]u8=nio_alloc(64*8);
    parse_hosts(cpages[0..cpn],np,hah,&haph,hpth,64);
    calib_pages(cpages,cpn,pa,&papos,pt,tt,st,&nst,&np);
    let ok:i32=0;
    if(np>0){''', count=3)

# ---- cmd_verdict: allocate + parse hosts before verdict_core ----
rep('''    parse_pages(buf,&np,pa,&papos,pt,tt,st,&nst,64,2048);
    let o_ans:[]u8=nio_alloc(4096);''',
'''    parse_pages(buf,&np,pa,&papos,pt,tt,st,&nst,64,2048);
    let haV:[]u8=nio_alloc(4096);
    let haposV:i32=0;
    let hptV:[]u8=nio_alloc(64*8);
    parse_hosts(buf,np,haV,&haposV,hptV,64);
    let o_ans:[]u8=nio_alloc(4096);''')

# NOTE: ha*/hpt* are intentionally not freed: each is ~1.5KB in a short-lived
# teach/verdict process invocation; the frozen code has the same pattern for
# several teach-time arenas. Determinism is unaffected (no reuse).

open(SRC,'w').write(src)
print('edits applied, new size', len(src), 'was', orig_len)
