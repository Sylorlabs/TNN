# PRIOR-ART CORPUS — OS pieces (frozen 2026-09-22)

**Status:** FROZEN. Installed as ordinary studied knowledge for ARM INFORMED
only, via teach with audit entries. ARM FROM-SCRATCH never sees this file.
**Rule:** descriptions of how humans have built things of the target class
(algorithms, idioms, example snippets) — NEVER full solutions to the frozen
verification scenarios. Each section ends with an explicit WITHHELD note.

---

## OS-BOOT — how humans build bootloaders

**MBR layout (the contract with the BIOS).** A bootable disk's first sector
is 512 bytes. The BIOS loads it to physical address 0x7C00 and jumps to it
with the CPU in 16-bit real mode. Bytes 510–511 must be the signature
0x55 0xAA — without it the BIOS does not treat the disk as bootable. Bytes
0–509 hold code and data; whatever is not code is conventionally zero-padded.
The emitter is an ordinary host program that writes these 512 bytes to a
file; the FILE is what would boot.

**Real-mode addressing.** Physical address = segment×16 + offset. Because the
sector lands at 0x7C00 = 0x07C0:0x0000, a common setup is DS=0x07C0 so that
plain offsets are sector-relative (offset 0x0010 reads physical 0x7C10).
The standard two-instruction idiom: load 0x07C0 into AX, then AX into DS.

**BIOS teletype output.** `INT 0x10` with AH=0x0E prints the character in AL
at the cursor and advances it (teletype mode). BH selects the display page
(0 for the usual case). So printing one character is: AH ← 0x0E, AL ← char,
`INT 0x10`.

**String-print loop (the classic shape).** Keep a pointer (SI) at a
zero-terminated message. Repeat: load the byte at SI and advance SI
(`lodsb` does both); if the byte is zero, stop; otherwise set AH=0x0E and
`INT 0x10`. The stop test is idiomatically `test al,al` + `jz done`.

**Halt.** After printing, the CPU must not run off into the padding. The
classic halt is `cli` (no interrupts) then `hlt` (stop until interrupt)
then `jmp $` (jump to self, so even a stray interrupt returns to the halt).
Without the jump, an interrupt would wake the CPU past the `hlt` into
whatever bytes follow.

**Example snippets (idioms, not a program):**
- `mov ah, 0x0E` / `int 0x10` — print the char in AL.
- `test al, al` / `jz done` — stop at the string terminator.
- `cli` / `hlt` — halt the CPU.

**WITHHELD:** the complete assembled stub byte sequence; exact instruction
offsets and jump displacements; the message placement and padding
computation. The corpus does not contain a buildable 512-byte image.

---

## OS-SCHED — how humans build round-robin schedulers

**The idea.** N tasks share one CPU. Each task runs for one fixed quantum
(a "tick"), then the scheduler picks the next task in a fixed cyclic order:
0,1,2,…,N−1,0,1,2,…. No priorities, no preemption inside a quantum — the
order itself is the policy. A schedule clock (tick counter) drives it;
`task = tick mod N` is the textbook selection.

**Task state.** Each task has a small control block (id, run count, saved
state in a real kernel). The scheduler keeps these in an array and walks it
cyclically. Per-task run counts are the accounting that proves fairness.

**Fairness measures.** Over a window of T ticks with N tasks, perfect
fairness is T/N runs each. *Skew* = max run-count − min run-count across
tasks (0 is perfect; small skew is the bar). *Starvation* = some task never
selected within a bounded window — the liveness bar every scheduler must
clear. A correct round-robin over a whole number of cycles has skew 0.

**Idioms:** `next = (current + 1) % n`; a `schedule()` function owning the
selection; tick loop calling schedule-then-run.

**WITHHELD:** any complete scheduler program; the frozen 8-task/800-tick
simulation and its expected output.

---

## OS-ALLOC — how humans build first-fit allocators with coalescing

**Free list.** The allocator manages a fixed pool. Free regions are tracked
as a linked list; each free block starts with a small header holding its
size and the next-block link (offsets, not pointers, in simple designs).
One head pointer (or offset) anchors the list.

**First-fit.** To satisfy a request of n bytes, scan the free list from the
head and take the FIRST block big enough — not the best, the first. If the
block is much bigger than n, split it: carve n (+ header) off the front and
return the remainder to the free list. If no block fits, report failure.
First-fit is fast and simple; its weakness is fragmentation.

**Coalescing (the anti-fragmentation move).** When a block is freed, check
its physical neighbors: if the block immediately before or after it in
memory is also free, merge them into one bigger free block (sizes add, one
header absorbed). The adjacency test is pure address arithmetic: block P
with size s is adjacent to block Q iff P + s == Q. Keeping the free list
sorted by address makes the neighbors easy to find — the predecessor and
successor in the list are the only candidates. Without coalescing, freeing
A then B leaves two small blocks that can never jointly satisfy one big
request even though the memory is all free; with coalescing they become one
block again. Coalescing runs on free (not on alloc), so the alloc path stays
a plain first-fit scan.

**Idioms:** header {size, next}; `if (prev + prev.size == blk) merge`;
split only if the remainder still fits a header plus a minimal payload;
failure = null/-1, never a partial block.

**WITHHELD:** any complete alloc/free implementation; the frozen op
sequence and any code shaped to it.
