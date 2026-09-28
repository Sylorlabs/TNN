#!/usr/bin/env python3
"""Surgical edits to B4's r12_classify -> merged V4 r12_classify."""
import sys

body = open('/tmp/b4_r12.txt').read()

def rep(old, new, count=1):
    global body
    assert body.count(old) == count, f"pattern found {body.count(old)}x (want {count}): {old[:70]!r}"
    body = body.replace(old, new)

# Edit 1: scratch carves for B1/B3 extras (all below B4's cond area at 100000)
rep("""    let AFFB:[]u8=sc[97920..97928];""",
"""    let AFFB:[]u8=sc[97920..97928];
    // V4-INTEG extras (B1/B3), all below B4's conditional area [100000,...).
    let CADJB:[]u8=sc[97928..97992];
    let SUBJA:[]u8=sc[97992..98056];
    let CVB:[]u8=sc[98056..98568];
    let SSTEMB:[]u8=sc[98568..99080];
    let SSTMC:[]u8=sc[99080..99976];""")

# Edit 2: B3 short-stem list after the deduped claim stem set
rep("""    // strip leading gerund ("Drinking coffee causes..." -> core without Drinking)""",
"""    // B3-CAU: short stems ("dam","fog") that the content-word filter drops.
    let nsst:i32=0;
    let ssoff:i32=0;
    i=0;
    while(i<nct){
        let ssto:i32=a_get(TOKA,2*i);
        let sstl:i32=a_get(TOKA,2*i+1);
        let ssll:i32=lower_copy(claim[ssto..ssto+sstl],TMPS);
        if(in_list(TMPS[0..ssll],lex_stop())==0 && ssll>0 && ssll<=4 && nsst<56){
            let sssl:i32=z_stem(claim[ssto..ssto+sstl],OUTS,TMPS,VBS);
            if(sssl>0 && sssl<=24){
                let ssq:i32=0;
                while(ssq<sssl){SSTEMB[ssoff+ssq]=OUTS[ssq];ssq=ssq+1;}
                a_put(SSTMC,2*nsst,ssoff);
                a_put(SSTMC,2*nsst+1,sssl);
                ssoff=ssoff+sssl;
                nsst=nsst+1;
            }
        }
        i=i+1;
    }
    // strip leading gerund ("Drinking coffee causes..." -> core without Drinking)""")

# Edit 3: B1 reporting-verb fallback before the aux/copula fallback
rep("""    if(pfound==0){
        // fallback: first auxiliary/copula among ALL tokens""",
"""    if(pfound==0){
        // B1-V4: fall back to a reporting verb rather than no predicate at
        // all ("None of the trials showed benefits" needs pred="show").
        let ri:i32=cs;
        while(ri<nw){
            let rso:i32=a_get(WORDA,4*ri+2);
            let rsl:i32=a_get(WORDA,4*ri+3);
            let rs3:[]u8=STEMA[rso..rso+rsl];
            if(in_list(rs3,lex_verb())==1){
                pred=rs3;
                pfound=1;
                break;
            }
            ri=ri+1;
        }
    }
    if(pfound==0){
        // fallback: first auxiliary/copula among ALL tokens""")

# Edit 4: B1 cadj + shared subjA + B3 cneg/cauflag/cv, after the aux fallback.
# Anchor: end of the aux-fallback block.
old_aux_tail = """            if(in_list(lw4,lex_be())==1){pred="be";break;}
            if(in_list(lw4,lex_have())==1){pred="have";break;}
            fi=fi+1;
        }
    }
    // ---- overlap gate on the whole text ----"""
new_aux_tail = """            if(in_list(lw4,lex_be())==1){pred="be";break;}
            if(in_list(lw4,lex_have())==1){pred="have";break;}
            fi=fi+1;
        }
    }
    // B1-V4: claim copula-complement stem ("The drug is ineffective" ->
    // "ineffect"), for "not un-X" resolution and "no longer" polarity.
    let cadj:[]u8="";
    let bi:i32=0;
    while(bi<nct){
        let bto:i32=a_get(TOKA,2*bi);
        let btl:i32=a_get(TOKA,2*bi+1);
        let bll:i32=lower_copy(claim[bto..bto+btl],TMPS);
        if(in_list(TMPS[0..bll],lex_be())==1){
            let bk:i32=bi+1;
            while(bk<nct){
                let kto:i32=a_get(TOKA,2*bk);
                let ktl:i32=a_get(TOKA,2*bk+1);
                if(z_cplen(claim[kto..kto+ktl])>3){
                    let kll:i32=lower_copy(claim[kto..kto+ktl],TMPS);
                    if(in_list(TMPS[0..kll],lex_stop())==0){
                        let ksl:i32=z_stem(claim[kto..kto+ktl],OUTS,TMPS,VBS);
                        let kq:i32=0;
                        while(kq<ksl){CADJB[kq]=OUTS[kq];kq=kq+1;}
                        cadj=CADJB[0..ksl];
                        break;
                    }
                }
                bk=bk+1;
            }
            break;
        }
        bi=bi+1;
    }
    // Subject anchor = first non-stop claim token's stem. ("Tea" is too
    // short for the content-word filter, but the cleft rule needs the
    // claim's subject: "It is not tea but coffee that causes cancer".)
    // V4-INTEG: one shared SUBJA for B1's cleft rule and B3's causal
    // helpers (mechanism, prevent, competitor, short-subject).
    let subjA:[]u8=firstA;
    let sj2:i32=0;
    while(sj2<nct){
        let jto:i32=a_get(TOKA,2*sj2);
        let jtl:i32=a_get(TOKA,2*sj2+1);
        let jll:i32=lower_copy(claim[jto..jto+jtl],TMPS);
        if(in_list(TMPS[0..jll],lex_stop())==0){
            let jsl:i32=z_stem(claim[jto..jto+jtl],OUTS,TMPS,VBS);
            if(jsl>0 && jsl<=24){
                let jsq:i32=0;
                while(jsq<jsl){SUBJA[jsq]=OUTS[jsq];jsq=jsq+1;}
                subjA=SUBJA[0..jsl];
                break;
            }
        }
        sj2=sj2+1;
    }
    // B3-CAU: claim polarity, causal flag, mechanism verb.
    let cneg:i32=0;
    if(pred.len>0){
        cneg=claim_neg(claim,TOKA,nct,pred,OUTS,TMPS,VBS);
    }
    let cauflag:i32=claim_causal(claim,TOKA,nct,pred,TMPS);
    let cvl:i32=0;
    if(cauflag==1){
        cvl=causal_verb(claim,TOKA,nct,CVB,TMPS,OUTS,VBS);
    }
    let cv:[]u8=CVB[0..cvl];
    // ---- overlap gate on the whole text ----"""
rep(old_aux_tail, new_aux_tail)

# Edit 5: B3 trailing-e bridge in the overlap gate
rep("""        if(in_stems(STEMA[so6..so6+sl6],STEMB,TSTMB,ntstm)==1){inter=inter+1;}
        i=i+1;""",
"""        let cs6:[]u8=STEMA[so6..so6+sl6];
        if(in_stems(cs6,STEMB,TSTMB,ntstm)==1){inter=inter+1;}
        else{
            // B3-CAU V4-R2 trailing-e bridge: the stemmer keeps a trailing
            // "e" on verb stems ("exercise") but strips it on nouns
            // ("exercis"), so cross-claim/evidence stem matching fails.
            // Retry with the trailing "e" stripped.
            if(sl6>2 && (STEMA[so6+sl6-1] as i32)==101){
                if(in_stems(STEMA[so6..so6+sl6-1],STEMB,TSTMB,ntstm)==1){inter=inter+1;}
            }
        }
        i=i+1;""")

# Edit 6: merged scan_text calls
rep("""    let dr:i32=scan_text(title,STEMA,CSTEMA,ncs,STEMB,TSTMB,ntstm,firstA,lastA,pred,need,NUMA,nnums,claim,CLAUA,PROTB,TOKC,STEMC,CSTMC,LOWB,CLVB,TMPS,OUTS,VBS,AFFB,tsup,Qc,sc);
    if(dr!=0){return 32+dr;}
    dr=scan_text(snip,STEMA,CSTEMA,ncs,STEMB,TSTMB,ntstm,firstA,lastA,pred,need,NUMA,nnums,claim,CLAUA,PROTB,TOKC,STEMC,CSTMC,LOWB,CLVB,TMPS,OUTS,VBS,AFFB,tsup,Qc,sc);
    if(dr!=0){return 32+dr;}
    if(AFFB[0]==1){return 16+5;}""",
"""    let dr:i32=scan_text(title,STEMA,CSTEMA,ncs,STEMB,TSTMB,ntstm,firstA,lastA,pred,cadj,subjA,need,NUMA,nnums,claim,CLAUA,PROTB,TOKC,STEMC,CSTMC,LOWB,CLVB,TMPS,OUTS,VBS,AFFB,cneg,cauflag,cv,SSTEMB,SSTMC,nsst,tsup,Qc,sc);
    if(dr!=0){return 32+dr;}
    dr=scan_text(snip,STEMA,CSTEMA,ncs,STEMB,TSTMB,ntstm,firstA,lastA,pred,cadj,subjA,need,NUMA,nnums,claim,CLAUA,PROTB,TOKC,STEMC,CSTMC,LOWB,CLVB,TMPS,OUTS,VBS,AFFB,cneg,cauflag,cv,SSTEMB,SSTMC,nsst,tsup,Qc,sc);
    if(dr!=0){return 32+dr;}
    // B2-CON: numeric guard (constrained DENY-only; abstain is neutral).
    let ng:i32=numeric_guard(claim,title,snip);
    if(ng==2){return 32+10;}
    if(AFFB[0]==1){return 16+5;}""")

open('/tmp/v4_r12.txt', 'w').write(body)
print("edits applied, merged r12_classify bytes:", len(body))
