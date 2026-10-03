# PREREG_INDEX_REPRO.md - INDEX lane, wave-20261002-0221pdt

Frozen: 2026-10-02 02:45 PDT (commit alone, before any implementation).
Status at freeze: PROPOSED (unexecuted). No results below were observed before freezing.

## Scope

Two sub-tasks on the same subsystem (scaling index):

(A) Preregistered clean reproduction of the 1000-MAP scaling wave
    (C204 measurements: 1393x indexed scan reduction, emergent
    move-to-front learner indexing keys). C204 went PROCESS-FAIL for
    canonical promotion after a self-disclosed python3 invocation; its
    numbers stay exploratory until this wave confirms or kills them in
    pure Zag under safebin. A prior clean rerun (C209, commit
    405fe57e5) exists but was exploratory with no frozen prereg; this
    wave is the preregistered confirmation.

(B) Index-cycle crash: reproduce with a minimal pure-Zag reproducer,
    fix in pure Zag, land an index-validation gate that must pass
    before the index is used in production. Red-team finding (C203,
    commit 98f68d6a3, ADV-IDX-CORRUPT): a cycle in the plen-bucket
    list crashes rebind_try_idx with "panic: slice index out of
    bounds"; no liveness/type/cycle check; candidate buffer overflow
    (512 safe entries in a 4096-byte buffer, loop bound allows 1024).

## Part A protocol (exact, frozen)

A1. Toolchain: safebin at /home/hatch/safebin (36 tools, no python).
    Every shell command prefixed with export PATH="$HOME/safebin".
    which python3 must return nothing (verified Step 0, NAMECHECK.md).
    Pinned znc: src/tools/toolchain/znc_linux_x86_64_abed8aa1,
    sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef.

A2. Base regeneration (in lane work dir, not touching canonical dirs):
    - Source: docs/lab/research-lead/overnight-20260928/rebinding_hardening/hard_base.zag
    - Apply expand.sh sed pipeline (1024->8192 nodes, 4096->16384
      edges, layout constants, plus 664s and 1232s exceptions).
    - Apply the 11 line-targeted frame-slot threshold substitutions
      (1000->10000) on lines 180,199,200,205,206,208,209,348,352,356,360.
    - cmp-verify regenerated base byte-identical against
      docs/lab/research-lead/overnight-20260928/scaling_cont/sc_base_expanded.zag
      (sha256 880f24de2b74138b47b1461dc6a451e6105bc2a3b69822938bcdf8ab47f09d95).
      If cmp fails: STOP, report BUILD-FAIL with diff.

A3. Patch and driver: copy sc_patch.zag and sc_driver.zag from
    scaling_cont into the lane work dir; sha256sum-verify identical:
    patch 9f819b8a1f7a4df7d83a1243988e7b609ee851d8cb8d64478d827a98580abf67,
    driver 8543d5e02fca12c64dd8473fd7337f698afb950df49b8ba2521eb89ee7e22aa4.

A4. Assembly (build.sh line ranges, frozen): from the expanded base
    take lines 1-296, 315-418, 427-441, 473-532, 544-812, 836-1356,
    1358-1591; append sc_patch.zag; append sc_driver.zag; result is
    sc_full.zag (expect 2158 lines). Function-count check: exactly 1
    definition each of main, ev_query, promote_graph, ev_teach,
    ev_teach_in, t2_gather, t2_lu_first, rb_chain_plen,
    rebind_try_idx, rebind_try_lin, idx_mode_set, fidx_add, mtf_win.

A5. Compile sc_full.zag with the pinned znc to sc_bin. Compile must
    exit 0 with no errors.

A6. Run sc_bin three times; capture stdout to repro_r1.txt,
    repro_r2.txt, repro_r3.txt. Compute sha256 of each.

## Part A kill bar (frozen, will not be weakened)

CONFIRMED iff ALL of the following hold:
  (i)   all three runs byte-identical to each other;
  (ii)  each run sha256 =
        eee373a21053b2a3a0005be8c1c83ed923f51b22c528b36cd9425d3052146d9d
        (the canonical C204/C209 output hash);
  (iii) the metric lines match the frozen expected table below
        exactly (implied by (ii), recorded here for the kill decision):
        - S100L Q0/Q1 scan=699; S100I Q0 scan=5; S500L scan=3464;
          S500I scan=5; S1000L scan=6964; S1000I scan=5.
          Reductions: 699/5 = 140x at 100 MAPs; 3464/5 = 693x at 500
          MAPs; 6964/5 = 1393x at 1000 MAPs. All ok=1.
        - EMM (indexed+MTF): Q0 tried=49, Q1 tried=1, Q2 tried=1,
          QSTALE tried=2, all ok=1. EML/EMI controls unchanged.
        - FAL gather factvisits=32760, lu50 factvisits=24800;
          FAI gather factvisits=167, lu50 factvisits=1092; np=4,
          hits=50 both arms.
KILLED iff any of (i)-(iii) fails. The killing evidence (which
condition failed, divergent hash, first divergent line) is recorded
in REPRO_RESULTS.md. A hash mismatch kills even if the headline
1393x number happens to match: byte-identical rerun is the bar.

Pure-Zag attestation (frozen requirement): the wave log must show
safebin activation, which python3 empty, and zero invocations of
python/python3 in any lane shell history; any forbidden invocation
is automatic PROCESS-FAIL with immediate disclosure.

## Part B protocol (exact, frozen)

B1. Minimal crash reproducer (crash_repro.zag, pure Zag, standalone):
    Replicates the vulnerable pattern of si_patch.zag rebind_try_idx
    (lines 156-170): cand buffer z_alloc(4096) bytes, collection loop
    bound nc<1024, 8 bytes written per candidate (set32 at nc*8 and
    nc*8+4), bucket list walked via a next-pointer accessor with no
    cycle/bounds check. Builds a 2-node cyclic bucket list
    (self-loop, the red-team C2 shape) and runs the collection.
    EXPECTED (frozen): the program panics with "slice index out of
    bounds" (nonzero exit), because the cycle drives nc to 1024 while
    only 512 entries fit. This is the pre-fix behavior.

B2. Fixed collection pattern (same reproducer, fixed walk):
    cycle detection (Floyd tortoise-and-hare on the next pointers),
    writes bounded by true buffer capacity, out-of-range next
    pointers treated as list end, only live MAP members collected.
    EXPECTED (frozen): completes with exit 0, collects each cyclic
    member exactly once, reports CYCLE-DETECTED. No panic on:
    self-loop, 3-cycle, out-of-range next pointer, non-MAP member.

B3. Index-validation gate (validate_gate.zag, pure Zag, tested against
    the real index structures: tag-40 index node, plen-bucket heads at
    fields 20/24/28/32, intrusive field-12 lists; FACT subject index:
    24 buckets over chained tag-40 nodes, intrusive FACT field 12):
    idx_validate(W) returns 1 (ACCEPT) iff every MAP bucket list is
    acyclic, every member id is in node range, live (field 36 == 1),
    tag 20, and its chain plen (rb_chain_plen of its root) equals its
    bucket plen; fidx_validate(W) returns 1 iff every FACT bucket
    chain is acyclic with members in range, live, tag 1.
    Gate test matrix (frozen expectations, each 3/3 deterministic):
      G1 healthy index: ACCEPT (both gates return 1).
      G2 cyclic plen bucket (self-loop): REJECT (return 0).
      G3 non-MAP member prepended to bucket: REJECT.
      G4 out-of-range next pointer: REJECT.
      G5 plen-mismatched member (plen-3 MAP in plen-5 bucket): REJECT.
      G6 cyclic FACT bucket chain: fidx gate REJECT.
    EXPECTED (frozen): G1 ACCEPT; G2-G6 REJECT.

B4. Production integration (fix.zag delta on the lane's sc_patch copy):
    rebind_try_idx calls idx_validate first and falls back to
    rebind_try_lin on REJECT; candidate collection uses the fixed
    walk; t2_gather/t2_lu_first dispatch consults fidx_validate and
    falls back to linear variants on REJECT; mtf_win search loop gets
    a step cap. Then rebuild sc_full with the fixed patch and rerun
    the Part A protocol (A4-A6).

## Part B kill bar (frozen, will not be weakened)

FIX-VERIFIED iff ALL of the following hold:
  (i)   B1 reproducer panics pre-fix as specified (crash reproduced);
  (ii)  B2 fixed pattern passes all five shapes with exit 0;
  (iii) B3 gate matrix matches frozen expectations (G1 ACCEPT,
        G2-G6 REJECT), 3/3 deterministic;
  (iv)  the fixed production rebuild still yields the canonical
        output hash eee373a21053b2a3a0005be8c1c83ed923f51b22c528b36cd9425d3052146d9d
        on 3/3 runs (fix+gate are no-ops on healthy state; the red
        team caveat that the scaling claim holds only on intact state
        is preserved, and intact-state numbers are unchanged).
FIX-FAIL iff any of (i)-(iv) fails, with the failing condition and
evidence recorded. A fix that changes healthy-state output fails
(iv) even if the crash is gone.

## Red-team self-review (frozen requirement)

CRASH_REPRO.md, FIX.md, and VALIDATION_GATE.md each end with a
red-team self-review section that attacks the work: alternative
explanations for the crash, ways the fix could be incomplete (missed
corruption shapes, gate bypass paths, performance regressions),
and what would falsify the verdict. The verdict lines name this
prereg as the governing frozen bar.

## Governance

This prereg is committed ALONE before any implementation file.
Prereg commit strictly precedes implementation commits. No kill bar
above may be weakened after seeing results; amendment requires a new
frozen prereg and re-execution. Pure Zag only; no Python anywhere.
