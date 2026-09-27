# PREREG B1-P9: B1-Class Bar Reformulation per Precedent P9 (DRAFT FOR FREEZE)

Wave: wave-20260927-0821pdt, lane 3 (prereg design).
Status: DRAFT. This document is not frozen. It becomes frozen only when a
future wave adopts it as the bar set for a B1-class re-freeze. Until then,
numbers may change by redraft only, never by post-freeze edit.
Freeze commit: PENDING (to be recorded at freeze time).
Prereg design commit (lane 3, this wave): 59b9df4b0b45ffef23704ad971ae9029e14d7126.

## 1. Provenance header (machine-checkable)

COMPONENT_LINEAGE:
- B1 BOUNCE, wave-20260925-1121pdt: DISCARD. KB4a measured mean
  per-channel delta 2.03 vs frozen floor 3.5; KB4b 17% vs frozen 25%; KB6
  max 4-neighbor delta-field gradient 14 vs frozen cap 8. The k-family is
  jointly unsatisfiable (roughly 3x gap on both axes: KB4a needs k >= 625
  where grad is about 22.8; KB6 needs k <= 219 where mean is about 1.02).
  Effect sub-visible, independently confirmed.
- Precedent P9 (1121pdt judge): "A bar set that a content-free control
  would pass is unfit to certify its candidate class. When a flat tint or
  other magnitude-only cheat would pass the frozen bars of a candidate
  whose goal is content or direction (B1's frozen KB4 here), the bar set
  must be repaired before any re-freeze: a direction or content bar for
  the candidate class (for example delta-field vs bounce-field
  correlation) and percentile-based rather than global-max edge bars. Bar
  weakness that did not cause the verdict is banked prospectively; it is
  never applied retroactively to move a bar this wave."
- Banked knowledge (1121pdt red team): pass 3's wash plus flat cool fill
  spend the shadow-color budget (about 2/255 at honest mixes); calibrate
  effect bars against base-render pixel statistics with a probe program.
  The flat-tint counterexample (a dishonest +4 tint passes KB4a, KB4b,
  KB4c, KB6, KB3, KB5) is the content-free control this reformulation
  must kill.

NEW_KNOWLEDGE_CLAIM: none. This prereg freezes no mechanism and tests
nothing. It is the repaired bar set that any future B1-class (post-pass
recolor) re-freeze must adopt. B1 BOUNCE's DISCARD verdict stands and is
not revisited by this document (P9 banked prospectively).

Inherited: the r8c substrate, the frozen baseline renders, the KB4
population definition (land mask from the world model, arch opening
excluded, blurred sh > 512, n = 141,684 as in 1121pdt), the structural
bars KB1/KB2/KB3/KB5/KB7, and the pinned toolchain
src/tools/toolchain/znc_linux_x86_64_abed8aa1 (SHA-256
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef).
New: the reformulated KB4a'/KB4b'/KB4c'/KB6' bars and the KB0' cheat-proof
control.

## 2. What this prereg is

A re-freeze template for the B1 candidate class (post-pass recolor
mechanisms whose goal is spatially varying indirect-illumination color
from the scene's own albedo). Any future B1-class re-test freezes its
mechanism against THIS bar set, not the 1121pdt KB4/KB6 bars. The
k-family mechanism class stays DISCARDed; this bar set does not revive
it.

## 3. The frozen bounce field (content reference)

The direction bars below are computed against the frozen bounce field:
the per-pixel shadow-depth field from the 1121pdt base render (the
dk*110/1024/1024 scaling field used in pass 3 of b1_baseline.zag), pinned
by SHA-256 at freeze time. It is the scene's own albedo-derived content
reference, frozen before any candidate renders. A future freezing wave
pins the exact blob; this draft freezes the definition.

## 4. Metric it moves

Cheat-proof certification of contentful recolor: the bar set must pass a
mechanism that genuinely adds spatially varying indirect illumination
and must fail a magnitude-only cheat. The old bars measured magnitude;
the new bars measure direction and content.

## 5. Reformulated kill bars (frozen; never moved after the seal)

KB0' (cheat-proof control, validity gate): the frozen flat-tint control
(best flat +c tint over the KB4 population, c chosen to maximize KB4a)
must FAIL KB4a' with correlation r < 0.10. If the control passes KB4a',
the bar set is VOID (P9 unmet) and the run does not count.

KB4a' (direction/content, the P9 bar): Pearson correlation r between the
per-pixel delta-field magnitude and the frozen bounce field over the KB4
population: r >= 0.35. Rationale: a flat tint has r near 0 by
construction; a genuine albedo-bounce recolor covaries with the scene's
own shadow depth. The 0.35 threshold is a draft number: the freezing
wave runs the frozen pure-Zag probe program against base-render pixel
statistics (per the banked lesson) to confirm it, and any change is by
redraft before freezing, never after.

KB4b' (effect spread, content-conditioned): at least 20% of the KB4
population with per-pixel mean per-channel |delta| >= 2.0 AND delta
direction aligned with the bounce field (per-pixel sign of the delta dot
bounce > 0 in at least 2 of 3 channels). The magnitude floor is lowered
from 3.5 to 2.0 per the banked knowledge (about 2/255 at honest mixes);
the alignment condition keeps it a content bar, not a magnitude bar.

KB4c' (effect cap, carried): max per-pixel per-channel |delta| <= 80.

KB6' (edge, percentile-based per P9): the 99th percentile (p99) of the
4-neighbor delta-field gradient over all pixels <= 8. This replaces the
global-max cap: a single hot pixel no longer fails an otherwise clean
field, and a genuinely blocky field still fails at p99.

KB1/KB2/KB3/KB5/KB7 (structural, carried from 1121pdt): byte-parity of
the baseline rebuild, determinism of reruns, HF ratio, luma variance
numerator ratio, and the invented-count guard, with their 1121pdt
thresholds unchanged.

Determinism: all runs executed twice; renders and verifier outputs
byte-identical across reruns (SHA-256).

Verdict mapping (frozen): all bars PASS means the candidate is certified
as a contentful recolor under the repaired bar set, still candidate
evidence only (no sealed pair is fabricated from any B1-class mechanism
without a separate judge ruling). Any bar FAIL means DEAD with killing
evidence. KB0' failure means VOID.

## 6. Cost budget

Render runs on the sealed battery and the skycrop battery plus verifier
runs, x2 for determinism, pure Zag. Cost is compute only.

## 7. Red-team confound list (considered before this draft freezes)

1. Knowledge vs architecture (bar gaming): the flat-tint counterexample
is frozen as KB0', so the content-free cheat is mechanically killed.
The red team runs the control itself and verifies r < 0.10.
2. Bounce-field tuning: the bounce field is pinned by SHA at freeze
time from the base render; the candidate may not recompute or select
it. The red team verifies the pin predates the candidate renders.
3. Percentile gaming (KB6'): p99 is resistant to single-pixel outliers
but a field that is blocky on 2% of pixels still fails; the red team
checks the gradient histogram, not just the p99 number.
4. Threshold calibration (banked lesson): the probe program calibrates
KB4a'/KB4b' floors against base-render pixel statistics before
freezing; the program is pure Zag and committed with the prereg.
5. Retroactive application (P9): this bar set is never applied to B1
BOUNCE; the DISCARD stands. The red team confirms no verdict in the
record is re-scored.
6. Sealed-pair discipline: no B1-class render becomes a sealed blind
pair except through the standing image-judge protocol (coded, tested,
provenance-labeled). This prereg fabricates no pair.
7. Pure Zag: verifier, probe program, and renders are pure Zag. Any
Python contact voids the evidence.

## 8. Standing rules applied

Pure Zag literally (no Python anywhere; any contact voids the evidence).
Frozen kill bars are never moved after the freeze. Missing evidence means
CANNOT-CONFIRM. The prereg freeze commit strictly precedes any
implementation commit (commit-order self-check). No em-dashes in this
document. The six governance rulings are untouched. The sealed blind
judge queue is untouched. Micah's frontier files are untouched. Nothing
is pushed to GitHub; commits stay local on tnn-native-lab.

## 9. Gate conditions (what this draft waits on)

This is a draft for a future wave's queue. A B1-class re-test may not
freeze on the old KB4/KB6 bars; it must adopt a P9-reformulated set, of
which this draft is the first. No governance ruling gates the bar set
itself. A new mechanism (not the k-family) is still required before any
re-test: bars do not invent mechanisms.
