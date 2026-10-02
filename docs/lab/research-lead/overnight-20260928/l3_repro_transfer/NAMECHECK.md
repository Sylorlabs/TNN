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

- [ ] R1 REPRO-BUILD: rebuilt from committed source, zero errors.
- [ ] R2 REPRO-DETERMINISM: 3/3 byte-identical per rebuilt binary.
- [ ] R3 REPRO-FIDELITY: digests match committed; M=(4,0,0); 9/9.
- [ ] R4 REPRO-AUDIT: C281 grep specs zero on committed machinery.
- [ ] R5 TRANSFER-SOLVE: Z PASS both, M'=(1,0,0) created=1.
- [ ] R6 TRANSFER-NECESSITY: L1-ONLY/ABL-X/ABL-Y/FRESH fail both.
- [ ] R7 TRANSFER-M-NECESSARY: NO-M fails both (ablation).
- [ ] R8 TRANSFER-CREATED: C-ROUND gain>0; origin audit clean.
- [ ] R9 TRANSFER-REUSE: Z2 PASS both, build_count==1.
- [ ] R10 TRANSFER-REVISE: code 2 both; Mprev=(1,0,0) sup=1;
      M=(1,0,0,4,0,0); Z3 PASS both.
- [ ] R11 TRANSFER-DETERMINISM: 3/3 byte-identical per binary.
- [ ] R12 TOOLCHAIN: safebin held for the whole run; no forbidden
      executable invoked.

## Namecheck audit notes

(Any anomaly found during the run is recorded here with the step
where it was found. None before implementation.)
