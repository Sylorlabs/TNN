# NAMECHECK.md - wave-20261002-1121pdt, lane CONTLEARN (queue item 9)

Lane: CONTLEARN. Worker: contlearn lane worker, wave-20261002-1121pdt.
Branch: lane-contlearn-20261002-1121pdt.
Worktree: ~/workspace/tnn-rsi-work/wave-20261002-1121pdt/contlearn/.
Task: three exercises under frozen preregs: (a) refusal-branch,
(b) learner-scheduled initiation, (c) cross-kind rebind.

## Step 0: toolchain guard (recorded first, before any other work)

Setup command run:
  bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
Setup output (tail):
  linked: 36 tools
  znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
  verify: python3 absent from safebin PATH (OK)
  verify: python absent from safebin PATH (OK)
  SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)

PATH exported as: export PATH="$HOME/safebin"

Literal outputs under the safebin PATH:
- `which python3` resolves to NOTHING (empty output).
- `which python` resolves to NOTHING (empty output).
- `which znc` resolves to /home/hatch/safebin/znc.

Guard: PASS. All lane work runs under the safebin PATH. Pure Zag only;
any forbidden-interpreter invocation is automatic PROCESS-FAIL.

## The six binding caveats (from CONTLEARN3/CLH2; all bind this lane)

1. Proposal CONTENT (mech=TRY_CHAIN) is a fixed researcher template. No
   claim of learner authorship of proposal content.
2. Proposal initiation is still event-triggered, not learner-scheduled.
3. No learner agency in the causal sense.
4. The gate's refusal branch is structurally enforced but empirically
   unexercised (0 MACHINERY_SKIPPED, three consecutive lanes).
5. No L3, no generality. Batteries are disclosed and prereg-frozen,
   not sealed adversarial.
6. Citation form stays machinery-enabled per the debate Q7 binding form.

Relation to this lane's exercises:
- Exercise (a) exercises a refusal path empirically for the first time
  (a new ledger-based instrument refusal, not the pf gate's branch; the
  pf gate's MACHINERY_SKIPPED branch remains unexercised and this is
  stated, not hidden). Caveats 1, 3, 5, 6 stand unchanged.
- Exercise (b) attacks caveat 2 directly: initiation timing caused by
  learner state (uncertainty accumulation) vs harness event index, with
  a kill bar on the distinction. Caveats 1, 3, 5, 6 stand unchanged;
  the claim is state-causation of timing, not learner authorship.
- Exercise (c) tests cross-kind rebind (count-kind learning rebound as
  chain-kind procedure) on the unmodified frozen core. Caveats all
  stand; the claim is bounded to the disclosed battery.

## Provenance of inherited artifacts

- Frozen base core for instruments (a) and (c): byte copy of
  docs/lab/rsi/runs/wave-20261002-0521pdt/CONTLEARN/clh2_core_control.zag,
  SHA-256 26b455e78a9b0ba0f6d6967c12ff8c05f9ebd9152dddca9efeb2a3b44064ec9d
  (the recorded nomain derivation of the frozen TNN-2 core). Verified by
  hash before any build; the frozen path is never written.
- Frozen base core for instrument (b): byte copy of
  docs/lab/rsi/runs/wave-20261002-0521pdt/CONTLEARN/clh2_core_treat.zag,
  SHA-256 627af6eb0e88141fdeb00baba0aab178a29df128aa0250398355db42d8557f63
  (the proposal-gated instrument from CONTLEARN3). Verified by hash
  before any build; the frozen path is never written.
- Drivers are new lane fixtures (0 cognition functions, 0 structural
  writes, 0 new tags/edges/opcodes/modes/bridges/handlers/semantic
  cases), written after each prereg freeze.
- Prior lane branch lane-contlearn-20261002-0821pdt read for provenance
  only (binding caveats recovered from its 0521pdt CONTLEARN verdict);
  nothing copied from it except the frozen core bytes above.

## Standing rules acknowledged

Pure Zag only. No Python anywhere. Prereg commit-order self-check
(K0) before any verdict: each prereg committed alone, implementation
strictly descendant. Kill bars frozen before implementation, never
moved after. No em-dashes in loop docs (verified with
check_no_dash.sh). Pathspec-only commits to this lane branch, this
lane dir plus docs/lab/rsi/runs/wave-20261002-1121pdt/contlearn/.
Never commit to tnn-native-lab. Never push. Never rebase. No writes
into scaling_5000_fixed or scaling_10000. Red lines: no spend, no
publish, no contacting outsiders, no purchases or bookings, no
irreversible commitments, never Google Drive.
