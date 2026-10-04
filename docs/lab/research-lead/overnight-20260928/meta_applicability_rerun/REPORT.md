# REPORT.md: Meta-Learning Applicability RERUN (Micah Priority 5)

## Verdict: FAIL (K3)

Per frozen PREREG (2026-10-02): "Verdict
META-APPLICABILITY-RERUN-COMPLETE requires K1-K8 all PASS. Any bar
failed: verdict is FAIL with the bar named, no reinterpretation."

K7 now PASSES (the recovery target): all three arms complete 3/3
byte-identical runs. K1, K2, K4, K5, K6, K8 PASS. K3 FAILS on its first
clause: TREAT_C=49 is not less than NAIVE_C/2=29.5. The failure is
reported straight; Section "K3 analysis" explains what it teaches.

## Transfer matrix (verify-tries per problem; lower is better)

| Domain | TREAT (Phase1+gate) | FRESH (no Phase1+gate) | NAIVE (Phase1, no gate) |
|--------|-------------------|----------------------|------------------------|
| A' (related) | 1,1,1,1,1 (total 5) | 6,1,1,1,1 (total 10) | 1,1,1,1,1 (total 5) |
| B (irrelevant) | 1,1,1,1,1 (total 5) | 1,1,1,1,1 (total 5) | 11,11,1,1,1 (total 25) |
| C (misleading) | 29,4,4,4,4,4 (total 49) | 24,4,4,4,4,4 (total 44) | 29,26,1,1,1,1 (total 59) |

All values measured 3/3 byte-identical (SHA-256 below). FRESH is
byte-identical to the 2026-10-01 FRESH run (hash match below), so the
base fix changed no observable behavior.

## Kill bars (frozen 2026-10-02)

- K1 positive transfer: TREAT_A'=5 < FRESH_A'=10. PASS.
- K2 neutral: TREAT_B=5 <= 2*FRESH_B=10 PASS; 5 < NAIVE_B/3=8.33 PASS.
  (NAIVE_B measured directly at 25, not via the redteam prediction.)
- K3 recovery: TREAT_C=49 < NAIVE_C/2=29.5 FALSE; last 3 C problems of
  TREAT trial-only (gate=0) TRUE. FAIL (first clause).
- K4 no false negatives: TREAT_A' gate=1 on all 5. PASS.
- K5 B no-burn: TREAT_B gate=0 on all 5. PASS.
- K6 C learns: TREAT_C0 gate=1 (one exploratory burn), w_cx 100->150
  strictly increases, TREAT_C1..C5 gate=0 (all five now measured,
  including the previously hung C5). PASS.
- K7 determinism: 3/3 byte-identical per arm. TREAT
  030fd9b50e423592e05682edcf485646d9c83bf1bc5916ff046b1be9ad449993;
  FRESH
  afe2fff8dc5982ed93e621180822825d51d438d029d8ded75e3e20c0ffadee0d
  (matches 2026-10-01); NAIVE
  97645756adead29e9d1fdc192c0a7e314ac0ae59d7d497799d06aa6050c3130f.
  PASS.
- K8 process: pure Zag, safebin PATH, `which python3 python` empty. PASS.

## Bug diagnosis: the 21st-problem stall (prior FAIL cause, now fixed)

Exact cause, confirmed by instrumentation (nodes/edges live count
printed per problem on a diagnostic build of the prior source):

1. Every failed `t2_trial` candidate assembles a fresh 4-op ISA graph
   (`t2_asm_chain`: 4 cells per link: 2 literals + guard + set) and every
   `t2_try_verify` allocates one frame node in `t2_exec`. On
   verification failure none of it was freed. Rebind failures
   (`pc_try_one`) leak the same way.
2. The node arena is 1024 slots. Measured live counts on the TREAT
   sequence: 81 after A-P0, +28/problem through the A/A' blocks (rebind
   successes are promoted and legitimately persist), 423 after B,
   then the C-P0 burn (25 failed rebinds) jumps 423->779, and C-P1..C-P4
   add about 51/problem, reaching 983 live nodes after C-P4.
3. C-P5 needs about 1034 nodes > 1024. Past the limit, every
   `alloc_node` falls through to `evict_node`, whose lowest-bid scan
   costs O(1024 nodes x 4096-edge is_prot/bid scans) per eviction.
   C-P5 performs dozens of allocs, each triggering a full scan: the run
   stalls in pathological slowdown. Not an infinite loop (`execute`
   carries a 1000-step budget; all arena scans are bounded). FRESH has
   only 16 problems and completes just under the limit, which is why the
   stall hit TREAT/NAIVE (21 problems) only.

Fix (in the rerun copy `ma_base.zag` only; frozen base untouched):

- New `t2_free_graph(W, root)`: walks the failed candidate's SEQ edges
  (type 12), BRANCHEQ true-targets (field12), and private literal nodes
  (field8 with tag 902 and alive), removes every edge touching a
  collected cell, marks collected cells dead.
- `t2_try_verify` reclaims the candidate graph on the failure path.
- `t2_exec` reclaims its per-verify frame node before returning.

Verified (promoted) graphs are never freed. No verify outcome, trial
count, gate decision, or consequence record can change: the experiment
path (activate/gather/features/gate/rebind/trial) never consults arena
counters, node bids, or map_standing, and with reclamation the arena
never fills so eviction never fires. Proof: the rerun FRESH 3/3 hash is
byte-identical to the 2026-10-01 FRESH hash. The APPL gate
(`ma_patch.zag`) and driver (`ma_driver.zag`) are unchanged.

## K3 analysis: what the failure teaches

The 2x clause was calibrated on the predicted NAIVE_C=159 (the
2026-10-01 prereg assumed the naive baseline burns ~25 rebind tries on
every C problem). Measured NAIVE_C=59: the naive baseline does NOT keep
burning. It burns on C-P0 (29: 25 failed rebinds + 4 trial) and C-P1
(26: 25 failed rebinds + 1 success), because the C-P0 trial promotes a
correct plen-4 MAP that rebind then reuses for 1 try each on C-P2..C5.

There is a genuine mechanism limitation underneath, not just a
miscalibrated bar. The APPL gate judges problem-level applicability
("attempt reuse at all?") but cannot distinguish per-candidate
applicability ("reuse WHICH structure?"). After the C0 burn it refuses
all reuse on C-like problems (gate=0 on C-P1..C5, paying trial cost 4
each), while the correct policy is "do not reuse the A-MAPs, but DO
reuse the C0-promoted plen-4 MAP" (1 try each, as naive discovers by
blind search). The gate's pessimism after a single failure record
conflates "rebind of prior structures failed" with "no reuse possible",
missing the C-P2..C5 reuse that naive captures. This points to
per-candidate (per-MAP) applicability judgments as the next frontier,
beyond the current problem-level gate. Reported as an informative
negative per standing rules: the decision-quality bars (K4/K5/K6) are
perfect, the totals favor the gate on every block (A' 5 vs 10, B 5 vs
25, C 49 vs 59), but the 2x recovery bar fails and the reason is
mechanism-relevant.

## Mechanism (unchanged from 2026-10-01)

The APPL gate (`ma_patch.zag`) makes reuse decisions from 8 observable
pre-reuse features: [np, pmax, c5, c4, c3, c2, cx, r], where cx counts
gathered paths containing a non-r1 edge. Each reuse attempt stores a
consequence record (features, success/failure, cost); max 32 records.

Decision rule: attempt reuse iff avg similarity to successes exceeds avg
similarity to failures by margin 15 (pessimistic prior). Optimistic when
fewer than 3 records exist.

Weight learning (consequence-driven, learner-owned): on each attempt,
find nearest opposite-outcome record G; for each feature j,
w_j += 25 * |F_j - G_j|, clamped to 800. The researcher owns the feature
list, formula, margin, ETA, and cap. The learner owns all weights,
records, and decisions.

Counterfactual replay: C0 features under final TREAT weights -> gate=0
(REPLAY-C0-finalW gate=0 wcx=150), confirming the learned weights (not
just record count) drive rejection. NAIVE replay stays gate=1 (no
records, nrec=0).

## Honest boundaries

- The C0 burn costs 29 verify-tries (25 failed rebind + 4 trial). The
  gate does not prevent the first misleading attempt; optimism under
  nrec<3 is by design (preregistered).
- K3's failure is reported without reinterpretation per the frozen
  verdict rule, with the mechanism-relevant analysis above.
- The base fix is confined to the unfrozen rerun copy; the frozen
  TNN-2 base (`learning_to_learn/l2l_base_trim.zag`) is byte-unchanged
  (verified clean). The fix addresses a resource-management defect in
  the miss policy, not a cognitive claim.
- Feature list, similarity formula, margin, ETA, cap, and optimism
  threshold are researcher-owned. Learner-owned: weights, records,
  decisions. This is L2 structural learning (consequence-driven weight
  adaptation), not L3 representational invention.

## Determinism

3 runs per arm, byte-identical outputs, SHA-256 recorded above.

## Process note

The fresh PREREG.md + NAMECHECK.md were staged for a prereg-alone
commit, but a concurrent worker's commit (12e7bc301, H-XIO-1 prereg)
swept the staged files before this worker's commit executed. Both files
were verified byte-intact in 12e7bc301 (timestamp 2026-10-02 14:25:36
UTC), which strictly precedes the fixed implementation's build and runs;
prereg-first ordering holds on content and time. The implementation and
results are committed separately below with explicit pathspecs.

## Files

- `ma_base.zag`: prior `ma_base.zag` (verbatim frozen base) + the
  t2_trial reclaim fix (`t2_free_graph`, frame reclaim). Diff vs the
  2026-10-01 source is confined to these additions.
- `ma_patch.zag`: APPL gate + two-pass rebind (unchanged).
- `ma_driver.zag`: 3-arm driver (unchanged).
- `build.sh`: 3-arm stamp/compile flow (cd updated to the rerun dir).
- `ma_full_treat/fresh/naive.zag`: concatenated build inputs.
- `ma_treat/fresh/naive_bin`: compiled binaries (263987 bytes each).
- `run_*.txt`: 9 run outputs (3 per arm), byte-identical per arm.
- `treat/fresh/naive_compile.txt`: build logs.
- `PREREG.md`: frozen preregistration (2026-10-02, fresh after base fix).
- `NAMECHECK.md`: toolchain guard, ordering note, diagnosis summary.
