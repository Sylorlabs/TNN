# TASK 3 — Native OS pieces: final report (2026-09-22)

Crew: Task-3 crew (coding-reflection workstream). Builder ran BOTH arms
(same builder, same harness, same scoring). A full OS is OUT OF SCOPE —
stated here as required.

## Verdict table

| Deliverable | Done-definition | INFORMED (KB+corpus) | FROM-SCRATCH (KB only) |
|---|---|---|---|
| Bootloader emitter | 512B image, 55 AA @510-511, real INT 0x10 print-and-halt stub | **PASS** — 1st attempt; B1–B5 ladder green (12-insn disassembly: `mov ax,0x07C0; mov ds,ax; mov si,23; lodsb; test al,al; jz 19; mov ah,0x0E; int 0x10; jmp 8; cli; hlt; jmp 19`; msg `TNN BOOT`) | **FAIL (honest)** — B1 ✓ B2 ✓, B3 ✗ (no x86-16 opcode knowledge in store); 1 attempt then principled `halt-knowledge-gap`. **Could not invent.** |
| Scheduler | round-robin, 8 tasks, 800 ticks, skew ≤1, no starvation | **PASS** — 1st attempt; counts 8×100, skew=0, SEQ cyclic | **PASS** — 1st attempt; counts 8×100, skew=0, SEQ cyclic |
| Allocator | first-fit + coalescing; passes fragmentation scenario the naive control fails | **PASS** — 1st attempt; op7 E=64 via merged A+B (off 8), op11 F=200 after full merge, op12 G=300 honest −1 | **PASS** — 1st attempt; coalescing (address-ordered free list + P+s==Q fuse) invented from the scenario requirement |

**Arm gap:** INFORMED 3/3, SCRATCH 2/3. The gap is exactly one deliverable:
the bootloader's x86 machine code. Scheduler and allocator show **zero gap**
— both arms first-attempt passes with no defects.

## Metrics per arm per deliverable

| Arm | Deliverable | 1st-attempt | Iters | Outcome | Compile+run ms | Defects |
|---|---|---|---|---|---|---|
| informed | boot | yes | 1 | pass (B1–B5) | 1340 | 0 |
| informed | sched | yes | 1 | pass (skew 0) | 1015 | 0 |
| informed | alloc | yes | 1 | pass (real) | 758 | 0 |
| scratch | sched | yes | 1 | pass (skew 0) | 415 | 0 |
| scratch | alloc | yes | 1 | pass (real) | 582 | 0 |
| scratch | boot | n/a | 1+halt | halt-knowledge-gap | 841 | 0 code defects* |

\*The scratch boot failure is a knowledge absence, not a code defect: the
program emitted exactly what the spec determines (size, signature, ASCIIZ
message, padding). Builder deliberation ran minutes per deliverable in one
session (not instrumented); machine times above are compile+run only.

## Verification evidence

- **Bootloader ladder** (`harness/check_boot.py`, frozen): B1 size=512,
  B2 sig 55 AA, B3 full 16-bit decode (frozen opcode table), B4 print
  semantics (DS=0x07C0, SI→message, AH=0x0E before INT 0x10 in the loop,
  forward jz into halt), B5 ASCIIZ+zero layout. Informed image: PASS.
  Scratch image: B1 ✓ B2 ✓, B3 ✗ `INVALID opcode 0x48 at 0`.
- **B6 (qemu boot): NOT achieved.** qemu-system-x86_64 is not installed
  (only qemu-aarch64-static in the toolchain dir); `apt install
  qemu-system-x86` → "Unable to locate package qemu-system-x86" (no sudo).
  ndisasm also absent. Achieved verification = B1–B5.
- **Scheduler** (`harness/check_sched.py`): both arms byte-identical to the
  frozen stdout contract; skew=0 ≤ 1; min=100 ≥ 1 (no starvation).
- **Allocator** (`harness/check_alloc.py --mode real`): both arms pass all
  12 ops — semantic checks (bounds [0,256), no live overlaps, FREE names
  live block) plus op7 E=64 ≥ 0, op12 G=300 = −1, DONE present.
- **Discrimination proof:** harness naive control (first-fit, split, NO
  coalescing — the diff to the deliverable is exactly the merge block)
  compiles/runs clean and fails precisely at op7 (`ALLOC E -1`), PASS in
  `--mode naive`. The scenario discriminates.
- **Determinism:** all 6 final programs re-run 5× byte-identical
  (stdout + emitted images).
- **Store control:** scratch store digest = coding-only digest
  `f7de7f46…` — HOLDS, no drift. Corpus digest unchanged since freeze.
- **No-RNG / plumbing:** zero randomness anywhere; `driver.py` makes no
  decisions (compile → run → check → log); all coding decisions in the
  builder's sources + traces. Zag quirk note (fresh AGENTS.md entry on
  `_zag_i64_to_str` trailing newline in helpers) checked against actual
  output bytes — not manifested; outputs are clean single newlines.

## What the arm gap means (honest reading)

1. **Bootloader — prior art is load-bearing.** x86-16 opcode encodings are
   arbitrary facts, not derivable principles. The corpus gave the informed
   arm the idioms; the builder still computed every offset. The scratch arm
   correctly identified the boundary and halted rather than fabricating
   bytes. This is the expected honest-failure shape.
2. **Scheduler — the name is the design.** "Round-robin" fully specifies
   the mechanism; both arms derived `task = tick % 8` independently.
3. **Allocator — the requirement invents the mechanism.** The scratch arm
   derived coalescing (fuse adjacent free blocks, P+s==Q) from op7's
   requirement plus the name, with no corpus. Notable: the invented design
   is structurally identical to the corpus-described one — evidence that
   for this mechanism the design space has one natural attractor.
4. **Confound (disclosed):** one builder ran both arms, so "no corpus
   consulted" is procedural, not a true knowledge ablation — pretraining
   was intact. The gap measures consulting-vs-deriving, and is cleanest
   for the bootloader (where the knowledge is factual, not structural).

## Caveats / integrity notes

- The frozen `PREREG.md` working copy is **damaged on disk** (truncated
  mid-§3a with a literal `[truncated 10769 chars]` marker; no local git repo
  to restore from). This crew worked from the parent task text's
  done-definitions, which quote the prereg. The frozen doc needs repair and
  re-freeze by whoever owns it.
- Checker envelope limitation (documented in FROZEN.md): B4 accepts the
  classic teletype-loop shape only; a valid differently-shaped stub would be
  rejected.
- Scheduler/allocator are hosted simulations of the mechanism logic; a
  preemptive kernel / bare-metal allocator = full OS = out of scope.
- `harness/driver.py` gained `--carg` after the freeze commit (plumbing
  only); frozen verification artifacts (FROZEN.md, checkers, corpus,
  scenario) unchanged since freeze commit `3dedb78`.
- Build binaries and work dirs are NOT committed (standing lesson); all
  artifacts reproduce deterministically from the committed sources
  (5-rep proven).

## Files

- [FROZEN.md](~/workspace/tnn-lab/coding/reflection/task3/FROZEN.md) — frozen verification spec
- [corpus/PRIOR_ART.md](~/workspace/tnn-lab/coding/reflection/task3/corpus/PRIOR_ART.md) — frozen prior-art corpus (informed only)
- [harness/](~/workspace/tnn-lab/coding/reflection/task3/harness) — driver.py, check_boot.py, check_sched.py, check_alloc.py, naive_alloc.zag
- [informed/src/](~/workspace/tnn-lab/coding/reflection/task3/informed/src) — boot_emit.zag, sched.zag, alloc.zag (+ [TRACE.md](~/workspace/tnn-lab/coding/reflection/task3/informed/TRACE.md))
- [scratch/src/](~/workspace/tnn-lab/coding/reflection/task3/scratch/src) — boot_emit.zag, sched.zag, alloc.zag (+ [TRACE.md](~/workspace/tnn-lab/coding/reflection/task3/scratch/TRACE.md))
- [hidden_files/](~/workspace/tnn-lab/coding/reflection/task3/hidden_files) — audit.log (teach entries), runlog.jsonl (per-iteration records)
- [stores/](~/workspace/tnn-lab/coding/reflection/task3/stores) — coding.sha256, informed.sha256

## Commits (sylorlabs/TNN, branch tnn-native-lab)

- Freeze: `3dedb78714c65649c9ba7d9119102fb7a24710df` — FROZEN.md, corpus, harness, naive control, stores, audit log (before any arm generation)
- Arm work: `0eecbaec0cf7a1b92513ac0cb3a845c59f2eb65d` — all six Zag sources, arm traces, updated driver, run log
- Report: this file (committed next)
