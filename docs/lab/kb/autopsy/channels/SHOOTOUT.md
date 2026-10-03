# PACKAGE 2 — Channel shootout results (KB4 SUSPECT gate)

**Frozen prereg:** `../PREREG_FROZEN_CHANNEL_SHOOTOUT.md`
(commit `bfe897e67c00a6f7e1f077ec5561f234f760bde0`, frozen BEFORE any run)
**Authorization (Micah, 2026-09-22, verbatim):** "now that we know it's an
info problem try more info go ahead and run test accordingly."
**Corpus:** `prose-learning/epistemic_wave/kb4_rerun/`; split per
`SPLIT_MANIFEST.json` (independently recomputed, canonical-SHA verified
`bce15d30…`; 93 calibration / 92 test adversarial-bearing stims).
**Determinism:** 3× runs byte-identical —
`out_A.txt` SHA256 `2824aab9700121634d423bf9829532217035cf30c6eecd3cde446dc1fbc02e82`,
`out_B.txt` SHA256 `0d0d804ed5c8ec768920492dae33c3c3fa8809343952b9b6e9038510e11c134f`
(all three runs, per file). Pure Zag runner (`src/chan.zag`), zero RNG.
Scorer cross-checked every Zag-emitted feature against truth.json's
non-truth fields (184/184 fixtures verified); no SKIP lines.

## Shootout table (TEST, A+B pooled, n=184)

Prior entropy H(adv_correct) = 0.9958 bits (denominator context: ~1 bit).

| channel | bits I(verdict; adv_correct) | resolution accuracy¹ | false-install² | SUSPECT rate | SUSPECT precision³ | cost/latency |
|---|---|---|---|---|---|---|
| (a) causal perturbation model | 0.0695 | 0.656 | 0.280 | 0.114 | 0.000 | immediate table lookup |
| (b) cross-time consistency (noise proxy) | 0.0110 | 0.560 | 0.398 | 0.000 | n/a | delayed re-observation (proxy) |
| (c) multi-source agreement | 0.0797 | 0.668 | 0.339 | 0.000 | n/a | immediate (second sense) |
| (d1) confidence threshold (NEG CONTROL) | 0.0003 | 0.484 | 0.474 | 0.000 | n/a | immediate table lookup |
| (d2) confidence delta (NEG CONTROL) | 0.0123 | 0.549 | 0.371 | 0.000 | n/a | immediate table lookup |
| (a)+(c) | **0.1483** | 0.811 | 0.151 | 0.511 | 0.383 | immediate (second sense) |
| (a)+(b) | 0.0637 | 0.653 | 0.347 | 0.359 | 0.348 | delayed re-observation (proxy) |

¹ P(verdict matches correct action | verdict ≠ SUSPECT); correct action =
INSTALL iff the adversarial judgment is correct.
² P(adv judgment wrong | verdict = INSTALL) — the deployability number.
³ Frozen operational definition: fraction of SUSPECT verdicts whose
primary/adversarial judgments differ. NOTE: (a)'s SUSPECTs all come from
calibrated middle-band cells (p ∈ (0.4, 0.6)) on *agreeing* judgments, so
the frozen proxy reads 0.000 — the SUSPECTs are genuinely ambiguous by
construction (calibrated p≈0.5), which the differ-proxy does not capture.
Reported as frozen; interpret with this caveat.

### Per-sense rows

Sense A (n=92):

| channel | bits | res_acc | false-install |
|---|---|---|---|
| (a) | 0.1570 | 0.714 | 0.162 |
| (b) | 0.0164 | 0.565 | 0.350 |
| (c) | 0.0483 | 0.641 | 0.339 |
| (d1) | 0.0003 | 0.489 | 0.444 |
| (d2) | 0.0447 | 0.630 | 0.327 |
| (a)+(c) | 0.1382 | 0.782 | 0.182 |
| (a)+(b) | 0.1315 | 0.705 | 0.261 |

Sense B (n=92):

| channel | bits | res_acc | false-install |
|---|---|---|---|
| (a) | 0.0230 | 0.595 | 0.395 |
| (b) | 0.0084 | 0.554 | 0.438 |
| (c) | 0.1206 | 0.696 | 0.339 |
| (d1) | 0.0011 | 0.478 | 0.515 |
| (d2) | 0.0043 | 0.467 | 0.600 |
| (a)+(c) | 0.1639 | 0.857 | **0.100** |
| (a)+(b) | 0.0226 | 0.596 | 0.423 |

## Champion

Per the frozen criterion (most bits; tie-break lower cost/latency;
false-install always alongside; >10% false-install = not deployable):

- **Champion on bits: (a)+(c) at 0.1483 bits — NOT DEPLOYABLE**
  (false-install-after-resolution 0.151 > 10% standing bar).
- **No deployable champion on the pooled test set** (every channel's
  false-install rate exceeds 10%).
- Noted: on sense B alone, (a)+(c) reaches false-install 0.100, exactly
  at the bar — fragile (single-sense, n=92) and not the frozen scoring
  unit; reported for completeness, not as a verdict.

## What the numbers say

1. **More info helps, but not enough.** The judgment-only baseline
   carried 0.02–0.03 bits (autopsy §3). The best corpus-implementable
   combination reaches 0.15 bits — a ~5–7× gain, resolution accuracy
   0.81 — yet still installs poison 15% of the time. The information
   needed for safe resolution is not in this corpus.
2. **(b) behaves as predicted: ~0 bits.** The noise variant re-observes
   the primary stimulus, not the adversarial one — the corpus limitation
   frozen in the prereg. A true cross-time channel remains untested.
3. **(c) replicates P-A1's lesson:** multi-source agreement carries
   0.08 bits but installs poison 34% of the time — correlated fooling
   defeats it, reported honestly as the autopsy predicted.
4. **Negative controls behaved as negative controls:** (d1) 0.0003 bits,
   resolution accuracy below chance (0.484) — confidence is
   anti-informative, confirmed again. (d2) 0.012 bits. Neither is a
   resolution channel; both are correctly excluded from deployment.
5. **(a) is the best single channel** (0.07 bits pooled; 0.157 on A),
   driven by the perturbation-class preservation prior (colorconst
   π=1.000, motiondir π=0.133 on calibration) crossed with the
   agreement pattern. Its SUSPECTs (11%) sit exactly in the calibrated
   middle band — the gate abstaining where abstention is correct.
6. **Combination (a)+(c) dominates on bits** because the two channels'
   errors are partially uncorrelated: (a) abstains on middle-band
   cells while (c) forces a binary verdict; requiring both to agree
   INSTALL filters correlated-fooling cases neither catches alone.
   Still not deployable.

## Consultant accounting

Asked pre-freeze (prompt in prereg §2; verbatims committed):
`consult_sol_verbatim.txt` (gpt-5.6-sol), `consult_grok46_verbatim.txt`
(grok-4.6 — labeled explicitly, never 4.7). grok failures: 0.

- **Included:** (d1) confidence-threshold negative control (sol's
  closing warning anticipated it); (d2) confidence-delta negative
  control (implementable core of grok-4.6 #4). Both frozen with
  median-threshold + calibration-accuracy orientation rules.
- **Excluded with reasons** (prereg §3): sol #1 analytic checker, #2
  physical sensor, #3 human, #4 counterfactual, #6 downstream
  instrument, #7 cross-modality — none implementable offline from
  judgment batches; sol #5's implementable core subsumed by (a)'s
  preservation prior; grok #1 human, #3 stimulus reconstruction, #5
  hand-engineered detectors — no raw stimulus/signal in corpus;
  grok #2 = already channel (c). Any learned-on-judgments model
  excluded per sol's explicit warning (apparent bits, ~0 causal bits).

## Consequence for the SUSPECT gate

- **Resolve SUSPECTs with (a)+(c) as the best available offline
  channel**, but DO NOT treat its INSTALLs as verified: at 15%
  false-install it fails the standing 10% bar, so (a)+(c)-INSTALLs must
  themselves remain provisional (flagged, auditable) until a genuinely
  independent channel exists.
- **The missing ~0.85 bits must come from outside this corpus:**
  human/trainer verification, a different physical sensor basis, or an
  analytic checker operating on actual stimulus data — the three
  channels §1.3 allows, none implementable here. The next experiment
  should build one of them rather than mining the judgment stream
  further: this shootout shows the judgment stream (plus its metadata)
  is nearly exhausted at ~0.15 bits.
- **(d1)/(d2) stay excluded** — including confidence anywhere in the
  resolution path is now disproven twice (autopsy + this shootout).
- **(b)-style cross-time consistency should be re-tested properly**
  once a corpus with delayed re-observation of the ADVERSARIAL
  stimulus exists; the proxy result (0.011 bits) says nothing about
  the real channel.

## Calibration appendix (frozen, from run1)

Sense A — CAL: `class agree n ncorrect pm`; THR d1: t=428 orient=1
(INSTALL iff conf<428); THR d2: t=-6 orient=1 (INSTALL iff delta<-6).

| class | agree=0 (n, correct, pm) | agree=1 (n, correct, pm) | π(preserved) |
|---|---|---|---|
| colordisc | 4, 0, 0 | 11, 8, 727 | 866 |
| colorconst | 6, 0, 0 | 4, 3, 750 | 1000 |
| shapetrans | 15, 4, 266 | 7, 3, 428 | 500 |
| pitchdisc | 5, 1, 200 | 10, 2, 200 | 400 |
| timbredisc | 11, 11, 1000 | 4, 4, 1000 | 266 |
| motiondir | 11, 2, 181 | 4, 1, 250 | 133 |

Sense B — THR d1: t=950 orient=1; THR d2: t=0 orient=1.

| class | agree=0 (n, correct, pm) | agree=1 (n, correct, pm) | π(preserved) |
|---|---|---|---|
| colordisc | 1, 0, 0 | 14, 8, 571 | 866 |
| colorconst | 7, 0, 0 | 3, 2, 666 | 1000 |
| shapetrans | 12, 2, 166 | 11, 7, 636 | 478 |
| pitchdisc | 7, 2, 285 | 8, 2, 250 | 400 |
| timbredisc | 11, 7, 636 | 4, 4, 1000 | 266 |
| motiondir | 14, 2, 142 | 1, 1, 1000 | 133 |

Small-cell limitation documented: per-(class×agree) cells are 1–15
samples (e.g. B/motiondir/agree n=1); permille values on tiny cells are
noisy — the pm thresholds (0.6/0.4) were frozen a priori and applied
mechanically regardless.

## Files

- `../PREREG_FROZEN_CHANNEL_SHOOTOUT.md` — frozen prereg (commit
  `bfe897e67c00a6f7e1f077ec5561f234f760bde0`)
- `consult_sol_verbatim.txt`, `consult_grok46_verbatim.txt`
- `prep_inputs.py`, `inputs/` — frozen channel inputs (stimclass,
  split, variant maps, calibration rows; no test truth)
- `src/chan.zag`, `src/R33_NATIVE_IO_V1.zag`, `src/BUILD.txt`
- `out/run1|2|3/out_{A,B}.txt` — 3× SHA256-identical Zag outputs
- `score_channels.py`, `out/run1/scores.json` (+run2; run3 unscored,
  byte-identical to run1)
- `SHOOTOUT.md` — this report
