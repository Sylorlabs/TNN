# VERDICT — B-T4 support-gap recruitment hard battery (R0 redo, 1x)

Crew B-DYNSG · Track R0 · 2026-09-21 · branch `tnn-native-lab`
Prereg: `units/PREREG_FREEZE.md` §2 (Micah signed 2026-09-21). R-9: **1x ONLY**.
Binary: `units/r0/impl/support_gap/sg_b4.zag` → `sg_b4 <leg 0|1> <perturb 0..4>`.
Pure Zag. Zero RNG in AI decision paths. Byte-identical reruns (M8 N=5).

## Frozen rule (R-8)

> The teacher supplies grounded whole experiences only; the learner recruits
> the largest unsupported span iff `support >= learned_support_min AND
> (support − runnerup_support) >= learned_margin`, else abstains with a reason
> code: `-1` (`d2`: 1=low support, 2=margin failed, 3=bank full, 4=no gap,
> 5=span already issued).

Recovered thresholds: leg0 `support_min 3, margin 2`; leg1 `support_min 4,
margin 3`.

## Battery design (deterministic, preregistered-in-source)

Per exposure `e = 1..16`, fresh arena per case:
- Teacher pre-seeds two live context chunks (`ctxAAAAA`, `ctxBBBBB`; 8 grounded
  observations each, then promote). The gap target is **never** promoted by the
  teacher — it must be *recruited* by the learner.
- Teacher supplies a complete grounded whole experience: every span of length
  2..8 at every stream position, observed `e` times (all recall-success
  labels). The learner sees whole streams; the target span is never handed
  over directly.
- **Clean** (8 reps/exposure): one 6-byte unsupported gap, no runner-up.
  Rule-correct decision: abstain `d2=1` for `e < minsup`; recruit the exact
  6-byte gap (start 16, len 6, byte-exact) for `e >= minsup`.
- **Contested** (4 reps/exposure): 6-byte gap vs a 5-byte runner-up gap with
  *equal* support. Rule-correct: **never** recruit — abstain `d2=1` while
  `e < minsup` (support clause fires first), `d2=2` (margin failed) once the
  support clause passes. This ordering was caught by the battery's own
  expected-value checks during development and is asserted, not assumed.
- **Controls**: fully-covered stream → `-1`/`d2=4` (no gap); target span
  promoted then archived → `-1`/`d2=5` (span already issued).

## Measured curves — no collapse at 1 exposure, no degradation at 16

**Clean sub-battery** (recruited / abstained / correct-decision, n=8):

| e | leg 0 | leg 1 |
|---|---|---|
| 1 | 0 / 8 / **8** (abstain d2=1) | 0 / 8 / **8** (abstain d2=1) |
| 2 | 0 / 8 / **8** (abstain d2=1) | 0 / 8 / **8** (abstain d2=1) |
| 3 | **8** / 0 / **8** (recruit) | 0 / 8 / **8** (abstain d2=1) |
| 4–16 | **8** / 0 / **8** (recruit) | **8** / 0 / **8** (recruit) |

Recruitment onset lands exactly on the recovered bars (leg0 at e=3, leg1 at
e=4). Every recruited chunk was verified byte-exact against the gap.

**Contested sub-battery** (n=4): **0 recruitments at all 16 exposures, both
legs.** Abstention reasons follow the rule's ordered conjunction exactly:
`d2=1` for e<minsup, `d2=2` for e≥minsup. Correct-abstain rate 4/4 everywhere.

**Controls** (both legs): `SG_C1_COVERED`: rid `-1`, d2 `4` ✅;
`SG_C2_ARCHIVED`: rid `-1`, d2 `5` ✅.

Full per-case table: `sg_table.csv` (256 clean + 128 contested rows).

## R-5 floor — PROPOSED, formal bar PENDING-MICAH-AMENDMENT

The frozen prereg states no R-5 floor, and this battery does not invent one.
Measured: correct-decision rate **8/8 at every exposure, both legs** (clean),
**4/4** (contested).

**Proposed floor** (for Micah's amendment decision): *minimum correct-decision
rate ≥ 7/8 per exposure across 1–16, both legs, with the contested
abstention rate exactly 8/8 (the margin rule must hold exactly — any
recruitment of a margin-failing span is a rule violation, not a statistic).*
Rationale: the rule is a deterministic conjunction, so near-perfect
correct-decision is the expectation; the 7/8 (not 8/8) allows for
implementation edge cases without masking systematic failure. The measured
battery exceeds this proposal everywhere.

**Formal B-T4 bar: PENDING-MICAH-AMENDMENT.** Nothing in this verdict asserts
a PASS against R-5.

## Other checks

- STORESEQ readback probe (`r0_probe_run`): 0 fails, both legs (hard gate —
  nonzero would abort before battery logic).
- Battery expected-value self-checks (`SG_FAILS_TOTAL`): 0, both legs.
- M8 N=5 adversarial perturbations: **PASS**, both legs (stdout/stderr/capture
  lines byte-identical across all 5 modes; exit 0 everywhere).
- M8 captures (canonical, perturb 0):
  - leg0: `STORE_IMAGE d3af411124d268cad6fdc5c682d96771c04f3a122fdb5b2d4514e621b2b4525a`, `LEDGER 563518471`
  - leg1: `STORE_IMAGE 491af1c409d0d7e0f608da59652f15b497f525e23f86c141113ee154762dbed8`, `LEDGER 1232367883`
- **METRICS.md vs ARM_INTERFACE.md**: schema conflict noted per instructions;
  this battery follows `METRICS.md` strings.
- **ZNC-2026-09-21-002** applies here too (store image built via
  word→byte decomposition, not `slice as *u8`).

## Files

- `units/r0/impl/support_gap/sg_b4.zag` — battery source (committed)
- `units/r0/evidence/support_gap/sg_leg0.log`, `sg_leg1.log` — canonical outputs
- `units/r0/evidence/support_gap/sg_table.csv` — 384-row per-case table
- `units/r0/evidence/support_gap/b4_m8.json` — gate verdicts
- `units/r0/evidence/support_gap/VERDICT_B4_SUPPORTGAP.md` — this file
