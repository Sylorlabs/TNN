#!/usr/bin/env python3
"""verify_b3536_classes.py — class-identity check: every class-defining
constant/expression from RT-JKLM's frozen attack drivers (ec8d5d13) must
appear verbatim in comp_drive.zag (no drift in the composition's classes).
"""
import os
import subprocess
import sys

REPO = os.path.expanduser("~/workspace/selfpam_run/tnn-lab")
WORK = os.path.expanduser("~/workspace/b3536_scratch")

FROZEN = {
    "drive35": "docs/lab/senses/pam-rebuild/round2/rt_jklm/drive35.zag",
    "drive36": "docs/lab/senses/pam-rebuild/round2/rt_jklm/drive36.zag",
}


def gshow(path):
    r = subprocess.run(["git", "show", f"ec8d5d13:{path}"],
                       capture_output=True, text=True, cwd=REPO)
    assert r.returncode == 0
    return r.stdout


def main():
    d35 = gshow(FROZEN["drive35"])
    d36 = gshow(FROZEN["drive36"])
    r36p = subprocess.run(["git", "show",
                           "6a30f5f9:docs/lab/senses/pam-rebuild/round2/r36_repair/r36_probe.zag"],
                          capture_output=True, text=True, cwd=REPO)
    assert r36p.returncode == 0
    r36 = r36p.stdout
    with open(os.path.join(WORK, "comp_drive.zag")) as f:
        drv = f.read()

    # (frozen_file, frozen_source, class, pattern that must appear in driver)
    checks = [
        # J35 (drive35::run_j)
        ("d35", "id base 1000+t", "J35", ".id=1000 + t"),
        ("d35", "conf 715+(t%5)", "J35", ".conf=715 + (t % 5)"),
        ("d35", "meas 2625+t*10", "J35", ".meas=2625 + t * 10"),
        ("d35", "id offset (t+4)*17", "J35", "((t + 4) * 17)"),
        ("d35", "conf offset (t+2)*7", "J35", "((t + 2) * 7)"),
        ("d35", "meas offset (t+3)*13", "J35", "((t + 3) * 13)"),
        ("d35", "label offset (t+1)*3", "J35", "((t + 1) * 3)"),
        # K35 (drive35::run_k)
        ("d35", "id base 2000+t", "K35", ".id=2000 + t"),
        ("d35", "conf/meas 6000+(t%3)", "K35", "6000 + (t % 3)"),
        ("d35", "six paths x20", "K35", "let path:i64 = t / 20;"),
        # L35 (drive35::run_l)
        ("d35", "forge id base 3000+t", "L35", "forge(3000 + t,"),
        ("d35", "replay source 4000/715/2625", "L35", ".id=4000, .conf=715, .meas=2625"),
        ("d35", "replay target 4001/999/8888", "L35", ".id=4001, .conf=999, .meas=8888"),
        # M35 (drive35::run_m)
        ("d35", "gh guess t*2654435761+1", "M35", "((t * 2654435761 + 1) as u64)"),
        ("d35", "gl guess t*40503+7", "M35", "((t * 40503 + 7) as u64)"),
        ("d35", "id base 5000+t", "M35", "forge(5000 + t,"),
        # J36 (drive36::run_j)
        ("d36", "spoofed id base 7000+t", "J36", "let id:i64 = 7000 + t;"),
        # K36 (drive36::run_k)
        ("d36", "id base 9000+t", "K36", "let id:i64 = 9000 + t;"),
        ("d36", "blind modal conf", "K36", "let conf:i64 = adv36_conf(t);"),
        ("d36", "blind modal meas", "K36", "let meas:i64 = adv36_meas(t);"),
        # L36 (drive36::run_l)
        ("d36", "junk commit id 9999", "L36", "cstep(bs, 9999, t, t * 2, 5)"),
        ("d36", "sample arena stride 8", "L36", "(t as i32) * 8"),
        # M36 (drive36::run_m as re-hosted by R-36 gen_r36.py -> m36a_precompute)
        ("d36", "id base 8000+t", "M36", "let id:i64 = 8000 + t;"),
        ("r36", "precompute call (gen_r36.py from drive36::run_m)", "M36", "m36a_precompute(A, B, bs);"),
        # honest-35 control
        ("d35", "honest id base 5000+t", "HONEST", ".id=5000 + t"),
    ]
    srcs = {"d35": d35, "d36": d36, "r36": r36}
    fails = 0
    for src_key, desc, cls, pat in checks:
        frozen_ok = pat in srcs[src_key]
        drv_ok = pat in drv
        status = "OK" if (frozen_ok and drv_ok) else "FAIL"
        if status == "FAIL":
            fails += 1
        print(f"[{status}] {cls}: {desc} (frozen={frozen_ok} driver={drv_ok})", flush=True)
    assert fails == 0, f"{fails} class-identity checks FAILED"
    print("class identity: no drift", flush=True)


if __name__ == "__main__":
    main()
