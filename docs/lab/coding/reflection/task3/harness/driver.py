#!/usr/bin/env python3
"""Task-3 deterministic harness driver. Plumbing only: compile, run, check, log.
Makes NO coding decisions. The builder (learner) reads records and decides.
"""
import json, os, subprocess, sys, time, hashlib

ZNC = "/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1"

def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def run(cmd, cwd, timeout=60):
    t0 = time.time()
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, timeout=timeout)
    return p.returncode, p.stdout, p.stderr, time.time() - t0

def main():
    # argv: step --id ID --arm ARM --deliv DELIV --src SRC --workdir WD
    #          --checker CHECKER [--cmode MODE] [--runarg A ...] [--log LOG]
    a = sys.argv[1:]
    assert a[0] == "step", "only 'step' supported"
    kw = {}
    runargs = []
    i = 1
    while i < len(a):
        if a[i] == "--runarg":
            runargs.append(a[i+1]); i += 2
        elif a[i].startswith("--"):
            kw[a[i][2:]] = a[i+1]; i += 2
        else:
            i += 1
    wid, arm, deliv = kw["id"], kw["arm"], kw["deliv"]
    src, wd = kw["src"], kw["workdir"]
    checker, cmode, logf = kw.get("checker"), kw.get("cmode"), kw["log"]
    hdr = os.path.dirname(os.path.abspath(__file__))
    if checker and not os.path.isabs(checker):
        checker = os.path.join(hdr, checker)
    srcdir = os.path.dirname(os.path.abspath(src))
    srcbase = os.path.basename(src)
    binpath = os.path.join(os.path.abspath(wd), wid)
    os.makedirs(os.path.abspath(wd), exist_ok=True)

    rec = {"id": wid, "arm": arm, "deliv": deliv, "src": srcbase,
           "src_sha256": sha(open(src, "rb").read())}
    # 1. compile (deterministic flags; cwd = source dir so @imports resolve)
    rc, out, err, dt = run([ZNC, srcbase, "-o", binpath,
                            "--no-analyze", "--no-zagd"], cwd=srcdir)
    rec["compile"] = {"rc": rc, "ms": round(dt*1000),
                      "stderr_sha256": sha(err), "stderr": err.decode("utf-8", "replace")}
    if rc != 0:
        rec["outcome"] = "compile-fail"
        emit(rec, logf); return
    # 2. run
    rc, out, err, dt = run([binpath] + runargs, cwd=os.path.abspath(wd), timeout=30)
    rec["run"] = {"rc": rc, "ms": round(dt*1000),
                  "stdout_sha256": sha(out), "stderr_sha256": sha(err),
                  "stderr": err.decode("utf-8", "replace")}
    if rc != 0:
        rec["outcome"] = "run-fail"
        emit(rec, logf); return
    # stash stdout for the checker
    outpath = binpath + ".stdout"
    open(outpath, "wb").write(out)
    # 3. check (checker reads program stdout on stdin; sees workdir via cwd)
    ccmd = [sys.executable, checker]
    if cmode:
        ccmd += ["--mode", cmode]
    p = subprocess.run(ccmd, stdin=open(outpath, "rb"), capture_output=True,
                       cwd=os.path.abspath(wd), timeout=30)
    rec["check"] = {"rc": p.returncode,
                    "report": p.stdout.decode("utf-8", "replace"),
                    "stderr": p.stderr.decode("utf-8", "replace")}
    rec["outcome"] = "pass" if p.returncode == 0 else "check-fail"
    emit(rec, logf)

def emit(rec, logf):
    line = json.dumps(rec, sort_keys=True)
    with open(logf, "a") as f:
        f.write(line + "\n")
    print(line)

if __name__ == "__main__":
    main()
