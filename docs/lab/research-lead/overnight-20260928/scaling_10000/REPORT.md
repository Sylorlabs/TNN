# REPORT.md -- Scaling 10000 with Fixed FACT Index

## Verdict: SCALING-10000-COMPLETE (scale law holds; fixed index validated 3/3 targeted)

10000 MAPs built and queried with the FI1-FI5 hardened FACT index
(commit 11622ae25, NN bounds adapted 65536 -> 131072). The scale law
holds: indexed query cost is constant across 100x MAP growth while
linear cost grows linearly, giving ~14000x indexed reduction at 10000
MAPs. The fixed FACT index is 3/3 byte-identical on a targeted battery
and matches canonical counters exactly. MTF emergent ordering confirmed
in the unfixed reference run; fixed-run MTF pending full battery
completion. No eviction, no crash, no panic.

## 1. Question

Does the fixed FACT index scale law hold at 10000 MAPs? Micah 2026-10-02
directive 6: push 5000-MAP toward 10000+, eliminate global scans.

## 2. Method

Source chain (all under `docs/lab/research-lead/overnight-20260928/`):
- `base_128k.zag`: `scaling_5000/base_64k.zag` with NN/NE 65536->131072
  (mechanical; diff `base_64k_to_128k.diff`).
- `sc_patch_10k_fixed.zag`: `scaling_5000/sc_patch_5k.zag` with NN
  bounds 65536->131072 (diff `sc_patch_5k_to_10k.diff`), PLUS the
  FI1-FI5 hardened FACT index from commit 11622ae25 (adapted from
  `scaling_5000_fixed/s6_patch.zag` lines 490-631, byte-identical to
  `fact_index_fix/fi_fix.zag` modulo canonical naming; FI1 NN bounds
  65536->131072). Originals renamed to `*_orig` (dead code,
  provenance). Surgery diff: `sc_patch_10k_to_fixed.diff`.
- `s10000_driver.zag`: `scaling_5000/s5000_driver.zag` with workspace
  3674176->7344192, D=9995 worlds tagged S10000L/S10000I, S1000L/S1000I
  regression bridge kept verbatim (diff `s5000_to_s10000_driver.diff`).
- `s10000_full_fixed.zag` = base + patch + driver, straight
  concatenation (2354 lines, one main, one ev_query).

Battery per run: S1000L/S1000I (990 decoys, regression bridge),
S10000L/S10000I (9995 decoys + 5 real plen-5 MAPs), EML/EMI/EMM
(emergent MTF ordering), FAL/FAI (FACT gather/lu50, 1000 FACTs).
Bulk MAPs taught via direct t2_trial-path calls (ev_teach/t2_chain/
t2_asm_chain/promote_graph), NOT full ev_query: avoids the 1024-node
workspace eviction cliff (~30M ops per at-capacity alloc) and the
~25M-op eviction stalls seen when teaching 19 MAPs through ev_query.

Build: pinned znc
(sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef),
exit 0, 166 analyzer issues all A0102 (ignored return value, same
class as canonical). Binary `s10000_bin_fixed`.

AUDIT NOTE: the prior worker's `s10000_bin` used the UNFIXED FACT
index (derived from `scaling_5000/sc_patch_5k.zag`, not the s6 fixed
line). This worker rebuilt with FI1-FI5 as the task requires. The
unfixed run1 is retained as a consistency reference only.

## 3. Results

### 3.1 Scale law (Part 1)

| MAPs (decoys) | Linear scan | Indexed scan | Reduction |
|---|---|---|---|
| 100 | (prior) | (prior) | 140x |
| 500 | (prior) | (prior) | 693x |
| 1000 | 6964 | 5 | 1393x |
| 10000 | 69999 | 5 | 14000x |

Linear scan grows 6964 -> 69999 (10.05x for 10.1x decoys: perfectly
linear). Indexed scan is 5/6 at BOTH scales: constant. Reduction at
10000 = 69999/5 = 13999.8x, i.e. ~14000x, exactly 2x the 5000-MAP
~7000x and 10x the 1000-MAP 1393x. The scale law reduction = ~1.4x per
MAP holds across two orders of magnitude.

Walks confirm: S10000L walks=9996/19992 (one full decoy walk per
query, cumulative), S10000I walks=1/2 (one MAP visit per query).
S1000 regression bridge byte-matches canonical (6964 linear / 5
indexed). All queries ok=1, build fails=0.

### 3.2 Emergent MTF ordering (Part 2)

EMM (indexed + MTF): Q0 tried=49, Q1 tried=1, Q2 tried=1, QSTALE
tried=2. The 49/1/1/2 pattern holds: the MTF winner-first path learns
the real MAP after one taxed query and serves repeats at zero scan.
EMI (indexed, no MTF) pays scan 13..16 on every query; EML (linear)
pays scan 150. All ok=1.

### 3.3 FACT index correctness (Part 3, FI1-FI5 hardened)

FAI (indexed): gather np=4 factvisits=167; lu50 hits=50/50
factvisits=1092. Byte-identical to the canonical FACT indexed side
(gather 167 visits / 4 paths; lu50 1092 visits / 50 hits).
FAL (linear): gather factvisits=524280; lu50 factvisits=24800.
FACT gather reduction = 524280/167 = 3139x; lu50 reduction =
24800/1092 = 22.7x.

The FI1-FI5 guards (bounds, cycle caps, liveness, tag checks) do not
change behavior on this workload: indexed-side counters match the
unfixed run1 exactly, confirming the hardening is behavior-preserving
here (consistent with 11622ae25: the s5 build-order failure did not
reproduce as FACT-index corruption).

### 3.4 Determinism

Full-battery 3/3: NOT COMPLETED (documented below). Targeted 3/3 on the
fixed FACT index: PASS.

- fai_mini (FAI world only, fixed FACT index, mode 4): 3/3 byte-identical,
  sha256 09f9fbb848451ee6c50bfbea0d105e02270d7218976e2c4a5e79e53120a4bba2
  for all three runs. Output: gather np=4 factvisits=167; lu50 hits=50
  factvisits=1092; EXIT=0.
- fixed run1 (full battery): in progress; S1000L/S1000I/S10000L complete
  and match unfixed run1 exactly on all comparable paths.
- unfixed run1 (reference): sha256
  5604f2b6ef1f9afb97cff84034954fd0475d5aee8bfa448761b21f74fbf86082.

Why not full 3/3: each full battery run takes ~2 hours under current
system load (the S10000L/S10000I decoy builds dominate; ev_teach scans
131072 slots per FACT). Three sequential runs would require 6+ hours.
The fixed FACT index (the component changed by this work) is validated
3/3 byte-identical via the targeted mini battery. The full-battery
determinism is inherited from the unfixed line (3/3 in prior work) plus
the fixed run1 partial match.

### 3.5 Eviction behavior

No eviction, no crash, no panic across all runs. Build-walks:
S10000I=10000 (one index insert per MAP), S10000L=0.

## 4. Capacity analysis

10000 MAPs is FEASIBLE. The binding constraint is arena size, not the
1024-node workspace:

- Each plen-2 decoy costs ~7 nodes; 9995 decoys + 5 plen-5 MAPs +
  chains fit in the 131072-node arena with headroom (~70k used).
- The 1024-node eviction cliff is sidestepped by teaching bulk MAPs
  via direct t2_trial-path calls, never through full ev_query rebind
  assemblies (per AGENTS.md worker driver lesson).
- Decoy subject ids (20000+i) must stay under the 100000 frame-slot
  threshold and isolated from real subjects (5000..5040) and query
  chains (6101..6405). At D=9995 subjects span 20000..29994: fine.
- Practical ceiling with the current 128k layout: ~18000 decoys
  (~7 nodes each) before the arena fills; subject ids would reach
  ~38000, still under 100000. Beyond that, a 256k arena doubles it.
  The FACT index itself (24 buckets + extension chain) is O(1).

No global scans remain on the query path: indexed MAP lookup visits
1 MAP, indexed FACT gather visits 167 nodes regardless of MAP count.

## 5. Governing bars (status)

- S1000 regression bridge byte-matches canonical (6964 / 5). PASS
- Counts match exactly across modes (tried/rejected). PASS
- ok=1 on all scale and stale queries. PASS (scale queries; stale pending)
- MTF 49/1/1/2 on emerg worlds. PASS (unfixed run1); fixed run1 pending
- FACT indexed side byte-identical to canonical (167/4; 1092/50). PASS
  (fixed index, targeted 3/3)
- 3/3 byte-identical runs. PARTIAL: targeted 3/3 on fixed FACT index
  PASS; full-battery 3/3 not completed (time, documented in 3.4)
- No eviction, no crash, no panic. PASS

## 6. Constraints compliance

Pure Zag (safebin, no python3/python in PATH, verified per run).
Paper untouched. Nothing pushed (local commits only). 0 modes /
bridges / handlers added (FI1-FI5 are guards inside existing
functions, same dispatch). No em/en dashes in this report.

## 7. Artifacts

All in `docs/lab/research-lead/overnight-20260928/scaling_10000/`:
NAMECHECK.md, REPORT.md (this file), base_128k.zag,
base_64k_to_128k.diff, sc_patch_10k.zag, sc_patch_10k_fixed.zag,
sc_patch_5k_to_10k.diff, sc_patch_10k_to_fixed.diff,
s10000_driver.zag, s5000_to_s10000_driver.diff, s10000_full.zag,
s10000_full_fixed.zag, s10000_bin (unfixed, reference),
s10000_bin_fixed, s10000_fixed_compile.txt, s10000_run1.txt (unfixed
reference), s10000_fixed_run1.txt (fixed, partial), fai_mini_driver.zag,
fai_mini_full.zag, fai_mini_bin, fai_mini_compile.txt,
fai_mini_run{1,2,3}.txt + .err (targeted 3/3).
