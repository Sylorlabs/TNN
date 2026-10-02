# NAMECHECK: lane TNN3H5, wave-20261001-2021pdt

Hypothesis under test: H5, generic supersession transition on the cognition path
(backlog accepted wave-20261001-1721pdt, ranked first by information gain,
underpins H6/H7/H9/H11).

## Step 0: worker toolchain guard (mandatory, recorded at startup)

1. Ran: `bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
   Result: SAFEBIN-READY, /home/hatch/safebin, 36 tools, znc OK
   (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1),
   verify: python3 absent from safebin PATH (OK), python absent (OK).
2. `export PATH="$HOME/safebin"`; then `which python3` printed NOTHING
   (exit 1). Guard satisfied: no python3 resolves in the worker PATH.
3. PURE ZAG ONLY for this lane: no Python for glue, analysis, verifiers,
   harnesses, or fixture provisioning. Shell invokes only pinned znc, runs
   binaries, git ops, file moves/copies. Any forbidden executable invocation
   is automatic PROCESS-FAIL and will be reported honestly.
4. Working copy: /home/hatch/workspace/tnn-rsi, branch tnn-native-lab.
   No push (never). No git reset --hard, no rebase. No commits by this worker;
   coordinator commits at wave end. Writes only inside
   docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H5/.
5. Documentation rule observed: no em-dashes in anything written in this lane.
6. Determinism standard: 3/3 byte-identical reruns, zero randomness in
   decision paths.

Recorded: 2026-10-01 20:25 PDT, worker session d411cf56 (subagent lane TNN3H5).
