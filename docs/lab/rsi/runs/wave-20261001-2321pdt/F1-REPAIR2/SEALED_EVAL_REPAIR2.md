# SEALED_EVAL_REPAIR2.md - F1-REPAIR2 sealed test results

Lane F1-REPAIR2, wave wave-20261001-2321pdt. Sealed runs executed
2026-10-02 ~00:45 PDT against the frozen F1 binary
`dev/f1_learn` (read-only copy of
`../F1/impl/f1_learn`, sha256
6f2b155b233a95ad1a8323e8565b9a798dc822db6eff57e065b71b5be8882847,
verified before running; match confirmed). 24 fresh sealed sum2
worlds (frozen 7300-series seeds, manifest sealed5/FIXTURE_SHA256.txt,
all hashes verified before runs). Frozen rule from
PREREG_REPAIR2.md (committed alone at b4dfa3f32 before any probe
was built, any fresh fixture was generated, or any fresh run
executed; implementation committed at 6bc6483c3; fixture manifest
committed at fed95fc76 before any sealed run).

No em-dashes are used in this document.

## 1. Determinism evidence

Each of the 48 sealed invocations (24 seeds x train/hidden) was
executed 3 times (runs5/1, runs5/2, runs5/3). All corresponding
outputs are byte-identical across the three repetitions
(cmp-verified, zero diffs). SHA-256 of all runs5/1 outputs is
recorded in runs5/DETERMINISM_SHA256.txt. The 24-seed set with 3/3
determinism per seed is complete (24/24). Zero NOTRIG worlds, zero
trace-parse failures.

## 2. Overfit rate on fresh worlds (frozen classification)

OVERFIT = hidden accuracy below 80 percent (f1_score acc on the
30-probe masked set, frozen pure-Zag scorer). CORRECT = at least
80 percent. The split is cleanly bimodal; no seed is near the
boundary.

| seeds | hidden | class |
|---|---|---|
| 18, 20 | 0/30 = 0% | OVERFIT |
| 19 | 3/30 = 10% | OVERFIT |
| 21 | 0/30 = 0% | OVERFIT |
| 0..17, 22, 23 | 30/30 = 100% | CORRECT |

Overfit rate: 4/24 = 17 percent. 3 of the 4 overfit seeds are
degenerate-path seeds (deg=1); seed 19 is a non-degenerate
overfit (first-trigger single doubling solved the 2-episode
buffer, later degenerate-form adds never repaired).

## 3. Part A: S-prime confirmation (frozen, conditioned on D)

Per-seed frozen S-prime S' (later-trigger burst to err_after=0,
any buffer size; pure-Zag r2sig) and POLICY-R check (pure-Zag
r2sig polok), with frozen labels:

| seed | trig | deg | S' | nrep | polok | label |
|---|---|---|---|---|---|---|
| 0 | 1 | 0 | 0 | 0 | 1 | CORRECT |
| 1 | 1 | 0 | 0 | 0 | 1 | CORRECT |
| 2 | 2 | 1 | 1 | 1 | 1 | CORRECT |
| 3 | 1 | 0 | 0 | 0 | 1 | CORRECT |
| 4 | 2 | 0 | 0 | 0 | 1 | CORRECT |
| 5 | 1 | 0 | 0 | 0 | 1 | CORRECT |
| 6 | 1 | 1 | 1 | 1 | 1 | CORRECT |
| 7 | 1 | 0 | 0 | 0 | 1 | CORRECT |
| 8 | 1 | 0 | 0 | 0 | 1 | CORRECT |
| 9 | 2 | 0 | 0 | 0 | 1 | CORRECT |
| 10 | 2 | 0 | 0 | 0 | 1 | CORRECT |
| 11 | 1 | 0 | 1 | 1 | 0 | CORRECT |
| 12 | 1 | 0 | 0 | 0 | 1 | CORRECT |
| 13 | 1 | 0 | 0 | 0 | 1 | CORRECT |
| 14 | 1 | 1 | 1 | 1 | 1 | CORRECT |
| 15 | 1 | 0 | 0 | 0 | 1 | CORRECT |
| 16 | 1 | 0 | 0 | 0 | 1 | CORRECT |
| 17 | 1 | 0 | 0 | 0 | 1 | CORRECT |
| 18 | 2 | 1 | 0 | 0 | 1 | OVERFIT |
| 19 | 1 | 0 | 0 | 0 | 0 | OVERFIT |
| 20 | 1 | 1 | 0 | 0 | 1 | OVERFIT |
| 21 | 1 | 1 | 0 | 0 | 1 | OVERFIT |
| 22 | 1 | 0 | 0 | 0 | 1 | CORRECT |
| 23 | 1 | 1 | 1 | 1 | 1 | CORRECT |

D-subset (deg=1): seeds 2, 6, 14, 18, 20, 21, 23 (D = 7 >= 6:
gate (a) passes). S'=1: seeds 2, 6, 14, 23 (all CORRECT).
S'=0: seeds 18, 20, 21 (all OVERFIT). misc_D = 0 <= 2.
Part A: PASS.

Secondary (unconditional, non-decisive): S' applied to all 24
seeds mispredicts 15/24 (the 15 non-degenerate CORRECT seeds
with S'=0, which need no repair). This is expected and is why
the frozen rule conditions on D, exactly as in F1-REPAIR.

## 4. Part B: POLICY-R on fresh worlds (all 24 seeds)

misc_B = seeds with polok=0: seeds 11 and 19 (misc_B = 2 <= 4).
Part B: PASS.

Per-burst contingency on the 14 fresh later bursts with at
least one construct (format ep,buf,ncon,dbl,last):

| seed | burst | dbl-first | complete | POLICY-R |
|---|---|---|---|---|
| 2 | 7,8,3,1,0 | yes | yes | hold |
| 6 | 3,4,3,1,0 | yes | yes | hold |
| 11 | 3,4,2,0,0 | no | yes | VIOLATION |
| 14 | 16,8,3,1,0 | yes | yes | hold |
| 18 | 5,6,1,0,6 | no | no | hold |
| 18 | 11,8,1,0,13 | no | no | hold |
| 19 | 3,4,1,0,4 | no | no | hold |
| 19 | 8,8,1,0,12 | no | no | hold |
| 19 | 12,8,1,0,6 | no | no | hold |
| 19 | 21,8,2,1,14 | yes | no | VIOLATION |
| 20 | 3,4,1,0,11 | no | no | hold |
| 20 | 5,6,1,0,14 | no | no | hold |
| 21 | 4,5,2,0,6 | no | no | hold |
| 23 | 14,8,3,1,0 | yes | yes | hold |

12/14 fresh later bursts satisfy POLICY-R. Both violations are
on non-degenerate seeds; POLICY-R holds on all 7 D-seeds
(polok=1) and on all 20 calibration D-seeds, i.e. 27/27
degenerate-path seeds across 5100/6100/7300.

## 5. The two violations (mechanistic analysis, post-hoc)

Seed 11 (non-D, CORRECT): first trigger solved the 2-episode
buffer with a single doubling (ADD r0,f0,f0, 10->0). The later
burst at ep 3 (buf=4) is [ADD r0,r0,f1 8->4; ADD r0,r0,f1
4->0]: accumulator-preserving first construct, yet the burst
completed. The preserved accumulator was already a clean
partial solution (r0=2x0), not a degenerate chain, so greedy
descent (+f1 twice) reached zero. POLICY-R's
accumulator-first-implies-stall direction assumed a degenerate
accumulator; it fails when the inherited accumulator is clean.

Seed 19 (non-D, OVERFIT): the later burst at ep 21 (buf=8) is
[ADD r0,f1,f1 38->36 (doubling first); ADD r0,r0,r0 36->14]
then STALL at 14. The doubling reset r0 to 2x1, but the
greedy second move on this buffer was the degenerate r0+r0
doubling, not the complementary add, and no third move
strictly improved. POLICY-R's doubling-first-implies-complete
direction assumed the post-doubling greedy path goes
+COMP,+COMP; it fails when the buffer favors the degenerate
second move even after a clean reset.

Refined gloss: a doubling first construct resets r0 to 2f and
replays first-trigger dynamics on the current buffer. Whether
the burst then completes depends on whether that buffer
favors the complementary add (repair, as in all D-seed cases)
or the degenerate doubling (stall, as in seed 19 ep 21).
POLICY-R is therefore a characterization of the typical
D-seed regime, not a universal burst law; its boundary is
exactly where the inherited accumulator is clean (seed 11)
or the post-reset buffer favors degeneracy (seed 19).

## 6. Verdict: REPAIR2-CONFIRMED (per the frozen decision rule)

Part A PASS (D=7 >= 6, misc_D=0 <= 2) and Part B PASS
(misc_B=2 <= 4). No bar was weakened; the rule fired exactly
as frozen in PREREG_REPAIR2.md section 3. The S-prime
relaxation (any buffer size) now holds on 27/27
degenerate-path seeds across three series (9/9 5100, 11/11
6100, 7/7 7300).

## 7. K-C0A audit (PASS)

Grep audit over all new lane code (dev/r2sig.zag,
dev/r2apply.zag, sealed5/*.sh): zero hits for forbidden
protected-semantic markers, downgrade kill-pattern markers,
and menu/kit/candidate-family markers. The probe and applier
are external trace readers; they contain no learner logic and
no semantic cases. The frozen binary was not modified.

## 8. Architecture accounting

0 cognition-substrate source lines added; no file outside this
lane touched; the F1, F1-FOLLOWUP, F1-BUFFER, and F1-REPAIR
lanes were read-only (sources extracted via git show from
recorded commits; binaries used read-only with sha256
verification). New code is sealed methodology only. No new
semantic cases, modes, bridges, routers, or handlers. No fix
is proposed for the F1 line.

## 9. Recommended next experiment

The two violations bound POLICY-R's scope precisely: test the
refined gloss (post-doubling second-move competition between
the complementary add and the degenerate doubling as a
function of buffer composition) with a fresh prereg on new
sealed worlds, predicting per-burst completion from the
second-move winner rather than the first-construct form. A
second open thread: seed 19 is a non-degenerate OVERFIT,
a class absent from the 5100/6100 series; its later
degenerate-form adds (r0+r0 at ep 3, partial +f0 adds) suggest
the degenerate path can be entered after the first trigger,
which the D definition (first-trigger only) does not capture.

Evidence paths (all under
docs/lab/rsi/runs/wave-20261001-2321pdt/F1-REPAIR2/):
- PREREG_REPAIR2.md (frozen definitions, rules, bars)
- dev/CALIBRATION_5100_6100_POLICY.md (training calibration)
- dev/r2sig.zag, dev/r2apply.zag, dev/r2sig, dev/r2apply
  (pure-Zag tools; validated on 5100/6100: exact calibration
  reproduction)
- dev/f1_learn, dev/f1_wgen, dev/f1_score (read-only copies;
  wgen verified byte-identical on the 6100 reference fixture)
- dev/ref_s4_train_0.ep (wgen reproduction reference)
- sealed5/ (24 fresh fixtures, gen5.sh, run_repair2.sh,
  FIXTURE_SHA256.txt)
- runs5/ (1, 2, 3 repetitions; DETERMINISM_SHA256.txt;
  fresh_table.txt; fresh_scores.txt; fresh_sigs.txt;
  verdict.txt)
