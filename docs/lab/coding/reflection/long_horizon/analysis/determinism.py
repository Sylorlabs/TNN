#!/usr/bin/env python3
"""Determinism check: 5 reps of full pipeline for 5 stages, byte-identical."""
import subprocess, os, sys, hashlib

WORKDIR = os.path.expanduser("~/workspace/lh_trial")
STAGES = ["A3", "B4", "C4", "A8", "B6"]  # per prereg

def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr

def sha(b):
    return hashlib.sha256(b).hexdigest()

def main():
    kb = open(os.path.join(WORKDIR, "lh_kb.txt")).read()
    delib = os.path.join(WORKDIR, "lh_delib")
    emit = os.path.join(WORKDIR, "lh_emit")
    znc = os.path.expanduser("~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1")

    all_ok = True
    for stage in STAGES:
        contract = open(os.path.join(WORKDIR, "contracts", f"{stage}.txt")).read()
        reps = []
        for rep in range(5):
            # propose
            rc, prop_out, _ = run([delib, "propose", stage, contract, kb])
            cand = [l for l in prop_out.split("\n") if l.startswith("CAND ")][0]
            # critique
            rc, crit_out, _ = run([delib, "critique", stage, contract, cand])
            acc = [l for l in crit_out.split("\n") if l.startswith("ACCEPT ")][0]
            spec = acc.split(" ", 2)[2]
            # compose
            rc, comp_out, _ = run([delib, "compose", stage, spec, f"{stage}-C1"])
            final_spec = [l for l in comp_out.split("\n") if l.startswith("FINAL ")][0][6:]
            # gen
            rc, gen_out, _ = run([emit, "gen", final_spec])
            # compile
            src = f"/tmp/det_{stage}_{rep}.zag"
            binp = f"/tmp/det_{stage}_{rep}_bin"
            open(src, "w").write(gen_out)
            run([znc, src, "-o", binp, "--no-analyze", "--no-zagd"])
            bin_bytes = open(binp, "rb").read()
            # run first test
            import re
            m = re.search(r'TEST in="(.*)" out="(.*)"', contract)
            tin, tout = m.group(1), m.group(2)
            if "|AGG|" in final_spec or "|SORT|" in final_spec:
                recs = tin.split(";")
                cmd = [binp, str(len(recs))] + recs
            else:
                cmd = [binp, tin]
            rc, rout, _ = run(cmd)
            reps.append({
                "spec": sha(final_spec.encode()),
                "src": sha(gen_out.encode()),
                "bin": sha(bin_bytes),
                "out": sha(rout.encode()),
            })
        # Compare all reps to rep 0
        ok = all(r == reps[0] for r in reps[1:])
        status = "PASS" if ok else "FAIL"
        print(f"{stage}: {status} (5 reps byte-identical: {ok})")
        if not ok:
            all_ok = False
            for i, r in enumerate(reps):
                print(f"  rep{i}: spec={r['spec'][:12]} src={r['src'][:12]} bin={r['bin'][:12]} out={r['out'][:12]}")
    print("DETERMINISM:", "PASS" if all_ok else "FAIL")
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
