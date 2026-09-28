# Contender D — RED TEAM (§5)

Self-red-team before claims. Every attack below was actually run 2026-09-24
against the final binaries. "Survived" means: no hang, no crash, no silent
corruption, behavior matches the documented contract.

## Sustained corruption (1292 blocks × 64 samples)

- **D2** (`susfaultmix` on `plan_long`): `ABSTAIN code=3` — the cue window no
  longer matches its plan-pure re-render, so the latch refuses to copy a pitch
  from corrupted audio. No hallucination, no crash. The damage itself is not
  healed (D2 has no repair story — documented).
- **D1** (`seq+susfaultmix` on fixture): 82,688 diffs, 100% inside fault blocks,
  0 outside. Damage cannot propagate: generation never reads the mix.

## Adversarial plan-text inputs (D2; D1 shares PAR's parser verbatim)

| Plan | Result |
|---|---|
| `plan_adv_emptywin.txt` — RESPOND window contains no events | `ABSTAIN code=1` → nominal rendered. Correct. |
| `plan_adv_badwin.txt` — window w0 > w1 (degenerate) | `ABSTAIN code=1` (gate 1 fires before the span check) → nominal. Correct; no hang. |
| `plan_adv_nomlie.txt` — nominal `1e18` (atof drops the exponent → 1.0) | `LATCHED f0q=28835840` (exact 440). The nominal is ignored by design; the PAR-shared parser gap is documented, not fixed (fixing the shared parser is out of scope). |
| `plan_adv_chain.txt` — second RESPOND whose window covers the first (latched) RESPOND | e=1 latches 440; e=2 `ABSTAIN code=1` → nominal 881. Latched RESPONDs (field12=1) are excluded from cue candidacy — no latch-chaining. Correct. |
| `plan_adv_hugeamp.txt` — cue amp 999999999 (i64 overflow in voice math) | Completes, no hang; latch still fires — the integrity gate survives because scratch and mix overflow *identically* (deterministic wraparound both sides). Rendered audio is garbage (wraps), PAR-shared. Documented, not hidden. |

## Polyphonic RESPOND cues

Multi-trap e=4 (220+330 dyad): `ABSTAIN code=1` → nominal. Two-voice and
three-voice windows tested via the same gate (ncue ≠ 1 → abstain). No
attempt to "pick a voice" — abstention is the contract.

## Sub-octave nominal lies

Near-miss plan (nominal 460, true cue 440): D2 latches the cue's declared
440 → 0c. The lie in the nominal is irrelevant because the nominal is never
trusted. Original plan (nominal 880, cue 440): latch 440 — the octave lie is
corrected, matching hybrid v2's latch on this case.

## Vibrato / glide cues vs the ZCR sensor

D2 never runs the ZCR sensor in its decision path — the sensor exists only in
`tests/measure_zcr.py` as a disclosed-biased instrument (−60c on the 440
response, −75c on D1's 880 nominal). Vibrato on the cue cannot perturb the
latch: the pitch comes from the plan's declared Q16 f0, and gate 2
(byte-compare of the re-rendered cue window) rejects any cue the renderer
cannot reproduce exactly. A glide cue (nonzero glide) renders identically in
scratch and mix (same pure function) → still latches the declared f0.

## Order permutation (§5: scrambled order must be bit-identical)

D1: seq == rev byte-identical (wav `cmp`), pre- and post-rebuild.
D2: seq == rev byte-identical. (Stride mode also exists; the two orders tested
suffice for the visit-order-independence claim since rendering is a pure
function of (plan, t).)

## Parser rail-pins (shared PAR parser — result applies to D1/D2/PAR equally)

Extreme numerics (1e18 nominal, 999999999 amp) complete without hang or crash.
Overflow wraps deterministically; no input tested produced a hang (all runs
under `timeout`). Negative/zero durations and degenerate windows abstain or
render empty. No new parser attack surface was added by either contender.

## What was NOT red-teamed (out of scope, documented)

- B/C cross-region leakage: N/A — D builds audio only (no B/C implementation).
- Video/dialogue/image paths: NOT TESTED — no D implementation; verdicts for
  those paths are `NOT TESTED`, never inferred.
- Native binary re-measurement: no native binary exists in the workspace;
  NATIVE's RT-LONG behavior is taken from the prereg's documented presumption
  (nominal rendering → 76.7c on the near-miss), disclosed in VERDICT.md.
