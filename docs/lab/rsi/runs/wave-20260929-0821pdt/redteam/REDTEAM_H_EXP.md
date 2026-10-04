# REDTEAM H-EXP: second opinion on the discriminating-experiment invention candidate

Wave: wave-20260929-0821pdt. Reviewer: red-team (skeptic posture).
Target: exp_learn.zag (impl commit), prereg PREREG_H_EXP.md (K-E1..K-E5),
evidence in evidence/ (run_hexp.sh, seven executions, binary sha
ea14d6b9db2b8809789234f785d84717f16f9391bdc0c9ed6ca83839c97fd728).

Method: independent re-execution from the committed sources via the
evidence run script; the attack battery below was fixed in the prereg
before implementation. Zero Python anywhere. No em-dashes in this
document.

## Kill-bar verification (exact numbers from evidence)

- K-E1 (P1 real pair): PASS. p1_r1.out: HYP1 lamp-block rules=12, HYP2
  temp-block rules=12, CANDIDATES len1=6 len2=36 len3=216, CHECKED 32,
  DIFFVAR pressure, PRED1 0 0 1, PRED2 0 1 1, SELECT 4 2. The selected
  sequence is exactly [4,2] (lamp_on, pressurize); both hypothesis names
  appear; the differing variable is stated as pressure.
- K-E2 (trace inspectability): PASS. All required fields present in
  order: names, per-hypothesis rule counts, per-length candidate
  counts, CHECKED 32, per-hypothesis predicted final states.
- K-E3 (P2 null): PASS. p2_r1.out contains the exact line
  "WITHHOLD: no discriminating experiment within length<=3" (grep
  count 1); zero occurrences of the substring SELECT; exit code 0;
  stderr empty.
- K-E4 (determinism): PASS. cmp p1_r1.out p1_r2.out identical; cmp
  p3_r1.out p3_r2.out identical.
- K-E5 (generalization, anti-hardcoding): PASS. p3_r1.out selects
  [0,4] (heat, lamp_on) with HYP1 cold-enables-lamp rules=12, HYP2
  lamp-always rules=10, CHECKED 10, DIFFVAR lamp, PRED1 1 0 0,
  PRED2 1 0 1.

## Attack battery results

1. Hardcoding: grep for the five hypothesis names across
   impl/exp_learn.zag returns zero hits; grep for literal selection
   sequences finds no encoded [4,2] or [0,4] constants outside the
   generic enumeration. The only action/vocabulary constants are the
   loop bounds (6 actions, length<=3), which are declared authored
   boundaries in the prereg. PASS.
2. Try-everything / longest-first bias: the null pair (P2) withholds
   rather than picking a random sequence, and the CHECKED counts are
   hand-verified correct (P1: 6 + 24 + 2 = 32 sequences before (4,2);
   P3: 6 + 4 = 10 before (0,4)), proving length-major lexicographic
   order, not longest-first. PASS.
3. Data-drivenness: P3 uses different rule contents and a different
   discriminator than P1 and still passes; the renamed-copy run
   (renamed_x.txt/renamed_y.txt) selects [4,2] with only the HYP1/HYP2
   name lines differing, proving behavior follows file CONTENTS, not
   filenames. PASS.
4. Byte determinism: K-E4, both pairs. PASS.
5. Scope honesty: the prereg's predicted boundary list is reproduced
   verbatim in the verdict below; no L3 or "genuine invention" claim
   is made. The true-world execution step is explicitly out of scope
   (queued as H-EXP2). PASS.

## Knowledge-vs-architecture confound check

The "knowledge" in this candidate is the hypothesis pair (supplied as
data); the "architecture" is the generic rule evaluator plus the
enumeration/selection loop. The confound to test: does the module know
the answer without the data? P3 answers no: with different rule data
it produces a different, correct selection, and with vacuous data
(P2) it withholds. The module cannot produce the right answer from
the P1 pair's names alone (names are never read as logic). Residual
authored knowledge: the action vocabulary, the length bound, the
state-variable ontology (t,p,l), and the pair contents themselves.
All are declared, not hidden.

## Prereg amendment review

The post-freeze amendment added the missing "HYP <name>" first lines
to the six hypothesis fixtures. Assessment: the amendment is
transparent (its own commit, c06a23cfb, with the reason stated),
pre-execution (no implementation run had occurred), and semantic-free
(it adds only the names the format spec already required; rule
contents byte-identical otherwise). It does not weaken any kill bar.
ACCEPTED as a legitimate transparent amendment, not a violation.

## Verdict: H-EXP SURVIVES as a bounded capability

Classification: bounded structural selection toward Level D
(self-directed evidence). Explicitly NOT L3: the hypotheses are
supplied as data (not discovered), the action vocabulary and length
bound are authored, the mechanism is enumerate-and-select (not
constructive invention), and it has no revision machinery (the
criterion-12 family remains failed, consistent with the morning
classification of procedure v1). It does not transfer beyond the
frozen world ontology.

Adoption recommendation: ADOPT as a loop-owned new capability in the
wave record with the boundary list above. Zero regressions possible:
no existing subsystem file was modified (all wave work is additive
under docs/lab/rsi/runs/wave-20260929-0821pdt/).
