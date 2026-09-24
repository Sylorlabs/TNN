#!/usr/bin/env python3
"""gen_cp_fse1b.py -- FS-E1b design-loop / post-freeze challenge-prediction (CP).

Colorconst only (the redesigned task). The adversary knows the repaired
registry (CH-CCN-3r) and the real fse1b binary. Deterministic search
(master seed, budget 5000 candidates) for scenes that make the REAL binary
INSTALL a claim != truth.

A candidate is KEPT iff BOTH hold:
  (i)  the fse1b binary INSTALLS a claim != truth, and
  (ii) truth is unambiguous under the frozen strong-truth criterion
       (PREREG_FS-E1.md: DIFFERENT iff different crops, or a local edit
       covering >=2x2 px each with per-pixel L1 >= 32; SAME iff identical
       crops; else AMBIGUOUS, not keep-eligible).

Usage: gen_cp_fse1b.py <master_seed> <outdir> <tag>
  outdir: fixtures dir (kept fixtures + ledger + manifest land here)
  tag: label used in fixture names and the ledger (e.g. design_20260923)

Python is fixture generation only -- never in any decision path.
"""
import sys, os, json, struct, hashlib, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
FORK = os.path.normpath(os.path.join(HERE, ".."))
FSE1_SRC = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2/forks/FS-E1/src"
sys.path.insert(0, FSE1_SRC)
import gen_cp_fse1 as P
import gen_r2a as G

CP_BUDGET = 5000
CP_KEEP = 100
CP_FAMILY = 4
CP_INDEX_BASE = 9000
BIN = os.path.join(FORK, "build", "fse1b")
TID = 1  # colorconst

CANDS = ([P.cand_ccn_patch] * 8 + [P.cand_ccn_xcrop] * 6 +
         [P.cand_ccn_mixed] * 3 + [P.cand_ccn_patch] * 3)

def run_binary(fx_path):
    ledger = fx_path + ".ledger"
    r = subprocess.run([BIN, "full", fx_path, ledger],
                       capture_output=True, text=True, timeout=60)
    out = {}
    for line in r.stdout.splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip()
    return out

def main():
    master = int(sys.argv[1])
    outdir = sys.argv[2]
    tag = sys.argv[3]
    scratch = os.path.join(FORK, "scratch_cp", "cpb_%s" % tag)
    os.makedirs(scratch, exist_ok=True)
    os.makedirs(outdir, exist_ok=True)
    kept = []
    n = 0
    for ci in range(CP_BUDGET):
        fn = CANDS[ci % len(CANDS)]
        rng = G.Rng(G.stream_seed(master, TID * 100 + (ci % len(CANDS)), ci))
        try:
            f, g, truth, strong, note = fn(rng, ci)
        except Exception:
            continue
        n += 1
        fx = os.path.join(scratch, "cp_ccn_%d.r2fx" % ci)
        P.write_r2fx(fx, TID, CP_INDEX_BASE + ci, 40, f, g)
        try:
            out = run_binary(fx)
        except Exception:
            continue
        disp = out.get("disposition", "?")
        claim = out.get("judgment", "?")
        tnorm = ("DIFFERENT" if truth == "DIFFERENT" else
                 "SAME" if truth == "SAME_SURFACE" else "AMBIG")
        cnorm = ("DIFFERENT" if claim == "DIFFERENT" else
                 "SAME" if claim == "SAME_SURFACE" else "?")
        if disp == "INSTALL" and cnorm != tnorm and tnorm != "AMBIG" and strong:
            kept.append((ci, note, truth, claim))
            if len(kept) >= CP_KEEP:
                break
        if (ci + 1) % 500 == 0:
            print("seed %d: %d/%d candidates, %d kept"
                  % (master, ci + 1, CP_BUDGET, len(kept)), flush=True)
    print("SEED %d: %d candidates run, %d KEPT" % (master, n, len(kept)),
          flush=True)
    manifest = []
    ledger_f = open(os.path.join(outdir, "cp_%s_ledger.jsonl" % tag), "w")
    for ki, (ci, note, truth, claim) in enumerate(kept):
        src = os.path.join(scratch, "cp_ccn_%d.r2fx" % ci)
        dst = os.path.join(outdir, "cp_ccn_%s_%d.r2fx" % (tag, ki))
        with open(src, "rb") as a, open(dst, "wb") as b:
            b.write(a.read())
        with open(dst, "r+b") as fh:
            fh.seek(0)
            hdr = fh.read(32)
            magic, t, i, fam, fo, fl, go, gl = struct.unpack("<8I", hdr)
            fh.seek(0)
            fh.write(struct.pack("<8I", magic, t, CP_INDEX_BASE + ki,
                                 CP_FAMILY, fo, fl, go, gl))
        tval = "DIFFERENT" if truth == "DIFFERENT" else "SAME_SURFACE"
        with open(dst + ".truth", "w") as tf:
            tf.write("truth=%s\n" % tval)
        h = hashlib.sha256(open(dst, "rb").read()).hexdigest()
        manifest.append("%s  ./cp_ccn_%s_%d.r2fx\n" % (h, tag, ki))
        ledger_f.write(json.dumps({"seed": master, "tag": tag, "idx": ki,
                                   "src_ci": ci, "note": note, "truth": tval,
                                   "claim": claim, "sha256": h}) + "\n")
    ledger_f.close()
    with open(os.path.join(outdir, "cp_%s_manifest.sha256" % tag), "w") as mf:
        mf.writelines(manifest)
    print("CP %s COMPLETE: %d kept total" % (tag, len(kept)))

if __name__ == "__main__":
    main()
