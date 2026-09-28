# VERDICT R2-15: FS-C Cross-Modal Booster Marginal-Gain fork

**Date:** 2026-09-23
**Fork:** R2-15 (debate D §4 FS-C). **Base:** R2-3 admission gate (reference disposition);
**booster:** cross-modal concurrence from the audio channel's independently-declared disjoint
evidence (audio gate span, clean token) — never required for unimodal percepts, never sufficient
alone.
**Instrument:** `src/fsc.zag` (pure Zag, zero RNG), built with the pinned toolchain
(`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`, 92,610-byte native binary).
**Fixtures:** FSC-BATT, 1,150 trials, frozen seed 20260923, `MANIFEST.fsc.sha256`.
**Verdict: ALIVE** — all five frozen kill bars pass; the booster is load-bearing, not decorative.

## Bar table (measured, mode ON = booster, mode OFF = ablation)

Multimodal adversarial subset = M-U (200) + M-W (200) + M-C (200) = 600 trials.
Recall set = M-N (400 trials). M-WA (150) is diagnostic (no bar).

| Bar | Requirement (frozen) | Measured | Pass |
|-----|----------------------|----------|------|
| KB-1 booster ablation | FI(ON) ≥ 5pp absolute below FI(OFF) on the 600-trial multimodal adversarial subset | OFF: 200/600 = 33.33%; ON: 0/600 = 0.00%. **Reduction = 33.33pp** (6.7× the bar) | ✅ |
| KB-2 correlated fooling (HARD) | M-C false installs ≤ 2% (≤4/200) | 0/200 = 0.00% | ✅ |
| KB-3 recall | M-N correct-install rate ON ≥ OFF − 5pp | ON: 400/400 = 100.00%; OFF: 400/400 = 100.00%. Loss = 0.00pp | ✅ |
| KB-4 overall (B5-style) | false installs ON ≤ 3% over the 600-trial adversarial battery | 0/600 = 0.00% | ✅ |
| KB-5 determinism (HARD) | 2 full passes/mode byte-identical; hash chains verified | 48/48 artifacts byte-identical (`cmp` clean); 24/24 chains independently verified | ✅ |

## Where the margin comes from (per-family dispositions)

| Family | Booster ON | Booster OFF (ablation) |
|---|---|---|
| M-N normal (400) | 400 installed, 400 correct | 400 installed, 400 correct |
| M-U uncorrelated spoof (200) | 0 installed (withheld) | 0 installed (withheld) |
| M-W within-modality persistent spoof (200) | 0 installed (withheld) | **200 installed, 200 FALSE** |
| M-C correlated cross-modal fooling (200) | 0 installed (withheld) | 0 installed (withheld) |
| M-WA audio-channel persistent spoof (150, diagnostic) | 0 installed — **150/150 true percepts starved** | 150 installed, 150 correct |

The booster's entire 33.33pp gain is the M-W family: the R2-1-shaped attack where the adversary
holds the visual corruption across the temporal gate span, breaking the base path's
declared-clean-gate assumption — the booster's independent second modality is the only clean
witness, and it withholds all 200. On M-U and M-C the base path's own gate check already withholds,
so the booster adds nothing there (honest decomposition, not hidden).

## Diagnostic (no bar): the booster's honest cost

M-WA: when the second modality is persistently attacked while the visual channel is clean, the
booster starves 150/150 true installs (100% starvation) that the base path installs correctly.
This is the genuine price of the concurrence rule — an adversary that can hold a corruption on
the audio channel can denial-of-service legitimate visual percepts. Reported, not bar-gated per
the frozen prereg; any deployment of the booster must answer it.

## What this verdict does NOT claim

1. The correlated-fooling family (M-C) fools the *formation* spans of both modalities jointly;
   both gate spans stay clean per the declared contract — which is why the base gate check fires
   first and the booster is never the deciding vote there. A joint spoof held across the gate
   spans too would defeat the union; that family was deliberately not built (it sits outside the
   R2-3 declared-clean contract and would kill any R2-3-derived fork, proving nothing about the
   booster specifically).
2. Scope is the frozen battery: 3-symbol vocabulary, naive front-ends, synthetic 48×48 / 8 kHz
   tokens. The booster is proven load-bearing *within this battery*, not against arbitrary
   adversaries — debate D front (a)'s ruling stands: enumerated families challenge the gate, they
   do not certify it.
3. KB-3 passes at 0.00pp loss only because the recall set (M-N) has a clean second modality;
   M-WA shows what happens when it isn't.

## Verification

- 2 passes × 2 modes × 6 batch files = 24 reports + 24 ledgers, **byte-identical across passes**
  (`cmp` clean, KB-5).
- 24/24 hash chains independently re-verified (`work/verify_fsc_ledger.py`): entry counts
  200/200/200/200/150 per mode per family, tail hashes match.
- Python↔Zag cross-validation (`work/xval_fsc.py`, `evidence/xval_log.txt`): 2,300 trials
  (1,150 × 2 modes), every vf/vg/af/ag field recomputed by the independent numpy mirror —
  **0 mismatches**.
- Fixture manifest: `../fixtures/fsc/MANIFEST.fsc.sha256` (6 batch files, 89,559,700 bytes total).

## Evidence

- `evidence/report_m{0,1}_fsc_{N,U,W,C,WA}_b*_p{1,2}.txt` — per-mode/per-family/per-pass reports.
- `evidence/ledger_m{0,1}_fsc_{N,U,W,C,WA}_b*_p{1,2}.txt` — hash-chained ledgers (p1 ≡ p2).
- `evidence/xval_log.txt` — 0-mismatch cross-validation log.
- `../fixtures/fsc/GENERATOR_LEDGER_FSC.md` — frozen generator record.
- `src/fsc.zag` — the booster + runner (new code); `r2p_front.zag`, `r2p_protos.zag` reused
  byte-identical from R2-3; R33 native sources byte-identical to R2-14's.
