# Contender D — VERDICT (frozen §6)

Per-path verdicts. This crew built audio only; every other path is NOT TESTED.

## §6 bar (frozen)

Overthrow on a path iff: ≥ all 9 quality bars, coherence ≥ NATIVE (xcorr +
contour decomposition), strictly better on ≥1 of {RT-LONG honest-cents,
RT-CASCADE, RT-EDGE, COST} with no regression elsewhere, byte-identical
reruns, and survives §5 red team. A TIE keeps NATIVE.

## D2 PLANREF — audio: OVERTHROW (with one disclosed caveat)

- 9/9 bars PASS, numbers identical to the PAR baseline.
- Coherence decomposition 1.000000 on all four components; fixture output is
  bit-identical to PAR, so coherence equals the documented audio reference.
- RT-LONG honest-cents, near-miss case (nominal 460, true cue 440):
  **D2 0c** (construction-exact latch of the cue's declared Q16 f0) vs
  hybrid v2's abstain-to-nominal **76.7c**. Strictly better, no contest.
- No regressions: fixture bit-identical to PAR (quality/CHOP/coherence all
  tie); RT-CASCADE 0/64/0 with latch intact; RT-EDGE frozen tie; COST within
  VM noise of PAR.
- Byte-identical reruns: 4/4 identical SHA.
- Survives §5 red team (REDTEAM.md): sustained corruption → clean abstain,
  adversarial plans → abstain-or-correct, polyphony → abstain, no hangs.
- **Caveat (disclosed):** no native binary exists in the workspace, so
  NATIVE's own RT-LONG response was not re-measured here. The comparison is
  against the preregistered reference behaviors: hybrid v2 abstains to the
  nominal (measured 76.7c on the near-miss; hybrid RESULTS.md), PAR renders
  the nominal (measured 1200c on the original). NATIVE is presumed nominal-
  rendering per PREREG_D.md §D2-C3. If NATIVE is ever measured latching exact
  pitch on the near-miss, this verdict downgrades to TIE.

## D1 MR-BIDI — audio: TIE (incumbent keeps)

Every preregistered D1 claim was a tie-claim and every one verified:
fixture bit-identical to PAR, frozen RT-EDGE bit-identical to PAR, seq==rev
bit-identical, 9/9 bars, CHOP clean, coherence 1.0, cascade confined,
deterministic. The 15 s window-cut extension (plan-gated backward release:
0.247–0.314 FS end transient → 0.0 FS, diffs confined to the declared
220-sample region) is a genuine, sample-proven improvement — but it is
**outside the frozen battery** (frozen RT-EDGE uses the clipped plan, where
D1 ties by design), so it does not satisfy §6's "strictly better on a frozen
axis". Reported as a documented bonus, not an overthrow.

## Path matrix

| Path | D1 | D2 |
|---|---|---|
| Audio | TIE | **OVERTHROW** (caveat above) |
| Video | NOT TESTED | NOT TESTED |
| Dialogue | NOT TESTED | NOT TESTED |
| Image | NOT TESTED | NOT TESTED |

## Honesty notes

- D2's "0 cents" is by construction (the latched value IS the plan's declared
  Q16 f0), not by measurement. The ZCR instrument reads −60c on D2's own
  440 response — disclosed in every result file, never presented as the claim.
  D2 is a plan cross-reference, not a pitch meter; the prereg says so plainly.
- D1's fixture output is intentionally identical to PAR's; its excerpt is a
  NEW render of a NEW plan, labeled as such — never presented as novel audio
  content on the fixture.
- The fixture's `659.25` is 12-TET-truncated, not rounded — formation schemes
  must reproduce the truncation to match the frozen text byte-identically.
