# XP-DAGFAN-1 VERDICT (orphan branch record)

Date recorded: 2026-10-03. Recorder: ORPHAN-EXECUTE (maintenance worker; claim minting paused).
Source branch: `lane-xdagfan-20261002` (tip `d9c0f9939`, local only, never pushed; worktree ~/workspace/tnn-dagfan).
Triage reference: `../orphan_triage/ORPHAN_TRIAGE.md` (DOCUMENT-THEN-DELETE, verdict previously captured nowhere).

## What this was

Experiment XP-DAGFAN-1: fan-out and fan-in composition beyond pipelines. The frozen composition operator xhier_compose (reused verbatim from frozen xhier_patch.zag, sha256 7ccde6e1...) was exercised on two scenarios beyond the pipeline case, with zero source changes. All identifiers opaque (relation numbers only); no domain labels. Directly relevant to overnight priority 1 (general DAG/fan-out/fan-in composition).

Lane files (10, all unique): `docs/lab/research-lead/overnight-20260928/xdagfan/` on the branch: NAMECHECK.md, PREREG.md, REPORT.md, xdagfan_bin, xdagfan_compile.txt, xdagfan_driver.zag, xdagfan_full.zag, xdagfan_run1.txt, xdagfan_run2.txt, xdagfan_run3.txt.

Governing prereg: `PREREG.md`, frozen alone at commit `7b685af35` before any implementation. Frozen predictions and kill bars K1-K10. No diamond handler was built, per the 2026-10-03 architectural clarification (cross-domain is not a mode; dependence on human domain identity is architectural failure).

## Scenarios tested

- Fan-out: one composite MAP_Z (Z1, id 254) consumed by two different higher composites (Z2a id 460, Z2b id 684). Composition graph: Z2a -> {X2a, Z1}, Z2b -> {X2b, Z1}, Z1 -> {t, MAP_Y}. Z1 has two consumers: a DAG, not a pipeline and not a tree.
- Fan-in: a query whose licensed answer requires combining two count contributors (2 + 3 = 5). Frozen prediction: the fixed-arity operator cannot express it (bound probe).

## Results

3/3 runs byte-identical (sha256 f18ae6b5810dc4b38113eaf1bbbabc854ad1dad8e6dbc2561d125a9a06b69e27). 55 PASS lines, 0 FAIL lines per run.

- H1 (fan-out main, 38/38): (20,94,3) -> 3, (30,95,3) -> 3. Trace: XHIER-COMPOSE ok nav=267 z=254 z2=460 and XHIER-COMPOSE ok nav=473 z=254 z2=684. The numerically identical Z1 id (254) is named by both composites: shared structure, not a second copy. Exactly 3 live MAP_Z; exactly 2 MAP_Z with LINK14->Z1 (the DAG signature); Z1 intact with exactly 2 LINK14 (->t, ->MAP_Y); Z2a and Z2b have no LINK14 to each other.
- H2 (pipeline controls, 6/6): the frozen single-level pipeline answers -2 on both level-2 queries and creates nothing: the level-2 answers come only from hierarchical composition.
- H3 (causal fan-out ablation, 8/8): after killing Z1 and the two cached answer facts, both (20,94,3) and (30,95,3) return -2 through the full pipeline (rebind rejected, xs5 fail, xhier fail). One ablation kills two consumers: the signature of shared structure rather than two independent pipelines. MAP_Z count stays 2; Z2a and Z2b stay live with edges intact but unusable.
- H4 (fan-in bound probe, 3/3): (60,98,5) -> -2 cleanly, no promotion, no crash, exactly as predicted. The fixed operator arity (one relseq slot plus one count slot, single MAP_Z verification) cannot express combining two count contributors.

## Kill bar disposition (K1-K10, all PASS)

- K1 REPLICATION: PASS. q1==2; Z1 LINK14->t and LINK14->MAP_Y; qx2a==22; q2a==3; Z2a LINK14->X2a and LINK14->Z1.
- K2 FAN-OUT CORRECT: PASS. q_b==3; Z2b (field4==95) exists; LINK14 Z2b->X2b; LINK14 Z2b->Z1-id (same 254); Z2b != Z2a; exactly 2 LINK14 out of Z2b.
- K3 DAG STRUCTURE: PASS. Exactly 3 live MAP_Z; 2 MAP_Z with LINK14->Z1; Z1 intact with exactly 2 LINK14; exactly one MAP_Z with LINK14->t; no LINK14 between Z2a and Z2b.
- K4 EXACT PIPELINE FAILS: PASS. H2 6/6.
- K5 FAN-IN BOUND: PASS. H4 3/3 (-2, no promotion, no crash).
- K6 CAUSAL FAN-OUT DEPENDENCE: PASS. H3 8/8.
- K7 DETERMINISM: PASS. 3/3 byte-identical whole-output runs.
- K8 HYGIENE: PASS. Zero em/en dash bytes in PREREG.md, NAMECHECK.md, REPORT.md (byte-verified).
- K9 FROZEN BASES: PASS. cc_base dc0e86d4..., un_patch 3e61056a..., xs5_patch 6e8c7a71..., xhier_patch 7ccde6e1... all match ledger; concatenation cmp-verified byte-identical to XP-HIER-1's frozen build block.
- K10 ARCHITECTURE ACCOUNTING: PASS. New code is driver-only (xdagfan_driver.zag, xd_ prefix); 0 new edge types, 0 new MAP types, 0 new opcodes, 0 new operators, 0 new executors, 0 new classifiers, 0 modes, 0 bridges, 0 handlers.

## Verdict

XP-DAGFAN-1-PASS. The frozen xhier_compose operator handles fan-out DAG composition with zero source changes; fan-in is an honest, cleanly predicted arity bound.

## Mechanism finding

Source-derived before execution, confirmed by the runs: fan-out works because xhier_compose treats the MAP_Z snapshot as read-only. xhier_try_pair only READS the named MAP_Z (navigates its relseq, aggregates at the endpoint); promote_graph allocates a NEW node and writes two LINK14 edges (to the relseq MAP, then to the MAP_Z). Nothing marks the shared MAP_Z consumed, retired, exclusive, or single-use. A second composition naming the same MAP_Z succeeds, producing a second composite that references the numerically identical id. The composition GRAPH is a DAG (shared substructure); each composition remains a binary pair (operator arity unchanged).

The fan-in bound is the same arity read the other way: exactly two LINK14 slots per composite (relseq MAP excluding MAP_Z; MAP_Z) and verification executing exactly one MAP_Z. A query needing two count contributors has no verifying pair.

## Two confounds found and neutralized (driver-only, kill bars unchanged)

1. Cached-answer confound (wave 1): promote_graph's ev_teach_in teaches exact answer facts, so post-ablation re-queries hit exact memory (activate) and return 3 without any composition. The driver now kills the two cached answer facts (ids 461, 685) alongside Z1; post-kill queries traverse the full pipeline (rebind rejected, xs5 fail, xhier fail) before returning -2. Check H3.0b records the fact kills. This is the same ablation intent as frozen K6, made clean.
2. Slot-recycling confound (wave 2): the frozen alloc_node recycles dead node slots (lowest id first), so Z1's slot 254 becomes live again (as a tag-30 node) during post-kill queries. A liveness check on the raw slot id is therefore the wrong ablation test; the correct check is structural: no live tag-20 MAP with field4==93 exists (xd_find_map_r(W,93)==-1). H3.4 uses this. The ablation itself is unaffected: Z1-as-MAP_Z is gone and no new MAP_Z is promoted.

## Honest bounds and open questions

- Fan-out demonstrated for exactly 2 consumers sharing 1 MAP_Z. 3/5/10+ consumers, deeper DAGs, and diamond re-convergence (A->B->D and A->C->D) are untested and explicitly future work.
- Fan-in bound confirmed for the 2-contributor case only; the general arity question (k contributors) is open.
- The fan-in failure is reported as a bound, not fixed. Per the architectural clarification it should trigger competing GENERAL composition hypotheses (for example: n-ary verification frames, multi-slot composites, recursive binary pairing), not a fan-in-specific handler. No such hypotheses are implemented here.
- Cycles and partial applicability are untested.
- Runtime: about 4 minutes per run under shared-machine load (load average above 11 during the runs); determinism held byte-identically across all three.

## Build and run record

- Frozen bases verified: cc_base dc0e86d4..., un_patch 3e61056a..., xs5_patch 6e8c7a71..., xhier_patch 7ccde6e1....
- Build: xdagfan_full.zag sha256 9b59bd588101c03ce2b8f606435323c64ed6b0b976ed94118fe94cc5b150538b, compiled with the pinned toolchain src/tools/toolchain/znc_linux_x86_64_abed8aa1, exit 0.
- Runs: xdagfan_run1.txt, xdagfan_run2.txt, xdagfan_run3.txt, all sha256 f18ae6b5810dc4b38113eaf1bbbabc854ad1dad8e6dbc2561d125a9a06b69e27.
- Dash hygiene: LC_ALL=C grep for U+2013/U+2014 returns 0 matches in PREREG.md, NAMECHECK.md, REPORT.md.

## Record status

This verdict was not in the canonical CLAIM_LEDGER.md (main ledger ends at C376) and not in any retained wave archive; it existed only on the orphan branch. Recorded here per the DOCUMENT-THEN-DELETE triage recommendation.
