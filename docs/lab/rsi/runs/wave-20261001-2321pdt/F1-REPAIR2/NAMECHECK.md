# NAMECHECK.md - F1-REPAIR2 lane (wave-20261001-2321pdt)

Replacement worker for F1-REPAIR2: confirms relaxed repair signature
S-prime (later to-zero burst, any buffer size) on 24 fresh sealed
sum2 worlds (new seed series), plus a repair-time policy experiment
characterizing what makes a later burst run to zero vs stall.

No em-dashes are used in this document.

## Step 0 (toolchain guard)

Commands run first, before any other work:

```
cd ~/workspace/tnn-rsi && sh docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh && export PATH="$HOME/safebin" && which python3; echo "which-exit=$?"
```

Exact verification output:

```
safebin: /home/hatch/safebin
linked: 36 tools
znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
verify: python3 absent from safebin PATH (OK)
verify: python absent from safebin PATH (OK)
SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
which-exit=1
```

`which python3` printed nothing and exited 1. Guard PASS.
All work is pure Zag (pinned znc) or shell invoking znc, running
binaries, git ops, cmp/sha256sum, grep, and file moves/copies.
Any forbidden executable invocation is automatic PROCESS-FAIL.

## Commits (this lane only)

| commit | content |
|---|---|
| | PREREG_REPAIR2.md frozen alone (Step 0 above) |
| | Implementation: instruments, run scripts (probe built only after prereg commit) |
| | Fresh fixture manifest (7100-series, SHA-256) before any sealed run |
| | Sealed runs: determinism, tables, verdict |
| | JUDGE_BRIEF.md |

## Ordering self-check (to be filled)

- prereg commit precedes first probe build: (pending)
- prereg commit precedes first fresh fixture generation: (pending)
- fixture manifest commit precedes first sealed run: (pending)
