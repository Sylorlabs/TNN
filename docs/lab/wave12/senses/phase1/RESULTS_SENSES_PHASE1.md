# RESULTS — Senses Phase 1: byte-originated ingress + deliberate memory-interface contract

Date: 2026-09-20. Branch: `tnn-native-lab`.
Prereg: `PREREG_SENSES_PHASE1.md` (**frozen before build** — this file reports against it).

## Verdict: GO

All 69 preregistered mechanical checks passed, all 8 kill bars probed and
unfired, two-build hash identity, byte-identical reruns, fresh-process
save/reload byte-identity.

## What was built (pure Zag, native)

- `se_ingress.zag` — RawRecord-lite ingress. `TNNRAW02` 80-byte header
  (magic, version, encoding, params, payload_len, sha256(payload)) + payload.
  Transactional validate → reserve → commit; owned copy on admit; explicit
  refusal codes (bad magic/version/encoding/param/len/hash, no capacity).
  Save/load via a single `records.bin` image.
- `se_memif.zag` — the deliberate memory-interface contract. 16-slot store;
  slots carry live, region (CORE/USER), **declared** strength (1..100),
  judgment, citation episode, and provenance (sensor record id + payload
  sha256). ONLY `mi_observe` admits sensor data into memory, and only with a
  non-NONE judgment. Deliberate kill needs evidence and refuses pinned/CORE.
  Recall is read-only. Append-only 256-entry op audit.
- `se_main.zag` — harness driver. Modes `harness` (full battery + save) and
  `verify` (fresh-process reload + re-verification).
- `run_phase1.sh` — static checks, two builds, two harness runs, replay diff,
  mechanical CL_CHECK verification, cross-build verify run.
- Substrate vendored: R33 native IO + SHA256-V2 + `cl/common.zag` (hashes in
  `SUBSTRATE_SHA256.txt`).

Envelope (prereg-bounded): PCM16LE mono 8,000 Hz (payload ≤ 4,096 B) and RGB8
1×1..4×4 frames. Deterministic encoded fixtures authored in the driver.

## Kill-bar probes (all fired clean — i.e. the probes behaved, the bars did not fire)

| Bar | Probe | Result |
|---|---|---|
| K-SE1 | Two full harness runs, diffed | byte-identical stdout, PASS |
| K-SE2 | admit with J_NONE / bad judgment / strength 0/101 / bad region / cite −1 / bad rec id; audit scan | all 7 refused with exact codes; `audit_scan`=1; every live slot traces to an OBSERVE entry |
| K-SE3 | 11-item malformed battery (bad magic, version, encoding, rate 7999, channels 0, odd payload, len mismatch, corrupted hash, RGB width 0, RGB len mismatch, truncation) | all refused with exact codes; record count and live-slot count unchanged; refusals=11 |
| K-SE4 | mutate caller buffer after admission | stored record byte-identical to pristine copy |
| K-SE5 | static scan: no strength computation from observation bytes | strength only caller-declared; PASS |
| K-SE6 | static scan: RNG / wall-clock / threads / floats | clean; PASS |
| K-SE7 | fresh-process reload of records + memory image | byte-identical records, metadata, 16 live slots, twin distinction survives; PASS |
| K-SE8 | kill pinned → PINNED; kill CORE → CORE; kill with evidence=0 → NO_EVIDENCE; legit kill OK; re-kill → NOTLIVE | all exact codes |

S1 paired counterexamples: PCM sign twin (sample[7] −1 vs +1) stays
distinguishable; RGB pixel-permuted twin has identical byte histogram but
different bytes. Both survive reload.

## Build determinism

Two independent znc compilations → identical binary hash
`08c3dc23b09629f684aeab02df5c86818e05d337395fcf498ff62ad789cf4261`.
Harness logs: `logs/run_harness_a.txt`, `logs/run_harness_b.txt`,
`logs/run_verify.txt`; `logs/replay_diff.txt` is empty.

## Honest boundaries (what this does NOT claim)

- No live-microphone/camera qualification, no S2 perception, no classifier.
- The delayed-credit/formula-strength machinery from R34 is NOT used:
  strength is declared by the caller and audited; the module performs no
  computation on observation content to produce it.
- N06/N14 executed evidence is cited as prior, not re-implemented; the
  durable-blob machinery is out of scope.
- Audio and vision remain **NOT_QUALIFIED** as senses. This phase establishes
  the ingress + contract skeleton only — the gate future classifiers must
  pass through.

## Files

- `PREREG_SENSES_PHASE1.md` (frozen pre-build)
- `se_ingress.zag`, `se_memif.zag`, `se_main.zag`
- `run_phase1.sh`, `SUBSTRATE_SHA256.txt`, `substrate/`
- `logs/` (build hashes, harness runs A/B, verify, empty replay diff)
- This file.

Excluded from commit (house convention): `se_bin_a`, `se_bin_b`,
`.zag-cache/`, `se_p1_store/` (regenerable store data).
