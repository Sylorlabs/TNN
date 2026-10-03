# NAMECHECK: adv_battery prereg wave wave-20261001-0821pdt

Lane: adv-battery-prereg. Worker: TNN RSI loop worker (subagent, depth 2).
Scope: prereg text only. No execution, no commits by this worker.

## Step 0: Toolchain guard activation (owner governance, mandatory)

Commands run before any other work, in this order:

```
$ bash ~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
safebin: /home/hatch/safebin
linked: 36 tools
znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
verify: python3 absent from safebin PATH (OK)
verify: python absent from safebin PATH (OK)
SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
$ export PATH="$HOME/safebin"
$ which python3        -> no output, exit 1 (absent)
$ command -v python   -> no output, exit 1 (absent)
$ command -v python3  -> no output, exit 1 (absent)
```

Result: PATH=/home/hatch/safebin only. python3 and python do not resolve.
PURE ZAG ONLY for this wave: no Python in glue, analysis, verifiers, or
harnesses. Shell only: file writes, git reads, grep, the dash check script.

Zag idiom noted: never use `as *i32` + `q[0..n]` slice construction inside
functions (pinned znc miscompiles it); use u8-backed cells with
little-endian get32/set32 helpers. No Zag code is written in this wave
(prereg text only), so the idiom rule has no live application here; it is
recorded for the downstream sealing and execution waves.

## Step 1: Forbidden-executable audit

Updated at wave end. This wave: prereg text only. Executables invoked:
sh (dash check script), bash (safebin setup), coreutils (ls, cat, grep,
head, mkdir, printf), git (log, branch, status reads only). No python,
python3, or other interpreters were invoked at any point. Final status:
AUDIT-CLEAN.

## Steps 2-5: not applicable (no build, no execution, no commits in this wave)

The coordinator commits the prereg freeze. This worker commits nothing.
