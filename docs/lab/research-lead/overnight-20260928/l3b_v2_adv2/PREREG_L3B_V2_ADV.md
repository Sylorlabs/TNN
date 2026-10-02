# PREREG: L3B v2 Independent Adversary (FROZEN)

Status: FROZEN. Committed alone before any attack implementation exists.
Lane: docs/lab/research-lead/overnight-20260928/l3b_v2_adv2/
Target: L3B-V2-PASS at 7a1d3265d (prereg 05620eaa2 + addendum 197e2547a).

## 0. Adversarial stance

Assume the v2 claim is false. The v2 claim: growth is generic program-space
search (205-program grammar: atoms VAR/CONST 0..8; ops ADD/MUL/SUB; depth<=2),
and revision is recall via a version archive with per-regime dispatch.
Try to break it: (1) is the 205-enumeration genuinely generic search or a
bigger vocabulary in disguise; (2) can dispatch be fooled; (3) does recall
survive churn; (4) where is the archive boundary.

The mechanism source is copied VERBATIM into the attack file; the harness
asserts the only differences are the replaced main() and the header comment
(function-by-function diff of all non-main functions must be empty), the
interpreter region is sha256-identical to 7a1d3265d, rel_of is absent.

## 1. Attack families (sealed worlds; symbols h0=97,h1=98, ts1=97,ts2=98)

### Family A: depth-3 required (tl2 = n^4)

Grammar analysis (from source): atoms degree <=1; depth-1 programs degree
<=2; depth-2 programs are op(VAR,d1) or SUB(d1,VAR), max degree 3
(MUL(VAR,d1) with d1 degree 2). No 205-program computes n^4 (degree 4).
Hand-checked: no in-grammar program fits (2,16),(3,81),(4,256) exactly
(candidate degree-3 forms through those points need constants/ops outside
the grammar; verified term by term against the 205 table order).

- Learn: n=2,3,4, tl1=n, tl2=n^4 = 16,81,256. allow_create=1, is_learn=1.
- Hidden: n=5,6,7, tl1=n, tl2=625,1296,2401. allow_create=0, tally=1.
  (Base predictor provably fails: best_cand returns (1,1,1), c0=1 != n.)

Frozen predictions:
- A-NOSEARCH: output contains TRACE-NO-GROWTH with why=nosearch2.
- A-HIDDEN: hidden tally = 0/3.
- A-CREATE: creates (cnt3) = 0 in Family A.
- A-BREAK-CONDITION: hidden = 3/3. A correct n^4 solution is impossible via
  the 205 table (degree argument above); 3/3 would prove smuggled semantics
  (template-widening in disguise) -> L3B-V2-ADV-BREAK.
- A-BOUNDED-CONDITION: nosearch + 0/3, or a coincidental table-program fit
  that still scores 0/3 on hidden (honest wrong guess, still bounded).

### Family B: constant outside 0..8 (tl2 = n+12)

Grammar analysis: in-grammar programs computing n+c exactly need c<=8
((A,V,Ck) k<=8; constant-yielding SUB forms give k<=8; MUL(VAR,C1)=n).
Provable: max p(1) over in-grammar programs is 10 ((A,V,(A,V,C8))),
but the window needs p(1)=13. No exact fit is possible at all.

- Learn: n=1,2,3, tl1=n, tl2=13,14,15. allow_create=1, is_learn=1.
- Hidden: n=4,5,6, tl1=n, tl2=16,17,18. allow_create=0, tally=1.

Frozen predictions:
- B-NOSEARCH: TRACE-NO-GROWTH why=nosearch2.
- B-HIDDEN: 0/3. B-CREATE: creates = 0.
- B-BREAK-CONDITION: hidden = 3/3 -> BREAK (smuggled constant).
- B-BOUNDED-CONDITION: nosearch + 0/3.

### Family C: ambiguous dispatch (first-match rule under attack)

Laws (all constructible): R1 tl2=2n key (A,V,V); R2 tl2=n+4 key (A,V,C4);
R3p tl2=n+6 key (A,V,C6). tl1=n (VAR) throughout.
At n=11,12,13 all three laws pairwise disagree (22/15/17, 24/16/18,
26/17/19), so no accidental dispatch during training.

- P1: R1 at n=11,12,13 -> v1 created, ser=1, key (V,(A,V,V)).
- P2: R2 at n=11,12,13 -> v2 created, ser=2, key (V,(A,V,C4)).
- P3: R3p at n=11,12,13 -> v3 created, ser=3, key (V,(A,V,C6)).
  (Each phase: 3 consecutive failures, clean 3-window, search finds the
  first exact fit: (A,V,V), (A,V,C4), (A,V,C6); archive key-miss -> CREATE.)
- Reactivation: n=21 under R2 law, tl=(21,25). Active v3 predicts 27 ->
  fail. try_dispatch scans a=0 (v1: 42!=25), a=1 (v2: 21,25 match) ->
  dispatch. Predicted signature: TRACE-DISPATCH from=3 to=2 on=21.
- Ambiguous probe: n=6 under R3p law, tl=(6,12). Active v2 predicts 10 ->
  fail. try_dispatch: a=0 (v1: 6,12 match) -> WRONG version picked by the
  first-match rule (observation came from R3p's law, i.e. v3's regime).
  Predicted signature: TRACE-DISPATCH from=2 to=1 on=6.
- Correction: n=7 under R3p law, tl=(7,13). Active v1 predicts 14 -> fail.
  try_dispatch: a=0 skip (active), a=1 (v2: 11!=13), a=2 (v3: 7,13 match)
  -> dispatch. Predicted signature: TRACE-DISPATCH from=1 to=3 on=7.
- Stability: n=8,9 under R3p law -> ok under v3.

Frozen predictions:
- C-CREATE: creates = 3 (no 4th version for the ambiguous point).
- C-DISP: dispatches (cnt4) = 3. C-RECALL: cnt5=3 and cnt6=3
  (zero-construction recalls, lgn unchanged across each dispatch).
- C-SIG1/2/3: the three grep signatures above, verbatim.
- C-BREAK-CONDITION: dispatch recalls a version never constructed, or a
  4th version is created for the ambiguous point (churn), or the r1/r2
  node ids in a dispatch trace do not equal the creation-time ids
  (faked recall evidence) -> BREAK.
- C-BOUNDED-CONDITION: exactly the wrong-pick-then-correct signature.
  Interpretation: dispatch CAN be fooled by ambiguous observations; the
  first-match rule is a bounded honest limitation, not a bug.

### Family D: 8-version churn + revisit (recall under pressure)

Laws: R1 2n (A,V,V); R2 n+4 (A,V,C4); R3 n+6 (A,V,C6); R4 n-2 (S,V,C2);
R5 3n (M,V,C3); R6 n^2 (M,V,V); R7 2n+1 (A,V,(A,V,C1)); R8 n+1 (A,V,C1).
At n=11,12,13 all eight laws pairwise disagree
(22,15,17,9,33,121,23,12 / 24,16,18,10,36,144,25,13 /
26,17,19,11,39,169,27,14), so training never accidentally dispatches.
First-exact-fit order verified per law against the 205 table order
(atoms, then d1 ADD/MUL/SUB, then depth-2): (A,V,V), (A,V,C4), (A,V,C6),
(S,V,C2), (M,V,C3), (M,V,V), (A,V,(A,V,C1)), (A,V,C1).

- P1..P8: each law at n=11,12,13 (allow_create=1, is_learn=1).
- Revisit R1: n=21 tl=(21,42): active v8 predicts 22 -> fail;
  try_dispatch scans a=0..6 (no match: laws disagree at 21), a=0 (v1:
  21,42 match) -> dispatch. Predicted: TRACE-DISPATCH from=8 to=1 on=21,
  r1/r2 equal v1's creation-time node ids (recallok).
- n=22,23 under R1 -> ok (tally=1).

Frozen predictions:
- D-CREATE: creates = 8. D-DISP: dispatches = 1.
- D-RECALL: cnt5=1 and cnt6=1.
- D-REVISIT: revisit tally = 3/3; creates stays 8 (no rebuild).
- D-KEYS: the eight TRACE-CREATE lines carry exactly the predicted keys.
- D-BREAK-CONDITION: revisit creates a 9th version (rebuild instead of
  recall), or dispatches to the wrong version, or recall node ids mismatch
  -> BREAK.
- D-BOUNDED-CONDITION: creates=8, one recall dispatch with node-id
  equality, 3/3 revisit.

### Family E: 9th version (archive boundary probe; same lifetime as D)

- R9: tl2 = n+7, key (A,V,C7), at n=11,12,13. Active v1 fails (22!=18);
  no archived version explains (18/19/20 not in {22,15,17,9,33,121,23,12}
/ {24,16,18...} wait: R2(12)=16, R3(11)=17; 18,19,20 absent from all
  eight laws at 11,12,13) -> 3 consecutive failures -> do_fire with
  vn=8. Source audit: do_fire has NO bounds check on vn; archive arrays
  are 8 entries (av_p1/av_p2/av_l1/av_l2/av_ser ia(8); av_k1/av_k2 384
  bytes = 8*48). The write goes out of bounds.

Frozen prediction:
- E-BOUNDARY: the 9th CREATE attempt executes with vn=8, writing past the
  archive arrays. Expected observable: abnormal termination (e.g.
  segfault) or corrupted output after the attempt; the termination
  signature (exit code + output tail) is identical across 3 runs.
- E is a ROBUSTNESS BOUNDARY finding, not a BREAK/BOUNDED input for the
  search claim: fix required before any integration. If the run instead
  exits 0 with sane output, record E-UNEXPECTED and investigate (latent
  heap overflow either way).

## 2. Verdict mapping

- L3B-V2-ADV-BREAK: any BREAK-CONDITION fires in A, B, C, or D.
- L3B-V2-ADV-BOUNDED: all of A, B, C, D follow their BOUNDED-CONDITIONs
  (E reported separately as a boundary finding either way).
- L3B-V2-ADV-FAIL: any frozen PRIMARY prediction mismatches 3/3 for a
  reason other than a BREAK condition (hand-derivation error; honest).

Primary predictions are the lettered items (A-NOSEARCH/HIDDEN/CREATE,
B-*, C-CREATE/DISP/RECALL/SIG1-3, D-CREATE/DISP/RECALL/REVISIT/KEYS,
E-BOUNDARY). Secondary diagnostics (raw traces) are informative only.

## 3. Kill bars

K1: this prereg is committed ALONE before any attack implementation;
verified with git merge-base --is-ancestor at commit time.
K2: every primary prediction matches on 3/3 byte-identical runs;
verdict follows the frozen mapping above.
K3: pure Zag + shell only; zero Python at every step; u8-backed cells
only; no em dashes (shell-only check_no_dash.sh); contaminated paper
untouched (empty diff); explicit pathspecs; live index.lock waited on,
never removed.

## 5. ONE-SYSTEM RULE compliance (standing directive 2026-09-30)

This work is an adversarial attack, not a capability build. Capability-source
accounting, recorded here and to be confirmed in the results:

- Cognition source lines added: 0 (mechanism functions copied verbatim;
  harness asserts non-main functions are byte-identical to 7a1d3265d).
- New hardcoded semantic cases: 0. New modes: 0. New bridges: 0.
- New task-specific handlers: 0. New learner-state structures: 0.
- The sealed worlds (Families A-E) are test fixtures in the attack main,
  not cognitive machinery; they are never proposed for adoption.

Lane ruling applied: "L3B adversary continues (if the constructor is a
finite menu, redesign toward incremental construction, never expand the
menu)". Families A and B probe exactly whether the 205-enumeration is a
finite menu with honest boundaries. If the verdict is BOUNDED, the
recommended next step is redesign toward incremental construction, never
grammar expansion.

## 6. What would falsify the BOUNDED verdict

A hidden 3/3 on Family A or B (a correct depth-3 or out-of-range-constant
solution appearing from the 205-enumeration), or a dispatch recall of a
never-constructed version, or a rebuild where recall was predicted.
Any of these -> BREAK: the enumeration would be a bigger vocabulary in
disguise, or dispatch evidence would be faked.
