# NAMECHECK.md - Lane F1, wave wave-20261002-0221pdt

Worker: F1 lane (repair-time policy + probe-menu adversarial attack).
Task parts: (A) design and sealed-test a repair-time policy for the F1
mechanism addressing the interleaved-error trigger gap; (B) probe-menu
equivalence red-team attack per Criterion 0 C0-B.

## Step 0 (toolchain guard, recorded before any other work)

- Ran `bash
  docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
  from ~/workspace/tnn-rsi. Output: `safebin: /home/hatch/safebin`,
  `linked: 36 tools`, `znc: OK`, `verify: python3 absent from safebin
  PATH (OK)`, `verify: python absent from safebin PATH (OK)`,
  `SAFEBIN-READY`.
- `export PATH="$HOME/safebin"` set in every shell used by this worker.
- `which python3` returns nothing (exit 1). `which python` likewise
  returns nothing (verified by the setup script).
- `which znc` resolves to `/home/hatch/safebin/znc` (the pinned
  toolchain).
- Pure Zag only: no Python anywhere (glue, analysis, verifiers,
  harnesses, byte checks). Shell only invokes znc, runs compiled
  binaries, performs git ops, cmp/sha256sum, grep, and file
  moves/copies. Any forbidden-executable invocation is automatic
  PROCESS-FAIL and will be disclosed immediately.
- Dash rule: zero em/en dashes in loop docs; scans only via
  `docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh`.

Step 0 recorded 2026-10-02 ~02:30 PDT, before any lane file was written.

## Lane scope and non-duplication

- This lane does not re-freeze the 2321pdt windowed failure-density
  trigger (PREREG_TRIG.md, verdict BUILD-FAIL on K-C0C-REG via
  pre-existing constructor overfit on fresh seed 2301, proven identical
  on the old binary). The structural difference in this lane is a
  non-forgetting cumulative failure-evidence repair trigger (POLICY-C),
  which addresses the remaining interleaved-error trigger gap the
  windowed trigger provably misses: sparse interleaving below the
  2-in-8 window density never fires the windowed trigger.
- The 2321pdt F1-REPAIR2 verdict REPAIR2-CONFIRMED (POLICY-R repair-burst
  characterization) stands; this lane does not alter it.
- F1 v4 BUILD-FAIL (wave-20261001-2021pdt, RT-EXEC EVIDENCE-HOLDS)
  stands on its frozen rule.

## Git discipline for this lane

- Write only under
  `docs/lab/rsi/runs/wave-20261002-0221pdt/F1/`.
- `PREREG_F1_REPAIR.md` is committed ALONE (no implementation files,
  no fixtures, no tools in that commit).
- Later commits use explicit pathspecs under this lane dir only.
- Never `git add -A`, never commit outside the lane, never push
  (local only). Retry on ref-lock failure. Never `git reset --hard`,
  never rebase.
