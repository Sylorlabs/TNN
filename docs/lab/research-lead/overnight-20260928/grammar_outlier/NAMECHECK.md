# NAMECHECK: Grammar Outlier-Exclusion Worker

## Step 0: Toolchain Guard (2026-10-02)

Safebin activated before any research computation:
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returned NOTHING. Guard check done.
No Python, no forbidden executables in PATH. Pure Zag for all research
computation. Shell only for: invoking znc, running the binary, git ops,
file copies, checksums, diffs.

## Worker identity

Grammar Outlier-Exclusion Worker. Mission: repair the C222 W5
denial-of-learning vulnerability (one bad example poisons the whole
induction batch) with an outlier-excluding induction variant whose
exclusion criterion is learner-derived. Unfrozen lane only. Frozen
dirs (grammar_induction, grammar_transfer) read only, never modified.

## Prereg discipline

PREREG.md was committed first and alone (commit 2858ea46b) before any
implementation file was written. The implementation commit strictly
follows it. No frozen kill bar was altered; the one post-prereg code
refinement (nbuild counts examples consistent with the induced
grammar rather than all licensed examples) is documented in REPORT.md
and touches no preregistered bar.

## Files

- PREREG.md: frozen preregistration (hypothesis, exclusion criterion,
  arms A-G with predicted outcomes, pass/fail bars).
- go_base.zag: byte copy of grammar_transfer/gt_base.zag.
  SHA-256 a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd
  (matches the transfer report's recorded hash).
- go_patch.zag: first 9056 bytes byte-identical to
  grammar_transfer/gt_patch.zag (verified with cmp; the original
  gi_induce and all machinery functions unchanged), followed by the
  appended outlier-excluding variant: go_bit, go_rix, go_tgtcount,
  go_cover, gi_induce2 (320 new Zag lines).
  SHA-256 4da885d9da801f191a68b7ec7050fb7659ae412c843efda74ee5a0a2d309562e
- go_driver.zag: experiment driver. EXL2 teaching mirrors gt_driver;
  arms A (clean), B (one unlicensed deceiver), C (two minority
  deceivers), D (50/50 disjoint), E (majority poisoning), F
  (coordinated piggyback minority), G (piggyback 50/50 probe), plus
  the original-gi_induce comparison on arms A and B.
  SHA-256 88a7313b8fd359eaf8a5d146b3a3207b7912bc62efaca9bd22bb3037a87a49e1
- go_build.sh: assemble + compile with the pinned znc
  (src/tools/toolchain/znc_linux_x86_64_abed8aa1).
- go_bin: compiled binary.
  SHA-256 3bf43436c3a230ada33fd51077a63f531d0d7da7fcf70c97bebc62ca5af986d4
- go_run1.txt, go_run2.txt, go_run3.txt: 3 deterministic runs,
  byte-identical
  (SHA-256 29de7c2b1b26e735388c8eed9f45e7ddb55845db570cf3e5d2efe9bbaf36eeaa).
- REPORT.md: results and verdict.

## Toolchain lessons applied (per AGENTS.md)

- New Zag code defines NO print helpers: all output goes through the
  byte-copied base emit/e64. This avoids the pinned-znc
  name/layout-dependent _zag_print miscompile found 2026-10-02.
  Every binary's stdout bytes were verified against predictions.
- No `as *i32` plus slice construction anywhere in new code; only
  z_alloc/get32/set32 byte-buffer idioms.
- New code uses only base primitives (z_alloc, get32, set32, ng, ns,
  alloc_node) plus arithmetic and bounded while loops.

## Constraints observed

- Pure Zag. Zero em/en dashes in docs.
- 0 modes/bridges/handlers. 0 new semantic cases. 0 base modifications.
- NO hardcoded deception signatures: gi_induce2 contains no relation
  ids (no 43/44/46 literals), no per-world constants. Thresholds
  (strict majority, minimal cardinality, attestation sums) are computed
  from the batch and the learner's fact store. The nlic<=2 type-70
  node layout cap and the 10-relation / 16-example compute caps are
  documented machinery limits, not deception signatures.
- Nothing pushed. Commits local only, explicit pathspecs.
