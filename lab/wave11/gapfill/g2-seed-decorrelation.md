# TNN wave11 gap-fill G2 — seed-stream decorrelation + rotation governance (Track 2, Arm B)

## 1. Slice
Governance and test machinery for the fenced Arm B: a statistical decorrelation test
on the seed-derivation function, plus master-seed rotation cadence and seed-chooser
accountability across epochs. This is testing/fencing machinery, not an AI decision
path — no draw this slice produces ever influences a decision.

## 2. Falsifiable claim
If the derivation function in
`~/workspace/tnn-lab/wave11/t2-rng-arm/findings/02-seeding-spec.md`
(SplitMix64 mix-chain over (master, trial, episode, stream)) produces decorrelated
subseeds, then adjacent episode subseeds and adjacent stream subseeds are
statistically indistinguishable from independent uniform u64 draws on the
preregistered statistics — and if any master seed is ever reused, re-registered
without an accountable chooser, or not rotated on cadence, the ledger rejects the
epoch and voids the cell. A failed decorrelation statistic or a single accepted
seed-reuse event kills this slice.

## 3. Design
**(a) Decorrelation test on the derivation function.** Deterministic given the
inputs — the test is a pure function of (master, trial, epoch), so reruns are
byte-identical. Probe set: 4096 episodes x 3 streams (the three prereg-enumerated
streams from 02: tie-break=0, phrasing=1, exploration=2).
- T1 uniformity: chi-square on the top 6 bits of all 12,288 derived subseeds,
  64 bins, dof=63. Builder computes the alpha=0.01 acceptance band and commits
  it before the first run.
- T2 adjacent-episode decorrelation: lag-1 Pearson correlation over the 4095
  adjacent pairs (episode e, e+1), same stream, each u64 mapped to [0,1).
  Threshold: |r| <= 3.5/sqrt(4095) per stream; worst stream governs.
- T3 adjacent-stream decorrelation: same as T2 across the 2 adjacent stream
  pairs per episode (0-1, 1-2), pooled over 4096 episodes. Same threshold form.
- T4 avalanche: for 256 probe master values (one-bit flips off a baseline, plus
  the all-zero master), mean Hamming distance between baseline and perturbed
  subseeds must satisfy 32 +/- 4 (out of 64 bits), per stream.
Negative control (required, run first): feed the test a deliberately weak
derivation (linear: subseed = master + episode*K + stream) and confirm every
statistic fires. A test that cannot fire on a bad KDF is itself void.

**(b) Master-seed rotation cadence + seed-chooser accountability.**
- One master seed per trial; hard epoch rollover every 16,384 episodes: a trial
  that would exceed the cap must register a new epoch (new master seed) or stop.
  The derivation mixes (trial_id, epoch_id) alongside the master, so identical
  master values in different epochs still produce disjoint subseeds — the loader
  additionally rejects an identical master-seed hash regardless.
- Registration: before the first draw of an epoch, the loader writes
  `op=RNG_MASTER_REGISTER, epoch_id, trial_id, chooser_id, seed_hash(sha256),
  chooser_signature, timestamp` to the append-only audit ledger
  (MA1's ledger; replay-proven: docs/lab/wave6/ledger-replay). The plaintext
  master seed is stored in the trial's seed-manifest file (offline, committed
  before the run); only the hash is in the ledger, so the ledger can never
  double as the replay key and replay still flows from logged subseeds only
  (per 02's seed-replay test, master redacted).
- Who chooses: the trial's human operator or the build driver, named in
  `chooser_id`. A machine-chosen seed must come from a pre-committed seed
  manifest (list of master seeds committed to git on the tnn-native-lab branch
  before the trial starts); an ad-hoc seed chosen at runtime is rejected.
  No seed may be chosen by, or influenced by, the AI under test.
- Anti-reuse check: at registration the loader scans all prior
  RNG_MASTER_REGISTER entries in the ledger; if seed_hash already appears in
  any prior epoch or trial, registration fails closed and the trial does not
  start. Any draw requested from an epoch with no accepted registration aborts
  the episode and marks the cell INVALID (02's fail-closed rule, extended to
  epochs). Revocation of AMENDMENT_2026-09-20_RNG_ARM_B.md additionally
  disables all registrations (per 09's governance kill).

## 4. Kill bar
This slice is killed (no patch-and-continue) if any of the following fire:
- K1 (decorrelation): T1 chi-square outside the committed alpha=0.01 band; or
  T2/T3 |r| exceeds 3.5/sqrt(N) on any stream; or T4 avalanche mean outside
  32 +/- 4. Firing K1 kills the *derivation function* — it must be
  re-specified from scratch, not tuned.
- K2 (test integrity): the negative control fails to fire all four statistics.
- K3 (reuse/accountability): any master-seed hash appears in two
  RNG_MASTER_REGISTER entries; or any registration accepted without
  chooser_id + chooser_signature; or any draw logged under an unregistered
  epoch; or any registration with a seed not on a pre-committed manifest.
- K4 (rotation): any epoch exceeds 16,384 episodes without a rotation
  registration. K3/K4 firing on a trial voids that trial's B-vs-C cell
  (reported as non-result, not a win for either arm).

## 5. Honesty notes
- Weakest point: SplitMix64 was designed exactly to decorrelate sequential
  inputs, so T1-T4 are expected to pass trivially. That is fine — this is a
  regression guardrail and a negative-control anchor, not a discovery tool.
  It does NOT prove security-grade randomness (not needed) and says nothing
  about xoshiro256** draw quality (irrelevant per 02's honesty notes).
- The decorrelation test probes the KDF, not the streams; stream isolation
  (no cross-stream state sharing) is still 02's logging contract, tested by
  its desync probe, not by this slice.
- Accountability does not equal entropy: a named human chooser can still pick
  a weak seed. The manifest requirement and the anti-reuse scan bound the
  damage, not the chooser's judgment; seed strength itself is audited, not
  assumed.
- The 16,384-episode cadence is a round governance number, not derived from
  any exhaustion analysis; xoshiro256** periods make it wildly conservative.
  Saying so openly: the cadence buys auditability, not statistical necessity.
- NOT claimed: that passing decorrelation tests make Arm B lawful or
  intelligent (the arm remains a measuring instrument for the B-vs-C
  comparison only); that rotation prevents a malicious operator (it prevents
  silent reuse, nothing more); or that 4096 episodes predict long-horizon
  behavior.

## 6. Next build step
Build the standalone derivation-probe binary in native Zag: implement the 02
derivation chain, sweep 4096 episodes x 3 streams, compute T1-T4
deterministically, run the weak-KDF negative control first to confirm the
statistics fire, then commit the reference thresholds before any real Arm B
trial may register a master seed.
