# NAMECHECK.md - lane F1RT, wave-20261002-1121pdt

Lane: F1RT (independent red team on the F1 seed-sensitivity finding).
Branch: lane-f1rt-20261002-1121pdt. Worktree:
~/workspace/tnn-rsi-work/wave-20261002-1121pdt/f1rt/
Run dir: docs/lab/rsi/runs/wave-20261002-1121pdt/f1rt/

## STEP 0 - Toolchain guard (recorded first, before any other work)

Safebin setup executed:
  bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
Setup output (literal):
  linked: 36 tools
  znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
  verify: python3 absent from safebin PATH (OK)
  verify: python absent from safebin PATH (OK)
  SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)

PATH exported to $HOME/safebin for all lane work.

Literal evidence:
  $ which python3
  (no output; exit 1)
  $ which znc
  /home/hatch/safebin/znc

Guard result: PASS. No forbidden interpreter is resolvable in this lane's
PATH. All research logic is pure Zag compiled by the pinned znc; shell is
used only to invoke znc, run binaries, and for git ops, cmp, sha256sum,
file moves/copies.

## Provenance of the artifact under judgment

- Finding: F1 seed-sensitivity (greedy-trial seed-sensitivity as a
  constructor property, magnitude X = R=13/40 overfit, T=2 first-trial
  classes, D_ops=9 structural paths, Cmax_ops=15/40 concentration).
- Verdict commit under red team: 655c8d7d6cffff47cef29e41c5b2dba31ae5ba27
  on branch lane-f1-20261002-0821pdt ("F1: sealed runs + analysis + verdict.
  K-DET PASS, NC-HARNESS PASS, bars ALL-PASS. FINDING CONFIRMED.").
- This lane did not produce the finding. Provenance of every file this lane
  touches is recorded in REPORT.md; the frozen constructor binary
  (sha256 6f2b155b233a95ad1a8323e8565b9a798dc822db6eff57e065b71b5be8882847)
  is used read-only and never modified.
- Standing rules for this wave read from
  docs/lab/rsi/runs/wave-20261002-1121pdt/NAMECHECK.md (coordinator level).
  Backlog read from
  docs/lab/rsi/runs/wave-20261002-0821pdt/BACKLOG.md (read-only).

## Lane scope (queue item 6)

Independent red team = promotion pipeline step 10 for the F1 finding.
Attacks: (a) harness artifact (seed leakage into world generation,
non-determinism in the test path, byte-non-identical reruns); re-run the
frozen battery in pure Zag, byte-identical reruns, multiple seeds. (b)
alternative explanations: ablate the suspected mechanism and check the
effect survives. (c) metric gaming: check the measured sensitivity is on a
metric the mechanism could not game. (d) independent reproduction from the
committed source alone. Deliverable: RED-TEAM VERDICT SURVIVES or
KILLED/WEAKENED with cited evidence, in REPORT.md.
