# NAMECHECK: L3 Reproduction and Transfer (L3-REPRO-TRANSFER)

Worker: L3 Reproduction and Transfer Worker (subagent, 2026-10-02).
Prereg: PREREG.md, frozen and committed BEFORE implementation
(this file's Step 0 predates the prereg commit; all implementation
steps postdate it).

## Step 0: Toolchain guard (mandatory, recorded before any work)

- Created $HOME/safebin with symlinks for 49 allowed tools
  (git, znc, sh, bash, ls, cp, mv, rm, mkdir, cat, grep, sed, awk,
  wc, cmp, sha256sum, git-receive-pack, git-upload-pack, find, diff,
  head, tail, sort, uniq, tr, cut, date, and other coreutils).
- Exported PATH="$HOME/safebin" for all work below.
- `which python3 python` returns EMPTY (no output before
  "guard-check-done"). Verified 2026-10-02.
- The pinned znc used for builds is
  $HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1
  (reached via its absolute path, not via PATH; it is the same
  pinned compiler the C281 build.sh names).
- No Python, no other interpreter, no network fetch of code is used
  anywhere in this experiment. Pure Zag for all research logic;
  shell only invokes znc, runs binaries, and does file/git ops.

## Pre-implementation checks (before the prereg commit)

- [x] C281 commits e5b747176 (prereg freeze) and 762cda924
  (implementation) located on branch tnn-native-lab.
- [x] Reference copies extracted to this directory and verified
  byte-identical to git show output (sha256 match recorded in
  REPORT.md).
- [x] Committed run-log digests match the C281 REPORT values
  (H1 abc3e018..., H2 ee0bf4ba...); extraction did not corrupt them.
- [x] Original C281 directory
  docs/lab/research-lead/overnight-20260928/xdomain_grammar_l2m/
  is untouched (git status clean for that path; this worker only
  reads it via git show).
- [x] Transfer world hand-derived expectations computed by hand
  from the frozen generic greedy algorithm (section 4 of PREREG.md);
  no implementation output was consulted.

## Post-freeze checks (filled as the experiment runs)

- [x] R1 REPRO-BUILD: rebuilt from committed source with the pinned
  znc, zero compile errors. Rebuilt binaries are BYTE-IDENTICAL to
  the committed h1_bin/h2_bin (sha256 6f076073... / af7870cd...).
- [x] R2 REPRO-DETERMINISM: 3/3 byte-identical runs per rebuilt
  binary (sha256 recorded in REPORT.md).
- [x] R3 REPRO-FIDELITY: run-output digests equal the committed
  digests (H1 abc3e018..., H2 ee0bf4ba...); M-PROG bytes (4,0,0)
  with C-ROUND 1 base=0 win=4,0,0 gain=2 score=2; TOTAL 9/9 both.
- [x] R4 REPRO-AUDIT: C281 prereg section 8 grep specs return zero
  matches on the committed machinery; SUPPLIED-INSTALL appears
  exactly once per committed run log, inside the SUPPLIED arm.
- [x] R5 TRANSFER-SOLVE: Z PASS both; H1 REBOUND a=5 param=83
  rebound_of=0; H2 VC-COMPOSE ok m1=1 m2=2 rel=83; m_created=1;
  M-PROG bytes (1,0,0).
- [x] R6 TRANSFER-NECESSITY: L1-ONLY, ABL-X, ABL-Y, FRESH fail both.
- [x] R7 TRANSFER-M-NECESSARY: NO-M fails both (rebind finds 48,
  Y lookup misses -> L2-FAIL); reproduction NO-M likewise fails.
- [x] R8 TRANSFER-CREATED: C-ROUND 1 base=0 win=1,0,0 gain=2
  score=2; origin audit clean (machinery code has no transfer-world
  literals; 83/84 only on add_fact lines in drivers); no
  SUPPLIED-INSTALL on the transfer TREAT path.
- [x] R9 TRANSFER-REUSE: Z2 PASS both; build_count==1 after Z+Z2.
- [x] R10 TRANSFER-REVISE: adapt code 2 both; Mprev (1,0,0) sup=1;
  M (1,0,0,4,0,0); Z3 (5,145) PASS both.
- [x] R11 TRANSFER-DETERMINISM: 3/3 byte-identical per transfer
  binary (H1 c03202cd..., H2 6bae6757...).
- [x] R12 TOOLCHAIN: safebin held for the whole run; `which
  python3 python` empty at start and end; pure Zag; 0
  modes/bridges/handlers.

## Namecheck audit notes

(Any anomaly found during the run is recorded here with the step
where it was found.)

- R8b machinery audit refinement (found during transfer build):
  the word-boundary grep for transfer-world literals in
  tr_learner.zag returns one match: the comment line
  `//   [24..27]=build_count i32, [28..31]=reserved.`
  The "24" is a byte offset inside the M slot layout comment
  (absolute bytes 2136..2139), not a world literal; the code uses
  the absolute constant 2136, never 24. Non-comment lines are fully
  clean of all transfer-world literals
  (81,82,83,84,24,36,48,60,72,96,120,145). Recorded as a comment-only
  exception, not a bar failure: the constructor cannot read comments,
  and the C281-style relation audit (71|72|73|74|81|82|83|84) is
  zero on all lines.
- No other anomalies. The frozen hand-derived transfer expectations
  (PREREG.md section 4) matched the implementation output exactly,
  including the 10-try TREAT Z trace, the C-ROUND winner bytes, and
  the adapt extension winner bytes.
