# REPORT: xdomain_causal_interv -- Third Domain Pair (Causal to Intervention)

## Verdict: XDOMAIN-CAUSAL-INTERV-COMPLETE. All 9 frozen kill bars PASS.

## Mission

Test H1 (learned typed contracts) and H2 (value-level function
composition) on a THIRD domain pair with UNMODIFIED mechanism logic,
to establish a generality pattern.

Prior:
- Chain to count: H1 PASS, H2 PASS.
- Arithmetic to planning: H1 PASS, H2 PASS (mechanism logic unmodified).
- This work: causal model to intervention planning. H1 PASS, H2 PASS.

## Domain

X: causal model. Facts (s,91,o): "s causes o". Behavior: walk r=91
to endpoint (predict final outcome). X(11)=13, X(21)=23.

Y: intervention planning. Facts (o,92,a): "outcome o needs action a".
Behavior: find_obj(v,92). Y(13)=101, Y(23)=102.

No paired X+Y training. No hint. No task label. No researcher mapping.
No CAUSAL_TO_INTERVENTION template.

Sealed Z: (11,93)->101. "Given initial state 11, what intervention?"
Requires X(11)=13 then Y(13)=101.

Z2/ZPRIME: (21,93)->102. X(21)=23 then Y(23)=102.

## H1 results (ci_h1.zag, mechanism UNMODIFIED from xt.zag)

3/3 byte-identical, sha256
`1c463c4e5d5aa571cc1a161d6421d68dee79923ce54aad9689d7a40f308c9d5b`.

Learned signatures (from probe observations only, zero literals):
- X: 1->1 (NODE->NODE). Correct.
- Y: 1->2 (NODE->NUM). Correct.
- D1: 1->1. Correct.
- D2: 1->2. Correct.

TREAT:
- Singles: Y(11)=-1 wrong, D2(11)=1 wrong. (X, D1 skipped by type.)
- Pairs: (X,Y): X(11)=13, Y(13)=101. Correct.
- Z-COMP z=4 a=0 b=1. Z-SIG 1->2.
- ARM-RESULT PASS tries=3.

Z2:
- Singles: Y(21)=-1, D2(21)=1 wrong; Z(21)=102 correct.
- Z-SINGLE m=4. tries=3 <= 4. Z2-RESULT PASS.

NOTYPE:
- 4 singles + 2 pairs = 6 tries > 3. Contract prunes search.

ABL-X / ABL-Y / FRESH: all Z-FAIL as expected.

## H2 results (ci_h2.zag, mechanism logic UNMODIFIED from vc_patch.zag)

3/3 byte-identical, sha256
`1484d8730ab8e282e6d8c16fb412793f58cbef1af44de8c43f3b2613e34f9e98`.

Modes: 1=CAUSAL, 2=INTERVENE (discovered pair, not given).
Stage2 requires learned Y as capability evidence.

TREAT:
- (1,1): causal(11)=13, causal(13)=13. Not 101.
- (1,2): causal(11)=13, interv(13)=101. Correct.
- VC-COMPOSE ok m1=1 m2=2 cm=2. ARM-RESULT PASS.

ZPRIME: (21,93)->102 via (1,2): causal(21)=23, interv(23)=102. PASS.

ABL-X: causal stage fails (no X); interv(11)=-1 then stages fail.
VC-COMPOSE fail. PASS-expected-fail.

ABL-Y: interv stage refuses (no Y capability); (1,1) gives 13 not 101.
VC-COMPOSE fail. PASS-expected-fail.

FRESH / NO-VC: fail as expected. TOTAL 6/6.

## Kill bars

- K1 H1-SOLVE: PASS. Z-COMP z=4 a=0 b=1, tries=3.
- K2 H1-CAUSAL: PASS. ABL-X, ABL-Y, FRESH all Z-FAIL.
- K3 H1-CONTRACT: PASS. NOTYPE 6 tries > TREAT 3 tries.
- K4 H1-REUSE: PASS. Z2 via Z direct, 3 tries <= 4.
- K5 H2-SOLVE: PASS. VC-COMPOSE ok m1=1 m2=2, v1=13 observed.
- K6 H2-CAUSAL: PASS. ABL-X, ABL-Y, FRESH, NO-VC all -2.
- K7 H2-REUSE: PASS. ZPRIME ans=102 via re-executed pipeline.
- K8 DETERMINISM: PASS. 3/3 byte-identical both binaries.
- K9 NO-TEMPLATE: PASS. Grep audit: only comments declaring absence.

## Why this matters

Three structurally different domain pairs now solved by BOTH H1 and H2
with unmodified mechanism logic:
1. navigation x aggregation (chain to count)
2. arithmetic x planning
3. causal model x intervention planning

The mechanisms are not domain-pair templates. H1's typed contracts
and H2's value-level composition are general cross-domain principles:
learned structures expose input/output behavior, and composition
follows from type compatibility (H1) or value passing (H2).

## Honest boundaries

- Behavior induction assumed as prior learning (same as prior waves).
- H1 kinds binary NODE/NUM from syntactic probe.
- H2 modes (CAUSAL, INTERVENE) researcher-defined; pair discovered.
- Expected used for final verification.
- One pair per wave; three pairs total across waves.
- Small distractor set.

## Architecture accounting

- ci_h1.zag: ~330 lines (mechanism identical to xt.zag).
- ci_h2.zag: ~200 lines (mechanism logic identical to vc_patch.zag).
- 0 modes, 0 bridges, 0 handlers, 0 new semantic cases.
- Frozen TNN-2 untouched (both standalone).

## Toolchain

Safebin PATH throughout. `which python3 python` empty (NAMECHECK
Step 0). Pinned znc, exit 0 both. Zero em/en dashes byte-verified.
Committed locally, nothing pushed.

## Deliverables

- PREREG.md (frozen c22be7faa, strictly before implementation)
- NAMECHECK.md (Step 0 guard)
- REPORT.md (this file)
- ci_h1.zag, ci_h1_bin, ci_h1_compile.txt, ci_h1_run1/2/3.txt
- ci_h2.zag, ci_h2_bin, ci_h2_compile.txt, ci_h2_run1/2/3.txt
