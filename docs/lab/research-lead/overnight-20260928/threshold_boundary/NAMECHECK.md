# Step 0: Standing-Rules Name-Check

Worker: Threshold Boundary-Mapping Red Team (follow-up).
Date: 2026-09-30.

Standing rules read at the top of LOOP_STATE.md (the four sections:
Standing owner rules; Standing owner rule: fork testing; Standing
ruling: pure-Zag red line scope; Standing rule: shell-only byte
checks).

Rules applying to this task and how they are honored:

1. PURE ZAG ONLY (owner red line, literal): every artifact of this
attack is pure Zag: the attack implementation, the sealed-world
definitions, the drivers, the build, the runs, and all analysis.
No Python is authored or executed anywhere, including for byte
checks. This is an attacker brief: I copy the frozen mechanism
verbatim and never modify sealed or frozen files.

2. Pure-Zag red-line scope: fixture provisioning counts as loop
work, so my frozen evidence tables and sealed family definitions
are Zag-only (hardcoded tables plus runtime sealed() self-checks).

3. Shell-only byte checks: dash checks use only
docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh.
No python3 for byte checks.

4. Image judge: not applicable. No image work in this task.

5. Fork testing: not applicable to this specific attack task. I
attack one frozen committed mechanism (d0d296650); I do not test
forks.

Name-check complete. Proceeding to Step 1.
