# H-GENBIAS-ADV Result: Independent Red Team on the N-First Generality Bias

**Date:** 2026-09-29
**Prereg:** PREREG_GENBIAS_ADV.md (commit 66f4c324e, frozen before implementation)
**Method:** Pure Zag, no Python. Harness `genbias_redteam.zag` reuses the
exact discovery machinery from genbias_test.zag (commit 0763c13d8):
enumeration, prog_uses_n, pfits/peval, proc store, both discoveries,
stage_pair, check_apply. Only the main audit matrix is new.
**Raw evidence:** GENBIAS_ADV_RAW.txt (3 runs, md5
0d864f30e85479f3879ab41d1fc25e84, byte-identical).
**Determinism:** 3/3 identical.

## Verdict: H-GENBIAS-GENERAL KILLED (as a general bias)

The N-first search order is NOT a safe generality bias. It fixes
uniform-length reverse overfitting, and even fixes uniform-length
broadcast-last overfitting, but it introduces a STRICT REGRESSION on
uniform-length constant-2 broadcast: the old code finds the generalizing
constant program (5/5 held-out lengths); N-first selects the coincidental
N-using overfit n-2 (1/5). This is exactly the overfit swap the prereg
warned about, on a first-order task, not a pathological corner.

Explicitly NOT overturned: the frozen H-GENBIAS SURVIVES (4/4) verdict on
bars K-G1..K-G4. Those bars were frozen before execution and all still
pass. Per governance, new attacks cannot retroactively unpass frozen
bars. What dies is the broader claim that N-first is a safe general
solution to discovery overfitting. H-GENBIAS is reclassified: a
task-specific search-order patch with a demonstrated regression mode,
not a generality bias.

## G-A1: Exhaustive fitter audit (KILL criterion MET)

10 task x regime cells. N-first winner generalization on held-out
lengths (L=2..7; L=3..7 for const2 where the truth needs L > 2):

| task | regime | NEW winner (bytes) | NEW gen | OLD winner | OLD gen |
|------|--------|--------------------|---------|------------|---------|
| reverse | uniform | n-1-k | 6/6 | 3-K | 1/6 |
| reverse | mixed | n-1-k | 6/6 | n-1-k | 6/6 |
| blast | uniform | n-1 | 6/6 | const 3 | 1/6 |
| blast | mixed | n-1 | 6/6 | n-1 | 6/6 |
| bfirst | uniform | n-n = 0 | 6/6 | const 0 | 6/6 |
| bfirst | mixed | n-n = 0 | 6/6 | const 0 | 6/6 |
| const2 | uniform | n-2 | 1/5 | const 2 | 5/5 |
| const1 | uniform | N+(1-N) = 1 | 6/6 | const 1 | 6/6 |
| identity | uniform | K+(N-N) = k | 6/6 | k | 6/6 |
| identity | mixed | K+(N-N) = k | 6/6 | k | 6/6 |

Kill criterion: "the N-first winner FAILS to generalize while SOME
fitter in the 1055-program space generalizes." MET by const2 uniform:
NEW selects SUB(N,C2) = n-2, correct only at L=4 (1/5); the old code's
winner, constant 2, is in the same program space and generalizes 5/5.
The bias actively prefers the worse program.

## G-A2: Transfer head-to-head (help / hurt / neutral)

- HELP (2 cells): reverse uniform (1/6 -> 6/6), blast uniform (1/6 ->
  6/6). Note the old code ALSO overfit uniform blast to constant 3;
  the bias repaired a second overfit the original report did not
  discuss.
- HURT (1 cell): const2 uniform (5/5 -> 1/5). Strict regression.
- NEUTRAL (7 cells): all mixed-regime cells (affine constraint forces
  b to match truth when >= 2 lengths are present, so no coincidental
  N-using fitter can win); bfirst/const1/identity uniform, where the
  N-first winners are SYNTACTICALLY N-using but SEMANTICALLY identical
  to the truth (n-n=0, N+(1-N)=1, K+(N-N)=k). These cosmetic
  re-identifications expose the bias as syntactic, not semantic:
  prog_uses_n rewards the mere presence of an N node even when N
  cancels out.

## G-A3: Pathological N construction (KILL criterion MET)

The const2 uniform attack is exactly the preregistered construction:
truth = constant 2 (no N), coincidental N-using fitter n-2 fits the
uniform n=4 training, N-first selects it, it fails held-out (1/5).
The const1 uniform attack was predicted vulnerable (n-3 fitter exists)
but the audit shows the cancelling program N+(1-N) = 1 is enumerated
earlier and wins (6/6): the bias is saved there by enumeration-order
luck, not by principle. A bias whose safety depends on which
coincidental fitter the enumeration happens to reach first is not a
generality guarantee.

## G-A4: Source audit (PASS)

No test literals ("abcd", "hello", "dcba", "olleh", "efgh", "hgfe") and
no hardcoded program bytes in pdiscover_direct, try_discover_pass,
prog_uses_n, or pdiscover_dry. Test strings appear only in harness
mains. The bias is a pure search-order change, honestly implemented.
G-A4 PASSES; the kill comes from the mechanism's logic, not from
cheating.

## Why this happens (mechanism)

With uniform-length training, the affine fit a*k + n0*b + c is
underdetermined in b: any (b, c) with n0*b + c fixed fits. N-first is a
bet that the truth uses N. For reverse and broadcast-last that bet pays
off. For constant-2 broadcast the truth is constant, and the bet picks
n-2, which is wrong everywhere except the training length. No
search-order bias can principledly resolve this: with single-length
data, generality is underdetermined, and syntactic N-presence is not a
proxy for generalizability (n-n=0 is "N-using" and constant).

## Recommendations

1. Do NOT port N-first to the remaining single-pass discovery copies
   (proc_learn.zag, bridge_learn.zag, route_learn.zag, integ_learn.zag,
   proc_cond.zag) until the const-regression is addressed. Porting
   spreads the regression to bridge subset procedures trained on
   uniform-length data.
2. Honest repairs, in order of principledness: (a) varied-length
   training evidence (data, not bias; this is what accidentally saved
   H-UNIFIED); (b) post-discovery validation on held-out lengths when a
   second length can be obtained or synthesized; (c) a semantic
   generality criterion. Syntactic N-preference should be retired as a
   claimed generality mechanism.
3. Update CANONICAL_STATE.md: H-GENBIAS honest boundaries must record
   the const2-uniform regression and the reclassification to
   task-specific patch.
4. The unified learner's training should include a uniform-length
   constant task in its regression suite so this failure mode is
   caught by future discovery changes.

## Classification

Bounded L2+ red-team result. One new genuine failure mode found,
one unreported second fix found (uniform blast), mechanism honestly
bounded. The frozen H-GENBIAS (4/4) bars stand; the general-bias
interpretation is killed.

## Commits

- 66f4c324e: Prereg H-GENBIAS-ADV FROZEN (G-A1..G-A4)
- (this commit): Harness + raw outputs + adversary report
