#!/usr/bin/env python3
"""Build probe_measure: exact-replica measurement of the proposer's
V2a/V2b/V3/BAR metrics for a list of bytecode policies (empty champion).
Uses the shared engine (bc_parse/pol_decide/dec_*) — same sources as the
frozen proposer."""
import os, csv

BASE = "/home/hatch/workspace/tnn-lab/rsi/autonomous_run_2"
tg = open(f"{BASE}/build/tables_gen.zag").read()
inc = open(f"{BASE}/src/policy_engine.zag.inc").read()

POLICIES = [
    ("4,1=2,5=1", "pre_is(OLD)+recompute_only(001)"),
    ("4,1=2,5=3", "pre_is(OLD)+recompute_only(011)"),
    ("1,1=2,1", "pre_is(OLD)+force_consult [V3 control]"),
]

gt = ''.join('1' if r['gt'] == 'NEW' else ('2' if r['gt'] == 'OLD' else '0')
             for r in csv.DictReader(open(f"{BASE}/build/proxy_battery.csv")))

helper = r"""
fn measure_one(champ:*u8, bc:[]u8, label:[]u8, pgt:[]u8)void {
    let pol:*u8=_zag_malloc(65536);
    ap32(pol,0,0);
    let e:i32=bc_parse(pol,bc,0);
    if(e!=0){_zag_print("PARSE-FAIL ");_zag_print(bc);_zag_println("");return;}
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
    let c_acc:i32=0;let c_wr:i32=0;let p_acc:i32=0;let p_wr:i32=0;
    let novel_diff:i32=0;let improved:i32=0;let pcost:i32=0;
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
        pcost=pcost+(dec_o(pd) as i32);
        let cnv:i32=dec_v(pol_decide(champ,2,i2));
        let pnv:i32=dec_v(pol_decide(pol,2,i2));
        if(cnv!=pnv){novel_diff=novel_diff+1;}
        i2=i2+1;
    }
    _zag_print("POL ");_zag_print(label);
    _zag_print(" v2a=");_zag_print(i64s(v2a as i64));
    _zag_print(" ndiff=");_zag_print(i64s(novel_diff as i64));
    _zag_print(" impr=");_zag_print(i64s(improved as i64));
    _zag_print(" c_acc=");_zag_print(i64s(c_acc as i64));
    _zag_print(" p_acc=");_zag_print(i64s(p_acc as i64));
    _zag_print(" c_wr=");_zag_print(i64s(c_wr as i64));
    _zag_print(" p_wr=");_zag_print(i64s(p_wr as i64));
    _zag_print(" dacc=");_zag_print(i64s((p_acc-c_acc) as i64));
    _zag_print(" dwr=");_zag_print(i64s((p_wr-c_wr) as i64));
    _zag_print(" pcost=");_zag_print(i64s(pcost as i64));
    _zag_println("");
    return;
}
fn main()void {
    let champ:*u8=_zag_malloc(65536);
    ap32(champ,0,0);
    let pgt:[]u8="PGT";
"""
main_calls = ""
for bc, label in POLICIES:
    main_calls += f'    measure_one(champ,"{bc}","{label}",pgt);\n'
src = tg + inc + helper.replace('"PGT"', f'"{gt}"') + main_calls + "}\n"

os.makedirs(f"{BASE}/work/r4", exist_ok=True)
dest = f"{BASE}/work/r4/probe_measure_full.zag"
open(dest, "w").write(src)
print("wrote", dest)
