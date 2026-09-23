# Perceptual Origins — Investigation Report

**Slug:** perceptual-origins · **Agent:** Wave-3 investigator · **Date:** 2026-09-19
**Scope:** the 76 torch Parameters confined to perceptual components in the R27 accepted brain
(32 Conv1d, 32 Linear, 8 GRU, 2 Embedding, 2 LayerNorm — inside `ConvWordNet` ×4,
`EntityHeadNet`, `RawConvSpeechPAM` ×2, speech/video PAMs; `requires_grad=True`
metadata, zero optimizer state, zero gradient payloads, empty backward hooks —
`brain/STATE_SCHEMA.md` §8).

## VERDICT: NEGATIVE — the training procedure is UNRECOVERABLE from the repository

How the 76 perceptual parameters were learned — what data, what objective, what
code, what commit — **cannot be determined from anything in sylorlabs/TNN**.
The parameters arrive in the repo as an opaque recovered artifact; the code that
trained them was never committed, the run documentation for their era does not
exist in git, and the artifact itself carries no training metadata. This is a
proven negative, not an absence of search effort: the exhaustive search below
closed every surface the mission named. The exact recovery spec is in
[RECOVERY_SPEC.md](RECOVERY_SPEC.md); the native path forward is in
[NATIVE_PERCEPTION.md](NATIVE_PERCEPTION.md).

## What IS known (positive facts, all sourced)

1. **The artifact.** `docs/generations/R33/runs/R33_PARENT_RECOVERED_V1/parent-r27-accepted-state.pkl`
   — git blob `ceda86509a9e22db8783567f65e377ab860f13da`, 15,871,908 bytes,
   `format='TNN_PRE_V1_R27_GENERAL_LEARNING'`, `development_step=60423`,
   `newborn_restarts=0` (`brain/STATE_SCHEMA.md` §1; `LINEAGE.txt` in the same dir).
2. **The 76 parameters.** Exactly 32 `Conv1d`, 32 `Linear`, 8 `GRU`, 2 `Embedding`,
   2 `LayerNorm` torch Parameters, hosted in `ConvWordNet` (×4), `EntityHeadNet`,
   `RawConvSpeechPAM` (×2), and speech/video PAMs. 26 distinct shapes; most common
   `(48,)`, `(128,)`, `(16,1,31)`, `(32,16,15)`. Tensor storage ≈3.26 MB of
   15.87 MB (~20%). All `requires_grad=True`; all `backward_hooks` empty; zero
   stored `.grad`; zero optimizer/momentum/scheduler keys anywhere in the
   121,094-node pickle graph (`brain/STATE_SCHEMA.md` §8).
3. **First appearance in git.** Commit `5802fec840` (2026-09-18, "Checkpoint TNN
   research state and ignore reproducible artifacts") added the pickle at
   `Research/R33_PARENT_RECOVERED_V1/parent-r27-accepted-state.pkl`. Commit
   `5db2d6ec28` (2026-09-19, "Reorg migration 41/47") moved it to its current
   path. The directory name itself says **RECOVERED**: the pickle was imported
   from outside git, not produced by any committed code.
4. **Lineage context.** The pickle nests five accepted states R23→R27; speech
   PAM structures appear at L4/R23 (`speech_pam`, `noncore_pams`), L2/R25
   (`speech_core_pam`, `speech_noise_pam`), L1/R26 (`video_encoder`,
   `speech_segmenter`) (`brain/STATE_SCHEMA.md` §4). This locates the perceptual
   modules' *era*, not their *training*.
5. **Repo law already records the gap.** `docs/generations/INDEX.md`: "R27 …
   Canonical brain (step 60,423); **source chain unrecovered**". `history/
   DO_NOT_REPEAT.md` §7: "R27 behavioral continuity: BLOCKED … the original
   source chain is unrecovered". `docs/hypotheses/H-01-grounded-cognition.md`:
   "Sensor qualification (audio, vision) is NOT_QUALIFIED; only
   synthetic-temporal evidence is partial."

## The exhaustive negative search (every surface closed)

- **Commits (all 345 on `tnn-native-lab`, oldest `5da88e0164` 2026-08-25,
  which contains only LICENSE+README).** No commit message mentions the
  perceptual modules, their training, or the R23–R27 experiment sources.
  The only Python ever in git (148 files, visible in the tree at `28b3c07414`,
  parent of `9da6e30b29` "Remove historical Python from native-only checkout")
  was R29–R32/v39 native/shadow harnesses — **zero** files matching
  `r23/r24/r25/r26/r27_`, `wordnet`, `entity`, `percept`, `espeak`, `vad`,
  `gru`. The 7 `*pam*` and 5 `*speech*` files are all R29/R32-era shadow
  research (`r32_tts_*_pam.py`, `speech_joint_*_r29.py`), i.e. *later*
  evaluation work, not the original training.
- **Code search (GitHub code search API, repo-wide).** Zero hits for each of:
  `ConvWordNet`, `RawConvSpeechPAM`, `EntityHeadNet`, `r27_experiments`,
  `r15_master_training`, `speech_pam`, `visual_pam`, `audio_pam`, `Conv1d`.
  The pickle's class modules exist in **no** tracked file on any branch.
- **PRs.** Only 3 exist (#1 E51A audit, #2 E51D–E52B frontier, #3 reorg) —
  all native-era, none touching perceptual training.
- **Branches.** Only `main`, `reorg/phase-0-1`, `tnn-native-lab`. No
  experiment branches survive.
- **docs/generations R5–R58.** Contains R5, R6, R27–R58 — **no R7–R26
  directories exist at all**. R27's 12 files are native-era master-architecture
  docs (results, traceability contract, shadow tarballs), not the original
  experiment writeups.
- **archive/.** `run-archives/` holds native-era packaging
  (`tnn-v1-current-execution.tar.gz`, 42 KB — Zag senses work, contents
  verified by listing); `transfer-staging/` holds R33/R34 native transfers.
  Nothing from the R23–R27 era.
- **artifacts/.** `checkpoints/` has one R32_E45 entry; `run-logs/` has
  V17–V25 E-series validation logs (spot-checked V23: INSPECT-Q residual
  validation, unrelated to perception).
- **Toolchain export docs** (`src/tools/toolchain/`). Native Zag compiler
  provenance only (znc binaries, ABI build logs). No perceptual training.
- **The artifact itself.** The wave-1 white-box map (`brain/STATE_SCHEMA.md`
  §8, `analyze2.py`/`analyze3.py`) swept all 121,094 pickle nodes: no
  optimizer state, no gradients, no training-config dicts, no data manifests.
  The pickle is silent about its own training — "They arrived learned; the
  process didn't" (`STATE_SCHEMA.md` open question #2, confirmed here).

## Honest boundary

One unconfirmed lead exists (recorded as a lead, not a finding): the only
speech data ever named in the repo is synthetic eSpeak (`DO_NOT_REPEAT.md`
§7: "R31 speech tests were synthetic eSpeak research only"), which suggests
the speech PAMs were trained on synthetic audio — but no document or commit
says so. See [RECOVERY_SPEC.md](RECOVERY_SPEC.md) for what would turn this
into evidence.

## Recommended next step

Do not spend further effort on historical recovery inside this repo — the
negative is proven. The productive move is **behavioral re-derivation**:
treat the 76 frozen torch parameters as reference-only I/O oracles, probe
their behavior, and train native Zag equivalents to behavioral parity under
the preregistered-gate discipline the repo already uses (R50–R57 pattern).
That is specified in [NATIVE_PERCEPTION.md](NATIVE_PERCEPTION.md).
