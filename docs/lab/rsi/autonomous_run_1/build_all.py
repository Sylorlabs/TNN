#!/usr/bin/env python3
"""Builds the autonomous run's Zag artifacts (glue only; all reasoning is Zag).

1. Runs gen_decide.py -> decide.zag.inc (single source of truth).
2. proposer.zag = proposer_head.zag + decide.zag.inc
3. subject.zag = rsi4c.zag (verbatim copy) + decide.zag.inc prepended,
   plus a `prop` mode: argv[1]="prop", argv[2]=extra ("c1".."c5"/"none"),
   argv[3..7]=kept slots, argv[8]=rep token.
Builds both with the pinned znc. No @import (paths are cwd-fragile);
single-source truth is by generation.
"""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ZNC = os.path.expanduser("~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1")
R4C = os.path.expanduser("~/workspace/tnn-lab/rsi/recency_vs_coherence/rsi4c.zag")
WORK = os.path.join(HERE, "work")
os.makedirs(WORK, exist_ok=True)

def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        print("FAILED:", " ".join(cmd)); print(r.stdout[-2000:]); print(r.stderr[-2000:])
        sys.exit(1)
    return r

os.chdir(HERE)
run([sys.executable, "gen_decide.py"])
inc = open("decide.zag.inc").read()
assert "fn decide(" in inc and "fn fld(" in inc

# ---- proposer ----
prop = open("proposer_head.zag").read() + "\n" + inc
open(os.path.join(WORK, "proposer.zag"), "w").write(prop)

# ---- subject: verbatim rsi4c.zag + prop mode ----
src = open(R4C).read()
# 1) mode dispatch: add prop
old_dispatch = '    if(_zag_strcmp(a1,"askfirst")==1){mode=4;}'
assert old_dispatch in src
src = src.replace(old_dispatch,
                  old_dispatch + '\n    if(_zag_strcmp(a1,"prop")==1){mode=5;}')
# 2) item loop: route mode 5 through decide()
old_loop = """        let v:i32=arm_verdict(mode,i);
        let cons:i32=arm_consulted(mode,i);
        let ops:i32=arm_ops(mode,cons);"""
assert old_loop in src
new_loop = """        let v:i32=0; let cons:i32=0; let ops:i32=0;
        if(mode==5){
            let exs:[]u8=_zag_arg(2);
            let extra:i32=slot_mask(exs);
            let kk:i32=0;
            let qi:i32=3;
            while(qi<=7){let qs:[]u8=_zag_arg(qi);kk=kk|slot_mask(qs);qi=qi+1;}
            let dd:i64=decide(0,i,kk,extra);
            v=(dd&(255 as i64)) as i32;
            cons=((dd>>8)&(255 as i64)) as i32;
            ops=((dd>>16)&(65535 as i64)) as i32;
        }else{
            v=arm_verdict(mode,i);
            cons=arm_consulted(mode,i);
            ops=arm_ops(mode,cons);
        }"""
src = src.replace(old_loop, new_loop)
# 3) mname: add prop label
old_mname = '    let s4:[]u8="askfirst";return s4;'
assert old_mname in src
src = src.replace(old_mname, old_mname + '\n    if(m==5){let s5:[]u8="prop";return s5;}')
subj = inc + "\n" + src
open(os.path.join(WORK, "subject.zag"), "w").write(subj)

# ---- compile ----
for name in ("proposer", "subject"):
    run([ZNC, os.path.join(WORK, name + ".zag"), "--no-zagd", "--no-analyze",
         "-o", os.path.join(WORK, name)], cwd=WORK)
    print("built", name)

# ---- smoke: proposer determinism (3x identical) ----
outs = set()
for _ in range(3):
    r = run([os.path.join(WORK, "proposer"), "-", "-", "-", "-", "-",
             "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "b0", "web0"])
    outs.add(r.stdout)
assert len(outs) == 1, "proposer not deterministic"
print("proposer deterministic 3/3")
print("---- round-0 deliberation ----")
print(sorted(outs)[0])
