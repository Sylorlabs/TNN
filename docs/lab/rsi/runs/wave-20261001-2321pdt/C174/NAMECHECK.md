# NAMECHECK.md - Lane C174 (wave-20261001-2321pdt)

## Step 0 (mandatory toolchain guard)

- Command: `cd ~/workspace/tnn-rsi && sh docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh && export PATH="$HOME/safebin"`
- safebin output: `safebin: /home/hatch/safebin` / `linked: 36 tools` / `znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)` / `verify: python3 absent from safebin PATH (OK)` / `verify: python absent from safebin PATH (OK)` / `SAFETY-READY: /home/hatch/safebin (36 tools, no python)`
- Verification: `which python3` printed NOTHING (empty stdout), exit code 1 (not found).
- PATH for this lane: `$HOME/safebin` only. Pure Zag only. Shell may invoke znc, run binaries, git ops, move/copy files.
- Forbidden-interpreter invocation = PROCESS-FAIL per governance.

## Progress log

- 2026-10-01 wave-20261001-2321pdt: Step 0 done (above). Spec chain
  read: SHARED_SUBSTRATE.md (550fa268b, 619 lines), ledger
  C174/C175/C180/C181/C182/C183, CONSEQ JUDGE_BRIEF.md
  (VALIDATION-PASS), Node2-v2 frozen prereg 4b05c8011 sections
  2.4 and 7 (migration-compat note), TNN3-SUBSTRATE lane scope
  checked (learner construction / contradiction trigger /
  learner standing are theirs; tag-61 store plus
  consequence-derived utility is this lane's).
- PREREG_C174.md frozen (this commit, prereg alone). Kill bars
  a-e fixed; seal procedure committed; no implementation yet.
- Implementation written and smoke-tested (selftest SELFTEST_OK,
  generator produces deterministic worlds). No tuning after seeing
  the generated world: constants and seeds stand as frozen.
