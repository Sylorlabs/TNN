# F30 THAC — VERDICT

Mechanism 30: Two-Head Adversarial Cap. PREREG_FORKROUND.md §3 F30 (frozen v2);
mechanism authority `fork_round/ideas/fable_forks.md` Mechanism C.
Frozen authority commit: `3a2eef44` (`sylorlabs/TNN`, `tnn-native-lab`).
Date: 2026-09-25. Pure Zag, zero RNG, pinned toolchain
`znc_linux_x86_64_abed8aa1` (SHA-256 `498abcb5...38e7e58ef`).

## Verdict: VOID (PREREG_FORKROUND.md §5)

The fork's novel intervention — the adversarial censor — is provably dead at
the training checkpoint. Per §5 this is reported with evidence, not killed.

### Evidence

1. **Censor never engaged.** `b_c = 0` = init after 600 epochs; `n_adv = 0`
   (censor adversarial updates) on every one of the 600 epoch log lines
   (`logs/train_f30_a.tsv`, col 17). The pre-registered liveness signal
   (`logs/OPTIMIZER_CHOICE.md`, recorded before training) was `b_c < 0`.
2. **Predictor = frozen baseline exactly.** `n_rev = 0` on all 600 epochs
   (loss reversal never fired); final weights `w1=1000, w2..w8=0,
   b_P=-100387` are numerically identical to the frozen MT-CONF 100x weights.
   Training twice produced byte-identical params and logs.
3. **`P ≡ 0` analytically.** With `b_P = −100387` and max `f1 = 1000`,
   `clamp(f1 − 100387, 0, 1000) = 0` on every cell.
4. **Censor vacuous at eval.** Full 37-leg battery (`run_eval.sh f30full`):
   PASS=37 FAIL=0, all A/B byte-identical. Bind rate `bind01 = (C_n < P)` =
   **0/4467 released cells on every family** (P ≡ 0, C_n ≥ 0 → min(P,C_n) = P
   always). Delivered head is numerically the §5 clamp attractor; the censor
   contributes nothing.
5. **Answer channel intact.** B9 release+correct identity vs M4 = 5240/5240
   (the M4 skeleton was never touched).

The THAC two-head mechanism was therefore never instantiated: the eval
artifact is the frozen §5 baseline wearing a decorative cap. The fork's
mechanisms were never tested (cf. F25 v1 VOID precedent).

### Kill-bar table (supporting evidence, not adjudication)

| Bar | Result |
|---|---|
| B1 1→0 transitions | 0 → PASS |
| B2 theater V1/V2 | 0/0 → PASS |
| B3 law (strict) | 2 G-violations (redteam; same 2 as NEC m9) → FAIL |
| B4 non-degenerate | meanConfCorrect = 0.0000 → FAIL (kill (b): 4 honest-leg hits) |
| B4b honest floor | 0.0000 on admit/cost/logic/revoke → FAIL |
| B5 separation | 0.0000 → FAIL |
| B6 recall | 1.0000 every family (M4-identical) → PASS |
| B7 abstention | 773/5240 = 0.1475 → PASS |
| B8 amended §4b | FAIL (vacuous) on 5 fams; PASS on ceiling D, ceiling P; VOID on redteam/trap |
| B9 frozen channel | 5240/5240 = 100% → PASS |
| B12 recorded | 0 crossings |
| B13 floor | 33 (F,d) with G < −0.100 → FAIL |
| B3pi recorded | 0 rising / 3467 pairs |
| Kill (a) | 0 hits → clear |
| Kill (b) | 4 hits → would KILL |
| Kill (c) | non-binding on 4467/4467 = 100% > 98% → would KILL (decorative) |
| NEC m9 deltas | redteam Gviol 2 vs 2 (no change); ceiling O 0 vs 4 (blanket −1.0, not a win) |

Full table: `analysis/killbars_f30.txt`.

### Failure mode: #9 — adversarial starvation (NEW, per §7)

The censor's training signal (predictor overconfidence, `P > Y`) is destroyed
by the predictor's own G-penalized collapse before the censor can learn. The
frozen §5 G-batch drives `b_P → −100387` (hence `P ≡ 0`) during phases A/B;
phase C — the only phase with wrong released cells — is therefore reached
with the predictor already at the clamp attractor, so `P_new > Y` never
occurs and the adversarial objective (`b_c −= 1` per overconfident cell)
fires zero times in 600 epochs. A suppress-only cap composed over a collapsed
predictor is vacuous: `min(P≡0, C_n) = P`, and the censor can never bind
(`C_n < P = 0` impossible). None of the ideas file's Q3 guesses for THAC
((3) uniform-manifold escape, (5) mask-invisible depth schedule) predicted
this: the censor died of starvation, not of over-suppression.

### What this rules out

Training the censor adversarially against a G-penalized predictor is
self-defeating under the frozen curriculum: the G-penalty removes the very
overconfidence the adversary needs to see. A live THAC would require either
(a) a predictor that retains overconfidence into phase C (e.g. no G-batch —
but that contradicts the frozen "G-penalized loss" spec), or (b) the censor
training against a frozen overconfident snapshot rather than the live
collapsing predictor. Both are different mechanisms, not this fork.

### §10 adjudication

**VOID.** Does not advance. No §6 horizon run (nothing live to extend).
