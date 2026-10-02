# PREREG.md -- Scaling 5000 Rerun with Fixed FACT Index (s6_* workstream)

Frozen: 2026-10-02. This prereg is committed ALONE before any
implementation. Kill bars below govern the verdict. No bar may be
weakened after results are seen.

## 1. Question

Does the FI1-FI5 hardened FACT index (commit 11622ae25) resolve the
s5 build-order-dependent query failure at 5000 MAPs, while preserving
the measured 13,107x indexed reduction?

Background: the s5 run (`../scaling_5000/REPORT_S5.md`) measured
65,534 linear visits vs 5 indexed at 5000 MAPs, but all queries
failed (tried=5, rejected=5, ans=-2) when 4990 broken plen-2 decoys
were built BEFORE the 5 real plen-5 MAPs. The FACT index fix worker
hardened the FACT subject index with general invariants FI1-FI5, but
their fi_diag3 replication did NOT reproduce the s5 failure as FACT
index corruption. The fix may therefore NOT resolve the s5 failure.
This prereg treats that as a genuine empirical question.

## 2. Design

Base: `s6_base.zag` = lines 1..1495 of the committed s5_full.zag
(byte-verified extraction; the exact base behind the s5 measurements).

Patch: `s6_patch.zag` = s5_patch.zag with `fidx_add`,
`t2_lu_first_idx`, `t2_gather_idx` renamed to `*_orig` (dead code,
provenance only) and the FI1-FI5 hardened replacements from the
committed fi_fix.zag appended under the canonical names. Dispatch
functions (`t2_lu_first`, `t2_gather`) are unchanged and now route to
the hardened variants when mode bit2 is set. Zero new modes, bridges,
handlers, or semantic cases.

Driver: `s6_driver.zag`. Each run builds three independent worlds
(65536 nodes, 131072 edges), each with 8 query chains
(q=80000+qi*200, 4 facts each, rel 1), 4990 broken plen-2 decoys
(s0=2000+i, rel 51), and 5 real plen-5 MAPs (s0=50000+i*10, rel 51,
ans=50004+i*10). Build mode is 5 (MAP index + FACT index), as in s5.
The three worlds differ ONLY in build order:

- Order D (decoys-first): chains, 4990 decoys, 5 real. The original
  failing order.
- Order R (real-first): chains, 5 real, 4990 decoys.
- Order I (interleaved): chains, then 5 rounds of (998 decoys + 1 real).

Per world, after build:
1. Chain integrity: walk each of the 5 real MAP graphs from its root;
   expect alternating tag 102/101 cells with literals
   s0,s0+1,s0+1,s0+2,s0+2,s0+3,s0+3,s0+4. Emit ok flag per MAP.
   Diagnostic for failure localization (build-time vs query-time).
2. Mode 0 (linear): query chains 0,1. Record ans, tried, rejected,
   scan (header 56), fcnt.
3. Mode 1 (MAP index): query chains 2,3. Same counters.
4. Mode 3 (MAP index + MTF): query chains 4,5. Same counters.
   Chain 5 exercises the MTF winner-first path written by chain 4.
5. FACT gather: chain 6 in mode 1 (linear FACT path), chain 7 in
   mode 5 (indexed FACT path). fcnt measures FACT lookup visits.
   Fresh chains avoid the activate short-circuit; counters zeroed
   before every query.

Query form matches s5: ev_query(W,q,50,q+104,0); ok means ans==q+104.

## 3. Frozen kill bars

K1 BUILD-ORDER INVARIANCE (primary regression test): in ALL three
orders, every query in steps 2..5 returns ok=1. If any order fails,
the FACT fix did not resolve the s5 build-order bug.

K2 SCALE LAW PRESERVED: in ALL three orders, every mode-1 query has
scan (header 56) <= 32, and every mode-0 query has scan >= 60000.
Indexed-to-linear reduction >= 1000x per order.

K3 DETERMINISM: 3/3 runs byte-identical. sha256 of each full run
stdout must match across the three runs.

K4 ROBUSTNESS: zero panics, zero hangs, all runs complete; build
fails=0 in every world.

## 4. Verdict mapping

- K1..K4 all pass: SCALING-5000-FIXED-COMPLETE.
- K1 fails: SCALING-5000-FIXED-FAIL. The report will use the chain
  integrity flags to localize: chains corrupt means build-time
  corruption persists despite FI1-FI5; chains intact but queries fail
  means query/rebind-path corruption. No new mechanism may be built
  to rescue K1 in this wave.
- K2 fails: SCALING-5000-FIXED-FAIL (scale law broken by the fix).
- K3 fails: nondeterminism; rerun and investigate, no verdict until
  3/3 identical.
- K4 fails: report the crash/hang; verdict FAIL.

Reported but not kill bars: MTF tried/rejected on chains 4 vs 5,
FACT fcnt mode 1 vs mode 5, build-walks per order.

## 5. Constraints

Pure Zag via pinned znc under safebin PATH. `which python3 python`
returns nothing. Unfrozen files only; frozen tree read-only.
Paper untouched. Nothing pushed. Commits use explicit pathspecs under
scaling_5000_fixed/ only. Prereg committed alone before implementation.
