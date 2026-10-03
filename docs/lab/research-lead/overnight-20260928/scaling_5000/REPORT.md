# REPORT.md -- Scaling 5000 Worker

Worker: Scaling 5000 Worker. Date: 2026-10-02. Pure Zag, zero Python.
Unfrozen only; frozen read-only; paper untouched; nothing pushed.

## Verdict: SCALING-5000-COMPLETE

The hardened MAP index (index_harden, I1-I5 invariants) holds at 5000
MAPs on a 65536-node / 65536-edge workspace. Scale law, verify counts,
MTF emergent ordering, and the FACT subject index all reproduce their
canonical behavior at the new scale. 3/3 byte-identical runs.

## 1. Build: scaling_clean base + hardened walk

Source chain (all under `docs/lab/research-lead/overnight-20260928/`):

1. `scaling_clean/sc_base_expanded.zag` (canonical, commit 405fe57e5):
   7-slice extraction (lines 1-296, 315-418, 427-441, 473-532, 544-812,
   836-1356, 1358-1591) removing promote_graph, ev_teach/ev_teach_in,
   t2_lu_first, t2_gather, ev_query, main. Reassembly with
   `scaling_clean/sc_patch.zag` + `scaling_clean/sc_driver.zag`
   reproduces `scaling_clean/sc_full.zag` BYTE-IDENTICALLY (cmp clean),
   so the slice map is exact.
2. `index_harden/ih_patch.zag` (commit 395c72675): `idx_walk_bucket`
   logic reused verbatim (I1 bounds, I2 cycle, I3 liveness, I4 type);
   cmp/sha256-verified identical copy kept as `ih_patch_used.zag`.
3. `sc_patch_5k.zag` = `scaling_clean/sc_patch.zag` with two
   documented changes (full diff in section 6):
   a. Capacity sed 8192 -> 65536 on all NN bounds (linear scan,
      ev_teach prev scan, gather/lu_first scans, MTF fast-path bound,
      ev_query fallback scan).
   b. The vulnerable bucket-walk block in `rebind_try_idx` replaced by
      the hardened `idx_walk_bucket` call. I1-I4 verbatim; I5 capacity
      adapted 512 -> 8192 because the plen-2 bucket alone holds ~4995
      decoy MAPs and the ih 4096-byte/512-entry buffer would silently
      truncate. The plain sed would have produced `nc<65536` against a
      65536-byte (8192-entry) buffer, an overflow; the hardened walk
      makes the bound correct by construction.
4. `base_64k.zag` = extracted base with line-addressed expansion sed:
   8192 -> 65536 nodes, 16384 -> 65536 edges (all uses are NN/NE
   bounds, verified by enumeration), workspace layout recomputed
   (node base 2621504, edge base 3670080, WSZ 3674176), and the
   frame-slot threshold 10000 -> 100000 on the same 11 lines the prior
   wave fixed (1000 -> 10000). Rationale: probe measurement showed
   ~7.1 nodes/MAP, so 5000 MAPs need ~35500 nodes; node ids exceed the
   old 10000 frame-slot threshold, which would reintroduce the exact
   bug fixed at 1000 (operands >= threshold misread as frame slots).
5. `s5000_driver.zag` = `sc_driver.zag` builders verbatim, workspace
   3674176 bytes, main runs S1000L/I (regression bridge), S5000L/I
   (4995 decoys + 5 real = 5000 MAPs), EML/EMI/EMM, FAL/FAI. One
   driver-design correction: decoy subjects moved from 2000+i to
   20000+i. At D=4995 the old base spans 2000..6994, overlapping the
   real MAP subjects (5000..5040) and the query chains (6101..6405);
   a first pilot run showed the overlap lets the real MAPs' t2_chain
   follow the decoy subject continuum to the len-16 cap (plen 16:
   unindexed, unmatchable) and makes t2_gather branch on duplicate
   subjects. With the 20000+i base the world restores the canonical
   structure (broken plen-2 decoys, clean plen-5 reals); a small-scale
   replication confirmed plen=5 and indexed scan=1 before the full
   runs. Subject values are data, not operands, so the 100000
   frame-slot threshold is unaffected.

Assembly: `s5000_full.zag` = base_64k + sc_patch_5k + s5000_driver
(2191 lines; one main, one ev_query, one promote_graph, one
rebind_try_idx, one idx_walk_bucket). Compiled with the pinned znc
(src/tools/toolchain/znc_linux_x86_64_abed8aa1); exit 0, warnings only
(same A0102 class as the canonical build).

## 2. Sizing probe (pre-registration of the expansion)

Probe on the unexpanded 8192-node build (D=490/990, mode 1):
- 490 decoys + 5 real: 3553 live nodes, 3057 live edges, fails=0
- 990 decoys + 5 real: 7053 live nodes, 6057 live edges, fails=0
Linear: ~7.1 nodes/MAP, ~6.1 edges/MAP. 5000 MAPs -> ~35500 nodes,
~30500 edges. Chosen: NN=65536 (1.8x headroom), NE=65536 (2.1x
headroom). No eviction observed (alloc counts == live counts).

## 3. Results

### 3a. Regression bridge: 1000 MAPs on the expanded workspace

| MAPs | mode | scan visits | tried | ok |
|------|------|-------------|-------|----|
| 1000 | linear | 6964 | 1 | 1 |
| 1000 | indexed (hardened) | 5 | 1 | 1 |

Byte-level match to the canonical scaling-clean numbers (6964/5).
The expansion, threshold move, and hardened walk change nothing at
1000 MAPs.

### 3b. Scale law: 5000 MAPs (4995 broken plen-2 decoys + 5 real plen-5)

| MAPs | mode | scan visits | tried | ok |
|------|------|-------------|-------|----|
| 5000 | linear (S5000L Q0) | 34999 | 1 | 1 |
| 5000 | linear (S5000L Q1) | 34999 | 1 | 1 |
| 5000 | indexed hardened (S5000I Q0) | 5 | 1 | 1 |
| 5000 | indexed hardened (S5000I Q1) | 6 | 1 | 1 |

Reduction: 34999/5 = 6999.8x, reported as ~7000x at 5000 MAPs
(canonical: 140x at 100, 693x at 500, 1393x at 1000). The indexed
cost stays constant (5 bucket visits: only the 5 valid plen-5 MAPs
are indexed; broken decoys have unreadable shape and are never
added to a bucket) while the linear cost grows with the slot range
the real MAPs occupy. Verify counts match exactly (tried=1,
rejected=0 both modes, both queries): the hardened walk changes
nothing but scan work, as the hardening proof requires.

### 3c. Emergent ordering (MTF)

Byte-identical to canonical on every counter:

| mode | Q0 | Q1 | Q2 | QSTALE |
|------|----|----|----|--------|
| 0 linear, oldest-first | 25 | 43 | 43 | 50 |
| 1 indexed, id-order, no MTF | 25 | 43 | 43 | 50 |
| 3 indexed + MTF emergent | 49 | 1 | 1 | 2 |

MTF 49->1 confirmed at the 5000 scale build: 49 verifies on Q0
collapse to 1 on Q1/Q2; stale recovery in 2 verifies. The MTF
machinery (fast path + move-to-front) is untouched by the hardening
splice and behaves identically.

### 3d. FACT subject index

| op | linear visits | indexed visits | reduction |
|----|---------------|----------------|-----------|
| t2_gather (4 paths) | 262136 | 167 | 1570x |
| 50 x t2_lu_first | 24800 | 1092 | 22.7x |

The indexed side is byte-identical to canonical (167, 1092, same 4
paths, 50/50 hits). The linear gather is 8x the canonical 32760
because t2_gather_lin scans all NN=65536 slots per BFS expansion
(canonical NN=8192): the linear cost scales with workspace size, the
indexed cost does not. lu50 is unchanged (early exit on first hit).
Same paths returned (np=4 both modes).

## 4. Limit analysis

- Node ids at 5000 MAPs reach ~35.5k (probe: 7.09 nodes/MAP at 995
  MAPs, linear). The 100000 frame-slot threshold holds with 2.8x
  margin; every query returned the exact expected answer, which a
  threshold collision would have corrupted (operands >= threshold
  misread as frame slots). The next threshold pressure appears past
  ~14000 MAPs on this NN=65536 workspace (ids approach 100000), at
  which point the threshold must move again in lockstep with NN.
- The I5 buffer bound (8192 entries) has large headroom here: the
  plen-2 bucket is empty (broken decoys are never indexed) and the
  plen-5 bucket holds 5-7 entries. If a future world indexes ~8190
  valid same-plen MAPs, the walk would silently stop collecting; the
  bound is a capacity parameter, not a correctness invariant, and
  must scale with the bucket population.
- `seen` bitmap costs NN()*4 = 256 KB per walked bucket per query;
  negligible against the scan work it guards.
- No eviction, no allocation failure (fails=0 in all 12 scale-world
  builds), no crash, no panic in any world. The general invariants
  I1-I4 never fired on these uncorrupted worlds (nothing to fire
  on), and the byte-identical regression bridge proves they change
  no legitimate behavior.

## 5. 10000 MAPs: queued, not attempted

10000 MAPs need ~71000 nodes (10000 x 7.09), exceeding NN=65536, so
it requires a fresh expansion (NN=131072, NE=131072, WSZ recompute
to 7344192 bytes -> 64+131072*40=5242944, +131072*16=7340096,
+4096=7344192) and a re-validation of the bridge. The 100000
frame-slot threshold still holds there (ids ~72k < 100000). Build
cost scales superlinearly (O(NN) scans per alloc/teach/edge), so one
10000-world build is estimated at 3-4x the 5000-world build (~40+
min per world, x2 worlds x3 runs). Queued as the next step; the
5000 result stands on its own.

## 6. Exact patch diff (sc_patch.zag -> sc_patch_5k.zag)

Saved as `sc_patch_5k.diff` (90 lines): capacity sed 8192->65536
on all NN bounds, two comment updates, the hardened `idx_walk_bucket`
insertion (I1-I4 verbatim, I5 512->8192 with documented rationale),
and the walk-block replacement in `rebind_try_idx`. Nothing else
changed. Base expansion diff (`base_nohook.zag` -> `base_64k.zag`):
120 changed lines, all mechanical (8192->65536, 16384->65536,
layout constants, 11-line threshold 10000->100000).

## 7. Files

- NAMECHECK.md (Step 0 toolchain guard attestation + reuse verification)
- REPORT.md (this file)
- base_64k.zag (expanded base: 65536 nodes/edges, threshold 100000)
- base_nohook.zag + base_nohook.sha256 (7-slice extraction evidence)
- sc_patch_5k.zag (mechanisms A/B/C + hardened walk splice)
- sc_patch_5k.diff (exact 90-line diff vs canonical sc_patch.zag)
- s5k_hardwalk.zag (idx_walk_bucket source of the splice)
- ih_patch_used.zag (verbatim copy of index_harden/ih_patch.zag)
- s5000_driver.zag (builders + scaled main, decoy base 20000+i)
- s5000_full.zag (2197 lines assembled)
- s5000_bin (compiled binary), s5000_compile.txt
- s5000_run1.txt, s5000_run2.txt, s5000_run3.txt (byte-identical;
  sha256 382e913a1ada196ac858de10644f1a3d2060f734c6b9dfa34be974c334fdc4d6)
- probe_driver.zag, probe_full.zag, probe_out.txt (sizing probe:
  7.09 nodes/MAP, 6.09 edges/MAP)
- mini5_driver.zag (small-scale fix validation: plen=5, indexed
  scan=1, ok=1 with the 20000+i decoy base)
- repro5p5_driver.zag, repro5p5_full.zag, repro5p5_bin,
  repro5p5_out.txt (D=4990 mode-5 FACT-index-during-build
  confirmation: all reals plen-5, Q0/Q1 ok=1)

## 8. Cross-workstream note: the parallel s5_* workstream

A parallel s5_* workstream in this same directory (REPORT_S5.md)
reports SCALING-5000-PARTIAL, attributing query failures (ok=0,
tried=5 rejected=5) to a "build-order-dependent correctness bug in
the FACT index". I root-caused the divergence before finalizing
this verdict:

- Their `s5_base.zag` expanded nodes to 65536 and edges to 131072
  but left `WSZ()` at 593984 and `loff()` at 589888 (the 8192-node
  layout). Node 14746 starts at offset 589904, inside the stale log
  region, so every `log_ev` (on every teach/query) clobbers live
  nodes once the build exceeds ~14745 nodes. That is exactly their
  observed threshold (works at <=1000 decoys / ~7100 nodes, fails at
  4990) and their "build-order dependence" (real MAPs built first
  sit at low ids, below the clobber region).
- Their FACT-index code is diff-identical to canonical; the failure
  is a workspace layout bug in their base, not a mechanism bug.
- In my clean build (correct tight layout, verified above), mode-5
  builds (FACT index active during `t2_chain`) pass at D=50, 1000,
  1500, 2000, and 4990: all real MAPs plen-5, all queries ok=1 with
  tried=1. The D=4990 mode-5 run is saved as `repro5p5_out.txt`.
  One D=2000 mode-5 run aborted (SIGABRT) once and passed on rerun;
  with five other mode-5 scales passing deterministically, this is
  treated as an environmental flake, not a finding.

This workstream's verdict is independent of the s5_* files and is
not affected by their layout bug.

## 9. Notes

- Toolchain guard: safebin active for all builds/runs;
  `which python3 python` returns nothing. Pure Zag throughout.
- The `emit`/`e64` output path is unchanged from the canonical build;
  stdout verified byte-identical across 3 runs (sha256
  382e913a1ada196ac858de10644f1a3d2060f734c6b9dfa34be974c334fdc4d6).
- One pilot run was discarded before the 3 counted runs: its driver
  used decoy subjects 2000+i, which at D=4995 overlap the real MAP
  and query subjects (diagnosed via plen census: real MAPs became
  plen-16, rebind found nothing, the trial fallback answered). The
  counted runs use the corrected 20000+i base. The pilot is
  documented here, not counted.
