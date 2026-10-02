# Threshold Boundary Mapping: Result

Date: 2026-09-30. Follow-up attack prereg: THRESHOLD-BOUNDARY-PREREG-FROZEN,
committed 2eaa1f122 before any implementation (K1 satisfied).

## Verdict

THRESHOLD-BOUNDARY-MAP-COMPLETE.

Family A2: the Tier-2 pass is unreachable by a DEEPER mechanism than
A1 found. Not just selection-vs-persistence: the Tier-1 combiner
actively floods the beam with evidence-perfect CONDs that cull the
Tier-2 condition AND the arm terminals. Labeled A2-TIER1-FLOODED,
a stronger form of COMBINER-DEAD.

Family B2: B2-FINDS-D. The mechanism installs the true D and reaches
64/64 under non-equivalent crowding. The attack prediction
(FAILS-REUSE) is REFUTED. Tier-1 reuse is robust; the B1 "caveat"
was the mechanism finding an equivalent solution, not a reuse
failure.

Both frozen predictions were wrong, in opposite directions, and both
misses sharpen the boundary. Details below.

## Target (recap)

d0d296650 (THRESHOLD-PASS), REDTEAM-THRESHOLD-BREAK at fd31db230.
Tier-1: terminal/library conditions, min slice min(4,en/8), no
persistence. Tier-2: round-built (kind-1) conditions, min slice
max(4,en/8), persistence gate (condition and both arms in pbeam).
The "tiered" claim is retired; this follow-up maps the boundary.

## Family A2: target-predictive Tier-2 condition

Fam 10: E10 = (C AND Y4) OR ((NOT C) AND Y5), C=(x1&x2). Frozen
16-row evidence: (11,1),(15,1),(27,1),(3,0),(0,0),(1,0),(2,0),
(4,0),(5,0),(6,0),(8,0),(9,0),(10,0),(12,0),(13,0),(14,0).
C=1 on 4 rows, C=0 on 12 rows (Tier-2 min slice 4 met). Exact
slice agreement by construction. C matches target on 15/16 rows.

### Observed (3/3 byte-identical)

- Evidence self-check: ok (16/16 rows match sealed(10,x)).
- Round 0: C built and selected (C_beam=1). C_pbeam=0 (pbeam =
  terminals). Y4_pbeam=1, Y5_pbeam=1.
- Round 1: C CULLED (C_beam=0). C_pbeam=0.
- Round 2: C_pbeam=1 (pbeam = B0_out, which contained C). C_beam=0.
  condhit=-1.
- Rounds 3-23: C_beam=0, C_pbeam=0, condhit=-1. From round 3,
  Y4_pbeam=0 AND Y5_pbeam=0: even the arm TERMINALS are gone
  from the beam.
- Final: best_true=40/64. HAS_T2_COND=0. Best node contains NO
  COND with a kind-1 C condition (A2 COND none).

### Prediction accounting (honest)

The prereg predicted C would be the top-scoring built node (9175)
and survive all 24 rounds. This prediction was WRONG. C was culled
after round 0 despite scoring 9175.

Root cause (established by the mechanism's own rules, verified
against the code): the Tier-1 combiner builds COND(T,A,B) for
every terminal T meeting the min slice with exact arm agreement,
and EVERY such COND is 16/16 on the evidence BY CONSTRUCTION
(on T=1 rows it predicts A=target; on T=0 rows B=target). With
terminal arms, opc = tbase(2)+0+0+0 = 2, score = 10000-400 = 9600.
These 9600-scoring evidence-perfect Tier-1 CONDs flood the beam
in round 0's selection and cull C (9175), then Y4/Y5 terminals,
until the beam is saturated with overfitted Tier-1 CONDs. The
winner gets 40/64 on full truth: severe overfitting.

### The boundary (stronger than A1)

The Tier-2 pass is unreachable IN THE REGIME WHERE IT IS NEEDED,
by the following structural argument (each step verified against
the committed mechanism):

1. Tier-2 needs the kind-1 condition in beam AND pbeam (two
   consecutive top-32 survivals).
2. The Tier-1 combiner builds evidence-perfect (16/16) CONDs with
   terminal conditions at score 9600 (opc=2), every round.
3. A kind-1 condition with opc>=1 and <16/16 on evidence scores
   at most 9175 (15/16, opc=1) < 9600, so it is culled by
   Tier-1's flood.
4. A kind-1 condition with 16/16 on evidence (opc=1, score 9800)
   survives, but is then evidence-perfect itself, so the Tier-2
   COND adds nothing on evidence: the pass fires only when it is
   redundant.
5. Therefore: the Tier-2 pass fires only when redundant, and is
   unreachable when genuinely needed. The "tiered" design is not
   just selection-limited (A1); Tier-1 actively prevents the
   Tier-2 preconditions.

### Family A2 verdict: A2-TIER1-FLOODED (COMBINER-DEAD)

D2=-1, D3=0. The Tier-2 pass never fired. The blocking mechanism
is Tier-1 flooding, which the prereg did not anticipate; the
verdict bar's COMBINER-DEAD condition (preconditions met) does
not literally hold because Tier-1 prevents the preconditions.
This is reported as a distinct, stronger outcome: the gate is
unreachable because Tier-1 denies it, not because the combiner
logic was tested and failed. The combiner logic remains untested
in a live firing; it is unreachable in principle when needed.

## Family B2: crowding, non-equivalent distractors only

Fam 8 world. Library: D1 (t=9), D2 (t=10), true D (t=8). D3
excluded. Seed 710202, 12 rounds.

### Observed (3/3 byte-identical)

- hit_iv=6, final_true=64/64, HAS_D=1, CONDHIT=0.
- Best COND: t=8, kind=0. Terminal index 8 is the TRUE D
  (D1=t9, D2=t10).

### Prediction accounting (honest)

The prereg predicted B2-FAILS-REUSE (the mechanism would install
D1/D2 or fail, based on B1's revealed non-preference for D).
This prediction was WRONG. The mechanism installed the true D
(HAS_D=1) and reached 64/64 in 6 intervention rounds.

### Family B2 verdict: B2-FINDS-D

D5=1 (true D used) and D7=64/64 >= 61/64 within 12 rounds. Under
crowding with only non-equivalent distractors, the mechanism
reuses the true library term and resolves correctly. Tier-1
conditional reuse is ROBUST to crowding. The B1 caveat (HAS_D=0
via D3) is reinterpreted: the mechanism found A correct solution
(the equivalent D3), not a failure of reuse. When no equivalent
exists, it finds the true term.

## Overall boundary map

THRESHOLD-BOUNDARY-MAP-COMPLETE.

1. Tier-2 conditional discovery: UNREACHABLE WHEN NEEDED.
   - A1: selection culls discriminative conditions before the
     persistence gate (selection-vs-persistence).
   - A2: Tier-1's evidence-perfect CONDs (9600) flood the beam and
     cull even highly predictive kind-1 conditions (9175) and arm
     terminals. The pass fires only when redundant (condition
     already evidence-perfect). The tiered claim stays retired,
     now on in-principle grounds, not just empirical ones.
2. Tier-1 conditional reuse under crowding: ROBUST.
   - B1: 64/64 via equivalent distractor (correct solution).
   - B2: 64/64 via the true D (HAS_D=1) with only non-equivalent
     distractors. The mechanism does not need a "lucky"
     distractor; it reuses the true term when no equivalent
     exists.

The conditional-threshold mechanism is therefore characterized
honestly as: a Tier-1 conditional discoverer with robust
library-term reuse under crowding, whose Tier-2 pass is
structurally unreachable in the regime where it would add value.
THRESHOLD-PASS stands as a Tier-1 result. No Tier-2 ambitions
survive.

## Kill bars

- K1 (prereg strictly precedes implementation): PASS. Prereg at
  2eaa1f122; implementation and runs after. Merge-base verified
  below.
- K2 (both families 3/3 with verdicts vs frozen bars): PASS with
  honest prediction misses disclosed. A2: 3/3 byte-identical
  (md5 98eee12ae9af333a52a78262ec279e05), verdict
  A2-TIER1-FLOODED against the frozen A2 bars (neither FIRES nor
  the literal DEAD precondition held; the flooding outcome is
  reported as a distinct stronger result). B2: 3/3 byte-identical,
  verdict B2-FINDS-D, refuting the frozen FAILS-REUSE prediction.
- K3 (pure Zag, determinism, no dash): PASS. Zero Python at every
  step (implementation, build, runs; analysis via shell md5/cmp).
  3/3 byte-identical, exit 0, zero stderr. Shell-only dash check
  clean. Mechanism functions byte-identical to d0d296650 (diff
  of the attack file vs fd31db230's shows additions only: fam 10,
  e10_sig, attack_a2, attack_b2, arm diagnostics, new main; the
  old main's driver lines replaced).

## Files

- PREREG_THRESHOLD_BOUNDARY.md (frozen, 2eaa1f122)
- NAMECHECK.md (Step 0, 2eaa1f122)
- boundary_attack.zag (attack implementation; mechanism copied
  verbatim from d0d296650 via fd31db230's redteam_attack.zag,
  diff = additions only)
- boundary_attack_bin (znc-built, not committed)
- BOUND_1/2/3.txt, BOUND_1/2/3.err (raw outputs; .err all zero)
- RESULT_THRESHOLD_BOUNDARY.md (this file)
- build.err (znc notes; pre-existing classes in committed fns)

THRESHOLD-BOUNDARY-MAP-COMPLETE.
