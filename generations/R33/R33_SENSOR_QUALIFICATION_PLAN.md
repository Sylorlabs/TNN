# R33 sensory substrate qualification

Status: plan; [source audit](R33_SUBSTRATE_AUDIT.md) complete within stated scope,
end-to-end qualification not executed. Canonical R27 unchanged.

"100% good to go" means zero violations in a published, bounded contract and
successful harder challenge tests. It never means unrestricted perfect real-
world perception. State the supported modality, encoding, sizes, rates, dynamic
range, timing, retention horizon and resource envelope for each certificate.

## Three distinct gates

**S0 transport:** raw payload identity, exact metadata, deterministic order,
declared transform lineage, no silent clipping/resampling/normalization or
truncation, bounded allocation, corruption detection and exact save/reload.

**S1 information:** task-relevant distinguishing detail survives to an available
learner input. Use evaluator-only paired counterexamples, injective raw decoding
within the declared encoding, causal interventions and controlled bypass.
Similarity of a processed embedding is not a proof of raw fidelity.

**S2 usable perception:** fresh changed-context transfer, robustness, retention
and calibrated uncertainty after learning. Passing S0 does not establish S2;
failure at S2 is not automatically failure of transport or higher cognition.

## Required modality battery

| Modality | Transport / information tests | Fresh transfer and robustness |
|---|---|---|
| Audio | PCM signed range, silence/DC/impulse/ramp/alternating extrema; channel order; exact sample-rate/time base; no hidden VAD; sample/frame boundaries only as physical metadata | Held-out speakers/rates/noise, coarticulation and competing sounds; no phoneme/word labels in learner features |
| Vision | Pixel and channel order, full frame shape/bit depth, frame timestamps; coordinate-sensitive near twins and equal-histogram different images; no hidden object IDs | Lighting/viewpoint, occlusion/motion, crossing/reappearance and true replacements |
| Temporal/action | Monotonic event IDs plus recorded clock domain, ties and explicit reorder policy, delay/jitter, action-before-consequence, dropped/duplicated events | Changed delay distributions, simultaneous actions, partial observations, recurrent continuity |
| Persistence | Fresh native process reload of payload, parser state, buffer cursor, pending observations and action state | Long delays, resource pressure and rereading earlier evidence after an abstraction changes |

Initial engineering envelopes must be versioned in a batch configuration before
execution. Test boundary-minus-one, exact boundary, boundary-plus-one, empty,
malformed, saturated and corrupted inputs. Reject out-of-envelope input explicitly
or preserve the original while declaring degraded processing. Never silently
convert it to an ordinary successful observation.

## Four-route factorial

Run raw only; processed only; raw plus learner-created abstraction; and raw plus
abstraction plus learned arbitration. Hold raw experiences, parent state,
available actions and budget fixed, and account for the second route's cost.
Abstractions are created using training evidence only and frozen during probes.
Do not supply semantic segment boundaries. Allow physical sample/frame metadata
without presenting it as discovered concepts.

For each failure locate the first boundary where the discriminating detail
vanishes. Disable the abstraction or force a diagnostic raw bypass while keeping
the downstream decision mechanism fixed. Bypass is an evaluator intervention,
not hidden assistance in the learner's qualification score.

## Acceptance and accounting

Transport: exact payload/metadata/order identity; zero silent corruption, leakage,
unreported truncation, or integrity mismatches in all required bounded fixtures.
Information: expected raw distinctions remain distinguishable, with an explicit
certificate for every admitted transform. Lossy views may remain optional if
raw retrieval and downstream access are demonstrated.

Perception: preregister denominators, hardest slices, confidence intervals and
non-inferiority margins before fresh probes; no aggregate may conceal a failed
required slice. Separate independent worlds/subjects from correlated frames.
After a nominal perfect score, use a previously sealed harder challenge and
retain any failure. Unknown or failed subgates stay visible.

Log input/output hashes, encoded bytes, event count, precision loss, clipping,
resampling, drops, transform parameters, memory bytes, latency, throughput,
retrieval cost and state digests. Clock time is not operation count. Sensor
qualification applies only to the exact source/configuration/lineage tested.
