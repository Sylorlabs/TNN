# PROTOTYPE_EVAL: trial-garbage reclamation

Lane: ARENA-ENG, wave-20261002-0521pdt. Date: 2026-10-02 PDT.
Prereg: PREREG_TRIALWALL.md (frozen alone at 43f3887cc before implementation).
Prototype: `trialwall.zag` (trialwall_bin), pure Zag, pinned znc, safebin,
`which python3` empty. Standalone: never wired into frozen TNN-2.

## Implementation (as preregistered)

- Per-candidate allocation log: `t2_cell_r` / `t2_lit_r` record every
  workspace node allocated for a trial candidate into a host-side log.
- `t2_try_verify_r`: verbatim verify; on REJECT frees exactly the logged
  nodes and runs one O(4096) edge sweep killing edges with a dead endpoint.
  On VERIFY frees nothing; promotion path untouched.
- `t2_exec_r`: verbatim execute; frees the scratch frame after the result
  integer is computed.
- `_r` assembler variants (`t2_asm_chain_r`, `t2_asm_count_r`,
  `t2_asm_sum_r`) are verbatim logic over the logging builders; on the
  (unreachable) mid-build alloc failure they free the partial log and sweep.
- Sweep runs per-reject, before the next candidate assembles: freed indices
  are reused by later allocs, so a stale SEQ edge would otherwise corrupt
  the next candidate's execute (seq_nx scans from slot 0).
- No ISA change, no new opcodes, no new modes/bridges/handlers. The verbatim
  ORIG core is untouched in the same binary (mode o/r selected by argv).

## Measurements

S1 wall broken (transfer T_A replica, 21 steps):
- ORIG: steps 0-14 in 4.3s total; step 15 marginal ~84s (28 evictions);
  step 16+ infeasible (sealed real-binary attempt: 72.6s / 124.1s).
- RECLAIM: steps 0-20 in 2.76s TOTAL. Cumulative T(0..14)=1.27s,
  T(0..15)=1.97s, T(0..20)=2.76s; max single step bounded by the total,
  every step far under the 5s bar. Flat curve, no blowup at step 15.
- S1: HOLD.

S2 no evictions:
- d_evict = 0 on all 21 reclaim steps (ORIG: 28 on step 15 alone).
- True live nodes (scan): 8, 16, 25, ... 165 at step 20 (~8/step: observes
  plus inquiry nodes). Far under the 1024 cap.
- S2: HOLD.

S3 outcome identity, feasible prefix (steps 0-14):
- Per-query (k, ans, tried, rej) byte-identical ORIG vs RECLAIM on all 15
  steps (diff of extracted fields: no differences). ans=-2 throughout,
  matching the sealed T_A.log.
- No promotions occur in either mode (every query misses), so the promoted
  MAP set is identically empty; taught facts come only from the identical
  observe sequence in both modes.
- Node/edge COUNTS differ as intended (reclaim keeps no trial garbage:
  edges 73 vs 339+ at step 20/14); hg(W,20) is gross allocs (never read by
  logic), true live count used instead.
- S3: HOLD.

S4 success path preserved (fresh workspaces, both modes):
- (i) sum-branch success, t_p2 pattern: ans=60, tried=1, rej=0, MAP
  s=110 r=41 ans=60 deps=3, 32-cell sig of 103:0 all identical;
  TAUGHT (110,41,60) found=1; nodes=67 edges=70 identical.
- (ii) chain-branch success, t_p1/t_f2 pattern, masked and unmasked:
  ans=201, tried=1, rej=0, MAP s=101 r=40 ans=201 deps=2,
  sig=102:101,101:102,102:102,101:201 all identical; TAUGHT found=1.
- Full 4-line outcome blocks diffed pairwise: IDENTICAL in all 3 pairs.
- S4: HOLD.

S5 purity:
- Pure Zag under safebin; zero python invocations; no new opcodes, modes,
  bridges, handlers; protected-core ISA untouched. Code delta is additive
  (_r variants + 4 helpers); the verbatim ORIG core is unmodified apart
  from write-only INSTR counters.
- S5: HOLD.

Determinism: reclaim 0-20 run twice, byte-identical (cmp clean).

## Verdict: APPROACH-VIABLE

All five frozen criteria hold. The wall is broken by trial-garbage
reclamation with provably identical trial outcomes (differentially verified
on 15 prefix steps plus 3 success scenarios).

## Queued for next wave: integration design for TNN-3

- Port the reclaim helpers (`log_add`, `trial_free_log`,
  `trial_sweep_edges`, frame freeing in the executor, logging builders)
  into the TNN-3 trial subsystem. This is a TNN-3 architecture decision,
  not a patch: frozen TNN-2 is untouched by this lane.
- Design notes: decrement the hg(W,20) telemetry counter on trial-free
  (prototype leaves it as gross allocs; harmless, nothing reads it);
  keep the per-reject sweep placement (correctness-critical, see above);
  the alloc-log already makes literal freeing exact, no hardening needed.
- Open question for the integration wave: whether miss_inquire's
  uncertainty/guide nodes (~3/query, intentional learner state, kept here)
  want their own lifecycle policy at larger scales; not the wall, noted.

## Files

- trialwall.zag (prototype source; ORIG core verbatim + INSTR + _r reclaim)
- trialwall_bin (built with pinned znc under safebin)
- tw_orig_14.txt (ORIG steps 0-14 profile), tw_orig_15.txt (ORIG wall point)
- tw_reclaim_20.txt (RECLAIM steps 0-20 profile), s4_final.txt (S4 outcomes)
- TRIALWALL_DIAGNOSIS.md, PREREG_TRIALWALL.md (frozen at 43f3887cc)

No transfer scoring was run. No simulated scores are reported as evidence.
