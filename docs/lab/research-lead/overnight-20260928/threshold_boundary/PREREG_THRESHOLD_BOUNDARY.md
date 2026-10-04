# Prereg: Threshold Boundary Mapping (FROZEN)

Date: 2026-09-30. Follow-up attack prereg. Committed alone before any
implementation, family generation, or test execution.

## Target

The conditional-threshold mechanism at commit d0d296650
(THRESHOLD-PASS), reproduced byte-identical at 07785ac78, attacked at
REDTEAM-THRESHOLD-BREAK (attack prereg 15982381c, attack files in
fd31db230, result: Family A BREAK, Family B SURVIVE-THIS-ROUND).

REDTEAM-THRESHOLD-BREAK established: the Tier-2 pass is unreachable
under beam selection pressure because a discriminative condition
(C = (x1 AND x2), 50% target-predictive, score 4800) is culled after
one round, while the persistence gate needs it in beam AND pbeam
(two consecutive survivals). The combiner logic was never reached.
The "tiered" characterization is retired; THRESHOLD-PASS stands as a
Tier-1 recalibration only.

This follow-up maps the exact boundary: WHERE does Tier-2 break,
and where (if anywhere) does it hold?

## Charge

Two precise questions left open by REDTEAM-THRESHOLD-BREAK:

1. A2: If the selection-vs-persistence conflict is removed (the
Tier-2 condition C is ALSO target-predictive, so it survives beam
culling), does the Tier-2 pass then FIRE, or does a second gate
block it? This tests the combiner logic in isolation.

2. B2: B1 survived via D3, a "lucky" distractor supporting an
equivalent solution (HAS_D=0). With ONLY non-equivalent distractors
(D1, D2), does the mechanism find the true D, or does the reuse
criterion fail honestly?

## Attack Family A2: target-predictive Tier-2 condition

New sealed family fam 10. Truth function identical to fam 9:

E10 = (C AND Y4) OR ((NOT C) AND Y5), C = (x1 AND x2),
Y4 = bit 3, Y5 = bit 4.

Reference implementation (Zag semantics, also the runtime check):

```
if(fam==10){
  let x1:i32=(x>>0)&1;
  let x2:i32=(x>>1)&1;
  let y4:i32=(x>>3)&1;
  let y5:i32=(x>>4)&1;
  let c:i32=x1 & x2;
  let nc:i32=c ^ 1;
  let r:i32=(c & y4) | (nc & y5);
  return r;
}
```

The family differs from fam 9 ONLY in the frozen evidence. The
evidence is chosen so C is target-predictive (survives selection)
while exact slice agreement and the Tier-2 min slice still hold.

### Frozen evidence (16 rows, no RNG)

Explicit (x, y=E10(x)) pairs:

(11,1), (15,1), (27,1), (3,0),
(0,0), (1,0), (2,0), (4,0), (5,0), (6,0),
(8,0), (9,0), (10,0), (12,0), (13,0), (14,0)

Verification by hand: C=(x1&x2)=1 exactly on {11,15,27,3}
(all are 3 mod 4; no other row is). On C=1 rows target=Y4=bit3:
11->1, 15->1, 27->1, 3->0. On C=0 rows target=Y5=bit4=0
(all twelve rows are <16). So the table above is exact.

The driver asserts sealed(10,x)==y for all 16 rows at startup and
reports EVIDENCE-MISMATCH if any row disagrees (a mismatch voids
the run; it does not count as a mechanism result).

### Why this evidence

- Tier-2 min slice: en=16, max(4,16/8)=4. C=1 on 4 rows, C=0 on
  12 rows. Both meet it.
- Exact slice agreement: on C=1 rows target=Y4 exactly; on C=0
  rows target=Y5 exactly. The Tier-2 combiner's arm condition is
  satisfiable by construction.
- C matches target on 15/16 rows (misses only x=3). Score:
  15*625 - 200*1 = 9175. Analytical prediction: C is the
  top-scoring built node in round 0 (all 8 terminals score at most
  8750; no pairwise node reaches 16/16 on this evidence, shown
  below), so C survives selection every round.
- No pairwise (opc=1) node reaches 16/16: E10 is 1 exactly on
  {11,15,27} = (x1&x2&x4) on this evidence, a 3-input conjunction;
  excluding x=3 (where C=1 but target=0) requires bit 3, so any
  exact node needs at least 3 inputs (opc>=2, built round>=1).
- Y5 (bit4): 14/16, score 8750. Predicted to survive in beam/pbeam.
- Y4 (bit3): 10/16, score 6250. Marginal for top-32; the
  extended D1 diagnostic reports its pbeam presence explicitly.
  If Y4 is absent from pbeam, the Tier-2 pass cannot build the
  true COND, which itself maps the boundary (the gate needs the
  condition AND both arms to survive selection).

### Protocol A2

Modeled exactly on A1-FAIR: initialize beam with 8 terminals (no
library term), load the 16 frozen rows, run 24x beam_extend_round
(mechanism functions copied verbatim from d0d296650, unmodified),
no interventions. hitbuf target = E10 full-64 signature.

Read-only diagnostics (do not affect search):
- D1: per round, kind-1 C-signature node in beam? In pbeam?
  (C signature from c_sig.)
- D1b (new): per round, Y4 terminal in pbeam? Y5 terminal in
  pbeam? (Terminal signatures computed at runtime; kind 0.)
- D2: CONDHIT round from hitbuf, or -1.
- D3: post-run scan has_t2_cond(best, C sig) (kind-1 condition
  with C signature under a COND).
- D4: true_correct(fam 10, best) over all 64 inputs.

### Frozen predictions for Family A2

- D1: C in beam for all 24 rounds (predicted top scorer at 9175).
  C in pbeam from round 2 onward (C enters the beam at round 0's
  selection, so it is in the input beam of rounds 1 and 2; pbeam
  at round r holds the input beam of round r-1).
- D1b: Y5 in pbeam from round 1 onward (predicted). Y4 in pbeam:
  uncertain, reported as observed.
- The Tier-2 pass preconditions on C are then met (kind-1, in
  beam+pbeam, exact agreement, min slice). The empirical question
  is whether condhit fires.

Two informative outcomes, both of which map the boundary:

A2-COMBINER-FIRES: D2 >= 0 (condhit fires) and D3 = 1. The
Tier-2 combiner logic is real. Boundary mapped: the pass fires
if and only if the condition (and both arms) survive selection,
i.e. only when the condition is already target-predictive. The
tiered CLAIM stays retired: the pass does not discover
discriminative conditions; it only fires when selection already
favors them. (Rehabilitation of the tiered claim would additionally
require firing on a discriminative condition, which A1 already
refuted; A2 alone does not revive it.)

A2-COMBINER-DEAD: D2 = -1 despite D1 showing C in beam+pbeam
simultaneously AND D1b showing both arms in pbeam. Then the
Tier-2 pass is broken at the logic level as well as the
selection level. (If an arm is missing from pbeam, the outcome is
reported as A2-ARM-GATED: the gate's three-node survival
requirement itself is the boundary, and the combiner logic
remains untested. This is still a boundary map, not a pass.)

D4 is reported in all cases (expected: best is C at 63/64 or the
Tier-2 COND at 64/64 if it fires; C alone gets 63/64 on full
truth since it misses x=3... actually C vs E10 on all 64 inputs
is reported as observed).

### Verdict bar for Family A2

A2-COMBINER-FIRES: D2 >= 0 and D3 = 1.
A2-COMBINER-DEAD: D2 = -1 with C in beam+pbeam and both arms in
pbeam (preconditions demonstrably met).
A2-ARM-GATED: D2 = -1 with at least one arm missing from pbeam
(the three-node survival requirement is the binding constraint).

## Attack Family B2: crowding, non-equivalent distractors only

Same frozen world as B1 (fam 8: E = (D AND Y4) OR ((NOT D) AND Y5)).
Library terms added in this order: D1 (t=9), D2 (t=10), then the
true D (t=8). D3 is EXCLUDED. Definitions (from the B1 prereg,
unchanged):

- D1: D XOR (x1 AND x2 AND x3). Diverges from D exactly where
  x1=x2=x3=1 (8 of 64 inputs).
- D2: D XOR x6. Diverges from D exactly where x6=1 (32 of 64).
- D: fam 8's d = (x1 & (x2^x3)) | ((x1^1) & (x2&x3)).

### Protocol B2

Modeled exactly on B1: seed 710202 (same evidence regime; only
the library composition changes), 8 terminals, library terms
D1, D2, D in that order (adversarial tie-break preserved: lower
node ids for distractors), passive() then 12 rounds
(beam_extend_round + select_iv/do_iv). hit_iv = first round with
true_correct >= 61/64, or 12.

Read-only diagnostics: D5 = has_d_subexpr(best, true D sig);
D6 = which condition terminal index the best COND uses; D7 =
true_correct(fam 8, best)/64.

### Frozen prediction for Family B2

Predicted: B2-FAILS-REUSE. Rationale: B1 revealed the mechanism
does not preferentially reuse the true D (it installed D3, the
equivalent distractor, despite D's lower terminal index). With no
equivalent distractor available, the mechanism is predicted to
install a D1/D2-based COND or fail to reach the bar, not to
install the true D. B2-FINDS-D remains possible and would refute
this attack prediction; it is the honest alternative.

### Verdict bar for Family B2

B2-FINDS-D: D5 = 1 (true D used) AND D7 >= 61/64 within 12 rounds.
B2-FAILS-REUSE: D5 = 0 or D7 < 61/64 after 12 rounds. D6 names
the installed condition in either case.

## Overall verdict

THRESHOLD-BOUNDARY-MAP-COMPLETE: both families executed 3/3 with
verdicts against the frozen bars above, and the boundary stated
as: (1) the exact precondition set under which the Tier-2 pass
fires or stays silent; (2) whether true-term reuse survives
crowding without an equivalent distractor. This follow-up does
not revive the tiered claim under any outcome; A2-COMBINER-FIRES
maps the pass as selection-dependent machinery, it does not
rehabilitate Tier-2 discovery.

## Kill bars

K1: this prereg strictly precedes family generation and testing.
Verified via git merge-base --is-ancestor before implementation.
Seeds: B2 seed 710202 frozen here (same as B1); A2 uses no RNG.
The fam 10 definition and frozen evidence table above are the
seal; implementation follows them exactly.

K2: both families executed 3/3 (byte-identical expected; A2 has
no RNG, B2 fixed seed) with per-family verdicts against the
frozen bars above.

K3: pure Zag, zero Python at every step (implementation, build,
runs, analysis via shell tools only). Committed mechanism
functions byte-identical to d0d296650 (verified by diff showing
only additions: fam 10, A2/B2 drivers, arm diagnostics, main).
No em dashes (shell-only check_no_dash.sh).

## Governance

- Attack the committed mechanism; do not modify it. The attack
  file is a copy of redteam_attack.zag; the diff against
  d0d296650's mechanism must show additions only.
- Owned path:
  docs/lab/research-lead/overnight-20260928/threshold_boundary/.
- Never touch
  docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md.
- Use explicit pathspecs on every git add and git commit. Run
  git status --porcelain before each commit; other workers stage
  their own files on this shared branch.
- If a live .git/index.lock is hit, wait and retry; never
  remove it.
- This prereg does not weaken any frozen bar. A2's evidence is
  chosen to favor the mechanism (the attacker's burden); B2's
  12-round bar is the same tight bar as B1.
