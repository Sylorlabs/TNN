# PREREG Amendment 2: world-change implementation (2026-10-02)

Status: pre-implementation (no implementation committed yet; the
trial run below used uncommitted scratch sources only). This amendment
changes only how the driver implements the world change, not the
operator, not the frozen kill bars K1-K7, and not the expected
answers.

## What the trial run revealed

The 2026-10-02 trial (R3-PASS; R1/R2/R4-FAIL) exposed two substrate
behaviors that confound the world-change signal. Both are pre-existing
substrate mechanics, not bugs in the revision operator (R2 showed
REVISE-STALE firing correctly).

### Finding 1: alloc_node recycles dead node ids

`alloc_node` (cc_base.zag) reuses the lowest dead node id. A
kill-then-teach world change therefore places the new fact in the OLD
fact's slot. The adaptation's cell-to-fact type-1 edge then silently
reads the new content: in R1, killing node 39 = (14,1,15) and teaching
(14,3,12) recycled node 39, so X' (whose 4th cell points at node 39)
was "fixed" by the substrate instead of broken. Compose then answered
through X' directly and the revision operator never fired. Proven by
scratch probe: cc_relseq(X') = 4 with 4th relation 3 after the
kill-then-teach change.

Fix: world changes that must present a clean break use
teach-then-kill. The new fact lands in a fresh slot; the old slot
stays dead; the adaptation's licensing edge still points at the dead
fact, so staleness is genuine and only the learner's revision can
repair it.

### Finding 2: redundant answer paths via cached shortcuts

The substrate answers through several redundant paths (rebind,
compose, adapt, chain-trial, sum-trial, bootstrap, activate-memory).
The phase-1 shortcut (11,71,14) and phase-2 shortcut (11,72,15) are
cached consequences of the pre-change regularity. After the world
change they are stale, but the chain-trial ([11,14,15]) and the
sum-trial (singleton {15}) still answer from them:

- R2 (dead end, expects -2): sum-trial answered 15 via (11,72,15).
- R4 (contract break, expects -2): sum-trial answered 15 via
  (11,72,15); chain-trial would also answer 15 via
  (11,71,14) + (14,1,15).

These paths do not touch the adaptation, but they confound the
adaptation-retraction signal (the kill bar wants -2 so the test
isolates what the ADAPTATION mechanism does).

Fix: R2 and R4 world changes withdraw the stale cached shortcuts
along with the world fact. Rationale: the shortcuts are cached
answers derived from the withdrawn/broken regularity; withdrawing
them is part of withdrawing the regularity. The experiment tests the
adaptation mechanism, not cache invalidation.

## Revised world changes (driver only)

- R1 PARAM-REVISE: teach (14,3,12) FIRST (fresh slot), THEN kill
  (14,1,15). Node 39 stays dead. X' is genuinely stale; only
  adapt_revise can produce X''.
- R2 RETRACT: kill (14,1,15) AND kill the phase-2 shortcut
  (11,72,15). Expect -2 with X' retired and zero live adapted MAPs.
- R4 CONTRACT-BREAK: teach (12,1,93), kill (12,1,13), kill the
  phase-1 shortcut (11,71,14), kill the phase-2 shortcut (11,72,15).
  (14,1,15) stays live but unreachable from 11. Expect -2 with X'
  still live, one live adapted MAP, type-16 edge count unchanged.
  The learner must not touch the adaptation when the break is in
  the contract.

## Unchanged

- revise_patch.zag operator: staleness detection untouched. One
  ordering fix: the retirement (field 36 = 0) now happens AFTER
  rev_extend_src, because retiring first let the new MAP's own
  construction recycle the retired slot. The type-16 revision edge
  is written during construction while the old MAP is still live,
  then the old MAP retires; edges persist.
- Kill bars K1-K7, queries, expected answers, determinism bar.
- R3 (no-change control): no world change, unaffected.
- Commit order: this amendment is committed alone before the
  implementation, per the prereg commit-order self-check.

## Finding 3 (added): retired MAP slots are recycled

A retired MAP node (field 36 = 0) is recycled by later
allocations (literals, cells, facts). "Retired" is therefore
observably "no longer a live MAP (tag 20 with field 36 = 1)",
not "field 36 = 0 forever". The driver checks MAP liveness
(tag-gated). The type-16 provenance edges persist regardless of
slot reuse, so the revision chain remains readable.
