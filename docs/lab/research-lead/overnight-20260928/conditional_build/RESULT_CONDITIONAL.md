# Conditional-First Build: Result

Date: 2026-09-30. Builder prereg: CONDITIONAL-PREREG-FROZEN,
committed 1981c00ea before any implementation (K1 satisfied).

## Verdict

CONDITIONAL-FAIL

Failing bar: P4(c). FREC instance 3 best true-correct is 32/64,
below the frozen bar of 40/64. All other bars pass. Partial passes
are diagnostics, never a pass.

## Bar-by-bar

- K1 (prereg commit strictly precedes implementation): PASS.
  Prereg at 1981c00ea; implementation in r3c.zag, r1c.zag,
  frcc.zag written and committed after.
- K2 (all runs complete): PASS. Nine runs, three per battery.
- K3 (pure Zag, 3/3 byte-identical, zero stderr): PASS.
  R3 md5 73170f1c6941ca944417babc93e48d67 (3/3).
  R1 md5 47ce2610a1fdcd55feba2f14b760152f (3/3).
  FREC md5 39117dc8d8e9eab35ad4e550f53a928f (3/3).
  All nine .err files zero bytes. Zero Python at every stage.
- P1 (CONDHIT round <= 2): PASS. CONDHIT round=0. The combiner
  proposed a COND with the target E signature in its first round.
- P2 (A2-PASS == 1): PASS. A2 REUSE_IV 4 true=64/64 HAS_D=1;
  A2 SCRATCH_IV 24 true=52/64. Reuse solves the conditional
  target exactly with fewer interventions than scratch.
- P3 (DROUND < 4): PASS. P1-BASE DROUND=1 (frozen baseline 4).
  The conditional machinery also accelerates the second
  compositional target, so this is not a one-target trick.
- P4(a) (A1-PASS == 1): PASS. A1 REUSE_IV 0 true=64/64.
- P4(b) (R1 PASS_SEEDS >= 0/5): PASS. Observed 1/5
  (seed 84044: 64/64). Frozen was 0/5. Improvement, not
  regression. Per-seed true: 40, 40, 56, 64, 48.
- P4(c) (FREC bests >= frozen): FAIL.
  I1 best 49/64 >= 46/64 PASS.
  I2 best 63/64 >= 63/64 PASS.
  I3 best 32/64 < 40/64 FAIL.
- F-CASE (six audits): none fire. PASS.
  String audit clean on added/modified lines of all three files
  (diff-scoped grep for Y4/Y5/y4/y5/710202/fam8/F-PARCOND/
  710101-710299: zero matches). Gate, enumeration, semantics,
  and tax audits verified by code review: the combiner iterates
  all beam members in beam order with no identity filter, the
  COND evaluator is the generic multiplexer from child truth
  tables, tax stays 200/opc with the uniform opc rule.

## Diagnosis of the P4(c) failure

The COND mechanism works as designed on the primary task: it
proposes the target conditional in round 0 and solves R3 Arm 2.
But the added expressivity regresses FREC instance 3.

Mechanism: in FREC phase 1 (32 passive evidence rows, no
interventions), the BAP licenses COND triples that perfectly fit
the observed rows (32/32 evidence fit at modest opc). These
proposals dominate the 32-wide beam on evidence score and displace
the binary candidates the frozen search selected. The displaced
candidates generalized better (frozen I3 best 40/64 true); the
COND-dominated beam converges on programs with perfect evidence
fit but 32/64 true accuracy on all five I3 seeds.

In short: conditional-first search overfits the evidence on I3.
The tax (200/opc) does not penalize the COND enough when it
achieves perfect evidence fit. This is a real behavioral
regression on a frozen control, exactly what the P4 bar exists
to catch.

## Scope

Bounded-L2 search-architecture experiment. No L3 claim, no
Criterion 0 claim. COND is researcher-supplied, like AND/OR/XOR/
NOT. The mechanism repairs the R3 Arm 2 compositional bottleneck
(P2) and generalizes to a second target (P3), but fails the
no-regression bar on FREC I3. It does not invent conditionals,
does not choose its own representation, and does not revise its
alphabet.

## Artifacts

- r3c.zag, r1c.zag, frcc.zag (mechanism sources, pure Zag)
- r3c_bin, r1c_bin, frcc_bin (pinned znc builds)
- COND_R3_1/2/3.txt, COND_R1_1/2/3.txt, COND_FRC_1/2/3.txt
  (raw outputs, 3/3 byte-identical per battery)
- Corresponding .err files (all zero bytes)
- PREREG_CONDITIONAL.md (frozen prereg)
- r3_base.zag, BASE_1/2/3.txt (measurement baseline)

CONDITIONAL-FAIL.
