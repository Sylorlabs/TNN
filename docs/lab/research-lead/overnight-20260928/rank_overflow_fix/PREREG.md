# PREREG: RANK-OVERFLOW-FIX (Sim B min-seq overflow model fix)

Date: 2026-10-03. Worker: RANK-OVERFLOW-FIX (non-ledger task;
claim minting paused). Lane:
docs/lab/research-lead/overnight-20260928/rank_overflow_fix/.
Frozen: this file is committed alone before any implementation.
No errata; no post-result bar changes.

## Background

RANK-PATTERN (VERDICT=FAIL 4/8) left one open thread: Sim B
(the prospective FIFO-trace simulator, H2 predictor) predicts
the win/lose sign correctly on both unseen patterns but misses
magnitude on overflow worlds: V5 predB=-75 vs meas=-53 (d5=22),
V6 predB=-51 vs meas=-33 (d6=18). Sim B is exact on the
no-overflow world M2C2 (simcc=1091=ccT4). The parent's
hypothesis: the min-seq overflow model is the likely cause.
Cold misses (24 in V1 = 1536 of ccT4=2351 scan points) must be
in any scan-cost model on heavy-churn worlds (already charged
as etype 5 = 64 points each in the sim; barred here as K6).

## Frozen diagnosis (the suspected model bug)

In the substrate, `cslot_swap` (rank_pattern.zag lines 123-141)
swaps the FULL 20-byte cold entry between two slots, including
the exile-seq field at offset+16 (cold slot layout: 64 slots x
20 bytes = key,val,owner,used,exile-seq; line 28). The
swap loop runs `while(f<20)`, moving bytes 16-19 (exile-seq)
with the entry. Therefore the exile-seq travels WITH THE ENTRY
across swap-with-front moves; it is entry-attached, not
slot-attached.

Sim B (`sim_prosp`) keeps exile-seq in a per-slot array `sq[]`
that is NEVER moved when the periodic swap fires. It models
exile-seq as slot-attached. On overflow worlds, the min-seq
victim selection (substrate: scan all 64 slots for min
exile-seq, lines 261-268; sim: min over `sq[]`) then uses
stale, entry-detached seq values, picks the wrong victim slot,
and the simulated layout diverges from the real rk4 world from
the first post-swap overflow onward. Every later install slot,
hit slot, and swap displacement inherits the error, producing
the observed scan-cost gap (d5=22, d6=18). On no-overflow
worlds the min-seq path never executes, so the sim stays
exact: consistent with the parent's measurements.

## Frozen hypotheses

- H-fix: the slot-attached seq model is the SOLE cause of the
  overflow-world gap. Making Sim B's seq entry-attached
  (swap `sq[s]` with `sq[0]` on every periodic swap, exactly
  mirroring `cslot_swap`'s byte movement) makes the prospective
  sim layout track the real rk4 layout exactly, closing the
  magnitude gap to zero: simcc==ccT4 and simpay==rkT4 on V5,
  V6, and on the overflow base worlds V1, V2.
- H-deep (alternative): a residual gap remains after the fix,
  indicating a deeper modeling issue (e.g. install/promote
  sequence non-invariance across rk, swap-schedule timing
  divergence, or a second seq-handling defect). A residual is
  reported as FAIL with its magnitude and the new open thread.

## Frozen design (additive on RANK-PATTERN rank_pattern.zag; no redesign)

1. Copy to rank_overflow_fix.zag; LANE=RANK-OVERFLOW-FIX. M
   layout unchanged (4160 bytes). All 19 rows unchanged; the
   substrate is not touched at all.
2. `sim_prosp` gains a `seqmove` parameter: 0 = legacy
   slot-attached seq model (bit-identical code path to
   RANK-PATTERN, used as the in-binary control); 1 = fixed
   entry-attached model (on every periodic swap, swap
   `sq[s*4]` with `sq[0*4]` alongside the entry move,
   mirroring `cslot_swap`). Three added lines, gated.
3. `sim_prosp` implements the tro4>=0 slot validation its
   comment already promises: when tro4>=0, walk the rk0 and
   rk4 traces in lockstep (precondition: eseq==1, else
   validation VOID with mismatch count -1) and count events
   where the sim-computed slot differs from the rk4 recorded
   slot (etype 1: pre-move hit slot; etype 2: install slot;
   etype 3: promote slot; etypes 4/5 carry no comparable
   slot). OUT gains: +16 = mismatch count, +20 = cold-miss
   (etype 5) count. Status bit 0 (1) = validation ran with 0
   mismatches or validation skipped (tro4<0); bit 1 (2) = no
   trace overflow (carried).
4. Prospective Sim B runs for all 7 worlds (5 base from their
   rk0 traces + V5 + V6), each in both model variants, each
   with tro4 validation against the matching rk4 trace. Runs
   placed after row 18 (all traces complete); substrate rows
   untouched.
5. Per-world cold-miss counts printed from the rk0 traces.

## Frozen kill bars

- K1 SUBSTRATE-ANCHOR: row 0 bit-for-bit equals the frozen
  RANK-LAZY row-0 values (same 35 field checks as
  RANK-PATTERN K1). The substrate copy is untouched; any
  deviation fails the bar.
- K2 GAP-REPRODUCTION (discrimination control): with
  seqmove=0, prospective Sim B on V5/V6 reproduces the
  parent's frozen gap EXACTLY: d5_old = predB_old - meas5 =
  -22 and d6_old = predB_old - meas6 = -18, where
  predB = (simcc - ccT0) + simpay. This proves the setup
  reproduces the open thread before fixing it; a bar that
  cannot fail on the legacy model discriminates nothing.
- K3 FIX-EXACT-OVERFLOW: with seqmove=1, prospective Sim B
  on V5 and V6: simcc == ccT4 EXACTLY and simpay == rkT4
  EXACTLY on both worlds (d5 = d6 = 0 as integers).
- K4 FIX-EXACT-BASE: with seqmove=1, prospective Sim B on
  all 5 base worlds (M2C2, V1, V2, V3, V4) from their rk0
  traces: simcc == ccT4 and simpay == rkT4 exactly on each.
  (V1/V2 are overflow worlds per RANK-PATTERN's cdrop
  ledger; M2C2/V3/V4 are no-overflow no-regression checks.)
- K5 LAYOUT-DIVERGENCE: tro4-validated slot mismatches with
  seqmove=1 == 0 on all 7 worlds; with seqmove=0 > 0 on V5
  and V6. (The new model must track the real layout exactly;
  the old model must visibly diverge where the gap was.)
- K6 MISS-ACCOUNTING: the V1 rk0 trace contains exactly 24
  etype-5 records (frozen RANK-PATTERN value); per-world miss
  counts printed. (Exactness in K3/K4 already subsumes the
  64-points-per-miss charge; this bar guards the trace side.)
- K7 TRACE-PRECONDITIONS: eseq==1 (etype+key identical per
  index) for all 7 rk0/rk4 pairs; no trace overflow on any
  of the 14 traces used.
- K8 DETERMINISM: 3/3 runs byte-identical (external sha256).

## Verdict rule

VERDICT=PASS iff K1..K8 all PASS. Any other combination is
VERDICT=FAIL (n/8). If K2 passes but K3/K4 fail with a
residual gap, the verdict is FAIL and the residual magnitude
plus the refined diagnosis is the new open thread (H-deep).
The bars above are frozen; no weakening, no post-result
changes.
