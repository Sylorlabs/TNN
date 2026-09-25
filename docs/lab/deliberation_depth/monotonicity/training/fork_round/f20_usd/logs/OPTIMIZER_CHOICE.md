# F20 USD — optimizer choice + inits (recorded BEFORE first training run)

Date: 2026-09-24. Author: F20 build crew (subagent).

## Optimizer
Deterministic integer online SGD — a mechanical extension of the frozen
PREREG_TRAINING.md §5 rule to the 9th weight. Zero RNG. Fixed file order.
Integer arithmetic with truncation-toward-zero division (tr_tdiv), same as
the frozen trainer.

Per released training cell (rel4=1, heldout=0), with
  f9 = max(0, (f6+f7)/2 − f5)            (integer ops; f6,f7,f5 in thousandths)
  C  = clamp((Σ_{i=1..8} w_i·f_i − w9·f9)/1000 + b, 0, 1000)
  Y  = 1000 if correct else 0
  rise = max(0, C − C_prev) iff same item has an earlier M4-released depth
         with y_prev=0, y=0 (C_prev recomputed with CURRENT weights, w9 term
         included — the theater penalty, same construction as §5)
  L = (C−Y)² + 2·[Y=0]·C² + 4·[rise>0]·(C−C_prev)²

Updates (DIV=4000000, frozen):
  w_i ← w_i − tr_tdiv(2(C−Y)f_i + 4[Y=0]·C·f_i + 8·rise·f_i, DIV)   i=1..8
  w9  ← w9 + tr_tdiv(2(C−Y)f9 + 4[Y=0]·C·f9 + 8·rise·f9, DIV)
        then PROJECTION: if w9<0 { w9=0 }   (after EVERY cell update;
        ideas/native1_forks.md Fork 1: "w9 ≥ 0 enforced by projection in
        the fitter (if w9<0 → 0 after each update)")
  b   ← b − tr_tdiv(2(C−Y)·1000 + 4[Y=0]·C·1000 + 8·rise·1000, DIV)

G-batch per epoch (the law as a training signal, unchanged from §5):
per training family F, adjacent depth pair, G in thousandths over
M4-released training cells with the CURRENT head (w9 term included):
if G_F(d+1) > G_F(d): b ← b − tr_tdiv(G_F(d+1) − G_F(d), 4).

## Curriculum / schedule
Phases A→B→C (admit/revoke/logic/cost d1..16; ceiling P/D even replicates
d1..64; trap d1..16, ceiling O even replicates d1..64, redteam d1..16),
2 epochs per phase per pass, passes=100 (600 epochs). Heldout cells
(odd P/O/D replicates) excluded from training AND from the G-batch,
exactly as the frozen trainer. Fixed file order = features.tsv row order.

passes=100 chosen to match the deepest trained-policy precedent
(SR-S1/SR-S9 100× Stage-1, mt_params_100x): maximal training gives the
fitter the fullest chance to lift w9>0, so a 0-fit (kill (c)) is maximally
meaningful rather than an undertraining artifact.

## Inits (frozen)
w1=1000, w2..w8=0, w9=0, b=0.
The F20 head therefore STARTS identical to the frozen §4 init
(M4-with-harness-confidence); the USD discount is LEARNED, not gifted.
If final weights equal init, nothing was learned (detectable in the log).

## Sanity direction of the w9 gradient
Trap cell (Y=0, C high, f9>0): +2(C−Y)f9 +4·C·f9 > 0 → w9 increases
(discount strengthens on confident-wrong trap survivors). Honest-correct
cell (f9≈0 by the mechanistic argument): no w9 movement. Correct cell
with f9>0 (the adversarial note's worry): 2(C−Y)f9<0 → w9 decreases,
and B4b watches for the re-weighting failure mode.

## Kill (c) operationalization (recorded before eval)
The fit is GLOBAL (one w9 for all legs), not per-leg. Kill (c) ("w9 fits
to 0 on a majority of legs") is therefore operationalized as:
KILL iff fitted w9 = 0 — the discount is then identically zero on all 37
eval legs (a strict majority). Additionally, per-leg discount activity
(mean w9·f9/1000 over M4-released cells) is reported as telemetry for all
37 legs; a live w9 with <1-thousandth mean discount on a majority of legs
would be reported as dead-weight evidence alongside the verdict.

## Gates honored
Pure Zag, zero RNG, []u8 arenas + au_get32/au_get64 LE accessors
(ZNC-2026-09-21-007), no fn named zalloc, no slice > 2^25 bytes,
pinned toolchain only (sha256 498abcb5…), A/B byte-identical builds,
training run twice → byte-identical params, B9 = 100% release+correct
identity vs M4.
