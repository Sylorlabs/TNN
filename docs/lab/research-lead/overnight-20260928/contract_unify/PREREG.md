# PREREG: CONTRACT-UNIFICATION (C418)

Status: PREREG-FROZEN. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/contract_unify/` only.
Worker: CONTRACT-UNIFICATION worker (subagent, 2026-10-03).
Parent mandate: implement the COMPRESSION-AUDIT's top candidate (C418):
one learned-contract mechanism unifying GEN's contract core, LCONT, and FC.

Design source: `compression_audit/COMPRESSION_AUDIT_MECHANISMS.md` sec 4
(read-only). Frozen scenario data below is copied from the committed
lanes `contract_drift_detect` (REPORT.md, PREREG.md) and
`formal_constraints` (REPORT.md, PREREG.md); nothing was re-run.

## 1. Question

Can ONE learned-contract mechanism reproduce LCONT's drift-detection and
revision verdicts AND FC's constrained-generation verdicts, with no
separate contract machinery and no per-scenario branches? The mechanism:
a contract is (consumes, produces, constraint-clauses, confidence);
operations are induct, check, grow, invalidate, revise.

## 2. Frozen unified module design

### 2.1 Contract representation (all integer, opaque)

A contract held in learner state:
- consumes: NFIELDS (input arity).
- constraint-clauses: list of (field, xform, k, lo, hi, active, dc).
  xform 0 = identity, 1 = integer divide by k, 2 = remainder mod k.
  Semantics: xform_k(input[field]) in [lo,hi].
  This clause ABI is taken verbatim from FC's frozen registry
  (formal_constraints/fc_main.zag reg_clause/reg_check).
- produces: judgment semantics. u_check returns 1 iff at least one
  active clause exists and every active clause holds; 0 otherwise.
  Empty active set judges 0 (reject/abstain). The CALLER decides what
  the judgment means: the drift harness treats it as a commitment to
  verify; the grammar composer treats it as admission. One check.
- confidence: per-clause disconfirmation counter dc; contract-level
  consecutive-failure run C_FAIL_RUN.

### 2.2 Operations (frozen signatures, integer only)

- u_induct(st, cbase): from the judgment table (JT_NF, JT_NA accepts,
  JT_NR rejects; each item (len, v0..v5), opaque integers) build the
  clause set. Minimal-commitment search: increasing cardinality (1,
  then 2); accept range [mn,mx] per (field, feature) measured over the
  accepts; a set is valid iff its conjunction rejects every reject
  whose len == NFIELDS (other lengths are separated by the nfields
  check, as in FC's frozen design). Among valid sets prefer FEWER
  clauses, then MAXIMAL total accept-region width (least committal:
  the contract rules out the least input space consistent with the
  evidence), then lexicographic on (field, xform, k) for determinism.
  Feature library (fixed, domain-neutral, from FC's frozen source):
  identity; div-by-k and mod-by-k for k in {2,4,8,16,32} (11 features).
  Writes the winning set with active=1, dc=0; sets CONTRACT_SET=1,
  NFIELDS, NCLAUSES, C_FIT_ERR (errors of the new set on the table).
  No separator found: no contract (CONTRACT_SET stays 0).
- u_check(st, cbase, nf, f0..f5): 1 iff nf == NFIELDS and at least one
  active clause and every active clause holds; else 0.
- u_grow(st, cbase, f0..f5): for each active clause, widen [lo,hi] to
  include the transformed observed value (GEN-style success recording).
  Implemented; not exercised by the frozen arms (disclosed bound).
- u_invalidate(st, cbase, judgment, consequence): returns ok =
  (judgment == consequence); C_TOTAL++, C_CORRECT += ok. If a contract
  is held: ok resets C_FAIL_RUN to 0 and zeroes active clauses' dc;
  failure increments C_FAIL_RUN and every active clause's dc; a clause
  reaching dc >= 2 is deactivated (retired, permanent until revise;
  U6-style). C_FAIL_RUN >= 3 latches C_REV_REQ = 1 and records
  C_FIRST_DETECT_Q (LCONT-style). Retirement is uniform: it fires in
  every scenario, never exempted (exempting it would be a
  per-scenario branch and fires F3).
- u_revise(st, cbase, enabled): iff C_REV_REQ == 1 and enabled == 1:
  compute C_OLDERR_ON_NEW = errors of the committed clause set on the
  window [REV_PTR, XN); call u_induct on that window (harness loads it
  into the judgment table first); C_REV_COUNT++; C_REV_REQ = 0;
  C_FAIL_RUN = 0; REV_PTR = XN. Else no-op.

The module takes only (state, integer bases, integer params). The
scenario identifier never appears in the module. The two scenario
harnesses (world data, teaching, query loops, composer) are the
experimental apparatus, as in the source lanes; they call the same
module functions.

### 2.3 The one new inductive-bias element (disclosed)

The source mechanisms' biases differ: LCONT's first fit scans
(slot 0..5, threshold 1..3) keeping strictly-fewer errors; FC's Occam
search takes the lexicographically first separating set. The unified
induct uses ONE fixed bias: minimal cardinality, then maximal
accept-region width (minimal commitment), then lexicographic. The width
direction is load-bearing for the drift targets (hand derivation in
sec 4) and was chosen accordingly. F2 tests exactly this: if one fixed
bias cannot cover all frozen inductions, the verdict is PARTIAL.

## 3. Frozen scenario data (copied from source lanes)

### 3.1 Drift scenario S1 (from contract_drift_detect PREREG sec 3)

World 0 law (driver side): label = (s2 >= 2). World 1 law: (s4 >= 2).
Training episodes world 0: E1 (1, 0,0,3,0,0,0, 1), E2 (2, 1,1,0,1,0,0, 0),
E3 (3, 0,0,2,0,1,0, 1), E4 (4, 2,3,1,0,0,1, 0).
Training episodes world 1: E1p (11, 0,0,0,0,3,0, 1), E2p (12, 1,0,1,1,0,1, 0),
E3p (13, 0,0,0,0,2,0, 1), E4p (14, 0,3,0,0,1,0, 0).
Phase 1 queries world 0 (8): P1 (0,0,0,0,0,0) P2 (1,1,2,0,0,0)
P3 (0,0,3,1,2,0) P4 (2,1,1,0,3,1) P5 (0,2,2,0,0,0) P6 (3,0,0,0,1,0)
P7 (1,1,3,0,0,2) P8 (0,0,1,2,0,0). All correct under the true law.
Phase 2 queries world 1 (12): Q1 (0,0,3,0,0,0) Q2 (1,1,0,0,3,0)
Q3 (0,0,1,0,2,1) Q4 (2,0,3,1,0,0) Q5 (0,1,2,0,1,0) Q6 (1,0,0,0,2,0)
Q7 (0,0,3,0,3,1) Q8 (2,2,1,1,0,0) Q9 (0,0,2,0,0,2) Q10 (1,3,0,2,1,0)
Q11 (0,0,3,0,1,0) Q12 (0,1,1,1,3,0).
Phase 3 queries world 1 (8): R1 (1,0,0,0,3,0) R2 (0,2,1,0,0,1)
R3 (0,0,2,1,2,0) R4 (2,0,0,0,1,0) R5 (0,3,3,0,0,0) R6 (1,1,1,1,3,1)
R7 (0,0,0,0,2,2) R8 (3,2,2,0,0,0).

### 3.2 Grammar scenario S2 (from formal_constraints PREREG)

Judgments: accepts (6): [19,87] [119,17] [51,85] [23,113] [81,55]
[117,49]; rejects (6): [19] [19,87,51] [11,47] [35,167] [3,87]
[129,51]. Trial pools (6): (1,3,5,7) (1,1,7,7) (3,5,7,1) (5,5,5,5)
(7,3,1,5) (1,7,3,5). Composer: grammar-blind, 78 candidates per trial
(1-word, 24 2-word, 1 3-word per codec hypothesis h in {8,16,32}),
blind rule minimize (nf,f0,f1,f2), ported verbatim from fc_main.zag
with u_check as the channel filter. Frozen Arm R picks:
(19,87) (17,119) (19,87) (85,85) (19,87) (19,87).

## 4. Arms and frozen predictions (hand-derived)

### Arm D (drift, revision enabled)

Teach E1..E4; load window [0,4) into the judgment table; u_induct.
Hand derivation: single-clause separators over the 11-feature library
include (0,identity,[0,0]), (1,identity,[0,0]), (2,identity,[2,3]),
(2,div2,[1,1]), (2,mod4,[2,3]), (2,mod8,[2,3]), (2,mod16,[2,3]),
(2,mod32,[2,3]) and mod variants on fields 0,1 (all width 0). Maximal
width is 1, attained by the field-2 identity/div/mod family;
lexicographic picks (field=2, xform=identity, k=0, lo=2, hi=3).
Frozen: induced clause (2, identity, [2,3]); C_FIT_ERR = 0.
Phase 1: 8/8 correct, req = 0.
Phase 2 Q1..Q3 under the stale clause: Q1 pred 1 act 0 FAIL (run 1,
dc 1); Q2 pred 0 act 1 FAIL (run 2, dc 2, clause retired); Q3 pred 0
(no active clause) act 1 FAIL (run 3, req latches, FIRST_DETECT_Q=3).
Teach E1p..E4p; u_revise: C_OLDERR_ON_NEW = 2 (stale clause errs on
E1p and E3p); u_induct on [4,8): accepts E1p,E3p, rejects E2p,E4p;
single-clause separators are (4,identity,[2,3]) (width 1),
(4,div2,[1,1]) (width 0), (4,mod4/8/16/32,[2,3]) (width 1);
lexicographic picks (field=4, xform=identity, k=0, lo=2, hi=3).
Frozen: revised clause (4, identity, [2,3]); revcount = 1;
C_FIT_ERR = 0; C_OLDERR_ON_NEW = 2.
Phase 2 remainder Q4..Q12: 9/9 correct. Phase 3: 8/8 correct, req = 0.

### Arm C (drift, revision disabled; control)

Like D through phase 1, world change, then 12 phase-2 queries with
u_revise disabled (enabled = 0). Frozen trace: Q1 FAIL (run 1, dc 1),
Q2 FAIL (run 2, clause retired), Q3 FAIL (pred 0, run 3, req latches
and is held), Q4 ok, Q5 ok, Q6 FAIL, Q7 FAIL, Q8 ok, Q9 ok, Q10 ok,
Q11 ok, Q12 FAIL. Frozen: correct = 6/12, req = 1 held,
revcount = 0, clause never replaced.
NOTE: this differs from the audit's "3/12" and from LCONT's frozen
Arm C. Reason: the unified u_invalidate includes U6-style clause
retraction at 2 consecutive disconfirmations (part of invalidate, not
of revise), which LCONT's original lacked; with revision disabled the
retraction still fires, voiding the stale commitment to pred 0. The
control still demonstrates no adaptation (revcount 0, req held,
6/12 far below 9/12). The deviation is a predicted consequence of
the unification, derived here before implementation.

### Arm G (grammar)

Load the 12 judgments; u_induct. Hand derivation: per the frozen FC
PREREG exhaustive check, the UNIQUE single separating clause is
(field=0, xform=mod, k=32, lo=17, hi=23) (accepts field-0 mod 32 in
{19,23,19,23,17,21}); minimal-commitment search finds it.
Frozen: nfields = 2, nclauses = 1, clause (0, 2, 32, 17, 23).
Composer with u_check filter over the six trials. Frozen picks:
(19,87) (17,119) (19,87) (85,85) (19,87) (19,87), matching frozen
Arm R. A researcher-compiled reference channel runs as a non-bar
replication check (R picks must equal the frozen six).

### Arm N (ablation: induct and revise disabled)

S1: teach E1..E4, no induct (CONTRACT_SET = 0), 8 phase-1 queries,
world change, 12 phase-2 queries with commitment 0 and the monitor
disengaged (no contract). Frozen: req never latches (0 throughout),
revcount = 0, CONTRACT_SET = 0, phase-2 correct = 7/12 (all-zero
commitments; labels 0 on Q1,Q4,Q5,Q8,Q9,Q10,Q11). Drift undetected
because no contract machinery is engaged.
S2: judgments taught, no induct (no clauses); composer runs blind
(no channel consultation, judgments inert). Frozen: all six picks are
the 1-word h=8 candidate (nf=1): (1,11) (1,9) (1,29) (1,45) (1,59)
(1,15); 0/6 well-formed; every pick diverges from Arm R.

## 5. Frozen kill bars

- K1: Arm D reproduces the frozen drift trace: phase-1 8/8 req=0;
  req latches at q=3 (FIRST_DETECT_Q=3); revised clause field=4
  (identity, [2,3]); revcount=1; C_FIT_ERR=0; C_OLDERR_ON_NEW=2;
  phase-2 remainder 9/9; phase-3 8/8 req=0.
- K2: Arm G: induced clause exactly (field=0, xform=2, k=32, lo=17,
  hi=23), nfields=2, nclauses=1; six picks exactly (19,87),
  (17,119), (19,87), (85,85), (19,87), (19,87).
- K3: 3/3 byte-identical runs (single binary runs all arms;
  sha256 equal); stderr empty.
- K4: mechanism hygiene: 0 new modes/bridges/handlers/semantic
  cases/opcodes/edge types beyond the frozen sources' vocabulary;
  opaque integer identifiers only; one contract module serves both
  arms (the scenario identifier never appears in the module;
  verified by grep).
- K5: Arm N fails as predicted: S1 req=0 throughout, revcount=0,
  CONTRACT_SET=0; S2 all six picks nf=1 (diverge from Arm R).
- K6: toolchain guard: safebin PATH, `which python3` and
  `which python` return nothing, pure Zag, pinned znc, shell only
  for build/run/verify.
- K7: zero em/en dash bytes in lane docs.

## 6. Falsification criteria (frozen)

- F1: if LCONT's commitment-vs-consequence loop cannot be expressed
  through the same u_check/u_invalidate the grammar arm uses without
  changing Arm D's verdicts (i.e. the module needs a separate
  commitment path), admission contracts and commitment contracts are
  distinct jobs. Verdict: SUBSUMPTION FAILS; LCONT survives as the
  commitment-contract mechanism.
- F2: if one fixed inductive bias cannot reproduce all three frozen
  inductions ((2,identity,[2,3]), (4,identity,[2,3]),
  (0,mod32,[17,23])) without per-data bias adjustments, induction
  bias is separate machinery. Verdict: PARTIAL (unified checking,
  invalidation, revision; separate induction).
- F3: if either arm needs per-scenario branches inside the unified
  module (module behavior keyed on which scenario's data it sees,
  beyond what the data itself determines), the unification is fake.
  Verdict: FAIL.

A PARTIAL or FAIL here is informative, not a defect: it maps exactly
where the contract jobs diverge.

## 7. Honest bounds (not claimed)

- u_grow is implemented but not exercised by the frozen arms.
- The direction of absorption is open: the test establishes that ONE
  mechanism suffices, not whether GEN's core absorbs LCONT/FC or a
  fresh module replaces all three. Governance decides the landing.
- U6's ledger status is unchanged; only the disconfirmation-counter
  pattern is reused.
- Out of scope: the chain family, L2 adapt operators, BP, DCE, NT,
  LM, INQ, COGOPS body invention.

## 8. Build and run plan (post prereg)

One file `cu_full.zag`: generic machinery (alloc, get32/set32, emit),
the unified contract module (u_induct, u_check, u_grow,
u_invalidate, u_revise), the drift harness, the grammar harness
(composer ported from fc_main.zag), the ablation arm. Build:
`znc cu_full.zag -o cu_bin`. Run 3x, sha256sum compare, stderr must
be empty. Write REPORT.md. Commit with explicit pathspecs.
