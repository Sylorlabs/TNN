// ================= V-QUAR-T paraphrase quarantine path =================
// Frozen loosened rule V-PARA (see DESIGN_FROZEN.md). Runs ONLY when the
// strict verdict_core did NOT install (vrc==0). For each page with >=1
// sentence and not injection-flagged, take its best sentence by query
// overlap (frozen best_for_page). Then:
//   P1. numeric signatures byte-equal: maximal [0-9.,] runs (internal
//       separators kept only between digits; trailing separators trimmed),
//       sorted, joined with \x01.
//   P2. rare-content-token Jaccard >= 0.60: tokenize(normalized, minlen 2)
//       minus the frozen stoplist (stoplist_para.txt); sorted unique sets;
//       inter*5 >= union*3, integer math. Empty sets never pass.
//   P3. >= 2 distinct hosts among the corroborating pages (H| lines, already
//       lowercase in the frozen driver; lowercased again here defensively).
//   P4. G6 clean: no group page in the strict run's injection-flag list
//       (o_fl), and only non-flagged pages are admitted as candidates.
// Medoid clustering: for medoid m, group(m) = {j : pair_ok(m,j)} (m in its
// own group). Winner = largest group with >=2 distinct hosts; ties broken by
// smallest medoid index. Deterministic.
// Emits on stdout: QUAR|1|<pids-csv>|<claim> and GATE|PARA|<pids-csv>.
// The claim is the medoid's normalized best sentence, byte-exact.
// ==========================================================================

// numeric tokens: maximal [0-9.,] runs; separators kept only between digits
fn qp_numtoks(s:[]u8,tt:[]u8,cap:i32,n:*i32)void {
    n[0]=0;
    let i:i32=0;
    while(i<s.len){
        let c:u8=s[i];
        if(c>=48 && c<=57){
            let st:i32=i;
            i=i+1;
            let go:i32=1;
            while(go==1 && i<s.len){
                let d:u8=s[i];
                if(d>=48 && d<=57){i=i+1; continue;}
                if(d==46 || d==44){
                    if(i+1<s.len){
                        let e:u8=s[i+1];
                        if(e>=48 && e<=57){i=i+2; continue;}
                    }
                    go=0;
                }else{
                    go=0;
                }
            }
            let en:i32=i;
            while(en>st){
                let t:u8=s[en-1];
                if(t==46 || t==44){en=en-1;}else{break;}
            }
            if(en>st && n[0]<cap){
                p32(tt,n[0]*8,st);
                p32(tt,n[0]*8+4,en-st);
                n[0]=n[0]+1;
            }
        }else{
            i=i+1;
        }
    }
    return;
}

// token byte-compare less-than (tokens are (start,len) into arena ab)
fn qp_tok_lt(ab:[]u8,ao:i32,al:i32,bo:i32,bl:i32)i32 {
    let m:i32=al;
    if(bl<m){m=bl;}
    let k:i32=0;
    while(k<m){
        let x:u8=ab[ao+k];
        let y:u8=ab[bo+k];
        if(x<y){return 1;}
        if(x>y){return 0;}
        k=k+1;
    }
    if(al<bl){return 1;}
    return 0;
}

fn qp_tok_eq(ab:[]u8,ao:i32,al:i32,bb:[]u8,bo:i32,bl:i32)i32 {
    if(al!=bl){return 0;}
    return bsub_eq(ab,ao,bb,bo,al);
}

// insertion sort of the (start,len) table by token bytes
fn qp_sort_toks(ab:[]u8,tt:[]u8,n:i32)void {
    let i:i32=1;
    while(i<n){
        let ks:i32=g32(tt,i*8);
        let kl:i32=g32(tt,i*8+4);
        let j:i32=i-1;
        while(j>=0){
            let js:i32=g32(tt,j*8);
            let jl:i32=g32(tt,j*8+4);
            if(qp_tok_lt(ab,ks,kl,js,jl)==1){
                p32(tt,(j+1)*8,js);
                p32(tt,(j+1)*8+4,jl);
                j=j-1;
            }else{
                break;
            }
        }
        p32(tt,(j+1)*8,ks);
        p32(tt,(j+1)*8+4,kl);
        i=i+1;
    }
    return;
}

// numeric signature: sorted tokens joined with \x01; returns byte length
fn qp_numsig(ab:[]u8,tt:[]u8,n:i32,out:[]u8,at:i32)i32 {
    qp_sort_toks(ab,tt,n);
    let o:i32=at;
    let i:i32=0;
    while(i<n){
        if(i>0){out[o]=1; o=o+1;}
        let so:i32=g32(tt,i*8);
        let sl:i32=g32(tt,i*8+4);
        let k:i32=0;
        while(k<sl){out[o]=ab[so+k]; o=o+1; k=k+1;}
        i=i+1;
    }
    return o-at;
}

// parse H| host lines; ht[pg]=(pos,len) into ha; lowercased defensively
fn qp_parse_hosts(buf:[]u8,np:i32,ha:[]u8,hapos:*i32,ht:[]u8)void {
    let i:i32=0;
    while(i<np){p32(ht,i*8,0); p32(ht,i*8+4,0); i=i+1;}
    let pos:i32=0;
    let ls:i32=0;
    let ll:i32=0;
    let cur:i32=-1;
    while(next_line(buf,&pos,&ls,&ll)==1){
        let ln:i32=ll;
        if(ln>0 && buf[ls+ln-1]==13){ln=ln-1;}
        if(ln>2 && buf[ls]==80 && buf[ls+1]==124){cur=cur+1; continue;}
        if(ln>2 && buf[ls]==72 && buf[ls+1]==124 && cur>=0 && cur<np){
            let hs:i32=ls+2;
            let hl:i32=ln-2;
            while(hl>0 && (buf[hs]==32 || buf[hs]==9)){hs=hs+1; hl=hl-1;}
            while(hl>0 && (buf[hs+hl-1]==32 || buf[hs+hl-1]==9)){hl=hl-1;}
            if(hl>0 && hapos[0]+hl<=ha.len){
                let c:i32=0;
                while(c<hl){
                    let ch:u8=buf[hs+c];
                    if(ch>=65 && ch<=90){ch=(ch as i32+32) as u8;}
                    ha[hapos[0]+c]=ch;
                    c=c+1;
                }
                p32(ht,cur*8,hapos[0]);
                p32(ht,cur*8+4,hl);
                hapos[0]=hapos[0]+hl;
            }
        }
    }
    return;
}

// stoplist: one word per line; '#'-comment lines skipped; stored lowercased
fn qp_stop_load(s:[]u8,sa:[]u8,st:[]u8,cap:i32,n:*i32)void {
    n[0]=0;
    let pos:i32=0;
    let ls:i32=0;
    let ll:i32=0;
    let ap:i32=0;
    while(next_line(s,&pos,&ls,&ll)==1){
        let ln:i32=ll;
        if(ln>0 && s[ls+ln-1]==13){ln=ln-1;}
        let a2:i32=ls;
        let b2:i32=ls+ln;
        while(a2<b2 && (s[a2]==32 || s[a2]==9)){a2=a2+1;}
        while(b2>a2 && (s[b2-1]==32 || s[b2-1]==9)){b2=b2-1;}
        if(b2>a2 && s[a2]!=35 && n[0]<cap && ap+(b2-a2)<=sa.len){
            let c:i32=0;
            while(c<b2-a2){
                let ch:u8=s[a2+c];
                if(ch>=65 && ch<=90){ch=(ch as i32+32) as u8;}
                sa[ap+c]=ch;
                c=c+1;
            }
            p32(st,n[0]*8,ap);
            p32(st,n[0]*8+4,b2-a2);
            n[0]=n[0]+1;
            ap=ap+(b2-a2);
        }
    }
    return;
}

fn qp_stop_has(sa:[]u8,st:[]u8,sn:i32,w:[]u8,ws:i32,wl:i32)i32 {
    let i:i32=0;
    while(i<sn){
        let ps:i32=g32(st,i*8);
        let pl:i32=g32(st,i*8+4);
        if(pl==wl && bsub_eq(sa,ps,w,ws,wl)==1){return 1;}
        i=i+1;
    }
    return 0;
}

// content token set: tokenize(minlen 2), drop stoplist words, sort, dedupe.
// Tokens reference the sentence bytes sb. Returns count in n.
fn qp_content_set(sb:[]u8,sa:[]u8,st:[]u8,sn:i32,ct:[]u8,cap:i32,n:*i32)void {
    n[0]=0;
    let raw:[]u8=nio_alloc(256*8);
    let rn:i32=0;
    tokenize(sb,raw,256,2,&rn);
    let i:i32=0;
    while(i<rn){
        let so:i32=g32(raw,i*8);
        let sl:i32=g32(raw,i*8+4);
        if(n[0]<cap && qp_stop_has(sa,st,sn,sb,so,sl)==0){
            p32(ct,n[0]*8,so);
            p32(ct,n[0]*8+4,sl);
            n[0]=n[0]+1;
        }
        i=i+1;
    }
    nio_free(raw);
    qp_sort_toks(sb,ct,n[0]);
    // dedupe in place
    let w:i32=0;
    let r:i32=0;
    while(r<n[0]){
        let ro:i32=g32(ct,r*8);
        let rl:i32=g32(ct,r*8+4);
        let dup:i32=0;
        if(w>0){
            let wo:i32=g32(ct,(w-1)*8);
            let wl:i32=g32(ct,(w-1)*8+4);
            if(qp_tok_eq(sb,ro,rl,sb,wo,wl)==1){dup=1;}
        }
        if(dup==0){
            p32(ct,w*8,ro);
            p32(ct,w*8+4,rl);
            w=w+1;
        }
        r=r+1;
    }
    n[0]=w;
    return;
}

// Jaccard >= 0.60 via inter*5 >= union*3; both sets sorted+unique; empty fails
fn qp_jacc_ok(ab:[]u8,at:[]u8,an:i32,bb:[]u8,bt:[]u8,bn:i32)i32 {
    let i:i32=0;
    let j:i32=0;
    let inter:i32=0;
    while(i<an && j<bn){
        let ao:i32=g32(at,i*8);
        let al:i32=g32(at,i*8+4);
        let bo:i32=g32(bt,j*8);
        let bl:i32=g32(bt,j*8+4);
        if(qp_tok_eq(ab,ao,al,bb,bo,bl)==1){
            inter=inter+1; i=i+1; j=j+1; continue;
        }
        if(qp_tok_lt(ab,ao,al,bo,bl)==1){i=i+1;}else{j=j+1;}
    }
    let uni:i32=an+bn-inter;
    if(uni<=0){return 0;}
    if(inter*5>=uni*3){return 1;}
    return 0;
}

fn qp_flagged(o_fl:[]u8,o_fln:i32,pg:i32)i32 {
    let i:i32=0;
    while(i<o_fln){
        if(g32(o_fl,i*4)==pg){return 1;}
        i=i+1;
    }
    return 0;
}

// distinct hosts among pages in idx[0..n)
fn qp_nhosts(ht:[]u8,ha:[]u8,idx:[]u8,n:i32)i32 {
    let c:i32=0;
    let i:i32=0;
    while(i<n){
        let pg:i32=g32(idx,i*4);
        let ps:i32=g32(ht,pg*8);
        let pl:i32=g32(ht,pg*8+4);
        let seen:i32=0;
        let k:i32=0;
        while(k<i){
            let qg:i32=g32(idx,k*4);
            let qs:i32=g32(ht,qg*8);
            let ql:i32=g32(ht,qg*8+4);
            if(ql==pl && bsub_eq(ha,qs,ha,ps,pl)==1){seen=1; break;}
            k=k+1;
        }
        if(seen==0){c=c+1;}
        i=i+1;
    }
    return c;
}

// The quarantine candidate pass. Called from cmd_verdict (TRAIN only) when
// the strict verdict did not install. All inputs are the frozen verdict's.
fn qp_quarantine(buf:[]u8,np:i32,pa:[]u8,pt:[]u8,st:[]u8,nst:i32,
    query:[]u8,o_fl:[]u8,o_fln:i32,sd:[]u8)void {
    // stoplist lives in the state dir (glue-copied); missing -> fail closed
    let sok:i32=0;
    let sbuf:[]u8=read_file(sd,"stoplist_para.txt",&sok);
    if(sok==0){return;}
    let sa:[]u8=nio_alloc(4096);
    let stab:[]u8=nio_alloc(256*8);
    let sn:i32=0;
    qp_stop_load(sbuf,sa,stab,256,&sn);
    nio_free(sbuf);
    if(sn==0){nio_free(sa); nio_free(stab); return;}
    let qlow:[]u8=normalize(query);
    let qt:[]u8=nio_alloc(512*8);
    let qn:i32=0;
    tokenize(qlow,qt,512,2,&qn);
    // per-page hosts
    let ha:[]u8=nio_alloc(4096);
    let ht:[]u8=nio_alloc(64*8);
    let hapos:i32=0;
    qp_parse_hosts(buf,np,ha,&hapos,ht);
    // per-page best sentences + features; cand[ ] = page indices admitted
    let ba:[]u8=nio_alloc(64*2048);
    let btab:[]u8=nio_alloc(64*8);
    let bpos:i32=0;
    let nsa:[]u8=nio_alloc(64*512);
    let nstab:[]u8=nio_alloc(64*8);
    let nspos:i32=0;
    let ctab:[]u8=nio_alloc(64*40*8);
    let ctn:[]u8=nio_alloc(64*4);
    let cand:[]u8=nio_alloc(64*4);
    let ncand:i32=0;
    let pg:i32=0;
    while(pg<np && ncand<64){
        if(page_nsent(st,nst,pg)>0 && qp_flagged(o_fl,o_fln,pg)==0){
            let best:[]u8=best_for_page(buf,pg,st,nst,qlow,qt,qn);
            if(best.len>0 && bpos+best.len<=ba.len){
                let c:i32=0;
                while(c<best.len){ba[bpos+c]=best[c]; c=c+1;}
                p32(btab,ncand*8,bpos);
                p32(btab,ncand*8+4,best.len);
                bpos=bpos+best.len;
                // numeric signature over the normalized best sentence bytes
                let bso:i32=g32(btab,ncand*8);
                let bsl:i32=g32(btab,ncand*8+4);
                let bs:[]u8=ba[bso..bso+bsl];
                let ntt:[]u8=nio_alloc(64*8);
                let nn:i32=0;
                qp_numtoks(bs,ntt,64,&nn);
                p32(nstab,ncand*8,nspos);
                let sl2:i32=qp_numsig(bs,ntt,nn,nsa,nspos);
                p32(nstab,ncand*8+4,sl2);
                nspos=nspos+sl2;
                nio_free(ntt);
                // content set
                let cn:i32=0;
                let cco:i32=ncand*40*8;
                let csl:[]u8=ctab[cco..cco+40*8];
                qp_content_set(bs,sa,stab,sn,csl,40,&cn);
                p32(ctn,ncand*4,cn);
                p32(cand,ncand*4,pg);
                ncand=ncand+1;
            }
            nio_free(best);
        }
        pg=pg+1;
    }
    // medoid clustering over admitted candidates
    let win_m:i32=-1;
    let win_n:i32=0;
    let gidx:[]u8=nio_alloc(64*4);
    let wgidx:[]u8=nio_alloc(64*4);
    let m:i32=0;
    while(m<ncand){
        let gn:i32=0;
        let j:i32=0;
        while(j<ncand){
            let ms:i32=g32(nstab,m*8);
            let ml:i32=g32(nstab,m*8+4);
            let js:i32=g32(nstab,j*8);
            let jl:i32=g32(nstab,j*8+4);
            let numeq:i32=0;
            if(ml==jl && bsub_eq(nsa,ms,nsa,js,ml)==1){numeq=1;}
            if(numeq==1){
                let mao:i32=g32(btab,m*8);
                let mal:i32=g32(btab,m*8+4);
                let jao:i32=g32(btab,j*8);
                let jal:i32=g32(btab,j*8+4);
                let ma:[]u8=ba[mao..mao+mal];
                let ja:[]u8=ba[jao..jao+jal];
                let mco:i32=m*40*8;
                let jco:i32=j*40*8;
                let mct:[]u8=ctab[mco..mco+40*8];
                let jct:[]u8=ctab[jco..jco+40*8];
                let mcn:i32=g32(ctn,m*4);
                let jcn:i32=g32(ctn,j*4);
                if(qp_jacc_ok(ma,mct,mcn,ja,jct,jcn)==1){
                    p32(gidx,gn*4,g32(cand,j*4));
                    gn=gn+1;
                }
            }
            j=j+1;
        }
        if(gn>=2 && qp_nhosts(ht,ha,gidx,gn)>=2){
            if(gn>win_n){
                win_n=gn;
                win_m=m;
                let k:i32=0;
                while(k<gn){p32(wgidx,k*4,g32(gidx,k*4)); k=k+1;}
            }
        }
        m=m+1;
    }
    if(win_m>=0){
        _zag_print("QUAR|1|");
        print_pids_csv(pa,pt,wgidx,win_n);
        _zag_print("|");
        let mbo:i32=g32(btab,win_m*8);
        let mbl:i32=g32(btab,win_m*8+4);
        let mb:[]u8=ba[mbo..mbo+mbl];
        _zag_print(mb);
        _zag_println("");
        _zag_print("GATE|PARA|");
        print_pids_csv(pa,pt,wgidx,win_n);
        _zag_println("");
    }
    nio_free(sa);
    nio_free(stab);
    nio_free(qlow);
    nio_free(qt);
    nio_free(ha);
    nio_free(ht);
    nio_free(ba);
    nio_free(btab);
    nio_free(nsa);
    nio_free(nstab);
    nio_free(ctab);
    nio_free(ctn);
    nio_free(cand);
    nio_free(gidx);
    nio_free(wgidx);
    return;
}
