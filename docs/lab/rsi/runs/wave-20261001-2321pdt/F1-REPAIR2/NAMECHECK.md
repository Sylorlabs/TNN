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
| b4dfa3f32 | PREREG_REPAIR2.md frozen alone (+ NAMECHECK.md Step 0, + dev/CALIBRATION_5100_6100_POLICY.md training calibration) |
| | Implementation: r2sig/r2apply (pure-Zag probe + applier), run scripts, read-only tool copies |
| | Fresh fixture manifest (7300-series, SHA-256) before any sealed run |
| | Sealed runs: determinism, tables, verdict |
| | JUDGE_BRIEF.md |

## Ordering self-check

- prereg commit (b4dfa3f32) precedes first probe build: YES (r2sig/r2apply compiled after b4dfa3f32)
- prereg commit precedes first fresh fixture generation: YES (gen5.sh runs after; enforced by script order)
- fixture manifest commit precedes first sealed run: YES (run_repair2.sh verifies FIXTURE_SHA256.txt before running)
- pre-prereg work was read-only only: YES (grep/awk inspection of committed traces; git show extraction of committed tool binaries; no probe built, no fresh fixture, no fresh run before b4dfa3f32)

## Validation (post-prereg, pre-sealed)

- r2sig on 20 calibration traces (9x 5100, 11x 6100): deg/Sprime/polok reproduce the frozen calibration tables exactly
  (5100 Sprime=1: seeds 0, 6, 12; 6100 Sprime=1: seeds 10, 12, 15, 17, 20; polok=1 on all 20)
- r2apply on synthetic tables: PASS/FAIL/INDETERMINATE paths verified
- K-C0A audit over new lane code: 0 hits on all three marker classes (PASS)
- Frozen binary sha256 verified: 6f2b155b233a95ad1a8323e8565b9a798dc822db6eff57e065b71b5be8882847
