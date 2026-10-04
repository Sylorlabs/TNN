# NAMECHECK: wave-20261001-1421pdt sealed adversarial battery (sealed_adv)

Worker: sealed adversarial battery on the three new TNN-2 mechanisms (M1 runtime
executable-graph construction; M2 learner-originated uncertainty guiding action;
M3 counterexample-driven revision).

## Step 0: Worker toolchain guard (MANDATORY FIRST STEP, completed before any research work)

- Ran: `bash ~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
  - Output: `safebin: /home/hatch/safebin`, `linked: 36 tools`, `znc: OK
    (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)`,
    `verify: python3 absent from safebin PATH (OK)`, `verify: python absent from
    safebin PATH (OK)`, `SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)`.
- Ran: `export PATH="$HOME/safebin"`.
- Verified: `which python3` prints nothing (exit code 1); `which python` prints
  nothing (exit code 1). `which znc` resolves to `/home/hatch/safebin/znc`.
- Guard status: PASS. All programs in this battery are Zag compiled with the
  pinned znc; zero Python anywhere (no glue, analysis, verifiers, harnesses).
  All shell work uses safebin tools only (coreutils, git, sha256sum, etc.).

## Step 1: Working copy state

- Working copy: ~/workspace/tnn-rsi, branch tnn-native-lab (verified with
  `git branch --show-current`).
- No git commit, push, checkout, or branch change performed by this worker;
  all files remain uncommitted (task instruction).

## Step 2: Mechanism source freeze (SHAs recorded here before any evaluation)

To be filled in Step 2 of the battery protocol (see SEALED_BATTERY_PREREG.md).
