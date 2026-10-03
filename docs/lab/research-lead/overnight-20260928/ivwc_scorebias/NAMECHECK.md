# NAMECHECK.md -- IVWC-SCOREBIAS

Worker: ivwc-scorebias (score-side bias-estimator improvements for the IVWC hybrid).
Lane: docs/lab/research-lead/overnight-20260928/ivwc_scorebias/
Branch: tnn-native-lab. Non-ledger task (claim minting paused).

## Step 0: toolchain guard (worker toolchain guard, Micah's ruling)

- Safebin: $HOME/safebin active for all scientific computation.
  Verified 2026-10-03: `export PATH="$HOME/safebin"; which python3 python`
  returns NOTHING (no output). `which` resolves only the 36 allowed
  tools (coreutils, git, sha256sum, etc.).
- Forbidden interpreters: python3/python do not resolve under the
  safebin PATH. /usr/bin/python3 exists on the machine but is never
  invoked by this worker (no python in verifiers, scorers, harnesses,
  analysis, or scratch).
- Compiler: pinned znc
  src/tools/toolchain/znc_linux_x86_64_abed8aa1
  (`znc 2026.07.0-dev (edition 2026)`), invoked via absolute path.
- All research logic in pure Zag. Shell used only to invoke znc,
  run the binary, sha256sum, and git ops.
- Git writes via /usr/bin/git directly (safebin git symlink is
  known-broken for writes). Commits use explicit pathspecs confined
  to ivwc_scorebias/. Local only, never pushed.

## Step 1: identity

Single-file pure-Zag program src/ivwc_scorebias.zag, built from a
verbatim copy of IVWC-HYBRID's src/ivwc_hybrid.zag (commit
a76763bba) plus score-side bias-estimator variants in MAIN only.
World/belief/composer/stepper/verifier/seeds untouched, so sealed
(bucket, eff) pairs are bit-identical to the hybrid/perbucket runs
(K3/K4 anchors verify this in-program).
