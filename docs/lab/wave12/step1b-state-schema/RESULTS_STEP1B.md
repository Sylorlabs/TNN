# RESULTS — Step 1b: state schema + replay protocol + evolution law

**Date:** 2026-09-20. **Build:** pure Zag, zero RNG (static grep clean),
native toolchain `znc_linux_x86_64_abed8aa1`.
**Verdict: GO.** No kill bar fired. Two dated amendments filed
(AMENDMENT_2026-09-20_schema.md), pending Micah's re-approval.

## Build hashes (deterministic toolchain — both invocations identical)
- `c93b801799cc65013b84da517b814c4daea1322c87299730b962490d0faef71b`
  (state1b_bin_a: `--no-zagd --no-analyze --no-foreground-cache`;
   state1b_bin_b: `--no-zagd`) — see build_hashes.txt.

## Evidence (47/47 mechanical checks green, run_step1b.sh)

**Replay protocol (17): 1000/1000 on both build hashes.** 100 episodes × 10
replays; per trial: rebuild from event-log replay (not from the hash), decode
STATE_E, recompute output, re-hash mem/audit, constitution check. Zero
mismatches; rerun transcripts byte-identical (run_replay_a.txt).

**Input-order permutation fuzzer (18 §6): 600/600.** Three deterministic
arrival orders (identity / reverse / rotate-37) × 100 episodes × 2 replays —
inputs are data, permutations are data; every permuted trajectory replays
byte-identically (run_perm.txt).

**Differential-replay discovery (16): method works.** Planted unlogged
refinement-round counter (p = 0.05 exactly): 5 batches × 460 pairs →
23/460 divergences per batch, first alarms at pairs 7, 10, 13, 16, 19
(all ≤ 460), hunt FOUND `rctr` 5/5. Exposure matches the 1−(1−p)^N bound
(P ≈ 1 − 7.6e−11 at N=460). **16-K1 did NOT fire.**
Negative control: 460 pairs, no perturbation → 0 alarms (no false positives).

**K2 closure + retroactive re-validation (16 §3c):** under the amended v2
schema (rctr logged), 5×460 pairs → 0 alarms — divergence is now attributable
to a logged state difference. **16-K2 did NOT fire.** Replay suite re-run
under v2: **1000/1000** (run_diffk2.txt).

**Conformance (20 episodes):** clean replay 20/20. Taxonomy inventory —
Class A 20/20 (planted omitted budget block; classifier located block @136),
Class C 20/20 (planted hash-then-mutate; caught by decode-consistency
cross-check @16), Class B 0 by construction (static audit), Class D 1
(tampered constitution_ref → fail-closed REFUSE, no silent divergence).
Probes: KB3 smaller-id tie-break ✓, KB4 budget-exhaustion refusal (B
unchanged) ✓, KB4 canonical event ordering (60 episodes, 0 violations) ✓,
KB2 touch-mask verifier (every event, 0 violations) ✓, variation-slot
budget fallback to canonical variant with marker ✓, D-queue codec
roundtrip ✓ (run_conform.txt).

## Kill-bar status
- KB1–KB5 (18): none fired. KB2/KB4 enforced by in-driver verifiers on every
  event of every episode; KB3 by tie-break probe + id-ascending scans;
  KB1/KB5 by 1600 replay trials + 600 permutation trials, zero differences.
- 16-K1/K2: NOT_FIRED (both).
- 17 (1000/1000, both build hashes): passed; no Class B root cause anywhere.

## What this does not claim
Replay proves reproducibility, not lawfulness of variation (17 §5). The
460-pair bound assumes regime coverage (16 §5). Sensor-deceivability remains
an accepted hole — the law guarantees determinism, not truth (18 §5). The
canonical event ordering is a preregistered choice, not a theorem (18 §5).

## Files (→ docs/lab/wave12/step1b-state-schema/)
PREREG_STATE_SCHEMA.md (frozen, committed pre-build) ·
AMENDMENT_2026-09-20_schema.md · s1b_state.zag · s1b_trans.zag ·
s1b_codec.zag · s1b_run.zag · state1b.zag · run_step1b.sh ·
substrate/ (vendored R33 SHA-256 / IO / cl/common) ·
run_replay_a.txt · run_replay_b.txt · run_perm.txt · run_difftest.txt ·
run_diffneg.txt · run_diffk2.txt · run_conform.txt · build_hashes.txt ·
sha256sums.txt · RESULTS_STEP1B.md
