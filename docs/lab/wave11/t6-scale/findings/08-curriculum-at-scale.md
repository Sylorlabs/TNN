# Slice 08 — Curriculum at 1000x scale (Track 6)

## 1. Slice
Track 6, slice 08: extend Track 4's three curricula (CODE / ENGLISH / MESSY-REALITY)
to the 1000x duration leg (60,000 episodes per arm, since 1x = 60 and 10x = 600 per
t4/11). Four questions: (a) does the curriculum still teach at scale — same bars,
same verdicts; (b) the episode budget: sublinear, linear, or superlinear mastery
cost vs the 1x/10x/100x legs; (c) catastrophic interference at 1000x — slice 16's
design extended, where the ledger-signature story either holds or breaks; (d) the
seven-control battery at 1000x — which bars still discriminate and which saturate.

## 2. Falsifiable claim
At the 1000x leg each curriculum still passes the seven-control battery on the same
bars it passed at 1x (C1 ≥90% retention, C3 100% trap-correct, C4 ≥90% post-
disconnect, C5 ≥75% novel probes, C6 ≥15-point curriculum-vs-control delta), mastery
costs at most 3x the episodes of the 100x leg (efficiency exponent α ≤ 0.5),
cross-curriculum deltas stay <5 points at every checkpoint, and no control
saturates: every positive control from t4/11 still fires against its fault arm at
1000x. If any bar that passed at 100x fails at 1000x, the curriculum does not scale —
no second chances, no bar-lowering.

## 3. Design
**Legs.** S1 (60 eps), S10 (600), S100 (6,000), S1000 (60,000) per arm. Arms: three
isolated baselines (one curriculum each), one interleaved integrated run, one
no-curriculum full-machinery control (C6). The 1000x leg runs ONLY the integrated
arm + no-curriculum control; baselines at 1000x are reconstructed from the 100x
leg curve fits (isolated-skill curves are already monotonic there — if they aren't,
the 1000x leg does not start).

**Checkpoints.** Full 24-check battery per curriculum at sparse checkpoints: every
20 (1x), 200 (10x), 2,000 (100x), 20,000 (1000x) episodes → 3 checkpoints per leg +
final. Interleaved cheap micro-checks: an 8-probe rotating subset (no reuse of
consumed probes, H-07 law) every 2,000 episodes at 1000x to catch mid-window
interference spikes (slice 16's asymmetric English→code / code→messy quizzes live
here). Ledger monitored continuously per slice 16's signature protocol.

**Budget question.** Efficiency metric E_c = episodes to first stage-exit pass of
curriculum c; exponent α_c = log10(E_c(1000x)/E_c(100x)). Code (finite formal
domain) is predicted α ≤ 0.2 — crystallization, not repetition. English (expressive
capacity, unbounded register space) α ≤ 0.5. Messy reality (noise is infinite)
α ≤ 0.5, with the bar on C5 novel-probe floors to detect noise-fitting.

**Interference at 1000x.** Slice 16's three signatures — cross-curriculum kills,
silent kills (no deliberative-standard citation), kill bursts >8/200eps with net
partition shrinkage — run continuously; at 1000x the window is 20,000 eps. The
deliberate-memory prediction: interference SATURATES because partitions and the
append-only ledger bound the damage mechanism — D_X(t) = baseline − interleaved
stays <5 points even over 60,000 episodes. If D_X exceeds 10 points and rehearsal
cannot restore within 2 cycles, or degradation appears with no ledger signature at
all (silent machinery contamination — the reasoning organs cross-contaminate
without any memory op, invisible to the ledger), the interleave design is killed.

**Battery at 1000x.** Expected saturations, preregistered before the run: C1's 90%
floor gets HARDER (60k episodes of retention) — meaningful; C6's 15-point delta
gets THINNER (a 60k-episode no-curriculum arm learns plenty from exposure) — if
the delta falls below 15 at 1000x while passing at 100x, that is a saturated
control, struck and re-preregistered with the experienced-control bar; C2's 0.75
transfer bar is predicted saturated — replaced at 1000x by hard-transfer probes
(code debugging → under-specified messy diagnosis with planted contradictions) at
bar ≥0.75, and the old bar retired if it hits ceiling. Every control must still
fire on its t4/11 positive fault arm at 1000x or be struck. Byte-identical reruns
required; audit buffers chunked under the 2^25-byte slice limit (validated
workaround); chunking must reproduce byte-identical replays or halt the leg.

## 4. Kill bar
- **Scale kill:** any control that passes at 100x but fails at 1000x on its unchanged
  bar kills the claim "this curriculum scales" — the leg is evidence, never a
  retune opportunity.
- **Budget kill:** α_c > 0.5 for any curriculum → the curriculum's episode cost is
  superlinear at scale; curriculum killed pending redesign.
- **Interference kill:** D_X(t) > 10 points with no ledger signature (silent
  contamination), or unrestorable by 2-cycle rehearsal → interleave design killed.
- **Battery kill:** <6 of 7 controls survive their 1000x positive controls →
  battery design dead; saturated controls (fire on genuine, silent on fault, or
  ceilinged) are struck and the battery re-preregistered.
- **Determinism kill:** any same-state result differs across reruns → halt all legs
  (substrate break). Integrity wrongness (C3) freezes advancement, never trains through.

## 5. Honesty notes
Weakest: the 100x leg doesn't exist yet (S100 gated, five-organ integration in
progress) — this entire design is a plan contingent on the 100x leg passing; the
1000x leg must not start on shaky 100x evidence. Micro-checkpoints are a
cost compromise (8 probes vs 24) and may miss spikes; this trades detection
latency for feasibility and says so openly. The no-curriculum arm at 60,000
episodes is no longer a "no experience" control — C6 measures curriculum added
value over raw exposure, which is the honest question at scale but changes what
a 15-point delta means. Ledger volume at 60k episodes is enormous (chunked, per
the slice-limit workaround); if replay cost dominates the run budget, that is a
toolchain fact to report, not a failure to hide.

## 6. Next build step
Do not start at 1000x. First: run S100 (6,000 eps) for the three isolated arms +
integrated arm, fit the E_c curves and check the battery survives the 10x→100x
jump with no saturation; only if all seven controls fire cleanly and α estimates
come in ≤0.5 does the 1000x leg get authorized. In parallel, cost the 60k-episode
ledger: measure chunked-audit replay time at the 100x volume and extrapolate
before committing the 1000x budget.
