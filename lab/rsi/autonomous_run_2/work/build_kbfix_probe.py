#!/usr/bin/env python3
"""Build the KB-FIX probe: tables_gen.zag + policy_engine.zag.inc +
chan_vals/cv_*/atom_true sliced MECHANICALLY from fixed src/afdisc.zag
(no transcription) + probe main. Per RUN_PREREG3 section 5."""
import sys

BASE = "/home/hatch/workspace/tnn-lab/rsi/autonomous_run_2"

src = open(f"{BASE}/src/afdisc.zag").read().splitlines(keepends=True)
# slice from 'fn chan_vals' to just before 'fn main'
start = next(i for i, l in enumerate(src) if l.startswith("fn chan_vals"))
end = next(i for i, l in enumerate(src) if l.startswith("fn main"))
sl = src[start:end]
assert any("fn atom_true" in l for l in sl), "atom_true missing from slice"
assert any("sn+8" in l for l in sl), "fix not present in slice"

probe_main = '''
fn main()void {
    let fail:i32=0;
    let checks:i32=0;
    let i:i32=0;
    while(i<24){
        let cv:i64=chan_vals(1,i);
        let pk:i64=pre_pack(1,i);
        let sn:i32=pk_sn(pk);
        let so:i32=pk_so(pk);
        if(cv_sn(cv)!=sn){fail=fail+1;}
        checks=checks+1;
        if(cv_so(cv)!=so){fail=fail+1;}
        checks=checks+1;
        if(cv_sn(cv)==255){fail=fail+1;}
        checks=checks+1;
        if(cv_so(cv)==255){fail=fail+1;}
        checks=checks+1;
        let prm:i32=0;
        while(prm<=6){
            let e8:i32=0;
            if(sn>=prm){e8=1;}
            if(atom_true(8,prm,1,i,cv)!=e8){fail=fail+1;}
            checks=checks+1;
            let e9:i32=0;
            if(so>=prm){e9=1;}
            if(atom_true(9,prm,1,i,cv)!=e9){fail=fail+1;}
            checks=checks+1;
            prm=prm+1;
        }
        i=i+1;
    }
    _zag_print("KB_FIX_PROBE checks=");
    _zag_print(i64s(checks as i64));
    _zag_print(" fail=");
    _zag_println(i64s(fail as i64));
    return;
}
'''

out = []
out.append(open(f"{BASE}/build/tables_gen.zag").read())
out.append(open(f"{BASE}/src/policy_engine.zag.inc").read())
out.append("".join(sl))
out.append(probe_main)
dest = f"{BASE}/work/kbfix_probe_full.zag"
open(dest, "w").write("\n".join(out))
print("wrote", dest, "slice_lines=", len(sl))
