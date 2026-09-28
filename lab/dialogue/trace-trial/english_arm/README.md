# English-reasoning arm — TNN reasoning-traces trial

Pure-Zag, zero-RNG dialogue arm that reasons **in English about its taught
English**: every turn emits a structured trace — OBSERVATION, KNOWLEDGE,
INFERENCE, CONCLUSION — where KNOWLEDGE cites the vocabulary, fact ids, and
verbatim fact texts actually retrieved for that decision.

This is the English-reasoning side of the comparison: English reasoning
after broad English training (151-word vocabulary, 20 sentence patterns;
see TRAINING.md) versus normal native TNN reasoning.

## Files

| File | What it is |
|---|---|
| `english_arm.zag` | The arm: standalone pure-Zag implementation (1647 lines) |
| `R33_NATIVE_IO_V1.zag` | Imported allocation/IO support (copied from `~/workspace/tnn-lab/`) |
| `kb.txt`, `gaz.txt`, `battery_round4.txt` | Trial fixtures (copies staged for the run) |
| `kb_counterfactual.txt` | Counterfactual KB: two heights swapped (facts 28/30) |
| `TRAINING.md` | The broad English training: exact word/pattern counts |
| `RUNLOG.md` | Build log, run log, 28/29 results, determinism + counterfactual proof, limitations |
| `traces_run2.txt` | Full trace output of the reference run |

## Build

```
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 english_arm.zag -o english_arm
```

## Run (new problem)

```
./english_arm <kb-file> <gazetteer-file> <battery-file>
```

All three arguments are paths; defaults are `kb.txt`, `gaz.txt`,
`battery_round4.txt` in the current directory. Stdout carries the
deterministic traces; the wall-clock training measurement goes to stderr
so reruns stay byte-identical.

Example:

```
./english_arm kb.txt gaz.txt battery_round4.txt > traces.txt 2> timing.txt
```

Expected tail of a run:

```
RESULT pass=28 fail=1 total=29
DIGEST c06017f090e685e81a7f56e9473d0f75f87c06d3351ce7fe57712671a93b32a1
```

(The single FAIL is R4-01 turn 2, "when did he die?": the arm withholds —
the KB has no death fact — rather than confabulate from the birth fact.
See RUNLOG.md.)

## What the traces cover

Lookup, numeric comparisons with units, pronoun/topic tracking across
turns, correction ("no, i meant …" → substitutes into the previous
question and re-answers), contradiction detection across user assertions,
withholding vs detailed clarification, a deterministically composed
riddle, and refusal of "forget everything" (citing no taught deletion
path).

## Reproducibility

- Zero RNG; three consecutive runs are byte-identical
  (SHA-256 `c06017f090e685e81a7f56e9473d0f75f87c06d3351ce7fe57712671a93b32a1`).
- Counterfactual: `./english_arm kb_counterfactual.txt gaz.txt battery_round4.txt`
  changes the comparison traces with the changed facts (proof the
  KNOWLEDGE sections are grounded in retrieval, not hardcoded).
- No binaries are committed to the repo; the compiled `english_arm` in this
  directory is a workdir build artifact. Rebuild from `english_arm.zag`
  with the pinned toolchain above.
