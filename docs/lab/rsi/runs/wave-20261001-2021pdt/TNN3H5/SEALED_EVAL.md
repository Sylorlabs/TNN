# SEALED EVALUATION: H5, wave-20261001-2021pdt

Adversary lane TNN3H5-ADVERSARY. Frozen binary tnn3_h5.bin verified by
SHA-256 before any run: 344ac89fb338ddbf46bea6be4c526d99410ea643278ab91fb06d76b7e33c4eb7
(matches the implementation record). Sealed worlds per SEALED_WORLDS.md,
designed post-freeze from the prereg family requirements. Each world was
compiled from a byte-copy of tnn3_h5.zag with only main replaced plus
appended driver (zero cognition lines changed, verified by diff), run 3
times, stdout hashed.

## Per-bar results

KB-W1 (white-box guide supersession, primary): PASS 8/8.
R1 final dump: 4 guide-class CON self-edges (guides on 51101-51104);
R2 final dump: 4 (guides on 51201/51207/51213/51229). Bar requires >= 6/8.
Hand-verified sample (R1 dump): nodes 4, 6, 8, 10 are tag 1 with
field24 == -999, each has a type-1 edge to a tag-30 node (4->2, 6->5,
8->7, 10->9; targets confirmed tag 30 with matching (s,r)), and each
carries a type-3 self-edge (E 4 3 4, E 6 3 6, E 8 3 8, E 10 3 10). The
never-resolved control guide (node 13, subject 51301) has no CON edge.
The falsifiable prediction does NOT fire: experience does write the CON
edges (8, not 0).

KB-W2 (white-box MAP supersession): PASS 8/8.
Per-probe MAP-CON delta (snapshot before first contradiction, recount
after final query): C1D1-D4 = 1,1,1,1; C2D1-D4 = 1,1,1,1. Bar requires
>= 6/8. Hand-verified: all six tag-20 MAP nodes in C1 (13, 30, 47, 64,
81, 98) and all six in C2 carry type-3 self-edges; the C1R1 MAP (node
81) shows DEP type-1 edges to its licensing facts (E 81 1 70, E 81 1 71),
the exact structure revise_on_contradict scans.

KB-B1 (no stale guide re-fire): PASS 8/8.
ev_act after resolution + subject re-presentation returned 0 on all 8
R-events (R1E1-E4: 0,0,0,0; R2E1-E4: 0,0,0,0). TNN-2 returned 30.

KB-B2 (twice-corrected value): PASS 8/8.
Final query on the contradicted fact key after the second contradiction:
C1D1-D4: 300,301,302,303 (expect 300-303); C2D1-D4: 620,621,622,623
(expect 620-623). Re-derivation queries between the contradictions
returned the once-corrected values (8/8).

KB-B3 (revert supersession): PASS 4/4.
C1R1: FA node 71 = (52501,5202,400), carries type-3 self-edge after the
contradiction and still at end; live node 86 = (52501,5202,400), a
different node, holds 400; final query 400. C1R2: FA 88 superseded,
live 103 fresh, query 401. C2R1: FA 70 superseded, live 86 fresh, query
53501. C2R2: FA 87 superseded, live 103 fresh, query 53510. In all four,
the stale taught node keeps its CON edge and the returned value is
sourced from a freshly taught node, never from the stale node.

KB-R1 (retention): PASS 12/12.
All 12 collateral probes correct after interference (6 chain facts,
3 MAP keys, 1 unrelated fact, 1 unrelated MAP key, 1 re-probe).
Supplementary: zero MAP-CON edges in the retention world (no spurious
supersession under interference).

KB-G1 (architecture accounting): PASS.
Independently re-verified against the SHA-256-verified base
(a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd):
added cognition lines 35 (<= 40), deleted cognition lines 57 (>= 40),
net -22 (<= 0); test-only delta (t_t2_revise rewrite, 9 added / 16
deleted) excluded per the prereg qualifier. t2_revise_graph and
t2_kill_edge fully removed. No new modes, bridges, routers, or handlers;
no core-ISA additions (only supersede and resolve_uncertainty, using
COMPARE and LINK); none of the forbidden protected semantic operations
present. No time/clock/random/seed/PID reads in the added lines.

KB-D1 (determinism): PASS.
3/3 byte-identical full stdouts (behavioral lines + canonical full state
dump) per sealed world:
- r1: 8d6ee6d85de33c9753b4eb1dae7b367596034ccc82925d1677a5fb5c481e8706 (x3)
- r2: 2be933bd7b185b6ff1d312670b153fbdcaa6d9137f53198be5233ad619625bae (x3)
- c1: 1b4a7f0a26a52b3a2e50afc849718f32d4cca9e866d1eaa11ce340f2c8b2b05b (x3)
- c2: e7e39734f78382f2ff8c2f97009f8ab200202525f45d3454aeab7c8f5ccccc38 (x3)
- ret: ad3e7e5408afa2f3596f3207e2fdaf3a81ea7cd91d45c8bd4d5d587ea25c6d16 (x3)

KB-P1 (process): PASS.
Adversary PATH was $HOME/safebin for the entire run; `which python3`
and `which python` print nothing. Shell invoked only the pinned znc,
built binaries, git read-only ops, and file moves/copies. Zero
forbidden-executable invocations.

Negative controls: NC-1 no (8 guide-CON edges, not 0); NC-2 no
(behavioral passes coincide with white-box edges); NC-3 no (no stale
guide fired post-resolution; superseded MAPs are never consulted on the
query path); NC-4 no; NC-5 no; NC-6 no (worlds materially different,
disjoint 51xxx-54xxx ranges, no FW1-FW9 or 1421pdt trivial variants);
NC-7 no (base hash matches; implementation artifacts dated after the
57aac4b81 freeze commit; no world leak to the builder).

## Verdict: H5 ADVANCES

All nine frozen bars pass. No bar fails; no battery-level void condition
fires. H5 advances past this wave per the prereg section 10 verdict
rules.

## Supplementary adversary observations (non-bar, recorded honestly)

S1. The prereg 3.6 re-derivation story does not occur for MAP keys. A
post-probe bridge-key query (C1S: 100, C2S: 900) returns the stale taught
value via promote_graph's shadowing exact-hit fact: because the shadow
fact is never contradicted, the key is never a miss, so the trial loop
never re-derives and no fresh MAP is promoted for that key. The
superseded MAP is never consulted (activate reads tag-1 facts only), so
this is not NC-3, but it bounds the 3.6 claim: H5 unpromotes stale MAPs
without re-deriving replacements on MAP keys. Worth carrying into TNN-3.

S2. KB-B2's fact-key query is recency-echo-passable (the expected value
equals the most recent observation), the same miscalibration the 1421pdt
triviality review found in M3-W2. The bar passes as frozen; the causal
weight in this battery is carried by KB-W2, which a parrot cannot pass.

S3. Positive control on ev_act: in the first sealed version (before the
documented context-flush fix), ev_act returned 30 when a still-live
guide's subject sat in the 4-slot context window. ev_act correctly fires
live guides and correctly returns 0 for resolved ones; the 8/8 zeros are
due to supersession, not a dead selector.

S4. KB-B3's "never the stale taught value" was read as node-sourced (the
value must not come from the superseded stale node), per the prereg 3.8
mechanism story, which is entirely about nodes. The re-observed value
returned from a freshly taught node is correct behavior; the white-box
node-identity checks (FA superseded, live node id != FA id) disambiguate
the value coincidence. Recorded here so the reading is auditable.
