# Senses inventory — Google Drive TNN upload (2026-09-20)

Status: INVENTORY COMPLETE. Read-only access; nothing in Drive was modified.
Inventory date: 2026-09-20. All ids/paths below are Drive file/folder ids for chaining.

## Canonical content roots (nested-TNN mess resolved)

The upload contains ~30 folders named "TNN" under different parents. The two
roots that matter for this program:

1. **Senses root (this inventory):** `My Drive / TNN / TNN / Research`
   - Folder id: `1RmVG3A2EPV4r6gFlayaCD1MyRdoVYaJA`
   - Modified: 2026-09-20T19:23:26Z
   - 1,797 children. Holds ALL R32/R33/R34 senses material below.
2. **Latest-modified TNN folder** (R33 native continuity):
   id `1SOpUCOmDflBQaCDDuTdX5URvBYMXEIQo` → `Research/` →
   `R33_NATIVE_N13A_FINGERPRINT_SCRATCH`, `R33_NATIVE_N17_R27_CONTINUITY`,
   `R33_NATIVE_IO_V1.zag`, `R33_NATIVE_SHA256_V2.zag`.
   Senses-relevant only as substrate copies; no new PAM/vision design found there.

Raw listing: `drive-inventory/research_folder_raw.json` (1,797 entries).
Senses-filtered catalog: `drive-inventory/senses_hits.json` (146 entries).

## A. Design / qualification documents (read in full)

| File | Size | What it is |
|---|---|---|
| `R33_SENSOR_QUALIFICATION_PLAN.md` | 4,671 | The S0/S1/S2 three-gate qualification contract. S0 transport (byte-originated), S1 information (paired counterexamples, raw bypass), S2 usable perception. Four-route factorial. Never silently convert out-of-envelope input. |
| `R33_B001_SENSORY_REVIEW.md` | 29,067 | Independent review of B000 negative witnesses + B001 corrective candidate. Defines the RawRecord architecture (owned immutable bytes + exact physical metadata + provenance + integrity + order identity). 9 falsification tests, 7 confounds, 11 component bugs (C01-01..C01-11) in the unexecuted B001 candidate. |
| `R33_NATIVE_N14_RESULT.md` | 4,342 | N14 bounded encoded-file S1 engineering PASS (182 child checks, 8 PCM16LE/RGB8 packets byte-exact after fresh-process reload, 14 malformed refusals with zero state mutation). Explicitly NOT mic/camera, NOT S2, NOT training. N14 consumed, may not rerun. |
| `R33_NATIVE_N06_RESULT.md` | 4,304 | N06 bounded raw sensor/trace/observer S0 PASS (377,264 sample/pixel values, 636 metadata fields, byte-identical two builds `b375cf44…`). Advances only the encoded-file lane. |
| `R33_N14_CLOSEOUT_SUMMARY.md` | 1,968 | N14 closeout: CLOSED BOUNDED ENCODED-FILE S1 PASS, consumed. |
| `R32_E45_E48_NATIVE_QUALIFICATION_REPORT.md` | 4,243 | Four valid native NEGATIVES (terminal-controller battery). R27 remains canonical. |
| `TNN_R34_V3_QUALIFICATION_CHECKLIST.md` | 1,952 | R34 qualification checklist. |
| `tnn-pre-v1-r6-rsi-SELF_ARCHITECTURE_REVISION.md` | 2,060 | Pre-v1 architecture revision note. |

## B. Native Zag sensor substrate (in Drive, pure Zag)

| File | Size | What it is |
|---|---|---|
| `R33_NATIVE_N14_SENSOR_INFORMATION/sensor.zag` | 7,076 | N06 sensor implementation copied byte-for-byte into N14. Byte-originated ingress (`rr_packet_validate`), durable blob store w/ SHA256, `sn_observe` generic observer (values + 12 physical metadata fields, no semantic labels). md5 `a2c227062200a8e830d4695fea61576a`. Identical copy in N06 folder and 8 other parents (10 copies total). |
| `R33_NATIVE_N14_SENSOR_INFORMATION/driver.zag` | 14,845 | N14 reconstruction-battery driver. |
| `R33_NATIVE_N14_SENSOR_INFORMATION/DESIGN.md` | 4,715 | N14 candidate design (8-fixture positive battery + negative refusal battery). |
| `R33_NATIVE_N14_SENSOR_INFORMATION/PREREGISTRATION.md` | 6,578 | Frozen prereg. |
| `R33_NATIVE_N06_SENSOR_TRACE/driver.zag` | 18,907 | N06 trace/observer driver. |
| `R33_NATIVE_N06_SENSOR_TRACE/PREREGISTRATION.md` | 6,337 | Frozen prereg. |
| `R33_B001_RAW_RECORD.zag` | 6,757 | RawRecord packet validator (`rr_packet_validate`, `rr_get32`). Reviewed in B001. |
| `durable.zag` | 14,389 | Durable telemetry/blob substrate (N05B journal lineage). |
| `R33_B001_COMPONENTS.zag` | 8,801 | B001 corrective candidate components (PCM16LE decode/encode, RGB8 ingest, order accept, protected LRU, chunk reconstruct). Reviewed-only; 11 bugs filed (C01-01..C01-11); never executed. |
| `R34_NATIVE_QUALIFICATION_STAGE_20260916/*.zag` | 1.2–7.9k | R34 memory lifecycle/association/hypothesis/provenance/curiosity Zag v1 files. |

## C. R32 acoustic/hearing PAM material (all REFERENCE_ONLY, Python/.pt)

- `R32_V39_RECURRENT_TEMPORAL_PAM_SEED_9714.pt` (408,065 B) + `R32_V39_CANDIDATE_RECURRENT_TEMPORAL_PAM_REFERENCE_ONLY.json`: 2-layer GRU, 20 epochs, val_loss 0.0569. Machinery: gradient-trained recurrent net; "memory" = hidden recurrent state. NO deliberate memory ops, NO memory-interface contract, NO CORE/USER separation. Claim boundary: "Native Zag reproduction is required before promotion."
- `R32_SEGMENTAL_PAM_DETERMINISTIC_COMPARISON_REFERENCE_ONLY.json`: two-seed comparison. DECISION (their own): **retire the gate-as-neural-sensory-bottleneck formulation; retain the frozen raw temporal route** — the raw route was stable across seeds, neural routes were seed-sensitive.
- `R32_LOCAL_HYPOTHESIS_PAM_SEED_35400.json` + `.pt` (372,963 B): local multi-hypothesis acoustic PAM, seed 35400.
- `R32_SEGMENTAL_PAM_SEED_35000/35001*.json`, `R32_DUAL_SEGMENTAL_PAM_SEED_35100/35101.json`: segmental/dual-segmental variants.
- R32 TTS PAMs (segmental recurrent, hybrid audio, dual segmental): reference JSONs + training logs + 2 `.py` sources. Output-side (speech synthesis) machinery, not hearing ingress.
- `R32_TTS_VOICE_DIVERSITY_RANDOM_REFERENCE_ONLY.json`: name contains RANDOM; voice-diversity experiment.
- `R31_ACOUSTIC_METACOG*.json`: acoustic resolver metrics (near_twin_active 0.997, etc.).
- `R32_EPISTEMIC_QUALIFICATION_V3_*`: stopped early — "Evaluator mismatch: control A was 0.7273 resolvable ... instead of authori[zed]".

## D. Vision (Python, all NO_GO honest negatives)

| Folder | Source | Result |
|---|---|---|
| `R51_P1_P2_TOOL_VISION_CORRECTION_20260918` | `r51_tool_vision.py` (7,094) | NO_GO — vision gate failed (tools gate passed) |
| `R52_LOCAL_VISUAL_GEOMETRY_20260918` | `r52_vision.py` (4,746) | NO_GO — occluded 0.6325 < 0.75 floor |
| `R53_OCCLUSION_MARGINAL_VISUAL_20260918` | `r53_vision.py` (4,670) | NO_GO — clean 0.8167, occluded 0.6229 |
| `R54_LEARNED_LOCAL_TEMPLATE_VISUAL_20260918` | `r54_vision.py` (4,199) | NO_GO — occluded 0.55 |

All four froze preregs before execution; all four failed their vision gates honestly.
Trajectory: hand geometric summaries → local cluster normalization → Bernoulli
occupancy prototypes → learned 3×3 templates; occlusion accuracy fell each step
(0.75 floor never met).

## E. Folders with run evidence

- `R33_NATIVE_N14_SENSOR_INFORMATION/`: BUILD_01..06, PREFLIGHT_01, admission pins, sha256 manifests, `INDEPENDENT_FINAL_REVIEW.md`, `POSTRUN_INDEPENDENT_REVIEW.md`.
- `R33_NATIVE_N06_SENSOR_TRACE/`: BUILD_01/02, admission registry, `ADMISSION_CONSUMED_EVIDENCE.json`.
- `R33_NATIVE_N14_LAUNCH_PRIMARY_V1/`, `R33_NATIVE_N14_RUN_PRIMARY_V1/`, `R33_NATIVE_N06_RUN_PRIMARY_V1/`: launch/run evidence.
- `R34_NATIVE_QUALIFICATION_STAGE_20260916/EVIDENCE/`.

## F. Explicitly NOT design evidence

- `.pt` binaries (4): unreadable as design; treated as opaque artifacts only.
- `.openai-download-*` suffixed duplicates: same content as canonical names.
- `SensorTest.h` (5,093 B, parent `1Ysa6dZ6UaXUfE0nyLzu-jiYToIc9qdk0`): C header, out of scope.
- `R32_E45_NATIVE_QUALIFICATION_NEGATIVE_*`: negative terminal-controller evidence (E45-E48), not senses ingress.
- R32 TTS/voice-diversity/streaming JSONs: output-side speech work, not sensory ingress.

## Bottom line for the redo

The Drive upload contains NO recoverable live-sensor (microphone/camera) design,
NO trained classifier with a memory-interface contract, and NO vision system that
passed its own gates. What it does contain: (1) a rigorous byte-originated
S0/S1 qualification contract + independent review, (2) a proven native Zag
encoded-file ingress/observer path (N06/N14), (3) an honest four-round vision
failure log, and (4) acoustic PAMs whose own comparison retired the neural
bottleneck in favor of the raw route. The redo starts from (1)+(2), not from (3)/(4).
