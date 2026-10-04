# SEALED_EVAL_H5R: sealed evaluation verdict (independent adversary)

Lane TNN3H5R, wave-20261001-2021pdt. Adversary: TNN3H5R-ADV (independent of
the H5R builder; no shared working state). Frozen binary: tnn3_h5r.bin,
SHA-256 59c7648287d1e8a1ae6ea851696aae38b3991e537679fc9fc2d4bd38dded0f9b
(verified before any world ran; the adversary independently rebuilt the
committed source to the identical hash). Sealed worlds: TNN3H5R/sealed/
(w_c1, w_c2, w_r1, w_r2, w_ret), designed post-freeze from PREREG_H5R.md
alone; pre-run SHA-256 recorded in SEALED_H5R.md. Pure Zag throughout;
safebin PATH; `which python3` printed nothing at lane startup (NAMECHECK_ADV.md
Step 0); zero forbidden-executable invocations.

Note on smoke keys: the builder's smoke key ranges (7xxx/8xxx) are
mentioned in IMPLEMENTATION_H5R.md, which the task authorized as evidence.
The sealed worlds use disjoint ranges (61xxx-65xxx, 71xxx-72xxx) and no
smoke values; nothing from the builder's smoke worlds is reused.

## KB-S1 (substrate gate, pre-run): PASS

Verified on the committed diff (830f95ab7) before any sealed world ran.
Base file SHA-256 f83571a0285fa99f0b184a2773ebfb3e74cdc80c9c67e3fa98a46e91a0857706
matches the frozen record. The diff contains BOTH hunks: the activate
tag-20 admission hunk (lines 153-157, tag-20 alternative keyed on
(f8,f4)) and the promote_graph deletion hunk (line 551,
`ev_teach_in(W,s,r,ans);` removed). The committed H5R source contains zero
occurrences of the shadow-fact teaching call. NC-0R does not fire; the
battery ran.

## KB-W0 (white-box, PRIMARY, applied first): 36/36 PASS

Across all 36 MAP-key probe snapshots (SNAP-IN before every MAP-key probe
in w_c1 and w_c2): zero live tag-1 facts on (s_m,r_m) in all 36 snapshots
(36 SNAP-IN lines, all t1live=0). Every probe returned the f28 of the
single live tag-20 MAP with (f8,f4)==(s_m,r_m): 36/36 "W0 ok" (livemap=1,
f28==returned value on every probe). Zero W0-FAIL, VAL-FAIL, or FRESH-FAIL
lines. The shadow fact is gone; the original sin that killed H5 is
corrected. NC-2R does not fire.

## Guide half (R battery)

- KB-W1R: 8/8 PASS. Exactly 4 guide-CON self-edges in w_r1 and exactly 4
  in w_r2, on guide-class nodes (tag 1, f24==-999, type-1 edge to tag-30).
- KB-S1R: PASS. w_r1 shows exactly 1 live guide-class node with no CON
  edge (the never-resolved control on 61109).
- KB-S2R: PASS. w_r2's wrong-key OBSERVE (62109,6209) produced 0 new
  guide-CON edges (0->0) and left all 4 guides live (4->4).
- KB-B1R: 8/8 PASS. ev_act returned 0 on all 8 resolution events after
  OBSERVE resolution and subject re-presentation (context hygiene per the
  H5 Attack 4 precedent: 4-distractor flush before the resolution
  sequence).

## MAP half (C battery)

- KB-B2R: 16/16 PASS. On all 8 double-contradiction probes, the
  post-first-contradiction MAP-key probe returned c1 and the
  post-second-contradiction probe returned c2, each via a fresh MAP
  (strictly increasing node ids).
- KB-B3R: 4/4 PASS. On all 4 revert probes, the post-revert MAP-key probe
  returned c0; the c1-answering MAP carries a CON self-edge at end; the
  answering node is a fresh MAP (id strictly greater than both superseded
  MAPs) with f28==c0.
- KB-W2R: 8/12 FAIL. The 8 double-contradiction probes pass cleanly
  (exactly 2 superseded tag-20 MAPs with CON self-edges, exactly 1 live
  MAP with f28==final expected value, all DEP targets live tag-1 facts).
  All 4 revert probes fail the DEP clause: the post-revert fresh MAP
  carries a DEP (type-1) edge to the SUPERSEDED original fact node.

Killing evidence (identical on C1R1, C1R2, C2R1, C2R2; C1R1 quoted):
live MAP id=298, f28=63501 (=c0, the reverted value); DEP edges to node
254 (tag-1, live: the never-contradicted chain fact) and node 255 (tag-1,
SUPERSEDED: the original (b,RF2,c0) fact killed by the first
contradiction). The live reverted fact (the node actually licensing the
c0 answer) has no DEP edge from the MAP.

Root cause (white-box, traced in the frozen trial loop): t2_trial tries
chain candidates in BFS/node-id order and promote_graph anchors DEP edges
to the accepted candidate's licensing facts. In the revert case the
candidate via the original (superseded, lowest-node-id) fact outputs c0,
which equals the reverted expected value, so it verifies first and the
fresh MAP's provenance anchors to the dead fact instead of the live
reverted fact. This is a property of the frozen trial loop's
first-verifying-candidate ordering, not of the H5R substrate hunks.

Consequence (white-box analysis): revise_on_contradict locates stale MAPs
via DEP edges to the contradicted fact. The revert MAP has no DEP edge to
its live licensing fact, so a future contradiction of that live fact would
not supersede the MAP; the MAP would keep answering via the MAP read
path. The revision chain is broken for revert-promoted MAPs. The bar
caught a genuine flaw, not a technicality.

- NC-1R: not fired (MAP-CON = 12 in w_c1, 12 in w_c2; the transition fires
  on MAPs).
- NC-3R: not fired (no FRESH-FAIL; every post-contradiction probe promoted
  a fresh MAP; no stale value was returned without fresh promotion).

## Retention

- KB-R1R: 12/12 PASS. All 12 collateral re-queries correct after
  interference (extra teaches, a fact-level contradict-and-revert cycle,
  two unresolved miss-queries).
- Supplementary: zero MAP-CON edges under interference (MAPCON-ALL=0).
  PASS as logged.

## Architecture and process

- KB-G1R: PASS. Incremental committed diff: 5 added cognition lines
  (non-blank, non-comment; budget <=15), 3 removed. No new modes,
  bridges, routers, or handlers. No core-ISA additions (only existing
  field reads, COMPARE, edge/link ops). None of the forbidden protected
  semantic operations. No time/clock/random reads. Cumulative vs the TNN-2
  base: 1573 vs 1591 lines, net negative (consistent with the builder's
  reported net -20 cognition lines). NC-4R does not fire.
- KB-D1: PASS. 3/3 byte-identical full-stdout runs per world:
  - w_c1: c37ceb6e2046403f058c4f79fe7347a23715bcb0e76fa31bf9c1595d12e6b4aa (x3)
  - w_c2: 43a5dea7ce9484901eb59be24501d23815259a05ef464a0c202ab245b8dd316e (x3)
  - w_r1: ae9a2fa636868a22fe53376d3142fd4a7b929d61cfb63d3fc95cdf8f5c13db49 (x3)
  - w_r2: bf388437b9677d7a450794698e2081cb7dc8b6c8d8e3862ff5bd0852be00fd8e (x3)
  - w_ret: 84191902c0c1adc8ca04ad96db2ba5e2029539c0afb3e53204eb50d2ba56479b (x3)
  NC-5R does not fire.
- KB-P1: PASS. Zero forbidden-executable invocations; safebin PATH for
  every command; `which python3` empty at startup and the toolchain guard
  recorded in NAMECHECK_ADV.md Step 0.
- NC-6R: not fired (worlds documented non-trivial in SEALED_H5R.md;
  disjoint ranges; MAP-key re-derivation design).
- NC-7R: not fired. Commit order: prereg 67ed888e4 (2026-10-02 04:14:04
  UTC) strictly before implementation 830f95ab7 (04:19:13 UTC) strictly
  before sealed world creation (04:27+ UTC). Base copy SHA-256 matches the
  frozen record. The sealed directory did not exist at builder time; the
  builder attested no read path to it.

## Verdict: H5R is KILLED

Killing bar: KB-W2R (8/12 < 12/12). Per the frozen verdict rules a failed
frozen bar is terminal for this wave; no re-tune, no amend-and-promote. A
killed H5R may return only via a fresh prereg plus fresh sealed worlds.

What the evidence says, precisely: the H5R substrate change itself works.
KB-W0 36/36 proves the original sin is corrected (no shadow fact on any
MAP key; every MAP-key probe answered by the single live tag-20 MAP), and
KB-B2R 16/16 plus KB-B3R 4/4 prove MAP supersession now causes genuine
behavioral revision with fresh MAP promotion. H5R is killed not for the
original sin but for a narrower flaw the W2R bar was designed to catch:
on revert probes, the frozen trial loop's first-verifying-candidate
ordering promotes the fresh MAP with provenance anchored to the
superseded original fact rather than the live reverted fact, breaking the
DEP-based revision chain for those MAPs. The guide half (KB-W1R, KB-S1R,
KB-S2R, KB-B1R) passes fully; the substrate change does not regress it.
