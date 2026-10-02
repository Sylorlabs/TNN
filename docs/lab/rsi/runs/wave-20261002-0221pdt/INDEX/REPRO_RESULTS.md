# REPRO_RESULTS.md - INDEX lane, wave-20261002-0221pdt (Part A)

Governing bar: PREREG_INDEX_REPRO.md (commit b507fe591, frozen alone
before implementation).

## Protocol executed (frozen A1-A6)

- Toolchain: safebin /home/hatch/safebin, 36 tools, no python.
  `which python3` empty in every shell (Step 0, NAMECHECK.md).
  Zero python/python3 invocations in this lane.
- Pinned znc sha256
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
  (prefix 498abcb5 matches the pinned value; verified before use).
- Base regenerated from
  docs/lab/research-lead/overnight-20260928/rebinding_hardening/hard_base.zag
  via the expand.sh sed pipeline plus the 11 line-targeted 1000->10000
  frame-slot threshold substitutions (lines
  180,199,200,205,206,208,209,348,352,356,360).
  cmp-verified byte-identical against the canonical
  scaling_cont/sc_base_expanded.zag (sha256
  880f24de2b74138b47b1461dc6a451e6105bc2a3b69822938bcdf8ab47f09d95).
- sc_patch.zag / sc_driver.zag copied into the lane and
  sha256sum-verified identical to canonical
  (9f819b8a1f7a4df7d83a1243988e7b609ee851d8cb8d64478d827a98580abf67 /
   8543d5e02fca12c64dd8473fd7337f698afb950df49b8ba2521eb89ee7e22aa4).
- Assembled sc_full.zag (2158 lines) per frozen line ranges; all
  function-count checks passed (the t2_gather:4 count is
  t2_gather_sum + lin + idx + dispatch, identical to canonical).
- Compiled with the pinned znc, exit 0 (warnings only, same class as
  canonical). Ran sc_bin 3x (each about 30 s, exit 0).

## Results

Run output hashes (3/3):
  eee373a21053b2a3a0005be8c1c83ed923f51b22c528b36cd9425d3052146d9d
  repro_r1.txt / repro_r2.txt / repro_r3.txt
This is exactly the canonical C204/C209 output hash. repro_r1.txt is
additionally cmp-identical to scaling_cont/run1.txt.

Metric lines (all ok=1):
  S100L Q0 scan=699   S100I Q0 scan=5     -> 140x
  S500L Q0 scan=3464  S500I Q0 scan=5     -> 693x
  S1000L Q0 scan=6964 S1000I Q0 scan=5    -> 1393x
  EMM Q0 tried=49, Q1 tried=1, Q2 tried=1, QSTALE tried=2
  FAL gather factvisits=32760, lu50 factvisits=24800
  FAI gather factvisits=167,   lu50 factvisits=1092 (np=4, hits=50)

## Kill-bar evaluation (frozen)

  (i)   3/3 runs byte-identical: HOLD.
  (ii)  hash equals the canonical eee373a21...: HOLD.
  (iii) metric table matches the frozen expected table: HOLD.
  Pure-Zag attestation: HOLD (safebin only, which python3 empty,
  no forbidden invocations).

## Verdict

Part A: CONFIRMED. The 1393x indexed scan reduction at 1000 MAPs
(6964 -> 5 scan visits), the 693x at 500 MAPs, the 140x at 100 MAPs,
the move-to-front emergent ordering (49 -> 1 verifies, stale
recovery in 2), and the FACT index reductions (gather 32760 -> 167,
lookup 24800 -> 1092) all reproduce cleanly in pure Zag under
safebin, 3/3 byte-identical to the canonical output. The C204
measurements are promoted from exploratory to preregistered-confirmed
evidence by this wave. The red-team caveat stands: the claim holds on
intact index state (Part B hardens the corrupt-state behavior).

## Red-team self-review (Part A)

- Could the byte-identical hash be a false friend (same bug
  reproduced faithfully)? Yes in principle: this confirms the
  MEASUREMENTS, not the absence of implementation flaws. The
  implementation flaws the red team found (index-cycle crash) are
  addressed in Part B, not by this rerun.
- The 1393x number measures scan visits (header 56), not wall time
  or verifies; the honest limits from the scaling_cont report still
  apply (index removes scan work, not verifies; t2_gather linear
  mode still O(8192); 8192-node ceiling).
- The reproduction used the unfrozen expanded base (8192 nodes),
  not the frozen 1024-node TNN-2 base; it confirms the scaling claim
  for the scaling line, nothing about the frozen core.
- Determinism: 3/3 byte-identical including the MTF emergent order,
  so no hidden nondeterminism in the measured paths.
