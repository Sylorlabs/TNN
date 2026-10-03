# PREREG: xdomain_causal_interv -- Cross-Domain Generality, Third Pair (Causal to Intervention)

## Status

FROZEN before implementation. This file is committed alone before any
mechanism code is written.

## Mission

Test H1 (learned typed contracts) and H2 (value-level function
composition) on a THIRD domain pair, with UNMODIFIED mechanism logic,
to establish a generality pattern.

Prior results:
- Chain to count: H1 PASS, H2 PASS.
- Arithmetic to planning: H1 PASS, H2 PASS (mechanism logic unmodified).
- This work: causal model to intervention planning.

## Domain design

No paired X+Y training. No "combine" hint. No task label.
No researcher-authored mapping between the domains.
No CAUSAL_TO_INTERVENTION template.

### World facts (r=91 causal, r=92 intervention)

Causal chains (r=91, "causes"):
- (11,91,12), (12,91,13): state 11 leads to 12 leads to 13.
- (21,91,22), (22,91,23): state 21 leads to 22 leads to 23.

Intervention links (r=92, "is addressed by"):
- (13,92,101): bad outcome 13 needs intervention 101.
- (23,92,102), (23,92,103): outcome 23 needs 102 (first) or 103.

Kinds via probe_kind (H1): 11,12,13,21,22,23 appear as subjects
-> NODE (1). 101,102,103 never appear as subjects -> NUM (2).

### X: causal model (learned independently)

Behavior: walk r=91 to endpoint (predict final outcome).
- X(11)=13, X(21)=23, X(12)=13.
- Learned signature: NODE->NODE.

### Y: intervention planning (learned independently)

Behavior: find_obj(v,92) (look up intervention for outcome).
- Y(13)=101, Y(23)=102.
- Learned signature: NODE->NUM.

### Distractors

- D1: identity. D1(v)=v. Signature NODE->NODE.
- D2: count r=91 outgoing. D2(11)=1, D2(13)=0. Signature NODE->NUM.

### Sealed Z

Z = (11,93) -> 101. "Given initial state 11, what intervention is needed?"
Requires: X(11)=13 (causal prediction), then Y(13)=101 (intervention).
- kin = probe_kind(11) = NODE. kout = probe_kind(101) = NUM.

### Z2 (reuse)

Z2 = (21,93) -> 102. Via Z direct application: X(21)=23, Y(23)=102.

## H1 mechanism (UNMODIFIED from xdomain_typed/xt.zag)

probe_kind, record_obs, finalize_sig, solve_z (type-directed single then
pair search), promote_comp. Only the world facts, relation IDs in
exec_map behaviors, and teaching queries change. The composition logic
is byte-identical in structure.

Expected H1 TREAT trace:
- Singles: Y(11)=-1 wrong, D2(11)=1 wrong. (X, D1 skipped by type.)
- Pairs: (X,Y): X(11)=13, Y(13)=101. Correct.
- Total: 3 tries. Z-COMP z=4 a=0 b=1.

Expected H1 Z2 trace:
- Singles: Y(21)=-1 wrong, D2(21)=1 wrong, Z(21)=102 correct.
- Total: 3 tries (<=4).

Expected H1 NOTYPE trace:
- Singles: X(11)=13, Y(11)=-1, D1(11)=11, D2(11)=1. All wrong. 4 tries.
- Pairs: (X,X): 13 wrong. (X,Y): 101 correct.
- Total: 6 tries > 3.

## H2 mechanism (UNMODIFIED logic from xdomain_value/vc_patch.zag)

Value-level composition: try ordered mode pairs, stage1 executes,
pass intermediate VALUE to stage2, verify against expected, promote.
Modes become CAUSAL (1) and INTERVENE (2) instead of CHAIN/COUNT.
The ordered-pair search, value passing, and two-stage verification
are preserved. Stage2 requires learned Y as capability evidence.

Expected H2 TREAT trace:
- (1,1): causal(11)=13, causal(13)=13. Not 101.
- (1,2): causal(11)=13, interv(13)=101. Correct. Promote.
- ABL-X: causal stage fails or wrong; all pairs fail.
- ABL-Y: interv stage refuses (no learned Y); all pairs fail.
- FRESH: no MAPs; fail.
- NO-VC: mechanism disabled; fail.

## Kill bars (frozen)

- K1 H1-SOLVE: H1 TREAT solves Z=(11,93)->101 via (X,Y) composite.
  Correct provenance (a=0,b=1). PASS iff ARM-RESULT PASS.
- K2 H1-CAUSAL: H1 ABL-X, ABL-Y, FRESH all fail (t<=0). PASS iff all
  three show PASS-expected-fail.
- K3 H1-CONTRACT: H1 NOTYPE solves but with strictly more tries than
  TREAT (t_notype > t_treat). PASS iff t_notype > t_treat.
- K4 H1-REUSE: H1 Z2=(21,93)->102 solved via Z direct, tries <= 4.
  PASS iff Z2-RESULT PASS.
- K5 H2-SOLVE: H2 TREAT solves Z via (CAUSAL,INTERVENE), v1=13
  observed, composite promoted. PASS iff VC-COMPOSE ok.
- K6 H2-CAUSAL: H2 ABL-X, ABL-Y, FRESH, NO-VC all return -2.
  PASS iff all four fail as expected.
- K7 H2-REUSE: H2 Z' on new subject via composite or re-execution.
  PASS iff ans correct.
- K8 DETERMINISM: 3/3 byte-identical runs for both H1 and H2 binaries.
  PASS iff sha256 match across 3 runs each.
- K9 NO-TEMPLATE: No CAUSAL_TO_INTERVENTION, CAUSAL_INTERVENE, or
  domain-pair literals in mechanism code. Grep audit. PASS iff clean.

Verdict XDOMAIN-CAUSAL-INTERV-COMPLETE requires K1-K9 all PASS.

## Honest boundaries (declared before implementation)

- Behavior induction (how X/Y got behaviors) assumed as prior learning.
- H1 kinds are binary NODE/NUM from syntactic probe.
- H2 modes (CAUSAL, INTERVENE) are researcher-defined; the pair is
  discovered by search, not given.
- Expected answer used for final verification (same as prior waves).
- One cross-domain pair (causal x intervention).
- Small distractor set (2).

## Deliverables

- PREREG.md (this file, frozen first)
- NAMECHECK.md (Step 0 guard)
- REPORT.md (results, kill bars, honest analysis)
- ci_h1.zag (H1 standalone, mechanism unmodified)
- ci_h2.zag (H2 standalone, mechanism logic unmodified)
- ci_h1_bin, ci_h2_bin (pinned znc builds)
- ci_h1_run1/2/3.txt, ci_h2_run1/2/3.txt (3/3 byte-identical)
- compile logs
