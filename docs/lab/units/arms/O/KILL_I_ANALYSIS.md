# Kill-(i) Adjudication — Arm O (Taught Vocabulary)

## Frozen bar
`units/PREREG_FREEZE.md` §3, unit O: "(i) taught-only vocabulary does not reach
M2 criterion in ≤½ the episodes of emergent-only P on T1 novel material —
acceleration claim dead"

## Evidence

### O (taught) — do_m2_t1, 2× byte-identical double-runs
| Tier | m2_etc | Episodes | Proposals | Ep0 F1 | Final F1 | Final P | Final R | Adopted |
|---|---|---|---|---|---|---|---|---|
| T1 prose | -1 | 16 | 4096 | 35.9 | 63.2 | 46.3 | 100.0 | 4096 |
| T1 code | -1 | 16 | 4096 | 27.8 | 53.0 | 36.1 | 100.0 | 4096 |

Criterion: boundary F1 ≥ 95% (single probe). Never met in 16 episodes on either
tier. m2_criterion_met=false on both.

### P (emergent) — comparator, 2× deterministic (2026-09-21, P_bin)
| Tier | m2_episodes | m2_ep0_recall | Note |
|---|---|---|---|
| T1 prose | 3 | 100% | Canonically invalid (M-7 leak) but deterministic |
| T1 code | 3 | 100% | Canonically invalid (M-7 leak) but deterministic |

## Application
Frozen bar: O must reach its M2 criterion in ≤ ½·3 = ≤1.5 episodes.
O reaches in ∞ episodes (never, on both tiers).
**Kill-(i) FIRES on both T1 tiers.**

## Interpretation
The taught vocabulary improves word segmentation (F1 35.9→63.2 on T1 prose,
27.8→53.0 on T1 code) and achieves 100% content recall, but it does not reach
the 95% boundary-F1 criterion within the 16-episode budget, let alone within
1.5 episodes. The acceleration claim — that taught vocabulary reaches criterion
faster than emergent vocabulary — is dead under the frozen comparative bar.

## Caveats (documented; do not alter the outcome under the frozen bar)
1. O's M2 criterion (boundary F1≥95%, single probe) is not the frozen program
   M-6 (content recall ≥99.5% AND boundary ≥95%, sustained 3 probes). O's
   implemented criterion is strictly easier (no sustained-3, no recall gate
   in the trigger) yet still unreachable for O's design.
2. P's M2 criterion (3 consecutive 100%-recall probes on fixed-size chunks)
   measures a different task than O's (word-boundary learning). The
   cross-mechanism ETC comparison is confounded by design.
3. Episode semantics differ: O's episode = 256 teach proposals; P's episode =
   full re-ingest sweep.
4. P's trial violates frozen M-7 (episode-0 recall 100%, not near-zero), making
   it canonically invalid. Its ETC=3 is used as the frozen comparator because
   it is deterministic (2× byte-identical) and is the only P number available.
5. O's "recall" (100.0%) is not a learning measure — it verifies byte-exact
   retrieval of ingested segments, which is trivially 100% after ingest. The
   learning signal in O's M2 is the boundary F1.

## Verdict on kill-(i)
**FIRES.** The acceleration claim is dead. Arm O's central claim does not hold
under the frozen comparative bar.
