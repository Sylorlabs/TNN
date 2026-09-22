# TASK 3 — Frozen verification spec (frozen 2026-09-22, harness-crew freeze)

**Status:** FROZEN. Public to both arms (it is the test battery, like Task 2's
oracle formulas). Any change needs a dated amendment with Micah's re-approval.
**Scope note:** a full OS is OUT OF SCOPE. Each deliverable is a pure-Zag
program; where the deliverable is a binary image, the Zag program EMITS it.
The scheduler and allocator are hosted simulations of the mechanism logic
(a real preemptive kernel scheduler / bare-metal allocator would be a full
OS — explicitly out of scope).

## Common law (all three deliverables, both arms)

- Pure Zag, pinned toolchain `znc_linux_x86_64_abed8aa1`, zero RNG in any
  decision path, deterministic. Final artifacts re-run 5x: stdout and all
  emitted files byte-identical across reps.
- Nothing hardcoded as knowledge: the programs must implement the mechanism,
  not a trace of expected outputs. (Enforced by builder discipline + audit;
  the checkers additionally validate semantic invariants — bounds,
  no-overlap, ordering — on every op, so a hardcoded trace is as much work
  as the mechanism.)
- Loop budget: 6 iterations per deliverable per arm (gen + ≤5 revises).
  First-attempt pass, iterations-to-working, time, defects all recorded.

## V1 — Bootloader emitter

Program: `boot_emit.zag`. Run: `boot_emit <outpath>` (argv[1]; default
`boot.bin` when absent). Must exit rc=0.

**Verification ladder** (`harness/check_boot.py`), run in order:

| Rung | Check |
|---|---|
| B1 size | file exists and is exactly 512 bytes |
| B2 signature | bytes[510] == 0x55, bytes[511] == 0xAA |
| B3 decode | bytes [0, code_end) decode fully under the frozen 16-bit opcode table below; code_end = address just past the `jmp` closing the halt loop (pattern `cli; hlt; jmp rel8` with target == the `cli` address). No unknown opcodes before code_end. |
| B4 print semantics | decoded code contains: `mov ax,0x07C0` + `mov ds,ax`; `mov si,imm16` with imm16 == code_end; a backward `jmp` (the print loop); inside the loop body, `mov ah,0x0E` before `int 0x10` in decode order; a forward conditional jump (`jz`/`jnz`) whose target lies in the halt region |
| B5 layout | bytes [code_end, 510): printable ASCII (0x20–0x7E), then one 0x00 terminator, then all 0x00 through byte 509 |
| B6 boot | ATTEMPTED: boot the image in qemu-system-x86_64 — see outcome note below |

**Frozen 16-bit opcode table** (decoder accepts exactly these; anything else
in [0, code_end) is INVALID): `B8..BF` mov r16,imm16 (3B); `8E D8`
mov ds,ax (2B); `BE` mov si,imm16 (3B); `AC` lodsb (1B); `84 C0`
test al,al (2B); `74` jz rel8 (2B); `75` jnz rel8 (2B); `B4` mov ah,imm8
(2B); `CD` int imm8 (2B); `EB` jmp rel8 (2B); `FA` cli (1B); `F4` hlt (1B).

**Accepted envelope (documented limitation):** the checker accepts the
classic teletype-loop shape (DS=0x07C0, SI→message, AH=0x0E loop, CLI/HLT/
JMP-$ halt, message immediately after code). A semantically valid stub with
a different shape (e.g. ES-based, `mov al,[si]`) would be rejected — that is
a checker limitation, recorded here, not a verdict on such a stub.

**B6 outcome (2026-09-22):** qemu-system-x86_64 is NOT installed on the lab
VM (only qemu-aarch64-static exists in the toolchain dir); `apt install
qemu-system-x86` fails ("Unable to locate package qemu-system-x86", no
sudo). ndisasm is not installed. B6 NOT ACHIEVED — the achieved verification
is rungs B1–B5 (size, signature, full disassembly, print semantics, layout).
Verdict PASS requires B1–B5.

## V2 — Scheduler

Program: `sched.zag`. Run: `sched` (no args). Must exit rc=0. The program
simulates 800 ticks of round-robin scheduling over 8 tasks (task id =
cyclic selection 0..7; per-task run accounting through a scheduler
structure — the builder's design choice).

**Frozen stdout contract** (byte-compared):

```
task 0: 100
task 1: 100
task 2: 100
task 3: 100
task 4: 100
task 5: 100
task 6: 100
task 7: 100
SEQ 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7
```

(`SEQ` = the first 16 scheduled task ids, proving cyclic order; the 8
counts prove fairness over 800 ticks.)

**Bars** (`harness/check_sched.py`): stdout byte-identical to the frozen
text above; skew = max(counts) − min(counts) ≤ 1; no starvation =
min(counts) ≥ 1. PASS requires all three.

## V3 — Allocator

Programs: `alloc.zag` (deliverable: first-fit WITH coalescing),
`harness/naive_alloc.zag` (harness control: first-fit WITHOUT coalescing —
identical code except free() never merges; the diff is the coalescing
logic). Run: no args. Must exit rc=0. The program manages a 256-byte pool
and executes the frozen op sequence below, printing one line per op.

**Frozen op sequence** (public; sizes in bytes):

```
1  ALLOC A 32
2  ALLOC B 32
3  ALLOC C 32
4  ALLOC D0 64    # occupies the tail so the leftover free block (56 B)
                 # can never satisfy the discriminating request
5  FREE A
6  FREE B
7  ALLOC E 64     # DISCRIMINATING OP: A,B adjacent+free; coalescing merges
                 # them into 72 payload bytes, so E fits. Without merging,
                 # the largest free payload block is 56 < 64 -> first-fit fails.
8  FREE C
9  FREE D0
10 FREE E
11 ALLOC F 200    # whole-pool coalescing check (needs full merge)
12 ALLOC G 300    # must FAIL honestly (larger than the pool)
```

**Frozen stdout contract:** per op, `ALLOC <id> <off>` where `<off>` is the
payload offset (≥0) or `-1` on failure; `FREE <id> OK`; final line `DONE`.

**Bars** (`harness/check_alloc.py --mode real|naive`):
- every reported `off ≥ 0` lies in the payload pool [0, 256) and the block
  [off, off+size) does not overlap any other live block (checker tracks
  liveness from the op log; sizes from the frozen sequence above);
- every `FREE <id>` names a live block;
- `--mode real`: op 7 `ALLOC E` off ≥ 0; op 12 `ALLOC G` off == −1; all other
  allocs off ≥ 0. (Naive-mode: ops 1–6 valid; op 7 off == −1 — this is the
  proof the scenario discriminates. Ops 8+ are executed but unchecked in
  naive mode; rc must still be 0.)
- PASS (real) requires all of the above.

**Why the scenario discriminates (paper argument, harness-crew):** with an
8-byte header, after ops 1–4 the free tail is 56 bytes. Ops 5–6 free A and B
(40 bytes each, adjacent). Merged: 80 − 8 = 72 ≥ 64 payload bytes → E fits.
Unmerged: the largest free payload block anywhere is 56 < 64 → first-fit
fails. Op 11 needs the full 256 payload bytes merged (200 ≤ 256 ✓). Op 12:
300 > 256 → both must fail.

## Determinism check (all deliverables)

`harness/rep5.sh <bindir>`: runs each final binary 5x, sha256 of
(stdout + emitted files); all 5 digests must match. Binaries themselves are
rebuilt once and compared (informational — znc output reproducibility is
not a scored bar).
