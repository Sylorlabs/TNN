# NAMECHECK.md -- IVWC-CASEBIAS

Worker: ivwc-casebias (case-level bias signals for phantom-type
errors in the IVWC hybrid).
Lane: docs/lab/research-lead/overnight-20260928/ivwc_casebias/
Branch: tnn-native-lab. Non-ledger task (claim minting paused).

## Step 0: toolchain guard (worker toolchain guard, Micah's ruling)

- Safebin: $HOME/safebin active for all scientific computation.
  Verified 2026-10-03: `export PATH="$HOME/safebin"; which python3 python`
  returns NOTHING (rc=1, no output). `which` resolves only allowed
  tools (coreutils, git, sha256sum, etc.).
- Forbidden interpreters: python3/python do not resolve under the
  safebin PATH. /usr/bin/python3 exists on the machine but is never
  invoked by this worker (no python in verifiers, scorers, harnesses,
  analysis, or scratch).
- Compiler: pinned znc
  src/tools/toolchain/znc_linux_x86_64_abed8aa1
  (`znc 2026.07.0-dev (edition 2026)`), invoked via absolute path.
- All research logic in pure Zag. Shell used only to invoke znc,
  run the binary, sha256sum, grep/wc audits, and git ops.
- Git writes via /usr/bin/git directly (safebin git symlink is
  known-broken for writes). Commits use explicit pathspecs confined
  to ivwc_casebias/. Local only, never pushed.

## Step 1: identity

Single-file pure-Zag program src/ivwc_casebias.zag, built from a
verbatim copy of IVWC-SCOREBIAS's src/ivwc_scorebias.zag (world,
belief, composer, stepper, verifier, seeds untouched) plus
case-level bias machinery in MAIN only: per-case residual tables
on (bucket, preff), multi-policy agreement, and (bucket,
believed-bumps); a preregistered train-feature audit; and a
harness-side oracle diagnostic fenced inside the SCORING section
(never learner-visible). Sealed (bucket, eff) pairs bit-identical
to scorebias (K3/K4 anchors verify in-program).
