# REPORT: XIO DEP-Hygiene Repair (fresh experiment, 2026-10-02)

Date: 2026-10-02
Worker: TNN research revival worker (watchdog-assigned)
Variant: UNFROZEN (unfrozen xio core only; frozen base byte-untouched)
Verdict: XIO-DEPHYGIENE-COMPLETE (BUILD-PASS, kill bars K1-K10 all hold)

## Summary

Both A4c residuals left open by canonical XIO-IDFIX are repaired on
the real XIO substrate. Post-recycle xio_dep_rel returns the new
occupant's relation (82) instead of the stale occupant's (81), through
the hygiene-aware delete path (tombstone layer) and through the raw
delete path that simulates missed hygiene (graph-target filter
layer). A masked trial that teaches a fact contradicting
adapter-verified knowledge is refused and superseded
(XIO-MASKED-REFUSED), never installed: the follow-up unmasked query
returns the true revised answer (3), not the poisoned fact (70), and
the poison census is zero. Legitimate learning is intact (unmasked
teach/activate/query; corroborating and novel masked teachings
unaffected). The C229 and C235 batteries are 3/3 byte-identical to
their committed baselines. All binaries are 3/3 byte-identical.

## What was built

Repair source: src/dephygiene_core.zag (the XIO-IDFIX core,
xio_idfix/idfix_full.zag lines 1678-1960, plus the changes below;
audited by diff, saved in outputs/core_diff.txt: additive except the
xio_dep_rel filter strengthening and the xio_query masked-trial
audit; no other function touched, no signature changes).

- L_TOMB: xio_tomb_edges marks every type-1 DEP edge sourced at a
  deleted MAP as tombstoned (from=-2; never recycled, never matched).
  xio_del_map_rh is the hygiene-aware delete (tombstone, then
  deactivate).
- L_LIVE: xio_dep_rel returns -1 unless the MAP id is live
  (field36==1, tag==20).
- L_GRAPH: xio_dep_rel follows a type-1 DEP edge only if its target
  fact is referenced by the MAP's own executable graph (collected by
  walking the graph with the xio_oty traversal pattern). Stale edges
  from a deleted previous occupant point at the old occupant's
  licensing facts, which the new occupant's graph never references, so
  recycling cannot shadow the new occupant regardless of edge-id
  reuse. Graphs that reference no facts (pure INC chains) keep the
  original behavior.
- Masked-trial protection: on masked queries, xio_query snapshots the
  adapter-verified answers for the query relation and the live (s,r)
  facts BEFORE the trial section, then xio_masked_audit supersedes
  (type-3 self-edge, respected by frozen activate) every newly taught
  fact that contradicts the snapshot, emitting XIO-MASKED-REFUSED.
  The snapshot precedes the trials because an invalidated adapter's
  node id can be recycled by the trial itself (observed in the
  pre-prereg probe), which would destroy the record the audit needs.

No new modes, bridges, handlers, protected-core operations, edge
types, or node types. The snapshot/audit state is data and control
flow, not a mode.

## Kill-bar results (all frozen in PREREG.md, commit c8c811a73)

| Bar | Requirement | Observed | Result |
|-----|-------------|----------|--------|
| K1 | H0 dep_rel(dead m1)==-1 | -1 (idfix core: 81) | PASS |
| K2 | H1 tombstone: t1 from==m1 3->0, tombstoned>=1, dep_rel==82, nm==m1 | 3->0, 6 tombstoned, 82, nm=27 reused | PASS |
| K3 | H2 raw delete: stale t1>=1 (untombstoned), dep_rel==82 | 3 stale, 82 via graph filter | PASS |
| K4 | H3: REFUSED s=31 r=93 ans=70; superseded==1; qm==70 | all observed (fact 436) | PASS |
| K5 | H4: qu==3; poison census==0 | 3; 0 (idfix: 70, poisoned) | PASS |
| K6 | H5a 14,14; H5b vc==1, contra 0/1/0 | all observed | PASS |
| K7 | dephy_c229 3/3 byte-identical to committed xio_run1.txt | sha256 3b10e33e... x3 | PASS |
| K8 | dephy_c235 3/3 byte-identical to committed xhio_run1.txt | sha256 6909ba0c... x3 | PASS |
| K9 | every binary 3/3 byte-identical | dephy_full 94e214d3... x3 | PASS |
| K10 | base intact; 0 modes/bridges/handlers; pure Zag | cmp OK; grep 0 hits; guard clean | PASS |

Control baseline (committed, not rebuilt): XIO-IDFIX T1
(xio_idfix/idfix_run1.txt, commit e4b25c110) shows live-deprel=81,
masked-via-adapter=70, unmasked-true=70. Treatment shows 82,
REFUSED+superseded, 3.

## Ablation reading (observed, matches prereg)

Each layer's unique contribution is visible. Tombstone clears the
hygiene path (H1: stale edges gone, dep_rel correct). The graph
filter covers the missed-hygiene path where tombstoning never ran
(H2: 3 stale edges still sourced at m1, yet dep_rel correct because
their targets are not in the new occupant's graph). Liveness covers
the dead slot (H0: -1 where the old code served 81). The masked audit
covers the poisoning the DEP layers cannot see (H3/H4: contradiction
refused and superseded; corroborating and novel teachings pass
through, H5b/H6).

## Provenance

- Freeze commit: c8c811a73 (PREREG.md + NAMECHECK.md Step 0 only,
  committed alone before any implementation existed). No prereg edits
  after the freeze.
- Repair source: src/dephygiene_core.zag
  (sha256 f873bd70343021a58f92e330b7c4043ac4e233f7887c8ee92131b6b7900c6c13)
- Driver: src/dephy_driver.zag
  (sha256 e8c98245900a536ee1a91af6e55b5cddcb27a9e0e435df3d6cea2cd4565bf885)
- Assemblies: dephy_full.zag (4b0e1ed3...), dephy_c229.zag
  (51b397c4...), dephy_c235.zag (37cfa31b...)
- Binaries: bin/dephy_full (b4a52f05...), bin/dephy_c229
  (b1371eff...), bin/dephy_c235 (003f57d5...)
- Run logs: outputs/dephy_{full,c229,c235}.run{1,2,3}.log (stdout,
  byte-exact), .err files (all empty), runs.exitcodes (all 0),
  sha256sums.txt, sources_bins.sha256, core_diff.txt
- Harness: build.sh, run.sh, verify.sh (shell only)
- Full checksums: outputs/sources_bins.sha256

## Constraint compliance

- Pure Zag: all research logic in Zag, compiled by the pinned znc
  (2026.07.0-dev) via safebin. Toolchain guard (NAMECHECK.md Step 0)
  clean before any work and re-verified after the prereg write:
  `which python3 python` returns empty. No Python invoked at any step.
- Unfrozen xio core only; frozen base (xio_full.zag lines 1-1677)
  extracted per assembly and cmp-verified byte-identical, never
  edited. Original C229/C235 drivers used verbatim (boundary-checked
  at assembly).
- Paper untouched. composition_integration/ untouched. Nothing pushed
  (commits local only).
- Zero new modes/bridges/handlers (grep audit: 0 hits). Zero new
  protected-core operations, edge types, or node types.
- No em or en dashes in deliverable documentation (audited).
- Compiler lessons honored: no `as *i32` plus slice construction; no
  new dynamic _zag_print (frozen emit/e64 used verbatim); no
  `!(... && ...)` in while conditions (grep-audited); if-nesting at 3
  or fewer in new code.

## Design note (honest)

The fresh design differs from the exploratory pass in two places,
both forced by pre-prereg probes (disclosed in PREREG.md section
10, /tmp only, not evidence): (1) the graph-target filter replaced
an edge-id-ordering sketch after the probe showed frozen decay and
eviction free edges, so id ordering cannot soundly discriminate stale
from current edges; (2) the masked audit snapshots verified answers
before the trials after the probe showed an invalidated adapter's
node id can be recycled by the trial itself. The exploratory
binaries and runs were not trusted and count for nothing.

## Limitations (honest)

- The repair targets the XIO-IDFIX core lineage (xio_adapters
  pipeline). The separately committed XIO-GENERAL core
  (xio_general/xio_core2.zag) is a different fork and is out of
  scope; unifying the forks is an architecture decision for the
  parent.
- L_GRAPH falls back to the original behavior for graphs that
  reference no facts (pure INC chains, e.g. t2_asm_sum); no sum MAPs
  appear in the tested worlds.
- The masked-audit snapshot covers adapters present at query time; an
  adapter invalidated AND recycled by an earlier query leaves no
  record (pre-existing idfix node-recycling behavior).
- The fixture replicates the A4c incident shape (delete, recycle,
  masked trial); it is not a fresh adversarial world. An independent
  red team against the repaired core is recommended follow-up.

## Recommended follow-ups (for the parent, not started)

- Independent red team against the repaired core (fresh adversarial
  worlds, not the A4c fixture): especially the exotic variant where a
  previous occupant is promoted late (high edge ids), low slots are
  freed by decay, and the new occupant lands low.
- Port assessment for the xio_general fork (separate architecture
  decision).
- Longer delete/reuse chains and larger edge tables; check tombstone
  sweep cost stays sublinear.
