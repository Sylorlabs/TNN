# VERDICT — F26 EFFIC (Deliberation-Efficiency Head), mech 26

- **Date:** 2026-09-24 (PDT)
- **Authority:** `PREREG_FORKROUND.md` §3 (F26) + §5b (repaired TRAIN-COORD v2)
  + `ideas/native2_forks.md` FORK 3 (authoritative on mechanism).
- **Verdict: VOID** — prereg §5/§5b training checkpoint: the final fitted head
  violates vetoes V1 (theater) and V3 (underconfidence floor). Reported with
  evidence below; **no eval spend** (policy binary not built, battery not run).

## 1. Stillborn gate (§5) — LIVE

Within-leg std(q) on the 51 training legs (heldout=0, released cells;
q = cumE·1000/max(1,E_ref), cumE = f5, E_ref = lower-median cumE at
(family,depth)): **16/51 = 31.4%** of legs with std(q) < 100.
Gate (>50%) not triggered → **LIVE**. Full table: `analysis/stillborn_f26.out`.

## 2. Training (TRAIN-COORD v2, literal)

- Optimizer + inits recorded in `PROTOCOL.md` **before** the first run:
  init 0, order [b,w1..w9], ±50 then ±8 then ±1, 8 sweeps, strict-L accept,
  boxes [−1000,1000], vetoes on final answer only.
- Trainer binary SHA (×2 builds): `4bd5677a50bb2878e897c21d791c1c48b30188a210dc80e8de87b02ea5b1f035`
- Training ×2 → byte-identical params + logs:
  - params SHA: `1109bc86187522d7ad081874750d28c3cf31185a315090a2119f64eadd1ccf54`
  - log SHA: `3ab30fd4aa9434525183ff8658b05e199fd19bb8bbc59badf2d201a4fce913fd`
- **Fitted head (mode 0):** b=268, w1=472, w2=21, w3=0, w4=−18, w5=237,
  w6=104, w7=345, w8=468, **w9=+469**.
  - Kill (b) (w9≈0): **does NOT fire** — w9 is large positive, the sign the
    spec expected. The efficiency mechanism is live in the fit.
  - Objective Σ(C−1000y)² = 161,752,711 on 4222 training cells.
- **Base control (mode 1, same trainer, w9 frozen 0):** b=287, w1=471, w2=2,
  w3=0, w4=0, w5=253, w6=168, w7=345, w8=469; objective 185,574,230.
  f9 improves the fit (Δobj ≈ −23.8M) with near-identical w1..w8 —
  the efficiency feature carries real signal.

## 3. Final-answer vetoes (§5b) — the evidence

Computed in-Zag in the trainer log AND independently in Python
(exact-integer replica of the head incl. truncation-toward-zero division);
**both agree exactly**:

| Veto | F26 (mode 0) | Base (mode 1) | Bar |
|------|--------------|---------------|-----|
| V1 theater (V1+V2 on training cells) | **175** (V1=0, V2=175) → **VOID** | **175** (identical) → VOID | = 0 |
| V2 meanConfCorrect | 0.9620 (3732324/3880) → clear | 0.9502 → clear | ≥ 0.55 |
| V3 (family,depth) G < −0.080, n_rel≥8 | **7 slots** → **VOID** | bad → VOID | = 0 |

- V1 breakdown (F26): all 175 are **V2-type** (wrong→wrong, conf rising):
  trap 90, P 70, D 15. Zero V1-type (correct→wrong, conf non-decreasing).
- V3 slots (F26): O d1 G=−0.400, O d2 −0.256, O d4 −0.217, O d8 −0.176,
  O d16 −0.153, cost d1 −0.196, revoke d1 −0.194.
- **The base control fails identically (V1=175, V3 bad)** — the theater is
  endemic to the squared-error-fitted linear head on these features, NOT
  caused by f9. f9 neither creates nor removes it.

## 4. Why the vetoes fired (mechanistic autopsy, not a tune-up)

1. The v2 objective (pure squared calibration error) fits margin-positive
   weights (w1=472 on clamped margin, w8=468 on max margin drop, w5=237,
   w7=345). On adversarial families (trap/P/D), wrong items' margins RISE
   with depth (the learner gets more confident in the wrong answer), so the
   head's confidence rises on wrong→wrong pairs — 175 V2 theater transitions.
   The V1 veto exists precisely to reject this head. It functioned as designed.
2. The same fit is severely underconfident on O-family and cost/revoke d1
   (G down to −0.400): the linear head cannot simultaneously match the
   high-confidence honest legs and the low-accuracy O legs — squared error
   splits the difference and V3 rejects the casualty slots.
3. This is the ideas file's flagged B2 risk realized ("f9 is not monotone
   along a path... V1 veto guards training") — except the theater is in the
   shared linear machinery, present with and without f9.

## 5. Adjudication (§10)

- **VOID** (§5/§5b). Not STILLBORN (gate: 31.4% < 50%). Not KILLED — the
  fork's falsification triggers were never reached (no eval):
  (a) high-depth B3/B8 vs base: untestable, no eval;
  (b) w9≈0: does NOT fire (w9=+469);
  (c) B4<0.50 honest: untestable, no eval.
- The F26 mechanism (deliberation-efficiency discount) was **never tested on
  the battery** — it died at the checkpoint because the shared trainer's
  objective cannot produce a veto-satisfying linear head on this feature set.
- **Generalization warning for the round:** TRAIN-COORD v2 as specified
  (vetoes removed from search, applied to the final answer) finds the
  unconstrained squared-error optimum, which violates V1/V3 on trap/P/D/O
  with AND without the new feature. F24/F27 (same trainer) and an F25 v2
  rebuild are likely to hit the same wall. v1 was analytically locked
  (vetoes in search); v2 is analytically VOID-bound (vetoes only at the end)
  for linear heads on these features. Whether a veto-aware search exists
  within the frozen spec is a **prereg-amendment question for the
  coordinator** — not fixed unilaterally here.
- Failure-mode mapping: the vetoed dynamic (margin-positive linear head
  gaining confidence on wrong items with depth on adversarial families) does
  not match carried FMs 1–8 cleanly; it is the dynamic the B2 bar exists to
  catch. Proposed as a candidate FM entry for the round's `VERDICT.md`
  (coordinator's adjudication), not numbered unilaterally here.

## 6. Artifacts (all in `fork_round/f26_effic/`)

- `PROTOCOL.md` (recorded pre-build), `src/train_f26.zag` + 7 harness
  modules (byte-identical, SHA-verified), `params/f26_params.zag`,
  `params/f26b_params.zag`, `logs/train_f26_run{1,2}.tsv`,
  `logs/train_f26b_run{1,2}.tsv`, `analysis/stillborn_f26.out`, this verdict.
- Not built (VOID, no eval spend): policy binaries, 37-leg battery.
- Determinism: builds ×2 byte-identical; training ×2 byte-identical
  (params + logs); veto counts reproduced by an independent Python
  exact-integer implementation.

## 7. Commit SHAs

- `2a5db535fad332d3e931e113d1e5d8ecc543776b` — F26 EFFIC fork tree
  (PROTOCOL.md, VERDICT_F26.md, trainer source + 7 byte-identical harness
  modules, params, training logs ×2, stillborn table), branch
  `tnn-native-lab`, repo `sylorlabs/TNN`, paths under
  `docs/lab/deliberation_depth/monotonicity/training/fork_round/f26_effic/`.
- (this section's fill-in committed as a follow-up amendment)
