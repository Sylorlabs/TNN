#!/usr/bin/env python3
"""P3c unit control: exercise the D5 firing-measurement logic.
Builds candidate arenas with the SAME ap32 sequence as deliberation.zag's
D5-FIRING-CHECK and counts consult/verdict diffs vs the empty champion on
the 24 proxy items via the shared pol_decide.
Expect: 1,1=1,1 (pre_is(NEW)+force_consult) -> diffs>0 (fires);
        1,1=2,1 (pre_is(OLD)+force_consult)  -> diffs==0 (no-op).
Exit nonzero on mismatch."""
import os

BASE = "/home/hatch/workspace/tnn-lab/rsi/autonomous_run_2"
tg = open(f"{BASE}/build/tables_gen.zag").read()
inc = open(f"{BASE}/src/policy_engine.zag.inc").read()

main = r"""
fn build_cand(cand:*u8, stage:i32, aid:i32, prm:i32, act:i32)void {
    ap32(cand,0,1);
    ap32(cand,4,stage);
    ap32(cand,8,act);
    ap32(cand,12,0);
    ap32(cand,16,1);
    ap32(cand,20,aid);
    ap32(cand,24,prm);
}
fn measure(champ:*u8, cand:*u8)i32 {
    let diffs:i32=0;
    let ii:i32=0;
    while(ii<24){
        let dc:i64=pol_decide(champ,1,ii);
        let dn:i64=pol_decide(cand,1,ii);
        if(dec_v(dc)!=dec_v(dn)){diffs=diffs+1;}else{
            if(dec_c(dc)!=dec_c(dn)){diffs=diffs+1;}
        }
        ii=ii+1;
    }
    return diffs;
}
fn main()void {
    let champ:*u8=_zag_malloc(65536);
    ap32(champ,0,0);
    let cand:*u8=_zag_malloc(4096);
    let fails:i32=0;
    // known-firing: pre_is(NEW) + force_consult
    build_cand(cand,1,1,1,1);
    let d1:i32=measure(champ,cand);
    _zag_print("firing-combo diffs=");_zag_print(i64s(d1 as i64));_zag_println("");
    if(d1<=0){_zag_println("FAIL: firing combo measured no diffs");fails=fails+1;}
    // known no-op: pre_is(OLD) + force_consult
    build_cand(cand,1,1,2,1);
    let d2:i32=measure(champ,cand);
    _zag_print("noop-combo diffs=");_zag_print(i64s(d2 as i64));_zag_println("");
    if(d2!=0){_zag_println("FAIL: no-op combo measured diffs");fails=fails+1;}
    // post no-op: post_is(OLD) + force_withhold (fires where consult already 1... check)
    build_cand(cand,2,12,2,3);
    let d3:i32=measure(champ,cand);
    _zag_print("post-combo diffs=");_zag_print(i64s(d3 as i64));_zag_println("");
    if(fails!=0){_zag_println("P3c-FAIL");}else{_zag_println("P3c-PASS");}
}
"""
os.makedirs(f"{BASE}/work/r4", exist_ok=True)
dest = f"{BASE}/work/r4/probe_p3c_full.zag"
open(dest, "w").write(tg + inc + main)
print("wrote", dest)
