# VERDICT V2-C (pure-Zag battery) — DEAD on RK-3 (preregistered); KD-1 FAILS by measurement

**Fork:** V2-C ("knowledge-first") — pure-Zag structural detectors (vknow.zag) +
  R2-4 gate (memgate.zag, byte-identical) + R2-4 deliberation (deliberate.zag)
**Battery:** 11,840 trials (10,915 R2A: 5,100 normal + 5,815 adversarial;
  925 harness: 370 primary + 370 noise + 185 adversarial), frozen order per
  PREREG_V2-A §3. dmask=4095.
**Date:** 2026-09-24
**Prereg:** `senses/pam-rebuild/v2/preregs/PREREG_V2-C.md` (frozen) +
  `PREREG_V2-C_AMEND1.md` (commit b81fa1b6693ee792a37f1ea4f7ba88eb3dfb821c, frozen)
**Implementation:** `senses/pam-rebuild/v2/forks/V2-C/src/` on branch
  `tnn-native-lab` (vsense_c_zag.zag, vknow.zag, memgate.zag, substrates,
  CALIBRATION_C_ZAG.md). Binaries built with pinned toolchain
  `znc_linux_x86_64_abed8aa1` (SHAs in RUNLOG.md). No source modified for this
  battery. Python used only for glue/scoring; all mechanisms pure Zag.
**Runs:** 3 full runs, byte-identical dispositions + ledger + metrics (B6 hard
  kill — PASS). Independent Python hash-chain ledger verification passed all
  3 runs (11,840 links each). Tracker vs memgate: 0 mismatches.

## Bars (measured, identical across 3 runs)

| Bar | Frozen bar | Measured | Verdict |
|-----|-----------|----------|---------|
| KD-1 adversarial wrong-high-conf | ≤537 | **675** | **FAIL** |
| KD-2 per-family | reported | see table | reported |
| RK-1 false permanent installs / 11,840 | ≤3% | 0.0% (0) | PASS |
| RK-2 wrong-HC reaching permanent install | ≤1% | 0.0% | PASS |
| RK-3 correct-HC reaching PASS+install | ≥85% | 14.6% | **FAIL (expected death)** |
| RK-5 wrong-HC → FAIL/UNRESOLVED over indep. evidence | ≥90% | 99.0% | PASS |
| B5 false permanent installs, adversarial | ≤3% | 0.0% | PASS |
| B1 frozen-370 primary judgment accuracy | ≥60% | 87.3% | PASS |
| B6 3× byte-identical + ledger verified | required | PASS | PASS |

## KD-1 decomposition (measured vs frozen R2-4 baseline 1,075)

| Family | R2-4 baseline | V2-C (dmask=4095) | Detector | Outcome |
|--------|--------------|-------------------|----------|---------|
| PTC-2 | 400 | 0 | D1 glide-gate | WORKS (caps to 650; 400/400 fired) |
| CCN-1 | 335 | 335 | D3 opposite-cast+texcorr | **NEVER FIRES** (see below) |
| COL-2 | 313 | 313 | D4 disabled | expected (0%) |
| CCN-2 | 17 | 17 | D5 | no reduction on wrong-HC |
| TMB-1 | 6 | 6 | D9 disabled | expected |
| harness adv | 4 | 4 | — | expected |
| **Total** | **1,075** | **675** | | **FAIL vs ≤537** |

Measured reduction: 400/1,075 = 37.2% (D1 only).

## KD-2 (COL-2 reduction specifically requested)

COL-2: 313 → 313 = **0% reduction** (D4 disabled per frozen calibration — the
COL-2 death-board separator could not be expressed in pure Zag within the
freeze window; documented in CALIBRATION_C_ZAG.md).

## Critical deviation from build-time projections

The amendment projected KD-1 ≈50–100 on the basis that D3 (CCN-1) would
eliminate the 335 CCN-1 wrong-high-confidence judgments ("D3 (CCN-1) 0/100 vs
baseline 335"). The committed binary does not reproduce that: on the actual
R2A battery fixtures D3 fires zero times.

Root cause (measured, `stats` mode):
- `r2a_colorconst_CCN-1_000.r24`: `d3_opp=0` — the opposite-cast test
  (b > 2r ∧ b > 2g) fails: panel-1 means r=0.0, g=127.5, b=100.1; the
  0.55-exposure renders are green-heavy, not strictly blue-dominant.
- `d3_corr=3993 < 9500` — the texcorr≥0.95 conjunction also fails on the
  0.55-exposure R2A renders (death-board median 0.9989 was on brighter
  fixtures; not transferable).
- 40/40 sampled CCN-1 fixtures: dmask=0 all wrong-HC (conf 756–852);
  dmask=4095 zero kcap fires. Harness colorconst adversarial (20 fixtures):
  4 wrong-HC at dmask=0, zero D3 fires at 4095.

The 0-FA calibration on NOISE was satisfied trivially; recall on the actual
trap family was never measured before the freeze. The amendment's safety
argument (§3 "D3 is safe, not reckless") therefore holds on noise but is
vacuous on the target family — D3 is inactive by construction on this
battery.

Consequence: CCN-1 contributes its full 335 to KD-1. Even with D1 perfect and
D4/D5/D9 as frozen, KD-1 = 675 > 537.

## RK-3 (the fork killer)

Measured 14.6% of correct-high-confidence percepts reach PASS-and-install
(prereg predicted ~9.4% or lower; either way far below the 85% survival bar).
The vknow caps depress confidence on correct percepts too (caps fire on
~noise-adjacent correct judgments, and the memgate's 750-install threshold
then misses them). Per frozen §5 the fork DIES on RK-3 as preregistered.

## KD-1 (the hypothesis killer)

Per frozen §5: "KD-1 fail → the knowledge hypothesis DIES by measurement
(reported as the deciding finding for Micah's hypothesis even though RK-3 is
the fork killer)."

Measured KD-1 = 675 > 537: **the knowledge hypothesis DIES by measurement.**
The honest reading: knowledge of the trap (D1) demonstrably helps where the
signature is structurally separable (PTC-2 glide: 400 → 0). But the two
largest remaining families — CCN-1 (335) and COL-2 (313) — defeat the
frozen pure-Zag detectors: D3's opposite-cast refinement has zero recall on
the actual fixtures, and D4 could not be built within the freeze window.
Teaching the system the trap's name and a signature does not suffice when
the signature test itself does not detect the trap.

## Verdict

**V2-C: DEAD.** RK-3 kill (preregistered) and KD-1 kill (measured) both fire.
The fork does not proceed. Do not build on V2-C's vknow detectors without
re-deriving them against the actual R2A fixtures with measured recall —
calibration on NOISE alone is not evidence of function.

## Evidence

- `RUNLOG.md` — full run log with source SHAs, build SHAs, fixture integrity
- `metrics.json` — all scored bars
- `RUN_DIGESTS.md` — per-run artifact digests (B6 evidence)
- `evidence/` — fixture integrity report, KD-1 family table, per-run
  dispositions/ledger/metrics digests, build hashes, compact per-trial
  evidence (sweep summary per family)
