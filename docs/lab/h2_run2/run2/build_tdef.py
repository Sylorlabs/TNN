#!/usr/bin/env python3
"""Build T-DEF: frozen run-1 FL2-default + actfault wrapper (D4 comparator).

Reuses run-1's frozen substrate_append/patch_learner verbatim; only adds the
D4 storm audit toggle (sched=8: silent/standard every 12 episodes).
Python orchestrates only; all logic is the vendored pristine + run-1 patches.
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RUN1 = os.path.expanduser("~/workspace/tnn-lab/training_paradigms/scaffold_release/forks/gl_adaptive_liar/build")
ZNC = os.path.expanduser("~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1")
BUILD = os.path.join(HERE, "build")
os.makedirs(BUILD, exist_ok=True)

sys.path.insert(0, RUN1)
import build as run1

STORM_GENOME = {"stated": 2, "teach_lie": 1, "sched": 8, "aa_lo": 1, "aa_hi": 128,
                "dens": 0, "keyrot": 0, "actfault": 1}
HONEST_GENOME = {"stated": 1, "teach_lie": 0, "sched": 0, "aa_lo": 1, "aa_hi": 64,
                 "dens": 0, "keyrot": 0, "actfault": 0}

def substrate_append_tdef(genome, params):
    s = run1.substrate_append(genome, params)
    old = ("fn h2_audit_active(ep:i32)i32 {\n"
           "    if(H2_SCHED==2){return 0;}\n"
           "    if(H2_SCHED==3 && ep<=48){return 0;}\n"
           "    if(ep>=H2_AA_LO && ep<=H2_AA_HI){return 1;}\n"
           "    return 0;\n}")
    new = ("fn h2_audit_active(ep:i32)i32 {\n"
           "    if(H2_SCHED==2){return 0;}\n"
           "    if(H2_SCHED==3 && ep<=48){return 0;}\n"
           "    if(H2_SCHED==8){return (((ep-1)/12)%2);}\n"
           "    if(ep>=H2_AA_LO && ep<=H2_AA_HI){return 1;}\n"
           "    return 0;\n}")
    assert old in s, "h2_audit_active anchor missing"
    return s.replace(old, new)

def build_tdef(genome, tag):
    work = os.path.join(BUILD, "tdef_" + tag)
    os.makedirs(work, exist_ok=True)
    for fn in ("gl_learner.zag", "gl_substrate.zag"):
        src = os.path.join(HERE, "orig", "tdef", fn)
        dst = os.path.join(work, fn)
        open(dst, "w").write(open(src).read())
    # append H2 substrate to the substrate file
    sub = os.path.join(work, "gl_substrate.zag")
    app = substrate_append_tdef(genome, dict(run1.DEFAULT_PARAMS))
    open(sub, "a").write(app)
    # patch learner
    lp = os.path.join(work, "gl_learner.zag")
    src = open(lp).read()
    src = run1.patch_learner(src, "default", genome, dict(run1.DEFAULT_PARAMS), "h2")
    # add round label from argv[1]
    old_main = ('    _zag_print("TN_FAILURES,");\n    h2_p32(f);\n    _zag_println("");')
    new_main = ('    _zag_print("TN_FAILURES,");\n    h2_p32(f);\n'
                '    _zag_print(",ROUND,");\n    _zag_print(_zag_arg(1));\n    _zag_println("");')
    assert old_main in src, "main anchor missing"
    src = src.replace(old_main, new_main)
    open(lp, "w").write(src)
    # static check: no rng
    bad = []
    for i, line in enumerate(src.splitlines(), 1):
        code = re.sub(r"//.*", "", line)
        if re.search(r"\brng\b|\brand\b|\bseed\b", code, re.I):
            bad.append((i, code.strip()[:60]))
    if bad:
        print("rng tokens in tdef learner:", bad[:5])
        return None
    # compile (cwd=work so imports resolve)
    out = os.path.join(work, "tdef_" + tag)
    r = subprocess.run([ZNC, "gl_learner.zag", "-o", out], cwd=work,
                       capture_output=True, text=True)
    if r.returncode != 0 or not os.path.exists(out):
        print("compile failed for", tag)
        print(r.stdout[-1500:])
        print(r.stderr[-1500:])
        return None
    print("built tdef_%s -> %s" % (tag, out))
    return out

if __name__ == "__main__":
    b1 = build_tdef(STORM_GENOME, "storm")
    b2 = build_tdef(HONEST_GENOME, "honest")
    if not b1 or not b2:
        sys.exit(1)
    print("T-DEF builds OK")
