# REPORT: TRUNCATE Theorem Boundary Conditions

Worker: Truncate Theorem Boundary Worker. Date: 2026-10-02.
Branch: tnn-native-lab, local only, nothing pushed.

## Governing bars

Verdict governed by the frozen kill bars in
`docs/lab/research-lead/overnight-20260928/truncate_theorem/PREREG.md`
(commit 49641f9c8) plus PREREG_AMENDMENT1.md (committed in HEAD
before any implementation commit by this worker): K-A1..K-A5,
K-B1..K-B4, K-C1..K-C4, K-T1..K-T3, K-D, K-H1, K-H2. PREREG.md
itself was not modified (sha256
5f297cb95a03b8bc11734e03cda96de336303d79a28b9355ab3772fe97f3bc5e,
identical to the frozen commit).

## Provenance note

The implementation sources (tt_patch.zag, tt_driver.zag,
build.sh) were present in the working tree from a prior
incomplete wave that never committed them and never produced a
REPORT. This worker read both Zag sources in full, checked each
against the PREREG plus Amendment 1 operator and arm specs,
rebuilt the binary from source under the safebin guard, and ran
all three runs itself. No result from the prior wave was
adopted; every value below was observed in this worker's own
build and runs.

Amendment 1 was honored: its arm A correction fixes a genuine
design bug verified independently from the frozen substrate
(ts_truncate_src and tt_nonprefix_src both require
cc_satisfy(src, s) == L; in arm A phase 2 the query source is
s = 32 while Z = [1,2,1] is rooted at 31 and no live (32,1,*)
fact exists, so the ev_query_tt fallback can never create the
head-drop from s = 32). The amendment changes only the creation
mechanism (direct adapt_nonprefix(W,31,0) call, s = 31 is Z
root), strengthens K-A1 with the nk = 1 determinism requirement,
and weakens no kill bar. Its K-H2 refinement (whole-word
mode/bridge/handler grep) is required because the frozen
identifier adapt_promote contains the substring "mode".

## Build record

- Safebin guard enforced by build.sh: python3/python do not
  resolve under $HOME/safebin; znc = /home/hatch/safebin/znc.
- Five frozen copies re-copied from ../adapt_revision_ops/ and
  sha256-verified identical: cc_base.zag
  (dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6),
  un_patch.zag
  (3e61056a3f46148393a386ee88fadb1328ab419ce627e77cb56a9aa6aa06eab2),
  adapt_patch.zag
  (867bd6d96d9d4026c39d9bc5a9c6944f9ac0427722a3f6451c325c49f60c2ff0),
  revise_patch.zag
  (5113000b1360bf3e978cb106f91f15a1e5956db113eb4b3c26a1ebde1fa7f6e3),
  ts_patch.zag
  (07b7b3952db65b04d8bccf288d28ff0a2aaa899fefd75a1da0250baa7d22b451).
- znc compile exit 0 (warnings only: zagd unavailable notice and
  A0102 ignored-return notes inside frozen code). tt_bin
  384548 bytes, sha256
  b42699fece7259cb9cbf1c2350b604dc857c053d1863097930a15568ae1f59ad.
- 3/3 runs byte-identical: sha256
  50d1fbf818b7b046f3587569afbe0fe568f7f071d1ec698d3ffca3fc29a0f8ff
  for run1.txt, run2.txt, run3.txt; cmp clean.
- REVISE2-STALE emission count across all runs: 0.

## Arm A: A-NONPREFIX-STALE (H-A: non-prefix TRUNCATE can go stale)

Observed: mapz = 27 (Z = [1,2,1]); direct call
adapt_nonprefix(W,31,0) returned nk = 1 and emitted
TT-NONPREFIX-MK id = 47 src = 27 linkto = 27 len = 2;
phase-2 query (32,72,34) answered 34 via the rebind path
(RB-STAT tried = 1 rejected = 0). Located Xt = 47, relseq
[2,1], ng(47,12) = 2, type-16 edge 47 -> 27, c0 = 1.
World change: taught (32,5,40) as node 59, killed (32,2,33);
withdrew the (32,72,34) shortcut. Phase-4 query (32,73,99)
answered -2 (ADAPT-CREATED n = 0).

- K-A1 PASS: ph2 = 34, nk = 1, Xt relseq [2,1], kind 2,
  type-16 Xt -> Z.
- K-A2 PASS: post-change cc_relseq(Xt) no longer reads [2,1]
  (p3 = 1). The head-drop shares licensing nodes with the
  source but its root differs; the pure-prefix protection does
  not extend to it, and the staleness is correctly detected.
- K-A3 PASS: post-change cc_relseq(Z) no longer reads [1,2,1]
  (p4 = 1). Documents why the revision gate stays closed.
- K-A4 PASS: no type-16 edge targets Xt and c1 = c0 = 1
  (p5 = 1). The frozen predicate declined revision because Z
  is not intact.
- K-A5 PASS: Xt still live (tag 20, field 36 = 1; p6 = 1) and
  ph4 = -2 (p7 = 1).

## Arm B: B-PREFIX-MID-REPLACE (H-B: damaged source, prefix middle)

Observed: mapx = 27 (X = [1,1,1]); phase-2 query (11,72,13)
created TS-TRUNC-MK id = 60 src = 27 linkto = 27 len = 2 via
the fallback (the head-drop [1,1] deduped away, no
TT-NONPREFIX-MK emission) and answered 13. Located Xt = 60,
relseq [1,1], ng(60,12) = 2,
type-16 edge 60 -> 27, c0 = 1. World change: taught (12,1,98)
as node 72, killed (12,1,13); withdrew the (11,72,13)
shortcut. Phase-4 query (11,73,99) answered -2
(ADAPT-CREATED n = 0; rebind tried = 2 rejected = 2).

- K-B1 PASS: ph2 = 13, Xt relseq [1,1], kind 2, type-16 Xt -> X.
- K-B2 PASS: post-change Xt is STALE (p3 = 1). Pure-prefix
  protection requires an intact source.
- K-B3 PASS: post-change X is not intact (p4 = 1).
- K-B4 PASS: no revision fired for Xt (p5 = 1); Xt still live
  (p6 = 1); ph4 = -2 (p7 = 1).

## Arm C: C-PREFIX-ROOT-REPLACE (H-C: damaged source, prefix root)

Observed: identical phase-2 shape to arm B (mapx = 27,
Xt = 60, kind 2, type-16 60 -> 27, c0 = 1, ph2 = 13).
World change: taught (11,1,77) as node 72, killed (11,1,12);
withdrew the (11,72,13) shortcut. Phase-4 query (11,73,99)
answered -2 (ADAPT-CREATED n = 0).

- K-C1 PASS: ph2 = 13, Xt = [1,1], kind 2, type-16 Xt -> X.
- K-C2 PASS: post-change Xt is STALE (p3 = 1).
- K-C3 PASS: post-change X is not intact (p4 = 1).
- K-C4 PASS: no revision fired for Xt (p5 = 1); Xt still live
  (p6 = 1); ph4 = -2 (p7 = 1).

## Arm T: T-THEOREM-CONTROL (positive control)

Observed: mapx = 27, Xt = 60 created in phase 2, ph2 = 13.
World change: taught (13,1,99) as node 72, no kill; withdrew
the (11,72,13) shortcut. Phase-4 query (11,73,13) answered 13
via the rebind path over Xt (RB-STAT tried = 1 rejected = 0).

- K-T1 PASS: ph2 = 13 and Xt = [1,1] created.
- K-T2 PASS: post-change X intact (cc_relseq reads [1,1,1],
  p3 = 1; cc_satisfy(X,11) = 3, p4 = 1) and Xt intact
  (cc_relseq reads [1,1], p2 = 1; cc_satisfy(Xt,11) = 2,
  p5 = 1). First-live determinism held: the duplicate
  (13,1,99) took a higher node id and did not disturb the
  prefix licensing.
- K-T3 PASS: no revision fired for Xt (no type-16 targets Xt,
  p6 = 1) and ph4 = 13 (p7 = 1).

## Harness

- K-D PASS: 3/3 byte-identical runs (sha256 equal, cmp clean).
- K-H1 PASS: zero em/en dash bytes in PREREG.md, REPORT.md,
  NAMECHECK.md, tt_patch.zag, tt_driver.zag (build.sh check
  prints "no em dashes" / "no en dashes").
- K-H2 PASS: five frozen copies sha256-identical to
  ../adapt_revision_ops/ originals; whole-word
  mode/bridge/handler grep on tt_patch.zag and tt_driver.zag
  returns 0; no `as *i32` slice pattern in new sources;
  build.sh enforces the safebin guard (aborts if
  python3/python resolve); all research logic is pure Zag
  (shell used only to invoke znc, run the binary, and do
  file/git operations).

## Boundary map (confirmed)

- Pure-prefix + source intact: cannot go stale (arm T: Xt and
  X intact, no revision, ph4 = 13 through Xt).
- Pure-prefix + source not intact: CAN go stale; the
  predicate correctly declines revision (arms B and C: Xt
  stale, X not intact, zero REVISE2-STALE emissions,
  type-16 edge counts unchanged).
- Non-prefix (head-drop) + source not intact: CAN go stale;
  the predicate correctly declines revision (arm A: Xt stale
  and detected, Z not intact, no revision, Xt still live,
  ph4 = -2).
- The "source intact" gate in the revision predicate is
  load-bearing, not decorative: in all three damage arms the
  adaptation went stale exactly when its source did, and the
  gate stayed closed in every case.
- Open question (unchanged, not a claim): non-prefix
  TRUNCATE with an intact source is not constructible in this
  substrate (the head-drop shares licensing nodes with its
  source, so any licensing death breaks both).

## Architecture accounting

- Cognition lines added (unfrozen): tt_patch.zag
  (tt_nonprefix_src, adapt_nonprefix, ev_query_tt) and
  tt_driver.zag (4 arms plus local helpers).
- New hardcoded semantic cases: 0. New modes: 0. New
  bridges: 0. New handlers: 0. New opcodes: 0. New MAP
  types: 0. New edge types: 0 (type-16 adapted-from edge
  reused; kind 2 recorded in MAP field 12 per the frozen
  Amendment 1 convention).
- The operators name no relation, MAP, length, query, or
  expected value.

## Verdict

ALL kill bars pass: K-A1..K-A5, K-B1..K-B4, K-C1..K-C4,
K-T1..K-T3, K-D, K-H1, K-H2.

**TRUNCATE-THEOREM-COMPLETE** (with boundary results).
