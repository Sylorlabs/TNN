# PREREG — Senses Phase 1: byte-originated ingress + deliberate memory-interface contract

Date: 2026-09-20. Status: **FROZEN BEFORE BUILD.**
Branch: `tnn-native-lab`. Dir: `docs/lab/wave12/senses/phase1/` (workspace: `~/workspace/tnn-lab/wave12/senses/phase1/`).

## Standing context

Drive inventory (`../INVENTORY_SENSES_DRIVE.md`) and assessment (`../ASSESSMENT_SENSES.md`):
R32 acoustic classifiers are DROPPED (no memory-interface contract — hidden GRU
state, seed-selected, not native Zag). R51–R54 vision are honest NO_GOs (Python).
What survives: the R33 S0/S1 qualification contract, the RawRecord architecture,
and the N06/N14 native encoded-file ingress path. The missing piece — the reason
the old work stays NOT_QUALIFIED — is the **memory-interface contract**: nothing
may enter deliberate memory except through a deliberate judged op.

## Falsifiable claim

A pure-Zag byte-originated sensor ingress plus a deliberate memory-interface
contract can be built such that:
(a) every admitted observation is byte-identical across replay from the same
    complete logged state;
(b) no observation enters deliberate memory without an explicit deliberate
    judgment (judgment code + declared strength + citation episode + region);
(c) malformed inputs are refused with zero state mutation;
(d) paired counterexamples differing in exactly one controlled item remain
    distinguishable at the memory interface;
(e) caller-buffer mutation after admission cannot alter the admitted record.

## Scope (bounded)

- Envelope: PCM16LE mono 8,000 Hz (payload ≤ 4,096 B) and RGB8 frames 1×1..4×4.
  Encoded-file fixtures authored deterministically in the driver. No live devices.
- Ingress: `TNNRAW02` 80-byte header (magic, version, encoding, params,
  payload_len, sha256(payload)) + payload. Transactional validate → reserve →
  commit. Explicit refusal codes. Owned copy on admit.
- Memory interface: 16-slot deliberate store. Slots carry live, region
  (CORE/USER), declared strength (1..100), judgment, citation episode, and
  provenance (sensor record id + payload sha256). Append-only op audit
  (256 entries × 8 words). ONLY `mi_observe` writes slots from sensor data,
  and only with judgment != NONE.
- Save/reload: records + memory image to files; fresh-process reload must be
  byte-identical.
- OUT OF SCOPE: live mic/camera, S2 learning/transfer, classifiers, N06
  durable-blob machinery (cited as prior, not re-implemented), performance.

## Kill bars (binding)

- **K-SE1 replay mismatch**: two full harness runs → byte-identical stdout.
  Any divergence kills.
- **K-SE2 silent admission**: admitting with judgment=NONE must refuse; an
  audit scan must show every live slot has a matching ADMIT entry. Violation kills.
- **K-SE3 refusal mutation**: after the malformed battery, record count and
  live-slot count are unchanged. Change kills.
- **K-SE4 aliasing**: mutating the caller buffer after admission must leave
  the stored record byte-identical. Difference kills.
- **K-SE5 computed strength**: static scan — the admit path performs no
  arithmetic on observation bytes to produce strength; strength is a declared
  caller parameter. Violation kills. (Honest boundary: caller discipline +
  static check; the audit records the declared judgment openly.)
- **K-SE6 RNG/wall-clock/threads**: static source scan over all phase-1
  sources. Hit kills.
- **K-SE7 save/reload identity**: fresh-process reload → byte-identical
  records, metadata, and memory image. Mismatch kills.
- **K-SE8 protected memory**: TNN-caller kill of a CORE-region or pinned slot
  must refuse. Success kills.

## Method

1. Static checks (K-SE5, K-SE6, bare @imports, vendored substrate).
2. Compile twice with the pinned znc; record build hashes.
3. `./se_bin_a harness` → `run_harness_a.txt`; `./se_bin_b harness` →
   `run_harness_b.txt`; diff must be empty (K-SE1).
4. `./se_bin_a verify <dir>` after harness saved state (K-SE7).
5. Mechanical bar checks: every `CL_CHECK,name,actual,expected` line must
   show actual == expected; any kill-bar probe failing aborts the verdict.
6. Verdict GO only if all checks pass and no kill bar fired. Any fired bar →
   verdict DEAD/KILLED with the witness committed as evidence.

## What this does not claim

No live-sensor qualification, no S2 perception, no classifier quality, no
vision beyond the RGB8 fixture envelope, no training readiness. Passing phase 1
establishes the ingress + contract skeleton only — the gate future classifiers
must pass through.
