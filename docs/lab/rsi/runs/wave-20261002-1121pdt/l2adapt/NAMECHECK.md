# NAMECHECK.md - lane l2adapt, wave-20261002-1121pdt

Lane: L2ADAPT (L2 Adaptive Reuse). Wave: wave-20261002-1121pdt.
Branch: lane-l2adapt-20261002-1121pdt, worktree ~/workspace/tnn-rsi-work/wave-20261002-1121pdt/l2adapt/.
Queue item 2, TOP PRIORITY: L2 adaptive reuse (extend/truncate/specialize/substitute ops,
cross-domain adaptation, ADAPT-REVISION interface-adaptation follow-ups).

## Step 0: toolchain guard (2026-10-02, 12:09 PDT)

Ran: `bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
Output tail:
- linked: 36 tools
- znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
- verify: python3 absent from safebin PATH (OK)
- verify: python absent from safebin PATH (OK)
- SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)

With `export PATH="$HOME/safebin"`:
- `which python3` resolves to NOTHING (empty output, verified literal)
- `which python` resolves to NOTHING
- `which znc` resolves to /home/hatch/safebin/znc
- `znc --version`: znc 2026.07.0-dev (edition 2026)

GUARD PASS. All lane work runs with PATH="$HOME/safebin"; pure Zag only; any
forbidden-interpreter invocation would be automatic PROCESS-FAIL for this lane wave.

## Standing rules acknowledged

Coordinator NAMECHECK.md read: prereg commit-order self-check before any verdict,
per-candidate PROPOSE/TEST/REDTEAM/VERDICT with frozen kill bars, red-team every
candidate, zero regressions for adoption, no em-dashes in docs (verify with
check_no_dash.sh), frozen lanes (no semantic-case treadmill, no kill-bar moves,
FW1-FW9 regression only), red lines (no spend/publish/outreach/push/Drive).
Pinned znc defects and workarounds recorded in ~/AGENTS.md, applied to all Zag work.

## Step 1: provenance targets

- composition_l2 frozen prereg: commit c521249ba
  "composition_l2: freeze PREREG (K1-K12) and NAMECHECK before implementation"
  (never got a clean implementation run; scaling wave went PROCESS-FAIL, exploratory only)
- ADAPT-REVISION truncate/specialize ops: commit 19c6433cc
  "ADAPT-REVISION-OPS-COMPLETE: truncate/specialize revision, 5/5 PASS, 3/3 deterministic"

Commit-order self-check on the prereg will run before any verdict.
