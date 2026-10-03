# KB4 §4(a) Adversarial False-Install Rerun — Closure Report

**Date:** 2026-09-22
**Prereg:** `docs/lab/prose-learning/epistemic_wave/PREREG.md` §4 Leg (a) (EPI-KB4), commit `36632534bd98`
**Gate design:** Frozen `BUILD_DOCS.md` §6 KB4 gate contract (phase-2 build crew)
**Verdict: FAIL (B) / DEGENERATE (A) — mechanism diagnosis below.**

## What was run

The frozen §4(a) protocol: rerun the original senses KB4 harness
(`tnn-lab/senses/rebuild/`, 1,849 runs) verbatim — same adversarial
fixtures, same ground truths — with the deliberative epistemic layer as
the install gate replacing the round-1 contradiction-only rule.

**Earlier crew's partial work.** No KB4 branch/commit existed in the repo.
The phase-2 build crew left an uncommitted local `delib.zag` (40KB) plus a
frozen `BUILD_DOCS.md` defining the §6 KB4 gate contract:
`delib gate <statedir> <batchfile>`, batch lines
`fixture_id \t judgment \t confidence \t source_id`;
L1 (source track record) + confidence-as-weak-evidence (+1/10pts, cap +10)
+ L4 (conflicting endorsed judgment on same stimulus → re-deliberate by
evidence strength) + L8 (same judgment repeated across variants → +20).
However, `delib.zag`'s gate mode **segfaults on any input** (including the
prebuilt `delib_bin`); it was never functional.

**What I built.** A clean minimal pure-Zag implementation of the SAME
frozen §6 contract (`kb4_gate.zag`, 34KB binary), not a new protocol:
integer-ID batch (no ground truth in the batch file — the gate binary
literally cannot see it), L1 +5/−5, confidence boost capped at +10,
L4 conflict → re-deliberate (new wins iff strictly greater evidence),
L8 +20 per prior same (stimulus, judgment), L4-consistent +10.
Install iff evidence ≥ 0. Zero RNG. Deterministic.

**Batch order.** The raw `raw_results.json` file order: per (approach,task),
primary fixtures, then noise, then adversarial. This is the frozen file
order and the order the §6 contract assumes (earlier variants establish
the endorsed judgment; later variants are checked against it). Stimulus
IDs collapse the variant path so the same logical fixture shares state
across variants, as §6 requires ("same stimulus").

## Results (3 repetitions, byte-identical)

| Approach | Adv installs | Adv false | Adv true | False-install rate | Verdict |
|---|---|---|---|---|---|
| A | 80 | 33 | 47 | 41.2% | **DEGENERATE** (<50 true) |
| B | 99 | 46 | 53 | 46.5% | **FAIL** (>30%) |

All three repetitions produced byte-identical output (SHA256 verified).
Baseline (contradiction-only): A 59.0% (79/134), B 55.0% (72/131).
The deliberative gate reduced installs but did not repair the rate.

Per the prereg, the ≤10% integration-clearance bar is unaffected; a
≤15% EPI-KB4 pass alone would not have cleared integration in any case.

## Mechanism diagnosis

The gate works as designed — it withholds 51 (A) / 37 (B) adversarial
judgments that contradict a correct primary judgment (the fooling
worked, the sense was wrong). The failure is structural, in the §6
contract's L4 assumption:

**The adversarial perturbation can change the ground truth.** "Differs
from primary" is therefore not evidence of error. From the judgment
stream alone (no ground truth — the gate must not see it), the gate
cannot distinguish:
- *Sense fooled*: wrong judgment, truth unchanged → should WITHHOLD, and
- *Stimulus changed*: right judgment, truth changed → should INSTALL.

Consequences, approach A:
- 33 true adversarial installs **withheld**: primary correct, adversarial
  correct, judgments differ (perturbation moved the truth; the sense
  correctly reported it). Direct cause of DEGENERATE (47 < 50).
- 21 false installs **not prevented**: primary correct, adversarial
  wrong, judgments *match* (sense failed to detect the perturbation).
  No conflict exists for L4 to catch.
- 12 false installs from consistent error (wrong on both, matched).

The L4 cross-variant conflict mechanism is unsound for KB4: it assumes
the stimulus — and therefore the correct judgment — is invariant across
variants, which the adversarial construction violates by design. No
confidence recalibration can repair this either (prior finding: wrong
judgments are at least as confident as correct ones; the +10 cap makes
confidence nearly constant). Repair requires a mechanism the §6 contract
does not provide: either (i) a perturbation-aware model (knowing which
perturbations change the truth), or (ii) an independent second
observation of the adversarial stimulus — both outside the frozen
contract. Per the prereg, 15–30% would require repair and rerun; at
>30% / DEGENERATE this leg is closed as FAIL with the diagnosis above.

## Reproducibility

- `kb4_gate.zag` — gate source (pure Zag, zero RNG)
- `R33_NATIVE_IO_V1.zag` — substrate I/O (copied from `../src/`)
- `kb4_gate` — built binary (pinned toolchain
  `toolchain/bin/znc_linux_x86_64_abed8aa1`; binary excluded from commit
  per repo convention — rebuild with the command in §7)
- `gen_batch.py` — batch generator (frozen order, integer IDs, no truth)
- `batch_A.txt`, `batch_B.txt` — gate inputs (924 / 925 lines)
- `out_A_rep{1,2,3}.txt`, `out_B_rep{1,2,3}.txt` — gate outputs
  (A reps SHA256 `d1e22b18…`, B reps `8a32c5f5…`; all three identical)
- `truth.json`, `mappings.json` — scorer-side truth (never fed to gate)
- `score_epi.py` — scorer; `epi_kb4_scores.json` — scores
- `analyze_fail.py` — failure-breakdown analysis

## §7 Build command

```
cd docs/lab/prose-learning/epistemic_wave/kb4_rerun
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 kb4_gate.zag -o kb4_gate --no-analyze
python3 gen_batch.py
./kb4_gate . batch_A.txt 370 > out_A_rep1.txt
./kb4_gate . batch_B.txt 370 > out_B_rep1.txt
python3 score_epi.py
```

## One-sentence verdict

The deliberative install gate (frozen §6 contract, pure Zag, 3×
byte-identical) fails KB4 — B at 46.5% false installs (FAIL), A
DEGENERATE with 47 true installs — because the adversarial perturbation
can change the ground truth, making the L4 cross-variant conflict
mechanism unsound: it cannot distinguish a fooled sense from a changed
stimulus without ground truth it is forbidden to see.
