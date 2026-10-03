# EVAL_G2.md — Fork G2: Predictive Residual Percept (PRP), full evaluation

Frozen prereg: `PREREG_G2.md` (committed alone as
`c242ec0980c3bb1cb84f3014ab11e9b2484ed095` before any G2 build output
existed). All bars applied mechanically from the prereg §4.

Evaluation driver: `evidence/eval_g2.py` (committed with sources).
G2 binary: `src/sense`, built from `src/g2_sense.zag` with the pinned
toolchain
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
(byte-identical rebuild from the committed source verified 2026-09-23).
Approach A binary: `evidence/bin_A`, rebuilt from frozen
`senses/rebuild/a_raw/sense.zag` (local test artifact, never committed;
probe stdout byte-identical to the committed Approach A evidence binary).

Fixture set: 925 harness fixtures
(370 primary + 370 noise + 185 adversarial, 6 tasks) + 240 G2 adversarial
augmentations (`augment/augment.py`, splitmix64, master seed 20260922,
byte-deterministic re-generation verified 240/240). Total adversarial:
425 of 1165 = 36.5% (≥30% requirement, prereg §3).

## B1 — G2 primary judgment accuracy (bar: mean ≥ 60%, equal task weights)

| task | n | G2 correct | G2 acc | A correct | A acc |
|---|---|---|---|---|---|
| colordisc | 60 | 29 | 48.3% | 29 | 48.3% |
| colorconst | 40 | 35 | 87.5% | 35 | 87.5% |
| shapetrans | 90 | 90 | 100.0% | 90 | 100.0% |
| pitchdisc | 60 | 60 | 100.0% | 50 | 83.3% |
| timbredisc | 60 | 45 | 75.0% | 45 | 75.0% |
| motiondir | 60 | 25 | 41.7% | 25 | 41.7% |
| **mean** | | | **75.4%** | | **72.6%** |

**B1: PASS** (75.4% ≥ 60%).

## B2 — head-to-head vs Approach A (identical 925 fixtures)

G2 mean primary **75.4%** vs A mean primary **72.6%** (delta **+2.8 pp**).
**G2 wins.** The entire delta is pitchdisc (G2 60/60 vs A 50/60); all other
tasks tie exactly. Caveat: G2's pitchdisc front-end is not a byte-faithful
port of A's — the residual layer's fine-grid or octave handling diverges
somewhere (not investigated further; the fork is dead on B5 regardless).

## B3 — efficiency (ops per percept, bytes per percept)

Mean ops per primary fixture (instrumented at element-visit grain):

| task | A mean ops | G2 mean ops | ratio |
|---|---|---|---|
| colordisc | 8,193 | 8,205 | 1.00× |
| colorconst | 8,193 | 8,205 | 1.00× |
| shapetrans | 27,651 | 92,187 | 3.34× |
| pitchdisc | 4,521,065 | 9,173,236 | 2.03× |
| timbredisc | 2,293,308 | 2,358,852 | 1.03× |
| motiondir | 28,674 | 28,686 | 1.00× |

G2 range: 8.2k–9.2M ops/fixture; A range: 8.2k–4.5M ops/fixture. The
hypothesis's claimed O(N)-vs-O(N²) saving does not materialize against A:
the residual layer is pure overhead — the costs sit in pitchdisc (2.0×)
and shapetrans (3.3×, the 90°-rotation re-profile), +12 ops/fixture on the
image tasks. Bytes per percept: G2 256 (residual vector) + 277 (ledger
record) = **533**; single-mode stdout ~733–788 B/fixture (10-per-task
sample) vs A ~92–139 B/fixture. G2 mean wall time per primary fixture:
~1.9 s (VM wall-clock under load, audio tasks dominate).

## B4 — memory-contract proof, batch over 425 adversarial fixtures (LOAD-BEARING)

Identical percepts through the contract gate vs the ablated
(always-install) gate; `sense batch <manifest>`:

| mode | records | installs | withholds | false installs |
|---|---|---|---|---|
| contract | 425 | 209 | 216 | 50 |
| ablated | 425 | 425 | 0 | 132 |

- Disposition alteration rate: **50.8%** (216/425, bar ≥ 10%).
- False installs: contract **50** < ablated **132**.

**B4: PASS** — the contract is not decoration; it changes most adversarial
dispositions and more than halves false installs.

## B5 — adversarial false-install rate (bar: ≤ 8% per install)

Contract mode: **50 false installs / 209 installs = 23.92%** (> 8%).

Per-task false-install rates (false / installs):

| task | installs | false | rate |
|---|---|---|---|
| colordisc | 53 | 11 | 20.8% |
| colorconst | 5 | 0 | 0.0% |
| shapetrans | 4 | 2 | 50.0% |
| pitchdisc | 24 | 0 | 0.0% |
| timbredisc | 70 | 10 | 14.3% |
| motiondir | 53 | 27 | 50.9% |

Per fixture: 50/425 = 11.8%.

**B5: FAIL** → **kill trigger.** The contract gates on predictive
consistency (small residuals + exact coarse-hash match), but consistency
is orthogonal to correctness. When the front end is fooled, the world
still "continues as it is" in invariant space: residuals stay small, hashes
match, and the contract certifies the mistake with a clean ledger entry.
The hash-equality gate does all the work and is uneven across tasks:
colorconst withholds 55/60 adversarial (installs 5, 0 false — brutally
strict, discarding correct judgments too), while motiondir installs 53/70
with 27 false.

## B6 — determinism + independent ledger re-verification

(bar: 3× byte-identical runs; ledger independently re-verified; any
mismatch → fork FAILS)

- **Single-mode 3× byte-identical**: first 10 primary fixtures per task
  (60 total), 3 runs each → **PASS** (all 180 runs byte-identical stdout).
- **Batch 3× byte-identical**: 425-record contract stream and 425-record
  ablated stream, 3 runs each →
  contract reps sha256
  `dc0315056d709f0ab5c8a87985d1990fd57d8e0c536bc5522ef4a7deae0070f9` (×3),
  ablated reps sha256
  `fa38a2d9a7d150b0d0d0a6e82c3c758fe9dd79a59bdb0422b0783bcd7018901c` (×3)
  → **PASS**.
- **Independent Python FNV-1a-64 ledger re-verification** (separate
  implementation from the Zag binary): re-parsed every batch record from
  stdout in fixture order and re-chained from genesis
  `L_0 = FNV-1a-64("G2-PRP-1")`;
  per-record `chain=` values and summary `ledger_final=` compared against
  the binary's emitted values:
  - contract: **425/425 records match**,
    ledger_final `cf4ab3fd62a17a71` (binary) = recompute → **PASS**.
  - ablated: **425/425 records match**,
    ledger_final `3582ea7ee3b45ff9` (binary) = recompute → **PASS**.

**B6: PASS.**

## B7 — beauty

Per prereg §4: (i) on the hypothesis's own elegance claim (prediction as
the single bridge from perception to memory) — the mechanism is coherent
and load-bearing (B4 PASS): one contract rule for all six tasks, with all
task-specific knowledge confined to the extractors and the prediction
function. But the bridge gates on the wrong property (B5 FAIL).
(ii) Output quality: G2 emits invariant-space residual vectors, not
sensory reconstructions; human ear/eye judging is N/A (documented, not
evaded — there is no audio/image artifact to judge).

## Integration (kill bar: ≥ 85%)

Complete percept + disposition + ledger records with exit 0 over the 925
harness fixtures: **925/925 = 100.0% → PASS.**

## Augmentation set (adversarial, G2-specific)

240 fixtures generated deterministically (splitmix64, seed 20260922;
re-generation byte-identical 240/240). G2 single-mode on augmentations:
**75.8%** (182/240); installs 123, withholds 117. Each method's
truth-invariance rule is machine-checked and asserted before writing
(`augment/augment.py`).

## pok-flag audit

The binary's contract gate reads a per-task "prediction available" flag
in ADDITION to the frozen `norm<24 && ph==oh` rule (flag is 0 only when
the forward model produced no prediction at all: shapetrans degenerate
mask, motiondir nsteps<3). WITHHOLD records with norm<24 and ph==oh that
could only come from the extra flag: **0** on this set — the gate behaved
exactly as the frozen two-condition rule; the B5 failure is in the rule
itself, not the extra flag.

## Verdict (mechanical, from the frozen bars)

| bar | result |
|---|---|
| B1 primary ≥ 60% | **PASS** (75.4%) |
| B2 head-to-head | G2 wins (+2.8 pp) |
| B4 contract-matters | **PASS** (50.8% altered, 50 < 132) |
| B5 false-install ≤ 8% | **FAIL** (23.92%) |
| B6 determinism + ledger | **PASS** |
| Integration ≥ 85% | **PASS** (100.0%) |

**G2 verdict: ☠️ KILLED** — kill reasons: B5 false-install rate 23.92% >
8% (adversarial, per install).

### What died and why (CEO-plain)

G2 is a memory gatekeeper: it predicts what it expects to perceive, and
only files a memory when reality matches the prediction closely. That
gate works — it throws out half the adversarial inputs and catches more
than twice as many bad memories as the always-file version. But the gate
checks the wrong thing. It asks "was this predictable?" when it should
ask "was this right?" A misleading input can be perfectly predictable —
the world keeps moving the way it was moving, even while the judgment
about it is wrong. So the gate filed 50 wrong memories out of 209
(24%), three times the 8% limit. The mechanism is elegant and it matters,
but it cannot tell a consistent mistake from a correct perception, and
that is fatal for a memory system.
