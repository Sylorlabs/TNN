# NAMECHECK: Composition L2 Adaptation Operator EXTEND-ONE (Orphan Recovery)

## Step 0: Triage Worker Note (2026-10-02)

This file was written by the watchdog triage worker during orphan
recovery, not by the original implementation worker. The original
worker never wrote NAMECHECK.md or REPORT.md.

- No code was compiled or run by the triage worker. Assessment only:
  file mtimes, sha256 checksums, git history, and file reads. No
  toolchain activation was required and no executables beyond
  standard shell inspection tools were invoked.
- Provenance: the directory was found untracked on branch
  tnn-native-lab at HEAD 05d1b7a28. PREREG.md and
  PREREG_AMENDMENT1.md were already committed (frozen) before this
  recovery; only implementation sources, build artifacts, and run
  outputs are added by the recovery commit. No file contents were
  altered except the creation of this NAMECHECK.md.

## Ordering evidence (verified)

- PREREG.md frozen ALONE: commit 897aa96b6, 2026-10-02 16:03:16 UTC.
  On-disk file mtime 16:02:03, byte-identical to the committed blob.
- PREREG_AMENDMENT1.md frozen ALONE: commit 9bf799fe4, 2026-10-02
  16:11:20 UTC. Byte-identical to the committed blob.
- Implementation files all postdate the prereg freeze: un_patch.zag
  copied 16:04:44, adapt_patch.zag 16:10:54, ad_driver.zag 16:11:14,
  ad_full.zag 16:11:26, ad_bin 16:11:41, ad_run1/2/3.txt 16:11:42-43.
- Both freeze commits are ancestors of the recovery base. Commit
  order self-check: prereg commits strictly precede this
  implementation commit.

## Amendment after results (flagged for director ruling)

- PREREG_AMENDMENT1 was written after the first implementation run.
  The amendment records the first-run sha256
  (2f974614491ed918aef055da1a809e46c1f358ddb980c7bcdd2bed61e93b9c3e);
  the first-run output file itself was overwritten by the re-run and
  is not on disk.
- The amendment did two things: (a) fixed a genuine operator bug
  (adapted MAPs promoted via adapt_promote, which teaches no derived
  fact, instead of promote_graph; the first run had A4-L1-ABL-Y answer
  107 against the frozen -2 bar); (b) dropped assertions p4/p5
  (segment-2 identity: the frozen prereg predicted MAP_Y, the
  unchanged unified DFS selects MAP_X via the plen-contract fallback
  tie-break), recorded as a wrong prediction about third-party DFS
  behavior, orthogonal to the L2 extension claim.
- Procedure followed: transparent amendment, committed alone
  (9bf799fe4), re-run only after re-freeze. Per standing governance,
  any kill-bar change after results requires the director's ruling
  before a COMPLETE verdict may be adopted. No verdict is declared by
  the recovery commit.

## Evidence inventory

- ad_run1.txt, ad_run2.txt, ad_run3.txt: byte-identical, sha256
  207d448a9aa7be0cab2161304358790742445a478260cd6e5280d1fe7a96b3ee.
- Amended kill bars per run output: A1 PASS (ans=108, adapted MAP
  with type-16 edge to MAP_X, MAP_Z LINK14 to adapted MAP, relseq
  [1,1,1,1]); A2 PASS (ans=108, relseq [1,1,1,2]); A3 PASS (ans=-2,
  zero adapted MAPs created); A4 all six L1 arms PASS
  (TREAT 107, ABL-X -2, ABL-Y -2, FRESH -2, REUSE 107, PROV).
- K7: un_patch.zag sha256
  3e61056a3f46148393a386ee88fadb1328ab419ce627e77cb56a9aa6aa06eab2,
  identical to composition_unified/un_patch.zag and to the value
  recorded in composition_integration/PREREG.md. cc_base.zag used
  read-only, never modified. un_patch.zag itself unmodified by this
  recovery (frozen reference copy).
- K6: zero em/en dashes in PREREG.md, PREREG_AMENDMENT1.md, and this
  NAMECHECK.md (byte-verified).
- Missing: REPORT.md (no verdict declared by the original worker);
  the original first-run output file (sha256 recorded in the
  amendment only).

## Non-duplication

- EXTEND-ONE closes the documented L2 gap "no extension operator"
  (COMPOSITION-LEVELS-COMPLETE). It is distinct from committed
  composition_l2 12/12 PASS (c521249ba, adaptive reuse battery),
  adapt_revision TRUNCATE/SPECIALIZE 4/4 (f1db655b4), and
  ADAPT-REVISION-OPS 5/5 (19c6433cc).

## Constraints observed

- Pure Zag research logic per the frozen PREREG. Local commits only,
  explicit pathspecs, nothing pushed. Paper untouched.
