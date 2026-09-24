#!/usr/bin/env python3
"""Generate the five H3 fix forks from novel_base.zag via surgical edits."""
import sys, os

SRC = os.path.expanduser("~/workspace/h4_deep_audit/h3fixes/src")
base = open(os.path.join(SRC, "novel_base.zag"), encoding="utf-8").read()

def sub_once(text, old, new):
    assert text.count(old) == 1, "pattern not unique/found: %r" % old[:60]
    return text.replace(old, new, 1)

# ---------------- common edits for F1,F2,F3,F4b ----------------
def common_edits(zag, kind):
    # C1: lequiv allocation
    zag = sub_once(zag,
        "    let lgrp:[]u8=nio_alloc(MAXLINES*4);\n",
        "    let lgrp:[]u8=nio_alloc(MAXLINES*4);\n    let lequiv:[]u8=nio_alloc(MAXLINES*4);\n")
    # C2: init
    zag = sub_once(zag,
        "        p32(lgrp,zi*4,-1);\n",
        "        p32(lgrp,zi*4,-1);\n        p32(lequiv,zi*4,0);\n")
    # C3: equiv stage in classify + lequiv record
    zag = sub_once(zag,
        """        if(isknown==1){
            p32(judg,cli*4,1);
            p32(lknow,cli*4,kseq);""",
        """        let equivk:i32=0;
        if(isknown==0 && LESION!=2){
            equivk=FIXEQUIVCALL;
            if(equivk>0){isknown=1; kseq=-2;}
        }
        if(isknown==1){
            p32(judg,cli*4,1);
            p32(lknow,cli*4,kseq);
            p32(lequiv,cli*4,equivk);""")
    zag = zag.replace("FIXEQUIVCALL", kind["call"])
    # C4: audit EQUIV flag
    zag = sub_once(zag,
        """        if(aj==1){
            alp=cat(lbuf,alp,"KNOWN|KSEQ=");
            alp=cat(lbuf,alp,i64s(g32(lknow,ali*4) as i64));
        }else{""",
        """        if(aj==1){
            alp=cat(lbuf,alp,"KNOWN|KSEQ=");
            alp=cat(lbuf,alp,i64s(g32(lknow,ali*4) as i64));
            if(g32(lequiv,ali*4)==1){
                alp=cat(lbuf,alp,"|EQUIV=%s");
            }
        }else{""" % kind["tag"])
    # insert helper functions before main
    zag = sub_once(zag, "fn main()i32 {", kind["helpers"] + "\nfn main()i32 {")
    # insert setup code (goes after K load, before corpus parse)
    zag = sub_once(zag,
        "    // ---- parse corpus file ----\n",
        kind["setup"] + "    // ---- parse corpus file ----\n")
    return zag

# ================= F1 =================
F1_HELPERS = r"""
fn f1_equiv(trar:[]u8,trtab:[]u8,trn:i32,n:[]u8)i32 {
    let i:i32=0;
    while(i<trn){
        let eo:i32=g32(trtab,i*12);
        let el:i32=g32(trtab,i*12+4);
        if(el==n.len && beq(trar[eo..eo+el],n)==1){return 1;}
        i=i+1;
    }
    return 0;
}
"""
F1_SETUP = r"""
    // ---- F1: translation-equivalence table ("TR|<seq>|<raw text>") ----
    let trpath:[]u8=_zag_arg(4);
    let trar:[]u8=nio_alloc(1048576);
    let trtab:[]u8=nio_alloc(MAXK*12);
    let trn:i32=0;
    let trpos:i32=0;
    if(trpath.len>0){
        let trok:i32=0;
        let trb:[]u8=read_path(trpath,&trok);
        if(trok==1){
            let tln:i32=0;
            let tls:i32=0;
            let tll:i32=0;
            while(next_line(trb,&tln,&tls,&tll)==1){
                let tl:[]u8=trb[tls..tls+tll];
                if(tl.len>0 && tl[tl.len-1]==13){tl=tl[0..tl.len-1];}
                if(bstart(tl,"TR|")==0){continue;}
                let tp1:i32=find_byte(tl,0,124);
                if(tp1<0){continue;}
                let tp2:i32=find_byte(tl,tp1+1,124);
                if(tp2<0){continue;}
                let tnl:i32=norm_into(nbuf,tl[tp2+1..tl.len]);
                if(trn<MAXK && trpos+tnl<=trar.len){
                    let tj:i32=0;
                    while(tj<tnl){trar[trpos+tj]=nbuf[tj]; tj=tj+1;}
                    p32(trtab,trn*12,trpos);
                    p32(trtab,trn*12+4,tnl);
                    p32(trtab,trn*12+8,trn);
                    trn=trn+1;
                    trpos=trpos+tnl;
                }
            }
        }
    }
"""
f1 = common_edits(base, {"tag": "TRANSLATION",
    "call": "f1_equiv(trar,trtab,trn,nar[cno..cno+cnl])",
    "helpers": F1_HELPERS, "setup": F1_SETUP})
open(os.path.join(SRC, "fix_f1.zag"), "w", encoding="utf-8").write(f1)
print("fix_f1.zag written", len(f1))

# ================= F2 =================
F2_HELPERS = r"""
fn sh_add(shbuf:[]u8,shpos:*i32,shtab:[]u8,shn:*i32,pre:[]u8,suf:[]u8,parity:i32)void {
    let po:i32=shpos[0];
    let i:i32=0;
    while(i<pre.len){shbuf[po+i]=pre[i]; i=i+1;}
    let so:i32=po+pre.len;
    i=0;
    while(i<suf.len){shbuf[so+i]=suf[i]; i=i+1;}
    shpos[0]=so+suf.len;
    let e:i32=shn[0]*20;
    p32(shtab,e,po);
    p32(shtab,e+4,pre.len);
    p32(shtab,e+8,so);
    p32(shtab,e+12,suf.len);
    p32(shtab,e+16,parity);
    shn[0]=shn[0]+1;
    return;
}
fn ax_add(axbuf:[]u8,axpos:*i32,axtab:[]u8,axn:*i32,suf:[]u8)void {
    let so:i32=axpos[0];
    let i:i32=0;
    while(i<suf.len){axbuf[so+i]=suf[i]; i=i+1;}
    axpos[0]=so+suf.len;
    p32(axtab,axn[0]*8,so);
    p32(axtab,axn[0]*8+4,suf.len);
    axn[0]=axn[0]+1;
    return;
}
fn f2_strip_end(s:[]u8)[]u8 {
    let e:i32=s.len;
    while(e>0){
        let c:u8=s[e-1];
        if(c==46 || c==33 || c==63){e=e-1;}else{break;}
    }
    return s[0..e];
}
fn f2_equiv(shbuf:[]u8,shtab:[]u8,shn:i32,axbuf:[]u8,axtab:[]u8,axn:i32,kar:[]u8,ktab:[]u8,kn:i32,n:[]u8)i32 {
    let cur:[]u8=f2_strip_end(n);
    let parity:i32=0;
    let pass:i32=0;
    let anystrip:i32=0;
    while(pass<4){
        let stripped:i32=0;
        let i:i32=0;
        while(i<shn){
            let po:i32=g32(shtab,i*20);
            let pl:i32=g32(shtab,i*20+4);
            let so:i32=g32(shtab,i*20+8);
            let sl:i32=g32(shtab,i*20+12);
            let pa:i32=g32(shtab,i*20+16);
            if(cur.len>pl+sl && bstart(cur,shbuf[po..po+pl])==1 && beq(cur[cur.len-sl..cur.len],shbuf[so..so+sl])==1){
                cur=cur[pl..cur.len-sl];
                parity=parity^pa;
                stripped=1;
                break;
            }
            i=i+1;
        }
        if(stripped==0){
            let a:i32=0;
            while(a<axn){
                let so:i32=g32(axtab,a*8);
                let sl:i32=g32(axtab,a*8+4);
                if(cur.len>sl && beq(cur[cur.len-sl..cur.len],axbuf[so..so+sl])==1){
                    cur=cur[0..cur.len-sl];
                    stripped=1;
                    break;
                }
                a=a+1;
            }
        }
        if(stripped==0){break;}
        anystrip=1;
        pass=pass+1;
    }
    if(anystrip==0){return 0;}
    if(parity==1){return 0;}
    if(k_lookup(kar,ktab,kn,cur)>=0){return 1;}
    let pdot:[]u8=nio_alloc(8192);
    let pi2:i32=0;
    while(pi2<cur.len){pdot[pi2]=cur[pi2]; pi2=pi2+1;}
    pdot[pi2]=46;
    if(k_lookup(kar,ktab,kn,pdot[0..pi2+1])>=0){return 1;}
    return 0;
}
"""
F2_SETUP = r"""
    // ---- F2: SHELLS-v1 (frozen) ----
    let shbuf:[]u8=nio_alloc(4096);
    let shpos:i32=0;
    let shtab:[]u8=nio_alloc(8*20);
    let shn:i32=0;
    sh_add(shbuf,&shpos,shtab,&shn,"it is not the case that the claim that "," is false",0);
    sh_add(shbuf,&shpos,shtab,&shn,"it is not the case that the statement that "," is wrong",0);
    sh_add(shbuf,&shpos,shtab,&shn,"it is not the case that the claim that "," is wrong",0);
    sh_add(shbuf,&shpos,shtab,&shn,"it is not the case that the statement that "," is false",0);
    sh_add(shbuf,&shpos,shtab,&shn,"it is not true that "," is false",0);
    sh_add(shbuf,&shpos,shtab,&shn,"it is false that ","",1);
    sh_add(shbuf,&shpos,shtab,&shn,"it is not true that ","",1);
    sh_add(shbuf,&shpos,shtab,&shn,"it is not the case that ","",1);
    let axbuf:[]u8=nio_alloc(1024);
    let axpos:i32=0;
    let axtab:[]u8=nio_alloc(3*8);
    let axn:i32=0;
    ax_add(axbuf,&axpos,axtab,&axn," is not false");
    ax_add(axbuf,&axpos,axtab,&axn," is not wrong");
    ax_add(axbuf,&axpos,axtab,&axn," is not incorrect");
"""
f2 = common_edits(base, {"tag": "NEGATION",
    "call": "f2_equiv(shbuf,shtab,shn,axbuf,axtab,axn,kar,ktab,kn,nar[cno..cno+cnl])",
    "helpers": F2_HELPERS, "setup": F2_SETUP})
open(os.path.join(SRC, "fix_f2.zag"), "w", encoding="utf-8").write(f2)
print("fix_f2.zag written", len(f2))
print("OK")

# ================= F3 =================
F3_HELPERS = r"""
fn f3_strip_punct(s:[]u8)[]u8 {
    let e:i32=s.len;
    while(e>0){
        let c:u8=s[e-1];
        if(c==46 || c==33 || c==63){e=e-1;}else{break;}
    }
    return s[0..e];
}
fn f3_tok(t:[]u8,offs:[]u8,lens:[]u8,maxw:i32)i32 {
    let nw:i32=0;
    let i:i32=0;
    while(i<t.len){
        if(nw>=maxw){break;}
        while(i<t.len && t[i]==32){i=i+1;}
        if(i>=t.len){break;}
        let s:i32=i;
        while(i<t.len && t[i]!=32){i=i+1;}
        p32(offs,nw*4,s);
        p32(lens,nw*4,i-s);
        nw=nw+1;
    }
    return nw;
}
fn f3_overlap(a:[]u8,b:[]u8,out:[]u8)i32 {
    let ao:[]u8=nio_alloc(1024);
    let al:[]u8=nio_alloc(1024);
    let bo:[]u8=nio_alloc(1024);
    let bl:[]u8=nio_alloc(1024);
    let na:i32=f3_tok(a,ao,al,256);
    let nb:i32=f3_tok(b,bo,bl,256);
    let k:i32=na;
    if(nb<k){k=nb;}
    while(k>=1){
        let so:i32=g32(ao,(na-k)*4);
        let sl:i32=a.len-so;
        let pl:i32=g32(bo,(k-1)*4)+g32(bl,(k-1)*4);
        if(sl==pl && beq(a[so..a.len],b[0..pl])==1){
            let w:i32=0;
            let i:i32=0;
            while(i<a.len){out[w]=a[i]; w=w+1; i=i+1;}
            if(pl<b.len){
                out[w]=32; w=w+1;
                i=pl+1;
                while(i<b.len){out[w]=b[i]; w=w+1; i=i+1;}
            }
            return w;
        }
        k=k-1;
    }
    return -1;
}
fn f3_join(a:[]u8,b:[]u8,conn:[]u8,out:[]u8)i32 {
    let sa:[]u8=f3_strip_punct(a);
    let w:i32=0;
    let i:i32=0;
    while(i<sa.len){out[w]=sa[i]; w=w+1; i=i+1;}
    i=0;
    while(i<conn.len){out[w]=conn[i]; w=w+1; i=i+1;}
    i=0;
    while(i<b.len){out[w]=b[i]; w=w+1; i=i+1;}
    return w;
}
fn f3_pair_match(a:[]u8,b:[]u8,kar:[]u8,ktab:[]u8,kn:i32,tmp:[]u8)i32 {
    let ml:i32=f3_overlap(a,b,tmp);
    if(ml>=0 && k_lookup(kar,ktab,kn,tmp[0..ml])>=0){return 1;}
    let jl:i32=f3_join(a,b,"",tmp);
    if(k_lookup(kar,ktab,kn,tmp[0..jl])>=0){return 1;}
    jl=f3_join(a,b," ",tmp);
    if(k_lookup(kar,ktab,kn,tmp[0..jl])>=0){return 1;}
    jl=f3_join(a,b,", ",tmp);
    if(k_lookup(kar,ktab,kn,tmp[0..jl])>=0){return 1;}
    jl=f3_join(a,b,", so ",tmp);
    if(k_lookup(kar,ktab,kn,tmp[0..jl])>=0){return 1;}
    jl=f3_join(a,b,", and ",tmp);
    if(k_lookup(kar,ktab,kn,tmp[0..jl])>=0){return 1;}
    jl=f3_join(a,b,"; ",tmp);
    if(k_lookup(kar,ktab,kn,tmp[0..jl])>=0){return 1;}
    return 0;
}
fn f3_triple_match(a:[]u8,b:[]u8,c:[]u8,kar:[]u8,ktab:[]u8,kn:i32,tmp:[]u8,tmp2:[]u8)i32 {
    let ml:i32=f3_overlap(a,b,tmp2);
    if(ml>=0 && f3_pair_match(tmp2[0..ml],c,kar,ktab,kn,tmp)==1){return 1;}
    ml=f3_join(a,b,"",tmp2);
    if(f3_pair_match(tmp2[0..ml],c,kar,ktab,kn,tmp)==1){return 1;}
    ml=f3_join(a,b," ",tmp2);
    if(f3_pair_match(tmp2[0..ml],c,kar,ktab,kn,tmp)==1){return 1;}
    ml=f3_join(a,b,", ",tmp2);
    if(f3_pair_match(tmp2[0..ml],c,kar,ktab,kn,tmp)==1){return 1;}
    ml=f3_join(a,b,", so ",tmp2);
    if(f3_pair_match(tmp2[0..ml],c,kar,ktab,kn,tmp)==1){return 1;}
    ml=f3_join(a,b,", and ",tmp2);
    if(f3_pair_match(tmp2[0..ml],c,kar,ktab,kn,tmp)==1){return 1;}
    ml=f3_join(a,b,"; ",tmp2);
    if(f3_pair_match(tmp2[0..ml],c,kar,ktab,kn,tmp)==1){return 1;}
    return 0;
}
fn f3_mark_known(judg:[]u8,lequiv:[]u8,lknow:[]u8,kgtab:[]u8,kgn:*i32,known_ct:*i32,nar:[]u8,ltab:[]u8,li:i32)void {
    p32(judg,li*4,1);
    p32(lknow,li*4,-2);
    p32(lequiv,li*4,1);
    let cno:i32=g32(ltab,li*24+8);
    let cnl:i32=g32(ltab,li*24+12);
    let kfi:i32=0;
    let kfound:i32=0;
    while(kfi<kgn[0]){
        let kfo:i32=g32(kgtab,kfi*8);
        let kfl:i32=g32(kgtab,kfi*8+4);
        if(kfl==cnl && beq(nar[kfo..kfo+kfl],nar[cno..cno+cnl])==1){kfound=1; break;}
        kfi=kfi+1;
    }
    if(kfound==0){
        p32(kgtab,kgn[0]*8,cno);
        p32(kgtab,kgn[0]*8+4,cnl);
        kgn[0]=kgn[0]+1;
        known_ct[0]=known_ct[0]+1;
    }
    return;
}
"""
# F3 needs a custom insertion: the reassembly pass goes between classify and corroboration,
# and it does NOT use the single-sentence equiv stage. So build F3 manually.
f3 = base
# C1, C2, C4 only (no C3 single-sentence stage)
f3 = sub_once(f3,
    "    let lgrp:[]u8=nio_alloc(MAXLINES*4);\n",
    "    let lgrp:[]u8=nio_alloc(MAXLINES*4);\n    let lequiv:[]u8=nio_alloc(MAXLINES*4);\n")
f3 = sub_once(f3,
    "        p32(lgrp,zi*4,-1);\n",
    "        p32(lgrp,zi*4,-1);\n        p32(lequiv,zi*4,0);\n")
f3 = sub_once(f3,
    """        if(aj==1){
            alp=cat(lbuf,alp,"KNOWN|KSEQ=");
            alp=cat(lbuf,alp,i64s(g32(lknow,ali*4) as i64));
        }else{""",
    """        if(aj==1){
            alp=cat(lbuf,alp,"KNOWN|KSEQ=");
            alp=cat(lbuf,alp,i64s(g32(lknow,ali*4) as i64));
            if(g32(lequiv,ali*4)==1){
                alp=cat(lbuf,alp,"|EQUIV=COMPOSED");
            }
        }else{""")
f3 = sub_once(f3, "fn main()i32 {", F3_HELPERS + "\nfn main()i32 {")
# Insert the reassembly pass between classify loop and corroboration
F3_PASS = r"""
    // ---- F3: compositional reassembly R-v1 (post-classify pass) ----
    let f3tmp:[]u8=nio_alloc(8192);
    let f3tmp2:[]u8=nio_alloc(8192);
    let f3idx:[]u8=nio_alloc(MAXLINES*4);
    let fpi:i32=0;
    while(fpi<pn){
        if((g32(ptab,fpi*12+8)&3)==0){
            let f3n:i32=0;
            let fli:i32=0;
            while(fli<lnc){
                if(g32(ltab,fli*24)==fpi && g32(ltab,fli*24+4)==2 && g32(judg,fli*4)==2){
                    p32(f3idx,f3n*4,fli);
                    f3n=f3n+1;
                }
                fli=fli+1;
            }
            let fti:i32=0;
            while(fti+2<f3n){
                let ia:i32=g32(f3idx,fti*4);
                let ib:i32=g32(f3idx,(fti+1)*4);
                let ic:i32=g32(f3idx,(fti+2)*4);
                if(g32(judg,ia*4)==2 && g32(judg,ib*4)==2 && g32(judg,ic*4)==2){
                    let ao:i32=g32(ltab,ia*24+8);
                    let al:i32=g32(ltab,ia*24+12);
                    let bo:i32=g32(ltab,ib*24+8);
                    let bl:i32=g32(ltab,ib*24+12);
                    let co:i32=g32(ltab,ic*24+8);
                    let cl:i32=g32(ltab,ic*24+12);
                    if(f3_triple_match(nar[ao..ao+al],nar[bo..bo+bl],nar[co..co+cl],kar,ktab,kn,f3tmp,f3tmp2)==1){
                        f3_mark_known(judg,lequiv,lknow,kgtab,&kgn,&known_ct,nar,ltab,ia);
                        f3_mark_known(judg,lequiv,lknow,kgtab,&kgn,&known_ct,nar,ltab,ib);
                        f3_mark_known(judg,lequiv,lknow,kgtab,&kgn,&known_ct,nar,ltab,ic);
                    }
                }
                fti=fti+1;
            }
            let fqi:i32=0;
            while(fqi+1<f3n){
                let ja:i32=g32(f3idx,fqi*4);
                let jb:i32=g32(f3idx,(fqi+1)*4);
                if(g32(judg,ja*4)==2 && g32(judg,jb*4)==2){
                    let ao2:i32=g32(ltab,ja*24+8);
                    let al2:i32=g32(ltab,ja*24+12);
                    let bo2:i32=g32(ltab,jb*24+8);
                    let bl2:i32=g32(ltab,jb*24+12);
                    if(f3_pair_match(nar[ao2..ao2+al2],nar[bo2..bo2+bl2],kar,ktab,kn,f3tmp)==1){
                        f3_mark_known(judg,lequiv,lknow,kgtab,&kgn,&known_ct,nar,ltab,ja);
                        f3_mark_known(judg,lequiv,lknow,kgtab,&kgn,&known_ct,nar,ltab,jb);
                    }
                }
                fqi=fqi+1;
            }
        }
        fpi=fpi+1;
    }

"""
f3 = sub_once(f3,
    "    // ---- corroboration: group candidates by normalized bytes ----\n",
    F3_PASS + "    // ---- corroboration: group candidates by normalized bytes ----\n")
open(os.path.join(SRC, "fix_f3.zag"), "w", encoding="utf-8").write(f3)
print("fix_f3.zag written", len(f3))

# ================= F4b =================
F4B_HELPERS = r"""
fn f4b_tok(t:[]u8,offs:[]u8,lens:[]u8,maxw:i32)i32 {
    let nw:i32=0;
    let i:i32=0;
    while(i<t.len){
        if(nw>=maxw){break;}
        while(i<t.len && t[i]==32){i=i+1;}
        if(i>=t.len){break;}
        let s:i32=i;
        while(i<t.len && t[i]!=32){i=i+1;}
        p32(offs,nw*4,s);
        p32(lens,nw*4,i-s);
        nw=nw+1;
    }
    return nw;
}
fn f4b_nonce_shape(t:[]u8)i32 {
    if(t.len<2){return 0;}
    let i:i32=0;
    while(i<t.len){
        let c:u8=t[i];
        let ok:i32=0;
        if(c>=65 && c<=90){ok=1;}
        if(c>=48 && c<=57){ok=1;}
        if(c==45){ok=1;}
        if(ok==0){return 0;}
        i=i+1;
    }
    return 1;
}
fn f4b_vocab_has(vbuf:[]u8,vtab:[]u8,vn:i32,t:[]u8)i32 {
    let i:i32=0;
    while(i<vn){
        let vo:i32=g32(vtab,i*8);
        let vl:i32=g32(vtab,i*8+4);
        if(vl==t.len && beq(vbuf[vo..vo+vl],t)==1){return 1;}
        i=i+1;
    }
    return 0;
}
fn f4b_strip_punct(t:[]u8)[]u8 {
    let e:i32=t.len;
    while(e>0){
        let c:u8=t[e-1];
        if(c==46 || c==33 || c==63 || c==44 || c==59 || c==58){e=e-1;}else{break;}
    }
    return t[0..e];
}
fn f4b_equiv(cn:[]u8,cr:[]u8,kar:[]u8,ktab:[]u8,kn:i32,vbuf:[]u8,vtab:[]u8,vn:i32)i32 {
    let cno:[]u8=nio_alloc(1024);
    let cnl:[]u8=nio_alloc(1024);
    let cro:[]u8=nio_alloc(1024);
    let crl:[]u8=nio_alloc(1024);
    let ko:[]u8=nio_alloc(1024);
    let kl:[]u8=nio_alloc(1024);
    let nn:i32=f4b_tok(cn,cno,cnl,256);
    let nr:i32=f4b_tok(cr,cro,crl,256);
    if(nn!=nr || nn==0){return 0;}
    let ki:i32=0;
    while(ki<kn){
        let kbo:i32=g32(ktab,ki*12);
        let kbl:i32=g32(ktab,ki*12+4);
        let kr:[]u8=kar[kbo..kbo+kbl];
        let nk:i32=f4b_tok(kr,ko,kl,256);
        let p:i32=0;
        while(p<nn && p<nk){
            let cto:i32=g32(cno,p*4);
            let ctl:i32=g32(cnl,p*4);
            let kto:i32=g32(ko,p*4);
            let ktl:i32=g32(kl,p*4);
            let ct:[]u8=f4b_strip_punct(cn[cto..cto+ctl]);
            let kt:[]u8=f4b_strip_punct(kr[kto..kto+ktl]);
            if(ct.len!=kt.len || beq(ct,kt)==0){break;}
            p=p+1;
        }
        let s:i32=0;
        while(s<nn-p && s<nk-p){
            let ci:i32=nn-1-s;
            let kj:i32=nk-1-s;
            let cto:i32=g32(cno,ci*4);
            let ctl:i32=g32(cnl,ci*4);
            let kto:i32=g32(ko,kj*4);
            let ktl:i32=g32(kl,kj*4);
            let ct:[]u8=f4b_strip_punct(cn[cto..cto+ctl]);
            let kt:[]u8=f4b_strip_punct(kr[kto..kto+ktl]);
            if(ct.len!=kt.len || beq(ct,kt)==0){break;}
            s=s+1;
        }
        let fixed:i32=p+s;
        let cmid_len:i32=nn-s-p;
        let kmid_len:i32=nk-s-p;
        if(fixed>=8 && kmid_len>=1 && kmid_len<=5 && cmid_len>=1 && cmid_len<=5){
            let has_nonce:i32=0;
            let mi:i32=p;
            while(mi<nn-s){
                let rto:i32=g32(cro,mi*4);
                let rtl:i32=g32(crl,mi*4);
                let nto:i32=g32(cno,mi*4);
                let ntl:i32=g32(cnl,mi*4);
                let rtok:[]u8=f4b_strip_punct(cr[rto..rto+rtl]);
                let ntok:[]u8=f4b_strip_punct(cn[nto..nto+ntl]);
                if(f4b_nonce_shape(rtok)==1 && f4b_vocab_has(vbuf,vtab,vn,ntok)==0){
                    has_nonce=1;
                    break;
                }
                mi=mi+1;
            }
            if(has_nonce==1){return 1;}
        }
        ki=ki+1;
    }
    return 0;
}
"""
F4B_SETUP = r"""
    // ---- F4b: K vocabulary (normed word tokens, deduped) ----
    let vbuf:[]u8=nio_alloc(1048576);
    let vtab:[]u8=nio_alloc(8192*8);
    let vn:i32=0;
    let vpos:i32=0;
    let vki:i32=0;
    while(vki<kn){
        let vko:i32=g32(ktab,vki*12);
        let vkl:i32=g32(ktab,vki*12+4);
        let vkr:[]u8=kar[vko..vko+vkl];
        let vo:[]u8=nio_alloc(1024);
        let vl:[]u8=nio_alloc(1024);
        let vnw:i32=f4b_tok(vkr,vo,vl,256);
        let vj:i32=0;
        while(vj<vnw){
            let to:i32=g32(vo,vj*4);
            let tl:i32=g32(vl,vj*4);
            let ttok:[]u8=vkr[to..to+tl];
            if(f4b_vocab_has(vbuf,vtab,vn,ttok)==0 && vn<8192 && vpos+tl<=vbuf.len){
                let vk:i32=0;
                while(vk<tl){vbuf[vpos+vk]=ttok[vk]; vk=vk+1;}
                p32(vtab,vn*8,vpos);
                p32(vtab,vn*8+4,tl);
                vn=vn+1;
                vpos=vpos+tl;
            }
            vj=vj+1;
        }
        vki=vki+1;
    }
"""
f4b = common_edits(base, {"tag": "NONCE_TEMPLATE",
    "call": "f4b_equiv(nar[cno..cno+cnl],rar[g32(ltab,cli*24+16)..g32(ltab,cli*24+16)+g32(ltab,cli*24+20)],kar,ktab,kn,vbuf,vtab,vn)",
    "helpers": F4B_HELPERS, "setup": F4B_SETUP})
open(os.path.join(SRC, "fix_f4b.zag"), "w", encoding="utf-8").write(f4b)
print("fix_f4b.zag written", len(f4b))

# ================= F5 =================
F5_NORM = r"""
fn skel_fold(cp:i32)u8 {
    if(cp==1072){return 97;}
    if(cp==1077){return 101;}
    if(cp==1086){return 111;}
    if(cp==1088){return 112;}
    if(cp==1089){return 99;}
    if(cp==1093){return 120;}
    if(cp==1110){return 105;}
    if(cp==1112){return 106;}
    if(cp==1109){return 115;}
    if(cp==1082){return 107;}
    if(cp==1084){return 109;}
    if(cp==1085){return 104;}
    if(cp==1090){return 116;}
    if(cp==1091){return 121;}
    if(cp==945){return 97;}
    if(cp==949){return 101;}
    if(cp==959){return 111;}
    if(cp==961){return 112;}
    return 0;
}
fn norm_into(dst:[]u8,s:[]u8)i32 {
    let w:i32=0;
    let i:i32=0;
    let pending:i32=0;
    while(i<s.len){
        let b:u8=s[i];
        if(b<128){
            if(is_ws(b)==1){pending=1; i=i+1; continue;}
            if(pending==1 && w>0){dst[w]=32; w=w+1;}
            pending=0;
            dst[w]=fold_byte(b);
            w=w+1;
            i=i+1;
            continue;
        }
        let cp:i32=-1;
        let seqlen:i32=0;
        if(b>=192 && b<=223 && i+1<s.len){
            let b1:u8=s[i+1];
            if(b1>=128 && b1<=191){
                cp=((b as i32)-192)*64+((b1 as i32)-128);
                seqlen=2;
            }
        }
        if(cp<0 && b>=224 && b<=239 && i+2<s.len){
            let b1:u8=s[i+1];
            let b2:u8=s[i+2];
            if(b1>=128 && b1<=191 && b2>=128 && b2<=191){
                cp=((b as i32)-224)*4096+(((b1 as i32)-128)*64)+((b2 as i32)-128);
                seqlen=3;
            }
        }
        if(cp<0 && b>=240 && b<=244 && i+3<s.len){
            let b1:u8=s[i+1];
            let b2:u8=s[i+2];
            let b3:u8=s[i+3];
            if(b1>=128 && b1<=191 && b2>=128 && b2<=191 && b3>=128 && b3<=191){
                cp=((b as i32)-240)*262144+(((b1 as i32)-128)*4096)+(((b2 as i32)-128)*64)+((b3 as i32)-128);
                seqlen=4;
            }
        }
        if(cp<0){
            if(b==160){pending=1; i=i+1; continue;}
            if(pending==1 && w>0){dst[w]=32; w=w+1;}
            pending=0;
            dst[w]=b;
            w=w+1;
            i=i+1;
            continue;
        }
        if(cp==8203 || cp==8204 || cp==8205 || cp==65279 || cp==8288 || cp==6158 || cp==173){
            i=i+seqlen;
            continue;
        }
        if((cp>=8234 && cp<=8238) || (cp>=8294 && cp<=8297)){
            i=i+seqlen;
            continue;
        }
        if(cp>=65281 && cp<=65374){
            let ab:u8=((cp-65248) as u8);
            if(pending==1 && w>0){dst[w]=32; w=w+1;}
            pending=0;
            dst[w]=fold_byte(ab);
            w=w+1;
            i=i+seqlen;
            continue;
        }
        if(cp==12288 || cp==160){
            pending=1;
            i=i+seqlen;
            continue;
        }
        let sk:u8=skel_fold(cp);
        if(sk!=0){
            if(pending==1 && w>0){dst[w]=32; w=w+1;}
            pending=0;
            dst[w]=fold_byte(sk);
            w=w+1;
            i=i+seqlen;
            continue;
        }
        if(pending==1 && w>0){dst[w]=32; w=w+1;}
        pending=0;
        let k:i32=0;
        while(k<seqlen){dst[w]=s[i+k]; w=w+1; k=k+1;}
        i=i+seqlen;
    }
    return w;
}
"""
f5 = base
# replace norm_into (keep the original fn signature line, replace body)
old_norm = '''fn norm_into(dst:[]u8,s:[]u8)i32 {
    let w:i32=0;
    let i:i32=0;
    let pending:i32=0;
    while(i<s.len){
        let c:u8=s[i];
        if(is_ws(c)==1){
            pending=1;
            i=i+1;
            continue;
        }
        if(pending==1 && w>0){
            dst[w]=32;
            w=w+1;
            pending=0;
        }
        if(pending==1){pending=0;}
        dst[w]=fold_byte(c);
        w=w+1;
        i=i+1;
    }
    return w;
}'''
assert f5.count(old_norm) == 1
f5 = f5.replace(old_norm, F5_NORM.strip(), 1)
open(os.path.join(SRC, "fix_f5.zag"), "w", encoding="utf-8").write(f5)
print("fix_f5.zag written", len(f5))
