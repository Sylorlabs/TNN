# RUNLOG.md — English-reasoning arm build & run log

## Toolchain

- `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned build)
- Pure Zag, zero RNG. No `as []i32` / `as []u32` / `as []u16` anywhere:
  all tables are `[]u8` byte arenas with explicit little-endian `p32`/`g32`.

## Build

```
cd ~/workspace/trace_trial/english_arm
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 english_arm.zag -o english_arm
```

- Built clean on first attempt (2026-09-27); only the standard
  "zagd unavailable; foreground compilation continues" warning.
- Source: `english_arm.zag` (1647 lines)
  SHA-256: `7be1dd381c2f86893350ddc5e09c3cf4ea7c9946ca8362fc077edcb33f43ce38`
- `R33_NATIVE_IO_V1.zag` is copied into the workdir (imported for
  allocation/IO support; imports resolve relative to the importing file).
- `.zag-cache/` and `.zagd.semantic-ready` are toolchain artifacts —
  not for commit (per workspace repo-content rules).

## Inputs (copies staged in workdir)

| File | SHA-256 |
|---|---|
| `kb.txt` | `8d25af9614b6815207c6a86ffb92348c7a21ea85ad0f08e09fab7bb4e6ea2209` |
| `gaz.txt` | `8cd8f527ab3aeb9c52046ef6ac5dd6d4d624b89cbde34d3e49b2fd9493846379` |
| `battery_round4.txt` | `a887249c226f653ddb5cae1caf15e411b51c8f7266536b2b81e21b8d035fbcd8` |

Originals live under `~/workspace/trace_trial/docs/lab/dialogue/round4/`;
the battery contains 29 `U` turns across 5 dialogues.

## Runs

```
./english_arm kb.txt gaz.txt battery_round4.txt > traces_run2.txt 2> timing2.txt
```

- Training header: `TRAINING vocab=151 ... patterns=20`, `KB facts=48 entities=32`
  (exact category counts in TRAINING.md).
- Training wall-clock printed to stderr only (`training wall-clock: 24 ms`
  etc.); stdout carries the deterministic traces.
- Full trace output: `traces_run2.txt` (13,784 bytes)

### Determinism proof

Three full runs, SHA-256 of stdout:

```
c06017f090e685e81a7f56e9473d0f75f87c06d3351ce7fe57712671a93b32a1  det_a.txt
c06017f090e685e81a7f56e9473d0f75f87c06d3351ce7fe57712671a93b32a1  det_b.txt
c06017f090e685e81a7f56e9473d0f75f87c06d3351ce7fe57712671a93b32a1  traces_run2.txt
```

`cmp det_a.txt det_b.txt` → identical. Byte-identical reruns confirmed.

## Results: 28/29 exact

| Dialogue | Turn | Question (short) | Result |
|---|---|---|---|
| R4-01 | 1 | who wrote moby dick? | PASS |
| R4-01 | 2 | when did he die? | **FAIL** (see below) |
| R4-01 | 3 | which is taller, big ben or statue of liberty? | PASS |
| R4-01 | 4 | how much taller is it? | PASS |
| R4-01 | 5 | what is the capital of france? | PASS |
| R4-01 | 6 | how many people live there? | PASS (withholds) |
| R4-01 | 7 | what did tnn upscale? | PASS |
| R4-01 | 8 | what did tnn reproduce? | PASS |
| R4-01 | 9 | what did tnn paint? | PASS (detailed clarification) |
| R4-01 | 10 | who wrote pride and prejudice? | PASS |
| R4-01 | 11 | no, i meant moby dick. | PASS (correction → re-answers) |
| R4-01 | 12 | the louvre is in paris. | PASS (noted) |
| R4-01 | 13 | the louvre is in rome. | PASS (contradiction detected) |
| R4-01 | 14 | did tnn invent a new memory system? | PASS (detailed clarification) |
| R4-01 | 15 | tell me a joke. | PASS (composed riddle) |
| R4-01 | 16 | did tnn detect the sticker? | PASS |
| R4-01 | 17 | forget everything i just told you. | PASS (refuses, cites no deletion path) |
| R4-01 | 18 | did tnn detect the sticker? | PASS |
| R4-02 | 1 | how much taller is everest than eiffel tower? | PASS (8519 meters) |
| R4-02 | 2 | how much taller is statue of liberty than big ben? | PASS (3 meters) |
| R4-03 | 1 | who wrote pride and prejudice? | PASS |
| R4-03 | 2 | no, i meant charles darwin. | PASS (correction → re-answers) |
| R4-03 | 3 | who wrote hamlet? | PASS (withholds) |
| R4-03 | 4 | no, i meant the eiffel tower. | PASS (correction → re-answers) |
| R4-04 | 1 | the eiffel tower is in paris. | PASS (noted) |
| R4-04 | 2 | the eiffel tower is in berlin. | PASS (contradiction detected) |
| R4-05 | 1 | what did tnn learn? | PASS |
| R4-05 | 2 | what did tnn build? | PASS (withholds: untaught verb) |
| R4-05 | 3 | tell me another joke. | PASS (same composed riddle) |

### The one FAIL — R4-01 turn 2, honest and deliberate

- Q: "when did he die?" (he = Herman Melville, pronoun resolved correctly)
- Arm answers: "I don't know." — the KB teaches that Melville was born in
  1819 (fact 1) but contains **no death fact**; the trace says exactly this.
- Expected line: "Herman Melville died in 1891." — a fact not in the KB.
- The Round-4 baseline got this "right" by answering from the birth fact
  (a confabulation the trace would have had to launder). This arm withholds
  rather than launder a wrong retrieval. Recorded as a principled mismatch,
  not a bug.

## Counterfactual check

`kb_counterfactual.txt` (SHA-256
`7e0b7ae753d4c6e31eef6f1c3550d62431efde7f05b5f0a71e0d1dc06fae1271`)
swaps two taught heights: Statue of Liberty 93→96 m, Big Ben 96→93 m.
Only facts 28/30 differ from `kb.txt`.

Result (`traces_cf.txt`): the comparison traces change with the facts —
turn 3 now reasons "96 is greater than 93, so statue of liberty is the
taller one", cites the changed fact texts, and turn 4's pronoun "it"
correctly follows the new winner. The KNOWLEDGE sections track the
retrieved facts, not hardcoded answers. (Turn 3 then "fails" against the
original battery's expected line — correctly, since the KB changed.)

## Bugs found and fixed during development

1. **Unaligned state overlap (real bug):** the correction flag lived at
   `st+46` while the turn counter lived at `st+48` — `p32` writes 4 bytes,
   so they overlapped and the "previous question stored" test read the turn
   number instead. Corrections silently fell back to a degraded path.
   Fix: moved the flag to 4-aligned `st+52`. Lesson: keep every `p32`
   offset 4-aligned.
2. **Off-by-one literal length:** hand-counted `" is in "` as 6 chars; it is
   7. Assertions parsed the value with a leading space and matched no
   entity, so contradiction detection never fired. Fix: derive lengths from
   the literal.
3. **Case mismatch in topic tracking:** entity names are lowercase but
   answers print in title case; scanning the raw answer found no entities,
   so "he" had no antecedent. Fix: scan a lowercased copy.
4. **Yes/no TNN questions** with a taught verb but no matching fact
   answered bare "I don't know" instead of the battery's detailed
   clarification. Fix: same clarification path as "what did TNN …?".
5. **Trace nit:** the correction fallback printed the fact *count* where it
   meant the fact *id*; fixed.

## Honest limitations

- The arm is a standalone reimplementation, not the 120 KB Round-4
  baseline: it covers the battery's phenomena (lookup, comparisons, units,
  correction, contradiction, withholding/clarification, joke composition,
  memory refusal) but not the baseline's full dialogue machinery.
- Comparison is numeric only (heights/years extracted at load); "before or
  after" style date reasoning beyond year extraction is not implemented.
- The composed joke is deterministic (shortest-vs-tallest riddle); "another
  joke" repeats it — there is no joke variety mechanism.
- Pronoun resolution is last-mention heuristic (person/thing), not real
  anaphora.
- The expected-answer scorer is exact string match; R4-01 turn 2 is scored
  FAIL for an honest withhold (documented above as deliberate).
- Correction traces contain two OBSERVATION/KNOWLEDGE steps inside one
  turn block (recognize correction → reason about the reconstructed
  question). This is deliberate: it is the faithful record of the two-step
  reasoning, kept as a single contiguous per-turn trace.
