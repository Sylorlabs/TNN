# LH-P3 — P3 ADAPTIVE-EPS: adoption & head-to-heads (Agent E4)

Date: 2026-09-19. All work ran on this Linux VM. Zag only, no Python. No git push.

P3 = R34 rule with adaptive exploration: explore iff `rng % period == 0`;
under `learn==1`, negative reward decrements `period` toward 2, positive
increments toward 20. Init `period=5` reproduces R34's fixed 1/5 rate, so any
difference vs the R34 baseline isolates the adaptation mechanism.

## 1. Integration

- Core: `toolchain/r34v3/r34_p3_learner_core.zag`
  (sha256 `4aa6d6b6a7103eb2c8f57117a5545dc8de99e92190196dd4656bce704f14bc1e`).
  Preserves all `r34v3_*` names; adds `explores` and `period` fields.
- Wire format v4 (`R34CLV04`/4), `R34V3_STATE_BYTES=168`: explores at offset
  96, period at 100, zero padding `[104..136]`, SHA256 over `[0..136]` stored
  at `[136..168]`. (Bumped from 160 per review: the new fields no longer sit
  in the old reserved region. Learning dynamics are unchanged by the bump —
  post-bump fingerprints reproduce the pre-bump values exactly.)
- Static isolation: no world/checkpoint import, no `cw_`/`CWOutcome`, no
  `cl_checkpoint_`, no regime symbol, no world/checkpoint transport sizes in
  the core. Canonical `r34_learner_core.zag` verified byte-identical
  (`canonical_core_unmodified=true` in every evidence bundle).
- Harnesses: `lh_c1_p3.zag` / `lh_c1_fixed.zag` (C1),
  `lh_p3_c2.zag` (C2), `lh_p3_c3.zag` / `lh_fixed_c3.zag` (C3),
  `lh_p3_checkpoint.zag` (checkpoint/continuation/refusal),
  `lh_p1_trial.zag` / `lh_p1_baseline.zag` (P1 stretch).
- Runner: `run_p3.sh` with modes `c1|c2|c3|ckpt|p1`; every run emits
  `RECEIPT.txt` (`failures=0` throughout), `SHA256SUMS`, and per-command
  stdout/stderr/exit captures. `scientific_exposure=0` on all receipts.

## 2. Checkpoint / continuation / refusal (new `ckpt` evidence)

`EVIDENCE_20260919T222454Z_ckpt`, `failures=0`.
- Full campaign passes: baseline 8/16, train A/B, evalA=16/16, evalB=16/16,
  two contexts recruited, return-A 15/16 with zero weight updates and
  `active=0`, 48 training updates, disabled-control and scramble gates pass,
  same-seed determinism (learner, world, stream) passes.
- 168-byte wire roundtrip passes; inner-state tamper refused (`cl_corrupt`);
  period-field tamper refused.
- P3-specific: `explores=3 > 0`, `period=20` (adapted up from init 5, within
  `[2,20]`).
- Mid-episode checkpoint (pending=1) written under quarantined parent tag
  `P3_QUARANTINED_PARENT_V1`; reload continuation reproduces the
  no-checkpoint reference exactly (state line and continuation positives
  match: `checkpoint_continuation_match=true`).
- Corrupted checkpoint refused (`P3CKPT_REFUSAL,2005` = `cl_corrupt`);
  torn checkpoint refused (`P3CKPT_REFUSAL,2001` = `cl_bad`).

## 3. C1 — 10× A(24)/B(24) head-to-head (`EVIDENCE_20260919T222501Z_c1`)

Matched learner/world seeds 12001/1201, 480 updates, one lineage per arm.
`train A/B; explores` per block:

| block | P3 A/B | P3 expl | fixed A/B | fixed expl |
|---|---|---|---|---|
| 1 | 22/20 | 5 | 18/18 | 11 |
| 2 | 22/23 | 1 | 19/20 | 7 |
| 3 | 22/21 | 3 | 20/18 | 8 |
| 4 | 22/21 | 3 | 19/19 | 8 |
| 5 | 23/21 | 2 | 19/20 | 7 |
| 6 | 22/21 | 3 | 16/18 | 12 |
| 7 | 20/21 | 5 | 16/20 | 10 |
| 8 | 21/22 | 3 | 21/19 | 7 |
| 9 | 21/22 | 3 | 17/20 | 9 |
| 10 | 23/22 | 1 | 21/21 | 5 |

- Training positives: P3 218+214=432/480; fixed 186+193=379/480.
- Exploration: P3 29 vs fixed 84 → 55 fewer, **65.5% saving** (compounds at
  10× vs the ~53% short-trial figure).
- Endpoints: all 20 A/B eval probes 16/16 both arms; return-A 15/16 both;
  switches 19 both; final fingerprints P3 710022 / fixed 642515.
- Same-seed determinism + world equality pass; `failures=0`.

## 4. C2 — 12 alternating visits (`EVIDENCE_20260919T222510Z_c2`)

Seeds learner 48111 / world 281. Return-A visits 2,4,6,8,10 all 16/16
(≥15/16 gate); every eval 16/16 with zero updates during probes. Endpoint:
updates 288, explores 16, period 20, switches 11, fp 754021.
`P3C2_FAILURES,0`; determinism passes.

## 5. C3 — 10% reward corruption (`EVIDENCE_20260919T222513Z_c3`)

Matched seeds 5555/51; corruption seeds 5600, 7777, 4242. All arms run twice,
determinism passes, all receipts `failures=0`. Collapsed probes (of 20/seed):

| corr seed | P3 collapsed | fixed collapsed | switches P3/fixed |
|---|---|---|---|
| 5600 | 2 (2-B, 7-A) | 2 (same) | 79/71 |
| 7777 | 3 (5-A, 7-B, 10-B) | 2 (7-B, 10-B) | 98/84 |
| 4242 | 3 (4-A, 6-B, 8-B) | 7 (1-B, 2-B, 3-A, 4-A, 6-B, 8-A, 8-B) | 97/98 |

- Totals: P3 8/60 collapsed probes vs fixed 11/60; switches 274 vs 253
  (+21, +8.3%).
- Verdict: **mixed mechanism**. Adaptive exploration modestly dampens
  aggregate collapse count but does not cure corruption fragility, and
  corrupted negatives amplify context switching. Per-seed effect is
  inconsistent (equal / worse / substantially better).

## 6. Stretch P1 — STRUCT-PROMOTE (`EVIDENCE_20260919T222250Z_p1`)

Implemented per `wave2/ruleslab/PREREG_P1_STRUCT_PROMOTE.md`: dual
accepted/candidate 2×2 tables; diagnosis on negative non-explore reward or a
16-episode timer; candidate policy measured for a 16-episode probe window
with learning frozen; PROMOTE iff candidate per-arm success ≥ accepted
per-arm success on every arm, else rollback (re-fork candidate). Ledger
emitted per gate. Trial: rules-lab A/B/return protocol
(base16→trainA40→evalA16→trainB40→evalB16→returnA16), world seed 17, learner
seeds 7331/12345/999, vs R34 baseline on the same protocol. `failures=0`,
same-seed determinism passes, P1 core isolation passes.

| seed | P1 trainA/trainB pos | base trainA/trainB pos | P1 evalA/evalB/retA | base evalA/evalB/retA | diag/prom/rb | probe eps |
|---|---|---|---|---|---|---|
| 7331 | 34/32 | 35/33 | 16/16/15 | 16/16/15 | 7/6/1 | 112 |
| 12345 | 34/29 | 35/30 | 16/16/15 | 16/16/15 | 7/6/1 | 112 |
| 999 | 35/33 | 36/34 | 16/16/15 | 16/16/15 | 7/6/1 | 112 |

- Lifetime per-arm ok (accepted policy): P1 121/118/123 of 144 vs baseline
  123/120/125 — P1 trails by exactly 2 per seed (accepted table decides off
  the last-promoted snapshot, so it lags the live candidate during
  training).
- Ledger (seed 7331): diags 1–3 promote the (0,0) policy in trainA
  (candidate 16/16 vs accepted choosing the failing arm); diag 4
  **rolls back** — candidate probed only arm (1,1), failing the every-arm
  gate on (0,0); diags 5–7 promote the (1,1) policy once the base window
  shows evidence. The gate works as preregistered.
- Cost: 112 probe episodes per 144 training episodes (~78% overhead).
- Against the prereg: the gate is live (not vacuous — 6/7 promotions);
  **endpoints are identical to R34, not strictly better** (evalA/evalB
  16/16, return-A 15/16 both arms, all seeds — R34 is already at ceiling on
  this clean protocol, so the predicted retention advantage cannot show);
  per-arm training tallies are slightly worse (−1.4%). By the prereg's
  falsification reading on per-arm tallies, the structural framing adds
  nothing on the clean protocol. The natural next test is the C3 corruption
  protocol, where quarantining damage in the candidate is the hypothesized
  win — not run here.

## 7. Recommendations

1. **Adopt P3 as the default for clean long-horizon work.** It reproduces
   R34's endpoints exactly (16/16 evals, 15/16 return-A across C1/C2 and the
   checkpoint campaign) while cutting exploration 65.5% at 10× blocks, and
   the 168-byte v4 wire roundtrips with continuation/refusal fully covered.
2. **C3 caveat stays attached:** under 10% reward corruption P3 reduces
   collapses 11→8 but increases switching; do not claim robustness.
   Switch-rule repair is still the open item.
3. **P1: do not promote on the clean protocol.** Mechanism verified live
   (promotions + a correct rollback, coherent ledger), but it costs ~78%
   probe overhead for endpoints identical to R34 and slightly worse training
   tallies. If pursued, test it under corruption, where the quarantine
   hypothesis actually bites.

## Evidence bundles

- `EVIDENCE_20260919T222501Z_c1` — C1 (wire bump rerun)
- `EVIDENCE_20260919T222510Z_c2` — C2 (wire bump rerun)
- `EVIDENCE_20260919T222513Z_c3` — C3 (wire bump rerun)
- `EVIDENCE_20260919T222454Z_ckpt` — P3 checkpoint/continuation/refusal
- `EVIDENCE_20260919T222250Z_p1` — P1 stretch (clean)
- Superseded pre-bump: `EVIDENCE_20260919T221740Z_c1`,
  `EVIDENCE_20260919T221800Z_c2`, `EVIDENCE_20260919T221821Z_c3`
  (identical learning fingerprints; wire container was 160).
- Superseded P1 attempts: `EVIDENCE_20260919T222037Z_p1` (compile typo),
  `EVIDENCE_20260919T222054Z_p1` (stream value→pointer bug; see note).

Note (Zag footgun found while debugging P1): passing a struct *value* where
a `*T` parameter is expected compiles but operates on a temporary — the
caller's struct is never updated. In `lh_p1_trial.zag`/`lh_p1_baseline.zag`
the stream init/accept calls had to be `&stream`. Worth a toolchain-level
warning someday.

## ⚠️ Contamination notice — 2026-09-20 (R34 hidden-randomness remediation)

**Status: QUARANTINED (comparisons).** LH-P3's own P3 core
(`r34_p3_learner_core.zag`) uses a seeded adaptive-exploration rule that is
preregistered as the mechanism under test (deliberate design, not hidden).
However, every head-to-head comparison in this document is against the R34 v3
baseline, whose training ran with `explore_enabled=1` — engaging the hidden
seeded LCG (`r34v3_rng`) in `r34v3_choose`, a violation of the no-randomness
law (r34 RNG probe, workstream 2/8, commits `072f25aa` / `4976cbf5` on branch
`tnn-native-lab`; Micah's ruling: REMEDIATE). The P3-vs-R34 comparisons —
including the recommendation to "adopt P3 as the default" — may not be cited
as canonical until the baseline is re-run clean (deliberate or state-varying
exploration, no LCG).
The original text above is left intact for the record.
