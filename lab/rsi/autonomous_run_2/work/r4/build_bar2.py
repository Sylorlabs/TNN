#!/usr/bin/env python3
"""Build probe_bar2: focused 2-rule search for BAR-refusal cases.
Rule1 in {14 one-rule fixers} x Rule2 in {all 756} and vice versa.
For each pair, run the exact gate sequence (V2a, V2b, V3, BAR) and report
pairs with improved>=2 AND (dacc<1 OR dwrong>0) that REACH BAR.
Empty champion. Pure Zag measurement via shared engine."""
import os, csv

BASE = "/home/hatch/workspace/tnn-lab/rsi/autonomous_run_2"
tg = open(f"{BASE}/build/tables_gen.zag").read()
inc = open(f"{BASE}/src/policy_engine.zag.inc").read()

ATOMS = {1: [0, 1, 2], 2: [None], 3: [None], 4: list(range(-6, 7)),
         5: list(range(-6, 7)), 6: list(range(-6, 7)), 7: [0, 1, 2],
         8: list(range(-3, 4)), 9: list(range(-3, 4)), 10: [None],
         11: [None], 12: [0, 1, 2], 13: list(range(-6, 7)),
         14: list(range(-6, 7)), 15: list(range(-6, 7))}
# (stage, aid, prm, act, aprm)
rules = []
for aid in range(1, 12):
    for prm in ATOMS[aid]:
        p = 0 if prm is None else prm
        rules.append((1, aid, p, 1, 0))
        rules.append((1, aid, p, 2, 0))
        for mask in range(8):
            rules.append((4, aid, p, 5, mask))
for aid in range(12, 16):
    for prm in ATOMS[aid]:
        rules.append((2, aid, prm, 3, 0))
        rules.append((2, aid, prm, 4, 1))
        rules.append((2, aid, prm, 4, 2))
print(f"# rules: {len(rules)}")

# the 14 fixers: (aid,prm,act,aprm) -> find indices
fixer_keys = [(1, 2, 5, 1), (1, 2, 5, 3)]
# expand: the 14 are pre_is(OLD),sm_le(-2),sm_le(-1),sm_eq(-2),dir_is(OLD_LEAD),
# so_ge(0),so_ge(1) x recompute_only(001/011)
# aid/prm: (1,2),(4,-2),(4,-1),(6,-2),(7,2),(9,0),(9,1)
fixer_ap = [(1, 2), (4, -2), (4, -1), (6, -2), (7, 2), (9, 0), (9, 1)]
fixers = []
for aid, prm in fixer_ap:
    for aprm in (1, 3):
        key = (4, aid, prm, 5, aprm)
        fixers.append(rules.index(key))
print(f"# fixers: {len(fixers)}")

gt = ''.join('1' if r['gt'] == 'NEW' else ('2' if r['gt'] == 'OLD' else '0')
             for r in csv.DictReader(open(f"{BASE}/build/proxy_battery.csv")))

def zag_rules(var, lst):
    lines = [f"    let {var}:*u8=_zag_malloc({len(lst)*20});"]
    for i, (st, aid, prm, act, aprm) in enumerate(lst):
        lines.append(f"    ap32({var},{i*20},{st});ap32({var},{i*20+4},{aid});"
                     f"ap32({var},{i*20+8},{prm});ap32({var},{i*20+12},{act});"
                     f"ap32({var},{i*20+16},{aprm});")
    return "\n".join(lines)

helper = r"""
fn build2(pol:*u8, ra:*u8, ia:i32, rb:*u8, ib:i32)void {
    let o1:i64=(ia as i64)*20;
    let o2:i64=(ib as i64)*20;
    ap32(pol,0,2);
    // rule 0 at 4, rule 1 at 276
    ap32(pol,4,ag32(ra,o1));ap32(pol,8,ag32(ra,o1+12));ap32(pol,12,0);
    ap32(pol,16,1);ap32(pol,20,ag32(ra,o1+4));ap32(pol,24,ag32(ra,o1+8));
    ap32(pol,276,ag32(rb,o2));ap32(pol,280,ag32(rb,o2+12));ap32(pol,284,0);
    ap32(pol,288,1);ap32(pol,292,ag32(rb,o2+4));ap32(pol,296,ag32(rb,o2+8));
    return;
}
fn gates(champ:*u8, pol:*u8, pgt:[]u8, o_v2a:*u8, o_nd:*u8, o_im:*u8, o_da:*u8, o_dw:*u8)void {
    // V2a
    let v2a:i32=1;
    let b:i32=0;
    while(b<=2){
        if(b==1){b=2;}
        let i:i32=0;
        while(i<24){
            let cv:i32=dec_v(pol_decide(champ,b,i));
            let pv:i32=dec_v(pol_decide(pol,b,i));
            if(cv==0){if(pv!=0){v2a=0;}}
            i=i+1;
        }
        if(b==0){b=2;}else{b=3;}
    }
    ap32(o_v2a,0,v2a);
    if(v2a==0){return;}
    let c_acc:i32=0;let c_wr:i32=0;let p_acc:i32=0;let p_wr:i32=0;
    let novel_diff:i32=0;let improved:i32=0;
    let i2:i32=0;
    while(i2<24){
        let cd:i64=pol_decide(champ,1,i2);
        let pd:i64=pol_decide(pol,1,i2);
        let cv2:i32=dec_v(cd);let pv2:i32=dec_v(pd);
        let g:i32=(pgt[i2]-48) as i32;
        if(cv2==g){c_acc=c_acc+1;}
        if(cv2!=0){if(cv2!=g){c_wr=c_wr+1;}}
        if(pv2==g){p_acc=p_acc+1;}
        if(pv2!=0){if(pv2!=g){p_wr=p_wr+1;}}
        if(pv2==g){if(cv2!=g){improved=improved+1;}}
        let cnv:i32=dec_v(pol_decide(champ,2,i2));
        let pnv:i32=dec_v(pol_decide(pol,2,i2));
        if(cnv!=pnv){novel_diff=novel_diff+1;}
        i2=i2+1;
    }
    ap32(o_nd,0,novel_diff);
    ap32(o_im,0,improved);
    ap32(o_da,0,p_acc-c_acc);
    ap32(o_dw,0,p_wr-c_wr);
    return;
}
fn pr_pair(fxr:*u8, fi:i32, rls:*u8, fj:i32, tag:[]u8, da:i32, dw:i32)void {
    _zag_print(tag);
    _zag_print(" r1=");_zag_print(i64s(ag32(fxr,(fi as i64)*20) as i64));
    _zag_print(",");_zag_print(i64s(ag32(fxr,(fi as i64)*20+4) as i64));
    _zag_print("=");_zag_print(i64s(ag32(fxr,(fi as i64)*20+8) as i64));
    _zag_print(",");_zag_print(i64s(ag32(fxr,(fi as i64)*20+12) as i64));
    _zag_print("=");_zag_print(i64s(ag32(fxr,(fi as i64)*20+16) as i64));
    _zag_print(" r2=");_zag_print(i64s(ag32(rls,(fj as i64)*20) as i64));
    _zag_print(",");_zag_print(i64s(ag32(rls,(fj as i64)*20+4) as i64));
    _zag_print("=");_zag_print(i64s(ag32(rls,(fj as i64)*20+8) as i64));
    _zag_print(",");_zag_print(i64s(ag32(rls,(fj as i64)*20+12) as i64));
    _zag_print("=");_zag_print(i64s(ag32(rls,(fj as i64)*20+16) as i64));
    _zag_print(" dacc=");_zag_print(i64s(da as i64));
    _zag_print(" dw=");_zag_print(i64s(dw as i64));
    _zag_println("");
    return;
}
fn main()void {
    let champ:*u8=_zag_malloc(65536);
    ap32(champ,0,0);
    let pgt:[]u8="PGT";
RULES
FIXERS
    let pol:*u8=_zag_malloc(65536);
    let o_v2a:*u8=_zag_malloc(4);let o_nd:*u8=_zag_malloc(4);
    let o_im:*u8=_zag_malloc(4);let o_da:*u8=_zag_malloc(4);let o_dw:*u8=_zag_malloc(4);
    let hits:i32=0;let tested:i32=0;
    let fi:i32=0;
    while(fi<NFIX){
        let fj:i32=0;
        while(fj<NRULE){
            // order 1: fixer first, other second
            build2(pol,fxr,fi,rls,fj);
            gates(champ,pol,pgt,o_v2a,o_nd,o_im,o_da,o_dw);
            tested=tested+1;
            if(ag32(o_v2a,0)==1){
                if(ag32(o_nd,0)==0){
                    if(ag32(o_im,0)>=2){
                        let da:i32=ag32(o_da,0);let dw:i32=ag32(o_dw,0);
                        if(da<1){hits=hits+1;pr_pair(fxr,fi,rls,fj,"HIT-DACC",da,dw);}
                        else{if(dw>0){hits=hits+1;pr_pair(fxr,fi,rls,fj,"HIT-DWRONG",da,dw);}}
                    }
                }
            }
            // order 2: other first, fixer second
            build2(pol,rls,fj,fxr,fi);
            gates(champ,pol,pgt,o_v2a,o_nd,o_im,o_da,o_dw);
            tested=tested+1;
            if(ag32(o_v2a,0)==1){
                if(ag32(o_nd,0)==0){
                    if(ag32(o_im,0)>=2){
                        let da2:i32=ag32(o_da,0);let dw2:i32=ag32(o_dw,0);
                        if(da2<1){hits=hits+1;pr_pair(rls,fj,fxr,fi,"HIT-DACC",da2,dw2);}
                        else{if(dw2>0){hits=hits+1;pr_pair(rls,fj,fxr,fi,"HIT-DWRONG",da2,dw2);}}
                    }
                }
            }
            fj=fj+1;
        }
        fi=fi+1;
    }
    _zag_print("tested=");_zag_print(i64s(tested as i64));
    _zag_print(" bar-refusal-hits=");_zag_print(i64s(hits as i64));_zag_println("");
    return;
}
"""

src = (tg + inc + helper
       .replace('"PGT"', f'"{gt}"')
       .replace('RULES', zag_rules('rls', rules))
       .replace('FIXERS', zag_rules('fxr', [rules[i] for i in fixers]))
       .replace('NFIX', str(len(fixers)))
       .replace('NRULE', str(len(rules))))
# fix pointer arithmetic names: fxr+(fi as i64)*20 needs the base var name

os.makedirs(f"{BASE}/work/r4", exist_ok=True)
dest = f"{BASE}/work/r4/probe_bar2_full.zag"
open(dest, "w").write(src)
print("wrote", dest)
