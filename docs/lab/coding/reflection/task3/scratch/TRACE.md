# ARM FROM-SCRATCH — build trace (2026-09-22)

Builder: same agent as informed arm. Knowledge consulted: coding KB ONLY
(`kb/data/entries.txt`, digest f7de7f46…). The prior-art corpus was NEVER
opened during this arm (it was authored and frozen beforehand — the
pretraining confound is disclosed in REPORT.md; the procedural bar is
no-consultation, and each derivation below is recorded from the spec).

## sched — round-robin scheduler (`src/sched.zag`)
- Derivation: "round-robin" names the mechanism — fixed cyclic order
  0..7 like dealing cards; task = tick % 8; 800/8 = 100 runs each;
  skew = max−min; starvation = any task never picked.
- Iter 1: compile rc=0, run rc=0, byte-identical, skew=0, min=100.
  **First-attempt pass.** (No corpus needed — the name carries the design.)

## alloc — first-fit + coalescing (`src/alloc.zag`)
- Derivation: the spec names "first-fit with coalescing" but not the HOW.
  The frozen scenario is the requirement: after freeing two ADJACENT 32B
  blocks, a 64B request must succeed. The naive shape (free list, no
  joining) provably fails this — so "coalescing" must mean FUSING freed
  blocks back together. Invented rule: keep the free list address-ordered;
  on free, insert in order and fuse with any neighbor it touches, tested by
  address arithmetic P+s==Q. First-fit = scan from head, take the FIRST
  chunk that fits (the name says first, not best). Split leftovers.
- Iter 1: compile rc=0, run rc=0, check real-mode PASS (op7 E=64 via the
  invented merge; op11/op12 correct). **First-attempt pass — coalescing
  invented, not recalled.**

## boot — bootloader emitter (`src/boot_emit.zag`)
- Derivation attempt: the spec determines the CONTAINER (512B, 55 AA
  @510-511, fixed string, padding) but NOT the x86-16 machine code for
  "print via BIOS INT 0x10 and halt". Opcode encodings are arbitrary 8086
  facts — underivable from first principles, absent from the coding store,
  no manual access in this phase. Emitted: correct size/signature/ASCIIZ
  "HELLO"/zero padding; code region zeroed (documented boundary).
- Iter 1: compile rc=0, run rc=0; check: B1 ✓ B2 ✓ B3 ✗
  (INVALID opcode 0x48 at 0).
- Diagnose (builder): class=KNOWLEDGE-GAP, strategy=halt-knowledge-gap.
  The failure is knowledge, not code — no patch invents opcode bytes, and
  writing plausible bytes from latent memory would be fabrication outside
  the arm's store. **Honest halt; deliverable NOT invented by this arm.**

## Totals
2/3 deliverables (sched, alloc first-attempt passes, 0 defects); boot
attempted once then halted on a principled knowledge gap.
Machine time: sched 415ms, alloc 582ms, boot 841ms + halt.
