# Q4 Alternative-Explanation Attack Preregistration: F-PARCOND

Date: 2026-09-30. Worker: Q4 Alternative-Explanation Attacker.
Pipeline step: 6 (alternative-explanation attack) for the F-PARCOND claim.
Target claim: "the learner discovered the F-PARCOND structure" (BUILD-PASS 5f56cc491).

## Objective

Attack, do not defend. For each alternative explanation below, either kill
it with evidence or let it stand and downgrade the discovery claim
accordingly. Empirical tests are preregistered here and implemented in
pure Zag after this prereg is committed.

## The six alternative explanations (K1)

### A1. Enumerative search in a 256-behavior space, not learning.

F-PARCOND D depends only on bits 0..2 (x1,x2,x3): 8 input combos, 256
possible boolean behaviors. The beam dedups candidates by 64-bit truth
signature (sigtab), so it can never hold more than 256 behaviorally
distinct candidates relevant to this family. "Discovery" is program
synthesis by enumerative search in a tiny space. The 3860 trace events
are mostly re-derivation of behaviorally equivalent expressions.

Test A1a (ENUM-32): replicate Phase 1 evidence exactly (8 passive with
seed 123456789 + 24 disagreement IVs, identical beam+IV procedure),
then score blind BFS-enumerated signatures (by op depth, no beam, no
guidance) on that evidence. Report: depth of first candidate with full
evidence score AND true 64/64, cumulative distinct signatures explored.
Compare against the beam's 3868 nodes.

Test A1b (ENUM-8): same BFS, scored on the 8 passive samples only.
Report whether the (evidence-score, depth) winner has true 64/64.

Predictions: P-A1a: BFS finds a fully-correct signature at depth <= 3
with < 1000 cumulative distinct signatures (vs beam 3868 nodes).
P-A1b: the passive-only winner does NOT have true 64/64 (the biased
passive set, 6/8 samples with bit5 == output, admits a spurious or
wrong small winner). P-A1b favors the learner; if it fails, the attack
is even stronger.

### A2. Disagreement-driven interventions are decorative at this budget.

The 24 IVs are selected by top-8 beam disagreement. Test RANDIV: exact
copy of phase1 with select_iv replaced by uniform-random selection
among unused x (same seeded LCG, fixed seed, deterministic). Report
BEST line and TRUE correct/64. Prediction P-A2: RANDIV reaches true
64/64 within the 24-round budget, showing the disagreement machinery
adds nothing over random sampling at this budget. (A low-budget
efficiency comparison is noted as follow-up, not tested here.)

### A3. The reuse gap is an evidence-quantity confound.

Baseline E4: learner reuse 64/64 vs MEM-COMP 56/64. But MEM-COMP built
D's table from 8 passive fam-6 samples (6/8 D-combo coverage) while the
learner's D1 came from 32 Phase-1 observations (full 8/8 coverage). Test
FULLMEM: build the D lookup table from the SAME 32 Phase-1 observations
(replicated evidence, seed 123456789), then compose C' = D_table XOR x4
on the replicated fam-6 passive set (seed 555555555) and score /64.
Prediction P-A3: FULLMEM reaches 64/64, tying learner reuse. Then the
64/64-vs-56/64 gap is explained by evidence quantity (32 obs full
coverage vs 8 obs partial coverage), not by representational generality
under composition. Also report the 32-obs combo coverage.

### A4. Researcher-authored search machinery does the work.

Analytic, with code references. The learner contributes no decisions: it
executes a fixed synthesis algorithm. Researcher-authored components:
beam width 32; candidate generation (NOT over singles, all 3 binary ops
over all ordered beam pairs); score = (c*10000)/en - 200*opc (a 200-point
per-op simplicity tax, i.e. MDL-style bias); IV policy (top-8
disagreement); keep bars (margin >= 0.15 over best observable,
opc <= 7, minimality). The A1a candidate-count comparison quantifies
whether beam guidance beats blind enumeration on the same evidence.

### A5. C0-C mislabeled: vocabulary coverage, not adaptation.

Analytic. The adversary family is expressible in the frozen vocabulary
{AND, OR, NOT, XOR} (the set is functionally complete, so ANY boolean
family is). The mechanism underwent zero change between training
families and F-PARCOND. The observed PASS shows the frozen search space
covered the adversary's pick, which is evidence about the vocabulary
choice, not about learner adaptability. A genuine unforeseen-form test
needs a target whose economical form lies outside the frozen vocabulary
(e.g. minimal form exceeding the op budget, or requiring a new operator
concept). Proposed relabel: "vocabulary coverage confirmed."

### A6. The 7-op keep bar is calibrated to the known answer.

Analytic. The target reference is 6 ops; the frozen bar is opc <= 7,
exactly one above. The result reports the 7-op solution as the minimal
found, so with opc <= 6 the run would FAIL (F2 fires). The prereg author
knew ADV_SPEC.md (sealed from the learner only, not from the bar
author) when setting the bar. BUILD-PASS is therefore conditional on a
bar tuned to the known target complexity, weakening it as evidence of
generality.

## Empirical implementation plan

One program, altexp.zag, pure Zag, fixed seeds, deterministic. main runs:

1. ENUM: BFS signature enumeration to depth 6 max. Signature = 64-bit
   truth table over x in 0..63 (same convention as term_sig/node_pred).
   Level 0 = 8 terminals (bit projections x0..x5, const 0, const 1).
   Level d+1 = {NOT s : s in level d} union {s op t : s in level d,
   t in union levels <= d}, op in {AND,OR,XOR}, dedup by (lo,hi).
   Score each new signature on three evidence sets: E-canonical (8 obs,
   one per (x1,x2,x3) combo), E-learner32 (replicated Phase-1 32 obs),
   E-passive8 (replicated 8 passive). For each set report: depth of
   first signature with full evidence score and true 64/64; cumulative
   distinct signatures explored to that point; (score, depth)-winner's
   true accuracy.
2. RANDIV: phase1 copy with random IV selection. Report BEST and TRUE
   lines in the phase1 format.
3. FULLMEM: replicated 32-obs evidence, D table over 8 combos, report
   combo coverage; replicated fam-6 8 passive (seed 555555555);
   C' = D_table[x1,x2,x3] XOR x4; report correct/64.

3/3 byte-identical runs required (same md5), zero stderr, zero Python,
zero em dash bytes.

## Frozen kill bars

- K1: A1..A6 enumerated here, prereg committed alone before any
  implementation. PASS if commit order verified.
- K2: A1a, A1b, A2, A3 executed as preregistered in pure Zag, 3/3
  byte-identical; A4/A5/A6 argued with code references. PASS if all
  empirical tests ran and results are reported honestly including
  predictions that failed.
- K3: per-explanation verdict (SUSTAINED or KILLED) stated plainly,
  plus an overall honest verdict on what the F-PARCOND result does and
  does not establish. PASS if no hedging and no verdict inflation.

## Falsifiers of my attack predictions

- FP-A1a: BFS needs >= 1000 signatures or depth > 3 to identify the
  target on E-learner32. (Weakens A1.)
- FP-A1b: passive-only BFS winner has true 64/64. (Strengthens attack:
  even the IVs were unnecessary.)
- FP-A2: RANDIV fails to reach true 64/64 in 24 rounds. (IV policy does
  real work; A2 dies.)
- FP-A3: FULLMEM < 64/64. (Reuse gap is real; A3 dies.)

## Verdict labels

- ATTACK-COMPLETE: all kill bars pass; per-explanation verdicts delivered.

## Governance

- Prereg committed alone before implementation.
- Owned path: docs/lab/research-lead/overnight-20260928/q4_altexp/ only.
- Pathspec commits, no sweeping.
- No Python at any stage. No em dashes.
