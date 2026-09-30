# Preregistration: G2 Refutation-Seeking IV Policy

Date: 2026-09-30. Worker: G2 Beam Builder.
Status: FROZEN. Committed before any implementation is written.

## 0. Standing rules name-check

- Pure Zag only. No Python at any stage: authoring, building with znc,
  running, verification (shell tools only: sha256sum, md5sum, cmp, grep,
  wc, git), byte checks (worker_snippets/check_no_dash.sh). Zero Python
  has been invoked from task start. No purity disclosure is needed.
- No em/en dash bytes in loop documentation (shell-verified before commit).
- Prereg commit strictly precedes implementation (commit-order self-check).
- Frozen base sources are never edited; work happens on copies under
  beam_g2/.
- The contaminated research paper is not touched.
- Commits local, owned pathspec only
  (docs/lab/research-lead/overnight-20260928/beam_g2/).
- Other workers' files are not touched.
- If a git lock is encountered, wait; never remove a live lock.

## 1. Design adopted

BEAM_NEXT_DESIGN.md section 4, G2 branch (commit 446233dd5):
"Refutation-seeking IV policy. A complement to (not replacement of)
the disagreement IV selector. For each unused x, compute agree_frac =
the fraction of beam members whose prediction matches the current
champion's prediction; select the x minimizing agree_frac, i.e.
maximal beam-internal disagreement about the champion's own prediction."

This builder adopts the primary operationalization (agree_frac).
The sparse-neighborhood alternative is not adopted.

Gating note: BEAM_NEXT_DESIGN gates G2 on branch (c), or on (a)+(b)
ruled out with no refuting evidence observed. G0 resolved G0-MERGED
(branch b). The parent explicitly tasked G2 per the G0 worker's
recommendation (RESULT_BEAM_G0.md section 9), citing the
evidence-accuracy caveat. This prereg follows the parent's direction
and records the caveat as a pre-registered alternative explanation
(section 6).

## 2. Scope and files

Owned directory:
docs/lab/research-lead/overnight-20260928/beam_g2/

Implementation files (modified copies of frozen bases):

- r3g.zag: R3 battery (Arms 1-2, fams 7-8) with G2 IV policy.
  Base: beam_unified_clean/r3u.zag (commit fc03664f2, BEAM-UNIFIED-FAIL).
- frg.zag: F-RECFOLD battery (3 instances x 5 seeds, fams 7-9,
  Phase-1 discovery only) with G2 IV policy.
  Base: beam_unified_clean/frecu.zag (commit fc03664f2).
- r1g.zag: R1 battery (5 seeds, P-RAND, F-PARCOND fam 5), copied
  unchanged from beam_unified_clean/r1u.zag. The R1 policy is
  select_iv_rand per the frozen policy; G2 does not modify R1.

Only the IV selection machinery changes in r3g.zag and frg.zag:

- select_iv_u replaced by select_iv_g2 (section 3).
- Call sites pass the IV index (section 3).
- Dead-code call sites updated for compilation only.

UNCHANGED (verified by diff after assembly):

- Candidate generation loop inside beam_extend_u (beam members, NOTs,
  pairwise AND/OR/XOR). This is the F-BLOAT basis.
- beam_extend_u retention logic (U1/U2/U3/U5/U6).
- score_node arithmetic.
- sealed families, passive, do_iv, true_correct, node_new_term,
  node_new_op, node_new_libterm, sigtab, PRNG, drivers (seeds, bars,
  evidence-loop structure), round structure.
- r1g.zag is byte-identical to r1u.zag.

## 3. G2 operationalization

### 3.1 Function signature

`fn select_iv_g2(st:[]u8, nodes:[]u8, beam:[]u8, bspec:[]u8, used:[]u8, iv_idx:i32)i32`

iv_idx is the 0-based count of IVs selected so far in the current
phase invocation. Call sites pass the loop variable r.

### 3.2 Interleave rule (frozen)

- If iv_idx % 2 == 0: use the frozen disagreement selector
  (verbatim logic from select_iv_u in the base file).
- If iv_idx % 2 == 1: use the refutation-seeking selector
  (section 3.3).

This satisfies "complement to (not replacement of)": both selectors
are used, each on 12 of 24 IVs per phase.

### 3.3 Refutation-seeking selector (frozen)

1. Build the hypothesis set H exactly as in select_iv_u: from the
   beam in beam order, take the first member of each distinct species
   (species ids from bspec), up to 8 hypotheses. Store node ids in
   hnode[0..H-1].
2. Champion = hnode[0]. By construction hnode[0] is beam[0] (the
   first beam member is the first of its species). beam[0] is the
   accuracy-first pick per U6.
3. For each unused x in 0..63:
   a. champ_p = node_pred(nodes, champion, x).
   b. agree = count of k in 0..H-1 where
      node_pred(nodes, hnode[k], x) == champ_p.
   c. c1 = count of k in 0..H-1 where
      node_pred(nodes, hnode[k], x) == 1.
   d. d = H - abs_i(2*c1 - H) (frozen disagreement measure).
4. Select the x minimizing agree. Tie-break: max d. Final tie-break:
   lowest x.
5. If H < 1, return -1 (as in the frozen code).

All predictions use node_pred on the learner's own nodes. No target,
family, or library knowledge enters. F-CASE applies unchanged.

### 3.4 Call sites

- r3g.zag phase2 (live): `select_iv_g2(st, nodes, beam, bspec, used, r)`
  where r is the loop variable (0..23).
- r3g.zag phase1 (dead code): signature updated for compilation;
  passes r.
- frg.zag phase1 (live): `select_iv_g2(st, nodes, beam, bspec, used, r)`
  where r is the loop variable (0..23).
- frg.zag phase2 (dead code): signature updated for compilation;
  passes r.
- r1g.zag: unchanged (select_iv_rand).

### 3.5 Cost

The refutation selector computes at most 64 * 8 = 512 node_pred
calls per IV selection, identical to the frozen disagreement
selector. IV predictions do not call score_node and do not affect
MAXSIMS. F-BLOAT measures candidate simulations in beam_extend_u,
which G2 does not modify.

## 4. Frozen control baselines

Control step: recompile each base file with znc (same pinned
compiler), run 3x, verify byte-identical to the committed raw
outputs from the unified clean rebuild.

- R1: beam_unified_clean/r1u.zag, 3/3 byte-identical md5
  89cb21e6359bafaf3d02d34575d3bd0a.
- R3: beam_unified_clean/r3u.zag, 3/3 byte-identical md5
  6a8568a7232de691606e09712df0f17d.
- F-RECFOLD: beam_unified_clean/frecu.zag, 3/3 byte-identical md5
  95b87706c9763e22e075a5b11fc79f38.

If any control fails to reproduce, halt and report; do not run G2
against a moved baseline.

The F-BLOAT ceilings from the unified clean prereg are reused
verbatim (BASE_battery maxima from the baseline runs):
- R1: BASE=1109, CEIL=(1109*110)/100=1219.
- R3: BASE=1149, CEIL=(1149*110)/100=1263.
- FREC: BASE=1130, CEIL=(1130*110)/100=1243.

G2 does not modify candidate generation, so the ceilings remain
valid. F-BLOAT fires iff any G2 driver invocation's MAXSIMS exceeds
CEIL_battery.

## 5. Falsifiers (frozen)

- F-FIT: fewer than 4 of 5 R1 seeds reach EVFIT=32/32 under G2
  (R1 driver, P-RAND, fam 5). r1g.zag is unchanged, so this is a
  pure regression guard.
- F-DIVERSE-FAIL: R3 Arm 2 still fails its frozen bar (A2-PASS=0:
  requires 64/64 AND reuse_iv*2 <= scratch_iv AND HAS_D=1).
  This is the primary outcome G2 targets.
- F-NODOM: NODOMV > 0 in any driver invocation. G2 does not modify
  retention; this is a regression guard. If it fires for the same
  exploration-round reason as the unified build, the report will
  note that the cause is the retention ordering, not the IV policy.
- F-TIE-HONEST: "TIE=DEFECT" or "TIECHECK=FAIL" appears in R1 output.
- F-REGRESS: R3 Arm 1 A1-PASS goes from 1 (frozen) to 0
  (requires 64/64 AND reuse_iv*2 <= scratch_iv).
- F-BLOAT: any G2 driver invocation's MAXSIMS exceeds CEIL_battery
  for its battery (ceilings in section 4).
- F-CASE: audit finds any new-machinery component keying on target,
  family, or library identity. The refutation selector uses only
  the learner's own beam predictions; no sealed values enter.

F-RECFOLD (frg.zag) is exploratory, not a falsifier: report B1/B2/B3
per the frozen F-RECFOLD bars for information.

## 6. Pre-registered alternative explanation

A1 ("merged, then would have lost anyway"): The G0-observed Q
candidates (round 2, accuracies 1, 1, 1, 9 of 64) were absorbed by
the species-merge rule, but they would have lost a fair
within-species retention fight due to low evidence accuracy. The
merge rule is not the binding constraint; the binding constraint is
that the generator never proposes behaviorally-good E-shaped
candidates, because the evidence lacks refuting power (post-mortem
Cause 3).

G2 kills A1 iff all of the following hold:
- (a) Under G2's refutation-seeking IVs, E-shaped candidates
  (Q signature: depth 3, operator histogram [2,1,1,0]) are proposed
  with evidence accuracy materially higher than the G0 baseline
  (at least one Q candidate above 32/64, i.e. above chance on the
  evidence).
- (b) R3 Arm 2 improves relative to the unified baseline
  (final_true above 52/64 on A2-REUSE, or A2-PASS=1).

If G2 fails F-DIVERSE-FAIL with Q candidates still at low accuracy,
A1 survives: the evidence was not the binding constraint.

Measurement: the G2 build does not include G0-style
instrumentation. Q-signature prevalence is assessed from the
retained beam members' operator histograms where logged. If the
data are insufficient to evaluate (a), the report will state so
honestly and A1 will be marked UNRESOLVED, not killed.

## 7. Kill bars (this build task)

- K1 (prereg frozen before implementation): this document committed
  strictly before any G2 source is written. Commit-order self-check
  required.
- K2 (all controls run): R1 (5 seeds), R3 (Arms 1-2), and F-RECFOLD
  (3x5) complete under G2; every falsifier in section 5 evaluated
  and reported. Frozen controls reproduced first (section 4).
- K3 (pure Zag, deterministic): Zag at every stage (authoring,
  building with znc, running, verification via shell tools only).
  Zero Python at every stage, from task start. 3/3 byte-identical
  runs per battery, zero stderr bytes. Zero em/en dash bytes in
  loop documentation (shell-verified with
  worker_snippets/check_no_dash.sh).

## 8. Verdict rule (frozen)

- G2-PASS iff K1-K3 hold AND no falsifier in section 5 fires.
- G2-FAIL otherwise, naming each fired falsifier and the
  measurement that fired it.

Honest scope (frozen): a PASS is bounded-L2 search robustness for
compositional reuse under refutation-seeking IV. Not L3, not
Criterion 0, not a Q4 revival. The G2 policy is generic search
machinery; it does not invent representations.

## 9. Governance

- Prereg-first; no implementation before this commit.
- Frozen base sources are never edited; work happens on copies in
  beam_g2/.
- The contaminated research paper is not touched.
- Commits local, owned pathspec only
  (docs/lab/research-lead/overnight-20260928/beam_g2/).
- Other workers' files are not touched.
- If a git lock is encountered, wait; never remove a live lock.
