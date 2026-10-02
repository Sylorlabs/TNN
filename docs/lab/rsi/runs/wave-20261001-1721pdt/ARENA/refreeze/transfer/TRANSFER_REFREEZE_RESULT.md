# TRANSFER REFREEZE RESULT: real frozen TNN-2 binary

Date: 2026-10-01 PDT
Worker: ARENA lane replacement worker, wave-20261001-1721pdt
Prereg: refreeze/transfer/TRANSFER_REFREEZE_PREREG.md (frozen before implementation)
Parent instruction: rerun the transfer protocol against the REAL frozen TNN-2
  binary; BLOCKED rather than simulated substitution; document discrepancies.

## Verdict: INFEASIBLE (BLOCKED on execution, not on binary availability)

The real frozen TNN-2 binary was located and hash-verified. A fresh frozen
prereg porting the transfer protocol to TNN-2's public interface was written.
A pure-Zag harness was implemented and all K5 checks pass. Sealed runs were
attempted, but TNN-2's trial loop hits a combinatorial wall that makes the
protocol uncompletable in feasible time. The simulated-learner 0.3333 is NOT
substituted and retains zero evidential weight for TNN-2. No transfer score
for TNN-2 is reported.

## 1. Binary identity (verified, not the blocker)

- Real frozen TNN-2 binary: docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2_bin
  SHA-256: 6044f91f8fe35e307e1d6f73a4ee73bffb930fa0a16a9c899048a086d0d5f77b
  MATCHES the CORE_FREEZE_TNN2_PREREG.md frozen record (verified by this worker).
- Frozen shim: docs/lab/research-lead/overnight-20260928/core_freeze_tnn2_shim/freeze_shim2_bin
  SHA-256: 9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954
  MATCHES the frozen shim record. Neither binary modified.

## 2. Discrepancy with PREREG_TRANSFER.md (documented per parent instruction)

PREREG_TRANSFER.md defines its learner as a minimal simulated learner
(checklist of four hypothesis forms); its K2 (checklist wipe) and K3
(verbatim-lookup storage control) are mechanics of that simulation and cannot
be literally rerun against TNN-2. Per the parent instruction, the real-binary
requirement governs: TRANSFER_REFREEZE_PREREG.md ports the protocol (same
worlds, same conditions structure T/F/X, same scoring S, same kill-bar intent)
to TNN-2's public OBSERVE/QUERY interface via the frozen shim. The M
(storage) condition was not ported (it tested the simulation's verbatim
failure mode; for TNN-2, verbatim cross-condition retrieval is impossible by
the disjoint-id/disjoint-surface construction, verified structurally).
The X condition was adapted to scrambled-A exposure (the checklist wipe has
no TNN-2 counterpart).

## 3. Harness (pure Zag, K7)

- tnn2_transfer_gen.zag: generates 168 world files (T/F/X conditions, train
  + held-out steps) with the exact world parameters from PREREG_TRANSFER.md;
  runs K5a/K5b/K5c in-run. Pure Zag, pinned znc, deterministic.
- K5a surface_class_disjoint=1; K5b Alaw_reject_on_B=36, Blaw_reject_on_A=36;
  K5c Alaw_reject_on_scrambled=24/24. All PASS.
- run_tnn2_transfer.sh: bash sequences frozen shim invocations only,
  implements the frozen consecutive/held-out criterion protocol.
- tnn2_transfer_score.zag: pure-Zag scorer (K4 determinism + S + kill bars).
- Toolchain: safebin guard re-activated; `which python3` empty; zero python
  invocations; zero em-dash bytes in lane docs.

## 4. Sealed execution attempt and timing evidence

World files verified correct by inspection (event encoding matches prereg
section 4). Shim smoke test passes (TNN-2 returns -2 miss on sequence
queries, as architecturally expected). Full protocol launched (3 runs).

Per-step wall-clock for T_A phase (fresh state, sequential steps):

| Steps | Time per step |
|-------|---------------|
| 0-14 | 28ms - 390ms |
| 15 | 72,646ms |
| 16 | 124,070ms |
| 17+ | not completed (killed; trend superlinear) |

Steps 0-14 complete in under 400ms each. At step 15 the per-query cost jumps
300x to 72s; step 16 takes 124s and the trend is worsening. A single
condition (up to 120 queries across phases) would require many hours; three
runs for K4 determinism are not feasible. The run was killed at T_A step 17
of run 1. No condition completed; no examples-to-criterion measured.

## 5. Root cause (source-verified, not speculative)

TNN-2's t2_trial (tnn2.zag:586) runs on every query miss. Its sum branch
enumerates ALL subsets of the subject's direct values (up to 2^12) and for
each calls t2_asm_sum (tnn2.zag:398), which builds an UNROLLED INC-cell
chain with cell count equal to the SUBSET SUM:

  while(i<total){ let c:i32=t2_inc(W,0); ... i=i+1; }

For sequence values in the tens (e.g., step 15's terms 15..87, subset sums
in the hundreds), each query triggers up to 128 subset trials, each
allocating hundreds of cells via alloc_node on an accumulating workspace.
The cost scales with the VALUES, not just the fact count, and it is
incurred on every miss. Since every sequence query is on a novel seq id,
every query misses, and the trial loop's exhaustive sum search dominates.
This is inherent to the frozen TNN-2 architecture, not to the harness or
encoding; no feasible encoding of the transfer worlds avoids it while
preserving the protocol's values.

## 6. Kill bars

- K1-K3, K5-K6: UNMEASURABLE (no condition completed; INFEASIBLE, not FAIL).
- K4: not established (runs incomplete).
- K7: PASS (pure Zag + bash; toolchain guard).
- K8: PASS by construction (identical B across conditions in the generator).
- Verdict mapping: the prereg defines VOID for K6 failure; here the
  measurement itself is infeasible, so the verdict is INFEASIBLE (a
  stronger statement than VOID: not "TNN-2 did not transfer" but "the
  transfer protocol cannot be executed against TNN-2").

## 7. Interpretation (no overclaim)

- This does NOT establish that TNN-2 cannot transfer. It establishes that
  the transfer protocol's online next-term-prediction measurement cannot be
  run against the frozen TNN-2 binary in feasible time.
- It is consistent with (but independent of) the TRANSFER_ANALYSIS.md
  finding that TNN-2 has no demonstrated C0-D reuse: the trial loop that
  would need to do the cross-task work is architecturally incapable of
  sustaining the measurement.
- The simulated-learner 0.3333 remains a protocol-validation score with
  zero evidential weight for any contestant total, including TNN-2.
- A future transfer measurement for TNN-2 would need either (a) a task
  whose values keep t2_asm_sum tractable (a different protocol, requiring
  its own prereg), or (b) architectural changes to the trial loop's search
  cost (a TNN-3 decision, not a patch).

## 8. Files

- refreeze/transfer/TRANSFER_REFREEZE_PREREG.md (frozen prereg)
- refreeze/transfer/tnn2_transfer_gen.zag + tnn2_transfer_gen (generator)
- refreeze/transfer/worlds/ (168 world files; K5 verified)
- refreeze/transfer/run_tnn2_transfer.sh (driver; runs killed at T_A step 17)
- refreeze/transfer/tnn2_transfer_score.zag + tnn2_transfer_score (scorer)
- refreeze/transfer/runs/run1/ (partial logs; T_A.log through step 16)
- refreeze/transfer/TRANSFER_REFREEZE_RESULT.md (this file)

Nothing committed, nothing pushed (per task). .wave_lock untouched.
