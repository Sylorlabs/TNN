# CRASH_REPRO.md - INDEX lane, wave-20261002-0221pdt (Part B, crash)

Governing bar: PREREG_INDEX_REPRO.md B1 (frozen).

## The defect

Red-team finding (C203, commit 98f68d6a3, ADV-IDX-CORRUPT case C2):
a cycle in the plen-bucket list crashes `rebind_try_idx` with
`panic: slice index out of bounds`. Root cause in
`scaling_index/si_patch.zag` lines 156-170:

  let cand:[]u8=z_alloc(4096);   // 4096 bytes = 512 entries x 8 bytes
  ...
      while(m>=0 && nc<1024){    // bound allows 1024 iterations
        hs(W,56,hg(W,56)+1);
        set32(cand,nc*8,m); set32(cand,nc*8+4,q);  // 8 bytes/entry
        nc=nc+1;
        m=ng(W,m,12);            // no cycle check, no bounds check
      }

512 entries fit; the loop allows 1024. A cyclic bucket list (the red
team built it with one store: bucket head's field-12 pointing to
itself) drives nc past 512, and the write at byte offset 4096
panics. Three compounding absences: no cycle detection, no liveness
or type check on members, and a loop bound that does not match the
buffer capacity.

Knowledge vs architecture assessment: this is a DATA-SHAPE gap with
an architectural edge, not a substrate flaw. The substrate (intrusive
singly-linked lists, fixed buffers, bounds-checked slices) behaved
exactly as specified: the panic is the bounds checker doing its job.
The defect is that the index layer trusted the shape of
learner-reachable state (the bucket list) without validating it.
Learner state is adversary-reachable in this architecture (eviction
and slot reuse can already leave stale ids in buckets; the red team
simulated exactly that), so any trusted-shape assumption over it is
a bug, not a violated precondition. The fix therefore has two parts:
make the consumer unable to panic on any shape (hardened walk), and
make production use conditional on shape validity (validation gate).

## Minimal reproducer

`work/crash_repro.zag` (+ `work/prelude.zag` base helpers, assembled
to `work/crash_repro_full.zag`): replicates the vulnerable pattern
with the exact constants (4096-byte buffer, nc<1024 bound, 8-byte
writes) over a minimal 2-node store with a self-loop (the red-team
C2 shape). Pure Zag, safebin, pinned znc.

Result (frozen B1 expectation: panic, nonzero exit, `nc=` never
prints):
  CRASH-REPRO-VULN-START
  collecting from cyclic bucket (head=0, 0->0)...
  panic: slice index out of bounds
  run-exit=1

Crash reproduced. The `nc=` line never printed: the panic fired
inside the collection loop, as specified.

## Fixed pattern

`work/crash_fixed.zag` (assembled to `work/crash_fixed_full.zag`):
the same program with the hardened walk: OOB-safe single step
(out-of-range next = list end), Floyd tortoise-and-hare cycle
detection, writes bounded by the true buffer capacity (512), only
live members collected.

Result (frozen B2 expectation: exit 0, each cyclic member collected
exactly once, no panic on any shape):
  T1-selfloop   PASS got=100001   (1 member, CYCLE-DETECTED)
  T2-3cycle     PASS got=100003   (3 members, CYCLE-DETECTED)
  T3-oobnext    PASS got=1        (OOB next treated as list end)
  T4-deadmem    PASS got=1        (dead member skipped)
  T5-healthy    PASS got=3        (healthy list unchanged)
  T6-oobhead    PASS got=0        (OOB head collects nothing)
  CRASH-FIXED-FAILURES=0, run-exit=0

B1 HOLD (crash reproduces pre-fix). B2 HOLD (fixed pattern passes
all six shapes).

## Red-team self-review (crash reproducer)

- The minimal reproducer abstracts the node store; it proves the
  MECHANISM (buffer/bound mismatch + unbounded cyclic walk), not the
  full-system path. The full-system path was already proven 3/3 by
  the red team's own adv_idx_corrupt run (panic at C2-CYCLE, node
  67). The minimal version is the regression test; the red-team run
  is the system-level evidence.
- The fixed pattern collects each cyclic member once rather than
  rejecting the list. A purist could argue a cyclic list should
  yield zero candidates. The production gate (VALIDATION_GATE.md)
  takes the strict position (REJECT the whole index); the walk takes
  the non-panicking position (never crash even if the gate is
  bypassed). Both properties hold simultaneously.
- The reproducer does not cover the C3 shape (OOB next pointer)
  panicking inside `ng` on the real workspace; T3 covers the fixed
  walk's OOB handling, and the gate test G4 covers strict rejection.
  On the vulnerable code, C3's exact failure mode (panic vs garbage
  reads) was never observed because C2 panicked first; the fix
  removes the question rather than answering it.
- `set32`/`get32` bounds behavior is the panic source; the fix never
  relies on catching the panic, only on never indexing out of
  bounds. There is no exception-handling construct to misuse here.
