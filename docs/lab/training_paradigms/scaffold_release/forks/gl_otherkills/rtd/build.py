#!/usr/bin/env python3
"""RT-D fork battery: fidelity gate first, then RT-D attack cells, then
main-store unit probes. Patched copies only; canonical sources untouched.

Phases:
  fid    - fork sources + original main (standard schedule). Gate:
           TN_FAILURES=0, glh_audit_total=269, gll_audit_total=271.
           Attack cells are NOT built until every fork passes.
  attack - RT-D cell per fork: the RT2 default_D patches re-applied
           verbatim (rt_ep_info RT_MODE=1, aa-gate patch, rt_fact
           instrumentation, main -> arm_gl(1,0,"rtd_")).
  unit   - main-store unit flood per fork (140 inserts / 128 slots).

Every binary runs twice; transcripts must be byte-identical.
"""
import hashlib
import os
import re
import shutil
import subprocess
import sys

ZNC = os.path.expanduser("~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1")
ROOT = os.path.dirname(os.path.abspath(__file__))
FORKS = os.path.join(ROOT, "forks")
BUILD = os.path.join(ROOT, "build")
EV = os.path.join(ROOT, "evidence")
UNIT = os.path.join(ROOT, "unit")

FORK_NAMES = ["canon", "f1", "f2", "r1"]

SUB_APPEND = """
// RT2 red-team schedule wrapper. RT_MODE: 0=standard, 1=flood (E15+ dense ACQ),
// 2=displace (E49-50 TEACH, E51+ ACQ contradictions), 3=silent-aa (standard schedule).
// etype literals: 3=ET_ACQ, 1=ET_TEACH (same values in every substrate copy).
const RT_MODE:i32={mode};
fn rt_ep_info(ep:i32,etype:*i32,key:*i32,val:*i32,auth:*i32)void {{
    if(RT_MODE==1 && ep>=15){{
        etype.*=3;key.*=((ep-15)%8)+1;val.*=300+ep;auth.*=0;return;
    }}
    if(RT_MODE==2 && ep>=49){{
        if(ep<=50){{etype.*=1;key.*=0;val.*=0;auth.*=0;return;}}
        etype.*=3;key.*=((ep-51)%8)+1;val.*=700+ep;auth.*=0;return;
    }}
    tn_ep_info(ep,etype,key,val,auth);
    return;
}}
"""

FACT_HELPER = """
// RT2 instrumentation: one RT_FACT metrics line (no behavior change).
fn rt_fact(px:[]u8,name:[]u8,val:i32)void {
    _zag_print("RT_FACT,");
    _zag_print(px);
    _zag_print(name);
    _zag_print(",");
    let s:[]u8=_zag_i64_to_str(val as i64);_zag_print(s);tn_free(s);
    _zag_println("");
    return;
}
"""

FACTS_BLOCK = """
    // RT2 instrumentation: first-aux facts (metrics only).
    let rtf_i:i32=0;let rtf_cpol:i32=-1;let rtf_upol:i32=-1;let rtf_ppol:i32=-1;let rtf_ncommit:i32=0;
    while(rtf_i<acount){
        let rtf_op:i32=tn_g32(audit,rtf_i*16+4);
        if(rtf_op==TN_OP_COMMIT){rtf_ncommit=rtf_ncommit+1;}
        if(rtf_op==TN_OP_COMMIT && rtf_cpol<0){rtf_cpol=tn_g32(audit,rtf_i*16+12);}
        if(rtf_op==TN_OP_UNINSTALL_PROVISIONAL && rtf_upol<0){rtf_upol=tn_g32(audit,rtf_i*16+12);}
        if(rtf_op==TN_OP_PROMOTE && rtf_ppol<0){rtf_ppol=tn_g32(audit,rtf_i*16+12);}
        rtf_i=rtf_i+1;
    }
    rt_fact(px,"commit_policy",rtf_cpol);
    rt_fact(px,"uninstall_policy",rtf_upol);
    rt_fact(px,"promote_policy",rtf_ppol);
    rt_fact(px,"ncommit",rtf_ncommit);
    rt_fact(px,"badep",badep);
"""

FREE_ANCHOR = "    tn_free(audit);tn_free(committed);\n    return f;"
AA_OLD = "if(ep>=29 && ep<=48){aa=1;}"
AA_NEW = "if(ep>=29 && ep<=48 && RT_MODE!=2 && RT_MODE!=3){aa=1;}"
ARM_FN = "fn arm_gl("


def read(p):
    with open(p, "r", encoding="utf-8") as f:
        return f.read()


def write(p, s):
    with open(p, "w", encoding="utf-8") as f:
        f.write(s)


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def no_rng_scan(d, tag, files):
    for fn in files:
        code = re.sub(r"//.*", "", read(os.path.join(d, fn)))
        hits = re.findall(r"(?i)\brng\b|rand\(|srand|/dev/urandom|[^a-z]seed[^a-z]", code)
        assert not hits, (tag, fn, hits)


def compile_and_run(d, learner_fn, tag):
    binp = os.path.join(d, "rtbin")
    cp = subprocess.run([ZNC, os.path.join(d, learner_fn), "--no-zagd",
                         "--no-analyze", "--no-foreground-cache", "-o", binp],
                        cwd=d, capture_output=True, text=True, timeout=600)
    if cp.returncode != 0:
        return (False, "COMPILE FAIL: " + cp.stderr[-2000:])
    outs = []
    for _ in (1, 2):
        r = subprocess.run([binp], cwd=d, capture_output=True, text=True, timeout=600)
        outs.append(r.stdout)
    h1 = hashlib.sha256(outs[0].encode()).hexdigest()
    h2 = hashlib.sha256(outs[1].encode()).hexdigest()
    det = (h1 == h2)
    os.makedirs(EV, exist_ok=True)
    with open(os.path.join(EV, "%s_run1.txt" % tag), "w") as f:
        f.write(outs[0])
    with open(os.path.join(EV, "%s_run2.txt" % tag), "w") as f:
        f.write(outs[1])
    with open(os.path.join(EV, "%s_meta.txt" % tag), "w") as f:
        f.write("tag=%s\nsha1=%s\nsha2=%s\ndeterministic=%s\n" % (tag, h1, h2, det))
    with open(os.path.join(EV, "%s_sources.txt" % tag), "w") as f:
        for fn in sorted(os.listdir(d)):
            if fn.endswith(".zag"):
                f.write("%s  %s\n" % (sha256_file(os.path.join(d, fn)), fn))
    return (det, "OK sha=%s" % h1[:12])


def build_fid(fork):
    tag = "%s_FID" % fork
    d = os.path.join(BUILD, tag)
    if os.path.isdir(d):
        shutil.rmtree(d)
    os.makedirs(d)
    for fn in ("gl_learner.zag", "gl_substrate.zag"):
        shutil.copy(os.path.join(FORKS, fork, fn), os.path.join(d, fn))
    no_rng_scan(d, tag, ("gl_learner.zag", "gl_substrate.zag"))
    return (tag,) + compile_and_run(d, "gl_learner.zag", tag)


def build_attack(fork):
    tag = "%s_D" % fork
    d = os.path.join(BUILD, tag)
    if os.path.isdir(d):
        shutil.rmtree(d)
    os.makedirs(d)
    for fn in ("gl_learner.zag", "gl_substrate.zag"):
        shutil.copy(os.path.join(FORKS, fork, fn), os.path.join(d, fn))
    # 1. substrate: append RT_MODE=1 wrapper
    sp = os.path.join(d, "gl_substrate.zag")
    s = read(sp)
    s += SUB_APPEND.format(mode=1)
    write(sp, s)
    # 2. learner: tn_ep_info -> rt_ep_info
    lp = os.path.join(d, "gl_learner.zag")
    s = read(lp)
    assert s.count("tn_ep_info(") >= 1, (tag, "tn_ep_info anchor")
    s = s.replace("tn_ep_info(", "rt_ep_info(")
    # 3. aa gate patch (verbatim RT2)
    assert s.count(AA_OLD) == 1, (tag, "aa anchor")
    s = s.replace(AA_OLD, AA_NEW)
    # 4. rt_fact helper + facts block (verbatim RT2)
    assert s.count(ARM_FN) == 1, (tag, "arm fn anchor")
    s = s.replace(ARM_FN, FACT_HELPER + "\n" + ARM_FN)
    assert s.count(FREE_ANCHOR) == 1, (tag, "free anchor")
    s = s.replace(FREE_ANCHOR, FACTS_BLOCK + FREE_ANCHOR)
    # 5. main() replacement: RT-D cell
    mi = s.index("fn main()i32 {")
    s = s[:mi]
    s += ("fn main()i32 {\n    let f:i32=0;\n    f=f+arm_gl(1,0,\"rtd_\");\n"
          "    _zag_print(\"RT_DONE,\");_zag_print(\"%s\");_zag_println(\"\");\n"
          "    return 0;\n}\n" % tag)
    write(lp, s)
    no_rng_scan(d, tag, ("gl_learner.zag", "gl_substrate.zag"))
    return (tag,) + compile_and_run(d, "gl_learner.zag", tag)


def build_unit(fork):
    tag = "unit_%s" % fork
    d = os.path.join(BUILD, tag)
    if os.path.isdir(d):
        shutil.rmtree(d)
    os.makedirs(d)
    shutil.copy(os.path.join(FORKS, fork, "gl_substrate.zag"), os.path.join(d, "gl_substrate.zag"))
    shutil.copy(os.path.join(UNIT, "unit_%s.zag" % fork), os.path.join(d, "unit_%s.zag" % fork))
    no_rng_scan(d, tag, ("gl_substrate.zag", "unit_%s.zag" % fork))
    return (tag,) + compile_and_run(d, "unit_%s.zag" % fork, tag)


def check_fid_gate():
    """Parse FID evidence; return list of failures (empty = gate passed)."""
    fails = []
    for fork in FORK_NAMES:
        p = os.path.join(EV, "%s_FID_run1.txt" % fork)
        checks = {}
        with open(p) as f:
            for line in f:
                if line.startswith("TN_CHECK,"):
                    parts = line.rstrip("\n").split(",")
                    if len(parts) == 4:
                        checks[parts[1]] = int(parts[2])
                elif line.startswith("TN_FAILURES,"):
                    checks["TN_FAILURES"] = int(line.rstrip("\n").split(",")[1])
        if checks.get("TN_FAILURES", -1) != 0:
            fails.append((fork, "TN_FAILURES=%s" % checks.get("TN_FAILURES")))
        if checks.get("glh_audit_total", -1) != 269:
            fails.append((fork, "glh_audit_total=%s" % checks.get("glh_audit_total")))
        if checks.get("gll_audit_total", -1) != 271:
            fails.append((fork, "gll_audit_total=%s" % checks.get("gll_audit_total")))
    return fails


def main():
    phase = sys.argv[1] if len(sys.argv) > 1 else "all"
    os.makedirs(BUILD, exist_ok=True)
    os.makedirs(EV, exist_ok=True)
    fails = []
    if phase in ("all", "fid"):
        for fork in FORK_NAMES:
            tag, det, msg = build_fid(fork)
            print("%-10s det=%s %s" % (tag, det, msg), flush=True)
            if not det or msg.startswith("COMPILE"):
                fails.append(tag)
        gfails = check_fid_gate()
        print("FIDELITY GATE: %s" % ("PASS" if not gfails else "FAIL %s" % gfails))
        fails += ["gate:" + g[0] for g in gfails]
        if gfails:
            print("GATE FAILED - attack cells will not be built")
            return 1
    if phase in ("all", "attack"):
        for fork in FORK_NAMES:
            tag, det, msg = build_attack(fork)
            print("%-10s det=%s %s" % (tag, det, msg), flush=True)
            if not det or msg.startswith("COMPILE"):
                fails.append(tag)
    if phase in ("all", "unit"):
        for fork in FORK_NAMES:
            tag, det, msg = build_unit(fork)
            print("%-10s det=%s %s" % (tag, det, msg), flush=True)
            if not det or msg.startswith("COMPILE"):
                fails.append(tag)
    print("FAILS=%d %s" % (len(fails), fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
