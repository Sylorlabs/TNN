# NAMECHECK.md: wave-20261001-0821pdt coordinator

Lane: wave-20261001-0821pdt coordinator. Role: coordinator for this wave.

## Step 0: Safebin / toolchain verification (mandatory first step)

Commands run at startup (before any other work):

1. `bash ~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
   Output: `SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)`;
   linked 36 tools; znc OK (pinned repo binary).
2. `export PATH="$HOME/safebin"` in every shell session.
3. `which python3` in safebin PATH: nothing (exit 1).
4. `command -v python`: nothing (exit 1).

SAFEBIN ACTIVE: python3/python do not resolve in this PATH.

## Step 1: forbidden-executable audit

No python3/python invocations made this wave by this coordinator.
Shell used only to invoke znc, run binaries, git operations, move/copy
files. All research computation in pure Zag. If a forbidden executable
is invoked, the affected lane is PROCESS-FAIL.

## Wave lock

Wave lock ~/workspace/tnn-rsi/.wave_lock is managed by the parent
agent (it removes the lock at wave end). This coordinator never touches it.

No em-dashes in this documentation.
