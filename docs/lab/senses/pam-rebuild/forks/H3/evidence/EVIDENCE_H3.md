# H3 Evidence

Fork H3 — "Counterfactual Predictive State". Frozen prereg: `PREREG_H3.md`.
Build: `src/BUILD_LOG.md` (pristine 53002-byte `sense_h3.zag`; binary sha256
`814252fb262fc37dcc20de5454a1911a271779a0b7de27d1d69c1fd369dd4b3f`,
byte-identical rebuild verified). A-binary rebuilt from committed
`senses/rebuild/a_raw/sense.zag`, byte-identical to the crew's build.
H3ADV: 120/120 validation-gate PASS, 0 discards. Base battery: 1,045
fixtures (370 primary + 370 noise + 185 harness-adversarial + 120 H3ADV),
20/20 spot-check vs pristine rebuild exact.

## Verdict table (CEO-plain)

| Bar | What it asks | Result |
|-----|--------------|--------|
| B1 | Is H3 right often enough on normal cases? (≥60%) | **0.7264 — PASS** |
| B2 | H3 vs A on the same 1,045 cases | **delta +0.000** on every split — informational |
| B3 | How much work H3 does vs A (operations, bytes) | **9.31× ops mean** (p50 3.29×, p95 57.87×); 194 bytes/transition — measured, no kill |
| B4 | Does the memory contract actually change decisions? (≥31/305, fewer false installs) | **177/305 differ; 70 vs 174 — PASS** |
| B5 | False-install rate on hostile cases (≤4%) | **22.95% (70/305) — FAIL** |
| B6 | Three identical runs, matching ledger hashes | **byte-identical; ledger recompute OK — PASS** |
| B7 | Mechanism elegance / sensory acceptance | elegance documented (`TRANSITION_EXAMPLE.md`); sensory N/A by design |
| Streaming KB1 | false permanent installs ≤4% | **14.3% on pitchdisc** (20/140); 0% elsewhere | ❌ KILL |
| Streaming KB2 | ≥90% injected false percepts withdrawn/quarantined at H=0 | **85.7% on pitchdisc**; 97–100% elsewhere | ❌ KILL |
| Streaming KB3 | confirmed-percept recall ≥80% | **0%** (5 scenes); vacuous on motiondir | ❌ KILL |
| Streaming KB4 | action regret ≥25% lower than A | **−89%…−466%** (4 scenes) | ❌ KILL |
| Streaming KB5 | byte-replay | **byte-identical** (motiondir 600-episode re-run) | ✅ |

## Kill outcome

**H3 DIES** — streaming kill bars KB3 and KB4 fire on the frozen
implementation. (See `VERDICT_H3.md`.)

## B1 viability — PASS (0.7264 ≥ 0.60)

Macro-average judgment accuracy on 370 frozen primary (equal task weights):

| Task | Accuracy | n |
|---|---|---|
| shapetrans | 1.000 | 90 |
| colorconst | 0.875 | 40 |
| pitchdisc | 0.833 | 60 |
| timbredisc | 0.750 | 60 |
| colordisc | 0.483 | 60 |
| motiondir | 0.417 | 60 |

Note: H3 inherits T0 (= Approach A) wholesale; colordisc/motiondir are
below 50% because A's estimator is. H3's judgment equals A's on every
fixture (B2).

## B2 head-to-head — informational, delta +0.000

| Split | H3 | A | Δ | n |
|---|---|---|---|---|
| primary | 0.741 | 0.741 | +0.000 | 370 |
| noise | 0.735 | 0.735 | +0.000 | 370 |
| adversarial | 0.492 | 0.492 | +0.000 | 185 |
| h3adv | 0.333 | 0.333 | +0.000 | 120 |

Per-task primary deltas are also exactly 0.000 (all six tasks). The
contract never installs a non-T0 claim on these 1,045 fixtures
(`judge != t0` count: **0**): H3's value is in the disposition
(withholding), never in a better judgment.

## B3 efficiency — measured (no kill)

Per-fixture ops ratio H3/A on primary (same counting grain):

| Task | mean | p50 |
|---|---|---|
| colorconst | 57.87 | 57.87 |
| shapetrans | 5.00 | 5.00 |
| motiondir | 3.29 | 3.29 |
| pitchdisc | 3.00 | 3.00 |
| colordisc | 3.00 | 3.00 |
| timbredisc | 2.01 | 2.01 |

Overall: mean 9.31×, p50 3.29×, p95 57.87×. The t2 57× is the Δ-spot
prediction (brightest-8×8 search + masked von Kries recompute per branch).
Bytes per percept: H3 canonical transition 194 bytes mean vs A's
`debug_vec=` (~50–200 bytes depending on task). H3's hypothesis targets
(H3(d): 30% of raw-value compute) are not met — reported as a finding.

## B4 contract ablation — PASS (load-bearing, not decoration)

Suite: 305 adversarial, same T0 judgments through a contract-less
always-INSTALL gate:
- Disposition differs: **177/305** (need ≥31) ✓
- False installs WITH contract: **70**; WITHOUT: **174** ✓ (60% reduction)

The contract genuinely changes decisions and strictly reduces false
installs. B4 passes.

## B5 adversarial false-install — FAIL (22.95% > 4%)

70/305 INSTALLED with judgment ≠ truth. All 70 from the harness
adversarial set; H3ADV: **0** false installs (40 quarantined, 80 withdrawn).
By task: shapetrans 30, pitchdisc 20, colordisc 14, colorconst 5,
motiondir 1, timbredisc 0.

Also: 57 false installs on *primary* fixtures (of 96 where T0 was wrong,
57 still installed). High-confidence (≥700) judgments: only 60/1045 —
INSTALLED keeps T0's margin confidence (×1.0), which rarely reaches 700.

## B6 determinism — PASS

60 fixtures (10/task, frozen primary) × 3 runs: stdout byte-identical
(60/60), ledger hashes independently recomputed with Python hashlib.sha256
(prev=zeros || canonical transition): 60/60 match. Any failure would have
killed the fork.

## B7 beauty

Mechanism elegance: one mechanism (prediction failure) does perception QC,
memory revision, and action gating — see `TRANSITION_EXAMPLE.md` for two
worked records (clean install; adversarial quarantine). Sensory
acceptance: preregistered N/A — H3 emits no audio/visual output by design
(it processes sensory input; branches emit claims + predictions only).

## Streaming (§6) — 6 scenes × 600 episodes, [B,B,B,A,A] interleave

Per-scene kill bars (pristine binary, isolated runs; memory replication
verified faithful per scene by exact `durable=` recompute):

| Scene | KB1 false-perm | KB2 handled | KB3 recall | KB4 regret Δ | Kill? |
|---|---|---|---|---|---|
| colordisc | 0/165 = 0.000 | 165/165 = 1.000 | 0/1 = 0.000 | +0.382 | **KB3** |
| colorconst | 0/162 = 0.000 | 162/162 = 1.000 | 0/1 = 0.000 | −0.894 | **KB3, KB4** |
| shapetrans | 0/154 = 0.000 | 150/154 = 0.974 | 0/1 = 0.000 | −1.890 | **KB3, KB4** |
| timbredisc | 0/0 = 0.000 | 0/0 = 1.000 | 0/1 = 0.000 | −4.656 | **KB3, KB4** |
| motiondir | 0/195 = 0.000 | 195/195 = 1.000 | 0/0 = 1.000 | +0.519 | — |
| pitchdisc | 20/140 = 0.143 | 120/140 = 0.857 | 0/3 = 0.000 | −0.895 | **KB1, KB2, KB3, KB4** |

Bars: KB1 ≤4%, KB2 ≥90%, KB3 ≥80%, KB4 ≥+25%.

Kill outcome: **H3 DIES** — KB3 fires on colordisc, colorconst,
shapetrans, timbredisc, pitchdisc; KB4 fires on colorconst, shapetrans,
timbredisc, pitchdisc; KB1 and KB2 fire on pitchdisc (20 injected false
percepts became durable; only 85.7% handled at H=0). Motiondir is the
only clean scene (KB3 vacuous: T0 never correctly installed a base claim,
so there is nothing to recall).

Mechanism (traced): the sticky quarantine permanently bans the true
claim after a counterfactual branch breaks ≥2 predictions on an episode
where it is false. Colordisc: SAME banned at episode 32 (base episode,
truth=DIFFERENT, T0 correct). Shapetrans: CIRCLE banned at episode 1.

Method notes: KB1 denominator = injected false percepts (adversarial
episodes with T0 ≠ truth), per prereg §8.1. KB3 = end-of-scene memory
state per prereg §8.3, via exact replication of the binary's mem-update
rules (validated by reproducing every episode's `durable=` flag). Ledger
verified per scene by independent recompute (`eval/verify_ledger.py`).
