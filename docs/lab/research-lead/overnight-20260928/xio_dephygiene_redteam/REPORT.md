# REPORT: Red Team vs XIO-DEPHYGIENE (2026-10-02)

Worker: TNN red-team worker (watchdog-assigned; resumed parked task,
replacement for a completed worker)
Lane: docs/lab/research-lead/overnight-20260928/xio_dephygiene_redteam/
Target: XIO-DEPHYGIENE PASS (ledger C308, results commit 5318cbfc9,
verdict XIO-DEPHYGIENE-COMPLETE)
Prereg: PREREG.md frozen 2459e2d2f, Amendments 1 (a16574382),
2 (c158342e3), 3 (6a8a7bc43). No bar was weakened by any amendment.
Branch at report time: lane-tnn3-20261002-1421pdt (swarm moved the
working branch; the full prereg chain is in-history). Commits local
only, never pushed.

## Verdict summary (per attack, frozen bars)

| Attack | Verdict | Tracer cross-check | Runs |
|---|---|---|---|
| A1 late-promotion + decay + low-recycle | ATTACK-FAILED | trace 82 == real 82 | 3/3 byte-identical, sha256 d03f730b... |
| A2 fact-less fallback boundary | ATTACK-SUCCEEDED (CONFIRMED kill) | trace 81 == real 81 | 3/3 byte-identical, sha256 d03f730b... |
| A3 adversarial id reuse (live-but-wrong) | ATTACK-SUCCEEDED (CONFIRMED kill) | trace 94 == real 94 | 3/3 byte-identical, sha256 d03f730b... |
| A3 control (perfect hygiene) | PASS (tombstone -> 82) | trace 82 == real 82 | 3/3 byte-identical |

No new breaks were found beyond the two preregistered kills. No
attack went VOID under the amended construction. No crash, panic, or
forbidden-executable invocation occurred in any run.

## A1: ATTACK-FAILED (the graph filter held)

Measurements (amended construction, Amendment 3): m1=227 (filler
shifted, recorded); STALE(227) = 3 edges, ids 224..226 (high, as
designed); F1/F2/F3 = 202/203/204; recycle verification passed
(202 203 204); nm=227 (first-fit recycle of the deleted MAP node);
CUR(227) = 7 edges, ids 9..241. The stale targets (nodes 202..204)
were live r=82 facts referenced by the new count graph (gn=7), so the
graph filter's premise was genuinely violated for them, exactly the
threat geometry preregistered. The id-order scan met edge 9 (CUR,
to=203, trel=82) before any stale edge: trace_rel=82, real_rel=82,
followed edge class CUR. Per the frozen bar (SUCCEEDS iff followed
edge in STALE or relation != 82): ATTACK-FAILED.

Honest note on margin: the CUR range (9..241) interleaves with the
stale range (224..226); the filter was saved because the lowest-id
candidate edge was current. The outcome hinged on edge-id order,
which is the repair's known-fragile premise (allocation is not
append-only, C308 probe 2). A1 as constructed did not break the
filter, but A3 shows what happens when a stale edge wins the id race.

## A2: ATTACK-SUCCEEDED (CONFIRMED kill of the repair)

Measurements: old chain MAP X=17 (provenance X->F1,F2,F3, r=81 facts,
low edge ids); sum graph built (t2_asm_sum writes no type-1 cell
edges, gn=0 confirmed); summand facts G1,G2 taught BEFORE the raw
delete per Amendment 1; raw delete X; promote sum MAP at nm=17
(first-fit recycle, as required); new occupant field4=82 with
MAP-level provenance X->G1,G2 (2 CUR edges, high ids). The gn==0
fallback kept the original first-live-fact behavior and followed
stale edge 13 (to=F1, live, r=81): trace_rel=81, real_rel=81,
followed edge class STALE. Per the frozen bar (SUCCEEDS iff dr==81):
ATTACK-SUCCEEDED. The tracer replicated the real return exactly, so
the kill is scored, not void.

What this breaks: the C308 repair's claim that the L_GRAPH filter
plus tombstones handle id recycling. The gn==0 fallback path has no
graph to filter against, so a raw-deleted occupant's stale low-id
provenance shadows the new occupant. This configuration is reachable
in real operation (t2_trial promotes sum MAPs WITH licensing facts),
not just constructible, so the unreachability escape bar does not
apply.

## A3: ATTACK-SUCCEEDED (CONFIRMED kill of the repair)

Measurements: m1=27; STALE(27) = 3 edges, ids 16..18 (low, K2
pattern); F1=node 2 deactivated; wrong fact (99,94,100) recycled
node 2 (verified); count graph built referencing F1 last (gn=7);
raw delete; promote at nm=27 (verified); CUR(27) = 7 edges, high
ids. The stale edge 16 (27->F1) now points at a LIVE fact with
r=94, referenced by the new occupant's graph, so the L_GRAPH filter
follows it: trace_rel=94, real_rel=94, followed edge class STALE,
target relation 94 != 82. Per the frozen bar (SUCCEEDS iff followed
edge in STALE AND target relation != 82): ATTACK-SUCCEEDED. Tracer
matched the real return exactly.

Control (same world, xio_tomb_edges applied right after the raw
delete): dep_rel=82, followed edge 255 = CUR. A3-CONTROL PASS. The
stale edge is NECESSARY for the wrong answer, which rules out
fixture artifacts as the cause.

What this breaks: the repair's core invariant. The stale and current
edges are content-identical (from, type, to, clk all equal); the
stale target is live and graph-referenced; only tombstone hygiene
(which the attack assumes missed) distinguishes them.

## Amendment 3 (transparent, committed 6a8a7bc43 before the amended
binary was built)

The frozen A1 and A3 step orders are mechanically unbuildable:
alloc_node is first-fit over field36==0, so each construction's
intermediate allocations consume the freed target MAP node before
the final promote_graph, and the require-nm==M step can never hold.
Demonstrated: the first attack binary (frozen A1 order) printed
nm=622, VOID nm!=m1, while the recycle verification passed; a probe
of the frozen A3 order printed nm=421, VOID nm!=m1, with node 27
holding a live tag-1 fact after the count-graph build (a step-5 fact
teach consumed it). The amended order moves each attack's raw delete
(missed hygiene) to immediately before its promote_graph call. Every
step's content is unchanged; stale sets are recorded at the same
point; decay still precedes provenance-edge writes; deactivation
still precedes re-teaching; the missed-hygiene condition is
unchanged. The verdict bars are unchanged. The frozen-order VOIDs are
preserved here as evidence, not scored.

## Guard for A2: field4-constrained gn==0 fallback (core)

Minimal guard, in xio_dep_rel (src/rt_core_g2.zag, +23/-9 lines vs
the stock core): in the gn==0 fallback branch, follow a type-1 edge
only if its target fact's relation equals the MAP's own promotion
relation (field4). field4 is zeroed by alloc_node on recycle and
written fresh by promote_graph, so it cannot be stale. Flat
flag-hoisted form (nesting <= 2) per the compiler-defect workaround;
no new modes, bridges, or handlers; pure Zag.

- G1: the A2 world rebuilt with the guard: trace_rel=82,
  real_rel=82, followed edge 93 = CUR (to=89, trel=82, gn=0); the
  stale r=81 edges are skipped. A2 VERDICT ATTACK-FAILED. Guarded
  tracer cross-check passed. 3/3 byte-identical, sha256 331f08f9...
  (A1 still ATTACK-FAILED; A3 still ATTACK-SUCCEEDED, confirming the
  guard is specific to the fallback path; A3 control still PASS.)
- G2: dephy_full / dephy_c229 / dephy_c235 rerun against the guarded
  core, 3/3 each: sha256 94e214d3... / 3b10e33e... / 6909ba0c...,
  byte-identical to the committed C308 baselines. K1-K6 predictions
  reproduced exactly; K9 holds.
- G3 (no overreach): the byte-identity above is the empirical check.
  Principled soundness: on every honest world the guard is a no-op
  for gn>0 paths and for gn==0 paths whose licensing facts match the
  MAP's relation (the t2_trial norm). Documented refinement (not
  preservation): an honest sum MAP with mixed-relation summand facts
  (t2_gather_sum collects ANY relation) now resolves its input
  relation to the MAP's own promotion relation instead of the
  first-live-fact's relation. This aligns the stage with the query
  relation it was promoted for and fails closed (-1) when no
  r-matching provenance exists, but it is a behavior change for that
  honest corner, stated here so it is not mistaken for a pure
  no-op.

## Guard for A3: tombstone-on-recycle in promote_graph (source-side)

Minimal guard, in promote_graph (src/rt_base_g3.zag): after
alloc_node and before any new edge is written, sweep type-1 edges
with from==m to from==-2. Rationale (preregistered): stale and fresh
provenance are content-identical and no id-ordering rule is sound, so
stale provenance must die at recycle time; the sweep is a no-op on
fresh nodes and on hygiene-deleted nodes (already -2). +16 lines,
additive hunk only: the guard-variant base differs from the frozen
base (sha256 dc0e86d4...) by this hunk alone (verified by diff, saved
in outputs/base_g3.diff). No new modes, bridges, or handlers; pure
Zag. DEPLOYMENT FLAG: this guard changes the frozen base's
promote_graph, which frozen t2_trial calls directly, so deploying it
is a parent architecture decision; it is demonstrated, not deployed,
in this lane.

- G1: the A3 world rebuilt with the guard: trace_rel=82,
  real_rel=82, followed edge 255 = CUR. A3 VERDICT ATTACK-FAILED.
  3/3 byte-identical, sha256 de842b21... As a side effect the guard
  also defeats A2 (stale edges tombstoned at promote; A2 followed
  edge 93 = CUR, dr=82), which is expected: recycle-time tombstoning
  subsumes the fallback-path symptom. A1 still ATTACK-FAILED; A3
  control still PASS.
- G2: dephy_full / dephy_c229 / dephy_c235 rerun against
  guard-base + stock core, 3/3 each: sha256 94e214d3... /
  3b10e33e... / 6909ba0c..., byte-identical to the committed C308
  baselines. K1-K6 predictions reproduced exactly; K9 holds.
- G3 (no overreach): byte-identity above is the empirical check.
  Principled soundness: the sweep only touches type-1 edges already
  sourced at the just-allocated node, which by construction belong to
  a previous occupant (a new node has none; a hygiene-deleted node
  has them at -2 already); honest re-promotion (e.g. K2/H1's nm==27
  reuse after tombstone+delete) is unaffected because there is
  nothing left to sweep.

## K10-analogous checks (both guards)

Pure Zag under safebin (Step 0 verified this session; which python3 /
which python return nothing; no forbidden executable invoked in any
build or run). 0 new modes/bridges/handlers (grep clean on all guard
sources). Frozen base byte-identical for the A2 guard; for the A3
guard the base diff is exactly the documented additive hunk.
Compiler-defect workarounds honored in all new Zag (no `as *i32` +
slice construction in functions, no _zag_print for dynamic content,
no `!(... && ...)` in while conditions per grep audit, if-nesting <=
3, 2-byte discipline N/A).

## Build and run ledger

- Pinned compiler: src/tools/toolchain/znc_linux_x86_64_abed8aa1
  via $HOME/safebin/znc.
- Unguarded attacks: build_rt.sh (base dc0e86d4... + core f873bd70...
  verified) -> bin/rt_a123; 3/3 runs byte-identical, d03f730b....
- G1 A2-guard: bin/rt_a123_g2 (base + core_g2 + guarded tracer
  driver); 3/3 byte-identical, 331f08f9....
- G1 A3-guard: bin/rt_a123_g3 (base_g3 + stock core + stock attack
  driver; stock tracer still faithful, xio_dep_rel unchanged); 3/3
  byte-identical, de842b21....
- G2 arms: 6 binaries (dephy_full/c229/c235 x g2/g3), 3/3 runs each,
  all byte-identical to committed C308 baselines (hashes above).
- All sources, assemblies, binaries, diffs, compile logs, and run
  logs are in this lane (src/, outputs/, bin/); sha256 recorded in
  outputs/rt_sources_bins.sha256 and outputs/guards_bins.sha256.

## Cognition lines touched

New Zag written for this red team: src/rt_attack.zag (344 lines:
A1/A2/A3 drivers, faithful tracer, copied A4c fixtures);
src/rt_attack_g2.zag (guarded tracer variant, 38 changed lines);
src/rt_core_g2.zag (A2 guard, +23/-9 vs stock core);
src/rt_base_g3.zag (A3 guard, +16 vs frozen base). No other cognition
lines added; no existing behavior altered except through the two
documented guard hunks.

## Bottom line for the research director

Two CONFIRMED kills against the committed XIO-DEPHYGIENE repair, both
with exact tracer/real cross-checks and 3/3 deterministic runs:

1. A2: the gn==0 fallback (kept as "original first-live-fact
   behavior" for fact-less sum graphs) follows a raw-deleted
   occupant's stale low-id provenance and returns the OLD relation
   (81), shadowing the new occupant (82). Reachable via the frozen
   t2_trial sum path, not just constructible.
2. A3: a stale provenance edge whose target was recycled into a
   live-but-wrong fact (r=94) passes the L_GRAPH filter (the target
   is live and graph-referenced) and returns 94 instead of 82. The
   control proves the stale edge is necessary for the wrong answer.

A1 did not break the filter (id order saved it), but the margin was
id-order luck, and A3 is the same threat winning the id race.

Both kills have minimal guards demonstrated in-lane with G1 (attack
fails), G2 (C308 K1-K10 byte-identical), and G3 (no overreach, with
one documented refinement for the A2 guard and a deployment flag for
the A3 guard, which touches the frozen base). Whether either guard is
promoted, and whether the A3 guard's base change is accepted, are
parent architecture decisions; nothing here weakens the C308 verdict
(XIO-DEPHYGIENE-COMPLETE stands for its K1-K10 bars) or claims the
repair is production-safe against missed hygiene.
