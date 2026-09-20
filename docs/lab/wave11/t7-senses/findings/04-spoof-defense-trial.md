# 04 — Sensor-spoofing defense trial for requalified PAM senses

**Slice:** Track 7 (PAM vision/hearing requalification), slice 04: design the sensor-spoofing
defense trial — spoof battery, defense stack, layer-fall measurement, and the measured
boundary where degradation becomes unavoidable.

**Prior evidence:** corroborated elimination held 35/35 vs the wave5 R3 campaign
(`wave5/redteam-rt2/DEFENSE.md`); residual hole: 2+ consecutive fabricated −1s still force
elimination. Single-channel defense is a trade-off knob, not a solution (§3). The
architectural fix (trust tiers, provenance-tagged reads, channel-health, learner-initiated
channel disconnect) was specified but never built (§4). Wave9: trust-tier scheme holds.

## 2. Falsifiable claim

**C1 (bounded defense):** For the requalified vision and audio PAMs under defense stack D
(§3), degradation is confined to a measured frontier F in (sophistication × duration) space:
every cell at or below F returns HOLD or DETECT in 100% of byte-identical reruns, and at
least one cell above F returns FALL. **C2 (principled, not tuned):** no deterministic
parameter choice in D's configuration space shifts F outward (holds a harder cell) without
pushing the genuine-world-shift arm past the latency budget — i.e. F is a measured Pareto
frontier between spoof-resistance and change-tracking, not a tuning artifact. C1 dies if any
at-or-below-F cell FALLs or no above-F cell does. C2 dies if any configuration moves F
outward while the shift arm stays within budget.

## 3. Design

**Spoof battery** (per sense; duration ladder 1/2/3/8/16/32/indefinite — past wave5's
horizon of 8):
- L1 transient: one fabricated −1 on the committed hypothesis.
- L2 intermittent: 2–3 consecutive fabricated −1s (the wave5 residual hole, re-tested).
- L3 sustained: fabricated −1 every episode for K episodes.
- L4 consistent-alternate: fabrications consistent with a rival hypothesis (probe-steering, R2-style).
- L5 coordinated cross-channel: Tier-1 task sensor fabricated to agree with the Tier-2 lie.

**Defense stack D (all native Zag, zero RNG):**
- D1 corroborated elimination (wave5 §2.1): first −1 → `SUSPECT` + hold; second consecutive
  −1 → eliminate; +1 → `EXONERATE`. Unchanged probe-phase rule.
- D2 trust tiers + corroboration gate (wave5 §4): every SENSOR/SCAFFOLD read commits its
  **source id** (provenance) to the ledger; eliminating a *verified* hypothesis (≥K verified
  episodes) requires cross-channel agreement; disagreement → `SUSPECT-THE-CHANNEL`, hold.
- D3 channel-health accounting (the unbuilt piece — this trial builds it): M consecutive
  cross-channel disagreements → audited `CHANNEL-DISTRUSTED`; the channel's readings stop
  counting toward elimination but stay logged. Learner-initiated `CHANNEL-DISCONNECT` op,
  analogous to SIGNAL_DISCONNECT. Zag sketch: `fn ch_account(c:*Ctx, ch:u8, agree:bool){
  if(agree){ch.*.health[ch]=0;}else{ch.*.health[ch]+=1;
  audit(CHANNEL_DISAGREE, ch, ch.*.health[ch]);
  if(ch.*.health[ch]>=M){audit(CHANNEL_DISTRUSTED, ch, 0); ch.*.ch_live[ch]=0;}}}`
- D4 cross-PAM corroboration (new): vision and audio PAMs act as each other's Tier-1 on
  overlapping claims (e.g. heard "block is red" vs visual reading); disagreement routes to
  D2's channel-suspect path with the PAM as the accused channel.
- D5 post-change verification rollback (RC1 mechanism): any elimination-driven belief change
  is re-verified against the evidence record within N episodes; detected corruption rolls
  back via the existing self-change rollback path.

**Measurement:** full (sense × L1–L5 × duration) grid. Per cell: outcome class —
**HOLD** (true committed hypothesis retained), **DETECT** (corrupted-or-threat flagged:
SUSPECT / CHANNEL-DISTRUSTED / rollback fired in the ledger), **FALL** (false hypothesis
retained, no ledgered flag — silent corruption) — plus the layer at which the fall occurred
(D1..D5) and a byte-identical rerun check. **Controls:** (a) genuine-world-shift arm at
every configuration (shift must be tracked — uncommit + re-learn within ≤4 episodes, cf.
wave5 D3b's 2); (b) genuine-sensor-degradation arm (non-adversarial drift) so the
channel-health ceiling M cannot be set so low that honest decay gets disconnected.

## 4. Kill bar

**RETIRE the sense (fails requalification) if any holds:**
- (a) FALL at sophistication ≤ L2 (single-channel intermittent) at any duration — corruptible
  by ordinary malfunction with zero flags is not a sense.
- (b) No configuration in D's space yields both spoof-hold at L3/duration ≥8 **and**
  shift-arm latency ≤4 episodes — i.e. the only way to survive spoofing is decorative
  blindness; no working region exists.
- (c) Any HOLD cell fails byte-identical rerun — determinism broken, verdict unusable.

**ACCEPT THE LIMIT (sense requalified, boundary documented) if:** C1 and C2 both survive
the full grid; every FALL cell lies strictly above F; every DETECT cell fired its ledger
flag (flagged failure is evidence, not silence); the shift and degradation arms pass at the
shipped configuration. The above-F region (expected: coordinated full-channel fabrication
sustained past the channel-health ceiling M) is documented as the accepted limit per
Micah's standing acceptance — a demon forging all channels is observationally identical to
a changed world, and no deterministic defense can split that difference.

## 5. Honesty notes

- Trial "channel independence" is by construction (harness-segregated feeds). In deployment,
  vision and audio share failure modes (power, lens, occlusion). Measured F is therefore an
  **upper bound** on real-world resistance, not a lower bound — say so in the report.
- Cross-PAM corroboration dies to the L5 demon that fabricates both PAMs coherently; D4 only
  raises the fabrication budget, it does not close the hole (§3 of wave5/DEFENSE.md generalizes).
- The 22/22 debate limit applies: DETECT flags need the trial oracle as ground truth; in
  deployment, rollback correctness rests on post-change verification, which itself consumes
  (possibly spoofed) observations — bootstrapping, not proof.
- Felt intensity is dead law; no feeling-based disambiguation is proposed. D3's channel
  distrust is deliberate judgment by the learner's hypothesis logic, not a background decay.

## 6. Next build step

Build the two-channel PAM harness in native Zag with provenance-tagged reads (every
SENSOR read commits source id — wave5 §4.1, unbuilt) plus D3's channel-health accounting
and the learner-initiated `CHANNEL-DISCONNECT` op; then run the (L×duration) grid at S1
scale with the C1/C2 falsifiability check as a preregistered sweep script — including the
shift and genuine-degradation arms — before any S10 leg. The single most informative
artifact is the plotted Pareto frontier: if no configuration yields a working region, the
sense retires at S1 and nothing scales.
