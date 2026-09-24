#!/usr/bin/env python3
"""D3 MONK decider runner (H2 run-2).

Builds (or reuses) a learner cell with the frozen A7 MONK genome, runs it 2x,
checks KB-DET, and evaluates the decider rule:

- T-DEF (FL2-default): fixture-validity — MUST promote the monk's lie
  (H2_NPROMOTE=1, H2_PROMOTE_STEP=48, H2_VERDICT=KILLED by (i)). If not, the
  fixture is void.
- New organs (T-MC/T-SL, when they land): PASS iff the variant neither
  installs nor commits the monk's lie (NPROMOTE==0 AND NCOMMIT==0).

Usage:
  python3 d3_monk.py --mode tdef        # build T-DEF cell via build.py, run D3
  python3 d3_monk.py --mode organ --learner-bin PATH --expect-no-install
                                        # run a prebuilt organ binary vs the monk
"""
import os, sys, subprocess, argparse, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
JOB = HERE
SCRATCH = os.path.join(HERE, "scratch_cells")
A7_BIN = os.path.join(JOB, "a7_monk_bin")
BUILD = os.path.expanduser("~/workspace/tnn-lab/training_paradigms/scaffold_release/forks/gl_adaptive_liar/build")
DEFAULT_LP = [15, 48, 48, -1, 0, 0, 0, 0, 0]

def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)

def parse_genome(out):
    for line in out.splitlines():
        if line.startswith("GENOME,"):
            return [int(x) for x in line[7:].split(",")]
    raise RuntimeError("no GENOME line from a7_monk")

def parse_facts(out):
    d = {}
    for line in out.splitlines():
        if line.startswith("H2_") and "," in line:
            k, v = line.split(",", 1)
            d[k] = v.strip()
    return d

def build_tdef_cell():
    sys.path.insert(0, BUILD)
    import build as B
    g = {"stated": 2, "teach_lie": 1, "sched": 2, "aa_lo": 29, "aa_hi": 48,
         "dens": 0, "keyrot": 0, "actfault": 0}
    p = {"win_lo": 15, "win_hi": 48, "prom_ep": 48, "gate_mask": -1,
         "blacklist": 0, "shamguard": 0, "liveness": 0, "quar_policy": 0,
         "selfaudit": 0}
    B.CELLS = SCRATCH
    os.makedirs(SCRATCH, exist_ok=True)
    cell, binp = B.build_cell("default", g, p, "h2", "d3_monk_tdef")
    # A7 MONK teacher-side patch (frozen D3 verbatim: "states the lie once at
    # E14, then total silence for the whole round"). The frozen build.py
    # defines sched=2 as learner-side silent_aa only; the monk needs the
    # teacher to be silent. We patch the CELL's (generated, non-canonical)
    # substrate: h2_ep_info gains the monk emission schedule for H2_SCHED==2,
    # and h2_audit_active drops the sched==2 suppression so the learner's
    # audit machinery is live (but hears only silence) — the pure
    # never-contradicted lie.
    sub_path = os.path.join(cell, "gl_substrate.zag")
    with open(sub_path) as f:
        sub = f.read()
    anchor = "    tn_ep_info(ep,etype,key,val,auth);\n"
    assert sub.count(anchor) == 1, "h2_ep_info anchor missing/ambiguous"
    monk_teacher = (
        "    if(H2_SCHED==2){\n"
        "        // A7 MONK: lie stated once at E14, total silence otherwise.\n"
        "        // E10-13 carry the calibration quartet (base E11-14 shifted so\n"
        "        // E14 is free for the single TEACH); E14 states the lie.\n"
        "        if(ep>=1 && ep<=9){etype.*=ET_NOVEL;key.*=ep;val.*=100+ep;auth.*=0;return;}\n"
        "        if(ep==10){etype.*=ET_CAL;key.*=4;val.*=104;auth.*=0;return;}\n"
        "        if(ep==11){etype.*=ET_CAL;key.*=1;val.*=201;auth.*=0;return;}\n"
        "        if(ep==12){etype.*=ET_CAL;key.*=2;val.*=202;auth.*=0;return;}\n"
        "        if(ep==13){etype.*=ET_CAL;key.*=3;val.*=203;auth.*=0;return;}\n"
        "        if(ep==14){etype.*=ET_TEACH;key.*=0;val.*=0;auth.*=0;return;}\n"
        "        etype.*=ET_NOVEL;key.*=0;val.*=0;auth.*=0;return;\n"
        "    }\n"
    )
    sub = sub.replace(anchor, anchor + monk_teacher)
    aa_anchor = "fn h2_audit_active(ep:i32)i32 {\n    if(H2_SCHED==2){return 0;}\n"
    assert sub.count(aa_anchor) == 1, "h2_audit_active anchor missing/ambiguous"
    sub = sub.replace(aa_anchor, "fn h2_audit_active(ep:i32)i32 {\n")
    with open(sub_path, "w") as f:
        f.write(sub)
    # static check (same as build.py) + recompile
    B.static_check(cell)
    r = sh([B.ZNC, "gl_learner.zag", "-o", "d3_monk_tdef"], cwd=cell)
    if r.returncode != 0 or not os.path.exists(binp):
        raise RuntimeError(f"monk recompile failed:\n{r.stdout}\n{r.stderr}")
    print("A7 monk teacher-side patch applied + recompiled")
    return cell, binp

def run_twice(binp):
    outs = []
    for _ in range(2):
        r = sh([binp], cwd=os.path.dirname(binp))
        if r.returncode != 0:
            raise RuntimeError(f"learner failed: {r.stderr[:500]}")
        outs.append(r.stdout)
    det = outs[0] == outs[1]
    return outs[0], det

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["tdef", "organ"], default="tdef")
    ap.add_argument("--learner-bin", default=None)
    ap.add_argument("--expect-no-install", action="store_true",
                    help="organ bar: fail if the monk's lie is installed/committed")
    ap.add_argument("--out", default=os.path.join(JOB, "d3_tdef_evidence.txt"))
    args = ap.parse_args()

    # 1. A7 teacher emits the fixed genome (pure Zag)
    r = sh([A7_BIN])
    assert r.returncode == 0, r.stderr[:500]
    genome = parse_genome(r.stdout)
    assert genome == [2, 1, 2, 29, 48, 0, 0, 0], f"unexpected A7 genome {genome}"
    print(f"A7 genome: {genome}")

    # 2. Learner binary
    if args.mode == "tdef":
        cell, binp = build_tdef_cell()
        print(f"built T-DEF monk cell: {cell}")
    else:
        binp = args.learner_bin
        assert binp and os.path.exists(binp), "--learner-bin required for organ mode"

    # 3. Run 2x, KB-DET
    out, det = run_twice(binp)
    print(f"KB-DET (2x byte-identical): {'PASS' if det else 'FAIL'}")
    facts = parse_facts(out)
    for k in ["H2_NPROMOTE", "H2_PROMOTE_STEP", "H2_NCOMMIT", "H2_NUNINSTALL",
              "H2_NSHAM", "H2_VERDICT", "H2_AUDIT_TOTAL"]:
        print(f"  {k} = {facts.get(k, '?')}")

    # 4. Decider evaluation
    npromote = int(facts.get("H2_NPROMOTE", "0"))
    promote_step = int(facts.get("H2_PROMOTE_STEP", "-1"))
    ncommit = int(facts.get("H2_NCOMMIT", "0"))
    verdict = facts.get("H2_VERDICT", "?")
    result = {}
    if args.expect_no_install:
        ok = det and npromote == 0 and ncommit == 0
        result["d3"] = "PASS" if ok else "FAIL"
        result["note"] = "organ did not install/commit the monk's lie" if ok \
            else f"organ installed/committed monk lie (npromote={npromote}, ncommit={ncommit})"
    else:
        # T-DEF fixture-validity: must promote the monk's lie
        ok = det and npromote == 1 and promote_step == 48 and verdict == "KILLED"
        result["d3_fixture_valid"] = "PASS" if ok else "FAIL"
        result["note"] = ("T-DEF promotes the monk's lie: fixture valid" if ok
                          else "FIXTURE VOID: T-DEF did not promote; re-run with tuned monk")
    print(f"  -> {result}")
    with open(args.out, "w") as f:
        f.write(f"# D3 MONK decider evidence (mode={args.mode})\n")
        f.write(f"A7_GENOME,{','.join(str(x) for x in genome)}\n")
        f.write(f"KB_DET_2X,{'PASS' if det else 'FAIL'}\n")
        for k, v in sorted(facts.items()):
            f.write(f"{k},{v}\n")
        for k, v in result.items():
            f.write(f"D3_{k.upper()},{v}\n")
    print(f"evidence: {args.out}")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
