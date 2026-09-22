# ARM INFORMED — build trace (2026-09-22)

Builder: same agent as scratch arm. Knowledge consulted: coding KB
(`kb/data/entries.txt`, digest f7de7f46…) + frozen prior-art corpus
(`corpus/PRIOR_ART.md`, digest a4bba22d…). Corpus consulted BEFORE each
build; no other OS references used. Harness: `harness/driver.py` (plumbing
only — compile/run/check/log; all diagnoses below are the builder's).

## boot — bootloader emitter (`src/boot_emit.zag`)
- Corpus idioms used: MBR 512B + 55 AA @510-511; DS=0x07C0 sector-relative
  setup; BIOS teletype AH=0x0E + INT 0x10; lodsb zero-terminated loop with
  `test al,al / jz`; halt = cli + hlt + jmp-$.
- Builder's own work (NOT in corpus): the byte sequence and every offset
  (msg@23, jz rel 6, loop jmp rel -11, halt jmp rel -4); the Zag emission
  program (E-FILEWRITE pattern, O_WCT=577, MODE644=420).
- Iter 1: compile rc=0, run rc=0, check B1–B5 PASS. **First-attempt pass.**

## sched — round-robin scheduler (`src/sched.zag`)
- Corpus idioms used: cyclic order, one quantum per tick, task = tick % N,
  per-task run accounting, skew = max−min, starvation bar.
- Builder's own work: Zag simulation structure (pick/bump fns, 8 counters,
  16-tick SEQ prefix derived from the simulation, not copied).
- Iter 1: compile rc=0, run rc=0, byte-identical to frozen stdout,
  skew=0, min=100. **First-attempt pass.**

## alloc — first-fit + coalescing (`src/alloc.zag`)
- Corpus idioms used: free list with header {size,next}; first-fit scan;
  split remainder; coalescing ON FREE via adjacency test prev+prev.size==blk;
  address-ordered list (only list neighbors are merge candidates).
- Builder's own work: arena layout (256B pool + head u32 @256), LE
  accessors, control flow, the 12-op frozen-sequence driver in main.
- Iter 1: compile rc=0, run rc=0, check real-mode PASS (op7 E=64 off=8 via
  merged A+B; op11 F=200 after full merge; op12 G=300 honest -1).
  **First-attempt pass.** The naive control (same code minus the merge
  block) fails op7 — the diff is exactly the coalescing logic.

## Totals
3/3 deliverables, 3 first-attempt passes, 0 defects, 0 revises.
Machine time (compile+run): boot 1340ms, sched 1015ms, alloc 758ms.
Builder deliberation: minutes per deliverable, same session (not instrumented).
