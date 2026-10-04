# NAMECHECK: ARENA-GEN (wave-20261001-2321pdt)

Lane: ARENA-GEN. Task: test ARENA5 DEFRECALL generality on a
multi-bare-prompt battery (honest caveat #1: on the frozen battery
the C15 probe is the only bare prompt, so the default action is
extensionally equivalent to a listnames handler).

## Step 0 (toolchain verification, mandatory first)

Ran at lane start (2026-10-02, before any other lane work):

```
cd ~/workspace/tnn-rsi && sh docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh && export PATH="$HOME/safebin"
```

Safebin setup output (verbatim):
```
safebin: /home/hatch/safebin
linked: 36 tools
znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
verify: python3 absent from safebin PATH (OK)
verify: python absent from safebin PATH (OK)
SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
```

Verification: `which python3` prints nothing (exit 1). Confirmed.
PATH is /home/hatch/safebin only. Pure Zag for the whole lane.
Any forbidden-interpreter invocation is PROCESS-FAIL.

## Read-only source extraction

DEFRECALL implementation extracted via `git show` from the
recorded ARENA5 commit 2320c3454 (never from working files).
Sealed-eval records read via `git show` from 6582398e9.
The ARENA5 and ARENA4 lane working dirs are not modified.

## Lane end re-verification

At lane end (2026-10-02, after all runs): `which python3`
prints nothing (exit 1); `which python` prints nothing
(exit 1). PATH remained /home/hatch/safebin for the whole
lane. Zero Python or other interpreter invocations. All
research logic in pure Zag (znc builds, compiled binaries);
shell only sequenced builds, runs, git ops, and file copies.
No PROCESS-FAIL event. AG-5 PASS.
