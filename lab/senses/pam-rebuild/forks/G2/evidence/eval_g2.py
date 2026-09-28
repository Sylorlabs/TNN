#!/usr/bin/env python3
"""G2 (PRP) head-to-head evaluation vs Approach A. Mechanical B1-B6.

Runs:
  1. A single-mode over all 925 harness fixtures -> per-task accuracy
  2. G2 single-mode over all 925 harness fixtures -> B1, B2, B3, integration
  3. G2 augmentations (240, via augment.py) -> adversarial material
  4. G2 batch mode: 425 adversarial x contract vs ablated -> B4, B5
  5. Determinism: 3x byte-identical runs (single subset + full batch) -> B6
  6. Independent FNV-1a-64 ledger re-verification (python) -> B6
Writes evidence/EVAL_G2.md.
"""
import os, re, subprocess, sys, time, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
G2DIR = os.path.normpath(os.path.join(HERE, ".."))
G2BIN = os.path.join(G2DIR, "src", "sense")
ABIN = os.path.join(HERE, "bin_A")
HARNESS = os.path.normpath(os.path.join(
    G2DIR, "..", "..", "..", "rebuild", "harness", "fixtures"))
AUG = os.path.join(G2DIR, "augment", "out")
SCRATCH = os.path.expanduser("~/workspace/tmp_commit/g2eval")
os.makedirs(SCRATCH, exist_ok=True)

TASKS = [
    ("colordisc", "t1_colordisc", ".img"),
    ("colorconst", "t2_colorconst", ".img"),
    ("shapetrans", "t3_shapetrans", ".img"),
    ("pitchdisc", "t4_pitchdisc", ".pcm"),
    ("timbredisc", "t5_timbredisc", ".pcm"),
    ("motiondir", "t6_motiondir", ".vid"),
]
TID = {t: i + 1 for i, (t, _, _) in enumerate(TASKS)}
JCODE = {  # task-keyed; must match parse_truth() in g2_sense.zag exactly
    ("colordisc", "SAME"): 0, ("colordisc", "DIFFERENT"): 1,
    ("colorconst", "SAME_SURFACE"): 0, ("colorconst", "DIFFERENT"): 1,
    ("shapetrans", "CIRCLE"): 0, ("shapetrans", "SQUARE"): 1,
    ("shapetrans", "TRIANGLE"): 2,
    ("pitchdisc", "SAME"): 0, ("pitchdisc", "HIGHER"): 1,
    ("pitchdisc", "LOWER"): 2,
    ("timbredisc", "PURE"): 0, ("timbredisc", "DARK"): 1,
    ("timbredisc", "RICH"): 2, ("timbredisc", "BRIGHT"): 3,
    ("motiondir", "STILL"): 0, ("motiondir", "N"): 1,
    ("motiondir", "NE"): 2, ("motiondir", "E"): 3,
    ("motiondir", "SE"): 4, ("motiondir", "S"): 5,
    ("motiondir", "SW"): 6, ("motiondir", "W"): 7,
    ("motiondir", "NW"): 8,
}
VARIANTS = ["primary", "noise", "adversarial"]

def run_bin(args, timeout=120):
    t0 = time.time()
    p = subprocess.run(args, capture_output=True, timeout=timeout)
    return p.returncode, p.stdout, time.time() - t0

def parse_kv(out):
    d = {}
    for line in out.decode("utf-8", "replace").splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            d[k] = v
    return d

def truth_of(path):
    with open(path + ".truth") as f:
        return f.read().strip().split("=", 1)[1]

def fixtures(task, tdir, ext, variant, base):
    d = os.path.join(base, tdir, variant)
    return sorted(os.path.join(d, f) for f in os.listdir(d) if f.endswith(ext))

# ---------------- FNV-1a-64 (independent reimplementation) ----------------
FNV_INIT = 14695981039346656037
FNV_PRIME = 1099511628211
MASK = 0xFFFFFFFFFFFFFFFF
def fnv_str(s):
    h = FNV_INIT
    for ch in s:
        h = ((h ^ ord(ch)) * FNV_PRIME) & MASK
    return h
def fnv_bytes(h, data):
    for b in data:
        h = ((h ^ b) * FNV_PRIME) & MASK
    return h

def main():
    assert os.path.exists(G2BIN), "G2 binary missing"
    assert os.path.exists(ABIN), "A binary missing"
    R = {"A": {}, "G2": {}}
    # ---------- 1+2: single-mode sweeps (cached) ----------
    cache_p = os.path.join(SCRATCH, "sweeps.json")
    import json as _json
    if os.path.exists(cache_p):
        with open(cache_p) as f:
            _R = _json.load(f)
        # json stringified the tuple keys; restore them
        import ast as _ast
        R = {lab: {_ast.literal_eval(k): v for k, v in d.items()}
             for lab, d in _R.items()}
        print("loaded cached sweeps", flush=True)
    else:
        def _save():
            with open(cache_p, "w") as f:
                _json.dump({lab: {repr(k): v for k, v in d.items()}
                            for lab, d in R.items()}, f)
        for label, binary, extra_keys in (("A", ABIN, []), ("G2", G2BIN, [])):
            for task, tdir, ext in TASKS:
                for variant in VARIANTS:
                    key = (task, variant)
                    R[label][key] = {"n": 0, "correct": 0, "ops": 0,
                                     "time": 0.0, "bad": 0, "install": 0,
                                     "withhold": 0}
                    for fx in fixtures(task, tdir, ext, variant, HARNESS):
                        rc, out, dt = run_bin([binary, task, fx])
                        st = R[label][key]
                        st["n"] += 1
                        st["time"] += dt
                        kv = parse_kv(out)
                        ok = (rc == 0 and "judgment" in kv and "confidence" in kv
                              and "ops" in kv)
                        if label == "G2":
                            ok = ok and all(k in kv for k in
                                            ("disposition", "residual_norm",
                                             "pred_hash", "obs_hash", "residuals",
                                             "ledger"))
                            if "residuals" in kv:
                                ok = ok and len(kv["residuals"].split(",")) == 256
                        if not ok:
                            st["bad"] += 1
                            continue
                        t = truth_of(fx)
                        if kv["judgment"] == t:
                            st["correct"] += 1
                        try:
                            st["ops"] += int(kv["ops"])
                        except ValueError:
                            pass
                        if label == "G2":
                            if kv["disposition"] == "INSTALL":
                                st["install"] += 1
                            else:
                                st["withhold"] += 1
            with open(cache_p, "w") as f:
                _json.dump({lab: {repr(k): v for k, v in d.items()}
                            for lab, d in R.items()}, f)
            print("saved sweeps cache", flush=True)
    # ---------- 3: augmentations ----------
    if not os.path.isdir(AUG) or sum(
            len([f for f in os.listdir(os.path.join(AUG, tdir))
                 if f.endswith(ext)])
            for _, tdir, ext in TASKS) < 240:
        print("running augment.py ...", flush=True)
        subprocess.run([sys.executable,
                        os.path.join(G2DIR, "augment", "augment.py")],
                       check=True)
    aug_n = aug_correct = 0
    aug_install = aug_withhold = 0
    for task, tdir, ext in TASKS:
        d = os.path.join(AUG, tdir)
        for fx in sorted(os.path.join(d, f) for f in os.listdir(d)
                         if f.endswith(ext)):
            rc, out, dt = run_bin([G2BIN, task, fx])
            kv = parse_kv(out)
            if rc != 0 or "judgment" not in kv:
                print("AUG FAIL", fx, rc); sys.exit(1)
            aug_n += 1
            if kv["judgment"] == truth_of(fx):
                aug_correct += 1
            if kv.get("disposition") == "INSTALL":
                aug_install += 1
            else:
                aug_withhold += 1
    assert aug_n == 240, "augmentation count %d != 240" % aug_n
    # ---------- 4: batch manifests (adversarial: 185 harness + 240 aug) --
    adv_lines = []
    for task, tdir, ext in TASKS:
        for fx in fixtures(task, tdir, ext, "adversarial", HARNESS):
            adv_lines.append((task, fx, "harness"))
        d = os.path.join(AUG, tdir)
        for fx in sorted(os.path.join(d, f) for f in os.listdir(d)
                         if f.endswith(ext)):
            adv_lines.append((task, fx, "aug"))
    adv_lines.sort()
    assert len(adv_lines) == 425, "adversarial total %d != 425" % len(adv_lines)
    manifests = {}
    for mode in ("contract", "ablated"):
        mp = os.path.join(SCRATCH, "adv_%s.manifest" % mode)
        with open(mp, "w") as f:
            for task, fx, _ in adv_lines:
                f.write("%s %s %s\n" % (task, fx, mode))
        manifests[mode] = mp
    batch_out = {}
    for mode, mp in manifests.items():
        for rep in range(3):
            p = os.path.join(SCRATCH, "batch_%s_r%d.txt" % (mode, rep))
            # resume: reuse a completed rep file from an interrupted run
            if os.path.exists(p) and open(p, "rb").read().count(b"rec=") >= 425:
                print("  reusing completed %s" % p, flush=True)
                with open(p, "rb") as f:
                    out = f.read()
            else:
                rc, out, dt = run_bin([G2BIN, "batch", mp], timeout=3600)
                assert rc == 0, "batch %s rep %d failed rc=%d" % (mode, rep, rc)
                with open(p, "wb") as f:
                    f.write(out)
            batch_out[(mode, rep)] = out
    # ---------- 5: determinism ----------
    det_single = True
    for task, tdir, ext in TASKS:
        fxs = fixtures(task, tdir, ext, "primary", HARNESS)[:10]
        outs = []
        for fx in fxs:
            o = run_bin([G2BIN, task, fx])[1]
            outs.append(o)
        for fx, o in zip(fxs, outs):
            for _ in range(2):
                if run_bin([G2BIN, task, fx])[1] != o:
                    det_single = False
    det_batch = all(batch_out[(m, 0)] == batch_out[(m, r)]
                    for m in ("contract", "ablated") for r in (1, 2))
    # ---------- 6: independent ledger verification ----------
    def verify_ledger(out):
        recs = []
        cur = {}
        for line in out.decode("utf-8", "replace").splitlines():
            if "=" not in line:
                continue
            k, v = line.split("=", 1)
            cur[k] = v
            if k == "chain":
                recs.append(cur); cur = {}
        h = fnv_str("G2-PRP-1")
        ok = True
        for r in recs:
            tid = TID[r["task"]]
            jc = JCODE[(r["task"], r["judgment"])]
            disp = 1 if r["disposition"] == "INSTALL" else 0
            norm = int(r["residual_norm"])
            ph = int(r["pred_hash"], 16); oh = int(r["obs_hash"], 16)
            rv = [(int(x) & 0xFF) for x in r["residuals"].split(",")]
            assert len(rv) == 256
            rec = bytes([tid & 0xFF, jc & 0xFF, disp & 0xFF,
                         norm & 0xFF, (norm >> 8) & 0xFF])
            rec += ph.to_bytes(8, "little") + oh.to_bytes(8, "little")
            rec += bytes(rv)
            h = fnv_bytes(h, rec)
            if "%016x" % h != r["chain"]:
                ok = False
        summ = parse_kv(out)
        if "%016x" % h != summ.get("ledger_final", ""):
            ok = False
        return ok, len(recs)
    led_ok_c, nrec_c = verify_ledger(batch_out[("contract", 0)])
    led_ok_a, nrec_a = verify_ledger(batch_out[("ablated", 0)])
    # ---------- batch stats ----------
    def batch_stats(out):
        st = {"n": 0, "correct": 0, "install": 0, "false": 0,
              "withhold": 0, "alt": None}
        cur = {}
        for line in out.decode("utf-8", "replace").splitlines():
            if "=" not in line:
                continue
            k, v = line.split("=", 1)
            cur[k] = v
            if k == "chain":
                st["n"] += 1
                if cur["correct"] == "1":
                    st["correct"] += 1
                if cur["disposition"] == "INSTALL":
                    st["install"] += 1
                    if cur["correct"] == "0":
                        st["false"] += 1
                else:
                    st["withhold"] += 1
                cur = {}
        s = parse_kv(out)
        assert int(s["records"]) == st["n"]
        assert int(s["installs"]) == st["install"]
        assert int(s["false_installs"]) == st["false"]
        return st
    bc = batch_stats(batch_out[("contract", 0)])
    ba = batch_stats(batch_out[("ablated", 0)])
    # disposition alteration: contract disp != ablated disp per record
    def disps(out):
        d = []
        cur = {}
        for line in out.decode("utf-8", "replace").splitlines():
            if "=" not in line:
                continue
            k, v = line.split("=", 1)
            cur[k] = v
            if k == "chain":
                d.append((cur["fixture"], cur["disposition"])); cur = {}
        return d
    dc = disps(batch_out[("contract", 0)])
    da = disps(batch_out[("ablated", 0)])
    assert [f for f, _ in dc] == [f for f, _ in da]
    altered = sum(1 for (_, x), (_, y) in zip(dc, da) if x != y)
    altered_rate = altered / len(dc)
    # pok-flag audit: WITHHOLD with norm<24 AND ph==oh can only come from the
    # binary's per-task "prediction available" flag (extra to the frozen
    # two-condition rule); count them.
    def pok_audit(out):
        n = 0
        cur = {}
        for line in out.decode("utf-8", "replace").splitlines():
            if "=" not in line:
                continue
            k, v = line.split("=", 1)
            cur[k] = v
            if k == "chain":
                if (cur["disposition"] == "WITHHOLD"
                        and int(cur["residual_norm"]) < 24
                        and cur["pred_hash"] == cur["obs_hash"]):
                    n += 1
                cur = {}
        return n
    pok_withholds = pok_audit(batch_out[("contract", 0)])
    # ---------- bars ----------
    g2_prim = [R["G2"][(t, "primary")]["correct"] /
               R["G2"][(t, "primary")]["n"] for t, _, _ in TASKS]
    a_prim = [R["A"][(t, "primary")]["correct"] /
              R["A"][(t, "primary")]["n"] for t, _, _ in TASKS]
    b1 = sum(g2_prim) / 6
    fi_rate = bc["false"] / bc["install"] if bc["install"] else 1.0
    integ = sum(R["G2"][(t, v)]["n"] - R["G2"][(t, v)]["bad"]
                for t, _, _ in TASKS for v in VARIANTS)
    integ_tot = sum(R["G2"][(t, v)]["n"]
                    for t, _, _ in TASKS for v in VARIANTS)
    integ_rate = integ / integ_tot
    # ---------- report ----------
    L = []
    L.append("# EVAL_G2.md — PRP fork head-to-head evaluation")
    L.append("")
    L.append("Frozen prereg: `PREREG_G2.md` (commit c242ec0980c3bb1cb84f3014ab11e9b2484ed095).")
    L.append("G2 binary: pure-Zag `src/g2_sense.zag` (no RNG, deterministic).")
    L.append("Approach A binary rebuilt from frozen `senses/rebuild/a_raw/sense.zag`.")
    L.append("")
    L.append("## B1 — G2 primary accuracy (bar: mean >= 60%)")
    L.append("")
    L.append("| task | G2 | A |")
    L.append("|---|---|---|")
    for (t, _, _), g, a in zip(TASKS, g2_prim, a_prim):
        L.append("| %s | %.1f%% | %.1f%% |" % (t, 100 * g, 100 * a))
    L.append("| **mean** | **%.1f%%** | %.1f%% |" % (100 * b1, 100 * sum(a_prim) / 6))
    L.append("")
    L.append("B1: %s (%.1f%% %s 60%%)" %
             ("PASS" if b1 >= 0.60 else "FAIL", 100 * b1,
              ">=" if b1 >= 0.60 else "<"))
    L.append("")
    L.append("## B2 — head-to-head (identical fixtures)")
    L.append("")
    L.append("G2 mean primary %.1f%% vs A mean primary %.1f%% (delta %+.1f pp)." %
             (100 * b1, 100 * sum(a_prim) / 6, 100 * (b1 - sum(a_prim) / 6)))
    L.append("")
    L.append("## B3 — cost")
    L.append("")
    L.append("| task | A mean ops | G2 mean ops |")
    L.append("|---|---|---|")
    for t, _, _ in TASKS:
        ao = R["A"][(t, "primary")]["ops"] / R["A"][(t, "primary")]["n"]
        go = R["G2"][(t, "primary")]["ops"] / R["G2"][(t, "primary")]["n"]
        L.append("| %s | %.0f | %.0f |" % (t, ao, go))
    g2t = sum(R["G2"][(t, "primary")]["time"] for t, _, _ in TASKS)
    g2n = sum(R["G2"][(t, "primary")]["n"] for t, _, _ in TASKS)
    L.append("")
    L.append("G2 mean wall time per primary fixture: %.1f ms." % (1000 * g2t / g2n))
    L.append("Bytes per percept: 256 (residual vector) + 277 (ledger record) = 533.")
    L.append("")
    L.append("## B4 — contract vs always-install ablation (425 adversarial)")
    L.append("")
    L.append("Contract: %d installs, %d withholds, %d false installs." %
             (bc["install"], bc["withhold"], bc["false"]))
    L.append("Ablated: %d installs, %d withholds, %d false installs." %
             (ba["install"], ba["withhold"], ba["false"]))
    L.append("Disposition alteration rate: %.1f%% (%d/%d) (bar: >= 10%%)." %
             (100 * altered_rate, altered, len(dc)))
    L.append("False-install reduction: %d -> %d." % (ba["false"], bc["false"]))
    L.append("B4: %s" % ("PASS" if altered_rate >= 0.10 and
                         bc["false"] < ba["false"] else "FAIL"))
    L.append("")
    L.append("## B5 — adversarial false-install rate (bar: <= 8%% per install)")
    L.append("")
    L.append("Contract false installs: %d / %d installs = %.2f%%." %
             (bc["false"], bc["install"], 100 * fi_rate))
    L.append("B5: %s" % ("PASS" if fi_rate <= 0.08 else "FAIL"))
    L.append("")
    L.append("## B6 — determinism + ledger (bar: 3x byte-identical, independent verify)")
    L.append("")
    L.append("Single-mode 3x byte-identical (60 fixtures): %s." %
             ("PASS" if det_single else "FAIL"))
    L.append("Batch-mode 3x byte-identical (425 records x2 modes): %s." %
             ("PASS" if det_batch else "FAIL"))
    L.append("Independent python FNV-1a-64 ledger verification: contract %s (%d recs), ablated %s (%d recs)." %
             ("PASS" if led_ok_c else "FAIL", nrec_c,
              "PASS" if led_ok_a else "FAIL", nrec_a))
    L.append("B6: %s" % ("PASS" if det_single and det_batch and led_ok_c
                         and led_ok_a else "FAIL"))
    L.append("")
    L.append("## Integration")
    L.append("")
    L.append("Clean single-mode records: %d/%d = %.2f%% (bar: >= 85%%)." %
             (integ, integ_tot, 100 * integ_rate))
    L.append("")
    L.append("pok-flag audit (WITHHOLD with norm<24 and ph==oh, contract mode): %d"
             " (0 = the extra prediction-available flag never changed a"
             " disposition on the eval set)." % pok_withholds)
    L.append("")
    L.append("## Augmentation set")
    L.append("")
    L.append("240 fixtures generated deterministically (splitmix64, seed 20260922);")
    L.append("G2 single-mode accuracy on augmentations: %.1f%% (%d/%d); installs %d, withholds %d." %
             (100 * aug_correct / aug_n, aug_correct, aug_n, aug_install,
              aug_withhold))
    L.append("")
    L.append("## Verdict")
    L.append("")
    bars = {
        "B1 primary>=60%": b1 >= 0.60,
        "B4 contract-matters": altered_rate >= 0.10 and bc["false"] < ba["false"],
        "B5 false-install<=8%": fi_rate <= 0.08,
        "B6 determinism+ledger": det_single and det_batch and led_ok_c and led_ok_a,
        "integration>=85%": integ_rate >= 0.85,
    }
    for k, v in bars.items():
        L.append("- %s: %s" % (k, "PASS" if v else "FAIL"))
    alive = all(bars.values())
    L.append("")
    L.append("**G2 verdict: %s**" % ("ALIVE" if alive else "KILLED"))
    if not alive:
        dead = [k for k, v in bars.items() if not v]
        L.append("Kill reasons: %s." % "; ".join(dead))
    with open(os.path.join(HERE, "EVAL_G2.md"), "w") as f:
        f.write("\n".join(L) + "\n")
    # LEDGER.md: chain summary + independent verification statement
    GL = []
    GL.append("# LEDGER.md — G2 hash-chained ledger (FNV-1a-64)")
    GL.append("")
    GL.append("Genesis L_0 = FNV-1a-64(\"G2-PRP-1\") = %016x." % fnv_str("G2-PRP-1"))
    GL.append("Record encoding (277 bytes): tid u8, judgment code u8, disposition u8,")
    GL.append("norm LE16, pred_hash LE64, obs_hash LE64, 256 signed residual bytes.")
    GL.append("Chain rule: L_n = FNV-1a-64(L_{n-1} || record bytes).")
    GL.append("")
    GL.append("## Batch chains (425 adversarial fixtures)")
    GL.append("")
    GL.append("| mode | records | final chain | independent python verify |")
    GL.append("|---|---|---|---|")
    GL.append("| contract | %d | %s | %s |" %
              (nrec_c, parse_kv(batch_out[("contract", 0)]).get("ledger_final"),
               "PASS" if led_ok_c else "FAIL"))
    GL.append("| ablated | %d | %s | %s |" %
              (nrec_a, parse_kv(batch_out[("ablated", 0)]).get("ledger_final"),
               "PASS" if led_ok_a else "FAIL"))
    GL.append("")
    GL.append("Determinism: batch stdout byte-identical across 3 runs per mode: %s."
              % ("PASS" if det_batch else "FAIL"))
    with open(os.path.join(HERE, "LEDGER.md"), "w") as f:
        f.write("\n".join(GL) + "\n")
    print("\n".join(L))

if __name__ == "__main__":
    main()
