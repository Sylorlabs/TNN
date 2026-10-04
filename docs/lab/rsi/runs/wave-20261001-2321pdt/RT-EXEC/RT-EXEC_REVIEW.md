# RT-EXEC red-team review: wave-20261001-2321pdt (F1 and TNN3H5R)

Reviewer: RT-EXEC. Method: read the full lane records, then independently
re-verified hashes (sha256sum), byte-identity (cmp), commit ordering
(git), and re-ran committed binaries and one committed sealed world from
source with the pinned znc. Read-only toward both lane dirs; nothing in
either lane was modified. Toolchain: safebin only, `which python3`
prints nothing (NAMECHECK.md Step 0); zero forbidden-executable
invocations in this review.

No em-dashes are used in this document.

## Prereg commit-order self-check (both lanes): PASS

- F1: prereg 50de694033d0d4d814be85555a73f4a129c9277e (2026-10-02
  06:32:33 UTC; commit contains only PREREG_TRIG.md and NAMECHECK.md, no
  implementation files) strictly precedes implementation
  ba5ebbf8b948f7fab786d6cfbe1a7d9708c5f41d (06:33:14 UTC).
- TNN3H5R: prereg dc7df4aba1db84e71e3e0b61c84adbf77244e590
  (2026-10-02 06:30:12 UTC; PREREG_H5R2.md alone) strictly precedes
  implementation 9db334bd4a01d21cce52da3bb2a1c45a10c4c172
  (06:31:39 UTC).

## Lane F1: EVIDENCE-HOLDS; recommend UPHOLD BUILD-FAIL (qualified)

### Attack 1: knowledge-vs-architecture confound

The trigger monitors only the learner's own binary error stream
(WIN=8 window, FMIN=2), with no domain content, no task knowledge, and
no semantic cases; the K-C0A source audit is clean and the constructor
(trial, burst, ISA) is unchanged from the prior wave. The wave's claim
is bounded infrastructure (a failure monitor), not an invention claim.
No confound found: the learned EQ structure on the interleaved families
comes from the pre-existing constructor once the trigger fires, which
is exactly the isolated variable.

### Attack 2: metric gaming

The worker reported the literal bar trip and did not weaken the bar.
Every number I could check cheaply matches the committed evidence:
- Sealed fixture hashes: all 23 match PREREG_TRIG.md section 8.
- Binary hashes: new impl/f1_learn =
  6f2b155b233a95ad1a8323e8565b9a798dc822db6eff57e065b71b5be8882847
  (matches SEALED_EVAL.md); prior wave's dev/bin/f1_learn =
  0c571abca5a3c16695115228114c327bb3370081304c9c3a1ea1354840aa2727
  (matches the NC-TRIG record).
- My re-run of the new binary on sealed rW2: train state byte-identical
  to sealed/runs/1/rW2_train.state; hidden pred byte-identical to
  runs/1/rW2_hidden.pred.
- Scorer (committed sealed/score): rW2 hidden ACC 0 30 0 (the tripped
  bar, confirmed); T-A hidden control ACC 30 30 100 (the passing claim,
  confirmed).
- rW2 train trace (new binary): 4 CONSTRUCT events, all-ADD overfit,
  matching the "4 constructs" record; rW2 train trace (old binary):
  8 TRIGGER lines, matching the "8 triggers" record.

### Attack 3: is the "pre-existing constructor limitation" attribution proven?

Yes, as strongly as this evidence form allows. I re-ran the prior
wave's frozen binary and the new binary on the sealed rW2 fixtures with
the documented invocation order. The two train states are byte-identical
(cmp). Both converge to the same 4-construct all-ADD overfit structure
(no EQ discovery on this seed). The old trigger fired 8 times on rW2,
so the failure is not even a trigger non-firing issue: the constructor
ran in both cases and overfit identically. The trigger change is
eliminated as a causal variable by construction: same constructor, same
seed, same inputs, byte-identical outputs.

### Attack 4: does the bar-calibration mistake invalidate the BUILD-FAIL?

No. The worker owns the mistake explicitly (JUDGE_BRIEF point 2):
K-C0C-REG used a fresh seed for the regression family without validating
that the unchanged, greedy, seed-sensitive constructor could solve it.
The mistake explains why the bar tripped, not whether the verdict
stands. The frozen verdict rule is literal (any kill bar trips means
BUILD-FAIL) and governance forbids weakening a frozen bar to force a
pass. The BUILD-FAIL stands on the bar as written.

### BUILD-FAIL vs PARTIAL-narrowed: recommendation UPHOLD BUILD-FAIL

PARTIAL is not a defined verdict in this lane's frozen verdict rules
(BUILD-PASS / BUILD-FAIL / VOID). Inventing a narrower verdict post-hoc
would be bar-weakening by another name, and the lane was correct not to
do it. Recommendation: UPHOLD BUILD-FAIL, with the exact qualification
that the killing evidence is a pre-existing constructor seed-sensitivity
(greedy depth-1 trial overfit on sealed seed 2301), proven by
byte-identical old/new train states on the sealed fixtures, and not a
trigger regression. Coordinator follow-ups, per the lane's own judge
brief: (a) accept the windowed trigger as the fixed failure monitor
(every trigger-specific bar passes; the superset property is
source-verifiable); (b) file the constructor's greedy-trial
seed-sensitivity (sum3 and rW2 overfits, both reproduced by the old
binary) as a separate constructor finding; (c) future regression legs
should reuse exact prior fixtures rather than fresh seeds when
constructor seed-robustness is not the variable under test.

Residual note: I did not independently re-run the prior wave's W2
fixtures (the lane's zero-regression-proof leg); that claim is neither
confirmed nor contradicted by my checks. The directionally stronger
check (old vs new on the killing fixtures) is confirmed above.

## Lane TNN3H5R: EVIDENCE-HOLDS; H5R2 ADVANCES stands

### Attack 1: single-worker seal integrity

The mitigations were frozen pre-implementation in PREREG_H5R2.md section
5.6 and every binding element I could check holds:
- Seeds, key ranges (83xxx-86xxx, disjoint from all prior batteries),
  value offsets, event patterns: all pinned in the prereg text.
- Driver template: the committed DRIVER_TMPL.zag blob hashes to
  f2d60568f55aef62d27d260a7ca3966933738b864b645e6c1e5e1cbfa1ea20af,
  exactly the prereg-frozen hash. The prereg's SHA-256 binds the
  template content.
- World hashes: all four sealed/*.zag files match the pre-run hashes in
  SEALED_H5R2.md.
- World assembly matches the frozen rule exactly: I decomposed w_c1.zag
  and the substrate portion differs from the committed tnn3_h5r2.zag by
  exactly the one main-swap line, followed by the 290-line template and
  the alias line.
- Commit sequence: exactly 3 commits (prereg 06:30:12, implementation
  06:31:39, sealed eval 06:34:48), no amends; the sealed commit touches
  only docs and world files; the substrate and binary are untouched
  between implementation and sealed commits (empty diff). No
  output-based tuning is visible in the commit sequence.

Procedural blemish noted: DRIVER_TMPL.zag first appears in the
implementation commit rather than the prereg commit. The seal holds via
content binding (the prereg hash matches the committed content), not
via commit timing. The builder's "written pre-freeze" attestation is
not independently verifiable from git, but no evidence contradicts it
and the frozen content is what ran.

### Attack 2: does t2_prov_ok genuinely anchor reverts to live facts?

Yes. I compiled the committed w_c1.zag with the pinned znc and ran it:
the full stdout SHA-256 is 76e5794c194b2e6d86e4776322048d6dfd05aac3d3f0c3bc411d6b14c1b673cc,
byte-identical to the lane's frozen KB-D1 record. White-box on that
run: 18 "W0 ok" lines (the w_c1 share of KB-W0), 6 probes each showing
exactly 2 superseded MAPs with CON self-edges plus 1 live MAP whose
every DEP edge is tag=1 sup=0, MAPCON-ALL=12 (NC-1R2 not fired), and 0
FAIL lines. The gate is load-bearing, not a narrower trick: the exact
superseded-MAP counts plus the DEP-to-live-facts clause cannot be
satisfied by promoting through dead provenance, and the W3 design
forces three dead lineages to be declined before the live fourth. The
DEP-to-live clause is the exact clause that killed H5R (8/12), now
12/12. The pinned known consequence (prereg 4.6) is honored: no bar
depends on dead-provenance promotion, and the behavioral bars
(KB-B2R 24/24, KB-B3 24/24) show declining dead-lineage candidates
causes no behavioral regression.

### Attack 3: KB-G1R architecture accounting honesty

Verified from the committed diff against the hash-verified H5R base
(blob d98d08f0746cab4fef88fb062933a314c12492f78ee98b496e8d8912cd7fd384,
matches the frozen record): the diff contains exactly the t2_prov_ok
helper and the four in-place gate modifications, nothing else. Counts:
5 occurrences of t2_prov_ok (1 definition + 4 call sites); 13 added
non-blank non-comment lines (9 helper + 4 modified sites), 4 removed,
net +9, budget <= 15. Zero new modes, bridges, routers, or handlers;
zero core-ISA additions; no forbidden protected semantic operations;
the helper is a read-path predicate over existing node state (ng/get32
plus the existing is_superseded predicate). The accounting is honest.
KB-S1 elements (gate at all four promote sites, H5R activate tag-20
admission hunk, zero shadow-fact teaching calls in promote_graph, all
inherited byte-identical from the verified base) are all present.

The scope note in SEALED_EVAL_H5R2.md is correct and I endorse it: this
advances the H5R2 hypothesis on the frozen sealed battery. It
establishes no broad generality claim and no L3 claim.

## Final per-lane verdicts

- F1: EVIDENCE-HOLDS. Recommend UPHOLD BUILD-FAIL with the exact
  qualification above: the killing evidence is pre-existing constructor
  seed-sensitivity proven by byte-identical old/new train states, not a
  trigger regression; the trigger itself passes every trigger-specific
  bar and is accepted as the fixed failure monitor per the lane's judge
  brief actions (a)-(c).
- TNN3H5R: EVIDENCE-HOLDS. H5R2 ADVANCES (BUILD-PASS) stands; the
  provenance gate is genuine, the seal mitigations hold, and the
  architecture accounting is honest.

## Commit ids and evidence paths

- F1: prereg 50de694033d0d4d814be85555a73f4a129c9277e; impl
  ba5ebbf8b948f7fab786d6cfbe1a7d9708c5f41d; sealed eval 3b159b401.
  Evidence: docs/lab/rsi/runs/wave-20261001-2321pdt/F1/ (PREREG_TRIG.md,
  IMPLEMENTATION.md, SEALED_EVAL.md, JUDGE_BRIEF.md, impl/, sealed/).
- TNN3H5R: prereg dc7df4aba1db84e71e3e0b61c84adbf77244e590; impl
  9db334bd4a01d21cce52da3bb2a1c45a10c4c172; sealed eval e20ba5402.
  Evidence: docs/lab/rsi/runs/wave-20261001-2321pdt/TNN3H5R/
  (PREREG_H5R2.md, IMPLEMENTATION_H5R2.md, SEALED_H5R2.md,
  SEALED_EVAL_H5R2.md, JUDGE_BRIEF.md, tnn3_h5r2.zag, tnn3_h5r2.bin,
  DRIVER_TMPL.zag, sealed/).
- This review: docs/lab/rsi/runs/wave-20261001-2321pdt/RT-EXEC/
  (NAMECHECK.md with Step 0, RT-EXEC_REVIEW.md).
- Review scratch (not committed): /tmp/rt_exec_recheck/.
