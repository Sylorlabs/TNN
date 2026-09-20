# Recovery Spec — what would answer "how were the 76 perceptual parameters learned?"

**Status:** the question is UNRECOVERABLE from sylorlabs/TNN as it stands
(see [ORIGINS.md](ORIGINS.md)). This document specifies exactly what artifact
or experiment would answer it, so any future recovery attempt is a targeted
retrieval, not another open-ended search.

## The missing provenance, precisely

To answer "how were the 76 parameters learned" with provenance, one needs all
four of: **(a)** the training code, **(b)** the training data, **(c)** the
objective/optimizer configuration, **(d)** the commit or run record binding
them to the accepted artifact. Current state of each:

| Item | Status in repo |
|---|---|
| (a) Training code | **Absent.** The pickle's class modules (`r15_master_training`, `r23_experiments`, `r25_release`, `r26_experiments`, `r27_experiments`, `r17_experiments`, `r20_experiments`) exist in zero tracked files (code search: 0 hits for every module and class name). The 148 Python files ever in git were R29–R32/v39 harnesses, removed by `9da6e30b29`. |
| (b) Training data | **Absent.** No dataset manifests, no audio/image corpora, no data dir contents (`data/` holds only `INDEX.md`). |
| (c) Objective / optimizer | **Absent.** Zero optimizer state, zero gradients, zero training-config keys in the 121,094-node pickle graph (`brain/STATE_SCHEMA.md` §8). |
| (d) Commit / run record | **Absent.** The pickle's first git appearance is `5802fec840` (2026-09-18, "Checkpoint TNN research state and ignore reproducible artifacts") — an import of external state, not a training run. No R7–R26 generation docs exist. |

## Artifact that would answer it (in priority order)

1. **The original experiment sources** — files defining the pickle's modules,
   most plausibly named `r15_master_training.py`, `r23_experiments.py`,
   `r25_release.py`, `r26_experiments.py`, `r27_experiments.py`
   (module names taken verbatim from the pickle's class references). These ran
   in agent sessions **before 2026-08-25** (oldest git commit `5da88e0164`)
   and were never committed. Recovery requires the session transcripts, logs,
   or working directories of the machine/account that produced
   `parent-r27-accepted-state.pkl` — i.e. Micah's pre-git experiment
   environment, if it still exists anywhere.
2. **Any run log from the R23–R27 training sessions** describing data,
   objective, and optimizer (the repo's `artifacts/run-logs/` holds only
   V17–V25 E-series validation logs; the R23–R27 logs are not there).
3. **A data manifest or dataset** matching the modules' input shapes
   (`RawConvSpeechPAM` = raw-waveform speech input; `ConvWordNet` = word-level
   conv features; `EntityHeadNet` = entity classification head). None in repo.

## Ruled out (do not re-search without new information)

- Full commit history (345 commits, `tnn-native-lab`) — searched; only
  content-bearing Python was R29+ harnesses.
- GitHub code search across all tracked files — 0 hits for all module/class
  names and for `Conv1d`.
- All 3 PRs, all 3 branches, `archive/`, `artifacts/`, `docs/generations`
  R5–R58, `src/tools/toolchain/`, the wiki surface (none), and the pickle's
  own internals (full node sweep by the wave-1 map).
- Pre-reorg paths: the pickle lived at `Research/R33_PARENT_RECOVERED_V1/`
  before reorg migration 41/47 (`5db2d6ec28`); its history before the
  2026-09-18 checkpoint does not exist in git.

## Unconfirmed lead (not evidence)

The only speech data ever named in the repo is synthetic eSpeak
(`history/DO_NOT_REPEAT.md` §7: "R31 speech tests were synthetic eSpeak
research only"). If the `RawConvSpeechPAM` modules were trained in the same
program culture, their data was likely synthetic audio — but **no document,
commit, or artifact states this**, and the R31 work postdates the pickle.
Treat as a hypothesis for re-derivation design, never as provenance.

## Recommended recovery path (practical, not historical)

Historical recovery depends on an environment outside this repo and may be
impossible. The productive substitute is **behavioral re-derivation**, which
answers the question the program actually needs ("what function must native
perception compute?") instead of the unanswerable one ("what exact gradient
run produced these weights?"):

1. Freeze the 76 torch parameters as **reference-only I/O oracles**
   (never promoted, never gradient-trained — consistent with the repo's
   REFERENCE_ONLY discipline, `DO_NOT_REPEAT.md` §6).
2. Probe each module's input→output behavior on designed synthetic curricula
   (clean → noisy → occluded → active-reinspection, the R50–R57 gate pattern).
3. Train native Zag equivalents to **behavioral parity** on those probes under
   preregistered gates, with all learning as ledgered structural revisions.
4. Record the native training's data, objective, and code with full provenance
   this time — closing the provenance gap by construction rather than by
   archaeology.

This is specified as a build plan in [NATIVE_PERCEPTION.md](NATIVE_PERCEPTION.md).
