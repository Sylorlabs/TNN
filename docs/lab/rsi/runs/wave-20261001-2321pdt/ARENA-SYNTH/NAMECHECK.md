# NAMECHECK: ARENA-SYNTH (wave-20261001-2321pdt)

Lane: ARENA-SYNTH (replacement synthesis worker). Synthesis lane only:
no experiments, no Python, shell for git/file ops. READ-ONLY toward
ARENA5, ARENA-GEN, ARENA-GEN-VERIFY, and RT-ARENA5 lane dirs.

## Step 0 (worker toolchain guard)

`safebin: /home/hatch/safebin`
`linked: 36 tools`
`znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)`
`verify: python3 absent from safebin PATH (OK)`
`verify: python absent from safebin PATH (OK)`
`SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)`

Direct checks: `which python3` prints nothing (exit=1);
`which python` prints nothing (exit=1).
