# SEALED_EVAL.md - F1 trigger wave sealed evaluation results

Lane F1, wave wave-20261001-2321pdt. Sealed runs executed 2026-10-01
~23:40 PDT against the frozen binary `impl/f1_learn` (sha256
6f2b155b233a95ad1a8323e8565b9a798dc822db6eff57e065b71b5be8882847,
verified before running; match confirmed). Fixture hashes verified
against PREREG_TRIG.md section 8 (all 23 match). Attack prereg:
PREREG_TRIG.md (committed alone at 50de69403 before any implementation
file existed; implementation committed at ba5ebbf8b).

No em-dashes are used in this document.

## 1. Determinism evidence

Each of the 22 sealed invocations was executed 3 times
(sealed/runs/1, runs/2, runs/3; 66 state/trace/pred outputs per
repetition). All corresponding outputs are byte-identical across the
three repetitions (cmp-verified, zero diffs). SHA-256 of all 66 runs/1
outputs is recorded in sealed/runs/DETERMINISM_SHA256.txt. Zero
randomness in decision paths. The determinism standard is met.

## 2. K-TRIG-FIRE: fires on interleaved errors (PASS)

Trigger episodes on sealed train runs (bar: at least one TRIGGER with
episode index < 12):

| pattern | triggers | first trigger ep | bar |
|---|---|---|---|
| T-A alternating | 2 | 2 | PASS |
| T-B 1-in-3 | 1 | 3 | PASS |
| T-C 1-in-4 | 1 | 4 | PASS |
| T-D bursty 2-on-6-off | 3 | 1 | PASS |

The old K1=2 consecutive trigger never fires on pattern A (verified:
NC-TRIG below, 0 triggers). The windowed trigger fires on all four.

## 3. K-TRACE: construction follows the trigger (PASS)

CONSTRUCT events per sealed train run (bar: at least 2, episode-indexed
at or after the first trigger):

| pattern | constructs | bar |
|---|---|---|
| T-A | 3 | PASS |
| T-B | 2 | PASS |
| T-C | 2 | PASS |
| T-D | 6 | PASS |

Example (T-A): TRIGGER 2 winfail=2 win=3 buf=3; CONSTRUCT 2 0 EQ
r0,f0,f1 err 4->2; CONSTRUCT 2 1 ADD r0,r0,r0 err 2->0. No structure
isomorphic to the final one existed in learner state before the first
construction event (seed state only).

## 4. K-LEARN-INTERLEAVED: the trigger enables learning (PASS)

Hidden accuracy on sealed 30-probe sets, trained state in
(bar: at least 80 percent):

| pattern | hidden | bar |
|---|---|---|
| T-A | 30/30 = 100% | PASS |
| T-B | 30/30 = 100% | PASS |
| T-C | 30/30 = 100% | PASS |
| T-D | 30/30 = 100% | PASS |

The learner discovers EQ and the 2x scaling from interleaved streams on
all four patterns. Firing without learning would fail here; it does not.

## 5. K-TRIG-CLEAN: no false positives (PASS)

TRIGGER lines on clean runs (bar: 0; frozen false-positive rate 0):

| clean world | triggers | accuracy | bar |
|---|---|---|---|
| C-A seed on y=0 (30 eps) | 0 | n/a | PASS |
| C-B sum2-trained on fresh y=2(x0+x1) | 0 | 30/30 | PASS |
| C-C quad-trained on fresh y=4x | 0 | 30/30 | PASS |

## 6. K-C0C-REG: no regression (TRIP on rW2)

| family | hidden | constructs | bar |
|---|---|---|---|
| R-W2 y=2(x0+x1), fresh seed | 0/30 = 0% | 4 | TRIP (0 < 80) |
| R-W3 2x->4x law change, fresh seed | 30/30 = 100% | 2 | PASS |

R-W3 trace matches the prior wave's W3 dynamics (TRIGGER 2, construct
2x; STALL 14, STALL 16 on the mixed buffer; TRIGGER 18, construct 4x;
remaining episodes correct). The revision machinery is preserved.

R-W2 root cause (killing evidence): the greedy depth-1 trial overfits
the sealed train seed (2301). Both the old and new binaries converge to
the identical overfit structure
`[ADD r0,f1,f1; ADD r0,r0,f1; ADD r0,r0,f0; ADD r0,r0,f0]`
(signatures byte-identical) and score 0/30 on the hidden set. The old
binary was run on the sealed rW2 fixtures as a diagnostic: 8 triggers,
same 4 constructs, 0/30. This is a pre-existing constructor limitation
(greedy argmin overfitting on this seed's values), not a trigger
regression.

Zero-regression proof (trigger scope): the new binary was run on the
prior wave's sealed W2 fixtures (unchanged). Result: TRIGGER 1
(winfail=2, same episode as the old consec=2 trigger), the same 3
constructs in the same order (ADD r0,f0,f0 6->2; ADD r0,r0,f1 2->1;
ADD r0,r0,f1 1->0), hidden 30/30, structure [4 4 4 2] identical to the
prior wave. The trigger change preserves previously passing behavior
exactly where the constructor is not seed-limited.

The bar as frozen measures hidden accuracy on a fresh seed, which
conflates trigger regression (the risk under test) with constructor
seed-robustness (pre-existing, out of scope). The bar trips on the
literal 80 percent threshold. It is not weakened to force a pass.

## 7. K-ABL-TA and K-BASE-TA (PASS)

T-A hidden (30 probes): trained 30/30 = 100%; seed-state (ablated)
13/30 = 43%; exact-match memorizer (24-episode budget) 13/30 = 43%.

- K-ABL-TA: 100 - 43 = 57pp >= 40. PASS.
- K-BASE-TA: 100 - 43 = 57pp >= 40. PASS.
  (Margins on T-B/T-C/T-D: 40pp, 60pp, 54pp; all >= 40.)

## 8. K-C0A source audit (PASS)

```
$ grep -n 'FIND_POLYNOMIAL_ORDER\|...' f1_isa.zag f1_learn.zag  -> exit 1, zero hits
$ grep -n 'COUPLED\|SPECIALIZE\|REIFY\|SPLIT_SCAN\|COND(' ...      -> exit 1, zero hits
$ grep -ni 'menu\|kit_\|candidate_list\|template' ...            -> exit 1, zero hits
```
The only tag dispatch is the frozen ISA op dispatch (generic execution
machinery). No researcher-authored semantic cases were added.

## 9. NC-TRIG negative control (PASS; battery has teeth)

Prior wave's frozen binary (sha256
0c571abca5a3c16695115228114c327bb3370081304c9c3a1ea1354840aa2727)
on sealed T-A train: 0 TRIGGER lines. The battery reproduces the W1
defect on the old mechanism and the new mechanism fires where the old
never did. Not a void.

## 10. Verdict: BUILD-FAIL

Tripped bar: K-C0C-REG on R-W2 (0/30 < 80 percent). The bar is not
weakened.

Qualification the coordinator needs: the trip is caused by a
pre-existing constructor limitation (greedy trial overfitting on sealed
seed 2301), proven by the old binary's identical failure on the same
fixtures. The trigger itself, which is the subject of this wave, passes
every trigger-specific bar: it fires on all four interleaving patterns
(K-TRIG-FIRE), construction follows (K-TRACE), the learner reaches
100 percent hidden on all four interleaved families (K-LEARN), it never
fires on clean worlds (K-TRIG-CLEAN), the learned structures are
load-bearing (K-ABL-TA, K-BASE-TA), the source audit is clean (K-C0A),
and the battery discriminates old from new (NC-TRIG). True regression
testing on the prior wave's W2 fixtures shows zero trigger regression
(identical trigger episode, constructs, 30/30, structure).

Passing bars: K-TRIG-FIRE, K-TRACE, K-LEARN-INTERLEAVED,
K-TRIG-CLEAN, K-C0C-REG on R-W3, K-ABL-TA, K-BASE-TA, K-C0A, NC-TRIG,
determinism 3/3. Bounded L2+ ceiling stands; no L3 claim follows.
