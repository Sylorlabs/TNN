# PAM Archaeology — Findings (T7-S01 / Wave 12 archaeology sweep)

**Date:** 2026-09-20 · **Agent:** T7-L1 builder · **Scope:** L1, L2, L3, L5
(L4 DEAD per Micah's standing correction — pre-git session files NOT searched,
not requested, not inventoried.)

**Verdict rule applied:** L1–L3 + L5 complete with logged coverage; zero
DESIGN-class hits → verdict **fragments only** (or "confirmed absent on searched
layers" if even fragments are disqualified). Per the standing correction, the
verdict is NOT held open for L4.

## Hit catalog

| ID | Location | Modality | Class | Pipeline-spec? | Parameters? | Provenance? | Runnable? | Recoverable? | Notes |
|---|---|---|---|---|---|---|---|---|---|
| PAM-ARC-001 | `~/workspace/tnn-lab/brain/STATE_SCHEMA.md` §7–8 (workspace file, no git ref) | vision+audio/speech | **fragment** (design-doc fragment) | no | partial (shapes listed, no values) | no | no | no | Names PAM organs (`visual_pam`, `audio_pam`, `speech_pam`, `speech_core_pam`, `speech_noise_pam`); documents 76 torch Parameters with shapes but no training provenance. Fails criterion (a) — no sensor→feature→representation→memory-interface contract. |
| PAM-ARC-002 | `~/workspace/tnn-lab/wave3/perceptual-origins/ORIGINS.md` | vision+audio/speech | **fragment** (investigation report) | no | no (params documented, no training) | no | no | no | Prior wave-3 effort; verdict: training procedure UNRECOVERABLE from repo. Records the negative evidence; not new. |
| PAM-ARC-003 | `~/workspace/tnn-lab/wave3/perceptual-origins/NATIVE_PERCEPTION.md` | vision+audio/speech | **fragment** (design-doc fragment) | partial | no | n/a | no | n/a | A forward-looking native PAM design spec (2026-09-19), explicitly "not yet executed". It proposes replacements for torch ops but contains no surviving historical PAM design — it is new work, not archaeology. Kept in catalog as context. |
| PAM-ARC-004 | `docs/generations/R33/runs/R33_PARENT_RECOVERED_V1/parent-r27-accepted-state.pkl` @ sylorlabs/tnn (blob `ceda86509a9e22db8783567f65e377ab860f13da`, 15.87 MB) | vision+audio/speech | **fragment** (artifact fragment, torch-era, no provenance) | no | yes (76 params) | no | no (class modules not in repo) | no | Torch-era parameter dump WITHOUT committed training provenance → FRAGMENT BY RULE per spec §3. First git appearance 2026-09-18 as external import ("Checkpoint TNN research state and ignore reproducible artifacts"). |
| PAM-ARC-005 | sylorlabs/tnn history (Research/r32_*.py @ `16c318c6`–`9da6e30b`; removed from native checkout by 9da6e30b) | audio/speech (synthetic TTS) | **fragment** | partial (module docstrings describe dual-route architecture) | **yes** (TRAINING.log committed) | yes (torch .pt seeds) | n/a | R29/R32-era shadow PAM research on synthetic TTS (`DualSegmentalTemporalPAM`, `RawWaveformMultitimescalePAM`, `TTSLocalHypothesisPAM`…). Fails criterion (a): acoustic classifiers outputting class logits, no sensor→feature→representation→memory-interface contract; later-era research, not the original PAM designs. |
| PAM-ARC-006 | sylorlabs/tnn: `docs/generations/R33/R33_B001_SENSORY_REVIEW.md` + `R33_SENSOR_QUALIFICATION_PLAN.md` @ `5802fec8` (via reorg path) | audio+vision (ingress) | **fragment** (design-doc fragment) | no | no | n/a | no | n/a | Sensory-ingress qualification criteria (S0 transport / S1 information / S2 usable perception). States what a sensory certificate must prove; does NOT itself describe a perceptual pipeline — a test plan, not a design. |
| PAM-ARC-007 | sylorlabs/tnn: `docs/generations/R33/runs/R33_NATIVE_N06_SENSOR_TRACE/`, `R33_B001_C02_RUN_PRIMARY_V1/audio_*.raw` @ `5802fec8` | audio (raw PCM) | **fragment** (artifact fragment) | no | n/a (byte-transport evidence) | yes (preregs+manifests) | yes (native Zag) | n/a | Native-Zag byte-ingress qualification runs (S0 raw-record traces). Sensory transport evidence only — not feature-extraction PAMs. Reviewed, excluded as non-candidates. |
| PAM-ARC-008 | sylorlabs/ghost_research branches asi-intelligence/frontier-relational-spectral: `07_agent_loop/src/perception.zig`, `step1_perception_plan.txt`, `16_agent_loop_live/src/perception.zig` | n/a (text corpus ingestion) | **not a candidate** | n/a | n/a | n/a | n/a | n/a | "Perception" = 16-byte corpus text ingestion into 128-bit Percept structs for the Ghost Scientist agent loop. Unrelated program (Ghost Scientist, not TNN); no vision/hearing semantics. Logged to document the alias sweep. |
| PAM-ARC-009 | sylorlabs/ghost_research history @ `39277e8`: `boundary_crossing/multi_sense.zig`, `docs/research/sense_genesis_round_w.md`, `sparse_poly_discovery/sense_genesis_round_w.zig`, `sensorimotor_closure_round_af.md` | n/a (rune semantics / artificial-life sense-genesis) | **not a candidate** | n/a | n/a | n/a | n/a | n/a | Multi-sense word-embedding disambiguation and organism receptor/effector-genesis experiments — Ghost Scientist program, unrelated to TNN PAMs. Logged to document the alias sweep. |

**DESIGN-class hits: 0.** No artifact meets both (a) explicit pipeline spec AND
(b) runnable artifacts or complete parameter set with provenance.

## Layer coverage logs

See `logs/l1-coverage.md`, `logs/l2-coverage.md`, `logs/l3-coverage.md`,
`logs/l5-coverage.md` (L4 intentionally skipped — DEAD per Micah 2026-09-20).

## Verdict

**Fragments only.** The only surviving perceptual material is the 76 torch
parameters inside the R27 accepted-state pickle (provenance-free by rule: not
a design), plus wave-3's own forward-looking NATIVE_PERCEPTION spec (new work,
not a recovery). Audio/vision remain NOT_QUALIFIED; the historical PAM designs
are not recoverable from any searched surface.

Next: Track 7's later slices must treat PAM vision/hearing as greenfield
rebuilds under the native-Zag laws — nothing to requalify.
