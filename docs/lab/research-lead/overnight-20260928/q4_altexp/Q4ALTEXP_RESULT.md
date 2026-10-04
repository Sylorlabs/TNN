# Q4 Alternative-Explanation Attack: Result (promotion step 6)

Prereg: `PREREG_Q4ALTEXP.md` committed as `836709080`, transparently amended
before implementation as `58576ea5d` (A1 changed from single evidence set to
three evidence sets). Commit ordering is valid: both prereg commits precede
this implementation. Zero Python used anywhere in this task.

Frozen kill bars (K2): A1a, A1b, A2, A3 executed exactly as preregistered.
`BEAMNODES=3868` below is cited from the original Q4 result (3,868 candidate
programs evaluated), not re-measured here.

## Method

`altexp.zag` (pure Zag, fixed seed 123456789) replicates the original Phase-1
evidence loop exactly (8 passive + 24 disagreement IVs, same RNG, same beam
machinery copied verbatim) and runs three tests:

- ENUM: all 256 3-bit behaviors scored on three evidence sets (canonical 8,
  replicated passive 8, replicated learner 32).
- RANDIV: Phase 1 with disagreement IVs replaced by deterministic random
  unused-input selection (same 24-round budget).
- FULLMEM: D lookup table from the same 32 Phase-1 observations, composed as
  C' = D_table XOR x4 over all 64 x.

`robust.zag` is EXPLORATORY (not preregistered, built after seeing results):
the original disagreement-IV phase1 run on 5 fresh seeds, reporting best
evidence fit, op count, true accuracy, and combo coverage per seed.

## Raw output (preregistered runs, 3/3 byte-identical, zero stderr)

```
Q4-ALTEXP
DBEHAVIOR=104
EVIDENCE32 n=32
ENUM SET=canonical TOP=8/8 TIES=1 TRUEUNIQUE=1 FIRSTTRUE=64/64
ENUM SET=passive8 TOP=8/8 TIES=8 TRUEUNIQUE=0 FIRSTTRUE=56/64
ENUM SET=learner32 TOP=32/32 TIES=2 TRUEUNIQUE=0 FIRSTTRUE=64/64
ENUM EVALS=256 BEAMNODES=3868
RANDIV BEST node=1551 ev_correct=32/32 opc=5
RANDIV TRUE correct=64/64
FULLMEM COVERAGE=7/8 CORRECT=64/64
DONE
```

md5 `00150b12e93ed312cfd8873f7a08463e` across all three runs.

## Raw output (exploratory robust probe, 2/2 byte-identical, zero stderr)

```
Q4-ROBUST-EXP
SEED=11 BESTEV=32/32 OPC=6 TRUE=64/64 COVER=8/8
SEED=22 BESTEV=32/32 OPC=5 TRUE=64/64 COVER=8/8
SEED=33 BESTEV=32/32 OPC=2 TRUE=56/64 COVER=7/8
SEED=44 BESTEV=32/32 OPC=5 TRUE=64/64 COVER=7/8
SEED=55 BESTEV=23/32 OPC=0 TRUE=40/64 COVER=8/8
DONE
```

## Per-alternative verdicts

### A1: tiny behavior-space enumeration - SUSTAINED (revised)

P-A1a (true behavior unique top on learner32 evidence): FAILED. FP-A1a fired:
TIES=2, TRUEUNIQUE=0. The learner's 32 observations cover only 7/8 combos, so
two behaviors (differing only on the unseen combo) tie at 32/32. The evidence
UNDERDETERMINES the target. The beam's 64/64 therefore came from evidence +
the researcher-authored 200/opc simplicity tax + luck, not from evidence alone.

P-A1b (passive evidence alone cannot identify D): CONFIRMED. TIES=8 on the
biased passive-8 set, first-top true accuracy only 56/64. The 24 interventions
were epistemically necessary - a pro-learner finding, honestly recorded.

On canonical full-coverage evidence, 256 behavior evaluations uniquely
identify D (TIES=1, TRUEUNIQUE=1). The search problem is trivial given combo
coverage; the adaptive IV policy failed to achieve full coverage (7/8).

The exploratory probe adjudicates luck vs systematic bias: on SEED=33 (7/8
coverage) the beam preferred a 2-op WRONG expression (32/32 evidence, 56/64
true) - the simplicity tax does NOT systematically recover truth from
underdetermined evidence. The preregistered seed's 64/64 was luck of the draw.
Revised A1: the "discovery" is underdetermined evidence plus a simplicity
prior that happened to pick correctly on one seed. SUSTAINED in this sharper
form; the original P-A1a uniqueness prediction is retracted.

### A2: disagreement interventions may be decorative - SUSTAINED

RANDIV (deterministic random IVs, same 24-round budget): 32/32 evidence fit,
5-op expression, TRUE 64/64. Random interventions matched the learner's
accuracy with FEWER ops than the disagreement-IV run's 7-op solution. The
disagreement-driven IV policy shows no advantage at this budget; it is
decorative. P-A2 confirmed and exceeded. Additionally, the original result's
"7-op minimal" language is false: a 5-op solution was found here, and
D = (x1 ^ (x2 & x3)) & (x2 | x3) is a 4-op form (verified on all 8 combos).

### A3: reuse gap may be an evidence-quantity confound - KILLED (strong form); refined point stands

FULLMEM reached 64/64, but combo coverage was 7/8 and the 64/64 depended on a
lucky default: the single unseen combo has D=0, which the majority table
guessed correctly. A lookup table cannot represent the unseen combo except by
luck, so this does NOT cleanly show "same 32 observations let memorization tie
the learner." The learner's 7-op expression genuinely generalized to the
unseen combo. The C0-D reuse gap (learner 64/64 vs MEM-COMP 56/64) survives A3
as stated. KILLED in its strong form.

Refined point that stands: Phase 2 installs the learner's own learned D
signature (which happened to be exactly the true behavior) as an atomic
terminal, then tests one-step composition XOR(D, x4). The "reuse" test is
composition given a perfect component, not re-derivation - a thin
operationalization of C0-D. And the 0-vs-24-IV reuse comparison inherits the
single-seed luck documented above.

### A4: researcher-authored beam machinery does the work - SUSTAINED

Every decision (beam width 32, candidate generation, score = acc*10000 -
200*opc, disagreement IV policy, keep bars) is researcher-authored; the
learner makes none. New load-bearing evidence: with TIES=2 on the evidence,
the 200/opc tax selected the true behavior on the lucky seed and a 2-op wrong
behavior on SEED=33. The tax, not learning, decided the unseen combo. The
"discovery" of the 8th combo is attributable to the researcher's MDL bias.

### A5: C0-C shows vocabulary coverage, not adaptation - SUSTAINED

The mechanism is byte-identical between training families and F-PARCOND; the
beam enumerates expressions over the frozen functionally-complete vocabulary
{AND, OR, NOT, XOR}. The adversary's independence is real, but the test
measures vocabulary coverage, not adaptation to an unforeseen form. New: D
has a compact 4-op form, so "conditional computation" is one reading of a
simple 3-bit Boolean function; the C0-C bar as operationalized cannot
distinguish "adapted to a new form" from "the frozen vocabulary covered it."

### A6: the opc <= 7 bar was calibrated to the known reference - SUSTAINED

The bar (<=7) sits exactly one above the known 6-op reference; the prereg
author knew ADV_SPEC when writing the bars. A 5-op solution exists (found by
RANDIV) and a 4-op form exists analytically, so a "compact" bar of <=5 - a
natural bar for a "minimal expression" claim - would have FAILED the original
7-op run. The bar is calibrated to the known answer, and the "minimal 7-op"
framing is false.

## K3: which claims stand, which fall, what would revive

STAND (weakened): the learner found a correct general 7-op expression for
F-PARCOND from 32 observations and composed it in Phase 2 with 0 IVs; the
C0-C first data point (adversary-designed family solved) and C0-D pairing
result are real measurements.

FALL: (1) "The learner discovered F-PARCOND structure" as a robust discovery
claim - the 64/64 is single-seed luck on underdetermined evidence (7/8
coverage, 2 tied behaviors), with 3/5 exploratory seeds at 64/64, one at
56/64, one an outright fit failure (23/32, 40/64). (2) The disagreement-IV
"active" component adds nothing over random at this budget. (3) The "minimal
7-op" language - 5-op found, 4-op exists. (4) The implication that the
evidence determined the answer - it admitted two answers and the
researcher-authored simplicity tax picked one.

What would revive the discovery claim: a preregistered multi-seed bar (e.g.,
beam reaches true 64/64 on >=4/5 fresh seeds with the IV policy achieving 8/8
combo coverage); a discovered form with no compact analytic alternative
defeating the vocabulary-coverage reading; a reuse test where the component is
imperfect or must be re-derived rather than installed as an exact terminal.

## Integrity notes

- Determinism: 3/3 byte-identical stdout (md5 above), zero stderr, exit 0.
  Exploratory probe 2/2 identical.
- Zero Python used in this task (build, run, byte checks via md5sum only).
- Honest miss: P-A1a predicted uniqueness on learner32 evidence; FP-A1a fired
  (TIES=2). The prediction is retracted; the sharper underdetermination
  finding replaces it.
- Scope: bounded L2 attack result. The F-PARCOND result is not killed
  outright, but its "discovery" headline does not survive step 6 intact.

Verdict: ATTACK-COMPLETE
