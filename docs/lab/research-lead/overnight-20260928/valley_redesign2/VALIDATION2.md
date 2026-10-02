# Valley Redesign-2 Validation (step b, attempt 2)

Prereg: `0310c7076` (VALLEY-REDESIGN2, 108 lines, committed alone).
Implementer: Valley Redesigner, 2026-09-30. Pure Zag, no Python.
Validator: `v2inst.zag` + `v2gen.zag` (concatenated as
`build/v2gen.zag`), binary `build/v2gen`.

## Implementation notes

- VM: frozen GENEXEC2 straight-line semantics copied op-for-op from
  `valley_run/vinst.zag` (ops 0..15).
- V1: per prereg (all non-empty proper prefixes <= s0, at most one
  tie, at least d-1 strictly below, full == |E|, s0 < |E|). Computed
  s0 is checked equal to the frozen prereg s0 (no S0-MISMATCH fired).
- V2: frozen REF-GREEDY (strict improvement, 34-symbol alphabet,
  lowest-index tiebreak, 500 iters).
- V3: exhaustive 1-edit over every proper prefix plus 2-edit
  (neighbors to length 12) for k <= 10. Every canonical path has
  L <= 11, so the 2-edit enumeration is COMPLETE: a pass would have
  been a proof of minimum 3-edit distance. Neighbors that are
  prefixes of F are skipped (canonical completion is not a shortcut).
- V4: implemented (hyp_a decision logic verbatim from hyp_a.zag
  commit 21d838921 with episode substitution; GREEDY-2 with 2-op
  lookahead) but never reached: every candidate failed at V3.
- One implementation fix during the run: the first build leaked one
  1KB stack buffer per VM call and was OOM-killed on id 6; the VM now
  takes a caller-reused stack buffer. The frozen V3 enumeration is
  unchanged; only the leak was fixed.

## Result

**0 of 10 candidates accepted. All rejected at V3 with a documented
1- or 2-edit solver.** CAL-0 passes (s0=1, IN0 solves 9/9).

| id | instance | V1 | V2 | V3 | failing solver found (decoded) |
|----|----------|----|----|----|-------------------------------|
| 1 | K1 x==2, n=2 | PASS | PASS | FAIL | [PUSH 0,PUSH -9,PUSH 5,DROP,IN0,MOD]: mod_nonneg(-9,x) is 1 iff x==2; 2 edits (replace+append) from k=5 prefix |
| 2 | K2 x==3, n=2 | PASS | PASS | FAIL | [PUSH 0,PUSH 7,PUSH 5,DROP,IN0,PUSH 2,GT]: x>2 iff x==3; 1 append from k=6 prefix |
| 3 | K3 x==5, n=3 | PASS | PASS | FAIL | [PUSH 0,PUSH 7,PUSH 5,IN0,EQ]: stacked 5 repurposed; 2 edits from k=4 prefix |
| 4 | K4 x==6, n=3 | PASS | PASS | FAIL | [PUSH 0,PUSH 6,PUSH 5,DROP,IN0,EQ]: 2 edits (replace+append) from k=5 prefix |
| 5 | K5 (x==2)&&(y==1) | PASS | PASS | FAIL | [...,IN1,DIV]: DIV acts as AND on bits; 1 append from k=8 prefix |
| 6 | K6 (x==3)&&(y==2) | PASS | PASS | FAIL | [...,IN1,PUSH 2,EQ,DIV]: same; 1 append from k=10 prefix |
| 7 | A1 x mod 3 | PASS | PASS | FAIL | [PUSH 0,DROP,IN0,PUSH -3,MOD]: negative-divisor MOD; 2 appends from k=3 prefix |
| 8 | A2 x mod 2 | PASS | PASS | FAIL | [PUSH 0,DROP,IN0,PUSH -2,MOD]: same shape |
| 9 | A3 x mod 5 | PASS | PASS | FAIL | [PUSH 0,DROP,IN0,PUSH -5,MOD]: same shape |
| 10 | A4 2x+1, x in 1..9 | PASS | PASS | FAIL | [PUSH 3,PUSH 7,ADD,IN0,PUSH 2,MUL,PUSH -1,SUB]: 2x-(-1); 2 appends from k=6 prefix |

V1 passed on all 10 (score profiles are real valleys against strict
greedy: V2 greedy halts at len 1 on every instance). V4 was never
reached. No instance is accepted; no mechanism runs are authorized.

## V5 determinism

```
5a1ff33ba67c724ef95a84489d14d68c75b30d92f2fe6d170f11a837434248cf  build/v2gen_run1.txt
5a1ff33ba67c724ef95a84489d14d68c75b30d92f2fe6d170f11a837434248cf  build/v2gen_run2.txt
5a1ff33ba67c724ef95a84489d14d68c75b30d92f2fe6d170f11a837434248cf  build/v2gen_run3.txt
```
3/3 byte-identical: yes.

## Kill bars

- K1: PASS. Prereg is 108 lines (<= 120), committed alone as
  0310c7076, strictly before implementation (ancestry verified with
  git merge-base --is-ancestor).
- K2: FAIL. 0 of 10 candidates accepted; 8 required. Every rejection
  names V3 and the exact solving neighbor above.
- K3: PASS. Pure Zag (no Python in implementation, validation,
  measurement, or byte checks); deterministic 3/3; dash-clean per the
  shell-only check_no_dash.sh snippet.

## Architectural yield (why the redesign died)

The failures are not bad luck; they are three lemmas about GENEXEC2:

1. 3-op solver lemma. If a 3-op program [IN0,X,Y] solves the target,
   any canonical path with an IN0-ending proper prefix fails V3.
   This kills ALL singleton-equality targets ([IN0,PUSH K,EQ]) and
   ALL mod-m targets ([IN0,PUSH m,MOD]) on GENEXEC2, regardless of
   prologue design. The v1 "bit-test" idea and the v2 "inert
   prologue" idea both die here.
2. 1-gate lemma. A proper prefix leaving two 0/1 bits atop the stack
   is 1 edit (MUL or DIV) from their AND. This kills compositional
   AND valleys under a 1-edit V3 (ids 5, 6).
3. MOD/DIV universality. mod_nonneg with a negative divisor encodes
   arbitrary small lookup tables (ids 1, 7, 8, 9); DIV acts as AND on
   bits (ids 5, 6). The 2-edit neighborhood on GENEXEC2 is far more
   expressive than the v1 design assumed, and "inert" prologue
   constants are repurposed by EQ/GT within 2 edits (ids 3, 4).

## Verdict

VALLEY-REDESIGN-FAIL (K2: 0/10 accepted, 8 required). This is a
validation-gate failure, not a B/C2/D mechanism failure. The battery
remains void: no accepted instances, no mechanism runs authorized.

## Recommended next step

Freeze the V3 checker as an oracle and run a bounded Zag search over
(target, canonical-path) pairs with L <= 11 to decide whether ANY
instance passes V1-V3 on GENEXEC2, with candidate substitution allowed
in the next prereg. The search must target families outside the three
dead lemmas (no 3-op IN0-led solver; no two-bit AND composition).
If the bounded search finds none, the V3 bar itself is unsatisfiable
on GENEXEC2 and the bar, not the instances, must be redesigned.
