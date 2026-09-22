#!/usr/bin/env python3
"""LH| long-horizon trial driver — decision-free harness.

Orchestrates the TNN-native deliberation (proposer/critic/composer via lh_delib)
and the generate->compile->run->test loop (via lh_emit + znc) across 26
dependency-ordered stages plus a fatigue probe.

The driver makes NO design decisions. It:
- calls lh_delib propose/critique/compose (TNN-native invention),
- calls lh_emit gen (mechanical translation),
- compiles with znc, runs the binary, compares to contract tests,
- appends all episodes to the shared ledger,
- records per-cycle metrics.

Usage: lh_driver.py <workdir>
Workdir contains: contracts/, lh_kb.txt, lh_delib, lh_emit binaries.
Outputs: ledger.txt, metrics.jsonl, results/.
"""
import subprocess, os, sys, json, time, hashlib

ZNC = os.path.expanduser("~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1")

def discover_stages(contracts_dir):
    """Discover stages from contracts/*.txt. Returns sorted [(stage, contract_path)]."""
    stages = []
    for fname in os.listdir(contracts_dir):
        if fname.endswith(".txt"):
            stage = fname[:-4]
            path = os.path.join(contracts_dir, fname)
            with open(path) as f:
                content = f.read()
            # Verify STAGE line matches filename
            for line in content.split("\n"):
                if line.startswith("STAGE "):
                    sid = line[6:].strip()
                    if sid == stage:
                        stages.append((stage, path))
                    break
    # Sort naturally by leading letter then number
    def key(s):
        letter = s[0]
        num = int(s[1:])
        return (letter, num)
    stages.sort(key=lambda x: key(x[0]))
    return stages

def run(cmd, **kw):
    """Run command, return (rc, stdout, stderr). No shell."""
    p = subprocess.run(cmd, capture_output=True, text=True, **kw)
    return p.returncode, p.stdout, p.stderr

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def main():
    workdir = sys.argv[1]
    contracts_dir = os.path.join(workdir, "contracts")
    kb_path = os.path.join(workdir, "lh_kb.txt")
    delib_bin = os.path.join(workdir, "lh_delib")
    emit_bin = os.path.join(workdir, "lh_emit")

    with open(kb_path) as f:
        kb_text = f.read()
    kb_sha = sha256_file(kb_path)

    ledger_path = os.path.join(workdir, "ledger.txt")
    metrics_path = os.path.join(workdir, "metrics.jsonl")
    results_dir = os.path.join(workdir, "results")
    os.makedirs(results_dir, exist_ok=True)

    ledger = open(ledger_path, "w")
    metrics = open(metrics_path, "w")

    # Ledger header
    ledger.write(f"LEDGER LH| trial start\n")
    ledger.write(f"KB-SHA {kb_sha}\n")
    ledger.write(f"KB-ENTRIES 6\n")  # LH-REC, LH-CMP, LH-CAP|x4
    ledger.flush()

    cycle_num = 0
    stage_results = {}

    def log_metric(**kw):
        kw["cycle"] = cycle_num
        kw["t"] = time.time()
        metrics.write(json.dumps(kw) + "\n")
        metrics.flush()

    def ledger_append(text):
        ledger.write(text)
        if not text.endswith("\n"):
            ledger.write("\n")
        ledger.flush()

    stages = discover_stages(contracts_dir)
    ledger.write(f"STAGES-DISCOVERED {len(stages)}\n")

    for stage, contract_path in stages:
        stage_start = time.time()
        with open(contract_path) as f:
            contract_text = f.read()

        ledger_append(f"\n=== STAGE {stage} ===")
        log_metric(event="stage_start", stage=stage)

        # --- Deliberation: propose ---
        cycle_num += 1
        rc, prop_out, _ = run([delib_bin, "propose", stage, contract_text, kb_text])
        ledger_append(prop_out.strip())
        log_metric(event="propose", stage=stage, rc=rc)

        # Check for HALT (honest halt: KB-MISS or PARAM-MISS)
        if "HALT" in prop_out and "CAND" not in prop_out:
            # Honest halt — proposer could not map DESC to taught capabilities.
            # This is the expected outcome for underivable tasks (fatigue probe).
            halt_kind = "KB-MISS" if "KB-MISS" in prop_out else "PARAM-MISS"
            ledger_append(f"HALT {stage} {halt_kind} (honest)")
            log_metric(event="halt", stage=stage, kind=halt_kind, defect=0)
            stage_results[stage] = {"status": f"halt_{halt_kind}", "cycles": 1}
            continue

        # Extract candidates
        cands = [l for l in prop_out.split("\n") if l.startswith("CAND ")]
        if not cands:
            ledger_append(f"NO-CANDIDATES {stage}")
            log_metric(event="no_candidates", stage=stage, defect=1)
            stage_results[stage] = {"status": "no_candidates", "cycles": 1}
            continue

        # --- Deliberation: critique ---
        cycle_num += 1
        cands_text = "\n".join(cands)
        rc, crit_out, _ = run([delib_bin, "critique", stage, contract_text, cands_text])
        ledger_append(crit_out.strip())
        log_metric(event="critique", stage=stage, rc=rc)

        accept_line = [l for l in crit_out.split("\n") if l.startswith("ACCEPT ")]
        if not accept_line:
            ledger_append(f"NO-ACCEPT {stage}")
            log_metric(event="no_accept", stage=stage, defect=1)
            stage_results[stage] = {"status": "no_accept", "cycles": 2}
            continue

        spec = accept_line[0].split(" ", 2)[2]
        crit_ep = f"{stage}-C1"  # from critic output

        # --- Deliberation: compose ---
        cycle_num += 1
        rc, comp_out, _ = run([delib_bin, "compose", stage, spec, crit_ep])
        ledger_append(comp_out.strip())
        log_metric(event="compose", stage=stage, rc=rc)

        final_spec = [l for l in comp_out.split("\n") if l.startswith("FINAL ")][0][6:]

        # --- Generate ---
        cycle_num += 1
        rc, gen_out, _ = run([emit_bin, "gen", final_spec])
        log_metric(event="gen", stage=stage, rc=rc, spec_sha=hashlib.sha256(final_spec.encode()).hexdigest()[:16])

        if gen_out.startswith("UNKNOWN_GOAL") or gen_out.startswith("UNTAUGHT"):
            ledger_append(f"GEN-FAIL {stage}: {gen_out.strip()}")
            log_metric(event="gen_fail", stage=stage, defect=1)
            stage_results[stage] = {"status": "gen_fail", "cycles": 4}
            continue

        src_path = os.path.join(results_dir, f"{stage}.zag")
        with open(src_path, "w") as f:
            f.write(gen_out)
        src_sha = sha256_file(src_path)

        # --- Compile ---
        cycle_num += 1
        bin_path = os.path.join(results_dir, f"{stage}_bin")
        rc, _, cerr = run([ZNC, src_path, "-o", bin_path, "--no-analyze", "--no-zagd"])
        log_metric(event="compile", stage=stage, rc=rc, src_sha=src_sha[:16])
        if rc != 0:
            ledger_append(f"COMPILE-FAIL {stage}: {cerr[:200]}")
            log_metric(event="compile_fail", stage=stage, defect=1)
            stage_results[stage] = {"status": "compile_fail", "cycles": 5}
            continue
        bin_sha = sha256_file(bin_path)

        # --- Run + Test (all contract tests) ---
        # Parse tests from contract
        tests = []
        for line in contract_text.split("\n"):
            if line.startswith("TEST "):
                # extract in="..." out="..."
                import re
                m = re.match(r'TEST in="(.*)" out="(.*)"', line)
                if m:
                    tests.append((m.group(1), m.group(2)))

        all_pass = True
        for ti, (tin, tout) in enumerate(tests):
            cycle_num += 1
            # Prepare args: for AGG/SORT, split on ; and pass count + records
            if "|AGG|" in final_spec or "|SORT|" in final_spec:
                records = tin.split(";")
                cmd = [bin_path, str(len(records))] + records
            else:
                cmd = [bin_path, tin]
            rc, rout, _ = run(cmd)
            # Normalize: strip trailing newline, for multi-line join with ;
            rout_norm = rout.strip().replace("\n", ";")
            passed = (rout_norm == tout)
            log_metric(event="test", stage=stage, test_idx=ti, passed=int(passed),
                      defect=int(not passed))
            if not passed:
                ledger_append(f"TEST-FAIL {stage}[{ti}]: got=[{rout_norm}] want=[{tout}]")
                all_pass = False

        if all_pass:
            first_working_time = time.time() - stage_start
            ledger_append(f"ACCEPTED {stage} spec_sha={hashlib.sha256(final_spec.encode()).hexdigest()[:16]} bin_sha={bin_sha[:16]}")
            log_metric(event="stage_accept", stage=stage, first_working_s=first_working_time,
                      n_tests=len(tests))
            stage_results[stage] = {"status": "pass", "cycles": cycle_num,
                                   "first_working_s": first_working_time,
                                   "spec": final_spec, "bin_sha": bin_sha}
        else:
            ledger_append(f"STAGE-FAIL {stage}")
            stage_results[stage] = {"status": "test_fail", "cycles": cycle_num}

        # --- Verification cycles (2 extra runs for determinism data) ---
        for vc in range(2):
            cycle_num += 1
            # Re-run first test
            tin, tout = tests[0]
            if "|AGG|" in final_spec or "|SORT|" in final_spec:
                records = tin.split(";")
                cmd = [bin_path, str(len(records))] + records
            else:
                cmd = [bin_path, tin]
            rc, rout, _ = run(cmd)
            rout_norm = rout.strip().replace("\n", ";")
            passed = (rout_norm == tout)
            log_metric(event="verify", stage=stage, verify_idx=vc, passed=int(passed),
                      defect=int(not passed))

    ledger.write(f"\nLEDGER END cycles={cycle_num}\n")
    ledger.close()
    metrics.close()

    # Summary
    print(f"Cycles: {cycle_num}")
    print(f"Stages: {len(stage_results)}")
    for s, r in stage_results.items():
        print(f"  {s}: {r['status']}")

if __name__ == "__main__":
    main()
