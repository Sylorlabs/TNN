#!/usr/bin/env python3
"""FL2 RT-B fork-test battery: patch verified bases, build, run twice, save evidence.

Bases are the verified RT2 artifacts (SHA-checked before patching):
  default_B   = RT-B attack cell (RT_MODE=3, main=arm_gl(2,1,"rtb_"))
  default_FID = fidelity cell  (RT_MODE=0, original main)
Fork patches touch gl_learner.zag only, via exact anchors (asserted).
"""
import difflib
import hashlib
import os
import re
import shutil
import subprocess
import sys

ZNC = os.path.expanduser("~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1")
ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_B = "/home/hatch/workspace/fl2rt/harnesses/default_B"
BASE_FID = "/home/hatch/workspace/fl2rt/harnesses/default_FID"
EV_B = "/home/hatch/workspace/fl2rt/evidence/default_B_sources.txt"
EV_FID = "/home/hatch/workspace/fl2rt/evidence/default_FID_sources.txt"
BUILD = os.path.join(ROOT, "build")
EV = os.path.join(ROOT, "evidence")
FILES = ["gl_learner.zag", "gl_substrate.zag"]


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


def check_base_shas(basedir, sources_txt):
    """Assert the base files are byte-identical to the frozen RT2 record."""
    want = {}
    for line in read(sources_txt).splitlines():
        sha, fn = line.split()
        want[fn] = sha
    for fn in FILES:
        got = sha256_file(os.path.join(basedir, fn))
        assert got == want[fn], (basedir, fn, got[:12], want[fn][:12])
    print("base OK: %s matches frozen record" % basedir)


# ---------------- fork patches (frozen per PREREG.md) ----------------

F1_BLOCK = """\
                // F1: endogenous verification channel (retrievability law-check,
                // f3 law-check class). After acting, the taught association (k,v)
                // must be retrievable from the learner's OWN store: main[k]==v or
                // quarantine holds (k,v). If not, the acted rule's effect contradicts
                // the memory system's own purpose; feed the SAME eliminative
                // machinery (survivor selection over sig0/sig1/sig2). General:
                // names no rule; applies to any present or future policy. The -3
                // SCAFFOLD aux marks endogenous (vs -1 world-signal) revocation.
                if(rc==TN_OK && revoke_step<0 && provisional>=0){
                    let retrievable:i32=0;
                    if(tn_main_has(mkey,mval,TN_NMAIN,k,v)==1){retrievable=1;}
                    if(tn_quar_has(qkey,qval,TN_NQUAR,k,v)==1){retrievable=1;}
                    if(retrievable==0){
                        let surv:i32=-1;
                        if(sig0>=1){surv=0;}
                        if(sig1>=1 && surv<0){surv=1;}
                        if(sig2>=1 && surv<0){surv=2;}
                        if(surv>=0){
                            let r2:i32=tn_audit(audit,&acount,ep,TN_OP_SCAFFOLD,act,-3);
                            if(r2==TN_OK){r2=tn_audit(audit,&acount,ep,TN_OP_UNINSTALL_PROVISIONAL,0,act);}
                            if(r2==TN_OK){r2=tn_audit(audit,&acount,ep,TN_OP_COMMIT,1,surv);}
                            if(r2==TN_OK){
                                provisional=-1;
                                committed[0]=surv as u8;
                                if(revoke_step<0){revoke_step=ep;}
                            }
                            if(r2!=TN_OK){rc=r2;}
                        }
                    }
                }
"""

F1_ANCHOR = """                    }
                }
            }
        }
        if(rc==TN_OK && kind==4){"""

F1_REPL = """                    }
                }
""" + F1_BLOCK + """            }
        }
        if(rc==TN_OK && kind==4){"""

LOCALS_ANCHOR = "    let connected:i32=1;let fire_step:i32=-1;let revoke_step:i32=-1;"
AA_ANCHOR = "                if(ep>=29 && ep<=48 && RT_MODE!=2 && RT_MODE!=3){aa=1;}"
GATE_ANCHOR = "        if(ep==48 && revoke_step<0 && provisional>=0){"
PSH_ANCHOR = '    f=f+arm_gl(2,1,"rtb_");'


def patch_f1(s):
    assert s.count(F1_ANCHOR) == 1, ("F1 anchor", s.count(F1_ANCHOR))
    return s.replace(F1_ANCHOR, F1_REPL)


def patch_testedness(s, kind, kval):
    """kind: 'seen' (F2) or 'count' (R1). kval: None or K."""
    assert s.count(LOCALS_ANCHOR) == 1, ("locals anchor", s.count(LOCALS_ANCHOR))
    assert s.count(AA_ANCHOR) == 1, ("aa anchor", s.count(AA_ANCHOR))
    assert s.count(GATE_ANCHOR) == 1, ("gate anchor", s.count(GATE_ANCHOR))
    if kind == "seen":
        s = s.replace(LOCALS_ANCHOR, LOCALS_ANCHOR + "let aa_seen:i32=0;")
        s = s.replace(AA_ANCHOR, AA_ANCHOR + "\n                if(aa==1){aa_seen=1;}")
        s = s.replace(GATE_ANCHOR,
                      "        if(ep==48 && revoke_step<0 && provisional>=0 && aa_seen==1){")
    else:
        s = s.replace(LOCALS_ANCHOR, LOCALS_ANCHOR + "let aa_count:i32=0;")
        s = s.replace(AA_ANCHOR, AA_ANCHOR + "\n                if(aa==1){aa_count=aa_count+1;}")
        s = s.replace(GATE_ANCHOR,
                      "        if(ep==48 && revoke_step<0 && provisional>=0 && aa_count>=%d){" % kval)
    return s


def patch_psh(s):
    assert s.count(PSH_ANCHOR) == 1, ("psh anchor", s.count(PSH_ANCHOR))
    return s.replace(PSH_ANCHOR, '    f=f+arm_gl(1,0,"psh_");')


FORKS = {
    "f1": lambda s: patch_f1(s),
    "f2": lambda s: patch_testedness(s, "seen", None),
    "f3": lambda s: patch_testedness(patch_f1(s), "seen", None),
    "r1a": lambda s: patch_testedness(s, "count", 3),
    "r1b": lambda s: patch_testedness(s, "count", 8),
    "ctl": lambda s: s,
}

# (tag, fork, base, psh?)
CELLS = []
for fk in ["f1", "f2", "f3", "r1a", "r1b"]:
    CELLS.append(("%s_FID" % fk, fk, "FID", False))
    CELLS.append(("%s_B" % fk, fk, "B", False))
    CELLS.append(("%s_PSH" % fk, fk, "B", True))
CELLS.append(("ctl_FID", "ctl", "FID", False))
CELLS.append(("ctl_B", "ctl", "B", False))


def build_cell(tag, fork, base, psh):
    d = os.path.join(BUILD, tag)
    if os.path.isdir(d):
        shutil.rmtree(d)
    os.makedirs(d)
    basedir = BASE_B if base == "B" else BASE_FID
    for fn in FILES:
        shutil.copy(os.path.join(basedir, fn), os.path.join(d, fn))

    lp = os.path.join(d, "gl_learner.zag")
    s = read(lp)
    base_src = s
    s = FORKS[fork](s)
    if psh:
        s = patch_psh(s)
    write(lp, s)

    # unified diff vs base (for the complexity measure)
    diff = "".join(difflib.unified_diff(
        base_src.splitlines(True), s.splitlines(True),
        fromfile="base/gl_learner.zag", tofile=tag + "/gl_learner.zag"))
    with open(os.path.join(EV, "%s_diff.txt" % tag), "w") as f:
        f.write(diff)

    # static no-randomness check on patched sources
    for fn in FILES:
        code = re.sub(r"//.*", "", read(os.path.join(d, fn)))
        hits = re.findall(r"(?i)\brng\b|rand\(|srand|/dev/urandom|[^a-z]seed[^a-z]", code)
        assert not hits, (tag, fn, hits)

    binp = os.path.join(d, "rtbin")
    cp = subprocess.run([ZNC, os.path.join(d, "gl_learner.zag"), "--no-zagd",
                         "--no-analyze", "--no-foreground-cache", "-o", binp],
                        cwd=d, capture_output=True, text=True, timeout=600)
    if cp.returncode != 0:
        return (tag, False, "COMPILE FAIL: " + cp.stderr[-2000:])

    outs = []
    for _ in (1, 2):
        r = subprocess.run([binp], cwd=d, capture_output=True, text=True, timeout=600)
        outs.append(r.stdout)
    h1 = hashlib.sha256(outs[0].encode()).hexdigest()
    h2 = hashlib.sha256(outs[1].encode()).hexdigest()
    det = (h1 == h2)
    with open(os.path.join(EV, "%s_run1.txt" % tag), "w") as f:
        f.write(outs[0])
    with open(os.path.join(EV, "%s_run2.txt" % tag), "w") as f:
        f.write(outs[1])
    with open(os.path.join(EV, "%s_meta.txt" % tag), "w") as f:
        f.write("tag=%s\nsha1=%s\nsha2=%s\ndeterministic=%s\n" % (tag, h1, h2, det))
    with open(os.path.join(EV, "%s_sources.txt" % tag), "w") as f:
        for fn in FILES:
            f.write("%s  %s\n" % (sha256_file(os.path.join(d, fn)), fn))
    return (tag, det, "OK sha=%s" % h1[:12])


def main():
    only = sys.argv[1:] or None
    os.makedirs(BUILD, exist_ok=True)
    os.makedirs(EV, exist_ok=True)
    check_base_shas(BASE_B, EV_B)
    check_base_shas(BASE_FID, EV_FID)
    cells = CELLS
    if only:
        cells = [c for c in cells if c[0] in only]
    fails = []
    for (tag, fork, base, psh) in cells:
        tag2, det, msg = build_cell(tag, fork, base, psh)
        print("%-10s det=%s %s" % (tag2, det, msg), flush=True)
        if not det or msg.startswith("COMPILE"):
            fails.append(tag2)
    print("CELLS=%d FAILS=%d %s" % (len(cells), len(fails), fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
