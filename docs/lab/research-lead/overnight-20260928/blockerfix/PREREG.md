# PREREG -- BLOCKERFIX: B6 (interpreter scratch bound) and B1 (namespace collision)

Lane: `lane/blockerfix`. Base: `87a822426`.
Frozen BEFORE any implementation and BEFORE any run under it.
Claim IDs reserved: **C570-C599**. Nothing outside that block is minted.

Pure Zag for all computation (brief section 0). Every run through
`tools/tnnwatch.sh` with the limit fixed HERE.

---

## 0. WHAT IS AND IS NOT BEING REOPENED

**B6 engine fix is NOT the one-liner.** The ledger (C398/C405) documents
`z_alloc(64)` -> `z_alloc(128)` as "the fix". This prereg treats 128 as an
UNVALIDATED HYPOTHESIS, because charter 162 forbids calling a capacity limit an
intelligence limitation when it is an implementation artefact, and charter 37
forbids magic numbers. The actual question is: **what is the true bound, is it
derivable, and is 128 principled or merely larger?**

**B1 engine fix is ALREADY DONE by two lanes and is NOT redone.**
`lane/scalingp8` (310a8a2d6) and `lane/eviction` (8f3a289fc, ec0f54aca) both
installed the sign-disjoint encoding. This lane verifies, does not reimplement.

---

## 1. B6 -- THE INTERPRETER SCRATCH BOUND

### 1.1 The measured artifact

`hcontlife5-invent/src/invent.zag::learner_interp` runs a length-`qlen`
program of 5 instruction codes on a value stack in `scr`:

| code | name | effect on `sp` |
|---|---|---|
| 0 | fit | `sp += 1` |
| 1 | exm | `sp += 0` |
| 2 | loo3 | `sp += 3` |
| 3 | med | `sp := 1` |
| 4 | avg | `sp := 1` |

Writes are `set32(scr, sp*4, v)`, so the highest byte offset touched is
`4*(max_sp)` where `max_sp` is the largest value `sp` reaches.

### 1.2 THE DERIVATION (frozen here, BEFORE measuring)

The largest `sp` reachable in a length-`L` program is obtained by maximising
the per-step increment. `loo3` contributes +3, `fit` +1, `exm` 0, and `med`/`avg`
both *reset* sp to 1 (they are never maximisers). So:

```
max_sp(L) = 3*(L-1) + 1 = 3L - 2      achieved by [loo3 x (L-1), fit]
```

where the trailing `fit` is required because `valid_prog` forces the last
instruction to be 0/3/4 (a producer), and the final `fit` contributes the +1.

**Frozen predicted bound: `scr_bytes_required(L) = 4*(3L-2) + 4 = 12L - 4`.**

(The `+4` is the terminal i32 word; `set32` at offset `4*(3L-3)` writes bytes
`12L-12 .. 12L-9`, and the final `get32(scr,(sp-1)*4)` reads `12L-8..12L-5`, so
the buffer must be at least `12L-4` bytes to be in-bounds with no slack.)

**Cross-check against the ledger's measured numbers, frozen as a KILL BAR:**

| L | predicted `12L-4` | ledger observation |
|---|---|---|
| 6 | 68 | "max write offset was 60 < 64" -- consistent |
| 7 | 80 | crashing program writes offset 64 of a 64-byte buffer |

**K1 (derivation).** An exhaustive Zag sweep over ALL `5^L` digit strings for
L=1..10, executing the real `learner_interp` against a **guarded** scratch,
records the true `max_sp(L)`. Kill bar: observed `max_sp(L) == 3L-2` for every
L in 1..10. Any L where the observed maximum is **below** `3L-2` is REPORTED as
such and the prediction is marked WRONG -- I am not allowed to lower the bar
after seeing it. Any L where it is **above** `3L-2` means my model of the
instruction set is incomplete and that is also a FAIL of the derivation.

**K2 (the frozen claim is FALSE as a sufficiency statement).** The documented
fix is `z_alloc(128)`. From the frozen derivation, 128 bytes covers
`12L-4 <= 128`, i.e. **L <= 11**. Kill bar: 128 is INSUFFICIENT at L=12
(`12*12-4 = 140 > 128`). This is the headline prediction and it is frozen:
**the one-line fix does not generalise; 128 is still a magic number.**

**K3 (bound is a function of L, not a constant).** The principled allocation
is `scr = z_alloc(12*L - 4)` (or `12*L` for slack), a function of program
length. This is not a new magic number because it is DERIVED from the
instruction set's maximum stack effect, and it is verifiable: `K4` asserts the
allocation is never below the measured `max_sp` and never above it by more than
one cell. Charter 37 satisfied by derivation, not by a larger literal.

**K4 (the invariant actually holds, at every L).** For L=1..10, run the
guarded interpreter on the worst-case program `[loo3 x (L-1), fit]` with a
buffer of exactly `12L-4` bytes. Kill bar: **zero** out-of-bounds accesses, and
the returned value is identical to the same program run with a 4096-byte
buffer. Any divergence is a FAIL.

**K5 (the crash reproduces).** Build the UNMODIFIED `z_alloc(64)` interpreter
and run the ledger's crashing program `[fit,loo3,loo3,loo3,loo3,loo3,fit]`
(length 7). Kill bar: reproduces the `panic: slice index out of bounds`. If it
does NOT crash, the ledger's root-cause claim is wrong and that is reported.

**K6 (minimum sufficient constant, honestly stated).** The smallest single
constant that is safe for ALL L<=11 is 128 bytes; for L<=10 it is 116. Reported
as: *the constant 128 is sufficient exactly up to L=11 and is therefore a
bounded-resource statement, not a fix.* Kill bar: a buffer of `12L-4` bytes is
sufficient at every L tested, and no smaller constant derived from the same
formula is.

**K7 (COST -- does a bigger scratch slow execution).** Wall and CPU for the
same workload at scr = 64 / 128 / 512 / 4096 bytes, 5 repetitions each,
serialised, reported as a table. Preregistered expectation, stated before
measurement: the interpreter touches only `0..4*max_sp` regardless of buffer
size, so a larger allocation should cost only the `z_alloc` zero-fill
(O(bytes), once) and should NOT change per-program cost. Kill bar for the
TRADE-OFF being real: if per-program cost rises by more than 5% from 64 to 4096
bytes, that is a measured cost and must be recorded as such. If it does not,
the honest statement is "larger scratch is free here; the ceiling is not a
speed ceiling".

---

## 2. B1 -- NAMESPACE COLLISION: VERIFY, THEN MAKE IT AN INVARIANT

### 2.1 Verify both lanes, independently

**K8 (agreement).** Extract `res_op`, `fr_get`, `fr_set` and every operand
write site from `lane/scalingp8` (310a8a2d6) and `lane/eviction` (ec0f54aca)
and compare the SEMANTICS. Kill bar: both encode node ref as `op>=0` and frame
ref as `op<0` with slot `(-op)-1`. **If they disagree, this lane says so
loudly and stops claiming closure.**

**K9 (the frozen C267 build is the accident).** In
`scaling_5000/s5000_full.zag` the encoding is `op>=100000 -> frame slot
op-100000` with `NN()=65536`. Kill bar: the collision condition is
`max_live_node_id >= FRAME_BASE`. With `NN=65536` and `FRAME_BASE=100000` the
condition is **unreachable** (`max node id = 65535 < 100000`), confirming the
lane/eviction finding that 5k was correct BY ACCIDENT of two unrelated
constants. This must be shown, not assumed.

### 2.2 The deliverable: turn the accident into an invariant

**K10 (cross-constant-space proof, by construction).** Under the sign-disjoint
encoding, node ids are non-negative and frame refs are negative. Therefore for
**every** pair `(NN, FRAME_BASE)` -- indeed for every arena size whatsoever --
no integer can be both a node id and a frame reference. `FRAME_BASE` is not
merely large enough; it is **not a parameter of the encoding at all**. The
correctness of the 5k run stops depending on `NN < FRAME_BASE`.

This is a proof obligation, discharged by **exhaustive test over a constant
sweep, not by argument alone** (charter: an invariant that is only argued is
not an invariant):

**K11 (constant-space fuzz).** Sweep `NN` over at least 6 values
(1024, 65536, 131072, 262144, 524288, 1048576) crossed with the legacy
`FRAME_BASE` values (1000, 10000, 100000) and with `FRAME_BASE = 0`, i.e. 24
combinations including the three configurations that are known- or
historically-dangerous. For each combination, inject malformed references of
every shape (negative-as-node, too-large-as-node, non-negative-as-frame,
i32-min-as-frame) at every guard site and require:
  (i) a DEFINED failure sentinel, never a wrong answer;
  (ii) the violation counter increments;
  (iii) the arena canary is intact;
  (iv) a subsequent well-formed query still returns the correct answer.

Kill bar K11a: **zero** collisions across the whole sweep under the
sign-disjoint encoding. Kill bar K11b: the legacy encoding is shown to FAIL the
same sweep (proving the test has teeth and is not vacuous).

Generators reuse `lane/propertyzag`'s malformed-reference generators. If they
cannot be reused directly, the substitution is documented in the report.

### 2.3 The missing verification

**K12 (C267 9-phase byte-identity under the NN=131072 rebuild).**
`lane/eviction` REPORT2 section 8 item 5 states this was **NOT DONE**. This is
the single most important missing measurement, because the queued
`NN=65536 -> 131072` rebuild is exactly what would have destroyed the accident.

Run the full 9-phase battery (`s5000_driver.zag:184-192`: S1000L, S1000I,
S5000L, S5000I, EML, EMI, EMM, FAL, FAI) under the sign-disjoint encoding at
**both** `NN=65536` and `NN=131072`, and compare against canonical
`scaling_5000/s5000_run1.txt` (sha256 `382e913a1ada...`, 64 lines).

Kill bar K12a: the 9-phase battery is **byte-identical to canonical** at both
arena sizes. Any answer difference is a hard FAIL -- correctness beats speed,
and in the no-eviction regime every change is a pure encoding change.

Kill bar K12b: 3/3 byte-identical on each reported run (determinism).

Kill bar K12c: output is non-empty (brief 4.0 -- an empty log is not a result).

**K13 (the accident is destroyed by the rebuild, and the fix survives it).**
Run the LEGACY encoding at `NN=131072` on the same battery. Preregistered
prediction, from the mechanism and before the run: the legacy encoding is
correct at `NN=65536` (node ids stay below 100000) and **BREAKS or changes
behaviour** at `NN=131072`, where node ids may reach 131071 >= FRAME_BASE. If
legacy-at-131072 happens to be byte-identical too, that is reported honestly as
"the accident survived this particular rebuild" and K13 is marked as such --
it does not license calling the legacy encoding safe.

---

## 3. RUN BUDGET AND DISCIPLINE

Shared machine, load observed 11-79. Everything strictly serial, never
parallel, always behind `tnnwatch.sh`.

| run | limit |
|---|---|
| B6 sweep L=1..10 (single binary, one process) | 600 s |
| B6 crash reproducer + fixed build | 120 s each |
| B6 cost table (4 sizes x 5 reps) | 900 s total, serialised |
| B1 constant sweep (24 combos) | 900 s total, serialised |
| B1 9-phase battery NN=65536 and NN=131072 | 900 s each |

No limit is extended after a miss. A timeout is recorded as TIMEOUT.

**Process-fail conditions** (recorded as FAIL, never as results): zero-byte
output; `rc != 0` on a build that should succeed; any forbidden interpreter;
namespace violations != 0 in a run that claims success; canary breach.

**Explicitly NOT claimed.** Nothing here is an L3 claim. Nothing here measures
learning quality. B6 closes a resource bound; B1 closes a namespace. Neither
says anything about whether the learner is intelligent, and no such inference
is licensed (brief section 9).