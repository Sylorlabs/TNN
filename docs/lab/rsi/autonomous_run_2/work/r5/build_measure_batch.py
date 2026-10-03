#!/usr/bin/env python3
"""Build measure_batch: honest (acc, wrong, cost) for a list of bytecode
policies via the shared engine. Usage: measure_batch <proxy-gt-24> <bc1> <bc2> ...
Output per policy: MEASURE <idx> <acc> <wrong> <cost>."""
import os

BASE = os.path.expanduser("~/workspace/tnn-lab/rsi/autonomous_run_2")
tg = open(f"{BASE}/build/tables_gen.zag").read()
inc = open(f"{BASE}/src/policy_engine.zag.inc").read()

main = r"""
fn main()void {
    let pgt:[]u8=_zag_arg(1);
    let i:i32=2;
    while(1){
        let bc:[]u8=_zag_arg(i);
        if(bc.len==0){break;}
        let pol:*u8=_zag_malloc(17412);
        ap32(pol,0,0);
        let e:i32=bc_parse(pol,bc,0);
        if(e!=0){
            _zag_print("MEASURE ");_zag_print(i64s((i-2) as i64));
            _zag_println(" PARSE-FAIL");
        }else{
            let acc:i32=0;
            let wr:i32=0;
            let cost:i32=0;
            let k:i32=0;
            while(k<24){
                let pd:i64=pol_decide(pol,1,k);
                let pv:i32=dec_v(pd);
                let g:i32=(pgt[k] as i32)-48;
                if(pv==g){acc=acc+1;}
                if(pv!=0){if(pv!=g){wr=wr+1;}}
                cost=cost+(dec_o(pd) as i32);
                k=k+1;
            }
            _zag_print("MEASURE ");_zag_print(i64s((i-2) as i64));
            _zag_print(" ");_zag_print(i64s(acc as i64));
            _zag_print(" ");_zag_print(i64s(wr as i64));
            _zag_print(" ");_zag_print(i64s(cost as i64));
            _zag_println("");
        }
        i=i+1;
    }
    return;
}
"""
open(f"{BASE}/work/r5/measure_batch_full.zag", "w").write(tg + inc + main)
print("wrote measure_batch_full.zag")
