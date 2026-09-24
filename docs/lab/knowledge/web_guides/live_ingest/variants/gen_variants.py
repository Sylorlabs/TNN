#!/usr/bin/env python3
"""Generate the 5 LI BUGFIX-1 head-to-head variant sources from the frozen
canonical webg.zag (or from webg_bf1.zag for the layered variant).

Every edit is an exact string replacement with an asserted occurrence count,
so transcription drift is impossible. Run: python3 gen_variants.py
Writes: ~/workspace/hh/variants_src/webg_{alt1,alt2,alt3,alt4,bf1_alt1}.zag
"""
import os

CANON = '/home/hatch/workspace/tnn-lab/knowledge/web_guides/webg.zag'
BF1SRC = ('/home/hatch/workspace/tnn-lab/knowledge/web_guides/live_ingest/'
          'variants/v-bf1/webg_bf1.zag')
OUTDIR = '/home/hatch/workspace/hh/variants_src'

IMPORT_OLD = '@import("R33_NATIVE_IO_V1.zag")'
IMPORT_NEW = ('@import("R33_NATIVE_IO_V1.zag")\n'
              '@import("R33_NATIVE_SHA256_V2.zag")')

PAGES_MARKER = ('// ---------- pages file: P|pid|title then S|sentence '
                '----------')

GATE_HEAD_OLD = (
    '    let minsrc:i32=dgeti(dt,dn,"MIN-SOURCES",1);\n'
    '    if(minsrc<1){minsrc=1;}\n'
    '    let rc2:i32=0;\n'
    '    if(wn2>=minsrc){'
)
ELSE_OLD = (
    '    }else{\n'
    '        if(loud==1){\n'
    '            _zag_println("ANSWER|UNCHECKABLE");\n'
    '            let j4:i32=0;'
)

PARSE_DEF_OLD = ('fn parse_pages(buf:[]u8,np:*i32,pa:[]u8,papos:*i32,pt:[]u8,'
                 'tt:[]u8,st:[]u8,nst:*i32,maxp:i32,maxs:i32)void {')
PARSE_INIT_OLD = '    np[0]=0;\n    nst[0]=0;\n'
S_CHECK_OLD = ('        }else{\n'
               '            if(ln>2 && buf[ls]==83 && buf[ls+1]==124){')
CALIB_DEF_OLD = ('fn calib_pages(cpages:[]u8,cpn:i32,pa:[]u8,papos:*i32,'
                 'pt:[]u8,tt:[]u8,st:[]u8,nst:*i32,np:*i32)void {')
CALIB_BODY_OLD = ('    parse_pages(cpages[0..cpn],np,pa,papos,pt,tt,st,nst,'
                  '64,512);')
CALIB_CALL_OLD = 'calib_pages(cpages,cpn,pa,&papos,pt,tt,st,&nst,&np);'
PARSE_A_OLD = ('    parse_pages(cpages[0..cpn],&np,pa,&papos,pt,tt,st,&nst,'
               '64,512);')
PARSE_B_OLD = ('    parse_pages(buf,&np,pa,&papos,pt,tt,st,&nst,64,2048);')
VC_DEF_OLD = ('fn verdict_core(buf:[]u8,np:i32,pa:[]u8,pt:[]u8,tt:[]u8,'
              'st:[]u8,nst:i32,')
VC_CALL_OLD = ',np,pa,pt,tt,st,nst,'
FREE_ST_OLD = 'nio_free(st);'

ALT1_FNS = '''// ALT1: context-window hash (ALTERNATIVES.md V-ALT1).
// Supporters of the winning cluster are independent iff the SHA-256 of the
// text around the matched key sentence differs. Context bytes =
// prev ++ 0x1F ++ next, where prev/next are the key sentence's immediate
// neighbors in store order within the page, in stored (original-case) bytes.
// A missing neighbor is replaced by the key sentence itself, so edge
// sentences and single-sentence pages never falsely collapse. The key
// arrives as raw claim text from cluster_best, so it is normalized here;
// candidate sentences are normalized before comparison (symmetric
// normalized-vs-normalized match). Verbatim copies collapse to one vote.
fn ctx_neighbors(pg:i32,buf:[]u8,st:[]u8,nst:i32,key:[]u8,po:*i32,pl:*i32,qo:*i32,ql:*i32)void {
    po[0]=-1;
    pl[0]=0;
    qo[0]=-1;
    ql[0]=0;
    let nkey:[]u8=normalize(key);
    let ks:i32=-1;
    let ko:i32=0;
    let kl:i32=0;
    let s:i32=0;
    while(s<nst){
        if(g32(st,s*12)==pg){
            let so:i32=g32(st,s*12+4);
            let sl:i32=g32(st,s*12+8);
            let nrm:[]u8=normalize(buf[so..so+sl]);
            let hit:i32=0;
            if(nrm.len==nkey.len && nio_equal(nrm,nkey)==1){hit=1;}
            nio_free(nrm);
            if(hit==1){ks=s; ko=so; kl=sl; break;}
        }
        s=s+1;
    }
    nio_free(nkey);
    if(ks<0){return;}
    po[0]=ko;
    pl[0]=kl;
    qo[0]=ko;
    ql[0]=kl;
    if(ks>0 && g32(st,(ks-1)*12)==pg){
        po[0]=g32(st,(ks-1)*12+4);
        pl[0]=g32(st,(ks-1)*12+8);
    }
    if(ks+1<nst && g32(st,(ks+1)*12)==pg){
        qo[0]=g32(st,(ks+1)*12+4);
        ql[0]=g32(st,(ks+1)*12+8);
    }
    return;
}

fn ctx_hash_distinct(widx:[]u8,wn:i32,buf:[]u8,st:[]u8,nst:i32,key:[]u8)i32 {
    let dg:[]u8=nio_alloc(wn*32);
    if(dg.len!=wn*32){return wn;}
    let zi:i32=0;
    while(zi<wn*32){dg[zi]=0; zi=zi+1;}
    let i:i32=0;
    while(i<wn){
        let pg:i32=g32(widx,i*4);
        let po:i32=-1;
        let pl:i32=0;
        let qo:i32=-1;
        let ql:i32=0;
        ctx_neighbors(pg,buf,st,nst,key,&po,&pl,&qo,&ql);
        if(po>=0 && qo>=0){
            let tmp:[]u8=nio_alloc(pl+1+ql);
            if(tmp.len==pl+1+ql){
                let n1:i32=0;
                let c1:i32=0;
                while(c1<pl){tmp[n1]=buf[po+c1]; n1=n1+1; c1=c1+1;}
                tmp[n1]=31;
                n1=n1+1;
                let c3:i32=0;
                while(c3<ql){tmp[n1]=buf[qo+c3]; n1=n1+1; c3=c3+1;}
                let d:[]u8=nio_alloc(32);
                if(d.len==32){
                    if(ns_sha256(tmp,d)==0){
                        let c5:i32=0;
                        while(c5<32){dg[i*32+c5]=d[c5]; c5=c5+1;}
                    }
                }
                nio_free(d);
            }
            nio_free(tmp);
        }
        i=i+1;
    }
    let n2:i32=0;
    let x:i32=0;
    while(x<wn){
        let isnew:i32=1;
        let y:i32=0;
        while(y<x){
            if(nio_equal(dg[x*32..x*32+32],dg[y*32..y*32+32])==1){isnew=0; break;}
            y=y+1;
        }
        if(isnew==1){n2=n2+1;}
        x=x+1;
    }
    nio_free(dg);
    return n2;
}

'''

ALT1_GATE_HEAD = (
    '    let minsrc:i32=dgeti(dt,dn,"MIN-SOURCES",1);\n'
    '    if(minsrc<1){minsrc=1;}\n'
    '    // ALT1 (context-window hash): the winning cluster must span\n'
    '    // >=MIN-SOURCES distinct context hashes (SHA-256 of prev ++ 0x1F\n'
    '    // ++ next around the key sentence); verbatim-copy supporters\n'
    '    // collapse to one vote.\n'
    '    let nctxd:i32=0;\n'
    '    if(wn2>=minsrc){nctxd=ctx_hash_distinct(widx,wn2,buf,st,nst,key);}\n'
    '    let rc2:i32=0;\n'
    '    if(nctxd>=minsrc){'
)
ALT1_ELSE = (
    '    }else{\n'
    '        if(loud==1){\n'
    '            _zag_println("ANSWER|UNCHECKABLE");\n'
    '            if(wn2>=minsrc){\n'
    '                _zag_print("GATE|SRC_CTXDUP|");\n'
    '                print_pids_csv(pa,pt,widx,wn2);\n'
    '                _zag_println("");\n'
    '            }\n'
    '            let j4:i32=0;'
)

ALT2_FNS = '''// ALT2: temporal separation (ALTERNATIVES.md V-ALT2).
// Supporters are independent iff their first-seen timestamps differ by
// >=86400s. Timestamps come from T| lines (glue: fetch time). Pages with no
// T| line each count as their own source (legacy-safe). Transitive collapse
// via union-find over the supporter pairs.
fn tget(tst:[]u8,pg:i32)i64 {
    if(g32(tst,pg*8)==-1){return -1;}
    return g32(tst,pg*8) as i64;
}

fn uf_find(par:[]u8,x:i32)i32 {
    let r:i32=x;
    while(g32(par,r*4)!=r){r=g32(par,r*4);}
    return r;
}

fn time_distinct(widx:[]u8,wn:i32,tst:[]u8)i32 {
    let par:[]u8=nio_alloc(wn*4);
    if(par.len!=wn*4){return wn;}
    let day:i64=86400 as i64;
    let r:i32=0;
    while(r<wn){p32(par,r*4,r); r=r+1;}
    let a:i32=0;
    while(a<wn){
        let ta:i64=tget(tst,g32(widx,a*4));
        let b:i32=a+1;
        while(b<wn){
            let tb:i64=tget(tst,g32(widx,b*4));
            if(ta>=0 && tb>=0){
                let dd:i64=ta-tb;
                if(dd<0){dd=0-dd;}
                if(dd<day){
                    let ra:i32=uf_find(par,a);
                    let rb:i32=uf_find(par,b);
                    if(ra!=rb){p32(par,ra*4,rb);}
                }
            }
            b=b+1;
        }
        a=a+1;
    }
    let nv:i32=0;
    let e:i32=0;
    while(e<wn){
        if(uf_find(par,e)==e){nv=nv+1;}
        e=e+1;
    }
    nio_free(par);
    return nv;
}

'''

ALT2_TLINE = '''            if(ln>2 && buf[ls]==84 && buf[ls+1]==124){
                // T|epoch : first-seen unix time for the most recent P| page
                // (optional; absent => the page counts as its own source).
                if(np[0]>0){
                    let ta:i32=ls+2;
                    let tb:i32=ls+ln;
                    while(ta<tb && (buf[ta]==32 || buf[ta]==9)){ta=ta+1;}
                    while(tb>ta && (buf[tb-1]==32 || buf[tb-1]==9)){tb=tb-1;}
                    if(tb>ta){
                        p32(tst,(np[0]-1)*8,atoi(buf[ta..tb]));
                        p32(tst,(np[0]-1)*8+4,0);
                    }
                }
            }
'''
ALT2_INIT = ('    np[0]=0;\n'
             '    nst[0]=0;\n'
             '    let tz:i32=0;\n'
             '    while(tz<maxp){p32(tst,tz*8,-1); p32(tst,tz*8+4,-1); tz=tz+1;}\n')
ALT2_GATE_HEAD = (
    '    let minsrc:i32=dgeti(dt,dn,"MIN-SOURCES",1);\n'
    '    if(minsrc<1){minsrc=1;}\n'
    '    // ALT2 (temporal separation): the winning cluster must span\n'
    '    // >=MIN-SOURCES time-separated votes (|dt|>=86400s); lockstep\n'
    '    // pages collapse to one vote. Pages with no T| line each count\n'
    '    // as their own source (legacy-safe).\n'
    '    let nvotes:i32=0;\n'
    '    if(wn2>=minsrc){nvotes=time_distinct(widx,wn2,tst);}\n'
    '    let rc2:i32=0;\n'
    '    if(nvotes>=minsrc){'
)
ALT2_ELSE = (
    '    }else{\n'
    '        if(loud==1){\n'
    '            _zag_println("ANSWER|UNCHECKABLE");\n'
    '            if(wn2>=minsrc){\n'
    '                _zag_print("GATE|SRC_TIMELOCK|");\n'
    '                print_pids_csv(pa,pt,widx,wn2);\n'
    '                _zag_println("");\n'
    '            }\n'
    '            let j4:i32=0;'
)

ALT3_FNS = '''// ALT3: provenance disjointness, 1-hop (ALTERNATIVES.md V-ALT3).
// Supporters are independent iff their outlink URL sets are disjoint; any
// shared URL merges the two pages (union over supporter pairs). Pages with
// no L| lines each count as their own source (legacy-safe). Implementable
// reduction of the debated transitive DAG: 1-hop direct outlink sets only.
// Cap: first 32 outlinks per page; beyond-cap URLs ignored (documented).
fn uf_find(par:[]u8,x:i32)i32 {
    let r:i32=x;
    while(g32(par,r*4)!=r){r=g32(par,r*4);}
    return r;
}

fn cite_shared(la:[]u8,lt:[]u8,lc:[]u8,pga:i32,pgb:i32)i32 {
    let na:i32=g32(lc,pga*4);
    let nb:i32=g32(lc,pgb*4);
    if(na<1 || nb<1){return 0;}
    let e1:i32=0;
    while(e1<na){
        let o1:i32=g32(lt,(pga*32+e1)*8);
        let l1:i32=g32(lt,(pga*32+e1)*8+4);
        let e2:i32=0;
        while(e2<nb){
            let o2:i32=g32(lt,(pgb*32+e2)*8);
            let l2:i32=g32(lt,(pgb*32+e2)*8+4);
            if(l1==l2 && nio_equal(la[o1..o1+l1],la[o2..o2+l2])==1){return 1;}
            e2=e2+1;
        }
        e1=e1+1;
    }
    return 0;
}

fn cite_disjoint(widx:[]u8,wn:i32,la:[]u8,lt:[]u8,lc:[]u8)i32 {
    let par:[]u8=nio_alloc(wn*4);
    if(par.len!=wn*4){return wn;}
    let r:i32=0;
    while(r<wn){p32(par,r*4,r); r=r+1;}
    let a:i32=0;
    while(a<wn){
        let b:i32=a+1;
        while(b<wn){
            if(cite_shared(la,lt,lc,g32(widx,a*4),g32(widx,b*4))==1){
                let ra:i32=uf_find(par,a);
                let rb:i32=uf_find(par,b);
                if(ra!=rb){p32(par,ra*4,rb);}
            }
            b=b+1;
        }
        a=a+1;
    }
    let nv:i32=0;
    let e:i32=0;
    while(e<wn){
        if(uf_find(par,e)==e){nv=nv+1;}
        e=e+1;
    }
    nio_free(par);
    return nv;
}

'''

ALT3_LLINE = '''            if(ln>2 && buf[ls]==76 && buf[ls+1]==124){
                // L|url : outlink/citation URL for the most recent P| page.
                // First 32 kept; beyond-cap URLs ignored (documented bound).
                if(np[0]>0){
                    let lpg:i32=np[0]-1;
                    let lcn:i32=g32(lc,lpg*4);
                    if(lcn<32){
                        let lua:i32=ls+2;
                        let lub:i32=ls+ln;
                        while(lua<lub && (buf[lua]==32 || buf[lua]==9)){lua=lua+1;}
                        while(lub>lua && (buf[lub-1]==32 || buf[lub-1]==9)){lub=lub-1;}
                        let lul:i32=lub-lua;
                        if(lul>0 && lapos[0]+lul<=la.len){
                            let lps:i32=lapos[0];
                            let lk:i32=0;
                            while(lk<lul){la[lps+lk]=buf[lua+lk]; lk=lk+1;}
                            lapos[0]=lps+lul;
                            p32(lt,(lpg*32+lcn)*8,lps);
                            p32(lt,(lpg*32+lcn)*8+4,lul);
                            p32(lc,lpg*4,lcn+1);
                        }
                    }
                }
            }
'''
ALT3_INIT = ('    np[0]=0;\n'
             '    nst[0]=0;\n'
             '    let lz:i32=0;\n'
             '    while(lz<maxp){p32(lc,lz*4,0); lz=lz+1;}\n')
ALT3_GATE_HEAD = (
    '    let minsrc:i32=dgeti(dt,dn,"MIN-SOURCES",1);\n'
    '    if(minsrc<1){minsrc=1;}\n'
    '    // ALT3 (provenance disjointness, 1-hop): the winning cluster must\n'
    '    // span >=MIN-SOURCES outlink-disjoint components; any shared URL\n'
    '    // merges pages. Pages with no L| lines each count as their own\n'
    '    // source (legacy-safe).\n'
    '    let ncite:i32=0;\n'
    '    if(wn2>=minsrc){ncite=cite_disjoint(widx,wn2,la,lt,lc);}\n'
    '    let rc2:i32=0;\n'
    '    if(ncite>=minsrc){'
)
ALT3_ELSE = (
    '    }else{\n'
    '        if(loud==1){\n'
    '            _zag_println("ANSWER|UNCHECKABLE");\n'
    '            if(wn2>=minsrc){\n'
    '                _zag_print("GATE|SRC_CITE_SHARED|");\n'
    '                print_pids_csv(pa,pt,widx,wn2);\n'
    '                _zag_println("");\n'
    '            }\n'
    '            let j4:i32=0;'
)

ALT4_FNS = '''// ALT4: metadata quorum (ALTERNATIVES.md V-ALT4).
// Four binary signals over the supporter set: >=2 distinct non-empty
// authors (A|), share platforms (SH|), publishers (PB|), CMS values (CG|).
// Install iff score >= 2. Empty strings never count as a distinct value.
// Backward compat: if no supporter carries any metadata, the gate is inert
// and the frozen page-count rule applies (legacy inputs unaffected).
fn metafin(buf:[]u8,ls:i32,ln:i32)i32 {
    if(ln>2 && buf[ls]==65 && buf[ls+1]==124){return 0;}
    if(ln>3 && buf[ls]==83 && buf[ls+1]==72 && buf[ls+2]==124){return 1;}
    if(ln>3 && buf[ls]==80 && buf[ls+1]==66 && buf[ls+2]==124){return 2;}
    if(ln>3 && buf[ls]==67 && buf[ls+1]==71 && buf[ls+2]==124){return 3;}
    return -1;
}

fn mdistinct(widx:[]u8,wn:i32,ma:[]u8,mx:[]u8,f:i32)i32 {
    let n:i32=0;
    let i:i32=0;
    while(i<wn){
        let pg:i32=g32(widx,i*4);
        let ms:i32=g32(mx,(f*64+pg)*8);
        let ml:i32=g32(mx,(f*64+pg)*8+4);
        if(ml>0){
            let isnew:i32=1;
            let j:i32=0;
            while(j<i){
                let pg2:i32=g32(widx,j*4);
                let ms2:i32=g32(mx,(f*64+pg2)*8);
                let ml2:i32=g32(mx,(f*64+pg2)*8+4);
                if(ml2==ml && nio_equal(ma[ms..ms+ml],ma[ms2..ms2+ml2])==1){isnew=0; break;}
                j=j+1;
            }
            if(isnew==1){n=n+1;}
        }
        i=i+1;
    }
    return n;
}

fn quorum_score(widx:[]u8,wn:i32,ma:[]u8,mx:[]u8,hasmeta:*i32)i32 {
    hasmeta[0]=0;
    let score:i32=0;
    let f:i32=0;
    while(f<4){
        let dc:i32=mdistinct(widx,wn,ma,mx,f);
        if(dc>0){hasmeta[0]=1;}
        if(dc>=2){score=score+1;}
        f=f+1;
    }
    return score;
}

'''

ALT4_MLINE = '''            let mf:i32=metafin(buf,ls,ln);
            if(mf>=0){
                // A|/SH|/PB|/CG| metadata for the most recent P| page
                // (optional; absent => legacy page-count rule). Last wins
                // on repeat fields.
                if(np[0]>0){
                    let mva:i32=ls+2;
                    if(mf>=1){mva=ls+3;}
                    let mvb:i32=ls+ln;
                    while(mva<mvb && (buf[mva]==32 || buf[mva]==9)){mva=mva+1;}
                    while(mvb>mva && (buf[mvb-1]==32 || buf[mvb-1]==9)){mvb=mvb-1;}
                    let mvl:i32=mvb-mva;
                    if(mvl>0 && mapos[0]+mvl<=ma.len){
                        let mvs:i32=mapos[0];
                        let mvk:i32=0;
                        while(mvk<mvl){ma[mvs+mvk]=buf[mva+mvk]; mvk=mvk+1;}
                        mapos[0]=mvs+mvl;
                        p32(mx,(mf*64+np[0]-1)*8,mvs);
                        p32(mx,(mf*64+np[0]-1)*8+4,mvl);
                    }
                }
            }
'''
ALT4_INIT = ('    np[0]=0;\n'
             '    nst[0]=0;\n'
             '    let mz:i32=0;\n'
             '    while(mz<256){p32(mx,mz*8,0); p32(mx,mz*8+4,0); mz=mz+1;}\n')
ALT4_GATE_HEAD = (
    '    let minsrc:i32=dgeti(dt,dn,"MIN-SOURCES",1);\n'
    '    if(minsrc<1){minsrc=1;}\n'
    '    // ALT4 (metadata quorum): install iff >=2 of the 4 metadata\n'
    '    // signals hold (>=2 distinct non-empty authors / share platforms /\n'
    '    // publishers / CMS values). No metadata on any supporter => the\n'
    '    // gate is inert and the frozen page-count rule applies.\n'
    '    let qscore:i32=0;\n'
    '    let qmeta:i32=0;\n'
    '    if(wn2>=minsrc){qscore=quorum_score(widx,wn2,ma,mx,&qmeta);}\n'
    '    let qok:i32=0;\n'
    '    if(wn2>=minsrc){\n'
    '        if(qmeta==0){qok=1;}else{if(qscore>=2){qok=1;}}\n'
    '    }\n'
    '    let rc2:i32=0;\n'
    '    if(qok==1){'
)
ALT4_ELSE = (
    '    }else{\n'
    '        if(loud==1){\n'
    '            _zag_println("ANSWER|UNCHECKABLE");\n'
    '            if(wn2>=minsrc && qmeta==1){\n'
    '                _zag_print("GATE|SRC_QUORUM|");\n'
    '                print_pids_csv(pa,pt,widx,wn2);\n'
    '                _zag_println("");\n'
    '            }\n'
    '            let j4:i32=0;'
)


def rep(src, old, new, count, label):
    c = src.count(old)
    assert c == count, '%s: found %d, expected %d' % (label, c, count)
    return src.replace(old, new)


def add_threading(src, def_params, call_args, calib_inner_args,
                  vc_def_params, vc_call_args,
                  alloc_block, free_block, label):
    # def_params: appended inside parse_pages/calib_pages defs (with types)
    # call_args: appended at outer call sites (names only; &local for *i32)
    # calib_inner_args: passed from calib_pages into parse_pages (params
    #   already *i32 there, so no &)
    # vc_def_params / vc_call_args: same split for verdict_core
    src = rep(src, PARSE_DEF_OLD,
              PARSE_DEF_OLD[:-len(')void {')] + def_params + ')void {',
              1, label + ':parse_def')
    src = rep(src, CALIB_DEF_OLD,
              CALIB_DEF_OLD[:-len(')void {')] + def_params + ')void {',
              1, label + ':calib_def')
    src = rep(src, CALIB_BODY_OLD,
              CALIB_BODY_OLD[:-len(');')] + calib_inner_args + ');',
              1, label + ':calib_body')
    src = rep(src, CALIB_CALL_OLD,
              alloc_block + CALIB_CALL_OLD[:-len(');')] + call_args + ');',
              4, label + ':calib_call')
    src = rep(src, PARSE_A_OLD,
              alloc_block + PARSE_A_OLD[:-len(');')] + call_args + ');',
              1, label + ':parse_a')
    src = rep(src, PARSE_B_OLD,
              alloc_block + PARSE_B_OLD[:-len(');')] + call_args + ');',
              1, label + ':parse_b')
    src = rep(src, VC_DEF_OLD, VC_DEF_OLD + vc_def_params, 1, label + ':vc_def')
    src = rep(src, VC_CALL_OLD, VC_CALL_OLD + vc_call_args, 4,
              label + ':vc_call')
    src = rep(src, FREE_ST_OLD, FREE_ST_OLD + '\n' + free_block, 6,
              label + ':free')
    return src


def build_alt1(base):
    src = base
    src = rep(src, IMPORT_OLD, IMPORT_NEW, 1, 'alt1:import')
    src = rep(src, PAGES_MARKER, ALT1_FNS + PAGES_MARKER, 1, 'alt1:fns')
    src = rep(src, GATE_HEAD_OLD, ALT1_GATE_HEAD, 1, 'alt1:gate')
    src = rep(src, ELSE_OLD, ALT1_ELSE, 1, 'alt1:else')
    return src


def build_alt2(base):
    src = base
    src = rep(src, PAGES_MARKER, ALT2_FNS + PAGES_MARKER, 1, 'alt2:fns')
    src = rep(src, PARSE_INIT_OLD, ALT2_INIT, 1, 'alt2:init')
    src = rep(src, S_CHECK_OLD,
              '        }else{\n' + ALT2_TLINE +
              '            if(ln>2 && buf[ls]==83 && buf[ls+1]==124){',
              1, 'alt2:tline')
    src = rep(src, GATE_HEAD_OLD, ALT2_GATE_HEAD, 1, 'alt2:gate')
    src = rep(src, ELSE_OLD, ALT2_ELSE, 1, 'alt2:else')
    alloc_block = '    let tst:[]u8=nio_alloc(64*8);\n'
    free_block = '    nio_free(tst);'
    src = add_threading(src, ',tst:[]u8', ',tst', ',tst',
                        'tst:[]u8,', 'tst,',
                        alloc_block, free_block, 'alt2')
    return src


def build_alt3(base):
    src = base
    src = rep(src, PAGES_MARKER, ALT3_FNS + PAGES_MARKER, 1, 'alt3:fns')
    src = rep(src, PARSE_INIT_OLD, ALT3_INIT, 1, 'alt3:init')
    src = rep(src, S_CHECK_OLD,
              '        }else{\n' + ALT3_LLINE +
              '            if(ln>2 && buf[ls]==83 && buf[ls+1]==124){',
              1, 'alt3:lline')
    src = rep(src, GATE_HEAD_OLD, ALT3_GATE_HEAD, 1, 'alt3:gate')
    src = rep(src, ELSE_OLD, ALT3_ELSE, 1, 'alt3:else')
    alloc_block = ('    let la:[]u8=nio_alloc(32768);\n'
                   '    let lapos:i32=0;\n'
                   '    let lt:[]u8=nio_alloc(64*32*8);\n'
                   '    let lc:[]u8=nio_alloc(64*4);\n')
    free_block = ('    nio_free(la);\n'
                  '    nio_free(lt);\n'
                  '    nio_free(lc);')
    src = add_threading(src, ',la:[]u8,lapos:*i32,lt:[]u8,lc:[]u8',
                        ',la,&lapos,lt,lc', ',la,lapos,lt,lc',
                        'la:[]u8,lt:[]u8,lc:[]u8,', 'la,lt,lc,',
                        alloc_block, free_block, 'alt3')
    return src


def build_alt4(base):
    src = base
    src = rep(src, PAGES_MARKER, ALT4_FNS + PAGES_MARKER, 1, 'alt4:fns')
    src = rep(src, PARSE_INIT_OLD, ALT4_INIT, 1, 'alt4:init')
    src = rep(src, S_CHECK_OLD,
              '        }else{\n' + ALT4_MLINE +
              '            if(ln>2 && buf[ls]==83 && buf[ls+1]==124){',
              1, 'alt4:mline')
    src = rep(src, GATE_HEAD_OLD, ALT4_GATE_HEAD, 1, 'alt4:gate')
    src = rep(src, ELSE_OLD, ALT4_ELSE, 1, 'alt4:else')
    alloc_block = ('    let ma:[]u8=nio_alloc(16384);\n'
                   '    let mapos:i32=0;\n'
                   '    let mx:[]u8=nio_alloc(4*64*8);\n')
    free_block = ('    nio_free(ma);\n'
                  '    nio_free(mx);')
    src = add_threading(src, ',ma:[]u8,mapos:*i32,mx:[]u8',
                        ',ma,&mapos,mx', ',ma,mapos,mx',
                        'ma:[]u8,mx:[]u8,', 'ma,mx,',
                        alloc_block, free_block, 'alt4')
    return src


BF1_GATE_HEAD_OLD = (
    '    let nsrc:i32=0;\n'
    '    if(wn2>=minsrc){nsrc=nsrc_count(widx,wn2,ha,ht);}\n'
    '    let rc2:i32=0;\n'
    '    if(nsrc>=minsrc){'
)
BF1_GATE_HEAD_NEW = (
    '    // LAYERED BF1+ALT1: the winning cluster must span >=MIN-SOURCES\n'
    '    // distinct hosts (frozen rule: ">=2 INDEPENDENT pages"; pages with\n'
    '    // no H| host each count as their own source) AND >=MIN-SOURCES\n'
    '    // distinct context hashes (ALT1). Either gate firing -> UNCHECKABLE.\n'
    '    let nsrc:i32=0;\n'
    '    let nctxd:i32=0;\n'
    '    if(wn2>=minsrc){nsrc=nsrc_count(widx,wn2,ha,ht); '
    'nctxd=ctx_hash_distinct(widx,wn2,buf,st,nst,key);}\n'
    '    let rc2:i32=0;\n'
    '    if(nsrc>=minsrc && nctxd>=minsrc){'
)
BF1_ELSE_OLD = (
    '            _zag_println("ANSWER|UNCHECKABLE");\n'
    '            if(wn2>=minsrc){\n'
    '                _zag_print("GATE|SRC_INDEPENDENCE|");\n'
    '                print_pids_csv(pa,pt,widx,wn2);\n'
    '                _zag_println("");\n'
    '            }\n'
)
BF1_ELSE_NEW = (
    '            _zag_println("ANSWER|UNCHECKABLE");\n'
    '            if(wn2>=minsrc){\n'
    '                if(nsrc<minsrc){\n'
    '                    _zag_print("GATE|SRC_INDEPENDENCE|");\n'
    '                    print_pids_csv(pa,pt,widx,wn2);\n'
    '                    _zag_println("");\n'
    '                }\n'
    '                if(nctxd<minsrc){\n'
    '                    _zag_print("GATE|SRC_CTXDUP|");\n'
    '                    print_pids_csv(pa,pt,widx,wn2);\n'
    '                    _zag_println("");\n'
    '                }\n'
    '            }\n'
)


def build_bf1_alt1(bf1src):
    src = bf1src
    src = rep(src, IMPORT_OLD, IMPORT_NEW, 1, 'bf1alt1:import')
    src = rep(src, PAGES_MARKER, ALT1_FNS + PAGES_MARKER, 1, 'bf1alt1:fns')
    src = rep(src, BF1_GATE_HEAD_OLD, BF1_GATE_HEAD_NEW, 1, 'bf1alt1:gate')
    src = rep(src, BF1_ELSE_OLD, BF1_ELSE_NEW, 1, 'bf1alt1:else')
    return src


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    base = open(CANON).read()
    bf1src = open(BF1SRC).read()
    variants = {
        'webg_alt1.zag': build_alt1(base),
        'webg_alt2.zag': build_alt2(base),
        'webg_alt3.zag': build_alt3(base),
        'webg_alt4.zag': build_alt4(base),
        'webg_bf1_alt1.zag': build_bf1_alt1(bf1src),
    }
    for fn, src in variants.items():
        p = os.path.join(OUTDIR, fn)
        open(p, 'w').write(src)
        print('wrote %s (%d bytes)' % (p, len(src)))


if __name__ == '__main__':
    main()
