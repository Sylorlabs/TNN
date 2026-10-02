# NAMECHECK: H-PI-REV2 step-5 re-execution under amended prereg (wave-20261001-2021pdt)

Lane: docs/lab/rsi/runs/wave-20261001-2021pdt/HPIREV2/
Task: re-execute H-PI-REV2 step-5 under the amended prereg frozen at
commit 72168c608. Run the amended bars (K-SB1/2/3/4a/4b/4c/5/6),
15-run matrix, 3/3 byte-identical determinism. No bar movement.
The original BASELINE-FAIL verdict is not relitigated.

## Step 0: worker toolchain guard (mandatory, before any other work)

- Ran docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh;
  output: SAFEBIN-READY (/home/hatch/safebin, 36 tools, no python).
- Exported PATH="$HOME/safebin" in every exec session (PATH does not
  persist across fresh-shell exec calls in this runtime, so the export
  was re-issued per command; no command ran without it).
- `which python3` with PATH=$HOME/safebin: prints NOTHING, exit code 1.
  Confirmed absent. (Without the safebin PATH export the system
  /usr/bin/python3 is visible, which is exactly why the safebin PATH
  is used for every command.)
- `which python`: prints NOTHING, exit code 1. Confirmed absent.
- znc resolves to /home/hatch/safebin/znc
  (pinned znc_linux_x86_64_abed8aa1).
- All work in this lane uses shell with safebin tools only
  (bash, awk, cat, cmp, cp, cut, date, diff, git, grep, head,
  mkdir, sha256sum, stat, tail, tee, timeout, touch, tr, uniq, wc,
  znc, which). No python3, python, gcc, or cc invoked at any stage.
  Any forbidden-executable invocation would make this wave
  PROCESS-FAIL; none occurred.

## Commit-order self-check (prereg before execution)

- Amended prereg file:
  docs/lab/rsi/runs/wave-20261001-1721pdt/HPIREV2/PREREG_PI_REV2_STEP5_BASELINE_AMENDED.md
- `git log` for that file shows exactly one commit:
  72168c60803b95b3b586eb1cf6f1fc9bd001b174 (2026-10-02).
- This matches the frozen amendment commit named in the task.
- No implementation work in this lane predates it: the lane dir
  docs/lab/rsi/runs/wave-20261001-2021pdt/HPIREV2/ was empty at lane
  start (created by the coordinator). All baseline sources and runs
  are created in this wave, after the freeze.
- Result: commit-order self-check PASS.

## Frozen code binding

- Mechanism under test: docs/lab/rsi/runs/wave-20260929-2321pdt/pi_rev2/proc_revise2.zag
- Working-tree sha256: dd3cb02dbd883243e350a89e328e570c35e2dc7a71f49f4e3aa51f0603a99a12
- Matches committed blob at 847a8f10f (git cat-file verified).
- Adversary byte 'r' per ADVERSARY_BYTE_SET4.md (set {k,m,r}, last
  letter sorted). Disjoint from all frozen fixture inputs by the
  frozen audit.

## Working copy state

- Working copy: /home/hatch/workspace/tnn-rsi, branch tnn-native-lab.
- No git commits made by this worker. No push. No reset. No rebase.
  All lane files remain uncommitted; the coordinator commits at wave
  end. No files written outside this lane dir.

## Toolchain notes

- znc quirk: no `as *i32` plus slice construction used anywhere in new
  Zag code (the B1T main reuses the existing safe idioms from the
  frozen shared code).
- znc A0102 lint text contains a compiler-emitted em-dash; raw build
  logs are kept in /tmp with sha256 hashes recorded in EXECUTION_LOG.md,
  exactly as the original step-5 lane did, to keep the lane byte-clean
  for K-SB6.
