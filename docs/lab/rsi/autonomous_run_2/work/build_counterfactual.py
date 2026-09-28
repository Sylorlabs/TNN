#!/usr/bin/env python3
"""Build the counterfactual probe: tables_gen.zag + policy_engine.zag.inc
(identical mechanism code the frozen proposer uses: bc_parse, pol_decide,
dec_v, dec_o) + probe main replicating the proposer's V2b/V3/BAR measurement
loop EXACTLY, fed with hand-corrected bytecode that the proposer's broken
L1 text translator cannot emit (u8-oprm sign bug). Labeled counterfactual:
measures what the gate WOULD have seen. Usage: probe <gt24> <bytecode>."""
import sys

BASE = "/home/hatch/workspace/tnn-lab/rsi/autonomous_run_2"
tg = open(f"{BASE}/build/tables_gen.zag").read()
inc = open(f"{BASE}/src/policy_engine.zag.inc").read()
main = '''
fn main()void {
    let pgt:[]u8=_zag_arg(1);
    let bcs:[]u8=_zag_arg(2);
    let champ:*u8=_zag_malloc(17412);
    let pol:*u8=_zag_malloc(17412);
    let e0:i32=bc_parse(champ,"",0);
    let e1:i32=bc_parse(pol,bcs,0);
    _zag_print("parse champ=");
    _zag_print(i64s(e0 as i64));
    _zag_print(" pol=");
    _zag_println(i64s(e1 as i64));
    let c_acc:i32=0;
    let c_wr:i32=0;
    let p_acc:i32=0;
    let p_wr:i32=0;
    let improved:i32=0;
    let pcost:i32=0;
    let i:i32=0;
    while(i<24){
        let cd:i64=pol_decide(champ,1,i);
        let pd:i64=pol_decide(pol,1,i);
        let cv:i32=dec_v(cd);
        let pv:i32=dec_v(pd);
        let g:i32=(pgt[i]-48) as i32;
        if(cv==g){c_acc=c_acc+1;}
        if(cv!=0){if(cv!=g){c_wr=c_wr+1;}}
        if(pv==g){p_acc=p_acc+1;}
        if(pv!=0){if(pv!=g){p_wr=p_wr+1;}}
        if(pv==g){if(cv!=g){improved=improved+1;}}
        pcost=pcost+(dec_o(pd) as i32);
        i=i+1;
    }
    let ndiff:i32=0;
    i=0;
    while(i<24){
        let cnv:i32=dec_v(pol_decide(champ,2,i));
        let pnv:i32=dec_v(pol_decide(pol,2,i));
        if(cnv!=pnv){ndiff=ndiff+1;}
        i=i+1;
    }
    _zag_print("champ acc=");
    _zag_print(i64s(c_acc as i64));
    _zag_print(" wrong=");
    _zag_println(i64s(c_wr as i64));
    _zag_print("pol acc=");
    _zag_print(i64s(p_acc as i64));
    _zag_print(" wrong=");
    _zag_print(i64s(p_wr as i64));
    _zag_print(" cost=");
    _zag_println(i64s(pcost as i64));
    _zag_print("improved=");
    _zag_println(i64s(improved as i64));
    _zag_print("novel_diff=");
    _zag_println(i64s(ndiff as i64));
    return;
}
'''
dest = f"{BASE}/work/counterfactual_full.zag"
open(dest, "w").write(tg + inc + main)
print("wrote", dest)
