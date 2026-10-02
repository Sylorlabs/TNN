# NAMECHECK_ADVERSARY.md - F1 adversary lane, wave wave-20261001-2021pdt

## Step 0 (toolchain guard)

I am the independent adversary for lane F1-ADVERSARY (sealed C0 battery and
sealed evaluation of the F1 implementation). I am independent of the F1
prereg author and the F1 implementation worker: I work from the committed
prereg PREREG_F1.md (committed alone at 27ef14078) and the frozen binary
only.

Safebin activation performed 2026-10-01 21:01 PDT, before any other work:

- Ran: bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
- Exported PATH="$HOME/safebin" (36 tools; pinned znc OK).
- `which python3` printed nothing (exit 1). `which python` printed nothing
  (exit 1). Toolchain guard satisfied.

Rules I follow this lane:

- PURE ZAG ONLY for analysis and scoring logic (compiled by the pinned znc).
  Shell only invokes the pinned znc, runs frozen binaries, performs git ops,
  cmp/sha256sum, and file moves/copies. Any forbidden executable invocation
  is automatic PROCESS-FAIL; none occurred.
- Working copy /home/hatch/workspace/tnn-rsi, branch tnn-native-lab.
  NEVER push. Never git reset --hard, never rebase. I do NOT git commit;
  the coordinator commits. I write ONLY inside
  docs/lab/rsi/runs/wave-20261001-2021pdt/F1/ (new files only:
  NAMECHECK_ADVERSARY.md, SEALED_C0.md, SEALED_EVAL.md; sealed files in
  F1/sealed/, which I create and the builder lane never reads).
- No em-dashes in any documentation I write. Determinism: 3/3
  byte-identical reruns for the sealed evaluation, verified by cmp and
  sha256sum.

## Frozen artifacts verified before sealed work

- Frozen binary: F1/dev/bin/f1_learn
- sha256: 0c571abca5a3c16695115228114c327bb3370081304c9c3a1ea1354840aa2727
  (verified with sha256sum before any sealed run; match confirmed).
- Protocol: f1_learn <episodes> <state_in|-> <state_out> <trace> <pred>
- Implementation sources (frozen): F1/impl/f1_isa.zag,
  F1/impl/f1_learn.zag. The C0-A audit below is run against these files as
  committed at the implementation-freeze commit recorded by the coordinator.

## My attack surfaces (from the prereg, my own design)

- C0-A: source audit for forbidden semantic names, researcher-named type
  tags/semantic branches, downgrade kill-pattern markers.
- C0-B: adversarial probe menu discriminating genuine trial-based
  construction from disguised menu selection (designed by me post-freeze).
- C0-C: post-freeze sealed worlds (4+ families): one requiring BRANCH/EQ
  discovery (untested in dev), one requiring multi-step composition, one
  with a mid-stream law change, one with a distractor law. Pre-run sha256
  recorded before execution.
- C0-D: VOID discipline throughout; any ordering violation, binary
  mismatch, or seal leak is reported as VOID, never as a verdict.

Verdict rule: BUILD-PASS requires every frozen kill bar; any kill bar trips
to BUILD-FAIL (bar named with evidence); C0-D trigger to VOID.
