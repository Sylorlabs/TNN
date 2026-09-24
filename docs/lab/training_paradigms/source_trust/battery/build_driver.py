#!/usr/bin/env python3
"""Generate driver_<fork>.zag from driver_template.zag and compile with znc.

Usage: build_driver.py <k|l|s|floor>

Per-fork contract (frozen by each fork's build spec; never edited here):
  k: k_new/k_decide/k_world/k_warrant      (worldfn mode: k_world on WORLD)
  l: st_hist_new/decide/st_world/st_warrant (worldfn mode: st_world on WORLD)
  s: s_init/s_decide/s_note/s_warrant       (note mode: s_note on EVERY episode)
  floor: f_new/f_decide/f_world/f_warrant   (worldfn mode, no-op)

The fork source is copied verbatim to build_<fork>/fork.zag; the driver
@import("fork.zag") resolves relative to the build cwd. Fork logic is never
modified — only this adapter layer is generated.
"""
import sys, os, shutil, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ZNC = os.path.expanduser("~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1")
LAB = os.path.expanduser("~/workspace/tnn-lab/training_paradigms/source_trust")

CONFIGS = {
    "k": dict(hist_ty="KHist", fnew="k_new", fdecide="k_decide",
               fwarrant="k_warrant",
               event="if(et==2){k_world(key as i32,val as i32,hp);}",
               src=os.path.join(LAB, "fork_k/k.zag")),
    "l": dict(hist_ty="ForkHist", fnew="st_hist_new", fdecide="decide",
               fwarrant="st_warrant",
               event="if(et==2){st_world(key as i32,val as i32,hp);}",
               src=os.path.join(LAB, "fork_l/fork_l.zag")),
    "s": dict(hist_ty="ForkHist", fnew="s_init", fdecide="s_decide",
               fwarrant="s_warrant",
               event="s_note(ep as i32,et as i32,src as i32,key as i32,val as i32,hp);",
               src=os.path.join(LAB, "fork_s/fork_s.zag")),
    "floor": dict(hist_ty="FHist", fnew="f_new", fdecide="f_decide",
               fwarrant="f_warrant",
               event="if(et==2){f_world(key as i32,val as i32,hp);}",
               src=os.path.join(HERE, "floor.zag")),
}

def build(fork):
    cfg = CONFIGS[fork]
    bdir = os.path.join(HERE, "build_%s" % fork)
    os.makedirs(bdir, exist_ok=True)
    tpl = open(os.path.join(HERE, "driver_template.zag")).read()
    src = (tpl.replace("%%HIST_TY%%", cfg["hist_ty"])
              .replace("%%FNEW%%", cfg["fnew"])
              .replace("%%FDECIDE%%", cfg["fdecide"])
              .replace("%%FWARRANT%%", cfg["fwarrant"])
              .replace("%%EVENT_BLOCK%%", cfg["event"]))
    assert "%%" not in src, "unsubstituted placeholder in generated driver"
    dpath = os.path.join(bdir, "driver_%s.zag" % fork)
    open(dpath, "w").write(src)
    shutil.copyfile(cfg["src"], os.path.join(bdir, "fork.zag"))
    r = subprocess.run([ZNC, "driver_%s.zag" % fork, "-o", "bin_%s" % fork],
                       cwd=bdir, capture_output=True, text=True)
    if r.stdout:
        print(r.stdout[-1500:])
    if r.returncode != 0 or not os.path.exists(os.path.join(bdir, "bin_%s" % fork)):
        print(r.stderr[-3000:] if r.stderr else "", file=sys.stderr)
        print("BUILD FAILED for", fork, file=sys.stderr)
        sys.exit(1)
    print("built driver for fork:", fork)

if __name__ == "__main__":
    build(sys.argv[1])
