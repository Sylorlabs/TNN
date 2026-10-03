# TNN wave11 — Track 2 (fenced RNG Arm B), slice 02: distributions, seeding, seed logging

## 1. Slice
Specify the RNG itself for Arm B: algorithm, distributions per injection point, exact seed derivation, and seed logging for byte-identical replay.

## 2. Falsifiable claim
A fenced RNG arm built as specified here (SplitMix64-derived subseeds, per-stream xoshiro256**,
ledger-logged subseeds written before first use) reproduces every Arm B episode byte-identically
from logged state alone; and any defect in seed logging aborts the run — it never silently
continues. If any replayed episode diverges by even one byte, or any defect falls through
silently, the claim is false and the spec is killed.

## 3. Design

**PRNG algorithm — two layers, both named, both seeded, no OS entropy.**
- *Seed-derivation KDF: SplitMix64.* Used once per (trial, episode, stream) to produce a
  subseed. Justification: designed exactly as a splittable mixer; excellent sequential
  decorrelation of its outputs; implementable in i64 add/mul/xor/shr only (fits Zag native
  codegen, no float, no atomics). It is never the draw generator — this keeps stream states
  independent of derivation.
- *Draw generator per stream: xoshiro256**.* Justification: 256-bit state, published and
  BigCrush-clean, fast, no long pathological runs, and its state is small enough to
  snapshot into the audit ledger. Deterministic given its 256-bit seed.

**Exact derivation (all values u64, i64 arithmetic):**
```
GOLDEN = 0x9E3779B97F4A7C15
mix64(z): z=(z^(z>>30))*0xBF58476D1CE4E5B9; z=(z^(z>>27))*0x94D049BB133111EB; return z^(z>>31)
derive(master, trial, episode, stream):
    s = mix64(master ^ GOLDEN)
    s = mix64(s ^ trial)
    return mix64(s ^ (episode | (stream << 32)))
```
Stream `s`'s xoshiro256** state = `[derive(...), mix64(derive(...) ^ 1), mix64(derive(...) ^ 2),
mix64(derive(...) ^ 3)]`. Streams: one per prereg-enumerated injection point
(tie-break=0, phrasing=1, exploration=2) per episode; independent by construction.

**Distributions at each injection point (justified):**
- *Tie-breaks:* uniform over N tied candidates — `uniform_int(n)` via Lemire's
  multiply-and-shift (no modulo bias). Uniform because a tie is defined as
  no-defensible-difference; any weighting would smuggle a hidden preference.
- *Phrasing candidates:* weighted choice, weights = the arm's own deliberate per-episode
  quality ranking (weights deterministic, computed before any draw), sampled by
  inverse-CDF over a u64 draw. Weighted because RNG may only choose *among acceptable
  expressions* — it must not surface a phrasing the deliberator ranked unfit.
- *Exploration (red-team only):* uniform over the prereg move set.

**Seed logging for byte-identical replay.** Before a stream's first draw, the engine
writes `op=RNG_SEED, trial, episode, stream_id, subseed` into the append-only audit
ledger (MA1's ledger, proven replayable: docs/lab/wave6/ledger-replay). The draw engine
holds no unlogged state: only per-stream draw counters in memory. Replay = read logged
subseeds, rebuild xoshiro256** states, re-run. Each episode additionally logs a u64
digest over all its RNG draws; replay recomputes it and a mismatch raises divergence.

**Seed-replay test.** (i) Run episode fresh, capturing logged seeds. (ii) Destroy all RNG
state; reconstruct streams from *logged seeds only* (master seed redacted from replay
input); re-run; outputs must match byte-identically. (iii) Desync probe: flip one bit of
one logged subseed — replay MUST diverge (proves logging is load-bearing, not ornamental)
and the digest check must fire.

**Fail-closed rule on seed-logging bugs.** Any draw requested from a stream with no
logged subseed, any failed seed-ledger write, or any digest mismatch aborts the episode
immediately and marks the trial cell INVALID — never silently fall back to a default or
zero seed, never continue on the hope of recovery.

## 4. Kill bar
The spec is killed (no patch-and-continue; re-specify from scratch) if any of: ≥1 episode
in the ≥200-episode replay set diverges by a single byte from its logged-seed replay;
the desync probe fails to diverge-and-fire; any draw is ever consumed outside a
prereg-enumerated stream; or any seed-logging defect is ever observed to fall through
silently. Separately, Arm B as a whole retires if it loses the comparison to Arm C on
adaptivity, judgment stability, integrity-trap performance, or replayability.

## 5. Honesty notes
- Weakest point: xoshiro256** quality is irrelevant to correctness — what matters is
  determinism and isolation. A "better" PRNG would not fix a logging bug.
- Weighted phrasing assumes weights are honestly ranked by the arm itself; if the
  ranking is gamed, RNG laundering follows. The weights are audited, not trusted.
- The digest check detects divergence, not causation — it proves *that* state split,
  not *why*. Diagnosis still needs the audit trail.
- NOT claimed: that Arm B is safe for canonical paths (amendment forbids it), that RNG
  adds intelligence (this spec is a measuring instrument for the comparison, nothing
  more), or that 200 replay episodes prove long-horizon stability.

## 6. Next build step
Build the seed-derivation + stream engine in native Zag as a standalone binary: run
200 episodes, destroy-and-replay from logged seeds, and run the desync probe. Nothing
else (no curricula, no comparison) until replay is byte-identical and fail-closed is
proven by the probe.
