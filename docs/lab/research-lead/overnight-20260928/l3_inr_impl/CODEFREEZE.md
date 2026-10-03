# L3-INR Implementation Code Freeze

**Frozen:** 2026-10-03. Implements the frozen prereg (ledger C363, K1-K12/KC0A-D).
**Prereg freeze:** commit `2a0ce93cf` (PREREG.md), design freeze `2ec76f977`.
**Commit order:** prereg commit strictly precedes this implementation (verified).

## Binaries (pure Zag, pinned znc)

- `build/learner_bin` — LEARNER process (phase state machine).
- `build/world_bin` — WORLD process (hidden order, protocol responses).
- `build/spearman` — DEV tool (attribute correlation check).
- Deterministic rebuild verified: `src/build.sh` recompiles and `cmp`s byte-identical.

## Source layout (`src/`)

- `prelude.zag` — I/O, string/number formatting, xorshift, file ops.
- `graph.zag` — reachability (`reach_of_edges`), ranking (`rank_by_reach`).
- `state.zag` — work.dat/kb.dat/edges.dat/slot/hyps persistence, trace, outbox.
- `learner.zag` — phase state machine (T1-T5b, C0-C5).
- `world.zag` — DEV world simulator (OBSERVE/TEST/COMMIT/DEFER protocol).
- `build.sh` — concatenation + pinned znc compile + rebuild check.

## Learner design (prereg section 4)

- **Two-process protocol:** learner writes requests to `outbox.txt`; shell driver
  (`run_arm.sh`) relays through `world_bin` into `inbox.txt`. Learner never
  receives the world path (information firewall, A-INFO).
- **Construction (T1/T4/T5a/T5b/C4):** propose-and-test over COMPLETE edge sets
  (prereg 4c, V2 defeat). ADD phase seeds E with a direct edge per positive
  training pair (known-true from OBSERVE; total-order positives form a DAG).
  No per-edge positive-gain requirement (anti-V2). Scores the complete set via
  the consequence channel (TEST-PAIR). DEL phase removes edges while full
  training acceptance holds (fewer edges preferred on ties).
- **Cycle guard:** ADD rejects edges that would close a directed cycle
  (hypothesis space is strict orders; disclosed here, names no topology).
- **T4 revision:** loads slot G, monitors 6 training pairs; on REJECT, purges
  toxic edges (directly contradicted by new training), adds new positives,
  DEL-minimizes, commits to slot G2 (preserving G for T3b) with parent pointer.
- **Hypotheses/probes (T5a/T5b):** unconstrained pairs → variants (cap 4);
  goal-directed TEST-PAIR probes; FORBIDDEN → mark out-of-domain; DEFER if no
  discriminating probe in-domain.
- **Controls:** C0 (attr-NN), C1 (memo+1NN), C2 (greedy attr-threshold OR),
  C3 (greedy single-edge hill climb), C4 (scratch construction + rank),
  C5 (id-order rank).

## Budgets (prereg section 6)

B_CONSTRUCT=3000, B_RANK=300, B_REVISE=2000, B_PROBE=150, B_SURFACE=50.
Per-arm caps in `run_arm.sh` mirror the learner's internal checks.

## DEV worlds (`dev/`, my designs, DEV ONLY)

- `dev_s1.world` — order e2<e0<e5<e8<e1<e7<e3<e9<e4<e6>; 18 train, 6+6 heldout.
- `dev_s1p.world` — same order, recoded attrs; fresh HELDOUT_C.
- `dev_s2.world` — e3/e9 swap; regime change for T4.
- `dev_s3a.world` — (s4,s5) unconstrained, in-domain probe.
- `dev_s3b.world` — (s4,s5) out-of-domain (PROBE_EXCEPT).
- `dev_s1trap.world` — greedy trap for C3.
- All attributes |Spearman| < 0.2 vs true order (verified by `spearman`).

## What this freeze does NOT cover

Sealed worlds (S1/S2/S3/S1p) are designed post-freeze by an independent
adversary. This freeze covers DEV validation only. The L3 verdict requires the
sealed battery + red team.
