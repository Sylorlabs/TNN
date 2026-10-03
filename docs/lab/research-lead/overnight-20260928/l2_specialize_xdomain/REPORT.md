# REPORT: L2-SPECIALIZE-XDOMAIN

Worker: L2 Adaptive Reuse subagent (depth 2/2), 2026-10-02.
Verdict: **L2-SPECIALIZE-XDOMAIN-PASS**. All 8 kill bars PASS, zero
falsifiers, 3/3 byte-identical runs.

## What was tested

Whether a learner holding a GENERAL parametric procedure (arithmetic
AGG fold MAP mG, fold-count recorded as a parameter) and planning
ROUTE MAPs (mD2 2-hop, mB0 3-hop), when asked for a planning total-cost
query it has no native AGG MAP for, SPECIALIZES the general procedure:
derives fold-count candidates {2,3} from its own target-domain MAP
inventory (plan step counts, MAP-id order), trials each with execution
verification (nf=2 fails on every grounding; nf=3 verifies on entry
(50,17,70)), fixes the verified parameters (nf=3, entry rel 17, fold
rels 15/16, discovered link rel 8) into persistent MAP mS with
specialized-from provenance to both mG and mB0, and reuses mS at
2.95x lower per-query search cost than the unspecialized general
procedure.

## Results (frozen numbers, all matched)

ARM-FULL (SPEC_ON=1):
  QA (100,43,12,A): S=44 E=1 term=43 val=12 via=1 (mG home replay)
  QB (50,53,-1,B):  S=48 E=1 term=53 val=-1 via=2 (mB0)
  Q2 (50,73,75,B):  S=2597 E=6 term=73 val=75 via=3 (specialize+promote mS)
  Q2B (same):       S=669 E=3 term=73 val=75 via=3 (mS reuse, no re-specialize)
  Q2C (50,95,36,B): S=1166 E=3 term=95 val=36 via=3 (mS, different values)
  Q2D (50,72,-1,B): S=815 E=3 term=-2 val=-2 via=-1 (mS refuses: fixed arity)
ARM-GENERAL (SPEC_ON=0, per-query re-derivation, no promotion):
  Q2:  S=1977 E=4 term=73 val=75 via=1
  Q2B: S=1977 E=4 term=73 val=75 via=1 (re-derives every query)
ARM-ABLATE-X (mG retired post-QB):
  Q2: S=99 E=2 term=-2 val=-2 via=-1, NM=3, t16=0

Key trace (FULL Q2): XS-STEPS 50,51,52,53 / XS-SRC id=1 /
XS-CANDIDATES 2,3 / XS-TRIAL nf=2 FAIL / XS-TRIAL nf=3 /
XS-ACCEPT re=17 s1=15 s2=16 lr=8 / XS-SPEC-NF 3 /
XS-SPEC-RELS 17,15,16 / XS-SPEC-COSTREL 8 / XS-SPEC-PROMOTE id=3.

## Kill bars

- K1 PASS: qa_via=1, qb_via=2, q2_via=3; line order QA<QB<Q2.
- K2 PASS: general answers Q2B correctly (73,75) at S=1977 > 669:
  general X is correct but suboptimal on target; specialization is
  required for best performance.
- K3 PASS: SPEC_NF=3, trial_fail_n=1, trial_total=2; the learner
  derived candidates {2,3} from its inventory and fixed nf=3 only
  after nf=2 failed verification. No parameter value named in
  xs_learner.zag (K7 audit clean).
- K4 PASS: 669 < 1977 (2.95x). Specialized outperforms general.
- K5 PASS: Q2B (73,75) and Q2C (95,36) via mS (values not baked
  in); Q2D refused (genuine narrowing, no spurious fire).
- K6 PASS: 3/3 byte-identical, sha256
  15affdeb0d6d218a34606c4980745bdcf2cea8e47150bac9c11eadfd6835fb4c.
- K7 PASS: 8/8 frozen grep patterns return 0 hits on
  xs_learner.zag.
- K8 PASS: ablation Q2 fails closed (-2, NM=3, t16=0); nothing
  to specialize without X.

Falsifiers fired: 0. In-Zag: BARS
k1=PASS k2=PASS k3=PASS k4=PASS k5=PASS k8=PASS.

Amortization (informational): FULL total after Q2B = 2597+669 =
3266 vs GEN 1977+1977 = 3954. The one-time specialize
investment (2597) pays off by the 2nd query.

## Amendments (all transparent, pre-verdict)

- AMENDMENT1 (pre-implementation): trial flags de-literalized
  (TRIAL2F/TRIAL3OK named values 2/3 in learner logic ->
  generic TRIAL_FAIL_N/TRIAL_TOTAL); t14 allowed-but-unused.
- AMENDMENT2 (pre-implementation): GEN Q2 E 5->4 (arithmetic);
  saw-spec gate (no re-specialize when a specialized MAP
  exists); stepset save/restore around candidate derivation;
  pipe dispatch on cap.
- AMENDMENT3 (pre-verdict): trial worksheet correction
  (decoy entry discovers s2 via fid 25 -> FAIL-TERM not
  FAIL-DISC2; trials 877/818 -> 903/903; FULL-Q2 2486->2597,
  GEN-Q2/Q2B 1866->1977); ABLATE retire moved post-QB to match
  frozen baseline. F-COUNT caught the slip; mechanics unchanged.

## Non-claims

One world family (arithmetic SUM x plan-cost aggregation),
builder-designed. The SPECIALIZE operator, candidate rule, and
adapter are researcher-supplied generic machinery; the L2 claim
is only that the learner decided WHICH parameters to fix via
inventory-derived candidates and verification trials. No
generality claim beyond the three arms; sealed-adversary
generality is open future work. 0 modes, 0 handlers, 0 new edge
types, pure Zag, safebin toolchain, zero forbidden executables.
Nothing pushed; commits local with explicit pathspec.

## Files

xs_learner.zag (generic machinery, K7-audited), xs_world.zag
(fact table + MAP teaching), xs_driver.zag (3 arms + in-Zag
bars), xs_full.zag (concatenated build input), xs_bin (pinned
znc build), xs_compile.txt, xs_run1/2/3.txt (byte-identical).
